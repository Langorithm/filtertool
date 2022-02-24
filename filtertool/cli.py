"""Collection of functions handling the interaction with the Command Line"""
import argparse
import errno
import sys
import argparse as ap
import filtertool.filter_class as filter_class
import filtertool.exceptions as exceptions
from filtertool.__init__ import __app_name__


def parse_arguments():
    parser = ap.ArgumentParser()
    parser.prog = __app_name__
    parser.add_argument("input", help="The image file to be modified.")
    parser.add_argument("filters", nargs="*", help="The filters to be applied and their respective arguments.")

    # CLI Options
    parser.add_argument("-o", "--output", help="name of the resulting image file, with file extension.")
    parser.add_argument("-d", "--display", action="store_true", help="displays the resulting image")
    parser.add_argument("-D", "--display-only", action="store_true",
                        help="displays the resulting image but disables saving it to disk")
    # parser.add_argument("-v", "--verbose", action="store_true")
    # TODO option: verbosity

    parser.formatter_class = argparse.RawTextHelpFormatter
    parser.epilog = _enhance_help_text(filter_class.filters)
    return parser.parse_args()


def gen_filter_sequence(filter_args):
    """Parses the list of CLI arguments, fetching the filter objects
    and associates the corresponding CLI to be passed to the filter's effect"""
    filter_seq = _gen_filter_seq_recursive(filter_args, filter_class.filters)

    return filter_seq


def _gen_filter_seq_recursive(filter_args, filters):
    """Heavy lifting for the gen_filter_sequence.
    Added as an aux function because recursion requires the filter objects to be passed."""
    # Base case
    if not filter_args:
        return []
    # Recursive case
    else:
        filter_name = filter_args[0]

        _check_filter_name(filter_name, filters)

        f = [f for f in filters if f.name == filter_name.lower()][0]

        f_arg_num = len(f.get_params())
        args = filter_args[1:1 + f_arg_num]
        params = _extract_params(f, args)
        # Recursion
        return [(f, params)] + _gen_filter_seq_recursive(filter_args[1 + f_arg_num:], filters)


def _extract_params(_filter, args):
    """Given a filter and the names of its arguments,
    convert from string to expected type and validate correctness of parameters.

    Return the list of parameters to be used when applying
    filter's effects."""
    expected_params = _filter.get_params()
    try:
        if len(expected_params) != len(args):
            raise ValueError
    except ValueError:
        print("\nError!\nMissing parameters.\n")
        sys.exit(errno.EINVAL)

    params = {}
    for i in range(len(args)):
        expected_param = expected_params[i]
        arg = args[i]

        try:
            param = _typecast_param(arg, expected_param)
            _validate_param(param, expected_param)
        except ValueError:
            sys.exit(errno.EINVAL)

        params[expected_param.name] = param

    return params


# ----- Usage and Help text functions ------
def _enhance_help_text(filters):
    text = "\nfilters:\n"
    for _filter in filters:
        text += f"  {_filter.name}\t\t[{_filter.description}]"
        params = _filter.get_params()
        for param in params:
            text += f"\n\t{param.name}: {param.description}"
        text += "\n \n \n"

    return text

# ----- Functions that check for exceptions arisen from mistakes in the CLI ------


def _typecast_param(param, expected_param):
    """Tries converting parsed parameter from string to what is needed for the filter's effect"""
    try:
        filter_param = expected_param.param_type(param)
    except ValueError as e:
        print("Error!")
        print(f"Expected '{expected_param.name}': {param.upper()} to be a '{expected_param.param_type}'.\n")
        raise e
    else:
        return filter_param


def _validate_param(param, expected_param):
    """Makes sure parameter complies with its preconditions"""
    try:
        if not expected_param.validity_func(param):
            raise exceptions.ConditionError(param=param, condition=expected_param.validity_str)
    except exceptions.ConditionError as e:
        print(e)
        raise e


def _check_filter_name(name, filters):
    """Verifies filter with given name is present in filter collection"""
    try:
        if not name.lower() in [f.name for f in filters]:
            raise ValueError(f"'{name.upper()}' is not a filter.")
    except ValueError as e:
        print("\nError!\n", e, "\n")
        raise e

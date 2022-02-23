"""Collection of functions handling the interaction with the Command Line"""
import sys
import argparse as ap
import filtertool.filter_class as filter_class
import filtertool.exceptions as exceptions


def parse_arguments():
    parser = ap.ArgumentParser()
    parser.add_argument("input", help="The image file to be modified.")
    parser.add_argument("filters", nargs="*", help="The filters to be applied and their respective arguments.")
    parser.add_argument("--output", "-o", help="name of the resulting image file, with file extension.")
    # TODO option: verbosity
    # TODO option: show image after processing
    # TODO customize the Help option so that it automatically explains available filters.
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
    assert (len(expected_params) == len(args))

    params = {}
    for i in range(len(args)):
        expected_param = expected_params[i]
        arg = args[i]

        param = _typecast_param(arg, expected_param)
        _validate_param(param, expected_param)

        params[expected_param.name] = param

    return params


# ----- Functions that check for exceptions arisen from mistakes in the CLI ------

def _typecast_param(param, expected_param):
    """Tries converting parsed parameter from string to what is needed for the filter's effect"""
    try:
        filter_param = expected_param.param_type(param)
    except ValueError:
        print("Error!")
        print(f"Expected '{expected_param.name}':{param.upper()} to be a '{expected_param.param_type}'.\n")
        sys.exit(1)
    else:
        return filter_param


def _validate_param(param, expected_param):
    """Makes sure parameter complies with its preconditions"""
    try:
        if not expected_param.validity_func(param):
            raise exceptions.ConditionError(param=param, condition=expected_param.validity_str)
    except exceptions.ConditionError as e:
        print(e)
        sys.exit(1)


def _check_filter_name(name, filters):
    """Verifies filter with given name is present in filter collection"""
    try:
        if not name.lower() in [f.name for f in filters]:
            raise Exception(f"'{name.upper()}' is not a filter.")
    except Exception as e:
        print("Error!\n", e, "\n")
        sys.exit(1)


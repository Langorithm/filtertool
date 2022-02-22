"""Collection of functions handling the interaction with the Command Line"""

import argparse as ap
import filtertool.filter_class as filter_class


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

        # TODO check filter names
        f = [f for f in filters if f.name == filter_name.lower()][0]

        f_arg_num = len(f.get_params())
        args = filter_args[1:1 + f_arg_num]
        params = _extract_params(f, args)
        # Recursion
        return [(f, params)] + _gen_filter_seq_recursive(filter_args[1 + f_arg_num:], filters)


def _extract_params(_filter, args):
    """Given a filter and the names of its arguments,
    convert from string to correct type and validate correctness.
    Return the list of parameters to be used in the application of the filter"""
    expected_params = _filter.get_params()
    assert (len(expected_params) == len(args))

    params = {}
    for i in range(len(args)):
        expected_param = expected_params[i]
        arg = args[i]

        # TODO validate parameters and types
        param = expected_param.param_type(arg)
        params[expected_param.name] = param

    return params

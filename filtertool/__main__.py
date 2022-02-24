import errno
import sys

from PIL import Image
import filtertool.cli as cli
import filtertool.output as output


if __name__ == '__main__':
    args = cli.parse_arguments()

    input_filename = args.input
    output_filename = args.output
    filters = cli.gen_filter_sequence(args.filters)

    try:
        image = Image.open(input_filename)
    except FileNotFoundError:
        print(f"No such file: {input_filename}")
        sys.exit(errno.ENOENT)

    for _filter, params in filters:
        image = _filter.apply(image, params)

    output.output_image(image, args, output_filename, filters)

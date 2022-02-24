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
        with Image.open(input_filename) as image:
            for _filter, params in filters:
                image = _filter.apply(image, params)

            output.output_image(image, args, output_filename, filters)

    except IOError as e:
        print(e)
        sys.exit(errno.EIO)




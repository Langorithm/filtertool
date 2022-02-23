import sys

from PIL import Image
import filtertool.cli as cli

if __name__ == '__main__':
    args = cli.parse_arguments()

    input_filename = args.input
    output_filename = args.output
    filters = cli.gen_filter_sequence(args.filters)

    try:
        image = Image.open(input_filename)
    except FileNotFoundError:
        print(f"No such file: {input_filename}")
        sys.exit(1)

    for _filter, params in filters:
        image = _filter.apply(image, params)

    # TODO allow no output file name in args
    image.save(output_filename)
    image.show()

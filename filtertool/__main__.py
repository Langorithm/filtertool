from PIL import Image
import filtertool.cli as cli

if __name__ == '__main__':
    args = cli.parse_arguments()

    input_filename = args.input
    output_filename = args.output
    filters = cli.gen_filter_sequence(args.filters)

    image = Image.open(input_filename)

    for _filter, params in filters:
        image = _filter.apply(image, params)

    # TODO allow no output file name in args
    image.save(output_filename)

"""File storing functions dealing with the resulting files"""
import os.path


def output_image(image, args, output_name, filters):
    display = args.display_only or args.display
    save = not args.display_only

    if display:
        image.show()
    if save:
        if output_name is None:
            output_name = _default_image_filename(args.input, filters)

        image.save(output_name)


def _default_image_filename(original_name, filters):
    result, _, filetype = original_name.rpartition(".")

    for _filter, args in filters:
        result += "_" + _filter.name
    result += "." + filetype

    return result


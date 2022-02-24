"""File storing functions dealing with the resulting files"""


def output_image(image, args, output_name):
    display = args.display_only or args.display
    save = not args.display_only

    if display:
        image.show()
    if save:
        image.save(output_name)


def _default_image_filename():
    # todo
    pass

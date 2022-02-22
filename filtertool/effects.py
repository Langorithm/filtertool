"""File to store the functions which handle the actual image modification"""
from PIL import Image
from PIL import ImageChops


def grayscale_fx(image, **_):
    """Turn an image into shades of gray via gray-scaling.

    Used keyword arguments: None

    [Does NOT change the image's mode (And RGB image stays RGB, so on)]
    """
    # Preserve the image's mode
    prev_mode = image.mode
    image = image.convert("LA")
    image = image.convert(prev_mode)
    return image


def rotate_fx(image, **kwargs):
    """Rotate an image N degrees counterclockwise. Currently, does not resize the image to fit.

    Used keyword arguments:
        - Degrees (type: int)"""
    deg = kwargs["Degrees"]

    image = image.rotate(deg)

    return image


def overlay_fx(image, **kwargs):
    """Composite a second image into the first by using the Overlay blending mode algorithm
    Used keyword arguments:
        - Image2_filename (type: str)
    [Does NOT change the image's mode (And RGB image stays RGB, so on)]
    """
    img1 = image
    img2 = Image.open(kwargs["Image2_filename"])

    # Prepare img2 to be blended
    result = _overlay_aux(img1, img2)

    return result


def _overlay_aux(image1, image2):
    """
    Because the Overlay function from PIL requires the images
    to be the same size, the overlaying (top) image needs to be
    padded to match the size of the bottom image.

    Additionally, the Overlay algorithm doesn't account for
    transparency, so we need to put the top image in a gray
    background.
    """
    im1_prev_mode = image1.mode
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")
    gray = (127,)*4

    top_image = Image.new("RGBA", image1.size, gray)
    top_image.paste(image2, (0, 0), image2)  # todo choose coordinates

    result = ImageChops.overlay(image1, top_image)
    result = result.convert(im1_prev_mode)
    return result


def memeify_fx():
    pass  # TODO

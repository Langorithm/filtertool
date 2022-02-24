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
    """Rotate an image N degrees counter-clockwise. Currently, does not resize the image to fit.

    Used keyword arguments:
        - DEGREES (type: int)"""
    deg = kwargs["DEGREES"]

    image = image.rotate(deg)

    return image


def overlay_fx(image, **kwargs):
    """Composite a second image into the first by using the Overlay blending mode algorithm
    Used keyword arguments:
        - IMG_2 (type: str)
        - X_PLACE (type: float)
        - Y_PLACE (type: float)
    [Does NOT change the image's mode (An RGB image stays RGB, so on)]
    """
    img1 = image
    img2 = Image.open(kwargs["IMG_2"])
    place = kwargs["X_PLACE"], kwargs["Y_PLACE"]
    # anchor = kwargs["Horizontal Anchor"], kwargs["Vertical Anchor"]
    # Prepare img2 to be blended
    result = _overlay_aux(img1, img2, place)

    return result


def _overlay_aux(image1, image2, placement, anchor=(.5, .5)):
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

    gray_padding = Image.new("RGBA", image1.size, "gray")
    placement = _calculate_placement(
        gray_padding, image2,
        placement, anchor)
    gray_padding.paste(image2, placement, image2)
    top_image = gray_padding

    result = ImageChops.overlay(image1, top_image)
    result = result.convert(im1_prev_mode)
    return result


def _calculate_placement(im1, im2, placement, anchor=(.5, .5)):
    """Given a pair of coordinates (placement and anchor) find out at what pixel position of Image1
    must one put the top left corner of Image2 so that the Anchor Point of Image2 matches with the Placement
    Point in Image1.
    As Placement and Anchor are numbers in the range [0,1], representing the relative
    width and height of Image 1 as a unit square, this function is necessary to perform
    the Paste operation with absolute pixel coordinates.
    """
    x_1, y_1 = im1.size
    x_2, y_2 = im2.size
    place_x, place_y = placement
    anchor_x, anchor_y = anchor     # .5, .5 center of the second image

    center_x_post = place_x * x_1
    center_y_post = place_y * y_1
    center_x_pre = int(x_2 * anchor_x)
    center_y_pre = int(y_2 * anchor_y)
    left_top_corner_placement = int(center_x_post - center_x_pre), int(center_y_post - center_y_pre)
    return left_top_corner_placement


def memeify_fx():
    pass  # TODO

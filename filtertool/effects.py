"""File to store the functions which handle the actual image modification"""
import math

from PIL import Image, ImageChops, ImageDraw, ImageFont


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


def memeify_fx(image, **kwargs):
    """
    Calculate the optimal font size for the upper and lower text to fit in the image in a single line.
    Then, draw those words in Impact, of the found size.
    Used parameters:
        DOWN_TEXT (type: str)
        TOP_TEXT (type: str)
    """
    down_text = kwargs["DOWN_TEXT"]
    top_text = kwargs["TOP_TEXT"]

    size_x, size_y = image.size
    text_boundary = size_x * 0.8, size_y * 0.1  # numbers experimentally checked to produce good pictures

    draw_context = ImageDraw.Draw(image)

    if len(top_text) > 0:
        top_placement = size_x * .5, size_y * 0.05
        font = _find_perfect_fit(image, top_placement, "Impact", top_text, text_boundary)
        draw_context.text(top_placement, text=top_text, font=font, anchor="mt", stroke_width=2, stroke_fill="black")
    if len(down_text) > 0:
        bottom_placement = size_x * .5, size_y * (1-0.05)
        font = _find_perfect_fit(image, bottom_placement, "Impact", down_text, text_boundary)
        draw_context.text(bottom_placement, text=down_text, font=font, anchor="mb", stroke_width=2, stroke_fill="black")

    return image


def _find_perfect_fit(image, xy, font_name, text, limits):
    """
    :param image: Image to be paste the image in. Passed for size reference and to create the drawing context.
    :param xy: Absolute pixel position where the text will be pasted, required for the measuring function (textbbox)
    :param font_name: Name of the font to be loaded.
    :param text: Text to measure in the given font, in different sizes.
    :param limits: Max horizontal and vertical sizes for the text. Used in calculating the optimal fit.
    :return: The resized font.
    """
    height, width = image.size
    estimated_text_size = 1 # int(math.sqrt(height * width))

    font = ImageFont.truetype(font_name, estimated_text_size)
    context = ImageDraw.Draw(image)

    text_fits = _does_text_fit(context, xy, text, font, limits)
    prev_text_fit = text_fits
    perfect_fit = False
    font_size = font.size

    while not perfect_fit:
        if text_fits:
            font_size  += 10
        else:
            font_size -= 10

        font = ImageFont.truetype(font_name, font_size)
        text_fits = _does_text_fit(context, xy, text, font, limits)
        perfect_fit = text_fits ^ prev_text_fit

    return font


def _does_text_fit(context, xy, text, font, limits):
    """Aids in checking if the current text and font combination fit inside a box of the given limits"""
    box = context.textbbox(xy, text, font, "mt", align="center", stroke_width=2)

    box_x0, box_y0, box_x1, box_y1 = box
    box_width  = box_x1 - box_x0
    box_height = box_y1 - box_y0
    limit_x, limit_y = limits

    return box_width <= limit_x and box_height <= limit_y

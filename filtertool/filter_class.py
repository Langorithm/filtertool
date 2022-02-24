"""
Represents an image filter, including its effect on files,
the type/requirements of its parameters.

"""
from typing import Any, NamedTuple, Callable
import filtertool.effects as effects


class Param(NamedTuple):
    name:           str
    description:    str
    param_type:     type
    validity_func:  Callable[[Any], bool]
    validity_str:   str


class Filter:
    """Filter docstring TODO"""
    # TODO verbosity description
    def __init__(self, name, help_text, effect, params=None):
        if params is None:
            params = []
        self.name = name.lower()
        self.description = help_text
        self._params = params
        self._effect = effect
        # TODO multiple names (gs = grayscale, rot = rotate, etc)

    def __repr__(self): return f"filter {self.name}, params: {self._params}"

    def add_param(self, param):
        """docstring TODO"""
        self._params.append(param)

    def get_params(self):
        return self._params

    def set_effect(self, effect):
        """Set the function this filter will apply to images"""
        self._effect = effect

    def apply(self, image, kwargs):
        """Apply the effect of the filter into the image"""
        return self._effect(image, **kwargs)

# ---------------------------------
# ------- Filter Instances --------
# ---------------------------------


filters = []

# --- GRAYSCALE ---
filter_gs = Filter(
    "grayscale",
    "Turn image black and white.",
    effects.grayscale_fx)
filters.append(filter_gs)

# --- ROTATE ---
param_rot_degrees = Param(
    name="DEGREES",
    description="Angle to rotate image by.",
    param_type=float,
    validity_func=lambda _: True,
    validity_str="")
filter_rot = Filter(
    name="rotate",
    help_text="Rotate the Image X degrees counter-clockwise.",
    effect=effects.rotate_fx,
    params=[param_rot_degrees])
filters.append(filter_rot)


# --- OVERLAY ---

# TODO Type Param has outgrown being a Named Tuple and should be its own class to avoid code duplication
param_overlay_place_x = Param(
    name="X_PLACE",
    description="Where to center the top image: from 0 (leftmost) to 1 (rightmost)",
    param_type=float,
    validity_func=lambda place_x: 0 <= place_x <= 1,
    validity_str=f"Invalid placement coordinate.\t 0 ≤ X ≤ 1"
)
param_overlay_place_y = Param(
    name="Y_PLACE",
    description="Where to center the top image: from 0 (top) to 1 (bottom)",
    param_type=float,
    validity_func=lambda place_x: 0 <= place_x <= 1,
    validity_str=f"Invalid placement coordinate.\t 0 ≤ Y ≤ 1"
)

supported_formats = ".png"
param_overlay_img2 = Param(
    name="IMG_2",
    description="Path to top image. Must be a PNG file.",
    param_type=str,
    validity_func=lambda filename: filename.lower().endswith(supported_formats),
    validity_str=f"Invalid file format.\t [Supported formats: {' '.join(supported_formats)}]")

filter_overlay = Filter(
    "overlay",
    "Blends a PNG image into the source image.",
    effects.overlay_fx,
    [param_overlay_img2,
     param_overlay_place_x, param_overlay_place_y]
    # param_overlay_anchor_x, param_overlay_anchor_y]
)
filters.append(filter_overlay)


# Deactivated code
"""
param_overlay_anchor_x = Param(
    name="Horizontal Anchor",
    param_type=float,
    validity_func=lambda anchor_x: 0 <= anchor_x <= 1,
    validity_str=f"Invalid anchor coordinate.\t 0 ≤ X ≤ 1"
)
param_overlay_anchor_y = Param(
    name="Vertical Anchor",
    param_type=float,
    validity_func=lambda anchor_y: 0 <= anchor_y <= 1,
    validity_str=f"Invalid anchor coordinate.\t 0 ≤ Y ≤ 1"
)
"""
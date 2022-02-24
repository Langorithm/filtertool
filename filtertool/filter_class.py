"""
Represents an image filter, including its effect on files,
the type/requirements of its parameters.

"""
from typing import Any, NamedTuple, Callable
import filtertool.effects as effects


class Param(NamedTuple):
    name:           str
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


# ------- Filter Instances --------

filters = set()

filter_gs = Filter(
    "grayscale",
    "Turn image black and white.",
    effects.grayscale_fx)
filters.add(filter_gs)

param_rot_degrees = Param(
    name="Degrees",
    param_type=int,
    validity_func=lambda n: n <= 360,
    validity_str="n<=360")
filter_rot = Filter(
    name="rotate",
    help_text="Rotate the Image N degrees clockwise.",
    effect=effects.rotate_fx,
    params=[param_rot_degrees])
filters.add(filter_rot)

supported_formats = ".png"
param_overlay_img2 = Param(
    name="Image2_filename",
    param_type=str,
    validity_func=lambda filename: filename.lower().endswith(supported_formats),
    validity_str=f"Invalid file format.\t [Supported formats: {' '.join(supported_formats)}]")
# TODO placing
filter_overlay = Filter(
    "overlay",
    "Blends a second image into the first.",
    effects.overlay_fx,
    [param_overlay_img2]
)
filters.add(filter_overlay)

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
    def __init__(self, name, description):
        self.name = name.lower()
        self.description = description
        self._params = []
        self._effect = None
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

gs = Filter("grayscale", "Turn image black and white.")
gs.set_effect(effects.grayscale_fx)
filters.add(gs)

rot = Filter("rotate", "Rotate the Image N degrees clockwise.")
degrees = Param(name="Degrees", param_type=int, validity_func=lambda n: n <= 360, validity_str="n<=360")
rot.add_param(degrees)
rot.set_effect(effects.rotate_fx)
filters.add(rot)

overlay = Filter("overlay", "Blends a second image into the first.")
img2 = Param(name="Image2_filename", param_type=str, validity_func=lambda: True, validity_str="")
# TODO placing
overlay.add_param(img2)
overlay.set_effect(effects.overlay_fx)
filters.add(overlay)

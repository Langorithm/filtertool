"""
Represents an image filter, including its effect on files,
the type/requirements of its parameters.

"""

from typing import Any, NamedTuple, Callable


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


# ------- effects functions --------
# TODO detail effect function specifications

def grayscale_fx(image, **_):
    print("The image has turned gray")  # TODO add actual functionality
    return image


# ------- Filter Instances --------

filters = set()

gs = Filter("grayscale", "Turn image black and white.")
gs.set_effect(grayscale_fx)
filters.add(gs)

from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Param:
    name:           str
    description:    str
    param_type:     type
    validity_func:  Callable[[Any], bool]
    validity_str:   str
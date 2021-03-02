from dataclasses import dataclass, field
from typing import Tuple

from numpy import ndarray
from magda.module import Module


@dataclass(frozen=True)
class Mask(Module.Interface):
    uid: str
    data: ndarray
    vrange: Tuple[float, float] = field(default=(0.0, 1.0))

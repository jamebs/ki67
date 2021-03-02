from dataclasses import dataclass

from numpy import ndarray
from magda.module import Module


@dataclass(frozen=True)
class Image(Module.Interface):
    uid: str
    data: ndarray

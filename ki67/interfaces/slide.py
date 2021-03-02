from dataclasses import dataclass, field
from pathlib import Path

from numpy import ndarray
from magda.module import Module


@dataclass(frozen=True)
class Slide(Module.Interface):
    uid: str
    filepath: Path
    image: ndarray
    x_offset: int = field(default=0)
    y_offset: int = field(default=0)

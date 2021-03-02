from dataclasses import dataclass

from pandas import DataFrame
from magda.module import Module


@dataclass(frozen=True)
class Markers(Module.Interface):
    uid: str
    markers: DataFrame

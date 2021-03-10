from dataclasses import dataclass

from pandas import DataFrame
from magda.module import Module


@dataclass(frozen=True)
class Labels(Module.Interface):
    uid: str
    fragments: DataFrame
    margin: int

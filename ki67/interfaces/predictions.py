from dataclasses import dataclass

from pandas import DataFrame
from magda.module import Module


@dataclass(frozen=True)
class Predictions(Module.Interface):
    uid: str
    predictions: DataFrame

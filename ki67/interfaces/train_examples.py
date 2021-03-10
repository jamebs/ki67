from dataclasses import dataclass

from numpy import ndarray
from magda.module import Module


@dataclass(frozen=True)
class TrainExamples(Module.Interface):
    uid: str
    data: ndarray
    labels: ndarray

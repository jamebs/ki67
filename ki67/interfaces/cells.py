from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict

from numpy import ndarray
from magda.module import Module


@dataclass(frozen=True)
class Cells(Module.Interface):
    class CellType(Enum):
        POSITIVE = 'positive'
        ALL = 'all'

    @dataclass(frozen=True)
    class CellsLabel:
        mask: ndarray
        labels: ndarray
        threshold: float

    uid: str
    data: Dict[CellType, CellsLabel]

    @classmethod
    def parse(cls, uid: str, data: Dict[str, ndarray]) -> Cells:
        return cls(
            uid=uid,
            data={
                cls.CellType.POSITIVE: cls.CellsLabel(
                    mask=data['p-mask'],
                    labels=data['p-labels'],
                    threshold=data['p-th'],
                ),
                cls.CellType.ALL: cls.CellsLabel(
                    mask=data['a-mask'],
                    labels=data['a-labels'],
                    threshold=data['a-th'],
                ),
            },
        )

    def serialize(self) -> Dict[str, ndarray]:
        positive = self.data[self.CellType.POSITIVE]
        all = self.data[self.CellType.ALL]
        return {
            'p-mask': positive.mask,
            'p-labels': positive.labels,
            'p-th': positive.threshold,
            'a-mask': all.mask,
            'a-labels': all.labels,
            'a-th': all.threshold,
        }

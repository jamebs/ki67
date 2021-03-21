from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Dict

from numpy import ndarray
from magda.module import Module


@dataclass(frozen=True)
class FuzzyCells(Module.Interface):
    class CellType(Enum):
        POSITIVE = 'positive'
        ALL = 'all'

    uid: str
    data: Dict[CellType, ndarray]

    @classmethod
    def parse(cls, uid: str, data: Dict[str, ndarray]) -> FuzzyCells:
        return cls(
            uid=uid,
            data={
                cls.CellType.POSITIVE: data['positive'],
                cls.CellType.ALL: data['all'],
            },
        )

    def serialize(self) -> Dict[str, ndarray]:
        positive = self.data[self.CellType.POSITIVE]
        all = self.data[self.CellType.ALL]
        return {
            'positive': positive,
            'all': all,
        }

from dataclasses import dataclass
from typing import Dict, Set

from magda.module import Module


@dataclass(frozen=True)
class Shards(Module.Interface):
    uid: str
    training: Dict[str, Set[str]]
    testing: Set[str]

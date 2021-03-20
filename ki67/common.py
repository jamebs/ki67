from dataclasses import dataclass, field
from typing import Optional


@dataclass(frozen=True)
class Request:
    uid: str


@dataclass(frozen=True)
class Shared:
    source: str
    target: str
    fragment: int
    experiments: Optional[str] = field(default=None)


@dataclass(frozen=True)
class Context:
    pass

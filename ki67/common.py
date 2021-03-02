from dataclasses import dataclass


@dataclass(frozen=True)
class Request:
    uid: str


@dataclass(frozen=True)
class Shared:
    source: str
    target: str
    stride: int


@dataclass(frozen=True)
class Context:
    pass

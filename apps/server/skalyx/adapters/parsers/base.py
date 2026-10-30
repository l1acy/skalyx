from dataclasses import dataclass
from typing import Protocol


@dataclass
class ParsedMetric:
    metric: str
    value: float | int | str
    unit: str | None = None


class Parser(Protocol):
    def parse(self, raw: bytes) -> list[ParsedMetric]:
        ...

__all__ = ('ParsedMetric', 'Parser',)

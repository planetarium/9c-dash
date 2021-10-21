from __future__ import annotations
import json

class Peer:
    def __init__(self, address: str, tip: int, difficulty: int):
        self._address = address
        self._tip = tip
        self._difficulty = difficulty
        return

    @property
    def address(self) -> str:
        return self._address

    @property
    def tip(self) -> int:
        return self._tip

    @property
    def difficulty(self) -> int:
        return self._difficulty

    @property
    def dead(self) -> bool:
        return self.tip < 0

    def to_dict(self) -> dict:
        return {
            "address": self.address,
            "tip": self.tip,
            "difficulty": self.difficulty,
        }

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, dict_: dict) -> Peer:
        return Peer(**dict_)

    @classmethod
    def raw_to_dict(cls, raw: str) -> dict:
        temp = raw.split(", ")
        return {
            "address": temp[0],
            "tip": int(temp[1]),
            "difficulty": int(temp[2]),
        }

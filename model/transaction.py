from __future__ import annotations
import json
import re

class Transaction:
    def __init__(self, id_: str, actions: list[str]):
        self._id = id_
        self._actions = actions
        return

    @property
    def id_(self) -> str:
        return self._id

    @property
    def actions(self) -> list[str]:
        return self._actions

    def to_dict(self) -> dict:
        return {
            "id_": self._id,
            "actions": self._actions,
        }

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def raw_to_dict(cls, raw) -> dict:
        return {
            "id_": raw["id"],
            "actions": [
                cls.extract_action_type(action_raw["inspection"])
                    for action_raw in raw["actions"]
            ]
        }

    @classmethod
    def from_dict(cls, dict_) -> Transaction:
        return Transaction(**dict_)

    @classmethod
    def extract_action_type(cls, inspection_raw) -> str:
        match = re.search(r"\"type_id\": \"(.+)\"", inspection_raw)
        if match:
            action_type = match[1]
            action_type = re.sub(r"[0-9]+$", "", action_type)
            return action_type
        else:
            return ""

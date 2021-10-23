from __future__ import annotations
import datetime
import json
from model.transaction import Transaction

class Block:
    def __init__(
        self,
        timestamp: float,
        index_: int,
        hash_: str,
        prev: str,
        difficulty: int,
        transactions: list[dict],
        miner: str
    ):
        self._timestamp = timestamp
        self._index = index_
        self._hash = hash_
        self._prev = prev
        self._difficulty = difficulty
        self._transactions = [
            Transaction.from_dict(transaction_dict)
                for transaction_dict in transactions
        ]
        self._miner = miner
        return

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def index_(self) -> int:
        return self._index

    @property
    def hash_(self) -> str:
        return self._hash

    @property
    def prev(self) -> str:
        return self._prev

    @property
    def difficulty(self) -> int:
        return self._difficulty

    @property
    def transactions(self) -> list[Transaction]:
        return self._transactions

    @property
    def miner(self) -> str:
        return self._miner

    def to_row(self) -> list:
        return [
            self.timestamp,
            self.index_,
            self.hash_,
            self.prev,
            self.difficulty,
            self.transactions,
            self.miner,
        ]

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "index_": self.index_,
            "hash_": self.hash_,
            "prev": self.prev,
            "difficulty": self.difficulty,
            "transactions": [
                transaction.to_dict() for transaction in self.transactions
            ],
            "miner": self.miner,
        }

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def raw_to_dict(cls, raw: dict) -> dict:
        return {
            "timestamp": cls.isoformat_to_timestamp(raw["timestamp"]),
            "index_": raw["index"],
            "hash_": raw["hash"],
            "prev": raw["previousBlock"]["hash"],
            "difficulty": raw["difficulty"],
            "transactions": [Transaction.raw_to_dict(transaction_raw)
                for transaction_raw in raw["transactions"]
            ],
            "miner": raw["miner"]
        }

    @classmethod
    def from_dict(cls, dictionary: dict) -> Block:
        return Block(**dictionary)

    @classmethod
    def from_row(cls, row: list) -> Block:
        return cls.from_dict({
            "timestamp": row[0],
            "index_": row[1],
            "hash_": row[2],
            "prev": row[3],
            "difficulty": row[4],
            "transactions": row[5],
            "miner": row[6],
        })

    @classmethod
    def isoformat_to_timestamp(cls, isoformat: str) -> float:
        precision = 26
        time_, timezone = isoformat.split("+")
        time_ = time_ + "0" * (precision - len(time_))
        return datetime.datetime.fromisoformat(time_ + "+" + timezone).timestamp()

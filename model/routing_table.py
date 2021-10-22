from __future__ import annotations
import datetime
import json
from model.peer import Peer

class RoutingTable:
    def __init__(
        self,
        timestamp: float,
        peers: list[str],
    ):
        self._timestamp = timestamp
        self._peers = [Peer.from_dict(peer) for peer in peers]
        self._local = self.peers[0]
        self._remotes = self.peers[1:]
        return

    @property
    def timestamp(self) -> float:
        return self._timestamp

    @property
    def peers(self) -> list[Peer]:
        return self._peers

    @property
    def local(self) -> Peer:
        return self._local

    @property
    def remotes(self) -> list[Peer]:
        return self._remotes

    @property
    def empty(self) -> bool:
        return len(self._remotes) == 0

    @property
    def dead(self) -> bool:
        return all([remote.dead for remote in self._remotes])

    @property
    def lag(self) -> int:
        if self.empty or self.dead:
            return -1
        else:
            return max(
                [peer.tip - self._local.tip for peer in self._remotes] + [0]
            )

    def to_dict(self) -> dict:
        return {
            "timestamp": self.timestamp,
            "peers": [peer.to_dict() for peer in self.peers],
        }

    def __repr__(self) -> str:
        return json.dumps(self.to_dict(), indent=4)

    @classmethod
    def from_dict(cls, dict_: dict) -> RoutingTable:
        return RoutingTable(**dict_)

    @classmethod
    def raw_to_dict(cls, raw: list[str]) -> dict:
        return {
            "timestamp": datetime.datetime.now().timestamp(),
            "peers": [
                Peer.raw_to_dict(peer_raw) for peer_raw in raw
            ],
        }

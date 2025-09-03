from dataclasses import dataclass


@dataclass
class Admin:
    id: int
    master: bool

from dataclasses import dataclass


@dataclass
class Package:
    '''Class for representing a package'''
    id: int
    address: str
    city: str
    state: str
    zipcode: int
    weight: int
    deadline: str = None
    special_notes: str = None

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other):
        return self.id == other.id
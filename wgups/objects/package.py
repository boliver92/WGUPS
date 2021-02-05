from dataclasses import dataclass
from typing import ClassVar
from wgups.enums.deliverystatus import DeliveryStatus
from wgups.ds.hashtable import HashTable


@dataclass
class Package:
    """Class for representing a package"""
    package_table: ClassVar[HashTable] = HashTable(10)

    id: int
    address: str
    city: str
    state: str
    zipcode: int
    weight: int
    deadline: str = None
    special_notes: str = None
    delivery_status: DeliveryStatus = DeliveryStatus.Loading

    def __post_init__(self):
        Package.package_table.insert(self)

    def __hash__(self) -> int:
        return self.id

    def __eq__(self, other):
        return self.id == other.id

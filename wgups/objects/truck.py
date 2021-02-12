from dataclasses import dataclass
from typing import ClassVar
from wgups.objects.package import Package


@dataclass()
class Truck:
    """
    Class representation of a truck.

    ...

    Attributes
        id: int
    """

    id: int
    packages = []

    truck_list: ClassVar[list] = []

    def __post_init__(self):
        Truck.truck_list.append(self)

    def set_packages(self, package_list: list):
        self.packages = package_list

from dataclasses import dataclass
from typing import ClassVar
from wgups.objects.hub import Hub
from wgups.objects.map_manager import MapManager
from wgups.enums.truck_status import TruckStatus
import wgups.ui.cli


@dataclass()
class Truck:
    """
    Class representation of a truck.

    ...

    Attributes
        id: int
            The truck ID
        packages: list
            A list containing the packages loaded onto the truck
        current_hub: Hub
            The hub where the truck is currently located to deliver a
            package
        truck_miles: int
            The total miles driven on the truck instance.
        truck_list: ClassVar[list]
            A static list containing all of the truck instances
        total_miles: ClassVar[int]
            A static int counter used to keep track of the total miles
            driven by all trucks
    """

    id: int
    packages = []
    current_hub: Hub = None
    truck_miles: int = 0
    priority_packages = []
    status: TruckStatus = TruckStatus.INACTIVE

    truck_list: ClassVar[list] = []
    total_miles: ClassVar[int] = 0

    def __post_init__(self):
        Truck.truck_list.append(self)
        self.current_hub = MapManager.name_to_hub_map.get("Western Governors University")


    def set_packages(self, package_list: list):
        """
        Sets the truck instance's package list to the package_list parameter.
        :param package_list: The package list to be associated with the truck
        """
        self.packages = [package for package in package_list]
        for package in self.packages:
            wgups.ui.cli.GUI.add_event(f"\u001b[34mPackage {package.id}\u001b[0m was loaded onto \u001b[32mTruck {self.id}.\u001b[0m")

    def toggle_status(self):
        if self.status == TruckStatus.INACTIVE:
            self.status = TruckStatus.ACTIVE
        else:
            self.status = TruckStatus.INACTIVE

        wgups.ui.cli.GUI.add_event(f"\u001b[34mTruck {self.id}\u001b[0m is now {self.status.value}")
from dataclasses import dataclass
from typing import ClassVar
from wgups.enums.delivery_status import DeliveryStatus
from wgups.objects.map_manager import MapManager


@dataclass()
class Package:
    """ A Package class to represent a package.

    The package class will be used to hold the package details of each
    package to be delivered.

    ...

    Attributes
        id: int
            The unique ID associated with the package.
        address: str
            The address of the hub where the package should be
            delivered.
        city: str
            The city of the hub where the package should be
            delivered.
        state: str
            The state of the hub where the package should be
            delivered.
        zip: int
            The zipcode of the hub where the package should be
            delivered.
        delivery_deadline: str
            The delivery deadline for the package.
        weight: int
            The total weight of the package.
        special_notes: str
            Special notes associated with the package.
        delivery_status: DeliveryStatus
            default = DeliveryStatus.LOADING
            The current delivery status of the package.
    """

    id: int
    address: str
    city: str
    state: str
    zip: int
    delivery_deadline: str
    weight: int
    special_notes: str
    delivery_status: DeliveryStatus = DeliveryStatus.LOADING

    # Class Variables
    package_list: ClassVar[list] = []

    def __post_init__(self):
        # Adds the package to the static package_list. This will allow
        # the possibility to easily iterate through all packages when
        # building the GUI
        Package.package_list.append(self)

        current_address_to_package_map = MapManager.address_to_package_map.get_or_default(self.address)
        if current_address_to_package_map is None:
            MapManager.address_to_package_map.put(self.address, [self])
        else:
            current_address_to_package_map.append(self)
            MapManager.address_to_package_map.put(self.address, current_address_to_package_map)

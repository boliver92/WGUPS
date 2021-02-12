from dataclasses import dataclass
from typing import ClassVar
from wgups.objects.map_manager import MapManager


@dataclass()
class Hub:
    """
    Class to represent each Hub that our trucks will be delivering packages to.

    ...

    Attributes

        name: str
            The name of the HUB

        address: str
            The address of the HUB
    """

    name: str
    address: str

    hub_list: ClassVar[list] = []

    def __post_init__(self):
        Hub.hub_list.append(self)
        MapManager.name_to_hub_map.put(self.name, self)
        MapManager.address_to_hub_map.put(self.address, self)
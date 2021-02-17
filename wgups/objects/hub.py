from dataclasses import dataclass
from typing import ClassVar

from wgups.ds.vertex import Vertex
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

    hub_list = []

    def __init__(self, name: str, address: str, vertex: Vertex = None):
        self.name = name
        self.address = address
        self.vertex = vertex
        self.vertex.hub = self
        self.vertex.address = self.address
        Hub.hub_list.append(self)
        MapManager.name_to_hub_map.put(self.name, self)
        MapManager.address_to_hub_map.put(self.address, self)

    def __repr__(self):
        return f"HUB: {self.name}, ADDRESS: {self.address}"
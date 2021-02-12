from wgups.ds.hashmap import Hashmap
from dataclasses import dataclass
from typing import ClassVar


@dataclass()
class MapManager:

    name_to_hub_map: ClassVar[Hashmap] = Hashmap()
    address_to_hub_map: ClassVar[Hashmap] = Hashmap()
    id_to_package_map: ClassVar[Hashmap] = Hashmap()
    address_to_package_map: ClassVar[Hashmap] = Hashmap()
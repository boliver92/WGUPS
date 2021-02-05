from dataclasses import dataclass
from typing import ClassVar
from wgups.ds.hashtable import HashTable
from wgups.ds.hashmap import HashMap


@dataclass()
class Hub:
    hub_table: ClassVar[HashMap] = HashMap(10)

    name: str
    address: str
    distance_to_hubs: HashMap = HashMap()

    def __post_init__(self):
        Hub.hub_table.insert(self.name, self)

    def __hash__(self) -> int:
        return len(self.name)

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __repr__(self):
        return f"HUB: {self.name}, ADDRESS: {self.address}"

    def set_distance_map(self, key, value):
        self.distance_to_hubs.insert(key, value)

        # rows = [i for i in rows if len(i) > 0]
        #
        # for i, col in enumerate(rows):
        #     hub_to_find = Hub.find_hub_by_name(keys[i])
        #     if hub_to_find:
        #         self.distance_to_hubs.insert(Hub.find_hub_by_name(keys[i]), rows[i])
        #
        # print(f"-------CURRENT HUB: {self.name}------------")
        # for key in keys[len(rows):]:
        #     hub_to_find = Hub.find_hub_by_name(key)
        #     if hub_to_find:
        #         print(f"Found HUB! {hub_to_find.name}, Value: {hub_to_find.distance_to_hubs.get_value_or_default(self)} ")
        #
        #     # if hub_to_find:
        #     #     print(f"********Source Hub = {self.name} destination = {hub_to_find.name}, miles = {hub_to_find.distance_to_hubs.get_value_or_default(self)}")
        #     #     self.distance_to_hubs.insert(key, hub_to_find.distance_to_hubs.get_value_or_default(self))
        #
        # print(f"---------Current HUB: {self.name}------------")
        # self.distance_to_hubs.print_hashmap()

    @classmethod
    def find_hub_by_name(cls, name: str):
        return Hub.hub_table.get_value_or_default(name)

    # @classmethod
    # def update_distance_map(cls, hub, list_of_distances):
    #     current_distance = Hub.distance_to_hubs.get_value_or_default(hub)
    #     if Hub.distance_to_hubs.get_value_or_default(hub) is None:

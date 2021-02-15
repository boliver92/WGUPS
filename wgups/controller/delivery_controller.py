from dataclasses import dataclass
import wgups.objects.truck as truck
import wgups.ui.cli as cli
from wgups.ds.graph import Graph
from wgups.objects.clock import Clock
from wgups.utils.data_reader import read_hubs, read_packages, create_trucks, create_vertexes, connect_vertexes, \
    load_truck
import time


@dataclass()
class DeliveryController:
    clock: Clock = Clock()
    special_events = {
        "8:00 AM": False,
        "9:05 AM": False,
        "10:20 AM": False
    }

    def start(self):
        routes = Graph()
        read_hubs()
        read_packages()
        create_trucks()
        create_vertexes(routes)
        connect_vertexes(routes)

    def tick(self):
        self._fire_special_events()
        print(self.clock)
        self.clock.add_minutes(5)

    def _fire_special_events(self):
        if self.clock.hour >= 8 and self.special_events.get("8:00 AM") is False:
            load_truck(1)
            truck.Truck.truck_list[0].toggle_status()
            self.special_events["8:00 AM"] = True

        if (self.clock.hour > 9 or (self.clock.hour == 9 and self.clock.minute >= 5)) and self.special_events.get("9:05 AM") is False:
            cli.GUI.add_event("Delayed packages received at 9:05 AM")
            load_truck(2)
            load_truck(3)
            self.special_events["9:05 AM"] = True

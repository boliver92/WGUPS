from dataclasses import dataclass
from typing import ClassVar
from wgups.ds.graph import Graph
from wgups.utils.data_reader import read_hubs, read_packages, create_trucks, create_vertexes, connect_vertexes
import time


@dataclass()
class DeliveryController:

    def start(self):
        routes = Graph()
        read_hubs()
        read_packages()
        create_trucks()
        create_vertexes(routes)
        connect_vertexes(routes)

    def tick(self, delay=1):


        time.sleep(delay)

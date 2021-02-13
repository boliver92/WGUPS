from dataclasses import dataclass
from typing import ClassVar
from wgups.ds.graph import Graph
from wgups.utils.data_reader import read_hubs, read_packages, create_trucks, create_vertexes, connect_vertexes
import time


@dataclass()
class DeliveryController:

    paused: ClassVar[bool] = False

    def start(self):
        routes = Graph()
        read_hubs()
        read_packages()
        create_trucks()
        create_vertexes(routes)
        connect_vertexes(routes)

    def run(self, delay=None):
        while not DeliveryController.paused:
            print("************************************************RUN**********************************")
            time.sleep(1)
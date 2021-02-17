from wgups.ds.graph import Graph, dijkstra_shortest_path, get_shortest_path
from wgups.ds.vertex import Vertex
import wgups.objects.clock as clok
from wgups.objects.hub import Hub
from wgups.objects.map_manager import MapManager
from wgups.enums.truck_status import TruckStatus
import wgups.ui.cli as cli
from wgups.enums.delivery_status import DeliveryStatus


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

    truck_list = []
    total_miles: float = 0.0
    AVERAGE_MPH = 18.0

    def __init__(self, id):
        self.id = id
        self.packages = []
        self.current_hub = MapManager.name_to_hub_map.get("Western Governors University")
        self.truck_miles: float = 0.0
        self.status: TruckStatus = TruckStatus.INACTIVE
        self.current_package = None
        self.current_path = []

        Truck.truck_list.append(self)

    def set_packages(self, package_list: list):
        """
        Sets the truck instance's package list to the package_list parameter.
        :param package_list: The package list to be associated with the truck
        """
        self.packages = [package for package in package_list]
        for package in self.packages:
            cli.GUI.add_event(
                f"\u001b[34mPackage {package.id}\u001b[0m was loaded onto \u001b[32mTruck {self.id}.\u001b[0m")

    def toggle_status(self):
        if self.status == TruckStatus.INACTIVE:
            self.status = TruckStatus.ACTIVE
        else:
            self.status = TruckStatus.INACTIVE

        cli.GUI.add_event(f"\u001b[34mTruck {self.id}\u001b[0m is now {self.status.value}")

    def has_package(self) -> bool:
        return len(self.packages) > 0

    def get_next_stop(self, graph):

        start_hub: Hub = self.current_hub
        start_vertex: Vertex = start_hub.vertex

        end_vertex = None
        end_distance = 1000.0

        dijkstra_shortest_path(graph, start_vertex)

        for package in self.packages:
            end_hub: Hub = MapManager.address_to_hub_map.get(package.address)
            end_vertex_to_compare: Vertex = end_hub.vertex
            if graph.edge_weights[(start_vertex, end_vertex_to_compare)] < end_distance:
                end_vertex = end_vertex_to_compare
                end_distance = graph.edge_weights[(start_vertex, end_vertex)]

        self.current_path = get_shortest_path(start_vertex, end_vertex)

    def deliver_package(self, clock):
        for package in self.packages:
            if package.address == self.current_hub.address:
                package.delivery_status = DeliveryStatus.DELIVERED
                self.packages.remove(package)
                cli.GUI.add_event(f"{clock}: Package {package.id} was delivered to {self.current_hub.address}")

    def goto_next_hub(self, graph: Graph, clock: clok.Clock) -> clok.Clock:
        simulated_clock = clok.Clock(clock.total_minutes)
        current_vertex = self.current_hub.vertex
        next_hub_vertex = self.current_path.pop()
        distance = graph.edge_weights[(current_vertex, next_hub_vertex)]

        simulated_clock.simulate_minutes(distance)

        next_hub = MapManager.name_to_hub_map.get(next_hub_vertex.label)
        self.current_hub = next_hub
        self.truck_miles += distance
        Truck.total_miles += distance

        return simulated_clock

    def tick(self, graph: Graph, clock: clok.Clock):
        if not self.has_package():
            self.toggle_status()
            return
        if len(self.current_path) == 0:
            self.get_next_stop(graph)

        simulated_clock = self.goto_next_hub(graph, clock)
        self.deliver_package(simulated_clock)
        clock.add_minutes(simulated_clock.total_minutes - clock.total_minutes) # Remove later - just for testing

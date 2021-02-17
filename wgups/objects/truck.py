from wgups.ds.graph import Graph, dijkstra_shortest_path, get_shortest_path
from wgups.ds.vertex import Vertex
from wgups.objects.clock import Clock
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
        self.active = False

        Truck.truck_list.append(self)

    def set_packages(self):
        """
        Sets the truck instance's package list to the package_list parameter.
        :param package_list: The package list to be associated with the truck
        """
        for package in self.packages:
            cli.GUI.add_event(
                f"\u001b[34mPackage {package.id}\u001b[0m was loaded onto \u001b[32mTruck {self.id}.\u001b[0m")
            package.delivery_status = DeliveryStatus.LOADED

    def toggle_status(self):
        if not self.active:
            self.status = TruckStatus.ACTIVE
            self.active = True
        else:
            self.status = TruckStatus.INACTIVE
            self.active = False

            if self.id != 3:
                truck3 = Truck.truck_list[2]
                if not truck3.active:
                    truck3.toggle_status()

        cli.GUI.add_event(f"\u001b[34mTruck {self.id}\u001b[0m is now {self.status.value}")

    def has_package(self) -> bool:
        return len(self.packages) > 0

    def get_next_stop(self, graph):

        start_hub: Hub = self.current_hub
        start_vertex: Vertex = start_hub.vertex

        end_vertex = None
        end_distance = 1000.0

        dijkstra_shortest_path(graph, start_vertex)

        if len(self.packages) > 1:
            for package in self.packages:
                for vertex in Vertex.vertex_list:
                    if vertex.address == package.address:
                        end_vertex_to_compare = vertex
                        if end_vertex_to_compare is not None and graph.edge_weights[(start_vertex, end_vertex_to_compare)] <= end_distance:
                            end_vertex = end_vertex_to_compare
                            end_distance = graph.edge_weights[(start_vertex, end_vertex)]
        else:
            package = self.packages[0]
            for vertex in Vertex.vertex_list:
                if vertex.address == package.address:
                    end_vertex = vertex

        self.current_path = get_shortest_path(start_vertex, end_vertex)

        if len(self.current_path) < 1:
            package = self.packages[0]
            for vertex in Vertex.vertex_list:
                if vertex.address == package.address:
                    end_vertex = vertex
                    self.current_path = get_shortest_path(start_vertex, end_vertex)

    def deliver_package(self, clock):
        for package in self.packages:
            if package.address == self.current_hub.address:
                package.delivery_status = DeliveryStatus.DELIVERED
                self.packages.remove(package)
                cli.GUI.add_event(f"{clock}: Package {package.id} was delivered to {self.current_hub.address}")

    def goto_next_hub(self, graph: Graph, clock: Clock) -> Clock:
        simulated_clock = Clock(clock.total_minutes)
        current_vertex = self.current_hub.vertex
        try:
            next_hub_vertex = self.current_path.pop()
        except IndexError:
            return simulated_clock
        distance = graph.edge_weights[(current_vertex, next_hub_vertex)]

        simulated_clock.simulate_minutes(distance)

        next_hub = MapManager.name_to_hub_map.get(next_hub_vertex.label)
        self.current_hub = next_hub
        self.truck_miles += distance
        Truck.total_miles += distance

        return simulated_clock

    def tick(self, graph: Graph, clock: Clock):
        if not self.has_package():
            self.toggle_status()
            return

        if len(self.current_path) <= 0:
            self.get_next_stop(graph)

        if len(self.current_path) > 0:
            simulated_clock = self.goto_next_hub(graph, clock)
            self.deliver_package(simulated_clock)
        else:
            return

        if simulated_clock.total_minutes > Clock.max_min:
            Clock.max_min = simulated_clock.total_minutes

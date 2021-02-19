from wgups.ds.graph import Graph, dijkstra_shortest_path, get_shortest_path
from wgups.ds.vertex import Vertex
from wgups.objects.clock import Clock
from wgups.objects.hub import Hub
from wgups.objects.package import Package
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
        self.expected_distance = 0.0
        self.priority_packages = []

        Truck.truck_list.append(self)

    def toggle_status(self):
        """
        Switches the truck status between active and inactive.

        For the sake of this program, truck3 is toggled to active as soon as truck 1 or 2 are inactive.

        Space Complexity:
            O(1)

        Time Complexity:
            O(1)
        """
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
        return len(self.packages) > 0 or len(self.priority_packages) > 0

    def get_next_stop(self, graph):

        start_vertex: Vertex = self.current_hub.vertex

        end_vertex = None
        end_distance = 1000.0

        dijkstra_shortest_path(graph, start_vertex)

        if len(self.priority_packages) > 0:
            for package in self.priority_packages:
                for vertex in Vertex.vertex_list:
                    if vertex.address == package.address:
                        end_vertex_to_compare = vertex
                        if end_vertex_to_compare is not None and graph.edge_weights[
                            (start_vertex, end_vertex_to_compare)] < end_distance:
                            end_vertex = end_vertex_to_compare
                            end_distance = graph.edge_weights[(start_vertex, end_vertex)]

        elif len(self.packages) > 0:
            for package in self.packages:
                if package.address == start_vertex.address:
                    self.packages.remove(package)
                    cli.GUI.add_event(f"Package {package.id} was delivered to {self.current_hub.address}")
                for vertex in Vertex.vertex_list:
                    if vertex.address == package.address:
                        end_vertex_to_compare = vertex
                        if end_vertex_to_compare is not None and graph.edge_weights[
                            (start_vertex, end_vertex_to_compare)] < end_distance:
                            end_vertex = end_vertex_to_compare
                            end_distance = graph.edge_weights[(start_vertex, end_vertex)]

        self.current_path = get_shortest_path(start_vertex, end_vertex)

        if len(self.current_path) <= 0:
            self.toggle_status()
            return

    def deliver_package(self, graph: Graph, clock, package=None):
        if package:
            cli.GUI.add_event(
                f"\u001b[31;1m({clock})\u001b[0m/ \u001b[34mTrucK {self.id}\u001b[0m: \u001b[32;1mPackage {package.id}\u001b[0m was delivered to \u001b[35;1m{self.current_hub.address}\u001b[0m. \u001b[33;1mDeadline: {package.delivery_deadline}\u001b[0m")
            if package in self.priority_packages:
                if len(package.nearby_packages) > 0:
                    for nearby_package in package.nearby_packages:
                        start_vertex = self.current_hub.vertex
                        nearby_hub = MapManager.address_to_hub_map.get(nearby_package.address)
                        end_vertex = nearby_hub.vertex
                        distance = round(graph.edge_weights[(start_vertex, end_vertex)], 1)
                        clock.simulate_minutes(distance)
                        cli.GUI.add_event(
                            f"\u001b[31;1m({clock})\u001b[0m/ \u001b[34mTrucK {self.id}\u001b[0m: \u001b[32;1mPackage {nearby_package.id}\u001b[0m was delivered to \u001b[35;1m{nearby_hub.address}\u001b[0m. \u001b[33;1mDeadline: {nearby_package.delivery_deadline}\u001b[0m")
                        self.truck_miles += distance * 2
                        clock.simulate_minutes(distance)
                        package.nearby_packages.remove(nearby_package)
                        nearby_package.delivery_status = DeliveryStatus.DELIVERED
                self.priority_packages.remove(package)
            package.delivery_status = DeliveryStatus.DELIVERED
            # # if package in self.packages:
            # #     self.packages.remove(package)
            # # if package in self.priority_packages:
            # #     for i in range(len(package.nearby_packages)):
            # #         self.packages.append(package.nearby_packages.pop())
            # #     self.priority_packages.remove(package)
            # cli.GUI.add_event(
            #     f"\u001b[31;1m({clock})\u001b[0m/ \u001b[34mTrucK {self.id}\u001b[0m: \u001b[32;1mPackage {package.id}\u001b[0m was delivered to \u001b[35;1m{self.current_hub.address}\u001b[0m. \u001b[33;1mDeadline: {package.delivery_deadline}\u001b[0m")



    def goto_next_hub(self, graph: Graph, clock: Clock) -> Clock:
        simulated_clock = Clock(clock.total_minutes)
        simulated_clock.meridian = clock.meridian

        current_vertex = self.current_hub.vertex
        if len(self.current_path) > 0:
            next_hub_vertex = self.current_path[0]
            self.current_path.remove(next_hub_vertex)

        distance = round(graph.edge_weights[(current_vertex, next_hub_vertex)], 1)

        if distance > 0.0:
            simulated_clock.simulate_minutes(distance)

        self.current_hub = next_hub_vertex.hub
        self.truck_miles += distance
        Truck.total_miles += distance

        return simulated_clock

    def get_priority_package(self, graph: Graph):

        if len(self.priority_packages) > 0:

            start_vertex = self.current_hub.vertex
            closest_package = None
            smallest_distance = 100.0
            dijkstra_shortest_path(graph, start_vertex)
            for priority_package in self.priority_packages:
                priority_package_hub = MapManager.address_to_hub_map.get(priority_package.address)
                priority_package_vertex = priority_package_hub.vertex
                distance = graph.edge_weights[(start_vertex, priority_package_vertex)]
                if distance < smallest_distance:
                    smallest_distance = distance
                    closest_package = priority_package
            return closest_package
        return None

    def travel_to(self, graph: Graph, clock: Clock, path_node: Vertex):

        current_vertex = self.current_hub.vertex
        distance_traveled = graph.edge_weights[(current_vertex, path_node)]
        clock.simulate_minutes(distance_traveled)
        self.current_hub = path_node.hub
        self.truck_miles += distance_traveled
        Truck.total_miles += distance_traveled

    def create_deliver_message(self, package: Package, clock: Clock):
        cli.GUI.add_event(f"{clock} / Truck {self.id}: Package {package.id} was delivered to {package.address}. Deadline {package.delivery_deadline}")

    def deliver_package(self, graph: Graph, clock: Clock):

        for package in self.priority_packages:
            for nearby_package in package.nearby_packages:
                if nearby_package.address == self.current_hub.address:
                    package.nearby_packages.remove(nearby_package)
                    self.packages.remove(nearby_package)
                    self.create_deliver_message(nearby_package, clock)
            if package.address == self.current_hub.address:
                self.create_deliver_message(package, clock)
                for nearby_package in package.nearby_packages:
                    nearby_package_hub = MapManager.address_to_hub_map.get(nearby_package.address)
                    nearby_vertex = nearby_package_hub.vertex
                    distance = graph.edge_weights[(self.current_hub.vertex, nearby_vertex)]
                    self.truck_miles += distance
                    clock.simulate_minutes(distance)
                    self.create_deliver_message(nearby_package, clock)
                    clock.simulate_minutes(distance)
                    self.truck_miles += distance
                    package.nearby_packages.remove(nearby_package)
                    self.packages.remove(nearby_package)
                self.priority_packages.remove(package)

    def find_path(self, graph: Graph, package: Package):

        start_vertex = self.current_hub.vertex
        dijkstra_shortest_path(graph, start_vertex)

        end_hub = MapManager.address_to_hub_map.get(package.address)
        end_vertex = end_hub.vertex

        return get_shortest_path(start_vertex, end_vertex)

    def tick(self, graph: Graph, clock: Clock) -> int:

        next_priority_package = self.get_priority_package(graph)

        if next_priority_package is not None:
            self.current_path = self.find_path(graph, next_priority_package)
            for path_node in self.current_path:
                self.travel_to(graph, clock, path_node)
                self.deliver_package(graph, clock)


        # delivery_clock = Clock(clock.total_minutes)
        #
        # for package in self.priority_packages:
        #     if package.address == self.current_hub.address:
        #         self.deliver_package(graph, delivery_clock, package)
        #         return
        #
        # for package in self.packages:
        #     if package.address == self.current_hub.address:
        #         self.deliver_package(graph, delivery_clock, package)
        #         return
        #
        # if not self.has_package():
        #     self.toggle_status()
        #     return
        #
        # travel_clock = None
        #
        # if len(self.current_path) <= 0:
        #     self.get_next_stop(graph)
        #
        # if len(self.current_path) > 0:
        #     travel_clock = self.goto_next_hub(graph, clock)
        #     for package in self.packages:
        #         if package.address == self.current_hub.address:
        #             self.deliver_package(travel_clock, package)
        #
        # if travel_clock is not None and (travel_clock.total_minutes > Clock.max_min):
        #     Clock.max_min = travel_clock.total_minutes

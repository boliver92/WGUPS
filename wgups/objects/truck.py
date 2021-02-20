from wgups.ds.graph import Graph, dijkstra_shortest_path, get_shortest_path
from wgups.ds.vertex import Vertex
from wgups.objects.clock import Clock
from wgups.objects.hub import Hub
from wgups.objects.package import Package
from wgups.objects.map_manager import MapManager
from wgups.enums.truck_status import TruckStatus
import wgups.ui.cli as cli
from wgups.enums.delivery_status import DeliveryStatus
import operator


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
        self.tick_count = 1

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

        cli.GUI.add_event(f"\u001b[34mTruck {self.id}\u001b[0m is now {self.status.value}")

    def has_package(self):
        return len(self.packages) > 0

    def travel_to(self, graph: Graph, clock: Clock, path_node: Vertex):

        current_vertex = self.current_hub.vertex
        distance_traveled = graph.edge_weights[(current_vertex, path_node)]
        clock.simulate_minutes(distance_traveled)
        self.current_hub = MapManager.address_to_hub_map.get(path_node.address)
        self.truck_miles += distance_traveled
        Truck.total_miles += distance_traveled

    def create_deliver_message(self, package: Package, clock: Clock):
        cli.GUI.add_event(
            f"{clock} / Truck {self.id}: Package {package.id} was delivered to {package.address}. Deadline {package.delivery_deadline}")

    def deliver_package(self, graph: Graph, clock: Clock):

        for package in self.packages:
            if package.address == self.current_hub.address:
                self.create_deliver_message(package, clock)
                package.delivery_status = DeliveryStatus.DELIVERED
                self.packages.remove(package)

    def find_path(self, graph: Graph):

        start_vertex = self.current_hub.vertex
        dijkstra_shortest_path(graph, start_vertex)
        end_vertex = None
        delivery_addresses = []
        for package in self.packages:
            delivery_addresses.append(package.address)
            if package.delivery_deadline == "9:00 AM":
                end_vertex = MapManager.address_to_hub_map.get(package.address).vertex
                self.current_path = get_shortest_path(start_vertex, end_vertex)
                return
            if package.delivery_deadline == "10:30 AM":
                end_vertex = MapManager.address_to_hub_map.get(package.address).vertex
                self.current_path = get_shortest_path(start_vertex, end_vertex)
                return
        for vertex in Vertex.vertex_list:
            if vertex.address in delivery_addresses:
                if end_vertex is None:
                    end_vertex = vertex
                else:
                    if vertex.distance < end_vertex.distance:
                        end_vertex = vertex

        self.current_path = get_shortest_path(start_vertex, end_vertex)

    @classmethod
    def load_packages(cls, graph):

        connected_packages = [13, 14, 15, 16, 19, 20]
        truck1 = Truck.truck_list[0]
        truck2 = Truck.truck_list[1]
        truck3 = Truck.truck_list[2]
        current_truck = truck1

        for package in Package.package_list:
            if ("Delayed" in package.special_notes or "truck" in package.special_notes) and "EOD" in package.delivery_deadline and (package not in truck1.packages and package not in truck3.packages and len(truck2.packages) < 16):
                truck2.packages.append(package)
                if package.id in connected_packages:
                    for id_number in connected_packages:
                        truck2.packages.append(Package.package_list[id_number-1])
                for comp_package in Package.package_list:
                    if comp_package.address == Package.package_list and (comp_package not in truck1.packages and comp_package not in truck3.packages) and "EOD" in comp_package.delivery_deadline and len(truck2.packages) < 16:
                        truck2.packages.append(comp_package)
                    if comp_package not in truck1.packages and comp_package not in truck3.packages and comp_package not in truck2.packages and "EOD" in comp_package.delivery_deadline and len(truck2.packages) < 16:
                        start_hub = MapManager.address_to_hub_map.get(package.address)
                        start_vertex = start_hub.vertex
                        dijkstra_shortest_path(graph, start_vertex)
                        comp_package_hub = MapManager.address_to_hub_map.get(comp_package.address)
                        comp_package_vertex = comp_package_hub.vertex
                        distance = graph.edge_weights[(start_vertex, comp_package_vertex)]
                        if distance < 2.0:
                            truck2.packages.append(comp_package)
            if ("9:00 AM" in package.delivery_deadline or "10:30 AM" in package.delivery_deadline) and ("Delay" not in package.special_notes and "truck" not in package.special_notes) and (package not in truck1.packages and package not in truck2.packages and package not in truck3.packages) and len(current_truck.packages) < 16:
                current_truck.packages.append(package)
                if package.id in connected_packages:
                    for id_number in connected_packages:
                        current_truck.packages.append(Package.package_list[id_number-1])
                for comp_package in Package.package_list:
                    if comp_package.address == Package.package_list and (comp_package not in truck1.packages and comp_package not in truck3.packages and comp_package not in truck2.packages) and len(current_truck.packages) < 16:
                        current_truck.packages.append(comp_package)
                    if comp_package not in truck1.packages and comp_package not in truck3.packages and comp_package not in truck2.packages and len(current_truck.packages) < 16:
                        start_hub = MapManager.address_to_hub_map.get(package.address)
                        start_vertex = start_hub.vertex
                        dijkstra_shortest_path(graph, start_vertex)
                        comp_package_hub = MapManager.address_to_hub_map.get(comp_package.address)
                        comp_package_vertex = comp_package_hub.vertex
                        distance = graph.edge_weights[(start_vertex, comp_package_vertex)]
                        if distance < 2.0:
                            current_truck.packages.append(comp_package)
                if current_truck == truck1:
                    current_truck = truck3
                else:
                    current_truck = truck1

        # for package in Package.package_list:
        #     if "Delayed" in package.special_notes or "truck" in package.special_notes:
        #         truck2.packages.append(package)
        #         for comp_package in Package.package_list:
        #             if comp_package.address == package.address and (comp_package not in truck1.packages and comp_package not in truck2.packages and comp_package not in truck3.packages):
        #                 current_truck.packages.append(comp_package)

    def tick(self, graph: Graph, clock: Clock):

        self.deliver_package(graph, clock)

        if not self.has_package():
            self.toggle_status()
            return

        if len(self.current_path) <= 0:
            self.find_path(graph)

        if len(self.current_path) <= 0:
            return

        self.travel_to(graph, clock, self.current_path.pop())
        self.deliver_package(graph, clock)

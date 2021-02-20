from wgups.controller.route_controller import RouteController
from wgups.ds.hashmap import Hashmap
from wgups.ds.vertex import Vertex
from wgups.enums.delivery_status import DeliveryStatus
from wgups.enums.truck_status import TruckStatus
from wgups.objects.clock import Clock
import wgups.ui.cli


class Truck(object):
    pass


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

    master_truck_list = []
    total_miles: float = 0.0
    AVERAGE_MPH = 18.0
    _find_by_id = Hashmap()

    def __init__(self, id):
        self.id: int = id
        self.status: TruckStatus = TruckStatus.INACTIVE
        self.miles: float = 0.0
        self.current_vertex: Vertex = Vertex.find_by_label("Western Governors University")
        self.path = []
        self.packages = []

        Truck.master_truck_list.append(self)
        Truck._find_by_id.put(self.id, self)

    def is_active(self) -> bool:
        return self.status == TruckStatus.ACTIVE

    @classmethod
    def find_by_id(cls, id: int) -> Truck:
        """
       Takes a int id of a Truck object to be found. The search
       method uses a hashmap
       :param id: The id of the Truck to be found
       :return: Truck object if it is found. Otherwise, None.

       Space Complexity:
           O(1)

       Time Complexity:
           O(1)
       """
        return Truck._find_by_id.get(id)

    def deliver_package(self, clock):

        for package in self.packages:
            if package.address == self.current_vertex.address:
                self.packages.remove(package)
                package.delivery_status = DeliveryStatus.DELIVERED
                wgups.ui.cli.GUI.add_event(
                    f"{clock} / {self.id} : Package {package.id} Delivered to {package.address}. Deadline: {package.delivery_deadline}")

    def tick(self, route_controller: RouteController, clock: Clock):
        self.deliver_package(clock)

        try:
            self.travel_to(route_controller, self.path[0], clock)
        except IndexError:
            self.toggle_status()

        self.deliver_package(clock)

    def travel_to(self, route_controller: RouteController, end_vertex: Vertex, clock: Clock):
        distance = route_controller.edge_weights[(self.current_vertex, end_vertex)]
        self.miles += distance
        Truck.total_miles += distance
        self.current_vertex = end_vertex
        clock.simulate_travel_time(distance)
        self.path.remove(self.current_vertex)

    def toggle_status(self):
        if self.status == TruckStatus.INACTIVE:
            self.status = TruckStatus.ACTIVE
        else:
            self.status = TruckStatus.INACTIVE

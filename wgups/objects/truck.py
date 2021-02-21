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

    def deliver_package(self, clock: Clock) -> bool:
        """Delivers packages in the truck.package list if the address
        matches the truck's current address.

        :param clock: The clock
         object to represent the current time.
        :return: True if the package is delivered, else False.

        Space Complexity
            O(1)
        Time Complexity
            O(n)
        """

        for package in self.packages:
            if package.address == self.current_vertex.address:
                self.packages.remove(package)
                package.delivery_status = DeliveryStatus.DELIVERED
                wgups.ui.cli.GUI.add_event(
                    (
                        f"{clock} / {self.id} : Package {package.id} Delivered to {package.address}. Deadline: {package.delivery_deadline}",
                        clock.total_minutes))
                return True

        return False

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

    def has_packages(self) -> bool:
        """ Returns True if the Truck objects package list has a package in it, otherwise False

        :return: Returns True if the Truck objects package list has a
        package in it, otherwise False

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """
        return len(self.packages) > 0

    def is_active(self) -> bool:
        """
        :return: Returns True if the truck status is
        TruckStatus.ACTIVE, otherwise False

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """
        return self.status == TruckStatus.ACTIVE

    def tick(self, route_controller: RouteController, clock: Clock):
        """The main method of the Truck class that handles the truck delivery logic.

        :param route_controller:
            The Graph that is being used to handle the routing and vertices.
        :param clock:
            The clock used to represent the Truck's time.

        Space Complexity
            O(1)
        Time Complexity
            O(n)
        """
        while self.deliver_package(clock):
            pass

        if len(self.path):
            try:
                self.travel_to_closest_vertex(route_controller, clock)
            except IndexError:
                if not self.has_packages():
                    self.toggle_status()
        elif not self.has_packages() and not len(self.path):
            self.toggle_status()

        self.deliver_package(clock)

    def toggle_status(self):
        """Changes the truck status based on it current status.

        If the truck status is inactive, it will change it to active.
        Otherwise the status will be changed to inactive.

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        if self.status == TruckStatus.INACTIVE:
            self.status = TruckStatus.ACTIVE
        else:
            self.status = TruckStatus.INACTIVE

    def travel_to_closest_vertex(self, route_controller: RouteController, clock: Clock):
        """ Changes the Truck object's current vertex to the nearest neighbor and updates the miles and clock time

        :param route_controller: The graph that contains the vertices.
        :param clock: The clock that is keeping time.

        Space Complexity
            O(1)

        Time Complexity
            O(n)
        """

        min_distance = 1000.0  # Used to keep the current min_distance.
        # Initialized at 1000 to make sure that it will be higher than
        # any other distance
        next_vertex = None

        for possible_vertex in self.path:
            if possible_vertex == self.current_vertex:
                continue
            distance = route_controller.edge_weights[(self.current_vertex, possible_vertex)]
            if distance < min_distance:
                min_distance = distance
                next_vertex = possible_vertex

        self.miles += min_distance
        Truck.total_miles += min_distance
        self.current_vertex = next_vertex
        clock.simulate_travel_time(min_distance)
        self.path.remove(self.current_vertex)

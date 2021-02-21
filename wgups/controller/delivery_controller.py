from wgups.ds.vertex import Vertex
from wgups.enums.delivery_status import DeliveryStatus
from wgups.objects.clock import Clock
from wgups.controller.route_controller import RouteController
from wgups.objects.truck import Truck
from wgups.utils.data_reader import create_hubs_and_vertices, read_packages, create_trucks, connect_vertices
from wgups.objects.package import Package
import wgups.ui.cli


class DeliveryController:
    special_events = {
        "8:00 AM": False,
        "9:05 AM": False,
        "10:20 AM": False,
        "Delay": False
    }

    def __init__(self, clock: Clock):
        self.clock = clock
        self.route_controller = RouteController()

        self.clock1 = Clock()
        self.clock2 = Clock(545)
        self.clock3 = Clock()

    def start(self):
        """Loads the data needed for the program to function.

        The method does the following:
            1. Creates a Graph instance to handle our vertices
            representing each Hub object.

            2. Calls wgups.utils.data_reader.read_hubs() to create a
            Hub instance for each hub in the WGUPS Distance table.

            3. Calls wgups.utils.data_reader.read_packages() to create a
            package instance for each package in the WGUPS Package File.

            4. Calls wgups.utils.data_reader.create_trucks() to create
            3 Truck instances

            5. Calls wgups.utils.data_reader.create_vertices() to
            create a vertex instance to represent each Hub and
            associates them with the Graph created in step 1.

            6. Calls wgups.utils.data_reader.connect_vertices() to
            create weighted undirected edges between all vertices.

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        create_hubs_and_vertices(self.route_controller)
        read_packages()
        create_trucks()
        connect_vertices(route_controller=self.route_controller)
        RouteController.visited_vertices.append(Vertex.find_by_label("Western Governors University"))

    def tick(self):
        """Calls each function required to update the application logic/data.

        :return: None

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        self._fire_special_events()
        truck1 = Truck.find_by_id(1)
        truck2 = Truck.find_by_id(2)
        truck3 = Truck.find_by_id(3)
        if truck1.is_active():
            truck1.tick(self.route_controller, self.clock1)
        if truck2.is_active():
            truck2.tick(self.route_controller, self.clock2)
        if truck3.is_active():
            truck3.tick(self.route_controller, self.clock3)

    def _fire_special_events(self):
        """ Used to activate special events when a Truck object's clock meets certain requirements

        If a active truck's clock reaches certain hour/minute threshold
        and the DeliveryController.special_events dict value is
        False for the key, then the event will fire.

        Space Complexity
            O(1)

        Time Complexity
            O(n)
        """

        # Load trucks and make truck 1 and 3 active at 8:00 AM.
        if self.clock.hour >= 8 and self.special_events.get("8:00 AM") is False:
            self._load_trucks(self.route_controller)
            truck1 = Truck.find_by_id(1)

            truck3 = Truck.find_by_id(3)
            truck1.toggle_status()
            truck3.toggle_status()

            self.special_events["8:00 AM"] = True

        # At 9:05 AM, the Delayed packages are received. If truck 1 or
        # truck 3 are inactive. Truck 2 will be changed to active.
        if ((self.clock1.hour > 9 or self.clock3.hour > 9) or ((self.clock1.hour == 9 and self.clock1.minute >= 5) or (
                self.clock3.hour == 9 and self.clock3.minute >= 5))) and self.special_events.get(
                "9:05 AM") is False:
            truck1 = Truck.find_by_id(1)
            truck3 = Truck.find_by_id(3)
            truck2 = Truck.find_by_id(2)

            # Delayed Packages Event Handler.
            if self.special_events.get("Delay") is False:
                delayClock = Clock(545)
                wgups.ui.cli.GUI.add_event((f"{delayClock}: Received Delayed Packages", delayClock.total_minutes))
                for package in truck2.packages:
                    if "Delayed" in package.special_notes:
                        package.delivery_status = DeliveryStatus.LOADING
                self.special_events["Delay"] = True

            # Activates truck 2 is truck 1 is inactive.
            if not truck1.is_active() and truck3.is_active() and self.clock1.total_minutes > self.clock2.total_minutes:
                self.clock2.add_minutes(self.clock1.total_minutes - self.clock2.total_minutes)
                for package in truck2.packages:
                    package.delivery_status = DeliveryStatus.LOADED
                truck2.toggle_status()
                self.special_events["9:05 AM"] = True

            # Activates truck 2 is truck 3 is inactive.
            elif truck1.is_active() and not truck3.is_active() and self.clock3.total_minutes > self.clock2.total_minutes:
                self.clock2.add_minutes(self.clock3.total_minutes - self.clock2.total_minutes)
                for package in truck2.packages:
                    package.delivery_status = DeliveryStatus.LOADED
                truck2.toggle_status()
                self.special_events["9:05 AM"] = True

            # Activates truck2 is either truck1 or truck3 are inactive.
            elif not truck1.is_active() or not truck3.is_active():
                for package in truck2.packages:
                    package.delivery_status = DeliveryStatus.LOADED
                truck2.toggle_status()
                self.special_events["9:05 AM"] = True

    @staticmethod
    def _load_trucks(route_controller: RouteController):
        """Loads each truck based on the nearest neighbor algorithm.

        This method loads the packages utilizing the nearest neighbor
        algorithm to load the next nearest package onto the truck. The
        method is designed that Truck1 is loaded first, Truck3 is
        loaded second. Truck 2 is loaded based on special_notes
        indicating that the package is delayed or must be on truck2 as
        they are discovered.

        :param route_controller: The RouteController that the vertices are located in.

        Space Complexity
            O(1)

        Time Complexity
            O(n^2)
        """
        truck1 = Truck.find_by_id(1)
        truck2 = Truck.find_by_id(2)
        truck3 = Truck.find_by_id(3)

        connected_packages = [13, 14, 15, 19, 16, 20]

        for package_id in connected_packages:
            package = Package.find_by_id(package_id)
            package_vertex = Vertex.find_by_address(package.address)
            truck3.packages.append(package)
            truck3.path.append(package_vertex)

        next_destination = truck1.current_vertex
        while len(truck1.packages) < 16:
            truck = truck1
            next_destination = route_controller.get_nearest_unvisited_neighbor(next_destination)
            if next_destination:
                if next_destination not in truck.path:
                    truck.path.append(next_destination)
                for package in Package.master_package_list:
                    if package.id == 9 and package.address == next_destination.address:
                        truck2.packages.append(package)
                        package.delivery_status = DeliveryStatus.LOADED
                        if next_destination not in truck2.path:
                            truck2.path.append(next_destination)
                    elif package.address == next_destination.address and (
                            "Delay" not in package.special_notes and "truck" not in package.special_notes) and package not in truck.packages and package not in truck3.packages and package not in truck2.packages:
                        truck.packages.append(package)
                        package.delivery_status = DeliveryStatus.LOADED
                        package_destination = Vertex.find_by_address(package.address)
                        if package_destination not in truck.path:
                            truck.path.append(package_destination)
                    elif package.address == next_destination.address and package.id not in connected_packages:
                        truck2.packages.append(package)
                        if next_destination not in truck2.path:
                            truck2.path.append(next_destination)
                        if "Delay" in package.special_notes:
                            package.delivery_status = DeliveryStatus.DELAYED
                        else:
                            package.delivery_status = DeliveryStatus.LOADED
            else:
                break

        next_destination = truck3.current_vertex
        while len(truck3.packages) < 16:
            truck = truck3
            next_destination = route_controller.get_nearest_unvisited_neighbor(next_destination)
            if next_destination:
                if next_destination not in truck.path:
                    truck.path.append(next_destination)
                for package in Package.master_package_list:
                    if package.id == 9 and package.address == next_destination.address:
                        truck2.packages.append(package)
                        package.delivery_status = DeliveryStatus.LOADED
                        if next_destination not in truck2.path:
                            truck2.path.append(next_destination)
                    elif package.address == next_destination.address and (
                            "Delay" not in package.special_notes and "truck" not in package.special_notes) and package not in truck.packages and package not in truck1.packages and package not in truck2.packages:
                        truck.packages.append(package)
                        package.delivery_status = DeliveryStatus.LOADED
                        package_destination = Vertex.find_by_address(package.address)
                        if package_destination not in truck.path:
                            truck.path.append(package_destination)
                    elif package.address == next_destination.address and package.id not in connected_packages:
                        truck2.packages.append(package)
                        if next_destination not in truck2.path:
                            truck2.path.append(next_destination)
                        if "Delay" in package.special_notes:
                            package.delivery_status = DeliveryStatus.DELAYED
                        else:
                            package.delivery_status = DeliveryStatus.LOADED
            else:
                break

        pkg9_index = truck2.path.index(Vertex.find_by_label("Third District Juvenile Court"))
        truck2.path.append(truck2.path.pop(pkg9_index))

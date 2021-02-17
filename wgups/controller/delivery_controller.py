from dataclasses import dataclass
from wgups.objects.truck import Truck
from wgups.objects.package import Package
import wgups.ui.cli as cli
from wgups.ds.graph import Graph
from wgups.enums.truck_status import TruckStatus
import wgups.objects.clock as clk
from wgups.utils.data_reader import read_hubs, read_packages, create_vertices, create_trucks, connect_vertices
import wgups.objects.package as package


class DeliveryController:
    special_events = {
        "8:00 AM": False,
        "9:05 AM": False,
        "10:20 AM": False
    }

    def __init__(self, clock: clk.Clock):
        self.clock = clock
        self.graph = Graph()

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
        read_hubs()
        read_packages()
        create_trucks()
        create_vertices(self.graph)
        connect_vertices(self.graph)

    def tick(self):
        """
        Calls each function required to update the application
        logic/data.

        :return: None

        Space Complexity
            O(1)

        Time Complexity
            O(1)
        """
        self._fire_special_events()
        truck1 = Truck.truck_list[0]
        truck2 = Truck.truck_list[1]
        truck3 = Truck.truck_list[2]
        if truck1.active:
            truck1.tick(self.graph, self.clock)
        if truck2.active:
            truck2.tick(self.graph, self.clock)
        if truck3.active:
            truck3.tick(self.graph, self.clock)
        self.clock.refresh()

    def _fire_special_events(self):
        """
        This method is used to simulate the special events outlined in
        the program requirements.

        The following special events are hardcoded into the method:

            1. At 8:00 AM, truck 1 is loaded and the truck status is
            switched to active.

            2. At 9:05 AM, The packages that were delayed are received.
            Truck 2 and 3 are loaded, Truck 2 status is switched to
            active.

            3. At 10:20 AM, Package #9's address is updated to reflect
            the corrected address

        :return: None

        Space Complexity:
            O(1)

        Time Complexity:
            O(1)
        """
        if self.clock.hour >= 8 and self.special_events.get("8:00 AM") is False:
            truck1 = Truck.truck_list[0]
            truck1.packages = [
                Package.package_list[14],  # (1) 13, 14, and 18
                Package.package_list[13],  # (2) Must be delivered with 14, 18
                Package.package_list[18],  # (3)
                Package.package_list[12],  # (4) Must be delivered with 15, 18
                Package.package_list[15],  # (5) Must be delivered with 12, 18
                Package.package_list[19],  # (6) Must be delivered with 12, 14
                Package.package_list[0],  # (7)
                Package.package_list[1],  # (8)
                Package.package_list[3],  # (9)
                Package.package_list[4],  # (10)
                Package.package_list[6],  # (11)
                Package.package_list[7],  # (12)
                Package.package_list[9],  # (13)
                Package.package_list[10],  # (14)
                Package.package_list[11],  # (15)
                Package.package_list[16]  # (16)
            ]
            truck1.set_packages()
            truck1.toggle_status()
            DeliveryController.special_events["8:00 AM"] = True

        if (self.clock.hour > 9 or (self.clock.hour == 9 and self.clock.minute >= 5)) and self.special_events.get(
                "9:05 AM") is False:
            truck2 = Truck.truck_list[1]
            truck3 = Truck.truck_list[2]

            cli.GUI.add_event("Delayed packages received at 9:05 AM")

            truck2.packages = [
                Package.package_list[5],  # (1)
                Package.package_list[24],  # (2)
                Package.package_list[2],  # (3)
                Package.package_list[17],  # (4)
                Package.package_list[35],  # (5)
                Package.package_list[37],  # (6)
                Package.package_list[20],  # (7)
                Package.package_list[21],  # (8)
                Package.package_list[22],  # (9)
                Package.package_list[23],  # (10)
                Package.package_list[25],  # (11)
                Package.package_list[26],  # (12)
                Package.package_list[28],  # (13)
                Package.package_list[24],  # (14)
                Package.package_list[27],  # (15)
                Package.package_list[31]  # (16)
            ]
            truck2.set_packages()
            truck2.toggle_status()

            truck3.packages = [
                Package.package_list[8],
                Package.package_list[29],
                Package.package_list[30],
                Package.package_list[32],
                Package.package_list[33],
                Package.package_list[34],
                Package.package_list[36],
                Package.package_list[38],
                Package.package_list[39]
            ]
            truck3.set_packages()

            DeliveryController.special_events["9:05 AM"] = True

        if (self.clock.hour > 10 or (self.clock.hour == 10 and self.clock.minute >= 20)) and self.special_events.get(
                "10:20 AM") is False:
            cli.GUI.add_event("Package #9's address was corrected to 410 S State St.")
            pkg = package.Package.package_list[8]
            pkg.address = "410 S State St"
            DeliveryController.special_events["10:20 AM"] = True

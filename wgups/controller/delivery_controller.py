from dataclasses import dataclass

from wgups.objects.hub import Hub
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

        truck1 = Truck.truck_list[0]
        truck2 = Truck.truck_list[1]
        truck3 = Truck.truck_list[2]
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

            # Truck 1
            Package.package_list[13].nearby_packages.append(Package.package_list[15])
            Package.package_list[13].nearby_packages.append(Package.package_list[14])
            Package.package_list[13].nearby_packages.append(Package.package_list[19])
            Package.package_list[13].nearby_packages.append(Package.package_list[20])
            Package.package_list[13].nearby_packages.append(Package.package_list[12])
            Package.package_list[39].nearby_packages.append(Package.package_list[3])
            Package.package_list[0].nearby_packages.append(Package.package_list[18])
            Package.package_list[0].nearby_packages.append(Package.package_list[11])

            # Truck 2
            Package.package_list[36].nearby_packages.append(Package.package_list[37])
            Package.package_list[36].nearby_packages.append(Package.package_list[8])
            Package.package_list[36].nearby_packages.append(Package.package_list[2])
            Package.package_list[29].nearby_packages.append(Package.package_list[9])
            Package.package_list[29].nearby_packages.append(Package.package_list[7])
            Package.package_list[29].nearby_packages.append(Package.package_list[2])







            # Package.package_list[13].nearby_packages = [
            #     Package.package_list[15],
            #     Package.package_list[14],
            #     Package.package_list[19],
            #     Package.package_list[20],
            #     Package.package_list[18],
            # ]
            #
            # Package.package_list[39].nearby_packages = [
            #     Package.package_list[3]
            # ]
            #
            # Package.package_list[0].nearby_packages = [
            #     Package.package_list[18],
            #     Package.package_list[11]
            #
            # ]

            truck1.priority_packages.append(Package.package_list[13])
            truck1.priority_packages.append(Package.package_list[30])
            truck1.priority_packages.append(Package.package_list[39])
            truck1.priority_packages.append(Package.package_list[0])

            for priority_package in truck1.priority_packages:
                for nearby_package in priority_package.nearby_packages:
                    truck1.packages.append(nearby_package)
                truck1.packages.append(priority_package)

            # truck2.priority_packages.append(Package.package_list[36])
            # truck2.priority_packages.append(Package.package_list[29])



            # for current_package in Package.package_list:
            #     if current_package not in truck1.packages and current_package not in truck2.packages:
            #         truck3.packages.append(current_package)

            truck1.toggle_status()


            DeliveryController.special_events["8:00 AM"] = True

        if (self.clock.hour > 9 or (self.clock.hour == 9 and self.clock.minute >= 5)) and self.special_events.get(
                "9:05 AM") is False:

            if not truck1.active or not truck3.active:
                cli.GUI.add_event("Delayed packages received at 9:05 AM")
                truck2.toggle_status()
                DeliveryController.special_events["9:05 AM"] = True

        if (self.clock.hour > 10 or (self.clock.hour == 10 and self.clock.minute >= 20)) and self.special_events.get(
                "10:20 AM") is False:
            cli.GUI.add_event("Package #9's address was corrected to 410 S State St.")
            pkg = Package.package_list[8]
            pkg.address = "410 S State St"
            DeliveryController.special_events["10:20 AM"] = True

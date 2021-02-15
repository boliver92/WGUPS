from dataclasses import dataclass
import wgups.objects.truck as truck
import wgups.ui.cli as cli
from wgups.ds.graph import Graph
from wgups.objects.clock import Clock
from wgups.utils.data_reader import read_hubs, read_packages, create_trucks, create_vertexes, connect_vertexes, \
    load_truck
import wgups.objects.package as package


@dataclass()
class DeliveryController:
    clock: Clock = Clock()
    special_events = {
        "8:00 AM": False,
        "9:05 AM": False,
        "10:20 AM": False
    }

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
        routes = Graph()
        read_hubs()
        read_packages()
        create_trucks()
        create_vertexes(routes)
        connect_vertexes(routes)

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
        print(self.clock)
        self.clock.add_minutes(5)

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
            load_truck(1)
            truck.Truck.truck_list[0].toggle_status()
            self.special_events["8:00 AM"] = True

        if (self.clock.hour > 9 or (self.clock.hour == 9 and self.clock.minute >= 5)) and self.special_events.get("9:05 AM") is False:
            cli.GUI.add_event("Delayed packages received at 9:05 AM")
            load_truck(2)
            load_truck(3)
            self.special_events["9:05 AM"] = True

        if (self.clock.hour > 10 or (self.clock.hour == 10 and self.clock.minute >= 20)) and self.special_events.get("9:05 AM") is False:
            cli.GUI.add_event("Package #9's address was corrected to 410 S State St.")
            pkg = package.Package.package_list[8]
            pkg.address = "410 S State St"
            self.special_events["10:20 AM"] = True

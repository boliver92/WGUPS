from typing import ClassVar
import os
import sys

import wgups.objects.clock as clk
import wgups.objects.package as pkg
import wgups.objects.truck as trk


class GUI:
    """A class used to represent the command-line interface GUI

    The goal of the class is to build the complete string GUI during
    each tick/frame and pushing it to the command-line at once.
    User input should interrupt the ticks to provide input

    ...

    Attributes
        package_string_list: ClassVar[list]
            A list that will hold the strings associated with the package
            information display of the GUI
        truck_string_list: ClassVar[list]
            A list that will hold the strings associated with the truck
            information display of the GUI
        running: bool
            Default: True

            A boolean variable indicating that the program is still
            active and that the main GUI loop should continue to
            run.
        ticks: int
            Default: 30

            The framerate/tickrate of the GUI.
    """
    package_string_list: list = []
    truck_string_list: list = []
    running: bool = True
    ticks: int = 2
    events: int = 10

    event_list: ClassVar[list] = []
    _string: ClassVar[str] = ""
    interrupted: ClassVar[bool] = False

    def __init__(self, clock: clk):
        self.clock = clock

    def tick(self, **kwargs):
        os.system("cls")

        """The main function for the GUI class.

        The function

        :return:
        """

        # Sets any variables passed into the run method.
        if len(kwargs) > 0:

            # Sets ticks/framerate
            if kwargs.get("ticks") is not None:
                self.ticks = kwargs.get("ticks")
                print(f"Ticks set to {self.ticks}")
            if kwargs.get("events") is not None:
                self.events = kwargs.get("events")

        # Loop that controls the GUI display
        self.flush()
        self._build_package_display()
        self._build_truck_display()
        self._build_event_display()
        self._build_time_display()
        self._build_user_input_display()
        self.clear()
        self.display()

    def _set_space(self, string: str, spacing: int) -> str:
        """
        Creates additional whitespace after a string if the string
        length is less than a desired length.

        :param string: The string to add the whitespace to
        :param spacing: The total desired length of the string
        :return:
            Original string with additional white spacing added to the
            end to meet the length requirements.
        """
        spaces = spacing - len(string)
        if spaces > 0:
            for i in range(spaces):
                string += " "

        return string

    def _build_event_display(self):
        list_length = len(GUI.event_list)
        if list_length <= self.events:
            GUI._string += "\n"
            for event in GUI.event_list:
                GUI._string += f"{event}\n"
        else:
            GUI._string += "\n"
            spliced_list = GUI.event_list[list_length - self.events::]
            for event in spliced_list:
                GUI._string += f"{event}\n"

    def _build_package_display(self, new_line_index: int = 6, **kwargs):
        """
        Iterates through Package.package_list and populates the
        GUI._string with each package information.

        :param new_line_index: Where to place a \n escape character in the
        string
        :return:
        """
        for i, package in enumerate(pkg.Package.package_list):
            # TODO: Provide kwargs to further set design options
            GUI._string += self._set_space(
                f"{self._set_space(f'Package {package.id}:', 11)} {package.delivery_status.value}",
                45
            )
            if (i + 1) % new_line_index == 0:
                GUI._string += "\n"

        GUI._string += "\n\n"

    def _build_single_package_display(self, package: pkg.Package):
        GUI._string += f"Package ID: {package.id}\n" \
                       f"Delivery Address: {package.address}\n" \
                       f"Delivery Deadline: {package.delivery_deadline}\n" \
                       f"Delivery City: {package.city}\n" \
                       f"Delivery Zip Code: {package.zip}\n" \
                       f"Package Weight: {package.weight}\n" \
                       f"Delivery Status: {package.delivery_status.value}\n"

    def _build_time_display(self):
        GUI._string += f"\n\u001b[31;1mCurrent Time: {self.clock}\u001b[0m"

    def _build_truck_display(self):
        """
        Iterates through Truck.truck_list and populates the GUI._string
        with each truck info.
        :return:
        """

        # Creates the underlined header for each truck.
        for truck in trk.Truck.truck_list:
            GUI._string += self._set_space(f"\033[4mTruck {truck.id}\033[0m", 68)

        GUI._string += "\n"

        for truck in trk.Truck.truck_list:
            GUI._string += self._set_space(f"Current Location: \u001b[34m{truck.current_hub.name}\u001b[0m", 69)
        GUI._string += "\n"

        for truck in trk.Truck.truck_list:
            GUI._string += self._set_space(f"Status: \u001b[34m{truck.status.value}\u001b[0m", 78)
        GUI._string += "\n"

        for truck in trk.Truck.truck_list:
            GUI._string += self._set_space(f"Total Miles Driven: \u001b[34m{truck.truck_miles}\u001b[0m", 69)
        GUI._string += "\n"

        for truck in trk.Truck.truck_list:
            pkg1: pkg.Package = truck.current_package
            if pkg1 is not None:
                GUI._string += self._set_space(
                    f"Currently Delivering: \u001b[34mPackage {truck.current_package.id}\u001b[0m", 69)
            else:
                GUI._string += self._set_space(f"Currently Delivering: \u001b[31mNone\u001b[0m", 69)

        GUI._string += "\n\n"

        for i in range(len(trk.Truck.truck_list)):
            GUI._string += self._set_space("----Truck Inventory----", 61)
        GUI._string += "\n"

        # List the remaining packages under each truck.
        for i in range(16):
            try:
                truck1_package = trk.Truck.truck_list[0].packages[i]
            except IndexError:
                truck1_package = None
            try:
                truck2_package = trk.Truck.truck_list[1].packages[i]
            except IndexError:
                truck2_package = None
            try:
                truck3_package = trk.Truck.truck_list[2].packages[i]
            except IndexError:
                truck3_package = None

            # Breaks the loop If there no more packages in any of the
            # package list
            if truck1_package is None and truck2_package is None and truck3_package is None:
                GUI._string += "\n"
                break

            if truck1_package is not None:
                GUI._string += self._set_space(f"Package {truck1_package.id}: {truck1_package.address}", 60)
            if truck2_package is not None:
                GUI._string += self._set_space(f"Package {truck2_package.id}: {truck2_package.address}", 60)
            if truck3_package is not None:
                GUI._string += self._set_space(f"Package {truck3_package.id}: {truck3_package.address}", 60)

            GUI._string += "\n"

    def _build_user_input_display(self):
        GUI._string += "\n\u001b[36;1mPress Ctrl+C to search package details.\u001b[0m" \
                       "\n\u001b[31mPress ESC to exit the program.\u001b[0m"

    def clear(self):
        """
        Clears the terminal
        """
        os.system("cls")

    def display(self):
        """ Displays the built string in the terminal.

        :return:
        """
        print(GUI._string)

    def exit(self):
        """ Stops the GUI run method loop and closes the program
        :return:
        """
        self.running = False
        sys.exit()

    def flush(self):
        """
        Clears GUI._string to prepare it to be populated with the next output stream
        """
        GUI._string = ""

    def show_package(self, package: pkg.Package):
        self.flush()
        self._build_single_package_display(package)
        self.clear()
        self.display()

    @classmethod
    def add_event(cls, event: str):
        GUI.event_list.append(event)

from wgups.ds.hashmap import Hashmap
from wgups.enums.delivery_status import DeliveryStatus
from wgups.objects.clock import Clock


class Package(object):
    pass


class Package:
    """ A Package class to represent a package.

    The package class will be used to hold the package details of each
    package to be delivered.

    ...

    Attributes
        id: int
            The unique ID associated with the package.
        address: str
            The address of the hub where the package should be
            delivered.
        city: str
            The city of the hub where the package should be
            delivered.
        state: str
            The state of the hub where the package should be
            delivered.
        zip: int
            The zipcode of the hub where the package should be
            delivered.
        delivery_deadline: str
            The delivery deadline for the package.
        weight: int
            The total weight of the package.
        special_notes: str
            Special notes associated with the package.
        delivery_status: DeliveryStatus
            default = DeliveryStatus.LOADING
            The current delivery status of the package.
    """

    # Class Variables
    master_package_list = []
    _find_by_id = Hashmap()

    def __init__(self, id: int, address: str, city: str, state: str, zip: int, delivery_deadline: str, weight: int,
                 special_notes: str, delivery_status: DeliveryStatus = DeliveryStatus.LOADING):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.delivery_deadline = delivery_deadline
        self.weight = weight
        self.special_notes = special_notes
        self.delivery_status = delivery_status
        if "Delayed" in self.special_notes:
            self.delivery_status = DeliveryStatus.DELAYED
        self.last_status_update: str = None
        self.event_list = []

        Package._find_by_id.put(self.id, self)
        Package.master_package_list.append(self)

        self.set_last_status_update(Clock(480))

    def add_event(self, event: tuple):
        """Adds an event to the package event_list

        The event tuple is added to the event list, the event list is
        then sorted based on the 2nd tuple value (int)

        :param event: tuple(str, int) of the event to be added. The str
        should be a string representation of the event. The int should
        be the clock.total_minute when the event occured.

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """
        self.event_list.append(event)
        sorted(self.event_list, key=lambda event_time: event_time[1])

    def set_last_status_update(self, clock: Clock):
        """Sets the package's last status update and adds the status update to the package's event list.

        :param clock: The clock being utilized when the status update
        is being updated.

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """
        self.last_status_update = f"{self.delivery_status.value} @ {clock}"
        self.add_event((f"{self.last_status_update}", clock.total_minutes))

    @classmethod
    def find_by_id(cls, id: int) -> Package:
        """ Returns the package with the associated package ID.

        Uses a hashmap to search the key and returns the value. The key
        is the package ID to be searched. If the key is found, the
        value is the package object associated with tbe key

        :param id: int ID of the package to be found.
        :return: Package if the ID is found. Otherwise none.

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """
        return Package._find_by_id.get(id)

    def __repr__(self):
        return f"\u001b[35mPackage {self.id}\u001b[0m"

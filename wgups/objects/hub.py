from wgups.ds.hashmap import Hashmap


class Hub(object):
    pass


class Hub:
    """
    Class to represent each Hub that our trucks will be delivering packages to.

    ...

    Attributes

        name: str
            The name of the HUB

        address: str
            The address of the HUB
    """

    master_hub_list = []
    _find_by_name_map = Hashmap()
    _find_by_address_map = Hashmap()

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address

        self._find_by_address_map.put(self.address, self)
        self._find_by_name_map.put(self.name, self)

    @classmethod
    def find_by_address(cls, address: str) -> Hub:
        """
        Takes a string address of a Hub object to be found. The search
        method uses a hashmap
        :param address: The address of the hub to be found
        :return: Hub object if it is found. Otherwise, None.

        Space Complexity:
            O(1)

        Time Complexity:
            O(1)
        """

        return Hub._find_by_address_map.get(address)

    @classmethod
    def find_by_name(cls, name: str) -> Hub:
        """
        Takes a string name of a Hub object to be found. The search
        method uses a hashmap
        :param name: The name of the hub to be found
        :return: Hub object if it is found. Otherwise, None.

        Space Complexity:
            O(1)

        Time Complexity:
            O(1)
        """

        return Hub._find_by_name_map.get(name)

    def __repr__(self):
        return f"HUB: {self.name}, ADDRESS: {self.address}"

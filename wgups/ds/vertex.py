from wgups.ds.hashmap import Hashmap


class Vertex(object):
    pass


class Vertex:
    vertex_master_list = []
    _find_by_label = Hashmap()
    _find_by_address = Hashmap()

    def __init__(self, label, address):
        self.label = label
        self.address = address

        Vertex._find_by_label.put(self.label, self)
        Vertex._find_by_address.put(self.address, self)


    @classmethod
    def find_by_label(cls, label: str) -> Vertex:
        """ Returns the vertex with the associated label.

        Uses a hashmap to search the key and returns the value. The key
        is the vertex label to be searched. If the key is found, the
        value is the vertex object associated with tbe key

        :param label: str label of the vertex to be found.
        :return: Vertex if the label is found. Otherwise none.

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """
        return Vertex._find_by_label.get(label)

    @classmethod
    def find_by_address(cls, address: str) -> Vertex:
        """ Returns the vertex with the associated label.

        Uses a hashmap to search the key and returns the value. The key
        is the vertex address to be searched. If the key is found, the
        value is the vertex object associated with tbe key

        :param address: str address of the vertex to be found.
        :return: Vertex if the address is found. Otherwise none.

        Space Complexity
            O(1)
        Time Complexity
            O(1)
        """

        return Vertex._find_by_address.get(address)

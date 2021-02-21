from wgups.ds.hashmap import Hashmap


class Vertex(object):
    pass


class Vertex:
    vertex_list = []
    _find_by_label = Hashmap()
    _find_by_address = Hashmap()

    def __init__(self, label, address):
        self.label = label
        self.address = address

        Vertex._find_by_label.put(self.label, self)
        Vertex._find_by_address.put(self.address, self)

    @classmethod
    def find_by_label(cls, label: str) -> Vertex:
        return Vertex._find_by_label.get(label)

    @classmethod
    def find_by_address(cls, address: str) -> Vertex:
        return Vertex._find_by_address.get(address)

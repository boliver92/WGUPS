class Vertex:
    vertex_list = []

    def __init__(self, label):
        self.label = label
        self.distance = float('inf')
        self.pred_vertex = None
        Vertex.vertex_list.append(self)
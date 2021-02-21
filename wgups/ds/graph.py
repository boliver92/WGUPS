class Graph:

    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}

    def add_vertex(self, new_vertex):
        """Adds a vertex to the graph's adjacency list

        :param new_vertex: The vertex to add to the adjacency dict

        Space Complexity:
            O(1)
        Time Complexity:
            O(1)
        """
        self.adjacency_list[new_vertex] = []

    def add_directed_edge(self, from_vertex, to_vertex, weight=1.0):
        """Adds a edge weight as a value to the graph's edge weights dict using a (from_vertex, to_vertex) tuple as the key

        :param from_vertex: The beginning vertex.
        :param to_vertex: The ending vertex.
        :param weight: The total distance to travel from the
        from_vertex to the to_vertex

        Space Complexity:
            O(1)
        Time Complexity:
            O(1)
        """
        self.edge_weights[(from_vertex, to_vertex)] = weight
        self.adjacency_list[from_vertex].append(to_vertex)

    def add_undirected_edge(self, vertex_a, vertex_b, weight=1.0):
        """Creates two directed edges connecting vertex_a and vertex_b with no limitation on direction

        :param vertex_a: The first vertex to connect
        :param vertex_b: The second vertex to connect
        :param weight: The weight/distance of the edge.

        Space Complexity
            O(1)
        Time Complexity:
            O(1)
        """
        self.add_directed_edge(vertex_a, vertex_b, weight)
        self.add_directed_edge(vertex_b, vertex_a, weight)


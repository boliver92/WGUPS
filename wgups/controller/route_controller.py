from wgups.ds.graph import Graph
from wgups.ds.vertex import Vertex


class RouteController(Graph):
    visited_vertices = []

    def __init__(self):
        super().__init__()

    def get_nearest_unvisited_neighbor(self, start_vertex: Vertex) -> Vertex:
        """Returns the closest unvisited vertex to the start_vertex

        This method returns the closest vertex to the start_vertex in
        the object's adjacency list. Once the closest vertex has been
        returned, it is appended to the
        RouteController.visited_vertices and will not be visited again
         in future method calls.
        :param start_vertex: The starting vertex when searching for
        the nearest neighbor.
        :return: The nearest vertex that has not been visited.

        Space Complexity
            O(1)
        Time Complexity
            O(n^2)
        """
        nearest_neighbor: Vertex = None
        min_distance = 1000.0
        for neighbor_vertex in self.adjacency_list[start_vertex]:
            if neighbor_vertex in RouteController.visited_vertices:
                continue
            distance = self.edge_weights[(start_vertex, neighbor_vertex)]
            if distance < min_distance:
                min_distance = distance
                nearest_neighbor = neighbor_vertex

        RouteController.visited_vertices.append(nearest_neighbor)
        return nearest_neighbor

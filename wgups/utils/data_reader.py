from wgups.ds.graph import Graph
from wgups.ds.vertex import Vertex
from wgups.objects.package import Package
from wgups.objects.hub import Hub
from wgups.objects.map_manager import MapManager
import csv


def read_packages():
    with open("./data/WGUPS Package File.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            package = Package(int(row["Package ID"]),
                              row["Address"],
                              row["City"],
                              row["State"],
                              int(row["Zip"]),
                              row["Delivery Deadline"],
                              int(row["Mass KILO"]),
                              row["Special Notes"])

        csv_file.close()


def read_hubs():
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        for row in list(csv_reader):
            Hub(row["Name"], row["Address"])

    csv_file.close()


def create_vertexes(graph: Graph):
    for hub in Hub.hub_list:
        vertex = Vertex(hub.name)
        graph.add_vertex(vertex)
        hub.vertex = vertex


def connect_vertexes(graph: Graph):
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        keys = list(csv_reader.fieldnames)[2:]

        for row in csv_reader:
            hub_a = MapManager.name_to_hub_map.get(row["Name"])
            vertex_a = hub_a.vertex
            for key in keys:
                hub_b = MapManager.name_to_hub_map.get(key)
                if hub_a == hub_b:
                    continue
                vertex_b = hub_b.vertex
                try:
                    distance = float(row[f"{key}"])
                except ValueError:
                    continue
                if distance == 0.0 or vertex_a == vertex_b or distance == "" or distance is None:
                    continue
                else:
                    graph.add_undirected_edge(vertex_a, vertex_b, distance)

    csv_file.close()

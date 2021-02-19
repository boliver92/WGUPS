from wgups.ds.graph import Graph, dijkstra_shortest_path, get_shortest_path
from wgups.ds.vertex import Vertex
from wgups.enums.delivery_status import DeliveryStatus
from wgups.objects.package import Package
from wgups.objects.hub import Hub
from wgups.objects.map_manager import MapManager
import csv
from wgups.objects.truck import Truck


def read_packages():
    with open("./data/WGUPS Package File.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            pkg = Package(id=int(row["Package ID"]),
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    zip=int(row["Zip"]),
                    delivery_deadline=row["Delivery Deadline"],
                    weight=int(row["Mass KILO"]),
                    special_notes=row["Special Notes"])

        csv_file.close()


def read_hubs():
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        for row in list(csv_reader):
            Hub(row["Name"], row["Address"], Vertex(label=row["Name"]))

    csv_file.close()


def create_vertices(graph: Graph):
    for hub in Hub.hub_list:
        graph.add_vertex(hub.vertex)

    # with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
    #     csv_reader = csv.DictReader(csv_file, delimiter=",")
    #     keys = csv_reader.fieldnames[2:]
    #
    #     for key in keys:
    #         new_vertex = Vertex(label=key)
    #         graph.add_vertex(new_vertex)
    #         hub = MapManager.name_to_hub_map.get(new_vertex.label)
    #         hub.vertex = new_vertex


def connect_vertices(graph: Graph):
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        keys = list(csv_reader.fieldnames)[2:]

        for row in csv_reader:
            for vertex in Vertex.vertex_list:
                if vertex.label == row["Name"]:
                    vertex_a = vertex
                    break
            for key in keys:
                for vertex in Vertex.vertex_list:
                    if vertex.label == key:
                        vertex_b = vertex

                        distance = float(row[f'{key}'])
                        graph.add_directed_edge(vertex_a, vertex_b, distance)

    csv_file.close()

    for vertex1 in Vertex.vertex_list:
        dijkstra_shortest_path(graph, vertex1)


def create_trucks(trucks_to_create: int = 3):
    for i in range(trucks_to_create):
        Truck(i + 1)

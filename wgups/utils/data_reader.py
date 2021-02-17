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
            Package(id=int(row["Package ID"]),
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
            Hub(row["Name"], row["Address"])

    csv_file.close()


def create_vertices(graph: Graph):
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        keys = csv_reader.fieldnames[2:]

        for key in keys:
            new_vertex = Vertex(label=key)
            graph.add_vertex(new_vertex)
            hub = MapManager.name_to_hub_map.get(new_vertex.label)
            hub.vertex = new_vertex


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
        for vertex2 in Vertex.vertex_list:
            print(f"Start Vertex: {vertex1.label}\nEnd Vertex: {vertex2.label}")
            print(get_shortest_path(vertex1, vertex2))
            print(f"Distance: {vertex2.distance}")


def load_truck(truck_to_load):
    if truck_to_load == 1:
        Truck.truck_list[0].set_packages([
            Package.package_list[14],  # (1) 13, 14, and 18
            Package.package_list[13],  # (2) Must be delivered with 14, 18
            Package.package_list[18],  # (3)
            Package.package_list[12],  # (4) Must be delivered with 15, 18
            Package.package_list[15],  # (5) Must be delivered with 12, 18
            Package.package_list[19],  # (6) Must be delivered with 12, 14
            Package.package_list[0],  # (7)
            Package.package_list[1],  # (8)
            Package.package_list[3],  # (9)
            Package.package_list[4],  # (10)
            Package.package_list[6],  # (11)
            Package.package_list[7],  # (12)
            Package.package_list[9],  # (13)
            Package.package_list[10],  # (14)
            Package.package_list[11],  # (15)
            Package.package_list[16]  # (16)
        ])

    if truck_to_load == 2:
        Truck.truck_list[1].set_packages([
            Package.package_list[5],  # (1)
            Package.package_list[24],  # (2)
            Package.package_list[2],  # (3)
            Package.package_list[17],  # (4)
            Package.package_list[35],  # (5)
            Package.package_list[37],  # (6)
            Package.package_list[20],  # (7)
            Package.package_list[21],  # (8)
            Package.package_list[22],  # (9)
            Package.package_list[23],  # (10)
            Package.package_list[25],  # (11)
            Package.package_list[26],  # (12)
            Package.package_list[28],  # (13)
            Package.package_list[24],  # (14)
            Package.package_list[27],  # (15)
            Package.package_list[31]  # (16)
        ])

    if truck_to_load == 3:
        Truck.truck_list[2].set_packages([
            Package.package_list[8],
            Package.package_list[29],
            Package.package_list[30],
            Package.package_list[32],
            Package.package_list[33],
            Package.package_list[34],
            Package.package_list[36],
            Package.package_list[38],
            Package.package_list[39]
        ])

    for truck in Truck.truck_list:
        for package in truck.packages:
            package.delivery_status = DeliveryStatus.LOADED


def create_trucks(trucks_to_create: int = 3):
    for i in range(trucks_to_create):
        Truck(i + 1)

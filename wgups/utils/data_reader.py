from wgups.controller.route_controller import RouteController
from wgups.ds.vertex import Vertex
from wgups.objects.package import Package
from wgups.objects.hub import Hub
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


def create_hubs_and_vertices(route_controller: RouteController):
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        for row in list(csv_reader):
            Hub(row["Name"], row["Address"])
            route_controller.add_vertex(Vertex(row["Name"], row["Address"]))

    csv_file.close()


def connect_vertices(route_controller: RouteController):
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        keys = list(csv_reader.fieldnames)[2:]

        for row in csv_reader:
            vertex_a = Vertex.find_by_label(row["Name"])
            for key in keys:
                vertex_b = Vertex.find_by_label(f"{key}")
                distance = float(row[f'{key}'])
                if distance > 0.0:
                    route_controller.add_directed_edge(vertex_a, vertex_b, distance)

    csv_file.close()


def create_trucks(trucks_to_create: int = 3):
    for i in range(trucks_to_create):
        Truck(i + 1)

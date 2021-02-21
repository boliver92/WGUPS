from wgups.controller.route_controller import RouteController
from wgups.ds.vertex import Vertex
from wgups.objects.package import Package
from wgups.objects.hub import Hub
import csv
from wgups.objects.truck import Truck


def create_hubs_and_vertices(route_controller: RouteController):
    """
    Reads the distance file and creates a hub and vertex object for
    each hub in the distance file.
    :param route_controller: The graph to add the vertex to.

    Space Complexity
        O(n)
    Time Complexity
        O(n)
    """

    # Open CSV file
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:

        # Create a dict from file details
        csv_reader = csv.DictReader(csv_file, delimiter=",")

        # Read through each row int the file and create a hub and vertex
        # object
        for row in list(csv_reader):
            Hub(row["Name"], row["Address"])
            route_controller.add_vertex(Vertex(row["Name"], row["Address"]))

        # Close the CSV file.
        csv_file.close()


def create_trucks(trucks_to_create: int = 3):
    """
    Creates a truck object for each trucks_to_create.
    :param trucks_to_create: The number of trucks to create. Default: 3

    Space Complexity
        O(1)
    Time Complexity
        O(n)
    """

    # Keep creating truck objects until you reach the required trucks
    # to create
    for i in range(trucks_to_create):
        Truck(i + 1)


def connect_vertices(route_controller: RouteController):
    """
    Connects each existing vertex with all existing vertices using a
    weighted directed edge.
    :param route_controller: The graph containing the vertices

    Space Complexity
        O(n)
    Time Complexity
        O(n^2)
    """
    # Open the CSV file
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:

        # Create a dict from the CSV filee.
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        # Collect all headers in a list from index 2 to the end to use
        # later.
        keys = list(csv_reader.fieldnames)[2:]

        # Iterate through each row in the dictionary and add a weighted
        # directed edge from the entry's related vertex to all other
        # vertices.
        for row in csv_reader:
            vertex_a = Vertex.find_by_label(row["Name"])
            for key in keys:
                vertex_b = Vertex.find_by_label(f"{key}")
                distance = float(row[f'{key}'])
                if distance > 0.0:
                    route_controller.add_directed_edge(vertex_a, vertex_b, distance)

        # Close the CSV file
        csv_file.close()


def read_packages():
    """
    Creates a package object from each package in the WGUPS pakage file

    Space Complexity
        O(n)
    Time Complexity
        O(n)
    """
    # Open the CSV file
    with open("./data/WGUPS Package File.csv", mode='r', encoding='utf-8-sig') as csv_file:

        # Create a dict from the CSV file.
        csv_reader = csv.DictReader(csv_file)

        # Iterate through each entry in the CSV file and create a
        # package object from the entry.
        for row in csv_reader:
            Package(id=int(row["Package ID"]),
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    zip=int(row["Zip"]),
                    delivery_deadline=row["Delivery Deadline"],
                    weight=int(row["Mass KILO"]),
                    special_notes=row["Special Notes"])

        # Close the CSV file.
        csv_file.close()

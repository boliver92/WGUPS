from wgups.ds.graph import Graph
from wgups.objects.map_manager import MapManager
from wgups.utils.data_reader import read_packages, read_hubs, create_vertexes, connect_vertexes
from wgups.ui.cli import GUI
from wgups.objects.truck import Truck
from wgups.objects.package import Package
from wgups.enums.delivery_status import DeliveryStatus


def create_trucks(trucks_to_create: int = 3):
    for i in range(trucks_to_create):
        Truck(i + 1)

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

    # This truck will be loaded 5 packages short initially to account
    # for delayed packages.
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
        Package.package_list[31]   # (16)
    ])

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


DEBUG = False

if __name__ == '__main__':

    routes = Graph()
    read_hubs()
    read_packages()
    create_trucks()
    create_vertexes(routes)
    connect_vertexes(routes)

    if DEBUG:
        pass
    else:
        cli = GUI()
        cli.run()

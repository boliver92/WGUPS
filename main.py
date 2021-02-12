from wgups.utils.data_reader import read_packages, load_hubs
from wgups.ui.cli import GUI
from wgups.objects.truck import Truck
from wgups.objects.package import Package


def create_trucks(trucks_to_create: int = 3):
    for i in range(trucks_to_create):
        print(Truck(id=i + 1))

    Truck.truck_list[0].set_packages([

    ])
    Truck.truck_list[1].set_packages([
        Package.package_list[2],
        Package.package_list[17],
        Package.package_list[35],
        Package.package_list[37]
    ])

if __name__ == '__main__':
    read_packages()
    create_trucks()

    #cli = GUI()
    #cli.run()
from wgups.ds.hashtable import HashTable
from wgups.ds.binary_search_tree import BinarySearchTree
from wgups.ds.bst_node import BSTNode
from wgups.objects.package import Package
from wgups.objects.hub import Hub
from wgups.ds.hashmap import HashMap
import csv


def load_packages():
    with open("./data/WGUPS Package File.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            package = Package(int(row["Package ID"]),
                              row["Address"],
                              row["City"],
                              row["State"],
                              int(row["Zip"]),
                              int(row["Mass KILO"]),
                              row["Delivery Deadline"],
                              row["Special Notes"])

        csv_file.close()


def load_hubs():
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        keys = reversed(csv_reader.fieldnames[2:])
        print(csv_reader)

        for row in reversed(list(csv_reader)):
            hub = Hub(row["Name"], row["Address"])
            for key in keys:
                if len(key) > 0:
                    hub.set_distance_map(key, row[key])
    csv_file.close()

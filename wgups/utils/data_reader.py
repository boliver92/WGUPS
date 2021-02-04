from wgups.ds.hashmap import Hashmap
from wgups.objects.package import Package
import csv

def load_packages() -> Hashmap:
    hashmap = Hashmap(10)
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
            hashmap.insert(package)

    csv_file.close()
    return hashmap
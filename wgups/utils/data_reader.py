from wgups.objects.package import Package
from wgups.objects.hub import Hub
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
        keys = reversed(csv_reader.fieldnames[2:])
        print(csv_reader)

        for row in list(csv_reader):
            Hub(row["Name"], row["Address"])

    csv_file.close()

from wgups.objects.package import Package
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


def load_hubs():
    with open("./data/WGUPS Distance Table.csv", mode='r', encoding='utf-8-sig') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=",")
        keys = reversed(csv_reader.fieldnames[2:])
        print(csv_reader)

        # for row in reversed(list(csv_reader)):
        #     hub = Hub(row["Name"], row["Address"])
        #     for key in keys:
        #         if len(key) > 0:
        #             hub.set_distance_map(key, row[key])
    csv_file.close()

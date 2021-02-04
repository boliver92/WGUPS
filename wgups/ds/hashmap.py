class Hashmap:
    hashmap = []

    def __init__(self, size: int):
        for i in range(size):
            self.hashmap.append([])

    def insert(self, item):
        bucket = hash(item) % len(self.hashmap)
        self.hashmap[bucket].append(item)

    def search(self, key):
        bucket = hash(key) % len(self.hashmap)
        bucket_list = self.hashmap[bucket]

        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None

    def remove(self, key):
        bucket = hash(key) % len(self.hashmap)
        bucket_list = self.hashmap[bucket]

        if key in bucket_list:
            bucket_list.remove(key)

    def print_hashmap(self):
        print(self.hashmap)
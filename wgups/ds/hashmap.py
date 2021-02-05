class HashMap:

    def __init__(self, size: int=10):
        self.hashmap = []
        for i in range(size):
            self.hashmap.append([])
        self.size = size

    def insert(self, key, value):
        bucket = hash(key) % len(self.hashmap)
        self.hashmap[bucket].append((key, value))

    def get_value_or_default(self, key, default=None):
        bucket = hash(key) % len(self.hashmap)
        bucket_list = self.hashmap[bucket]

        for k, v in bucket_list:
            if k == key:
                return v
        else:
            return default

    def remove(self, key):
        bucket = hash(key) % len(self.hashmap)
        bucket_list = self.hashmap[bucket]

        if key in bucket_list:
            k, v = key
            if k == key:
                bucket_list.remove(key)

    def print_hashmap(self):
        for row in self.hashmap:
            for entry in row:
                print(entry)

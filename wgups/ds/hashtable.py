class HashTable:

    def __init__(self, size: int=10):
        self.hashtable = []
        for i in range(size):
            self.hashtable.append([])
        self.size = size

    def insert(self, item):
        bucket = hash(item) % len(self.hashtable)
        self.hashtable[bucket].append(item)

    def search(self, key):
        bucket = hash(key) % len(self.hashtable)
        bucket_list = self.hashtable[bucket]

        if key in bucket_list:
            item_index = bucket_list.index(key)
            return bucket_list[item_index]
        else:
            return None

    def remove(self, key):
        bucket = hash(key) % len(self.hashtable)
        bucket_list = self.hashtable[bucket]

        if key in bucket_list:
            bucket_list.remove(key)

    def print_hashmap(self):
        for row in self.hashtable:
            for entry in row:
                print(entry)
class Hashmap:

    def __init__(self, size: int = 10):
        """

        :param size:
        """
        self.hashmap: list = []
        self.size = size
        for i in range(size):
            self.hashmap.append([])

    def put(self, key, value):
        """Inserts a key, value pair into the hashmap.

        Inserts a key, value pair into the hashmap. If the key already
        exists in the hashmap, it will be overridden.

        :param key: The key to be searched
        :param value: The value to be associated with the key

        Space Complexity
            O(n)
        Time Complexity
            O(Log(n))
        """

        # Obtains the index of bucket list that should contain the key
        # and assigns list to bucket_list
        bucket = hash(key) % self.size
        bucket_list = self.hashmap[bucket]

        # Searches for the key in the bucket_list. If the key is found,
        # key_exists is changed to True
        key_exists = False
        for index, entry in enumerate(bucket_list):
            entry_key, entry_val = entry

            if entry_key == key:
                key_exists = True
                break

        # If the key exists, overwrite with the new value. Otherwise,
        # append the new key, value pair to the bucket_list
        if key_exists:
            bucket_list[index] = (key, value)
        else:
            bucket_list.append((key, value))

    def get(self, key):
        """
        Returns the value of a specific key.

        :param key: The key to be searched
        :return: value of the key if the key exists. Otherwise, None.

        Space Complexity
            O(n)
        Time Complexity
            O(Log(n))
        """

        # Obtains the index of bucket list that should contain the key
        # and assigns list to bucket_list
        bucket = hash(key) % self.size
        bucket_list = self.hashmap[bucket]

        for entry in bucket_list:
            entry_key, entry_value = entry

            if entry_key == key:
                return entry_value

        return None

    def get_or_default(self, key, default=None):
        """
        Returns the value of a specific key. If a value is not found
        then return the default parameter

        :param key: The key to be searched
        :param default: The value to be returned if the key is not found.
        :return: value of the key if the key exists. Otherwise, the
        default value will be returned.

        Space Complexity
            O(n)
        Time Complexity
            O(Log(n))
        """

        # Obtains the index of bucket list that should contain the key
        # and assigns list to bucket_list
        bucket = hash(key) % self.size
        bucket_list = self.hashmap[bucket]

        found_key = False
        for index, entry in enumerate(bucket_list):
            entry_key, entry_value = entry

            if entry_key == key:
                found_key = True
                break

        if found_key:
            return entry_value
        else:
            return default

    def remove(self, key) -> bool:
        """
        Removes a key, value pair for the Hashmap if the key exists.

        :param key: The key of the key, value pair.
        :return: True if the key was found and removed. Otherwise, False.

        Space Complexity
            O(n)
        Time Complexity
            O(Log(n))
        """

        # Obtains the index of bucket list that should contain the key
        # and assigns list to bucket_list
        bucket = hash(key) % self.size
        bucket_list = self.hashmap[bucket]

        found_key = False
        for index, entry in enumerate(bucket_list):
            entry_key, entry_val = entry

            if entry_key == key:
                found_key = True
                break

        if found_key:
            bucket_list.pop(index)
            return True
        else:
            return False

    def __str__(self):
        return "".join(str(item) for item in self.hashmap)
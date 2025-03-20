from datetime import datetime, timedelta

class HashTable:
    # initializes a hashtable with a given capacity and double hashing parameters.
    def __init__(self, initial_capacity=40, c1=0, c2=1):
        self.initial_capacity = initial_capacity
        self.package_table = [None] * initial_capacity  # table to store packages
        self.bucket_status_table = ["EMPTY_SINCE_START"] * initial_capacity  # tracks if bucket is empty
        self.c1 = c1  # first constant for double hashing
        self.c2 = c2  # second constant for double hashing

    # insert a package into the hash table using double hashing for collision resolution.
    def insert(self, package):
        i = 0  # variable to track the number of probes
        buckets_probed = 0  # counter for the number of probes made
        N = len(self.package_table)  # number of buckets in the table
        bucket = hash(package.id_number) % N  # initial bucket index based on package id

        # attempt to find an empty bucket to insert the package
        while buckets_probed < N:
            # if the bucket is empty or available for removal, insert the package
            if self.bucket_status_table[bucket] in ["EMPTY_SINCE_START", "EMPTY_AFTER_REMOVAL"]:
                self.package_table[bucket] = package
                self.bucket_status_table[bucket] = "OCCUPIED"
                return True

            # update the bucket index using double hashing
            i += 1
            bucket = (hash(package.id_number) + (self.c1 * i) + (self.c2 * i ** 2)) % N
            buckets_probed += 1

        # if no empty bucket is found, resize the table and reinsert the package
        self.resize()
        self.insert(package)
        return True

    # search for a package by its key (package id).
    def lookup(self, key):
        attempt = 0  # number of probes for searching
        checked_buckets = 0  # probes made during the lookup
        table_size = len(self.package_table)  # number of buckets in the table
        bucket = hash(key) % table_size  # initial bucket index for the lookup

        # search through the hash table
        while self.bucket_status_table[bucket] != "EMPTY_SINCE_START" and checked_buckets < table_size:
            # if the package is found, return it
            if self.package_table[bucket] and self.package_table[bucket].id_number == key:
                return self.package_table[bucket]

            # update the bucket index using double hashing
            attempt += 1
            bucket = (hash(key) + self.c1 * attempt + self.c2 * attempt ** 2) % table_size
            checked_buckets += 1

        # return None if the package is not found
        return None

    # resize the hash table to accommodate more packages by doubling its capacity.
    def resize(self):
        # create a new hash table with double the initial capacity
        resizedHT = HashTable(initial_capacity=self.initial_capacity * 2, c1=self.c1, c2=self.c2)

        # reinsert all packages from the current table into the resized table
        for package in self.package_table:
            if package:
                resizedHT.insert(package)

        # update the hash table with the resized version
        self.initial_capacity = resizedHT.initial_capacity
        self.package_table = resizedHT.package_table
        self.bucket_status_table = resizedHT.bucket_status_table

    # generate a string representation of the hash table for display.
    def __str__(self):
        # start building the string to display the table
        tablestring = "   --------\n"
        for index, item in enumerate(self.package_table):
            # if the bucket is empty, display 'E'; otherwise, display the package
            value = str(item) if item else 'E'
            tablestring += '{:2}:|{:^6}|\n'.format(index, value)
        tablestring += "   --------"
        return tablestring

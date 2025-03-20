from datetime import timedelta

class Truck:
    # constants for truck properties
    avg_speed = 18  # default miles per hour
    maxpckgs = 16  # max packages the truck can carry

    def __init__(self, truck_id, mph=avg_speed, max_num_packages=maxpckgs):
        # Initializing truck properties
        self.id = truck_id
        self.packages_id_list = []
        self.mph = mph
        self.maxpckgs = max_num_packages
        self.total_distance_traveled = 0
        self.mileage_timestamps = []
        self.driver = None
        self.time_obj = timedelta(hours=8, minutes=0, seconds=0)
        self.hub_address = "4001 South 700 East"
        self.at_hub = True

    # Adds mileage to the truck's total distance
    def add_miles(self, miles):
        self.total_distance_traveled += miles

    # Checks if the truck is full
    def is_full(self):
        return len(self.packages_id_list) == self.maxpckgs

    # Assigns a package to the truck if there's room
    def assign_package(self, package):
        if len(self.packages_id_list) < self.maxpckgs:
            self.packages_id_list.append(package.id_number)
            package.assigned_truck_id = self.id
            return True
        return False

    # delivers a package and updates its status and the truck's time and distance
    def deliver_package(self, ht, package_id, distance_traveled):
        package = ht.lookup(package_id)
        self.packages_id_list.remove(package_id)
        self.at_hub = False
        self.add_miles(distance_traveled)
        self.time_obj += timedelta(minutes=(distance_traveled / self.mph * 60))
        self.mileage_timestamps.append([self.total_distance_traveled, self.time_obj])
        package.delivery_status = "Delivered"
        package.delivery_timestamp = self.time_obj

    # sets all packages to "En route" when they're on the truck
    def set_packages_en_route(self, ht):
        for package_id in self.packages_id_list:
            package = ht.lookup(package_id)
            package.delivery_status = "En route"
            package.en_route_timestamp = self.time_obj

    # Sends the truck back to the hub, updates time and distance
    def send_back_to_hub(self, distance_from_hub):
        self.add_miles(distance_from_hub)
        self.time_obj += timedelta(minutes=(distance_from_hub / self.mph * 60))
        self.mileage_timestamps.append([self.total_distance_traveled, self.time_obj])
        self.at_hub = True

    # Returns a list of the truck's assigned packages
    def get_package_list(self, ht):
        return [ht.lookup(package_id) for package_id in self.packages_id_list]

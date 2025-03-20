#driver.py

class Driver:
    # initializes the driver to its ID
    def __init__(self, driver_id):
        self.driver_id = driver_id
        self.truck = None

    # removes the Truck from being assigned to this Driver
    def remove_truck(self):
        if self.truck:
            self.truck.driver = None  # Unassign the driver from the truck
            self.truck = None
    # assigns a Truck to this Driver from the available truck_list
    def assign_truck(self, truck_list):
        #try to find an unassigned truck from the list
        unassigned_truck = self._find_unassigned_truck(truck_list)

        if unassigned_truck:
            unassigned_truck.driver = self  # Assign this driver to the truck
            self.truck = unassigned_truck  # Link the truck to this driver
            return True
        return False

    #helper method to find an unassigned truck in the list
    def _find_unassigned_truck(self, truck_list):
        for truck in truck_list:
            if truck.driver is None:  # Find a truck without a driver
                return truck
        return None

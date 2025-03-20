# package.py
from datetime import datetime, timedelta

class Package:
    # constructor to initialize the package with relevant details
    def __init__(self, id_number, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline,
                 package_mass, special_notes, delivery_status):
        self.id_number = id_number
        self.delivery_address = delivery_address
        self.delivery_city = delivery_city
        self.delivery_state = delivery_state
        self.delivery_zip = delivery_zip
        self.delivery_deadline = delivery_deadline
        self.special_notes = special_notes
        self.package_mass = package_mass
        self.delivery_status = delivery_status
        self.delivery_timestamp = None
        self.assigned_truck_id = None
        self.on_truck = False
        self.en_route_timestamp = None

    # checks if the package has been assigned to a truck
    def is_truck_assigned(self):
        return self.assigned_truck_id is not None

    # gets the required truck id if mentioned in special notes
    def get_required_truck_id(self):
        if "Can only be on truck" in self.special_notes:
            # extracts truck id from special notes
            truck_id = [int(i) for i in self.special_notes.split() if i.isdigit()]
            return truck_id[0] if truck_id else None
        return None

        # New method to print address based on time for Package 9
    # returns the delayed arrival time if the package is delayed at the depot
    def get_delayed_arrival_time(self):
        if "Delayed on flight---will not arrive to depot until" in self.special_notes:
            # extracts the timestamp of delayed arrival from special notes
            for token in self.special_notes.split():
                try:
                    timestamp = datetime.strptime(token, "%H:%M")
                    return timedelta(hours=timestamp.hour, minutes=timestamp.minute)
                except ValueError:
                    pass
            # Check if the address is wrong (Package #9)
        if "Wrong address listed" in self.special_notes:
            # return a default delay if the address is wrong
            return timedelta(hours=10, minutes=20)
        return None

    from datetime import datetime

    class Package:
        def __init__(self, id_number, delivery_address, delivery_city, delivery_state, delivery_zip, delivery_deadline,
                     package_mass, special_notes, delivery_status):
            self.id_number = id_number
            self.delivery_address = delivery_address
            self.delivery_city = delivery_city
            self.delivery_state = delivery_state
            self.delivery_zip = delivery_zip
            self.delivery_deadline = delivery_deadline
            self.special_notes = special_notes
            self.package_mass = package_mass
            self.delivery_status = delivery_status
            self.delivery_timestamp = None
            self.assigned_truck_id = None
            self.on_truck = False
            self.en_route_timestamp = None

        def get_delayed_arrival_time(self):
            if "Delayed on flight---will not arrive to depot until" in self.special_notes:
                for token in self.special_notes.split():
                    try:
                        timestamp = datetime.strptime(token, "%H:%M")
                        return timedelta(hours=timestamp.hour, minutes=timestamp.minute)
                    except ValueError:
                        pass
            return None

        # New method for address change based on time
        def get_delayed_address(self):
            # Check if this is package 9 and address should change based on time
            if self.id_number == 9:
                # Get current time
                current_time = datetime.now().time()

                # Compare current time with 10:20 AM
                if current_time < datetime.strptime("10:20", "%H:%M").time():
                    # Before 10:20 AM, use the wrong address
                    self.delivery_address = "300 State St"
                    self.delivery_zip = "84103"
                else:
                    # After 10:20 AM, use the correct address
                    self.delivery_address = "410 S State St., Salt Lake City, UT 84111"
                    self.delivery_zip = "84111"

            return self.delivery_address

    # converts delivery deadline to a timedelta object for easier comparison
    def delivery_deadline_delta(self):
        # converts the deadline string to timedelta format
        for token in self.delivery_deadline.split():
            try:
                timestamp = datetime.strptime(token, "%H:%M")
                return timedelta(hours=timestamp.hour, minutes=timestamp.minute)
            except ValueError:
                pass
        return None

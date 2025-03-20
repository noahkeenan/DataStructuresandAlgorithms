#Noah Keenan Student ID: 012119454 WGU
# WGUPS Routing Program - Main Execution File
import csv
from datetime import datetime, timedelta

from Driver import Driver
from HashTable import HashTable
from Package import Package
from Truck import Truck

#constants
trucks = 3  #number of trucks available
drivers = 2  #number of drivers available

# loads Package data from the 'packages.csv' file and inserts it into the HashTable
def load_package_data(ht):
    with open('packages.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            package = Package(
                int(row[0]), row[1], row[2], row[3], row[4], row[5],
                row[6], row[7], "At the hub"
            )
            ht.insert(package)

#parse 'distances.csv' to create distance matrix
def load_distance():
    with open('distances.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        num_addresses = get_address_count()
        distance_data = [[0 for _ in range(num_addresses)] for _ in range(num_addresses)]
        src_address_index = 0

        for src_address in csv_reader:
            for dest_address_index in range(num_addresses):
                if src_address[dest_address_index]:
                    dist = float(src_address[dest_address_index])
                    distance_data[src_address_index][dest_address_index] = dist
                    distance_data[dest_address_index][src_address_index] = dist
            src_address_index += 1
    return distance_data

# parses 'addresses.csv' and returns a list of street addresses
def load_address():
    with open('addresses.csv') as csv_file:
        address_list = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            full_address = row[0].split("\n")
            street_address = full_address[1].strip()
            address_list.append(street_address)
    return address_list

# counts the number of addresses in 'addresses.csv'
def get_address_count():
    num_addresses = 0
    with open('addresses.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            num_addresses += 1
    return num_addresses

# gets the distance between two addresses using their indices in the address list
def distance_between(address1, address2):
    distance_list = load_distance()
    address_list = load_address()
    address1_index = address_list.index(address1)
    address2_index = address_list.index(address2)
    return distance_list[address1_index][address2_index]

# assigns packages to the truck, ensuring optimization of the delivery route
def assign_packages(ht, truck):
    while len(get_assignable_packages(ht, truck)) > 0 and not truck.is_full() and truck.at_hub:
        address = truck.hub_address if len(truck.packages_id_list) == 0 else \
            ht.lookup(truck.packages_id_list[-1]).delivery_address

        nearest_package = get_closest_package(address, get_assignable_packages(ht, truck))
        truck.assign_package(nearest_package)

        if nearest_package.id_number == 9:
            nearest_package.delivery_address = "410 S State St"
            nearest_package.delivery_city = "Salt Lake City"
            nearest_package.delivery_state = "UT"
            nearest_package.delivery_zip = "84111"
            organize_packages(ht, truck)

        for list in get_lists_associated_packages(ht):
            if nearest_package in list:
                for associated_package in list:
                    if not associated_package.is_truck_assigned():
                        truck.assign_package(associated_package)

        organize_packages(ht, truck)


# sorts the truck's package list by prioritizing the shortest distance between each package
def organize_packages(ht, truck):
    sorted_package_id_list = []
    current_address = truck.hub_address
    package_list = truck.get_package_list(ht)

    # loop through the package list, appending package ids in the order of shortest distance
    while len(package_list) != 0:
        nearest_package = get_closest_package(current_address, package_list)
        sorted_package_id_list.append(nearest_package.id_number)
        current_address = nearest_package.delivery_address
        package_list.remove(nearest_package)

    # set the truck's package id list to the sorted list
    truck.packages_id_list = sorted_package_id_list


# finds and returns the package with the shortest distance to the current address
def get_closest_package(current_address, package_list):
    nearest_package = None
    nearest_distance = None

    # iterate through the list to find the nearest package to the current address
    for package in package_list:
        if package is not None:
            # initialize nearest package if it's the first one
            if nearest_package is None:
                nearest_package = package
                nearest_package_address = nearest_package.delivery_address
                nearest_distance = distance_between(nearest_package_address, current_address)
            # compare distance if a nearest package has already been found
            else:
                package_address = package.delivery_address
                package_distance = distance_between(package_address, current_address)

                if package_distance < nearest_distance:
                    nearest_package = package
                    nearest_distance = package_distance

    return nearest_package

# initializes trucks and drivers based on the minimum of configured trucks and drivers
def initialize_trucks_drivers(NUM_TRUCKS, NUM_DRIVERS):
    truck_list, driver_list = [], []
    num_trucks_drivers = min(NUM_TRUCKS, NUM_DRIVERS)

    for current_truck_num in range(1, num_trucks_drivers + 1):
        truck_list.append(Truck(current_truck_num))

    for current_driver_num in range(1, num_trucks_drivers + 1):
        driver = Driver(current_driver_num)
        driver.assign_truck(truck_list)
        driver_list.append(driver)

    return truck_list, driver_list


# delivers all packages until every package in the hashtable is marked as delivered
def deliver_all_packages(ht, truck_list):
    while not all_packages_delivered(ht):
        for truck in truck_list:
            # set delivery status to "en route" for all packages being delivered
            truck.set_packages_en_route(ht)

            currentadd = truck.hub_address
            current_package_index = 0

            # deliver all packages loaded onto the truck
            while len(truck.packages_id_list) > 0:
                package_id = truck.packages_id_list[current_package_index]
                package = ht.lookup(package_id)

                # calculate the distance for each delivery and update the truck's total mileage
                distance_traveled = distance_between(currentadd, package.delivery_address)
                truck.deliver_package(ht, package_id, distance_traveled)

                # update the current address to the package's delivery address
                currentadd = package.delivery_address

            # after delivering all packages, the truck returns to the hub
            truck.send_back_to_hub(distance_between(currentadd, truck.hub_address))

        # assign more packages to the trucks
        for truck in truck_list:
            assign_packages(ht, truck)


# checks and returns true if all packages in the hashtable are delivered
def all_packages_delivered(ht):
    for package in ht.package_table:
        if package is not None and package.delivery_timestamp is None:
            return False
    return True

# returns a list of unassigned packages from the hashtable
def get_unassigned_packages(ht):
    unassigned_packages = []

    for package in ht.package_table:
        if package is not None and package.is_truck_assigned() is False:
            unassigned_packages.append(package)

    return unassigned_packages


# returns a list of packages that can be assigned to the given truck
def get_assignable_packages(ht, truck):
    unassignable_packages = get_unassignable_packages(ht, truck)
    assignable_packages = []

    # iterate through the unassigned packages and determine which can be assigned to the truck
    for package in get_unassigned_packages(ht):
        if package is not None and package not in unassignable_packages:
            assignable_packages.append(package)

    return assignable_packages



# OBJECTIVE: Returns a list of unassigned Packages that cannot be assigned to the given Truck
def get_unassignable_packages(ht, truck):
    unassignable_packages = []
    associated_package_lists = get_lists_associated_packages(ht)

    # Iterate through the Package list and check for unassignable Packages
    for package in ht.package_table:
        if package is not None:
            # If the Package is already assigned to a Truck, add it to the unassignable list
            if package.is_truck_assigned():
                unassignable_packages.append(package)

            # If the Package must be delivered by a different Truck, add it to the unassignable list
            elif package.get_required_truck_id() is not None and package.get_required_truck_id() is not truck.id:
                unassignable_packages.append(package)

                # Add associated Packages to the unassignable list if applicable
                if len(associated_package_lists) > 0:
                    for list in associated_package_lists:
                        if package in list:
                            for associated_package in list:
                                if associated_package not in unassignable_packages:
                                    unassignable_packages.append(associated_package)

            # If the Package is delayed and cannot be assigned yet, mark it as unassignable
            elif package.get_delayed_arrival_time() is not None and package.get_delayed_arrival_time() > truck.time_obj:
                if package not in unassignable_packages:
                    unassignable_packages.append(package)

    return unassignable_packages



# returns a list of lists, where each list contains packages that must be delivered together
def get_lists_associated_packages(ht):
    # master list of associated package groups
    associated_packages_lists = []


    # iterate through each package in the hashtable and create associations based on special notes
    for current_package in ht.package_table:
        if current_package is not None and "must be delivered with" in current_package.special_notes:
            # get the list of packages that are directly associated with the current package
            associated_packages = findcommon_pckg(ht, current_package)

            # flags and variables to check if existing lists need to be combined
            combine_lists = False
            list_to_combine = None

            # space-time complexity: o(n^2)
            # check if any of the associated packages are already in an existing list in the master list
            if len(associated_packages_lists) > 0:
                for package in associated_packages:
                    for list in associated_packages_lists:
                        if package in list:
                            combine_lists = True
                            list_to_combine = list
                            break

            # space-time complexity: o(n)
            # if any package in associated_packages exists in an existing list, add to that list instead of creating a new one
            if combine_lists:
                for package in associated_packages:
                    if package not in list_to_combine:
                        list_to_combine.append(package)
            # if none of the packages are in an existing list, create a new list and add it to the master list
            else:
                associated_packages_lists.append(associated_packages)
    return associated_packages_lists


# function that checks the special notes of a package and returns other packages that must be delivered with it
def findcommon_pckg(ht, package):
    if "must be delivered with" in package.special_notes:
        # create a list to hold the associated packages
        associated_packages = [package]

        # process special notes and extract other package ids that need to be delivered with the current one
        specnotes = package.special_notes.replace(",", " ")
        tokennotes = specnotes.split()
        package_ids_list = [int(i) for i in tokennotes if i.isdigit()]

        # append associated packages to the list
        for package_id in package_ids_list:
            package = ht.lookup(package_id)
            associated_packages.append(package)
            additional_packages = findcommon_pckg(ht, package)

            if additional_packages is not None:
                for additional_package in additional_packages:
                    if additional_package not in associated_packages:
                        associated_packages.append(additional_package)

        return associated_packages

# Displays a menu for the user to interact with and choose an action
def user_interface(ht, truck_list):
    # Display the program title
    print("Noah Keenan 012119454\n")
    print("Welcome to the Western Governors University Parcel Service")

    # List the menu options for the user
    print("Please pick an option to retrieve a full report or specific package information.\n")
    print("1. Full Report")
    print("2. Lookup Specific Package")
    print("3. Exit Program")
    valid_options = [1, 2, 3]

    option = None

    while option is None:
        user_input = input("\nEnter your selection here: ")

        if user_input.isdigit() and int(user_input) in valid_options:
            option = int(user_input)
        else:
            print("Error: Invalid option provided.")

    # process the selected option
    if option == 1: general_report(ht, truck_list)
    if option == 2: spef_pckg(ht, truck_list)
    if option == 3:
        print("The program will now close.")
        quit()


# Displays a status report for all packages at a user-specified time
def general_report(ht, truck_list):
    # Get the user input for the desired time to generate the report
    report_datetime = prompt_time()

    # Show the status report for all packages at the chosen time
    print("Status report of all packages at " + report_datetime.strftime("%I:%M %p"))

    # Loop through each package and display delivery status at the given time
    for package in range(1, len(ht.package_table) + 1):
        if package is not None:
            display_package_query(ht, package, report_datetime)

    # Show the total mileage for all trucks at the specified time
    print_total_mileage_at_time(truck_list, report_datetime)

    # Prompt the user to choose the next action
    user_interface(ht, truck_list)


# queries and displays specific package information at a given time
def spef_pckg(ht, truck_list):
    # get the user input for the desired time and package id
    report_datetime = prompt_time()
    package_id = prompt_package_id(ht)

    # show the package details at the specified time
    print("displaying package information at " + report_datetime.strftime("%I:%M %p"))
    display_package_query(ht, package_id, report_datetime)

    # prompt the user for the next action
    user_interface(ht, truck_list)


# displays the information for a specific package at the specified time
def display_package_query(ht, package_id, report_datetime):
    # fetch the package using the provided package id
    package = ht.lookup(package_id)

    # convert the specified report time to timedelta for comparison
    report_timedelta = timedelta(hours=report_datetime.hour, minutes=report_datetime.minute)

    # prepare the package information string for display
    inform_status = "[package id = %d] " % package.id_number
    if package.assigned_truck_id:
        inform_status += "\ttruck id: " + str(package.assigned_truck_id)
    else:
        inform_status += "\ttruck id: N/A"
    # determine and append the package's delivery status
    if package.en_route_timestamp > report_timedelta:
        inform_status += "\tdelivery status: at the hub"
    elif package.delivery_timestamp > report_timedelta:
        delivery_timestamp_datetime = datetime.strptime(str(package.delivery_timestamp), "%H:%M:%S")
        inform_status += "\tdelivery status: en route to delivery address, expected delivery at " + delivery_timestamp_datetime.strftime(
            "%I:%M %p")
    else:
        delivery_timestamp_datetime = datetime.strptime(str(package.delivery_timestamp), "%H:%M:%S")
        inform_status += "\tdelivery status: delivered at " + delivery_timestamp_datetime.strftime("%I:%M %p")
    cutoff_time = timedelta(hours=10, minutes=20)
    if report_timedelta < cutoff_time:
        # Before 10:20 AM, use temporary address
        if package.id_number == 9:
            package.delivery_address = "300 State St"
            package.delivery_city = "Salt Lake City"
            package.delivery_state = "UT"
            package.delivery_zip = "84103"
        # After 10:20 AM, use correct address
    if report_timedelta > cutoff_time:
        if package.id_number == 9:
            package.delivery_address = "410 S. State St."
            package.delivery_city = "Salt Lake City"
            package.delivery_state = "UT"
            package.delivery_zip = "84111"
    # append additional package details
    inform_status += "\taddress: " + package.delivery_address
    inform_status += "\tcity: " + package.delivery_city
    inform_status += "\tzip code: " + package.delivery_zip
    inform_status += "\tpackage weight: " + package.package_mass + " kilograms"
    inform_status += "\tdelivery deadline: " + package.delivery_deadline

    # display the complete package information
    print(inform_status)


# calculates and prints the total mileage of all trucks at a specific time
def print_total_mileage_at_time(truck_list, report_datetime):
    # convert the given report time to a timedelta object for comparisons
    report_timedelta = timedelta(hours=report_datetime.hour, minutes=report_datetime.minute)

    # variable to store the cumulative mileage
    total_mileage = 0

    # calculate the mileage for each truck at the report time
    for truck in truck_list:
        if len(truck.mileage_timestamps) > 0:
            index = len(truck.mileage_timestamps) - 1

            while index > 0:
                timestamp_mileage = truck.mileage_timestamps[index][0]
                timestamp_timedelta = truck.mileage_timestamps[index][1]

                # if the timestamp is before the report time, add the mileage
                if timestamp_timedelta <= report_timedelta:
                    total_mileage += timestamp_mileage
                    print("truck %d's mileage: %0.2f miles" % (truck.id, timestamp_mileage))
                    break
                else:
                    index -= 1
            if index == 0:
                print("truck %d's mileage: %0.2f miles" % (truck.id, 0.00))

    # print out the total mileage of all trucks at the specified time
    print("\nthe total mileage of all trucks at " + report_datetime.strftime(
        "%I:%M %p") + " is %0.2f miles" % total_mileage)


# prompts the user for a time to generate the report
def prompt_time():
    report_datetime = None

    # continuously ask for input until the user provides a valid time
    while report_datetime is None:
        try:
            report_datetime = datetime.strptime(input("what time would you like a report from? : "), "%I:%M %p")
        except:
            print("\terror: invalid time format. please try again.\n")

    return report_datetime


# prompts the user to input a valid package id
def prompt_package_id(ht):
    package_id = None

    # continuously prompt the user for a valid package id
    while package_id is None:
        user_input = input("please enter the id of the package you would like to view: ")

        if user_input.isdigit():
            if ht.lookup(int(user_input)) is not None:
                package_id = int(user_input)
            else:
                print("\tno package found with the provided id.\n")
        else:
            print("\terror: invalid input. please try again.\n")

    return package_id


def main():
    # initialize the delivery hashtable and load package data
    delivery_ht = HashTable()
    load_package_data(delivery_ht)

    # create trucks and drivers
    truck_list, driver_list = initialize_trucks_drivers(trucks, drivers)

    # check for delayed start times based on package arrivals
    delayed_start_time = None

    for package in delivery_ht.package_table:
        if package is not None and package.get_delayed_arrival_time() is not None:
            if delayed_start_time is None or delayed_start_time > package.get_delayed_arrival_time():
                delayed_start_time = package.get_delayed_arrival_time()

    if len(truck_list) > 1:
        last_truck_index = len(truck_list) - 1
        truck_list[last_truck_index].time_obj = delayed_start_time

    # assign packages to trucks
    for truck in truck_list:
        assign_packages(delivery_ht, truck)

    # start delivering packages until all are delivered
    deliver_all_packages(delivery_ht, truck_list)

    # display the interactive menu to the user
    user_interface(delivery_ht, truck_list)


if __name__ == "__main__":
    main()

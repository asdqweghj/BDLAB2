class ControllerFacility:
    def __init__(self, model_facility, view_facility):
        self.model_facility = model_facility
        self.view_facility = view_facility

    def add_facility(self):
        # Request the ID of the facility to be updated
        facility_id = self.view_facility.get_facility_id()

        venue_id, facility_name, facility_type = (
            self.view_facility.get_facility_input())

        # Call a method from the Model class to add a facility
        success = (self.model_facility.add_facility
                   (facility_id, facility_name, facility_type, venue_id))

        # Display a message about the result of the operation
        if success:
            self.view_facility.show_facility_message("Successfully Added New Facility")
        else:
            self.view_facility.show_facility_message("Facility Not Added")

    def view_facilities(self):
        # Call a method from the Model class to retrieve all facilities
        facilities = self.model_facility.get_all_facilities()

        # Display facilities via a method from the View class
        self.view_facility.show_facility(facilities)

    def update_facility(self):
        # Request the ID of the facility to be updated
        facility_id = self.view_facility.get_facility_id()

        # Check if there is a facility with the specified ID
        facility_exists = self.model_facility.check_facility_existence(facility_id)

        if facility_exists:
            # Request updated facility details from the user
            venue_id, facility_name, facility_type = (
                self.view_facility.get_facility_input())
            # Call a method from the Model class to update the facility
            success = (self.model_facility.update_facility
                       (facility_id, venue_id, facility_name, facility_type))

            # Display a message about the result of the operation
            if success:
                self.view_facility.show_facility_message("Successfully Updated A Facility")
            else:
                self.view_facility.show_facility_message("Facility Not Updated")
        else:
            self.view_facility.show_facility_message("Facility With This ID Does Not Exist")

    def delete_facility(self):
        # Request the ID of the facility to be deleted
        facility_id = self.view_facility.get_facility_id()

        # Check if there is a facility with the specified ID
        facility_exists = self.model_facility.check_facility_existence(facility_id)

        if facility_exists:
            # Call a method from the Model class to delete a facility
            success = self.model_facility.delete_facility(facility_id)

            # Display a message about the result of the operation
            if success:
                self.view_facility.show_facility_message("Successfully Deleted A Facility")
            else:
                self.view_facility.show_facility_message("Facility Not Deleted")
        else:
            self.view_facility.show_facility_message("Facility With The Specified ID Does Not Exist")

    def create_facility_sequence(self):
        # Call method create_facility_sequence from class ModelFacility
        self.model_facility.create_facility_sequence()
        self.view_facility.show_facility_message("Successfully Created Facility Sequence")

    def generate_rand_facility_data(self, number_of_operations):
        # Call method generate_rand_facility_data from class ModelFacility
        success = self.model_facility.generate_rand_facility_data(number_of_operations)

        if success:
            self.view_facility.show_facility_message(
                f"{number_of_operations} Facilities Successfully Created")
        else:
            self.view_facility.show_facility_message("Facility Not Created")

    def truncate_facility_table(self):
        # Call the method of the corresponding model
        success = self.model_facility.truncate_facility_table()

        if success:
            self.view_facility.show_facility_message("All Facilities Data Successfully Deleted")
        else:
            self.view_facility.show_facility_message("All Facilities Data Not Deleted")
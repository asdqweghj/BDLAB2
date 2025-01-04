class ControllerVenue:
    def __init__(self, model_venue, view_venue):
        self.model_venue = model_venue
        self.view_venue = view_venue

    def add_venue(self):
        venue_id = self.view_venue.get_venue_id()
        name, address, city, capacity = self.view_venue.get_venue_input()
        if self.model_venue.add_venue(venue_id, name, address, city, capacity):
            self.view_venue.show_venue_message("Successfully Added A Venue")
        else:
            self.view_venue.show_venue_message("Venue Not Added")

    def view_venues(self):
        venues = self.model_venue.get_all_venues()
        self.view_venue.show_venues(venues)

    def update_venue(self):
        venue_id = self.view_venue.get_venue_id()

        # Check if the venue exists
        venue_exists = self.model_venue.check_venue_existence(venue_id)

        if venue_exists:
            # Get updated venue data
            name, address, city, capacity = self.view_venue.get_venue_input()
            # Update venue
            success = self.model_venue.update_venue(venue_id, name, address, city, capacity)

            if success:
                self.view_venue.show_venue_message("Successfully Updated A Venue")
            else:
                self.view_venue.show_venue_message("Venue Not Updated")
        else:
            self.view_venue.show_venue_message("Venue Does Not Exist With This ID")

    def delete_venue(self):
        venue_id = self.view_venue.get_venue_id()

        # Check if the venue exists
        venue_exists = self.model_venue.check_venue_existence(venue_id)

        if venue_exists:
            if self.model_venue.delete_venue(venue_id):
                self.view_venue.show_venue_message("Successfully Deleted A Venue")
            else:
                self.view_venue.show_venue_message("Venue Not Deleted")
        else:
            self.view_venue.show_venue_message("Venue Does Not Exist With This ID")

    def create_venue_sequence(self):
        self.model_venue.create_venue_sequence()
        self.view_venue.show_venue_message("Successfully Generated Venue Sequence")

    def generate_rand_venue_data(self, number_of_operations):
        success = self.model_venue.generate_rand_venue_data(number_of_operations)

        if success:
            self.view_venue.show_venue_message(f"{number_of_operations} Venues Successfully Generated")
        else:
            self.view_venue.show_venue_message("Venue Not Created")

    def truncate_venue_table(self):
        success = self.model_venue.truncate_venue_table()

        if success:
            self.view_venue.show_venue_message("Successfully Deleted All Venue Data")
        else:
            self.view_venue.show_venue_message("Venue Data Not Deleted")
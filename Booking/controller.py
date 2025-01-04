class ControllerBooking:
    def __init__(self, model_booking, view_booking):
        self.model_booking = model_booking
        self.view_booking = view_booking

    def add_booking(self):
        # Request the ID of the booking to be updated
        booking_id = self.view_booking.get_booking_id()

        user_id, facility_id, booking_date, start_time, end_time, status = (
            self.view_booking.get_booking_input())

        # Call a method from the Model class to add a booking
        success = (self.model_booking.add_booking
                   (booking_id, booking_date, start_time, end_time, status, user_id, facility_id))

        # Display a message about the result of the operation
        if success:
            self.view_booking.show_booking_message("Successfully Added New Booking")
        else:
            self.view_booking.show_booking_message("Booking Not Added")

    def view_bookings(self):
        # Call a method from the Model class to retrieve all bookings
        bookings = self.model_booking.get_all_bookings()

        # Display bookings via a method from the View class
        self.view_booking.show_booking(bookings)

    def update_booking(self):
        # Request the ID of the booking to be updated
        booking_id = self.view_booking.get_booking_id()

        # Check if there is a booking with the specified ID
        booking_exists = self.model_booking.check_booking_existence(booking_id)

        if booking_exists:
            # Request updated booking details from the user
            user_id, facility_id, booking_date, start_time, end_time, status = (
                self.view_booking.get_booking_input())
            # Call a method from the Model class to update the booking
            success = (self.model_booking.update_booking
                       (booking_id, user_id, facility_id, booking_date, start_time, end_time, status))

            # Display a message about the result of the operation
            if success:
                self.view_booking.show_booking_message("Successfully Updated A Booking")
            else:
                self.view_booking.show_booking_message("Booking Not Updated")
        else:
            self.view_booking.show_booking_message("Booking With This ID Does Not Exist")

    def delete_booking(self):
        # Request the ID of the booking to be deleted
        booking_id = self.view_booking.get_booking_id()

        # Check if there is a booking with the specified ID
        booking_exists = self.model_booking.check_booking_existence(booking_id)

        if booking_exists:
            # Call a method from the Model class to delete a booking
            success = self.model_booking.delete_booking(booking_id)

            # Display a message about the result of the operation
            if success:
                self.view_booking.show_booking_message("Successfully Deleted A Booking")
            else:
                self.view_booking.show_booking_message("Booking Not Deleted")
        else:
            self.view_booking.show_booking_message("Booking With The Specified ID Does Not Exist")

    def create_booking_sequence(self):
        # Call method create_booking_sequence from class Modelbooking
        self.model_booking.create_booking_sequence()
        self.view_booking.show_booking_message("Successfully Created Booking Sequence")

    def generate_rand_booking_data(self, number_of_operations):
        # Call method generate_rand_booking_data from class Modelbooking
        success = self.model_booking.generate_rand_booking_data(number_of_operations)

        if success:
            self.view_booking.show_booking_message(
                f"{number_of_operations} Bookings Successfully Created")
        else:
            self.view_booking.show_booking_message("Booking Not Created")

    def truncate_booking_table(self):
        # Call the method of the corresponding model
        success = self.model_booking.truncate_booking_table()

        if success:
            self.view_booking.show_booking_message("All Bookings Data Successfully Deleted")
        else:
            self.view_booking.show_booking_message("All Bookings Data Not Deleted")
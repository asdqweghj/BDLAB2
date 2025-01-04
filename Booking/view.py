class ViewBooking:
    def show_booking(self, bookings):
        print("Bookings:")
        for booking in bookings:
            print(
                f"Booking ID: {booking[0]},User ID: {booking[1]}, Facility ID: {booking[2]} Booking date: {booking[3]}, Start time: {booking[4]}, End time: {booking[5]}, Status: {booking[6]} ")
            
    def get_booking_input(self):
        booking_date = input("Input booking date(HH:MM:SS): ")
        start_time = input("Input start time (HH:MM:SS): ")
        end_time = input("Input end time (HH:MM:SS): ")
        status = input("Input status: ")
        user_id = int(input("Input User ID: "))
        facility_id = int(input("Input Facility ID: "))
        return booking_date, start_time, end_time, status, user_id, facility_id
    
    def get_booking_id(self):
        return int(input("Input Booking ID: "))
    
    def show_booking_message(self, message):
        print(message)
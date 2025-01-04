from model import Model

from Booking.view import ViewBooking
from Booking.model import ModelBooking
from Booking.controller import ControllerBooking

from Facility.view import ViewFacility
from Facility.model import ModelFacility
from Facility.controller import ControllerFacility

from Payment.view import ViewPayment
from Payment.model import ModelPayment
from Payment.controller import ControllerPayment

from Users.view import ViewUser
from Users.model import ModelUser
from Users.controller import ControllerUser

from Venue.view import ViewVenue
from Venue.model import ModelVenue
from Venue.controller import ControllerVenue

from Analytics.view import ViewAnalytics
from Analytics.model import ModelAnalytics
from Analytics.controller import ControllerAnalytics


class Controller:
    def __init__(self):
        self.model = Model()
        self.view_booking = ViewBooking()
        self.view_facility = ViewFacility()
        self.view_payment = ViewPayment()
        self.view_user = ViewUser()
        self.view_venue = ViewVenue()
        self.view_analytics = ViewAnalytics()

        self.model_booking = ModelBooking(self.model)
        self.model_facility = ModelFacility(self.model)
        self.model_payment = ModelPayment(self.model)
        self.model_user = ModelUser(self.model)
        self.model_venue = ModelVenue(self.model)
        self.model_analytics = ModelAnalytics(self.model)

        self.controller_booking = ControllerBooking(self.model_booking, self.view_booking)
        self.controller_facility = ControllerFacility(self.model_facility, self.view_facility)
        self.controller_payment = ControllerPayment(self.model_payment, self.view_payment)
        self.controller_user = ControllerUser(self.model_user, self.view_user)
        self.controller_venue = ControllerVenue(self.model_venue, self.view_venue)
        self.controller_analytics = ControllerAnalytics(self.model_analytics, self.view_analytics)

    def run(self):
        methods = {
            '1': self.controller_booking.add_booking,
            '2': self.controller_facility.add_facility,
            '3': self.controller_payment.add_payment,
            '4': self.controller_user.add_user,
            '5': self.controller_venue.add_venue,
            '6': self.controller_booking.view_bookings,
            '7': self.controller_facility.view_facilities,
            '8': self.controller_payment.view_payments,
            '9': self.controller_user.view_users,
            '10': self.controller_venue.view_venues,
            '11': self.controller_booking.update_booking,
            '12': self.controller_facility.update_facility,
            '13': self.controller_payment.update_payment,
            '14': self.controller_user.update_user,
            '15': self.controller_venue.update_venue,
            '16': self.controller_booking.delete_booking,
            '17': self.controller_facility.delete_facility,
            '18': self.controller_payment.delete_payment,
            '19': self.controller_user.delete_user,
            '20': self.controller_venue.delete_venue,
            '21': self.generate_rand_data,
            '22': self.truncate_all_tables,
            '23': self.display_analytics
        }

        while True:
            choice = self.show_menu()

            if choice in methods:
                methods[choice]()
            elif choice == '24':
                break

    MENU_OPTIONS = [
        "Add New Booking",
        "Add New Facility",
        "Add New Payment",
        "Add New User",
        "Add New Venue",
        "Show Bookings",
        "Show Facilities",
        "Show Payments",
        "Show Users",
        "Show Venues",
        "Update Booking",
        "Update Facility",
        "Update Payment",
        "Update User",
        "Update Venue",
        "Remove Booking",
        "Remove Facility",
        "Remove Payment",
        "Remove User",
        "Remove Venue",
        "Create Data By Random",
        "Delete All Data",
        "View Analytics",
        "Exit"
    ]

    def show_menu(self):
        self.view_facility.show_facility_message("\nMain Menu:")
        for idx, option in enumerate(self.MENU_OPTIONS, start=1):
            self.view_facility.show_facility_message(f"{idx}. {option}")
        return input("Choose an action : ")

    def create_venue_sequence(self):
        self.controller_venue.create_venue_sequence()

    def generate_rand_venue_data(self, number_of_operations):
        self.controller_venue.generate_rand_venue_data(number_of_operations)

    def create_facility_sequence(self):
        self.controller_facility.create_facility_sequence()

    def generate_rand_facility_data(self, number_of_operations):
        self.controller_facility.generate_rand_facility_data(number_of_operations)

    def create_user_sequence(self):
        self.controller_user.create_user_sequence()

    def generate_rand_user_data(self, number_of_operations):
        self.controller_user.generate_rand_user_data(number_of_operations)

    def create_booking_sequence(self):
        self.controller_booking.create_booking_sequence()

    def generate_rand_booking_data(self, number_of_operations):
        self.controller_booking.generate_rand_booking_data(number_of_operations)

    def create_payment_sequence(self):
        self.controller_payment.create_payment_sequence()

    def generate_rand_payment_data(self, number_of_operations):
        self.controller_payment.generate_rand_payment_data(number_of_operations)

    def generate_rand_data(self):
        number_of_operations = int(input("Input Number Of Generations: "))
        self.create_booking_sequence()
        self.generate_rand_booking_data(number_of_operations)
        self.create_facility_sequence()
        self.generate_rand_facility_data(number_of_operations)
        self.create_payment_sequence()
        self.generate_rand_payment_data(number_of_operations)
        self.create_user_sequence()
        self.generate_rand_user_data(number_of_operations)
        self.create_venue_sequence()
        self.generate_rand_venue_data(number_of_operations)

    def truncate_all_tables(self):
        if input("Confirm The Action. Type Yes or No: ") == "Yes":
            self.controller_booking.truncate_booking_table()
            self.controller_facility.truncate_facility_table()
            self.controller_payment.truncate_payment_table()
            self.controller_user.truncate_user_table()
            self.controller_venue.truncate_venue_table()
        else:
            print("Ok")

    def display_analytics(self):
        print("-------------------------------------------------------------------------------")
        self.controller_analytics.most_booked_venue()
        print("-------------------------------------------------------------------------------")
        self.controller_analytics.user_activity()
        print("-------------------------------------------------------------------------------")
        self.controller_analytics.payment_analysis()
        print("-------------------------------------------------------------------------------")
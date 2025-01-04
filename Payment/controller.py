class ControllerPayment:
    def __init__(self, model_payment, view_payment):
        self.model_payment = model_payment
        self.view_payment = view_payment

    def add_payment(self):
        # Request the ID of the payment to be updated
        payment_id = self.view_payment.get_payment_id()

        booking_id, amount, payment_date, payment_status = (
            self.view_payment.get_payment_input())

        # Call a method from the Model class to add a payment
        success = (self.model_payment.add_payment
                   (payment_id, amount, payment_date, payment_status, booking_id))

        # Display a message about the result of the operation
        if success:
            self.view_payment.show_payment_message("Successfully Added New Payment")
        else:
            self.view_payment.show_payment_message("Payment Not Added")

    def view_payments(self):
        # Call a method from the Model class to retrieve all payments
        payments = self.model_payment.get_all_payments()

        # Display payments via a method from the View class
        self.view_payment.show_payment(payments)

    def update_payment(self):
        # Request the ID of the payment to be updated
        payment_id = self.view_payment.get_payment_id()

        # Check if there is a payment with the specified ID
        payment_exists = self.model_payment.check_payment_existence(payment_id)

        if payment_exists:
            # Request updated payment details from the user
            booking_id, amount, payment_date, payment_status = (
                self.view_payment.get_payment_input())
            # Call a method from the Model class to update the payment
            success = (self.model_payment.update_payment
                       (payment_id, booking_id, amount, payment_date, payment_status))

            # Display a message about the result of the operation
            if success:
                self.view_payment.show_payment_message("Successfully Updated A Payment")
            else:
                self.view_payment.show_payment_message("Payment Not Updated")
        else:
            self.view_payment.show_payment_message("Payment With This ID Does Not Exist")

    def delete_payment(self):
        # Request the ID of the payment to be deleted
        payment_id = self.view_payment.get_payment_id()

        # Check if there is a payment with the specified ID
        payment_exists = self.model_payment.check_payment_existence(payment_id)

        if payment_exists:
            # Call a method from the Model class to delete a payment
            success = self.model_payment.delete_payment(payment_id)

            # Display a message about the result of the operation
            if success:
                self.view_payment.show_payment_message("Successfully Deleted A Payment")
            else:
                self.view_payment.show_payment_message("Payment Not Deleted")
        else:
            self.view_payment.show_payment_message("Payment With The Specified ID Does Not Exist")

    def create_payment_sequence(self):
        # Call method create_payment_sequence from class ModelPayment
        self.model_payment.create_payment_sequence()
        self.view_payment.show_payment_message("Successfully Created Payment Sequence")

    def generate_rand_payment_data(self, number_of_operations):
        # Call method generate_rand_payment_data from class Modelpayment
        success = self.model_payment.generate_rand_payment_data(number_of_operations)

        if success:
            self.view_payment.show_payment_message(
                f"{number_of_operations} Payments Successfully Created")
        else:
            self.view_payment.show_payment_message("Payment Not Created")

    def truncate_payment_table(self):
        # Call the method of the corresponding model
        success = self.model_payment.truncate_payment_table()

        if success:
            self.view_payment.show_payment_message("All Payments Data Successfully Deleted")
        else:
            self.view_payment.show_payment_message("All Payments Data Not Deleted")
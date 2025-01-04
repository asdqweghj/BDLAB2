class ViewPayment:
    def show_payment(self, payments):
        print("Payments:")
        for payment in payments:
            print(
                f"Payment ID: {payment[0]},Booking ID: {payment[1]}, Amount: {payment[2]}, Payment date: {payment[3]}, Status: {payment[4]} ")
            
    def get_payment_input(self):
        amount = input("Input amount: ")
        payment_date = input("Input payment date(HH:MM:SS): ")
        payment_status = input("Input status: ")
        booking_id = int(input("Input Booking ID: "))
        return amount, payment_date, payment_status, booking_id
    
    def get_payment_id(self):
        return int(input("Input Payment ID: "))
    
    def show_payment_message(self, message):
        print(message)
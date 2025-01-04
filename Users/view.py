class ViewUser:
    def show_users(self, users):
        print("Users:")
        for user in users:
            print(
                f"ID: {user[0]}, First name: {user[1]}, Last name: {user[2]}, Email: {user[3]}, Phone number: {user[4]}, Date of registration: {user[5]}")
            
    def get_user_input(self):
        first_name = input("Input first name: ")
        last_name = input("Input last name: ")
        email = input("Input email: ")
        phone_number = input("Input phone number: ")
        date_of_registration = input("Input date of registration: ")
        return first_name, last_name, email, phone_number, date_of_registration
    
    def get_user_id(self):
        return int(input("Input User ID: "))
    
    def show_user_message(self, message):
        print(message)
            
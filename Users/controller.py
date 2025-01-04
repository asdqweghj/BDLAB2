class ControllerUser:
    def __init__(self, model_user, view_user):
        self.model_user = model_user
        self.view_user = view_user

    def add_user(self):
        user_id = self.view_user.get_user_id()
        first_name, last_name, email, phone_number, date_of_registration = self.view_user.get_user_input()
        if self.model_user.add_user(user_id, first_name, last_name, email, phone_number, date_of_registration):
            self.view_user.show_user_message("Successfully Added A User")
        else:
            self.view_user.show_user_message("User Not Added")

    def view_users(self):
        users = self.model_user.get_all_users()
        self.view_user.show_users(users)

    def update_user(self):
        user_id = self.view_user.get_user_id()

        # Check if the user exists
        user_exists = self.model_user.check_user_existence(user_id)

        if user_exists:
            # Get updated user data
            first_name, last_name, email, phone_number, date_of_registration = self.view_user.get_user_input()
            # Update user
            success = self.model_user.update_user(user_id, first_name, last_name, email, phone_number, date_of_registration)

            if success:
                self.view_user.show_user_message("Successfully Updated A User")
            else:
                self.view_user.show_user_message("User Not Updated")
        else:
            self.view_user.show_user_message("User Does Not Exist With This ID")

    def delete_user(self):
        user_id = self.view_user.get_user_id()

        # Check if the user exists
        user_exists = self.model_user.check_user_existence(user_id)

        if user_exists:
            if self.model_user.delete_user(user_id):
                self.view_user.show_user_message("Successfully Deleted A User")
            else:
                self.view_user.show_user_message("User Not Deleted")
        else:
            self.view_user.show_user_message("User Does Not Exist With This ID")

    def create_user_sequence(self):
        self.model_user.create_user_sequence()
        self.view_user.show_user_message("Successfully Generated User Sequence")

    def generate_rand_user_data(self, number_of_operations):
        success = self.model_user.generate_rand_user_data(number_of_operations)

        if success:
            self.view_user.show_user_message(f"{number_of_operations} Users Successfully Generated")
        else:
            self.view_user.show_user_message("User Not Created")

    def truncate_user_table(self):
        success = self.model_user.truncate_users_table()

        if success:
            self.view_user.show_user_message("Successfully Deleted All User Data")
        else:
            self.view_user.show_user_message("User Data Not Deleted")
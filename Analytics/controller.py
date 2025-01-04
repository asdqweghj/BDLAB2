class ControllerAnalytics:
    def __init__(self, model_analytics, view_analytics):
        self.model_analytics = model_analytics
        self.view_analytics = view_analytics

    def most_booked_venue(self):
        # Отримати дані аналітики
        most_booked_venue_data = self.model_analytics.most_booked_venue()

        # Відобразити результати
        if most_booked_venue_data:
            self.view_analytics.display_most_booked_venue(most_booked_venue_data)
        else:
            print("Error With Most Booked Venue Analytics")

    def user_activity(self):
        # Отримати дані аналітики
        user_activity_data = self.model_analytics.user_activity()

        # Відобразити результати
        if user_activity_data:
            self.view_analytics.display_user_activity(user_activity_data)
        else:
            print("Error With User Activity Analytics")

    def payment_analysis(self):
        # Отримати дані аналітики
        payment_analysis_data = self.model_analytics.payment_analysis()

        # Відобразити результати
        if payment_analysis_data:
            self.view_analytics.display_payment_analysis(payment_analysis_data)
        else:
            print("Error With Payment Analytics")
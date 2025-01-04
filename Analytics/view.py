class ViewAnalytics:
    def display_most_booked_venue(self, most_booked_venue_data):
        print("Найпопулярніше місце:")
        for row in most_booked_venue_data:
            venue_id, venue_name, total_bookings = row
            print(f"ID: {venue_id}, Назва: {venue_name}, Кількість бронювань: {total_bookings}")

    def display_user_activity(self, user_activity_data):
        print("Найактивніші користувачі:")
        for row in user_activity_data:
            user_id, first_name, last_name, total_bookings = row
            print(f"ID: {user_id}, Ім'я: {first_name} {last_name}, Кількість бронювань: {total_bookings}")

    def display_payment_analysis(self, payment_analysis_data):
        print("Аналіз платежів:")
        for row in payment_analysis_data:
            payment_status, total_amount, count_payments = row
            status_text = "Успішні" if payment_status else "Неуспішні"
            print(f"Статус: {status_text}, Загальна сума: {total_amount}, Кількість платежів: {count_payments}")
class ModelAnalytics:
    def __init__(self, db_model):
        self.conn = db_model.conn

    def most_booked_venue(self):
        """
        Запит для визначення найпопулярнішого місця (Venue), 
        на основі кількості бронювань (Booking).
        """
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT 
                    v."venue_id",
                    v."name" AS venue_name,
                    COUNT(b."booking_id") AS total_bookings
                FROM 
                    "venue" v
                JOIN 
                    "facility" f ON v."venue_id" = f."venue_id"
                JOIN 
                    "booking" b ON f."facility_id" = b."facility_id"
                GROUP BY 
                    v."venue_id",v."name"
                ORDER BY 
                    total_bookings DESC
                LIMIT 1; -- Найпопулярніше місце
            """)

            data = c.fetchall()
            self.conn.commit()
            return data
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Analytics Of Most Booked Venue: {str(e)}")
            return None

    def user_activity(self):
        """
        Запит для визначення найактивніших користувачів (Users),
        на основі кількості їхніх бронювань (Booking).
        """
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT 
                    u."user_id",
                    u."first_name", 
                    u."last_name", 
                    COUNT(b."booking_id") AS total_bookings
                FROM 
                    "users" u
                JOIN 
                    "booking" b ON u."user_id" = b."user_id"
                GROUP BY 
                    u."user_id", u."first_name", u."last_name"
                ORDER BY 
                    total_bookings DESC
                LIMIT 5; -- П'ять найактивніших користувачів
            """)

            data = c.fetchall()
            self.conn.commit()
            return data
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Analytics Of User Activity: {str(e)}")
            return None

    def payment_analysis(self):
        """
        Запит для аналізу платежів (Payment) за статусом, 
        загальною сумою та кількістю.
        """
        c = self.conn.cursor()
        try:
            c.execute("""
                SELECT 
                    p."payment_status",
                    COUNT(p."payment_id") AS total_payments,
                    SUM(p."amount") AS total_revenue
                FROM 
                    "payment" p
                GROUP BY 
                    p."payment_status"
                ORDER BY 
                    total_revenue DESC;
            """)

            data = c.fetchall()
            self.conn.commit()
            return data
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Analytics Of Payments: {str(e)}")
            return None
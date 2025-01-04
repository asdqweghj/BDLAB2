import alch
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Time
from sqlalchemy.orm import relationship


class Booking(alch.Base):
    __tablename__ = 'booking'
    booking_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    facility_id = Column(Integer, ForeignKey('facility.facility_id'), nullable=False)
    booking_date = Column(DateTime, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    status = Column(String, nullable=False)

    user = relationship("User", back_populates="bookings")
    facility = relationship("Facility", back_populates="bookings")
    payments = relationship("Payment", back_populates="booking", cascade="all, delete-orphan")

class ModelBooking:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_booking(self, booking_id, user_id, facility_id, booking_date, start_time, end_time, status):
        try:
            user_exists = self.session.query(Booking).filter_by(user_id=user_id).first()
            facility_exists = self.session.query(Booking).filter_by(facility_id=facility_id).first()
            if not user_exists or not facility_exists:
                print("Error: User ID or Facility ID does not exist.")
                return False
            new_booking = Booking(
                booking_id=booking_id,
                user_id=user_id,
                facility_id=facility_id,
                booking_date=booking_date,
                start_time=start_time,
                end_time=end_time,
                status=status
            )
            self.session.add(new_booking)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error With Adding A Booking: {str(e)}")
            return False

    def get_all_bookings(self):
        c = self.conn.cursor()
        try:
            c.execute('SELECT * FROM "booking"')
            return c.fetchall()
        except Exception as e:
            print(f"Error With Retrieving Bookings: {str(e)}")
            return None

    def update_booking(self, booking_id, user_id, facility_id, booking_date, start_time, end_time, status):
        try:
            user_exists = self.session.query(Booking).filter_by(user_id=user_id).first()
            facility_exists = self.session.query(Booking).filter_by(facility_id=facility_id).first()
            if not user_exists or not facility_exists:
                print("Error: User ID or Facility ID does not exist.")
                return False
            booking = self.session.query(Booking).filter(Booking.booking_id == booking_id).first()
            if booking:
                booking.user_id = user_id
                booking.facility_id = facility_id
                booking.booking_date = booking_date
                booking.start_time = start_time
                booking.end_time = end_time
                booking.status = status
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With Updating A Booking: {str(e)}")
            return False

    def delete_booking(self, booking_id):
        try:
            booking = self.session.query(Booking).filter(Booking.booking_id == booking_id).first()
            if booking:
                self.session.delete(booking)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With Deleting A Booking: {str(e)}")
            return False

    def check_booking_existence(self, booking_id):
        c = self.conn.cursor()
        try:
            # Перевірка існування запису
            c.execute('SELECT 1 FROM "booking" WHERE "booking_id" = %s', (booking_id,))
            return bool(c.fetchone())
        except Exception as e:
            print(f"Error With Checking Booking Existence: {str(e)}")
            return False

    def create_booking_sequence(self):
        c = self.conn.cursor()
        try:
            # Створення або оновлення послідовності для booking_id
            c.execute("""
                DO $$
                DECLARE
                    max_id INT;
                BEGIN
                    -- Знаходимо максимальний booking_id
                    SELECT COALESCE(MAX(booking_id), 0) INTO max_id FROM "booking";

                    -- Перевіряємо, чи існує послідовність
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM pg_sequences 
                        WHERE schemaname = 'public' AND sequencename = 'booking_id_seq'
                    ) THEN
                        -- Створення нової послідовності
                        EXECUTE 'CREATE SEQUENCE booking_id_seq START WITH ' || (max_id + 1);
                    ELSE
                        -- Оновлення існуючої послідовності
                        EXECUTE 'ALTER SEQUENCE booking_id_seq RESTART WITH ' || (max_id + 1);
                    END IF;
                END $$;
            """)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Creating Booking Sequence: {str(e)}")
            return False

    def generate_rand_booking_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            c.execute("""
              INSERT INTO "booking" ("booking_id", "booking_date", "start_time", "end_time", "status", "user_id", "facility_id")
            SELECT 
                nextval('booking_id_seq'), 
                -- Випадкова дата і час в межах 30 днів від сьогодні
                (CURRENT_DATE + (random() * 30)::int * interval '1 day') + (random() * interval '12 hours')::time AS booking_date,
                -- Випадковий час початку (з округленням до секунд)
                (CURRENT_TIME + (random() * interval '10 hours'))::time(2) AS start_time,
                -- Випадковий час завершення (на 2 години пізніше)
                ((CURRENT_TIME + (random() * interval '10 hours')) + interval '2 hours')::time(2) AS end_time,
                -- Випадковий статус
                (random() > 0.5)::boolean AS status,
                -- Випадковий user_id
                floor(random() * (SELECT max("user_id") FROM "Users") + 1)::integer AS user_id,
                -- Випадковий facility_id
                floor(random() * (SELECT max("facility_id") FROM "Facility") + 1)::integer AS facility_id
            FROM generate_series(1, %s);
            """, (number_of_operations,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Generating Booking Data: {str(e)}")
            return False

    def truncate_booking_table(self):
        c = self.conn.cursor()
        try:
            # Очищення таблиці booking
            c.execute('DELETE FROM "booking"')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Truncating Booking Table: {str(e)}")
            return False
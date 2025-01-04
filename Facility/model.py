import alch
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship


class Facility(alch.Base):
    __tablename__ = 'facility'
    facility_id = Column(Integer, primary_key=True)
    facility_name = Column(String, nullable=False)
    facility_type = Column(String, nullable=False)
    venue_id = Column(Integer, ForeignKey('venue.venue_id'), nullable=False)

    bookings = relationship("Booking", back_populates="facility")


class ModelFacility:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_facility(self, facility_id, facility_name, facility_type, venue_id):
        """
        Додає новий об'єкт до таблиці Facility.
        """
        try:
            venue_exists = self.session.query(Facility).filter_by(venue_id=venue_id).first()
            if not venue_exists:
                print("Error: Venue ID does not exist.")
                return False

            new_facility = Facility(
                facility_id=facility_id,
                facility_name=facility_name,
                facility_type=facility_type,
                venue_id=venue_id
            )
            self.session.add(new_facility)
            self.session.commit()
            return True 
        except Exception as e:
            self.session.rollback()
            print(f"Error With Adding A Facility: {str(e)}")
            return False 

    def get_all_facilities(self):
        c = self.conn.cursor()
        try:
            c.execute('SELECT * FROM "facility"')
            return c.fetchall()
        except Exception as e:
            print(f"Error With Retrieving Facilities: {str(e)}")
            return None

    def update_facility(self, facility_id, facility_name, facility_type, venue_id):
        """
        Оновлює дані об'єкта Facility за його ID.
        """
        try:
            venue_exists = self.session.query(Facility).filter_by(venue_id=venue_id).first()
            if not venue_exists:
                print("Error: Venue ID does not exist.")
                return False

            facility = self.session.query(Facility).filter(Facility.facility_id == facility_id).first()
            if facility:
                facility.facility_name = facility_name
                facility.facility_type = facility_type
                facility.venue_id = venue_id
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With Updating A Facility: {str(e)}")
            return False

    def delete_facility(self, facility_id):
        """
        Видаляє об'єкт Facility за його ID.
        """
        try:
            facility = self.session.query(Facility).filter(Facility.facility_id == facility_id).first()
            if facility:
                self.session.delete(facility)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With Deleting A Facility: {str(e)}")
            return False 

    def check_facility_existence(self, facility_id):
        c = self.conn.cursor()
        try:
            # Перевірка існування запису
            c.execute('SELECT 1 FROM "facility" WHERE "facility_id" = %s', (facility_id,))
            return bool(c.fetchone())
        except Exception as e:
            print(f"Error With Checking Facility Existence: {str(e)}")
            return False

    def create_facility_sequence(self):
        c = self.conn.cursor()
        try:
            # Створення або оновлення послідовності для facility_id
            c.execute("""
                DO $$
                DECLARE
                    max_id INT;
                BEGIN
                    -- Знаходимо максимальний facility_id
                    SELECT COALESCE(MAX(facility_id), 0) INTO max_id FROM "facility";

                    -- Перевіряємо, чи існує послідовність
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM pg_sequences 
                        WHERE schemaname = 'public' AND sequencename = 'facility_id_seq'
                    ) THEN
                        -- Створення нової послідовності
                        EXECUTE 'CREATE SEQUENCE facility_id_seq START WITH ' || (max_id + 1);
                    ELSE
                        -- Оновлення існуючої послідовності
                        EXECUTE 'ALTER SEQUENCE facility_id_seq RESTART WITH ' || (max_id + 1);
                    END IF;
                END $$;
            """)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Creating Facility Sequence: {str(e)}")
            return False

    def generate_rand_facility_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            c.execute("""
                INSERT INTO "facility" ("facility_id", "facility_name", "facility_type", "venue_id")
                SELECT 
                    nextval('facility_id_seq'),
                    (array['Football', 'Basketball', 'Voleyball', 'Golf', 'Tennis'])[floor(random() * 5) + 1] AS facility_name,
                    CASE 
                        WHEN random() < 0.5 THEN 'Indoor'
                        ELSE 'Outdoor'
                    END AS facility_type,
                    floor(random() * (SELECT max("venue_id") FROM "venue") + 1)::int AS venue_id
                FROM generate_series(1, %s);
            """, (number_of_operations,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Generating Facility Data: {str(e)}")
            return False

    def truncate_facility_table(self):
        c = self.conn.cursor()
        try:
            # Очищення таблиці facility
            c.execute('DELETE FROM "facility"')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Truncating Facility Table: {str(e)}")
            return False

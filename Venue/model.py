import alch
from sqlalchemy import Column, Integer, String

class Venue(alch.Base):
    __tablename__ = 'venue'
    venue_id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    address = Column(String(64), nullable=False)
    city = Column(String(25), nullable=False)
    capacity = Column(Integer, nullable=False)


class ModelVenue:
    def __init__(self, db_model):
        self.conn = db_model.conn  
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_venue(self, venue_id, name, address, city, capacity):
        try:
            new_venue = Venue(
                venue_id=venue_id,
                name=name,
                address=address,
                city=city,
                capacity=capacity
            )
            self.session.add(new_venue)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error Adding Venue: {str(e)}")
            return False 

    def get_all_venues(self):
        c = self.conn.cursor()
        try:
            c.execute('SELECT * FROM "venue"')
            return c.fetchall()
        except Exception as e:
            print(f"Error Retrieving Venues: {str(e)}")
            return None

    def update_venue(self, venue_id, **kwargs):
        try:
            venue = self.session.query(Venue).filter(Venue.venue_id == venue_id).first()
            if venue:
                for key, value in kwargs.items():
                    setattr(venue, key, value) 
                self.session.commit()
                return True  
            return False  
        except Exception as e:
            self.session.rollback()
            print(f"Error Updating Venue: {str(e)}")
            return False 

    def delete_venue(self, venue_id):
        try:
            venue = self.session.query(Venue).filter(Venue.venue_id == venue_id).first()
            if venue:
                self.session.delete(venue)
                self.session.commit()
                return True 
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error Deleting Venue: {str(e)}")
            return False

    def check_venue_existence(self, venue_id):
        c = self.conn.cursor()
        try:
            c.execute('SELECT 1 FROM "venue" WHERE "venue_id" = %s', (venue_id,))
            return bool(c.fetchone())
        except Exception as e:
            print(f"Error Checking Venue Existence: {str(e)}")
            return False

    def create_venue_sequence(self):
        c = self.conn.cursor()
        try:
            c.execute("""
                DO $$
                DECLARE
                    max_id INT;
                BEGIN
                    SELECT COALESCE(MAX(venue_id), 0) INTO max_id FROM "venue";

                    IF NOT EXISTS (
                        SELECT 1 
                        FROM pg_sequences 
                        WHERE schemaname = 'public' AND sequencename = 'venue_id_seq'
                    ) THEN
                        EXECUTE 'CREATE SEQUENCE venue_id_seq START WITH ' || (max_id + 1);
                    ELSE
                        EXECUTE 'ALTER SEQUENCE venue_id_seq RESTART WITH ' || (max_id + 1);
                    END IF;
                END $$;
            """)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error Creating Venue Sequence: {str(e)}")
            return False

    def generate_rand_venue_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            c.execute("""
                INSERT INTO "venue" ("venue_id", "name", "address", "city", "capacity")
                SELECT 
                    nextval('venue_id_seq'),
                    -- Назва спортивного комплексу
                    (array['Arena Sports', 'Champion Gym', 'Victory Stadium', 'Golden Field', 
                       'Elite Fitness', 'Powerhouse Arena', 'Olympic Hall', 'Titanium Dome', 
                       'Active Life Center', 'Dynamic Gym'])[row_number] AS name,
                    -- Унікальна адреса
                    'Street ' || row_number || ', Building ' || floor(random() * 100 + 1)::int AS address,
                    -- Випадкове місто
                    (array['New York', 'Los Angeles', 'Chicago', 'Houston', 'Miami'])[floor(random() * 5) + 1] AS city,
                    -- Випадкова місткість
                    floor(random() * 100 + 10) AS capacity
                FROM (
                    SELECT row_number() OVER () AS row_number
                    FROM generate_series(1, %s)
                ) AS numbered_rows;
            """, (number_of_operations,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error Generating Venue Data: {str(e)}")
            return False

    def truncate_venue_table(self):
        c = self.conn.cursor()
        try:
            c.execute('DELETE FROM "venue"')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error Truncating Venue Table: {str(e)}")
            return False
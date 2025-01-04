import alch
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

class User(alch.Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    date_of_registration = Column(Date, nullable=False)

    bookings = relationship("Booking", back_populates="user")


class ModelUser:
    def __init__(self, db_model):
        self.conn = db_model.conn
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_user(self, user_id, first_name, last_name, email, phone_number, date_of_registration):
        """
        Додає нового користувача у таблицю.
        """
        try:
            new_user = User(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone_number=phone_number,
                date_of_registration=date_of_registration
            )
            self.session.add(new_user)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error adding user: {str(e)}")
            return False 

    def get_all_users(self):
        c = self.conn.cursor()
        try:
            c.execute('SELECT * FROM "users"')
            return c.fetchall()
        except Exception as e:
            print(f"Error retrieving users: {str(e)}")
            return None

    def update_user(self, user_id, **kwargs):
        """
        Оновлює дані користувача за його ID.
        """
        try:
            user = self.session.query(User).filter(User.user_id == user_id).first()
            if user:
                for key, value in kwargs.items():
                    setattr(user, key, value)
                self.session.commit()
                return True
            return False 
        except Exception as e:
            self.session.rollback()
            print(f"Error updating user: {str(e)}")
            return False 

    def delete_user(self, user_id):
        """
        Видаляє користувача за його ID.
        """
        try:
            user = self.session.query(User).filter(User.user_id == user_id).first()
            if user:
                self.session.delete(user)
                self.session.commit()
                return True 
            return False  
        except Exception as e:
            self.session.rollback()
            print(f"Error deleting user: {str(e)}")
            return False

    def check_user_existence(self, user_id):
        c = self.conn.cursor()
        try:
            c.execute('SELECT 1 FROM "users" WHERE "user_id" = %s', (user_id,))
            return bool(c.fetchone())
        except Exception as e:
            print(f"Error checking user existence: {str(e)}")
            return False

    def create_user_sequence(self):
        c = self.conn.cursor()
        try:
            c.execute('''
                DO $$
                DECLARE
                    max_id INT;
                BEGIN
                    SELECT COALESCE(MAX(user_id), 0) INTO max_id FROM "users";

                    IF NOT EXISTS (
                        SELECT 1
                        FROM pg_sequences
                        WHERE schemaname = 'public' AND sequencename = 'user_id_seq'
                    ) THEN
                        EXECUTE 'CREATE SEQUENCE user_id_seq START WITH ' || (max_id + 1);
                    ELSE
                        EXECUTE 'ALTER SEQUENCE user_id_seq RESTART WITH ' || (max_id + 1);
                    END IF;
                END $$;
            ''')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error creating user sequence: {str(e)}")
            return False

    def generate_rand_user_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            c.execute("""
            INSERT INTO "users" ("user_id", "first_name", "last_name", "email", "phone_number", "date_of_registration")
            SELECT
                nextval('user_id_seq'), 
                -- Випадкове ім'я
                first_name,
                -- Випадкове прізвище
                last_name,
                -- Генерація email на основі імені та прізвища
                LOWER(first_name || '.' || last_name || '@gmail.com') AS email,
                -- Генерація номера телефону
                '380' || floor(100000000 + random() * 900000000)::bigint,
                -- Дата реєстрації за останній рік
                CURRENT_DATE - floor(random() * 365)::int AS date_of_registration
            FROM (
                SELECT 
                    -- Вибір випадкового імені
                    (array['Michael', 'Sofia', 'Tom', 'Alex', 'Stan', 'Anna', 'John', 'Emma', 'Oliver', 'Ava'])[floor(random() * 10) + 1] AS first_name,
                    -- Вибір випадкового прізвища
                    (array['Wall', 'Johnes', 'Tesla', 'Fire', 'Smith', 'Brown', 'Taylor', 'Wilson', 'Davies', 'Evans'])[floor(random() * 10) + 1] AS last_name
                FROM generate_series(1, %s)
            ) AS random_data;
            """, (number_of_operations,))
            self.conn.commit()
            return True  
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Generating User Data: {str(e)}")
            return False
    
    def truncate_users_table(self):
        c = self.conn.cursor()
        try:
            c.execute('DELETE FROM "users"')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error truncating users table: {str(e)}")
            return False

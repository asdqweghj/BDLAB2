import alch
from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship


class Payment(alch.Base):
    __tablename__ = 'payment'
    payment_id = Column(Integer, primary_key=True)
    booking_id = Column(Integer, ForeignKey('booking.booking_id'), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False)
    payment_status = Column(Boolean, nullable=False)

    booking = relationship("Booking", back_populates="payments")


# Клас для операцій із таблицею Payment
class ModelPayment:
    def __init__(self, db_model):
        self.conn = db_model.conn  # Для сумісності зі старою структурою
        self.engine = alch.create_engine(alch.DATABASE_URL)
        self.session = alch.Session.configure(bind=self.engine)
        self.session = alch.Session()

    def add_payment(self, payment_id, booking_id, amount, payment_date, payment_status):
        """
        Додає новий платіж до таблиці.
        """
        try:
            # Перевірка існування booking_id
            booking_exists = self.session.query(Payment).filter_by(booking_id=booking_id).first()
            if not booking_exists:
                print("Error: Booking ID does not exist.")
                return False

            new_payment = Payment(
                payment_id=payment_id,
                booking_id=booking_id,
                amount=amount,
                payment_date=payment_date,
                payment_status=payment_status
            )
            self.session.add(new_payment)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            print(f"Error With Adding A Payment: {str(e)}")
            return False  

    def get_all_payments(self):
        c = self.conn.cursor()
        try:
            c.execute('SELECT * FROM "payment"')
            return c.fetchall()
        except Exception as e:
            print(f"Error With Retrieving Payments: {str(e)}")
            return None

    def update_payment(self, payment_id, booking_id, amount, payment_date, payment_status):
        """
        Оновлює дані платежу за його ID.
        """
        try:
            booking_exists = self.session.query(Payment).filter_by(booking_id=booking_id).first()
            if not booking_exists:
                print("Error: Booking ID does not exist.")
                return False

            payment = self.session.query(Payment).filter(Payment.payment_id == payment_id).first()
            if payment:
                payment.booking_id = booking_id
                payment.amount = amount
                payment.payment_date = payment_date
                payment.payment_status = payment_status
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With Updating A Payment: {str(e)}")
            return False

    def delete_payment(self, payment_id):
        """
        Видаляє платіж за його ID.
        """
        try:
            payment = self.session.query(Payment).filter(Payment.payment_id == payment_id).first()
            if payment:
                self.session.delete(payment)
                self.session.commit()
                return True
            return False
        except Exception as e:
            self.session.rollback()
            print(f"Error With Deleting A Payment: {str(e)}")
            return False 

    def check_payment_existence(self, payment_id):
        c = self.conn.cursor()
        try:
            # Перевірка існування запису
            c.execute('SELECT 1 FROM "payment" WHERE "payment_id" = %s', (payment_id,))
            return bool(c.fetchone())
        except Exception as e:
            print(f"Error With Checking Payment Existence: {str(e)}")
            return False

    def create_payment_sequence(self):
        c = self.conn.cursor()
        try:
            # Створення або оновлення послідовності для payment_id
            c.execute("""
                DO $$
                DECLARE
                    max_id INT;
                BEGIN
                    -- Знаходимо максимальний payment_id
                    SELECT COALESCE(MAX(payment_id), 0) INTO max_id FROM "payment";

                    -- Перевіряємо, чи існує послідовність
                    IF NOT EXISTS (
                        SELECT 1 
                        FROM pg_sequences 
                        WHERE schemaname = 'public' AND sequencename = 'payment_id_seq'
                    ) THEN
                        -- Створення нової послідовності
                        EXECUTE 'CREATE SEQUENCE payment_id_seq START WITH ' || (max_id + 1);
                    ELSE
                        -- Оновлення існуючої послідовності
                        EXECUTE 'ALTER SEQUENCE payment_id_seq RESTART WITH ' || (max_id + 1);
                    END IF;
                END $$;
            """)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Creating Payment Sequence: {str(e)}")
            return False

    def generate_rand_payment_data(self, number_of_operations):
        c = self.conn.cursor()
        try:
            c.execute("""
                INSERT INTO "payment" ("payment_id", "booking_id", "amount", "payment_date", "payment_status")
                SELECT 
                    nextval('payment_id_seq'),
                    floor(random() * (COALESCE((SELECT max("booking_id") FROM "booking"), 1)) + 1)::int AS booking_id,
                    round((random() * 100 + 50)::numeric, 2) AS amount,
                    clock_timestamp() - (random() * interval '30 days') AS payment_date,
                    CASE 
                        WHEN random() < 0.5 THEN true
                        ELSE false
                    END AS payment_status
                FROM generate_series(1, %s);
            """, (number_of_operations,))
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Generating Payment Data: {str(e)}")
            return False

    def truncate_payment_table(self):
        c = self.conn.cursor()
        try:
            # Очищення таблиці payment
            c.execute('DELETE FROM "payment"')
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            print(f"Error With Truncating Payment Table: {str(e)}")
            return False

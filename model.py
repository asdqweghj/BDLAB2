import psycopg

class Model:
    def __init__(self):
        self.conn = psycopg.connect(
            dbname='postgres',
            user='postgres',
            password='Ddd.12350987',
            host='localhost',
            port=5432
        )
        self.create_tables()

    def create_tables(self):
        c = self.conn.cursor()
        # Check for tables
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'booking')")
        booking_table_exists = c.fetchone()[0]

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'facility')")
        facility_table_exists = c.fetchone()[0]

        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'payment')")
        payment_table_exists = c.fetchone()[0]
        
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'users')")
        users_table_exists = c.fetchone()[0]
        
        c.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'venue')")
        venue_table_exists = c.fetchone()[0]

        if not booking_table_exists:
            c.execute('''
                        CREATE TABLE "booking" (
                            "booking_id" SERIAL PRIMARY KEY,
                            "user_id" INTEGER NOT NULL,
                            "facility_id" INTEGER NOT NULL,
                            "booking_date" TIME NOT NULL,
                            "start_time" TIME NOT NULL,
                            "end_time" TIME NOT NULL,
                            "status" BOOLEAN NOT NULL
                        )
                    ''')
        if not facility_table_exists:
            c.execute('''
                        CREATE TABLE "facility" (
                            "facility_id" SERIAL PRIMARY KEY,
                            "venue_id" INTEGER NOT NULL,
                            "facility_name" TEXT NOT NULL,
                            "facility_type" TEXT NOT NULL
                            
                        )
                    ''')
        if not payment_table_exists:
            c.execute('''
                        CREATE TABLE "payment" (
                            "payment_id" SERIAL PRIMARY KEY,
                            "booking_id" INTEGER NOT NULL,
                            "amount" MONEY NOT NULL,
                            "payment_date" TIME NOT NULL,
                            "payment_status" BOOLEAN NOT NULL
                        )
                    ''')
        if not users_table_exists:
            c.execute('''
                        CREATE TABLE "users" (
                            "user_id" SERIAL PRIMARY KEY,
                            "first_name" TEXT NOT NULL,
                            "last_name" TEXT NOT NULL,
                            "email" TEXT NOT NULL,
                            "phone_number" TEXT NOT NULL,
                            "date_of_registration" DATE NOT NULL
                        )
                    ''')
        if not venue_table_exists:
            c.execute('''
                        CREATE TABLE "venue" (
                            "venue_id" SERIAL PRIMARY KEY,
                            "name" TEXT NOT NULL,
                            "address" TEXT NOT NULL,
                            "city" TEXT NOT NULL,
                            "capacity" INTEGER NOT NULL
                        )
                    ''')

        self.conn.commit()
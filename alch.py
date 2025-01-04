from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = 'postgresql+psycopg://postgres:Ddd.12350987@localhost:5432/postgres'
engine = create_engine(DATABASE_URL)

Base = declarative_base()

Session = sessionmaker()
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# The database is initialised.
engine = create_engine("postgresql://irfthlqtvpqjek:35496e5703ba65a8c9fe2a2075e9d4395a7aa6e29ccc710c8f3966ea4eea7ba5@ec2-99-81-16-126.eu-west-1.compute.amazonaws.com:5432/d6iso2pc6h1bkj")
Session = sessionmaker(bind=engine)
Session.expire_on_commit = False

Base = declarative_base()
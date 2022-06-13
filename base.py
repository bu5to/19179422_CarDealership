from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# The database is initialised.
engine = create_engine("postgres://vglacsrsmzejof:07d04f521d50bb923ad37e6fcc55deabdd2a80984ec9d118880d8401abfa0cfc@ec2-54-228-32-29.eu-west-1.compute.amazonaws.com:5432/d3krde6k3aj05f")
Session = sessionmaker(bind=engine)
Session.expire_on_commit = False

Base = declarative_base()
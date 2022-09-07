from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# The database is initialised.
engine = create_engine(os.environ.get('DATABASE_URL'))
Session = sessionmaker(bind=engine)
Session.expire_on_commit = False

Base = declarative_base()
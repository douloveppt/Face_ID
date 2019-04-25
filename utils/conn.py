from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

url = 'mysql+pymysql://root:641212@127.0.0.1:3306/tornado'
engine = create_engine(url)

Base = declarative_base(bind=engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

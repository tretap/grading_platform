import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gpps_db import *
 
engine = create_engine('sqlite:///gpps_db.db', echo=False)
# commit the record the database

def create_class(username,code,name,discription,member):
	Session = sessionmaker(bind=engine)
	session = Session()

	class_r = Classroom(name, username, code, discription, member)
	session.add(class_r)

	session.commit()


def create_assigment(name, classowner, discription, quiz = ""):
	Session = sessionmaker(bind=engine)
	session = Session()

	class_a = Assignment_db(name, classowner, discription, quiz)
	session.add(class_a)

	session.commit()

 
import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gpps_db import *

engine = create_engine('sqlite:///gpps_db.db', echo=False)


# commit the record the database

def create_quiz(problem, solution, example, test_case,id_assign):
    Session = sessionmaker(bind=engine)
    session = Session()

    quiz = Quiz_db(problem, solution, example, test_case,id_assign)
    session.add(quiz)

    session.commit()


def create_assigment(name, classowner, discription, quiz=""):
    Session = sessionmaker(bind=engine)
    session = Session()

    class_a = Assigment_db(name, classowner, discription, quiz)
    session.add(class_a)

    session.commit()

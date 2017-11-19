import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from cpo_db import *

engine = create_engine('sqlite:///cpo_db.db', echo=False)


# commit the record the database

def create_class(user_id,class_name, class_description, class_member):
    Session = sessionmaker(bind=engine)
    session = Session()
    user_account = account_load(user_id)
    class_r = Classroom(class_name, user_account.username,user_account.user_id,class_description, class_member)

    #def __init__(self, name_class, teacher, teacher_code, discription, member="", assignment=""):
    session.add(class_r)

    session.commit()


def create_assigment(name, classowner, discription, quiz=""):
    Session = sessionmaker(bind=engine)
    session = Session()

    class_a = Assignment_db(name, classowner, discription, quiz)
    session.add(class_a)

    session.commit()


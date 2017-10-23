from sqlalchemy import *
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
 
engine = create_engine('sqlite:///gpps_db.db', echo=True)
Base = declarative_base()
 
########################################################################
class Account(Base):
    """"""
    __tablename__ = "account"
 
    id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    code = Column(String)
    role = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, username, password, code, role):
        """"""
        self.username = username
        self.password = password
        self.code = code
        self.role = role
 
# create tables
Base.metadata.create_all(engine)

class Classroom(Base):
    """"""
    __tablename__ = "classroom"
 
    id = Column(Integer, primary_key=True)
    name_class = Column(String)
    teacher = Column(String)
    teacher_code = Column(String)
    discription = Column(String)
    member = Column(String)
    assigment = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, name_class, teacher, teacher_code, discription, member = "", assigment = ""):
        """"""
        self.name_class = name_class
        self.teacher = teacher
        self.teacher_code = teacher_code
        self.discription = discription
        self.member = member
        self.assigment = assigment
 
# create tables
Base.metadata.create_all(engine)

class Assigment_db(Base):
    """"""
    __tablename__ = "assigment"
 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    classowner = Column(String)
    discription = Column(String)
    quiz = Column(String)
 
    #----------------------------------------------------------------------
    def __init__(self, name, classowner, discription, quiz = ""):
        """"""
        self.name = name
        self.classowner = classowner
        self.discription = discription
        self.quiz = quiz
 
# create tables
Base.metadata.create_all(engine)
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
    def __init__(self, name_class, teacher, teacher_code, discription, member = "", assignment = ""):
        """"""
        self.name_class = name_class
        self.teacher = teacher
        self.teacher_code = teacher_code
        self.discription = discription
        self.member = member
        self.assignment = assignment
 
# create tables
Base.metadata.create_all(engine)

class Assignment_db(Base):
    """"""
    __tablename__ = "assignment"
 
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

class Quiz_db(Base):
    """"""
    __tablename__ = "quiz"

    #problem = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    problem = Column(String)
    solution = Column(String)
    example = Column(String)
    test_case = Column(String)
    id_assign  = Column(String)

    def __init__(self, problem, solution, example, test_case,id_assign):

        self.problem = problem
        self.solution = solution
        self.example = example
        self.test_case = test_case
        self.id_assign = id_assign

# create tables
Base.metadata.create_all(engine)
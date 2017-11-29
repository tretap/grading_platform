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
    #----------------------------------------------------------------------
    def __init__(self, username, password):
        """"""
        self.username = username
        self.password = password
 

########################################################################
class Student_information(Base):
    """"""
    __tablename__ = "student_information"
 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    lastname = Column(String)
    student_id = Column(String)
    role = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, name, lastname, student_id, role):
        """"""
        self.name = name
        self.lastname = lastname
        
        self.student_id = student_id
        self.role = role

########################################################################
class Classboard(Base):
    """"""
    __tablename__ = "classboard"
 
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, name, description):
        """"""
        self.name = name
        self.description = description
 

########################################################################
class Classboard_member(Base):
    """"""
    __tablename__ = "classboard_member"
 
    id = Column(Integer, primary_key=True)
    _id = Column(Integer)
    member = Column(Integer)
    #----------------------------------------------------------------------
    def __init__(self, _id, member):
        """"""
        self._id = _id
        self.member = member


########################################################################
class Classboard_db_assignment(Base):
    """"""
    __tablename__ = "classboard_listof_assignment"
 
    id = Column(Integer,primary_key=True)
    _id = Column(Integer)
    assignment = Column(Integer)
    #----------------------------------------------------------------------
    def __init__(self, _id, assignment):
        """"""
        self._id = _id
        self.assignment = assignment


########################################################################
class Assignment(Base):
    """"""
    __tablename__ = "assignment"
 
    id = Column(Integer,primary_key=True)
    name = Column(String)
    description = Column(String)
    scoring_type = Column(String)
    assignment_score = Column(Integer)
    open_time = Column(String)
    close_time = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, name, description, scoring_type, assignment_score, open_time, close_time):
        """"""
        self.name = name
        self.description = description
        self.scoring_type = scoring_type
        self.assignment_score = assignment_score
        self.open_time = open_time
        self.close_time = close_time


########################################################################
class Assignment_db_quiz(Base):
    """"""
    __tablename__ = "assignment_listof_quiz"
 
    id = Column(Integer,primary_key=True)
    _id = Column(Integer)
    quiz = Column(Integer)
    #----------------------------------------------------------------------
    def __init__(self, _id, quiz):
        """"""
        self._id = _id
        self.quiz = quiz


########################################################################
class Quiz(Base):
    """"""
    __tablename__ = "quiz"
 
    id = Column(Integer,primary_key=True)
    name = Column(String)
    description = Column(String)
    solution = Column(String)
    example = Column(String)
    testcase = Column(String)
    #----------------------------------------------------------------------
    def __init__(self, name, description, solution, example, testcase):
        """"""
        self.name = name
        self.description = description
        self.solution = solution
        self.example = example
        self.testcase = testcase
########################################################################
class Submission_log(Base):
    __tablename__ = "Submission_log"

    class_id = Column(Integer, primary_key=True)
    assignment_id = Column(Integer)
    quiz_id = Column(Integer)
    answer_id = Column(String)
    time = Column(String)
    user_id = Column(String)
    client_ip  = Column(String)

    def __init__(self,class_id,assignment_id,quiz_id,answer_id,user_id,client_ip,time):
        """"""
        self.class_id = class_id
        self.assignment_id = assignment_id
        self.quiz_id = quiz_id
        self.answer_id = answer_id
        self.user_id = user_id
        self.client_ip = client_ip
        self.time = time

    ########################################################################
class Login_log(Base):
    __tablename__ = "Login_log"

    log_index = Column(Integer, primary_key=True)
    user_id = Column(String)
    time = Column(String)
    client_ip  = Column(String)
    def __init__(self, user_id,client_ip, time):
        """"""
        self.user_id = user_id
        self.time = time
        self.client_ip = client_ip


# create tables
Base.metadata.create_all(engine)
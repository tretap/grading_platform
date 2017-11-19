from sqlalchemy import *
#from sqlalchemy import Column, Date, Integer,create_engine, String

from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()
engine = create_engine('sqlite:///cpo_db.db', echo=True)

class Account(Base):
    """"""
    __tablename__ = "account"

    user_id = Column(Integer, primary_key=True)
    username = Column(String)
    password = Column(String)
    student_id = Column(String)
    role = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, username, password, student_id, role):
        """"""
        self.username = username
        self.password = password
        self.student_id = student_id
        self.role = role


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

    # ----------------------------------------------------------------------
    def __init__(self, name_class, teacher, teacher_code, discription, member="", assignment=""):
        """"""
        self.name_class = name_class
        self.teacher = teacher
        self.teacher_code = teacher_code
        self.discription = discription
        self.member = member
        self.assignment = assignment


class Assignment_db(Base):
    """"""
    __tablename__ = "assignment"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    classowner = Column(String)
    discription = Column(String)
    quiz = Column(String)

    # ----------------------------------------------------------------------
    def __init__(self, name, classowner, discription, quiz=""):
        """"""
        self.name = name
        self.classowner = classowner
        self.discription = discription
        self.quiz = quiz





class Quiz_db(Base):
    """"""
    __tablename__ = "quiz"

    # problem = Column(String, primary_key=True)
    id = Column(Integer, primary_key=True)
    problem = Column(String)
    solution = Column(String)
    example = Column(String)
    test_case = Column(String)
    id_assign = Column(String)

    def __init__(self, problem, solution, example, test_case, id_assign):
        self.problem = problem
        self.solution = solution
        self.example = example
        self.test_case = test_case
        self.id_assign = id_assign


#Base.metadata.create_all(engine)

class account_load():
    user_id = None
    username = None
    password = None
    student_id = None
    role = None

    def __init__(self,input_user_id):
        metadata = MetaData(engine)
        account_table = Table('account', metadata, autoload=True)

        account_data = account_table.select().execute()


        for row in account_data:
            if input_user_id == row.user_id:
                self.user_id = row.user_id
                self.username = row.username
                self.password = row.password
                self.student_id = row.student_id
                self.role = row.role
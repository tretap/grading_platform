import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.inspection import inspect

#inspect(a).identity

from gpps_db import *
 
engine = create_engine('sqlite:///gpps_db.db', echo=False)
# commit the record the database

#------------------This Section for Create DB------------------------#

def add_account(username, password, name, lastname, student_id, role):
    Session = sessionmaker(bind=engine)
    session = Session()

    _account = Account(username, password)
    _profile = Student_information( name, lastname, student_id, role)

    session.add(_account)
    session.add(_profile)

    session.commit()

def create_classroom(name,discription,id_teacher):
    Session = sessionmaker(bind=engine)
    session = Session()

    class_ = Classboard(name, discription)
    session.add(class_)
    session.commit()

    result = session.query(Classboard).filter(Classboard.name.in_([name])).first()

    class_mem = Classboard_member(result.id,id_teacher)
    session.add(class_mem)
    session.commit()

def add_member(id_class, id_member):
    Session = sessionmaker(bind=engine)
    session = Session()

    class_ = Classboard_member(id_class, id_member)
    session.add(class_)

    session.commit()


def create_assigment(id_class, name, description, scoring_type, assignment_score, open_time, close_time):
    Session = sessionmaker(bind=engine)
    session = Session()

    _assignment = Assignment(name, description, scoring_type, assignment_score, open_time, close_time)
    session.add(_assignment)
    session.commit()

    result = session.query(Assignment).filter(Assignment.name.in_([name])).first()

    assignment_info = Classboard_db_assignment(id_class,result.id)
    session.add(assignment_info)
    session.commit()


def create_quiz_db(id_assignment, name, problem, solution, example, testcase):
    Session = sessionmaker(bind=engine)
    session = Session()

    _quiz = Quiz(name, problem, solution, example, testcase)
    session.add(_quiz)
    session.commit()

    result = session.query(Quiz).filter(Quiz.name.in_([name])).first()

    quiz_info = Assignment_db_quiz(id_assignment, result.id)
    session.add(quiz_info)
    session.commit()

#-----------------------------------------------------------------------------------------------#

#----------------------This Section for GET INFORMATION FORM DB --------------------------------#

def get_login(POST_USERNAME, POST_PASSWORD):
    Session = sessionmaker(bind = engine)
    s = Session()

    query = s.query(Account).filter(Account.username.in_([POST_USERNAME]), Account.password.in_([POST_PASSWORD]))
    result = query.first()

    return result

def get_role(id_member):
    Session = sessionmaker(bind = engine)
    s = Session()

    query = s.query(Student_information).filter(Student_information.id.in_([id_member]))
    result = query.first()

    return result.role

def get_username(id_member):
    Session = sessionmaker(bind = engine)
    s = Session()

    query = s.query(Account).filter(Account.id.in_([id_member]))
    result = query.first()

    return result.username

def get_allClassID(id_member):

    metadata = MetaData(engine)
    all_class = Table('classboard_member', metadata, autoload = True).select().execute()

    result  = []

    for row in all_class:
        if row.member == id_member:
            result.append(row._id)

    return result

def get_allmemberClassID(id_class):

    metadata = MetaData(engine)
    all_class = Table('classboard_member', metadata, autoload = True).select().execute()

    result  = []

    for row in all_class:
        if row._id == id_class:
            result.append(row.member)

    return result

def get_ClassInfo(id_class):

    Session = sessionmaker(bind = engine)
    s = Session()

    query = s.query(Classboard).filter(Classboard.id.in_([id_class]))
    result = query.first()

    return result 

def get_allAssignmentID(id_class):

    metadata = MetaData(engine)
    all_assignment = Table('classboard_listof_assignment', metadata, autoload = True).select().execute()

    result  = []

    for row in all_assignment :
        if row._id == id_class:
            result.append(row.assignment)

    return result

def get_AssignmentInfo(id_assignment):

    Session = sessionmaker(bind = engine)
    s = Session()

    query = s.query(Assignment).filter(Assignment.id.in_([id_assignment]))
    result = query.first()

    return result 

def get_allQuizID(id_assignment):

    metadata = MetaData(engine)
    all_quiz = Table('assignment_listof_quiz', metadata, autoload = True).select().execute()

    result  = []

    for row in all_quiz:
        if row._id == id_assignment:
            result.append(row.quiz)

    return result

def get_QuizInfo(id_quiz):

    Session = sessionmaker(bind = engine)
    s = Session()

    query = s.query(Quiz).filter(Quiz.id.in_([id_quiz]))
    result = query.first()

    return result 


#-----------------------------------------------------------------------------------------------#

#----------------------This Section for EDIT INFORMATION FORM DB --------------------------------#
def edit_classroom(id_class,name,discription):
    Session = sessionmaker(bind=engine)
    session = Session()

    id_class = int(id_class)
    class_ = session.query(Classboard).filter(Classboard.id.in_([id_class])).first()

    class_.name = name
    class_.description = discription

    session.commit()

def edit_assignment_db(id_assignment, name, description, scoring_type, assignment_score, open_time, close_time):
    Session = sessionmaker(bind=engine)
    session = Session()

    id_assignment = int(id_assignment)
    class_ = session.query(Assignment).filter(Assignment.id.in_([id_assignment])).first()

    class_.name = name
    class_.description = description
    class_.scoring_type = scoring_type
    class_.assignment_score = assignment_score
    class_.open_time = open_time
    class_.close_time = close_time

    session.commit()

#-----------------------------------------------------------------------------------------------#

#----------------------This Section for DELETE INFORMATION FORM DB --------------------------------#
def delete_classroom(id_class):
    Session = sessionmaker(bind=engine)
    session = Session()

    _class = session.query(Classboard).filter(Classboard.id.in_([id_class])).first()
    session.delete(_class)
    session.commit()

    #-------------------DELETE ASSIGNMENT IN CLASS------------#

    list_of_assignment = get_allAssignmentID(id_class)
    print(list_of_assignment)

    for i in list_of_assignment:
        delete_assigment(id_class, int(i))

    #-------------------DELETE MEMBER IN CLASS----------------#

    list_of_member = get_allmemberClassID(id_class)
    print(list_of_member)

    for i in list_of_member:
        delete_member(id_class, int(i))

    #---------------------------------------------------------#

def delete_member(id_class, id_member):
    Session = sessionmaker(bind=engine)
    session = Session()

    class_ = session.query(Classboard_member).filter(Classboard_member._id.in_([id_class]),Classboard_member.member.in_([id_member])).first()
    session.delete(class_)

    session.commit()


def delete_assigment(id_class, id_assignment):
    Session = sessionmaker(bind=engine)
    session = Session()

    _assignment = session.query(Assignment).filter(Assignment.id.in_([id_assignment])).first()
    session.delete(_assignment)
    session.commit()

    result = session.query(Classboard_db_assignment).filter(Classboard_db_assignment._id.in_([id_class]),Classboard_db_assignment.assignment.in_([id_assignment])).first()
    session.delete(result)
    session.commit()

    list_of_quiz = get_allQuizID(id_assignment)

    for i in list_of_quiz:
        delete_quiz_db(id_assignment, int(i))


def delete_quiz_db(id_assignment, id_quiz):
    id_quiz = int(id_quiz)

    Session = sessionmaker(bind=engine)
    session = Session()

    query = session.query(Quiz).filter(Quiz.id.in_([id_quiz]))
    _quiz = query.first()
    session.delete(_quiz)
    session.commit()

    result = session.query(Assignment_db_quiz).filter(Assignment_db_quiz._id.in_([id_assignment]),Assignment_db_quiz.quiz.in_([id_quiz])).first()
    session.delete(result)
    session.commit()

    #For more about Quiz student db delete

def add_Submission_log(class_id,assignment_id,quiz_id,answer_id,user_id,client_ip,time):
    Session = sessionmaker(bind=engine)
    session = Session()

    log =  Submission_log(class_id, assignment_id, quiz_id, answer_id, user_id,client_ip, time)
    session.add(log)
    session.commit()

def add_login_log(user_id,client_ip, time):
    Session = sessionmaker(bind=engine)
    session = Session()

    log =  Login_log(user_id,client_ip, time)

    session.add(log)
    session.commit()
def get_testcase(id_quiz):
    Session = sessionmaker(bind=engine)
    s = Session()

    query = s.query(Quiz).filter(Quiz.id.in_([int(id_quiz)]))
    result = query.first()

    return result.testcase

def get_solution(id_quiz):
    Session = sessionmaker(bind=engine)
    s = Session()

    query = s.query(Quiz).filter(Quiz.id.in_([int(id_quiz)]))
    result = query.first()

    return result.solution


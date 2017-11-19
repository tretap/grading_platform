from flask import Flask, flash, redirect , render_template, request,session ,abort
from sqlalchemy import *
import os
import importlib
from CPO_create_class import *

from sqlalchemy.orm import sessionmaker
engine = create_engine('sqlite:///gpps_db.db', echo=False)

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

from cpo_db import *


@app.route("/")
def home():
    if not session.get('logged_in'):
        return render_template('login.html')

    else :

        return home_page()

@app.route('/login', methods=['POST'])
def login():
    POST_USERNAME = str(request.form['username'])
    POST_PASSWORD = str(request.form['password'])
    Session = sessionmaker(bind = engine)
    s = Session()
    query = s.query(Account).filter(Account.username.in_([POST_USERNAME]), Account.password.in_([POST_PASSWORD]))
    result = query.first()
    print("query = ")

    if result:
        login_account = account_load(result.user_id)
        session['logged_in'] = True
        session['user_id'] = login_account.user_id
        session['class'] = None
        print('login sucessfuly')
        return home_page()
    else :
        print('login fail')
        return render_template('login.html',s_w_html = "wrong id!")


@app.route('/logout')
def logout():
    session['logged_in'] = False
    session['user_id'] = None
    session['class'] = None
    return home()

@app.route("/classboard") #main page
def home_page():
    print('homepage')
    metadata = MetaData(engine)
    user_account = account_load(session['user_id'])

    class_table = Table('classroom',metadata, autoload = True)
    class_data = class_table.select().execute()

    list_html = []
    dict_html = {}

    for row in class_data :

        list_student_id_st = row.member.split(",")
        list_student_id_th = row.teacher_id.split(",")

        if (user_account.student_id in list_student_id_st )or (str(user_account.user_id) in list_student_id_th or user_account.role == 'admin'):

            dict_html['id'] = row.id
            dict_html['name'] = row.name_class
            dict_html['name_teacher'] = row.teacher
            dict_html['about'] = row.description
            list_html.append(dict_html)
            dict_html = {}
    print( list_student_id_th)
    return render_template('classboard.html',list_html = list_html,role = user_account.role,name = user_account.username)

def classboard_loading():
    return home_page()

@app.route('/createclass')
def class_create_page():
    return render_template('createclass.html')

@app.route('/createclass', methods=['POST'])
def make_class():

    Session = sessionmaker(bind = engine)
    s = Session()
    user_account = account_load(session['user_id'])
    class_name = str(request.form['classname'])
    about_class = str(request.form['classdescription'])
    member = str(request.form['member'])


    if class_name == "" or class_name == " " or about_class == "" or about_class == " ":
        return render_template('createclass.html', error_msn = "Sorry sir, name or about can't be blank!")

    if len(about_class) < 1 :
        return render_template('createclass.html', error_msn = "Description must be 10 or more characters")

    query = s.query(Classroom).filter(Classroom.name_class.in_([class_name]))
    result = query.first()

    if result :
        return render_template('createclass.html', error_msn = "This class has already in system .")
    create_class(user_account.user_id,class_name,about_class,member)
    #def create_class(class_name, class_description, class_member):

    return classboard_loading()
@app.route('/classboard_load')
def classboard_loading():
    return home_page()

@app.route("/load_class/<string:class_name>")
def loadingclass(class_name):

    user_account = account_load(session['user_id'])
    session['class'] = class_name

    metadata = MetaData(engine)




    class_a = Table('assignment',metadata, autoload = True)
    dt_a = class_a.select().execute()

    list_html = []
    dict_html = {}

    for row in dt_a :
        #row.name,row.owner
        if row.classowner == class_name :
            dict_html['name'] = row.name
            dict_html['about'] = row.description 

            list_html.append(dict_html)

            dict_html = {}

    print(list_html)

    if user_account.role == 'admin':
        return render_template('assigmentboard.html', list_html=list_html, code='admin', role='admin')
    return render_template('assigmentboard.html',list_html = list_html,code = user_account.student_id,role = user_account.role)

@app.route('/cam_load')
def assigment_create_page():
    return render_template('assignmentcreate.html')



@app.route('/createassigment', methods=['POST'])
def do_assigment():

    Session = sessionmaker(bind = engine)
    s = Session()

    assig_name = str(request.form['a_name'])
    about_assig = str(request.form['a_about'])


    if assig_name == "" or assig_name == " " or about_assig == "" or about_assig == " ":
        return render_template('assignmentcreate.html', error_msn = "Sorry sir, name or about can't be blank!")

    if len(about_assig) < 10 :
        return render_template('assignmentcreate.html', error_msn = "Description must be 10 or more characters!")

    query = s.query(Assignment_db).filter(Assignment_db.name.in_([assig_name]))
    result = query.first()

    if result :
        return render_template('assignmentcreate.html', error_msn = "This assignment has already in system .")

    #--------------------------#

    metadata = MetaData(engine)






    create_assigment(assig_name, session['class'], about_assig)

    return loadingclass(session['class'])

@app.route('/quiz_load')
def quiz_board_page_load():
	return loadingquiz(assignment_now) #Just bug , but it can work short time.

@app.route("/quiz_load/<string:quiz_name>")
def loadingquiz(quiz_name):
	global assignment_now
	assignment_now = quiz_name

	metadata = MetaData(engine)

	#######
	ac = Table('account', metadata, autoload=True)

	dt_ac = ac.select().execute()

	code = ""
	role = ""

	for row in dt_ac:
		if username_gobal == row.username:
			code = row.code
			role = row.role

	#######

	class_a = Table('quiz', metadata, autoload=True)
	dt_a = class_a.select().execute()

	list_html = []
	dict_html = {}

	for row in dt_a:
		# row.name,row.owner
		if row.id_assign == assignment_now:
			dict_html['problem'] = row.problem.split(":")[0]
			#dict_html['rank'] = None

			list_html.append(dict_html)

			dict_html = {}

	#print(list_html)

	return render_template('quizboard.html', list_html=list_html, code=code, role=role)


@app.route('/quizpage_load/<string:quiz_name>')
def quiz_page_load(quiz_name, error="", code=""):
    # quiz_info_html = {'problem':'problem data','solution':'solution data','example':'example data'}

    metadata = MetaData(engine)

    class_a = Table('quiz', metadata, autoload=True)
    dt_a = class_a.select().execute()

    quiz_info_html = {}

    for row in dt_a:
        # row.name,row.owner
        if row.problem.split(":")[0] == quiz_name:
            quiz_info_html = {'name': row.problem.split(":")[0], 'problem': row.problem.split(":")[1],
                              'solution': row.solution, 'example': row.example}
            # dict_html['rank'] = None

    return render_template('submission.html', quiz_info=quiz_info_html, error=error, code=code)


if __name__ == '__main__':
    app.debug = False
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8000)
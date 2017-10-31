
from flask import Flask, flash, redirect , render_template, request,session ,abort

import os

from sqlalchemy.orm import sessionmaker
#from tabledef import *
#from create_user import *
from create_quiz import create_quiz
from gpps_db import *
from create_class_file import *

#wait for new version

engine = create_engine('sqlite:///gpps_db.db', echo=False)

app = Flask(__name__)

username_gobal = ""
class_now = ""
assignment_now = ""

#-------------------------#
# This Sector for Login & Logout System and Home Page 

@app.route("/")
def home():
	if not session.get('logged_in'):
		return render_template('login.html')#,s_w_html = s_w)

	else :
		#return render_template('home.html')
		return home_page(username_gobal)

@app.route('/login', methods=['POST'])
def do_login():

	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])

	#-----------------------------------# For Check in database
	Session = sessionmaker(bind = engine)
	s = Session()
	query = s.query(Account).filter(Account.username.in_([POST_USERNAME]), Account.password.in_([POST_PASSWORD]))
	result = query.first()
	#-----------------------------------#

	if result:
		session['logged_in'] = True

		global username_gobal

		username_gobal = POST_USERNAME
		return home_page(POST_USERNAME)
	else :
		return render_template('login.html',s_w_html = "OMG Something wrong!")

@app.route('/logout')
def logout():
	session['logged_in'] = False
	global username_gobal
	global class_name
	username_gobal = ""
	class_now = ""
	assignment_now = ""
	return home()

#-------------------------#
@app.route('/classboard_load')
def classboard_loading():
	return home_page(username_gobal)

@app.route("/classboard")
def home_page(username):

	metadata = MetaData(engine)
	ac = Table('account', metadata, autoload = True)

	dt_ac = ac.select().execute()

	code = ""
	role = ""

	for row in dt_ac:
		if username == row.username :
			code = row.code
			role = row.role

	class_r = Table('classroom',metadata, autoload = True)
	dt = class_r.select().execute()

	list_html = []
	dict_html = {}

	for row in dt :
		#row.name,row.owner
		list_code_st = row.member.split(",") 
		list_code_th = row.teacher_code.split(",")

		if code in list_code_st or code in list_code_th:
			dict_html['id'] = row.id
			dict_html['name'] = row.name_class
			dict_html['name_teacher'] = row.teacher
			dict_html['about'] = row.discription

			list_html.append(dict_html)

			dict_html = {}

	return render_template('classboard.html',list_html = list_html,role = role)

@app.route('/createclass_load')
def class_create_page():
	return render_template('createclass.html')

@app.route('/createclass', methods=['POST'])
def do_class():

	Session = sessionmaker(bind = engine)
	s = Session()

	class_name = str(request.form['classname'])
	about_class = str(request.form['classdescription'])
	member = str(request.form['member'])


	if class_name == "" or class_name == " " or about_class == "" or about_class == " ":
		return render_template('createclass.html', error_msn = "Sorry sir, name or about can't be blank!") 

	#if POST_USERNAME.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890' or POST_PASSWORD.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890':
		#return render_template('register.html', error_msn = "you can use only Eng Charecter and Diginumber")

	if len(about_class) < 10 :
		return render_template('createclass.html', error_msn = "Description must be 10 or more characters")

	query = s.query(Classroom).filter(Classroom.name_class.in_([class_name]))
	result = query.first()

	if result :
		return render_template('createclass.html', error_msn = "This class has already in system .")

	#--------------------------#

	metadata = MetaData(engine)
	ac = Table('account', metadata, autoload = True)

	dt_ac = ac.select().execute()

	code = ""
	role = ""

	for row in dt_ac:
		if username_gobal == row.username :
			code = row.code

	create_class(username_gobal,code,class_name,about_class,member)

	return classboard_loading()

@app.route("/load_class")
def auto_load_class():
	return loadingclass(class_now)

@app.route("/load_class/<string:class_name>")
def loadingclass(class_name):

	global class_now
	class_now = class_name

	metadata = MetaData(engine)

	ac = Table('account', metadata, autoload = True)

	dt_ac = ac.select().execute()

	code = ""
	role = ""

	for row in dt_ac:
		if username_gobal == row.username :
			code = row.code
			role = row.role

	class_a = Table('assignment',metadata, autoload = True)
	dt_a = class_a.select().execute()

	list_html = []
	dict_html = {}

	for row in dt_a :
		#row.name,row.owner
		if row.classowner == class_name :
			dict_html['name'] = row.name
			dict_html['about'] = row.discription 

			list_html.append(dict_html)

			dict_html = {}

	print(list_html)


	return render_template('assigmentboard.html',list_html = list_html,code = code,role = role)

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

	#if POST_USERNAME.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890' or POST_PASSWORD.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890':
		#return render_template('register.html', error_msn = "you can use only Eng Charecter and Diginumber")

	if len(about_assig) < 10 :
		return render_template('assignmentcreate.html', error_msn = "Description must be 10 or more characters!")

	query = s.query(Assignment_db).filter(Assignment_db.name.in_([assig_name]))
	result = query.first()

	if result :
		return render_template('assignmentcreate.html', error_msn = "This assignment has already in system .")

	#--------------------------#

	metadata = MetaData(engine)
	ac = Table('account', metadata, autoload = True)

	dt_ac = ac.select().execute()

	code = ""
	role = ""

	for row in dt_ac:
		if username_gobal == row.username :
			code = row.code

	create_assigment(assig_name, class_now, about_assig)

	return loadingclass(class_now)

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

@app.route('/create_quiz')
def load_quiz_create_page():
	return render_template('createquiz.html')

@app.route('/createquiz', methods=['POST'])
def do_quiz():

	Session = sessionmaker(bind=engine)
	s = Session()

	problem = str(request.form['problem'])
	solution = str(request.form['solution'])
	example = str(request.form['example'])
	test_case = str(request.form['test-case'])
	id_assignm = assignment_now
	#rank = str(request.form['rank'])

	if problem == "" or solution == "" or example == "" or test_case == "":
		return render_template('createquiz.html', error_msn = "Sorry sir, name or about can't be blank!")

	query = s.query(Quiz_db).filter(Quiz_db.problem.in_([problem.split(":")[0]]))
	result = query.first()

	if result :
		return render_template('createquiz.html', error_msn = "This Quiz has already in system .")

	create_quiz(problem, solution, example, test_case, id_assignm)

	return loadingquiz(assignment_now)

@app.route('/quizpage_load/<string:quiz_name>')
def quiz_page_load(quiz_name):
	#quiz_info_html = {'problem':'problem data','solution':'solution data','example':'example data'}
	
	metadata = MetaData(engine)

	class_a = Table('quiz', metadata, autoload=True)
	dt_a = class_a.select().execute()

	quiz_info_html = {}

	for row in dt_a:
		# row.name,row.owner
		if row.problem.split(":")[0] == quiz_name:
			quiz_info_html = {'name':row.problem.split(":")[0],'problem':row.problem.split(":")[1],'solution':row.solution,'example':row.example}
			#dict_html['rank'] = None

	return render_template('submission.html',quiz_info = quiz_info_html)

@app.route('/submission_answer/<string:quiz_name>', methods=['POST'])
def submission_answer(quiz_name):


	f = request.form['file']
	if (f != None and f != ''):
		with open(f) as file_data:
			x = file_data.readlines()
		print("choosen file")
		print(x)
	else:
		print("no file choosen")
		return quiz_page_load(quiz_name)

	return quiz_page_load(quiz_name)

if __name__ == '__main__':
	app.debug = True
	app.secret_key = os.urandom(12)
	app.run(host='localhost', port=8000)
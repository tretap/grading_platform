from flask import Flask 
from flask import Flask, flash, redirect , render_template, request,session ,abort

import os

from sqlalchemy.orm import sessionmaker
#from tabledef import *
#from create_user import *

from gpps_db import * 
from create_class_file import *

#wait for new version

engine = create_engine('sqlite:///gpps_db.db', echo=False)

app = Flask(__name__)

username_gobal = ""
class_now = ""

#-------------------------#
# This Sector for Login & Logout System and Home Page 

@app.route("/")
def home():
	if not session.get('logged_in'):
		return render_template('login.html')#,s_w_html = s_w)

	else :
		#return render_template('home.html')
		return home_page(username_gobal)
"""
@app.route('/registers')
def register_page():
	return render_template('register.html')
"""


"""
@app.route('/register', methods=['POST'])
def do_register():

	Session = sessionmaker(bind = engine)
	s = Session()

	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])
	POST_C_PASSWORD = str(request.form['password-confrim'])

	#--------------------------#Check Text in register page , Protection 

	if POST_PASSWORD != POST_C_PASSWORD:
		return render_template('register.html', error_msn = "Password != Confrim Password")

	if " " in POST_USERNAME or " " in POST_PASSWORD:
		return render_template('register.html', error_msn = "Can't Use Free Space in username or password  ") 

	#if POST_USERNAME.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890' or POST_PASSWORD.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890':
		#return render_template('register.html', error_msn = "you can use only Eng Charecter and Diginumber")

	if len(POST_PASSWORD) < 7 :
		return render_template('register.html', error_msn = "Password should more 7 char!")

	query = s.query(User).filter(User.username.in_([POST_USERNAME]))
	result = query.first()

	if result :
		return render_template('register.html', error_msn = "This user has already in system .")

	#--------------------------#

	create_id(POST_USERNAME,POST_PASSWORD)

	return home()

"""

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
		return render_template('login.html',s_w_html = "OMG Something wrong !")

@app.route('/logout')
def logout():
	session['logged_in'] = False
	global username_gobal
	global class_name
	username_gobal = ""
	class_now = ""
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
		return render_template('createclass.html', error_msn = "Sorry sir, name or about can't be void!") 

	#if POST_USERNAME.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890' or POST_PASSWORD.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890':
		#return render_template('register.html', error_msn = "you can use only Eng Charecter and Diginumber")

	if len(about_class) < 10 :
		return render_template('createclass.html', error_msn = "Something wrong in about area!")

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

	class_a = Table('assigment',metadata, autoload = True)
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
		return render_template('assignmentcreate.html', error_msn = "Sorry sir, name or about can't be void!") 

	#if POST_USERNAME.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890' or POST_PASSWORD.lower() not in 'abcdefghijklmnopqrstuvwxyz1234567890':
		#return render_template('register.html', error_msn = "you can use only Eng Charecter and Diginumber")

	if len(about_assig) < 10 :
		return render_template('assignmentcreate.html', error_msn = "Something wrong in about area!")

	query = s.query(Assigment_db).filter(Assigment_db.name.in_([assig_name]))
	result = query.first()

	if result :
		return render_template('assignmentcreate.html', error_msn = "This assigment has already in system .")

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
def quiz_create_page():
	return render_template('quizboard.html') #Just bug , but it can work short time.

"""
@app.route("/load_post/<int:post_id>")
def loading_post(post_id):
	db = create_engine('sqlite:///board.db', echo = False)
	
	metadata = MetaData(db)
	posts = Table('posts',metadata, autoload = True)

	dt = posts.select().execute()

	dict_html = {}

	for row in dt :
		#row.name,row.owner
		if int(row.id) == int(post_id) :
			dict_html['name'] = row.name
			dict_html['owner'] = row.owner
			dict_html['msn'] = row.messenger 


	return render_template('post.html',post = dict_html)

"""

if __name__ == '__main__':
	app.debug = True
	app.secret_key = os.urandom(12)
	app.run(host='localhost', port=8000)
from flask import Flask 
from flask import Flask, flash, redirect , render_template, request,session ,abort

import os
import importlib
import sys

from functional import *
from sqlalchemy.orm import sessionmaker
from gpps_db import *
from db_function import *

sys.path.append("/Users/mac/Documents/GitHub/grading_platform/images/")

engine = create_engine('sqlite:///gpps_db.db', echo=False)

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))



#-------------------------#
# This Sector for Login & Logout System and Home Page 

@app.route ("/")
def home():
	if not session.get('logged_in'):
		return render_template('login.html')

	else :
		return home_page()

@app.route('/login', methods=['POST'])
def do_login():

	POST_USERNAME = str(request.form['username'])
	POST_PASSWORD = str(request.form['password'])

	result = get_login(POST_USERNAME, POST_PASSWORD)

	if result:
		session['logged_in'] = True
		session['id'] = result.id

		return home_page()
	else :
		return render_template('login.html',s_w_html = "Can't to access to system.!")

@app.route('/logout')
def logout():
	session['logged_in'] = False
	session['id'] = None
	session['assignment'] = None
	session['class'] = None

	return home()

#--------------------------------------------------------#

# This Section for Class Board #

@app.route('/classboard_load')
def classboard_loading():
	return home_page()

@app.route("/classboard")
def home_page():
	
	list_html = []
	dict_html = {}

	_class = get_allClassID(session.get('id'))

	session['class'] = None
	session['assignment'] = None

	for one_class in  _class:
		_info = get_ClassInfo(one_class)

		dict_html['id'] = _info.id
		dict_html['name'] = _info.name
		dict_html['about'] = _info.description

		list_html.append(dict_html)

		dict_html = {}


	return render_template('classboard.html',list_html = list_html,role = get_role(session.get('id')),name = get_username(session.get('id')))

@app.route('/createclass_load')
def class_create_page():
	return render_template('createclass.html')

@app.route('/createclass', methods=['POST'])
def create_class():

	if get_role(session.get('id')) == "student":
		return home_page()

	class_name = str(request.form['classname'])
	about_class = str(request.form['classdescription'])


	if class_name == ""  or about_class == "" :
		return render_template('createclass.html', error_msn = "Sorry sir, name or about can't be blank!") 


	create_classroom(class_name, about_class, session.get('id'))

	return home_page()

@app.route("/load_class")
def auto_load_class():
	return loadingclass(session.get('class'))

@app.route("/load_class/<string:id_class>")
def loadingclass(id_class):

	#----------------------CHECK---------------------#

	list_secure = get_allClassID(session.get('id'))

	if int(id_class) not in list_secure:
		return home_page()

	#-------------------------------------------------#

	session['class'] = int(id_class)
	session['assignment'] = None

	list_html = []
	dict_html = {}
	role = get_role(session.get('id'))

	list_assignment = get_allAssignmentID(int(id_class))

	for single_assignment in list_assignment :
		
		_info = get_AssignmentInfo(single_assignment)

		if (check_datetime_withNow(_info.open_time) == True) or role != "student":
			if (check_datetime_withNow(_info.close_time) == False) or role != "student":

				dict_html['id'] = _info.id
				dict_html['name'] = _info.name
				dict_html['about'] = _info.description

				list_html.append(dict_html)

				dict_html = {}


	return render_template('assigmentboard.html',list_html = list_html, role = get_role(session.get('id')),name = get_username(session.get('id')))

@app.route('/load_editClass/<string:class_id>')
def load_editclass(class_id,error_msn = ""):

	#---------------------------- Protection System ------------------------#

	if get_role(session.get('id')) == "student":
		return home_page()

	#---------------------------- Protection system-------------------------#

	result = get_ClassInfo(class_id)

	_class = {}

	_class['id'] = result.id
	_class['name'] = result.name
	_class['about'] = result.description

	session['class'] = int(class_id)

	return render_template('editclass.html', error_msn = error_msn , _class = _class)


@app.route('/editclass', methods=['POST'])
def edit_class():

	if get_role(session.get('id')) == "student":
		return home_page()

	class_name = str(request.form['classname'])
	about_class = str(request.form['classdescription'])


	if class_name == ""  or about_class == "" :
		return load_editclass(session.get('class') , error_msn = "Sorry sir, name or about can't be blank!")

	edit_classroom(session.get('class'),class_name,about_class)

	return home_page()

@app.route('/delete_class/<string:id_class>')
def delete_class(id_class):

	#---------------------------- Protection System ------------------------#

	role = get_role(session.get('id'))

	if role == "student":
		return home_page()

	for i in id_class:
		if i not in "0123456789":
			return home_page()

	#---------------------------- Protection system-------------------------#

	delete_classroom(int(id_class))

	return home_page()


@app.route('/create_assignment_load')
def assigment_create_page():
	return render_template('assignmentcreate.html')

@app.route('/createassigment', methods=['POST'])
def do_assigment():

	assig_name = str(request.form['a_name'])
	about_assig = str(request.form['a_about'])
	assignment_score = str(request.form['score'])
	opentime = str(request.form['start1']) + "/" + str(request.form['start2']).replace(":","/")
	closetime = str(request.form['end1']) + "/" + str(request.form['end2']).replace(":","/")


	if assig_name == ""  or about_assig == "" :
		return render_template('assignmentcreate.html', error_msn = "Sorry sir, name or about can't be blank!") 
	#--------------------------#

	create_assigment(session.get('class'), assig_name, about_assig, "auto", assignment_score, opentime, closetime)

	return loadingclass(session.get('class'))


@app.route('/load_editAssignment/<string:id_assignment>')
def load_editassignment(id_assignment,error_msn = ""):

	#---------------------------- Protection System ------------------------#

	if get_role(session.get('id')) == "student":
		return home_page()

	#---------------------------- Protection system-------------------------#

	result = get_AssignmentInfo(int(id_assignment))
	session['assignment'] = int(id_assignment)

	time_split = result.open_time.split("/")
	_time = {}
	_time['open_time1'] = time_split[0] +"/" + time_split[1] +"/" + time_split[2]
	_time['open_time2'] = time_split[3] +":" + time_split[4]

	time_split = result.close_time.split("/")
	_time['close_time1'] = time_split[0] + "/" + time_split[1] + "/" + time_split[2]
	_time['close_time2'] = time_split[3] + ":" + time_split[4]

	return render_template('editassignment.html', error_msn = error_msn , assig = result, _time = _time)


@app.route('/editassignment', methods=['POST'])
def edit_assignment():

	assig_name = str(request.form['a_name'])
	about_assig = str(request.form['a_about'])
	assignment_score = str(request.form['score'])
	opentime = str(request.form['start1']) + "/" + str(request.form['start2']).replace(":", "/")
	closetime = str(request.form['end1']) + "/" + str(request.form['end2']).replace(":", "/")

	if assig_name == "" or about_assig == "":
		return load_editassignment(session.get('assignment'), error_msn="Sorry sir, name or about can't be blank!")
	# --------------------------#

	edit_assignment_db(session.get('assignment'), assig_name, about_assig, "auto", assignment_score, opentime, closetime)

	return loadingclass(session.get('class'))

@app.route('/delete_assignment/<string:id_assignment>')
def delete_assignment(id_assignment):

	#---------------------------- Protection System ------------------------#

	role = get_role(session.get('id'))

	if role == "student":
		return loadingclass(session.get('class'))

	for i in id_assignment:
		if i not in "0123456789":
			return loadingclass(session.get('class'))

	#---------------------------- Protection system-------------------------#

	delete_assigment(session.get('class'), int(id_assignment))

	return loadingclass(session.get('class'))

@app.route("/load_assignment/<string:id_assignment>")
def loadingassignment(id_assignment):

	id_assignment = int(id_assignment)

	#-------------------CHECK ------------------------------#
	
	list_secure = get_allAssignmentID(session.get('class'))

	if id_assignment not in list_secure:
		return loadingclass(session.get('class'))

	#-------------------------------------------------------#

	session['assignment'] = id_assignment

	list_html = []
	dict_html = {}

	list_quiz = get_allQuizID(id_assignment)

	for single_quiz in list_quiz:

		print(single_quiz)
		_info = get_QuizInfo(single_quiz)

		dict_html['id'] = _info.id
		dict_html['name'] = _info.name

		list_html.append(dict_html)

		dict_html = {}

	return render_template('quizboard.html', list_html=list_html, role = get_role(session.get('id')),name  = get_username(session.get('id')))

@app.route("/quizpage_load/<string:id_quiz>")
def loadingquiz(id_quiz):

	id_quiz = int(id_quiz)

	#-------------------CHECK ------------------------------#
	
	list_secure = get_allQuizID(session.get('assignment'))

	if id_quiz not in list_secure:
		return loadingassignment(session.get('assignment'))

	#-------------------------------------------------------#

	_info = get_QuizInfo(id_quiz)
	quiz_info_html = {'name':_info.name,'problem':_info.description,'example':_info.example}

	return render_template('submission.html', quiz_info = quiz_info_html, error = "", role = get_role(session.get('id')),name  = get_username(session.get('id')))

@app.route('/create_quiz')
def load_quiz_create_page():
	return render_template('createquiz.html')

@app.route('/createquiz', methods=['POST'])
def create_quiz():

	name = str(request.form['name'])
	problem = str(request.form['problem'])
	solution = str(request.form['solution'])
	example = str(request.form['example'])
	testcase = str(request.form['test-case'])
	n = []
	p = []
	sol = []
	e = []
	tc = []

	if name == "" or problem == "" or solution == "" or example == "" or testcase == "":
		
		target = os.path.join(APP_ROOT, 'images/')
		
		if not os.path.isdir(target):
			os.mkdir(target)
		
		#print(request.files.getlist("file"))
		
		for file in request.files.getlist("file"):
			
			filename = file.filename
			
			if ".py" not in filename:
				return render_template('createquiz.html', error_msn="Sorry sir, name or about can't be blank!")
			
			destination = "".join([target, filename])
			
			file.save(destination)

			pyfile = destination
			
			print('py file = ' + pyfile)
			#print(filename[:len(filename) - 3])
			
			"""prob = importlib.import_module(filename[:len(filename) - 3])"""
			f = open(pyfile, 'r')
			j = 0
			i = 0
			name_mode = False
			prob_mode = False
			solu_mode = False
			exam_mode = False
			test_mode = False

			for line in f:
				if name_mode:
					if("# Problem" not in line):
						n.append(line)

				if "# Name" in line:
					name_mode = True
					test_mode = False
					solu_mode = False
					exam_mode = False
					prob_mode = False

				if prob_mode:
					if ("# Solution" not in line):
						p.append(line)

				if "# Problem" in line:
					name_mode = False
					test_mode = False
					solu_mode = False
					exam_mode = False
					prob_mode = True
					i = i + 1
					j = 0

				if solu_mode:
					if ("# Example" not in line):
						sol.append(line)

				if "# Solution" in line:
					name_mode = False
					test_mode = False
					solu_mode = True
					exam_mode = False
					prob_mode = False

				if exam_mode:
					if ("# Test cases" not in line):
						e.append(line)

				if "# Example" in line:
					name_mode = False
					test_mode = False
					solu_mode = False
					exam_mode = True
					prob_mode = False

				if test_mode:
					tc.append(line)
					try:
						out = eval(command[:-2])
						out = str(out) + "\n"

						"""testcase = out"""
						
					except:
						continue
				if "# Test cases" in line:
					name_mode = False
					test_mode = True
					solu_mode = False
					exam_mode = False
					prob_mode = False
		destination = destination.replace('/','\\')
		f.close()
		os.remove(destination)
					

		name = "".join(n)
		name = name.replace('\"\"\"', '')
		name = name.replace('\'\'\'', '')
		problem = "".join(p)
		solution = "".join(sol)
		example = "".join(e)
		testcase = "".join(tc)
		#print(problem, solution, example);

	create_quiz_db(session.get('assignment'), name, problem, solution, example, testcase)

	return loadingassignment(session.get('assignment'))

@app.route('/delete_quiz/<string:id_quiz>')
def delete_quiz(id_quiz):

	#---------------------------- Protection System ------------------------#

	role = get_role(session.get('id'))

	if role == "student":
		return loadingassignment(session.get('assignment'))

	for i in id_quiz:
		if i not in "0123456789":
			return loadingassignment(session.get('assignment'))

	#---------------------------- Protection system-------------------------#

	delete_quiz_db(session.get('assignment'), int(id_quiz))

	return loadingassignment(session.get('assignment'))

@app.route('/submission_answer/<string:id_quiz>', methods=['POST'])
def submission_answer(id_quiz):
	target = os.path.join(APP_ROOT, 'images/')
	if not os.path.isdir(target):
		os.mkdir(target)
	print(request.files.getlist("file"))

	for file in request.files.getlist("file"):

		filename = file.filename
		destination = "".join([target, filename])
		if ".py" not in file.filename:
			return render_template('submission.html', quiz_info=id_quiz, error="",role=get_role(session.get('id')), name=get_username(session.get('id')))
		file.save(destination)

		pyfile = destination
		print('py file = ' + pyfile)
		print(filename[:len(filename) - 3])
		#prob = importlib.import_module(filename[:len(filename) - 3])
		f = open(pyfile, 'r')
		j = 0
		i = 0
		write_mode = False
		"""print(f.read())"""

		for line in f:
			# print(line)
			if "# Problem" in line:
				write_mode = False
				i = i + 1
				j = 0
			if write_mode:
				j = j + 1
				command = line.replace('print(', 'prob.')
				try:
					out = eval(command[:-2])
					out = str(out) + "\n"

					fin = open(filename + "_" + str(i) + str(j) + '_input.txt', 'w')
					fin.write(line)

					fout = open(filename + "_" + str(i) + str(j) + '_output.txt', 'w')
					fout.write(out)
				except:
					continue

			if "# Test cases" in line:
				write_mode = True

		destination = destination.replace('/','\\')
		f.close()
		os.remove(destination)
				
		return render_template('submission.html', quiz_info=id_quiz, error="",role=get_role(session.get('id')), name=get_username(session.get('id')))


if __name__ == '__main__':
	app.debug = False
	app.secret_key = os.urandom(12)
	app.run(host='0.0.0.0', port=8000)
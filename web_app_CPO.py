from flask import Flask, flash, redirect , render_template, request,session ,abort
from sqlalchemy import *
import os
import importlib
from create_class_file import *

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
    print(result.username)
    if result:
        login_account = account_load(result.user_id)
        session['logged_in'] = True
        session['user_id'] = login_account.user_id
        print('login sucessfuly')
        return home_page()
    else :
        print('login fail')
        return render_template('login.html',s_w_html = "wrong id!")


@app.route('/logout')
def logout():
	session['logged_in'] = False

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
        list_student_id_th = row.teacher_student_id.split(",")

        if user_account.student_id in list_student_id_st or user_account.student_id in list_student_id_th:
            dict_html['id'] = row.id
            dict_html['name'] = row.name_class
            dict_html['name_teacher'] = row.teacher
            dict_html['about'] = row.discription
            list_html.append(dict_html)
            dict_html = {}
    print( user_account.username)
    return render_template('classboard.html',list_html = list_html,role = user_account.role,name = user_account.username)
def classboard_loading():
	return home_page()

@app.route('/createclass')
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

    if len(about_class) < 1 :
        return render_template('createclass.html', error_msn = "Description must be 10 or more characters")

    query = s.query(Classroom).filter(Classroom.name_class.in_([class_name]))
    result = query.first()

    if result :
        return render_template('createclass.html', error_msn = "This class has already in system .")
    create_class(class_name,about_class,member)

    return classboard_loading()

if __name__ == '__main__':
	app.debug = False
	app.secret_key = os.urandom(12)
	app.run(host='localhost', port=8000)
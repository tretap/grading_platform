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

@app.route('/load_dataLog')
def load_dataLog():
    login_html = get_login_logAll_db()
    submission_html = get_submission_logAll_db()

    return render_template('log.html',login_html = login_html,submission_html = submission_html)

@app.route('/load_profile_out')
def load_profileOut():
    profile = get_information_user(session.get('id'))

    return render_template('Profile_out.html',profile = profile)

@app.route('/load_edit_profile_out')
def load_editprofileOut():
    profile = get_information_user(session.get('id'))

    return render_template('Profile_edit.html',profile = profile)


@app.route('/editprofile', methods=['POST'])
def edit_profile_web():

    name = str(request.form['Name'])
    lastname = str(request.form['Surname'])


    if name == ""  or lastname == "" :
        return load_editprofileOut()

    profile = get_information_user(session.get('id'))

    edit_information_user(session.get('id'),name,lastname,profile.student_id,profile.role)

    return home_page()

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

@app.route('/load_memberClass')
def load_memberClass_web():

    list_member = get_allmemberClassID(session.get('class'))

    list_html = []
    dict_html = {}

    for i in list_member:
        result = get_information_user(i)

        dict_html['id'] = result.id
        dict_html['student_id'] = result.student_id
        dict_html['name'] = result.name

        #print(dict_html)
        list_html.append(dict_html)

        dict_html = {}

    return render_template('Member_list.html',list_html = list_html,name = get_username(session.get('id')),role = get_role(session.get('id')))

@app.route('/add_Memberclass_web', methods=['POST'])
def add_member_class_web():

    data_name = 'class' + '_' + str(session.get('class')) + '_member'
    target = os.path.join(APP_ROOT, 'log_addmember\\')
    if not os.path.isdir(target):
        os.mkdir(target)
    file = request.files.getlist("file")[0]
    filename = file.filename
    if ".csv" not in filename:
        return load_memberClass_web()

    destination = target + data_name + '.csv'
    file.save(destination)

    pyfile = destination
    f = open(pyfile, 'r')

    for line in f:
        information_line = line.split(",")
        if information_line[0] == "" or information_line[1] == "":
            os.remove(destination)
            return load_memberClass_web()

        if  check_account_db(information_line[0]):
            _id = get_id_member_db(information_line[0])
            add_member(session.get('class'),int(_id))
        else :
            _id = add_account(information_line[0],"password",(information_line[1].split(" "))[0],(information_line[1].split(" "))[1],information_line[0],"student")
            add_member(session.get('class'),int(_id))

    os.remove(destination)
    return load_memberClass_web()


@app.route('/delete_memberClass/<string:id_member>')
def delete_member_class_web(id_member):
    delete_member(session.get('class'),int(id_member))

    return load_memberClass_web()

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


    return render_template('assigmentboard.html',about = get_ClassInfo(session.get('class')).description,list_html = list_html, role = get_role(session.get('id')),name = get_username(session.get('id')))

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
    if "/" not in request.form['start1'] or ":" not in request.form['start2'] or "/" not in request.form['end1'] or ":" not in request.form['end2']:
        return render_template('assignmentcreate.html', error_msn="Time platform Error!")

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
def loadingquiz(id_quiz, error="", result=[], preload_code=''):
    id_quiz = int(id_quiz)

    # -------------------CHECK ------------------------------#

    list_secure = get_allQuizID(session.get('assignment'))

    if id_quiz not in list_secure:
        return loadingassignment(session.get('assignment'))

    # -------------------------------------------------------#

    _info = get_QuizInfo(id_quiz)
    quiz_info_html = {'id': _info.id, 'name': _info.name, 'problem': _info.description, 'example': _info.example}
    target = os.path.join(APP_ROOT, 'submission\\')
    id = session.get('id')
    id_class = session.get('class')
    id_assignment = session.get('assignment')
    data_name = str(id) + '_' + str(id_class) + '_' + str(id_assignment)+'_' + str(id_quiz)
    if os.path.exists(target + data_name + '.py'):
        f_answer = open(target + data_name + '.py', 'r')
    else:
        f_answer = []
    # print(list(f_answer))
    preload_code = "".join(list(f_answer))
    return render_template('submission.html', quiz_info=quiz_info_html, error=error, role=get_role(session.get('id')),
                           name=get_username(session.get('id')), result=result, preload_code=preload_code)



@app.route('/create_quiz')
def load_quiz_create_page():
    return render_template('createquiz.html')


@app.route('/createquiz', methods=['POST'])
def create_quiz():
    id = session.get('id')
    id_class = session.get('class')
    id_assignment = session.get('assignment')
    name = str(request.form['name'])
    problem = str(request.form['problem'])
    solution = str(request.form['solution'])
    example = str(request.form['example'])
    testcase = str(request.form['test-case'])
    n = []
    p = []
    sol = []
    e = []
    get_test_case = ''
    data_name = 'solution'  + '_' + str(id_class) + '_' + str(id_assignment)
    target = os.path.join(APP_ROOT, 'solution\\')
    if not os.path.isdir(target):
        os.mkdir(target)
    destination = target + data_name + '.py'
    if name == "" or problem == "" or solution == "" or example == "" or testcase == "":

        file = request.files.getlist("file")[0]

        filename = file.filename
        if ".py" not in filename:
            return render_template('createquiz.html', error_msn="Sorry sir, name or about can't be blank!")
        file.save(destination)

        pyfile = destination
        print('py file = ' + pyfile)
        print(filename[:len(filename) - 3])
        prob = importlib.import_module(filename[:len(filename) - 3])
        f = open(pyfile, 'r')
        j = 0
        i = 0
        name_mode = False
        prob_mode = False
        solu_mode = False
        exam_mode = False
        test_mode = False
        """print(f.read())"""

        for line in f:
            print(line)
            if name_mode:
                if ("# Problem" not in line):
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
                j = j + 1
                get_test_case += line
                command = line.replace('print(', 'prob.')
                try:
                    out = eval(command[:-2])
                    out = str(out) + "\n"
                    print("Answer : " + out)

                except:
                    continue
            if "# Test cases" in line:
                name_mode = False
                test_mode = True
                solu_mode = False
                exam_mode = False
                prob_mode = False
        f.close()
        os.remove(destination)
        name = "".join(n)
        name = name.replace('\"\"\"', '')
        problem = "".join(p)
        problem = problem.replace('\"\"\"', '')
        solution = "".join(sol)
        example = "".join(e)
        testcase = get_test_case
        print(problem, solution, example)
    else:

        pass

    quiz_id = create_quiz_db(session.get('assignment'), name, problem, solution, example, testcase)
    file_name = target + data_name + '_' + str(quiz_id) + '.py'
    final_sol = open(file_name, 'w')
    final_sol.write(solution)

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
    score = 0
    id = session.get('id')
    id_class = session.get('class')
    id_assignment = session.get('assignment')
    add_Submission_log(id_class, id_assignment, id_quiz, id, str(request.remote_addr), datetime.datetime.now().strftime("%d/%m/%y/%H/%M"))

    target = os.path.join(APP_ROOT, 'submission\\')
    result =  []

    if not os.path.isdir(target):
        os.mkdir(target)
    #print(request.files.getlist("file"))

    #get file
    file = request.files.getlist("file")[0]
    filename = file.filename

    #print(destination)
    data_name = str(id) + '_' + str(id_class) + '_' + str(id_assignment) + '_'+str(id_quiz)
    if ".py" not in file.filename:#not file upload or invalid file
        #print("Get data")
        answer = str(request.form['answer'])

        if (answer != ""):#text field check
            print('from text field')
            print(answer)

            fin = open(target + data_name + '.py', 'w')
            answer = answer.replace('\r','')

            fin.write(answer)
            fin.close()
        else:
            return loadingquiz(int(id_quiz), "no answer",result)
    else:
        destination = target + data_name + '.py'
        file.save(destination)


    ####edit
    sol_name = 'solution' + '_' + str(id_class) + '_' + str(id_assignment) + '_' + str(id_quiz)
    sol_module = importlib.import_module('solution.'+sol_name)
    try:
        prob = importlib.import_module('submission.'+data_name)
    except:
        result.append('syntax error')
        print('syntax error')
        return loadingquiz(int(id_quiz), "", result)

    f_answer = open(target +data_name+  '.py', 'r')

    importlib.reload(prob)

    for i in f_answer:
        if 'print' == i[0:5]:
            command_data = remove_print(i)
            print("command_data : "+command_data)
            get_out = 'error'
            try:
                get_out = str(eval("prob."+command_data))
            except:
                pass
                #continue
            print("get_out : " + get_out)
            result.append(get_out)

    print('find testcase')
    testcase_str = get_testcase(id_quiz)
    testcase_str = testcase_str.replace('\r','')
    testcase_line = testcase_str.split('\n')
    #print(testcase_line)

    for i in range(len(testcase_line)):
        test_line = testcase_line[i]
        sol = str(eval("sol_module."+test_line))
        answer = ''
        try:
            answer =  str(eval("prob."+test_line))
        except:
            pass
        result.append('testcase '+str(i))
        result.append('solution = '+sol)
        result.append('answer   = '+ answer)
        if sol == answer:
            result.append('pass')
        else :
            result.append('fail')

            if check_score_table(id,id_assignment,id_quiz):
                score_id = get_score_table_id(id,id_assignment,id_quiz)
                edit_score_table(score_id, id, id_assignment, id_quiz, 0, datetime.datetime.now().strftime("%d/%m/%y/%H/%M"))
            else :
                create_score_table(id, id_assignment, id_quiz, 0, datetime.datetime.now().strftime("%d/%m/%y/%H/%M"))
            return loadingquiz(int(id_quiz), "fail", result)
        print('sol = '+sol+' answer = '+answer)

    ####compile

    score = get_AssignmentInfo(int(id_assignment)).assignment_score
    print('score = '+str(score))

    if check_score_table(id, id_assignment, id_quiz):
        score_id = get_score_table_id(id, id_assignment, id_quiz)
        edit_score_table(score_id, id, id_assignment, id_quiz, score, datetime.datetime.now().strftime("%d/%m/%y/%H/%M"))
    else:
        create_score_table(id, id_assignment, id_quiz, score, datetime.datetime.now().strftime("%d/%m/%y/%H/%M"))

    return loadingquiz(int(id_quiz), "pass",result)

if __name__ == '__main__':
    app.debug = False
    app.secret_key = os.urandom(12)
    app.run(host='0.0.0.0', port=8000)
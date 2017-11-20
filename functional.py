import datetime 

def check_datetime_withNow(time_input):
	time_now = datetime.datetime.now().strftime("%d/%m/%y/%H/%M")

	time_input = time_input.split("/")
	time_now = time_now.split("/")

	for i in range(len(time_input)):
		time_input[i] = int(time_input[i])
	for i in range(len(time_now)):
		time_now[i] = int(time_now[i])

	obj_date_input = datetime.datetime(time_input[2],time_input[1],time_input[0],time_input[3],time_input[4])
	obj_date_now = datetime.datetime(time_now[2],time_now[1],time_now[0],time_now[3],time_now[4])

	obj_date = obj_date_now - obj_date_input


	if int(obj_date.days) > 0 :
		return True
	else :
		return False
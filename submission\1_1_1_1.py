 def loop_F_inal(num):
	_sum = ""
	sum_ = ""
	for i in range(1,num+1):
		for j in range(1,i+1):
			_sum += str(j)

	for i in range(num, 0,-1):
		for j in range(i,0,-1):
			sum_ += str(j)

	#for i in range(num, 0,-1):

	return _sum + sum_[1::]

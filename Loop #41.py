# Name #
'''TEST HELLO FILE'''

# Problem #

'''
Loop #41
	Hello Form Outer sideeeeeeeeeeeeeeee
'''

# Solution #
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

# Example #
print(loop_F_inal(3))
print(loop_F_inal(4))

# Test cases #
loop_F_inal(8)
loop_F_inal(7)
loop_F_inal(6)
loop_F_inal(9)
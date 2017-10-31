
import math
def sin_gen(amplitude,size):
    data = [0 for x in range(size)]

    for i in range(size):
        data[i] = amplitude*math.sin(i/size * (2*math.pi) )

    return data

# Example #
#print(sin_gen(1,4))
#print(sin_gen(2,8))

# Test cases #
print(sin_gen(1,4))
print(sin_gen(2,8))
print(sin_gen(3,16))
print(sin_gen(4,32))

#0.0, 1.1480502970952693, 2.1213203435596424, 2.77163859753386, 3.0, 2.77163859753386, 2.121320343559643, 1.1480502970952697, 3.6739403974420594e-16, -1.148050297095269, -2.1213203435596424, -2.7716385975338595, -3.0, -2.77163859753386, -2.121320343559643, -1.148050297095271]
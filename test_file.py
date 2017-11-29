# Name #
"""Test problem"""
# Problem #
"""plus number 20 times"""

# Solution #
def Hello_N_time(n):
    k = 0
    for i in range(n+1):
        k += i
    return k
# Example #
print(Hello_N_time(1))
# Test cases #
print(Hello_N_time(20))


import math


def st_harmonic_cos_amp(data):
    cos_comp = [math.cos(x/len(data) * (2*math.pi) ) for x in range(len(data))]
    result = (2/len(data))*sum([data[x]*cos_comp[x] for x in range(len(data))])

    return  result
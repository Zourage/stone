import math as m
import statistics as s
def hyp(a, b):
    return m.sqrt(((a * a) + (b * b)))
def mid(l):
    t = s.median(l)
    return t
print(hyp(3,4), mid([5,1,9]))

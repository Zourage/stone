def item(a):
    b = a[0]
    for c in a:
        if (c > b):
            b = c
    return b
def sort_put(a):
    b = []
    for c in a:
        d = []
        e = 0
        while ((e < len(b)) and not (b[e] > c)):
            d = (d + [b[e]])
            e = (e + 1)
        d = (d + [c])
        while (e < len(b)):
            d = (d + [b[e]])
            e = (e + 1)
        b = d
    return b
print(item([3,9,2]), sort_put([5,1,4,1,9]))

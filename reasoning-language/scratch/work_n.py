def tally(l):
    m = {}
    for w in l:
        if (w in m):
            m = {**m, w: (m[w] + 1)}
        else:
            m = {**m, w: 1}
    return m
print(tally(["a","b","a"]))

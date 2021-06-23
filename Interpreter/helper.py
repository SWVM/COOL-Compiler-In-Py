def read_list(func, fin):
    length = fin.readline()
    return map( [i for i in range(length)], func(fin) )

def read_lst(func, fin, args=[]):
    count = int(fin.readline())
    lst = []
    for i in range(count):
        lst.append(func(fin, *args))
    return lst

def get_cycle():
    pass

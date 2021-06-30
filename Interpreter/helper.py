from os import name

def error(line, msg):
    print("ERROR: %s: Exception: %s" % (line, msg))
    exit(1)

def read_lst(func, fin):
    length = int(fin.readline())
    lst    = []
    for i in range(length):
        lst.append(func(fin))
    return lst

class Recurse(Exception):
    def __init__(self, so, e, exp):
        self.so = so
        self.e  = e
        self.exp= exp

def tail_recursive(f):
    def decorated(*args, **kwargs):
        while True:
            try:
                return f(*args, **kwargs)
            except Recurse as r:
                args = r.args
                kwargs = r.kwargs
                continue
    return decorated

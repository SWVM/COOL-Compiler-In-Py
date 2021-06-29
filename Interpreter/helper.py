
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
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

def rec(*args, **kwargs):
    print("")
    raise Recurse(*args, **kwargs)

def rec1(*args, **kwargs):
    print("")
    return rec1(*args, **kwargs)

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

if __name__ == "__main__":
    rec1()
    tail_recursive(rec)()
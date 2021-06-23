from helper import *
from env import *

class Cool_Id():
    def __init__(self, name, line):
        self.name = name
        self.line = line



class Cool_Prog():
    def __init__(self, fname):
        self.fin = open(fname, "r")
        self.cmap = {}
        self.imap = {}
        self.pmap = {}

    def read_class_map(self, fin):
        assert fin.readline() == "class_map\n"
        class_num = int(fin.readline())
        for i in range(class_num):
            cname = fin.readline()[:-1]
            self.cmap[cname] = read_list(Cool_attri.read, fin)
        # TODO: class map
    def read_imp_map(self, fin):
        assert fin.readline() == "implementation_map\n"
        class_num = int(fin.readline())
        for i in range(class_num):
            cname = fin.readline()[:-1]
            self.imap[cname] = read_list(Cool_method.read, fin)
        # TODO: imp map
    def read_parent_map(self, fin):
        assert fin.readline() == "parent_map\n"
        class_num = int(fin.readline())
        for i in range(class_num):
            cname = fin.readline()[:-1]
            self.pmap[cname] = fin.readline()[:-1]
        # TODO: parent map





class Cool_attri():
    def read(fin):
        init = fin.readline()[:-1]
        name = fin.readline()[:-1]
        type = fin.readline()[:-1]
        if init == "initializer":
            init = Cool_Expr.read(fin)
            return Cool_attri(name, type, init)
        return Cool_attri(name, type)

    def __init__(self, name, type, init = None):
        self.name = name
        self.type = type
        self.init = init

class Cool_method():
    def read(fin):
        name = fin.readline()[:-1]
        formals = read_list( lambda x: x.readline()[:-1], fin)
        body = Cool_Expr.read(fin)
        return Cool_method(name, formals, body)

    def __init__(self, name, formals, body):
        self.name = name
        self.formals = formals
        self.body = body





class Cool_Expr():
    def __init__(self):
        pass
    def read():
        

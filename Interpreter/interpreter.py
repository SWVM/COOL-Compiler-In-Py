from helper import read_lst
from env import *
from cool_expr import *
import sys


class Cool_Prog():
    def __init__(self, fname):
        self.fin = open(fname, "r")
        self.cmap = {}
        self.imap = {}
        self.pmap = {}

    def read(self):
        self.read_class_map()
        self.read_imp_map()
        self.read_parent_map()
        self.fin.close()

    def read_class_map(self):
        assert self.fin.readline() == "class_map\n"
        class_num = int(self.fin.readline())
        for i in range(class_num):
            cname = self.fin.readline()[:-1]
            self.cmap[cname] = read_lst(Cool_attri.read, self.fin)
        # TODO: class map
    def read_imp_map(self):
        assert self.fin.readline() == "implementation_map\n"
        class_num = int(self.fin.readline())
        for i in range(class_num):
            cname = self.fin.readline()[:-1]
            self.imap[cname] = read_lst(Cool_method.read, self.fin)
        # TODO: imp map
    def read_parent_map(self):
        assert self.fin.readline() == "parent_map\n"
        class_num = int(self.fin.readline())
        for i in range(class_num):
            cname = self.fin.readline()[:-1]
            self.pmap[cname] = self.fin.readline()[:-1]
        # TODO: parent map

    def get_attris(self, cname):
        return self.cmap[cname]:



class Cool_attri():
    def read(fin):
        init = fin.readline()[:-1]
        name = fin.readline()[:-1]
        type = fin.readline()[:-1]
        if init == "initializer":
            init = Cool_expr.read(fin)
            return Cool_attri(name, type, init)
        return Cool_attri(name, type)

    def __init__(self, name, type, init = None):
        self.name = name
        self.type = type
        self.init = init

class Cool_method():
    def read(fin):
        name = fin.readline()[:-1]
        formals = read_lst( lambda x: x.readline()[:-1], fin)
        owner = fin.readline()[:-1]
        body = Cool_expr.read(fin)
        return Cool_method(name, formals, body)

    def __init__(self, name, formals, body):
        self.name = name
        self.formals = formals
        self.body = body

class evaluator():
    def __init__(self, prog):
        self.prog = prog
    
    def run(self):
        entry = Expr_DDispatch("", Expr_New("","Main"), Expr_New("","main"), [])
        return self.eval(Cool_void(), Store(), Env(), entry)
    
    def eval(self, so, s, e, exp):
        if isinstance(exp, Expr_Assign):
            pass
        elif isinstance(exp, Expr_New):
            cname = exp.tname.name
            if cname == "SELF_TYPE":
                cname = so.get_type()
            attris = self.prog.get_attris(cname)
            name_to_loc = {x.name : s.malloc() for x in attris}
            atypes      = [x.type for x in attris]
            # locs   = list(map(lambda x: s.malloc(), attris))
            # anames = list(map(lambda x: x.name,     attris))
            # atypes = list(map(lambda x: x.type,     attris))
            
            if cname == "Int":
                
            

        



if __name__ == "__main__":
    prog = Cool_Prog("D:\\SysDir\\Documents\\COOL-Compiler-In-Py\\Interpreter\\arith.cl-type")
    
    s = Store()
    e = Env()
    

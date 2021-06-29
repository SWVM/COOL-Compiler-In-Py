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
            methods = read_lst(Cool_method.read, self.fin)
            for m in methods:
                self.imap[ (cname, m.name) ] = m
            # self.imap[cname] = read_lst(Cool_method.read, self.fin)
        # TODO: imp map
    def read_parent_map(self):
        assert self.fin.readline() == "parent_map\n"
        class_num = int(self.fin.readline())
        for i in range(class_num):
            cname = self.fin.readline()[:-1]
            self.pmap[cname] = self.fin.readline()[:-1]
        # TODO: parent map

    def get_attris(self, cname):
        return self.cmap[cname]

    def get_formals(self, cname, mname):
        return self.imap[ (cname, mname) ].formals

    def get_mbody(self, cname, mname):
        return self.imap[ (cname, mname) ].body




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

class Evaluator():
    def __init__(self, prog):
        self.prog = prog
        self.s    = Store()
    
    def run(self):
        entry = Expr_DDispatch("", Expr_New("",Cool_Id("Main")), Cool_Id("main"), [])
        decorated_eval = tail_recursive(Evaluator.eval)

        return decorated_eval(self, Cool_void(), Store(), Env(), entry)
    
    def eval(self, so, s, e, exp):
        if isinstance(exp, Expr_Assign):
            var = exp.var.name
            loc = e[var]
            rhs = exp.expr
            val = self.eval(so, s, e, rhs)
            self.s.set(loc, val)
            return val

        elif isinstance(exp, Expr_Integer):
            return Cool_int(exp.int_value)

        elif isinstance(exp, Expr_String):
            return Cool_string(exp.str_value)

        elif isinstance(exp, Expr_Bool):
            return Cool_bool(exp.bool_value)

        elif isinstance(exp, Expr_Id):
            name = exp.cool_id.name
            if  name == "self":
                return so
            else:
                return self.s[ e[name] ]

        elif isinstance(exp, Expr_Arith):
            v1 = self.eval(so, s, e, exp.e1)
            v2 = self.eval(so, s, e, exp.e2)
            # TODO: how to do puls? 
            if exp.op == "plus":
                return v1+v2
            elif exp.op == "times":
                return v1*v2
            elif exp.op == "minus":
                return v1-v2
            elif exp.op == "divide":
                return v1/v2

        elif isinstance(exp, Expr_New):
            # inc stack dpeth? idk
            cname = exp.tname.name
            if cname == "SELF_TYPE":
                cname = so.get_type()

            attris = self.prog.get_attris(cname)
            anames = [x.name for x in attris]
            atypes = [x.type for x in attris]
            ainits = [x.init for x in attris]
            locs   = [self.s.malloc() for x in attris]
            init_values = [Cool_value.init_for(t) for t in atypes]
            name_loc    = {name:loc for name,loc in zip(anames, locs)}
            # Ojb creation
            if cname == "Int":
                v1 = Cool_int()
            elif cname == "String":
                v1 = Cool_string()
            elif cname == "Bool":
                v1 = Cool_bool()
            else:
                v1 = Cool_obj(cname, name_loc )
            # attris init
            self.s.update( {loc:val for loc,val in zip(locs, init_values) } )
            # evaluate init
            for var,init in zip(anames, ainits):
                if init:
                    self.eval(v1, s, name_loc, Expr_Assign("", Cool_Id(var), init))
            # raise? maybe not
            return v1

        elif isinstance(exp, Expr_DDispatch):
            line      = exp.line
            expr      = exp.expr
            mname     = exp.method.name
            arg_exprs = exp.args
            # eval args
            arg_vals  = [ self.eval(so, s, e, arg_e) for arg_e in arg_exprs ]
            # eval expr/so
            v0 = self.eval(so, s, e, expr)
            cname = v0.get_type()
            if cname == "void":
                error(line, "dispatch on void")
            # get method
            formals = self.prog.get_formals(cname, mname)
            locs    = [self.s.malloc() for f in formals]
            body    = self.prog.get_mbody(cname, mname)
            # bind args 
            args_locs = {arg:loc for arg,loc in zip(formals, locs)}
            self.s.update( {loc:val for loc,val in zip(locs, arg_vals)} )
            # get object env
            attri_locs = v0.get_attris().copy()
            new_e = attri_locs.update(args_locs)
            raise Recurse(self, v0, s, new_e, body)

        elif isinstance(exp, Expr_SDispatch):
            line      = exp.line
            expr      = exp.expr
            target    = exp.target.name
            mname     = exp.method.name
            arg_exprs = exp.args
            # eval args
            arg_vals  = [ self.eval(so, s, e, arg_e) for arg_e in arg_exprs ]
            # eval expr/so
            v0 = self.eval(so, s, e, expr)
            cname = v0.get_type()
            if cname == "void":
                error(line, "dispatch on void")
            # get method
            formals = self.prog.get_formals(target, mname)
            locs    = [self.s.malloc() for f in formals]
            body    = self.prog.get_mbody(target, mname)
            # bind args 
            args_locs = {arg:loc for arg,loc in zip(formals, locs)}
            self.s.update( {loc:val for loc,val in zip(locs, arg_vals)} )
            # get object env
            attri_locs = v0.get_attris().copy()
            new_e = attri_locs.update(args_locs)
            raise Recurse(self, v0, s, new_e, body)

        elif isinstance(exp, Expr_SelfDispatch):
            line = exp.line
            expr = Expr_Id("", Cool_Id("self"))
            mname= exp.method
            args = exp.args
            Expr_DDispatch(line, expr, mname, args)
            raise Recurse(self, so, s, e, Expr_DDispatch(line, expr, mname, args))

        elif isinstance(exp, Expr_Block):
            v0 = None
            for expr in exp.exprs:
                v0 = self.eval(so, s, e, expr)
            return v0
        
        elif isinstance(exp, Expr_While):
            predicate = exp.predicate
            body      = exp.body
            val = self.eval(so, s, e, predicate)
            if val.value:
                self.eval(so, s, e, body)
                raise Recurse(self, so, s, e, exp)
            else:
                return Cool_void()

        elif isinstance(exp, Expr_Isvoid):
            v0 = self.eval(so, s, e, exp)
            if isinstance(v0, Cool_void):
                return Cool_bool(True)
            else:
                return Cool_bool(False)

        elif isinstance(exp, Lt):
            # TODO: resume from here
            

        



if __name__ == "__main__":
    prog = Cool_Prog("D:\\SysDir\\Documents\\COOL-Compiler-In-Py\\Interpreter\\test.cl-type")
    prog.read()
    e = Evaluator(prog)
    # e.eval(None, "", {}, Expr_New("",Cool_Id("B")) )
    r = e.run()

    print("DONE")
    

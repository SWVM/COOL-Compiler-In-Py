from copy import deepcopy, copy
from Helpers import *
from Cool_types import Cool_Id

class Typing_env():
    def __init__(self, debug = False):
        self.o = {}
        self.m = {}
        self.c = None
        self.debug = debug
    def clear(self):
        self.__init__(debug == self.debug)
    def cp():
        return deepcopy(self)
    def add_method(self, method):
        pass
    def add_var(self, var):
        pass
    def set_class(self, cname):
        pass

class Cool_expr():
    # factory class
    def read(fin):
        line = fin.readline()[:-1]
        ename= fin.readline()[:-1]
        if ename == "assign":
            var = Cool_Id.read(fin)
            expr= Cool_expr.read(fin)
            return Expr_Assign(line, var, expr)
        elif ename == "dynamic_dispatch ":
            e       = Cool_expr.read(fin)
            m       = Cool_Id.raed(fin)
            args    = read_lst(Cool_expr.read, fin)
            return Expr_DDispatch(line, e, m ,args)
        elif ename == "static_dispatch ":
            e       = Cool_expr.read(fin)
            t       = Cool_Id.read(fin)
            m       = Cool_Id.raed(fin)
            args    = read_lst(Cool_expr.read, fin)
            return Expr_SDispatch(line, e, t, m, args)
        elif ename == "self_dispatch ":
            m       = Cool_Id.raed(fin)
            args    = read_lst(Cool_expr.read, fin)
            return Expr_SelfDispatch(line, m, args)
        elif ename == "if":
            predicate = Cool_expr.read(fin)
            bt        = Cool_expr.read(fin)
            bf        = Cool_expr.read(fin)
            return Expr_If(line, predicate, bt, bf)
        elif ename == "while":
            predicate = Cool_expr.read(fin)
            body      = Cool_expr.read(fin)
            return Expr_While(line, predicate, body)
        elif ename == "block":
            exprs = read_lst(Cool_expr.read, fin)
            return Expr_Block(line, exprs)
        elif ename == "new":
            cname = Cool_Id.read(fin)
            return Expr_New(line, cname)
        elif ename == "isvoid":
            e = Cool_expr.read(fin)
            return Expr_Isvoid(line, e)
        elif ename in ["plus","minus","times","divide"]:
            e1 = Cool_expr.read(fin)
            e2 = Cool_expr.read(fin)
            return Expr_Arith(line, ename, e1, e2)
        elif ename in ["lt","le","eq"]:
            lhs = Cool_expr.read(fin)
            rhs = Cool_expr.read(fin)
            return Expr_Cmp(line, op, lhs, rhs)
        elif ename == "not":
            e = Cool_expr.read(fin)
            return Expr_Not(line, e)
        elif ename == "negate":
            e = Cool_expr.read(fin)
            return Expr_Negate(line, e)
        elif ename == "string":
            s = fin.readline()[:-1]
            return Expr_String(line, s)
        elif ename == "identifier ":
            i = Cool_Id.read(fin)
            return Expr_Id(line, i)
        elif ename in ["true", "false"]:
            return Expr_Bool(ename)
        elif ename == "integer":
            int_value = fin.readline()[:-1]
            return Expr_Integer(line, int_value)
        elif ename == "let":
            fun = lambda x: Expr_Binding()
            bindings = read_lst()
        elif ename == "case":
            # TODO: create read function in each child class/ this might be a better design
        else:
            raise Exception("expr not yet implemented")

    def __init__(self, line, static_type = None):
        self.static_type = static_type
        self.line   = line

    def get_type(self, env):
        return self.static_type if self.static_type else self.eval()

    def eval(self):
        raise Exception("eval not overriden")

    def __str__(self):
        raise Exception("str not overriden")

class Expr_Assign(Cool_expr):
    def __init__(self, line, var, expr):
        self.var = var
        self.expr = expr
        super().__init__(line)
    def __str__(self):
        return "assign\n"

class Expr_DDispatch(Cool_expr):
    def __init__(self, line, expr, method, args):
        self.expr = expr
        self.method = method
        self.args = args
        super().__init__(line)

class Expr_SDispatch(Cool_expr):
    def __init__(self, line, expr, target, method, args):
        self.expr = expr
        self.target = target
        self.method = method
        self.args = args
        super().__init__(line)

class Expr_SelfDispatch(Cool_expr):
    def __init__(self, line, method, args):
        self.method = method
        self.args = args
        super().__init__(line)

class Expr_If(Cool_expr):
    def __init__(self, line, predicate, bt, bf):
        self.predicate = predicate
        self.bt = bt
        self.bf = bf
        super().__init__(line)

class Expr_While(Cool_expr):
    def __init__(self, line, predicate, body):
        self.predicate = predicate
        self.body = body
        super().__init__(line)

class Expr_Block(Cool_expr):
    def __init__(self, line, exprs):
        self.exprs = exprs
        super().__init__(line)

class Expr_New(Cool_expr):
    def __init__(self, line, tname):
        self.tname = tname
        super().__init__(line)

class Expr_Isvoid(Cool_expr):
    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)

class Expr_Arith(Cool_expr):
    def __init__(self, line, op, e1, e2):
        self.e1 = e1
        self.e2 = e2
        self.op = op
        super().__init__(line)

class Expr_Cmp(Cool_expr):
    def __init__(self, line, op, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op  = op
        super().__init__(line)

class Expr_Not(Cool_expr):
    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)

class Expr_Negate(Cool_expr):
    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)

class Expr_Integer(Cool_expr):
    def __init__(self, line, int_value):
        self.int_value = int_value
        super().__init__(line)
    def __str__(self):
        return "int: " + self.int_value + "\n"

class Expr_String(Cool_expr):
    def __init__(self, line, str_value):
        self.str_value = str_value
        super().__init__(line)

class Expr_Id(Cool_expr):
    def __init__(self, line, cool_id):
        self.cool_id = cool_id
        super().__init__(line)

class Expr_Bool(Cool_expr):
    def __init__(self, line, bool_value):
        self.bool_value = bool_value
        super().__init__(line)

class Expr_Let(Cool_expr):
    def __init__(self, line, bindings, body):
        self.bindings = bindings
        self.body = body
        super().__init__(line)

class Expr_Binding(Cool_expr):
    def __init__(self, line, name, btype, expr = None):
        self.name = name
        self.btype= btype
        self.expr = expr
        super().__init__(line)

class Expr_Case(Cool_expr):
    def __init__(self, line, expr, elements):
        self.expr = expr
        self.elements = elements

class Expr_CaseElement(Cool_expr):
    def __init__(self, line, name, ctype, expr):
        self.name = name
        self.btype= btype
        self.expr = expr
        super().__init__(line)

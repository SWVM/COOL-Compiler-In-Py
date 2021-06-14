from copy import deepcopy, copy
from Helpers import *

class Cool_Id():
    def read(fin):
        line = fin.readline()[:-1]
        name = fin.readline()[:-1]
        return Cool_Id(name, line)

    def __init__(self, name, line):
        self.name = name
        self.line = line
    def __str__(self):
        return "Id: %s \t at line %s\n" % (self.name, self.line)
    def __repr__(self):
        return self.__str__()
    def get_name(self):
        return self.name

class Cool_type():
    def __init__(self, tname, selftype = False):
        self.tname = tname
        self.selftype = selftype

    def __eq__(self, other):
        return self.tname == other.tname

    def __str__(self):
        if self.selftype:
            return "SELF_TYPE(%s)" % self.tname
        else:
            return self.tname


class Typing_env():
    def __init__(self, o = None, m = None, c = None, do_debug = False):
        self.o = o
        self.m = m
        self.c = c
        self.do_debug = do_debug
    def debug(self):
        print(self.o)
        print(self.m)
        print(self.c)
    def clear(self):
        self.__init__(debug == self.debug)
    def copy(self):
        return deepcopy(self)
    def add_method(self, method):
        pass
    def add_var(self, var):
        pass
    def add_vars(self, vars):
        self.o.update(vars)
    def set_class(self, cname):
        pass
    def get_selftype(self):
        return self.c
    def get_method_signiture(self, c, m):
        if not (c, m) in self.m:
            raise Exception("unbound method %s" % (var_name))
        return self.m[(c,m)].signiture
    def get_method_return(self, c, m):
        if not (c, m) in self.m:
            raise Exception("unbound method %s" % (var_name))
        return self.m[(c,m)].return_type
    def typeof(self, cid):
        var_name = cid.get_name()
        if not var_name in self.o:
            raise Exception("unbound identifier %s" % (var_name))
        return self.o[var_name]
class Cool_expr():
    INHERITANCE_GRAPH = None

    # factory class
    def read(fin):
        kwargs = {}  # holds extra details for sub classes
        kwargs["line"] = fin.readline()[:-1]
        kwargs["ename"] = fin.readline()[:-1]
        if kwargs["ename"] == "assign":
            return Expr_Assign.read(fin, **kwargs)
        elif kwargs["ename"] == "dynamic_dispatch":
            return Expr_DDispatch.read(fin, **kwargs)
        elif kwargs["ename"] == "static_dispatch":
            return Expr_SDispatch.read(fin, **kwargs)
        elif kwargs["ename"] == "self_dispatch":
            return Expr_SelfDispatch.read(fin, **kwargs)
        elif kwargs["ename"] == "if":
            return Expr_If.read(fin, **kwargs)
        elif kwargs["ename"] == "while":
            return Expr_While.read(fin, **kwargs)
        elif kwargs["ename"] == "block":
            return Expr_Block.read(fin, **kwargs)
        elif kwargs["ename"] == "new":
            return Expr_New.read(fin, **kwargs)
        elif kwargs["ename"] == "isvoid":
            return Expr_Isvoid.read(fin, **kwargs)
        elif kwargs["ename"] in ["plus","minus","times","divide"]:
            return Expr_Arith.read(fin, **kwargs)
        elif kwargs["ename"] in ["lt","le","eq"]:
            return Expr_Cmp.read(fin, **kwargs)
        elif kwargs["ename"] == "not":
            return Expr_Not.read(fin, **kwargs)
        elif kwargs["ename"] == "negate":
            return Expr_Negate.read(fin, **kwargs)
        elif kwargs["ename"] == "string":
            return Expr_String.read(fin, **kwargs)
        elif kwargs["ename"] == "integer":
            return Expr_Integer.read(fin, **kwargs)
        elif kwargs["ename"] == "identifier":
            return Expr_Id.read(fin, **kwargs)
        elif kwargs["ename"] in ["true", "false"]:
            return Expr_Bool.read(fin, **kwargs)
        elif kwargs["ename"] == "let":
            return Expr_Let.read(fin, **kwargs)
        elif kwargs["ename"] == "case":
            return Expr_Case.read(fin, **kwargs)
        else:
            raise Exception("expr not yet implemented: "+ kwargs["ename"])

    def __init__(self, line, static_type = None):
        self.static_type = static_type
        self.line   = line

    def get_type(self, env):
        return self.static_type if self.static_type else self.eval()

    def typeCheck(self, env, inheritance):
        raise Exception("eval not overriden in " + str(type(self)))

    def __str__(self):
        return str(type(self))
        # raise Exception("str not overriden")

class Expr_Assign(Cool_expr):
    def typeCheck(self, env, inheritance):
        vtype = env.typeof(self.var)
        etype = self.expr.typeCheck(env, inheritance)
        if not inheritance.get_node(etype).is_child(vtype):
            raise Exception("%s does not conform %s in assign" % (vtype, etype))
        return etype

    def __init__(self, line, var, expr):
        self.var = var
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        var = Cool_Id.read(fin)
        expr= Cool_expr.read(fin)
        return Expr_Assign(kwargs["line"], var, expr)
    def __str__(self):
        return "assign\n"

class Expr_DDispatch(Cool_expr):
    def typeCheck(self, env, inheritance):
        t0 = self.expr.typeCheck(env, inheritance)
        mname = self.method.get_name()
        signiture = env.get_method_signiture(t0, mname)
        arguments = list(map(lambda x: x.typeCheck(env, inheritance), self.args))
        if not len(signiture) == len(arguments):
            raise Exception("wrong number of acttualy arguments")
        for i in range(len(signiture)):
            if not signiture[i] == arguments[i]:
                raise Exception("argument %d type %s does not conform in formal type %s" % (i, arguments[i], signiture[i]))
        rtype = env.get_method_return(t0, mname)
        if rtype == "SELF_TYPE":
            rtype = env.get_selftype()
        return rtype

    def __init__(self, line, expr, method, args):
        self.expr = expr
        self.method = method
        self.args = args
        super().__init__(line)
    def read(fin, **kwargs):
        e       = Cool_expr.read(fin)
        m       = Cool_Id.read(fin)
        args    = read_lst(Cool_expr.read, fin)
        return Expr_DDispatch(kwargs["line"], e, m ,args)

class Expr_SDispatch(Cool_expr):
    def typeCheck(self, env, inheritance):
        t0 = self.expr.typeCheck(env, inheritance)
        t  = self.target.get_name()
        if not inheritance.get_node(t0).is_child(t):
            raise Exception("%s does not conform to %s in static static dispatch" % (t0, t))
        mname = self.method.get_name()
        signiture = env.get_method_signiture(t, mname)
        arguments = list(map(lambda x: x.typeCheck(env, inheritance), self.args))
        if not len(signiture) == len(arguments):
            raise Exception("wrong number of acttualy arguments")
        for i in range(len(signiture)):
            if not signiture[i] == arguments[i]:
                raise Exception("argument %d type %s does not conform in formal type %s" % (i, arguments[i], signiture[i]))
        rtype = env.get_method_return(t0, mname)
        if rtype == "SELF_TYPE":
            rtype = env.get_selftype()
        return rtype

    def __init__(self, line, expr, target, method, args):
        self.expr = expr
        self.target = target
        self.method = method
        self.args = args
        super().__init__(line)
    def read(fin, **kwargs):
        e       = Cool_expr.read(fin)
        t       = Cool_Id.read(fin)
        m       = Cool_Id.read(fin)
        args    = read_lst(Cool_expr.read, fin)
        return Expr_SDispatch(kwargs["line"], e, t, m, args)

class Expr_SelfDispatch(Cool_expr):
    def typeCheck(self, env, inheritance):
        t0 = env.get_selftype()
        mname = self.method.get_name()
        signiture = env.get_method_signiture(t0, mname)
        arguments = list(map(lambda x: x.typeCheck(env, inheritance), self.args))
        if not len(signiture) == len(arguments):
            raise Exception("wrong number of acttualy arguments")
        for i in range(len(signiture)):
            if not signiture[i] == arguments[i]:
                raise Exception("argument %d type %s does not conform in formal type %s" % (i, arguments[i], signiture[i]))
        rtype = env.get_method_return(t0, mname)
        if rtype == "SELF_TYPE":
            rtype = env.get_selftype()
        return rtype

    def __init__(self, line, method, args):
        self.method = method
        self.args = args
        super().__init__(line)
    def read(fin, **kwargs):
        m       = Cool_Id.read(fin)
        args    = read_lst(Cool_expr.read, fin)
        return Expr_SelfDispatch(kwargs["line"], m, args)

class Expr_If(Cool_expr):
    def typeCheck(self, env, inheritance):
        predicate_type = self.predicate.typeCheck(env, inheritance)
        if not predicate_type == "Bool":
            raise Exception("conditional has type %s instead of bool" % predicate_type)
        bt_type        = self.bt.typeCheck(env, inheritance)
        bf_type        = self.bf.typeCheck(env, inheritance)

        return inheritance.lub(bt_type, bf_type)

    def __init__(self, line, predicate, bt, bf):
        self.predicate = predicate
        self.bt = bt
        self.bf = bf
        super().__init__(line)
    def read(fin, **kwargs):
        predicate = Cool_expr.read(fin)
        bt        = Cool_expr.read(fin)
        bf        = Cool_expr.read(fin)
        return Expr_If(kwargs["line"], predicate, bt, bf)

class Expr_While(Cool_expr):
    def typeCheck(self, env, inheritance):
        predicate_type = self.predicate.typeCheck(env, inheritance)
        if not predicate_type == "Bool":
            raise Exception("conditional has type %s instead of bool" % predicate_type)
        self.body.typeCheck(env, inheritance)

        return "Object"

    def __init__(self, line, predicate, body):
        self.predicate = predicate
        self.body = body
        super().__init__(line)
    def read(fin, **kwargs):
        predicate = Cool_expr.read(fin)
        body      = Cool_expr.read(fin)
        return Expr_While(kwargs["line"], predicate, body)


class Expr_Block(Cool_expr):
    def typeCheck(self, env, inheritance):
        for e in self.exprs:
            rtype = e.typeCheck(env, inheritance)
        return rtype

    def __init__(self, line, exprs):
        self.exprs = exprs
        super().__init__(line)
    def read(fin, **kwargs):
        exprs = read_lst(Cool_expr.read, fin)
        return Expr_Block(kwargs["line"], exprs)

class Expr_New(Cool_expr):
    def typeCheck(self, env, inheritance):
        tname = self.tname.get_name()
        if tname == "SELF_TYPE":
            return env.get_selftype()
        if not inheritance.has_node(tname):
            raise Exception("unknown type %s in new" % tname)
        return tname

    def __init__(self, line, tname):
        self.tname = tname
        super().__init__(line)
    def read(fin, **kwargs):
        cname = Cool_Id.read(fin)
        return Expr_New(kwargs["line"], cname)

class Expr_Isvoid(Cool_expr):
    def typeCheck(self, env, inheritance):
        self.expr.typeCheck(env, inheritance)
        return "Bool"

    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        e = Cool_expr.read(fin)
        return Expr_Isvoid(kwargs["line"], e)

class Expr_Arith(Cool_expr):
    def typeCheck(self, env, inheritance):
        t1 = self.e1.typeCheck(env, inheritance)
        t2 = self.e2.typeCheck(env, inheritance)
        if (not t1 == "Int") or (not t2 == "Int"):
            raise Exception("%s %s in arith instead of ints" % (t1, t2))
        return "Int"

    def __init__(self, line, op, e1, e2):
        self.e1 = e1
        self.e2 = e2
        self.op = op
        super().__init__(line)
    def read(fin, **kwargs):
        e1 = Cool_expr.read(fin)
        e2 = Cool_expr.read(fin)
        return Expr_Arith(kwargs["line"], kwargs["ename"], e1, e2)

class Expr_Cmp(Cool_expr):

    def __init__(self, line, op, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.op  = op
        super().__init__(line)
    def read(fin, **kwargs):
        lhs = Cool_expr.read(fin)
        rhs = Cool_expr.read(fin)
        return Expr_Cmp(kwargs["line"], kwargs["ename"], lhs, rhs)

class Expr_Not(Cool_expr):
    def typeCheck(self, env, inheritance):
        t = self.expr.typeCheck(env, inheritance)
        if not t == "Bool":
            raise Exception("not applied to %s instead of Bool" % t)
        return "Bool"

    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        e = Cool_expr.read(fin)
        return Expr_Not(kwargs["line"], e)

class Expr_Negate(Cool_expr):
    def typeCheck(self, env, inheritance):
        t = self.expr.typeCheck(env, inheritance)
        if not t == "Int":
            raise Exception("negate applied to %s instead of Bool" % t)
        return "Int"

    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        e = Cool_expr.read(fin)
        return Expr_Negate(kwargs["line"], e)

class Expr_Integer(Cool_expr):
    def typeCheck(self, env, inheritance):
        return "Int"

    def __init__(self, line, int_value):
        self.int_value = int_value
        super().__init__(line)
    def read(fin, **kwargs):
        int_value = fin.readline()[:-1]
        return Expr_Integer(kwargs["line"], int_value)
    def __str__(self):
        return "int: " + self.int_value + "\n"

class Expr_String(Cool_expr):
    def typeCheck(self, env, inheritance):
        return "String"

    def __init__(self, line, str_value):
        self.str_value = str_value
        super().__init__(line)
    def read(fin, **kwargs):
        s = fin.readline()[:-1]
        return Expr_String(kwargs["line"], s)

class Expr_Id(Cool_expr):
    def typeCheck(self, env, inheritance):
        return env.typeof(self.cool_id)

    def __init__(self, line, cool_id):
        self.cool_id = cool_id
        super().__init__(line)
    def read(fin, **kwargs):
        i = Cool_Id.read(fin)
        return Expr_Id(kwargs["line"], i)

class Expr_Bool(Cool_expr):
    def typeCheck(self, env, inheritance):
        return "Bool"

    def __init__(self, line, bool_value):
        self.bool_value = bool_value
        super().__init__(line)
    def read(fin, **kwargs):
        return Expr_Bool(kwargs["line"], kwargs["ename"])

class Expr_Let(Cool_expr):


    class Binding():
        def __init__(self, name, btype, expr = None):
            self.name = name
            self.btype= btype
            self.expr = expr
        def read(fin):
            init = fin.readline()[:-1]
            name = Cool_Id.read(fin)
            btype= Cool_Id.read(fin)
            if init == "let_binding_no_init ":
                init = None
            elif init == "let_binding_init":
                init = Cool_expr.read(fin)
                # LET error line number
            return Expr_Let.Binding(name, btype, init)

    def __init__(self, line, bindings, body):
        self.bindings = bindings
        self.body = body
        super().__init__(line)
    def read(fin, **kwargs):
        bindings = read_lst(Expr_Let.Binding.read, fin)
        body     = Cool_expr.read(fin)
        return Expr_Let(kwargs["line"], bindings, body)

class Expr_Case(Cool_expr):
    class CaseElement(Cool_expr):
        def __init__(self, name, ctype, expr):
            self.name = name
            self.btype= btype
            self.expr = expr
        def read(fin):
            var     = Cool_Id.read(fin)
            vtype   = Cool_Id.read(fin)
            body    = Cool_expr.read(fin)
            return Expr_Case.Element(var, vtype, body)
    def __init__(self, line, expr, elements):
        self.expr = expr
        self.elements = elements
        super().__init__(line)
    def read(fin, **kwargs):
        expr     = Cool_expr.read(fin)
        elements = read_lst(Expr_Case.Element.read, fin)
        return Expr_Case(kwargs["line"], expr, elements)

class Expr_Internal(Cool_expr):
    def typeCheck(self, env, inheritance):
        return self.static_type.get_name()

    def __init__(self, static_type, details):
        self.details = details
        super().__init__(0, static_type = static_type)

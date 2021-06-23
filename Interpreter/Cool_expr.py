class Cool_Id():
    def read(fin):
        line = fin.readline()[:-1]
        name = fin.readline()[:-1]
        return Cool_Id(name, line)

    def __init__(self, name, line):
        self.name = name
        self.line = line

class Cool_expr():
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
        elif kwargs["ename"] == "eq":
            return Expr_Equal.read(fin, **kwargs)
        elif kwargs["ename"] in ["lt","le"]:
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

    def __init__(self, line):
        self.line   = line

    def tc(self, env):
        self.flush_types(env)
        return self.static_type

    def flush_types(self, env):
        self.static_type = self.typeCheck(env)
        return self.static_type

    def __str__(self):
        return "%s\n%s\n%s" % (self.line, self.static_type.static_str(), self.tostr())
    def tostr(self):
        raise Exception("TOSTR IS NOT OVERIDDEN IN CLASS: " + str(type(self)))

class Expr_Assign(Cool_expr):
    def __init__(self, line, var, expr):
        self.var = var
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        var = Cool_Id.read(fin)
        expr= Cool_expr.read(fin)
        return Expr_Assign(kwargs["line"], var, expr)
    def tostr(self):
        return "assign\n%s%s" % (self.var, self.expr)

class Expr_DDispatch(Cool_expr):
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
    def tostr(self):
        return "dynamic_dispatch\n%s%s%s" % (self.expr, self.method, elst_to_str(self.args))

class Expr_SDispatch(Cool_expr):
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
    def tostr(self):
        return "static_dispatch\n%s%s%s%s" % (self.expr, self.target, self.method, elst_to_str(self.args))

class Expr_SelfDispatch(Cool_expr):
    def __init__(self, line, method, args):
        self.method = method
        self.args = args
        super().__init__(line)
    def read(fin, **kwargs):
        m       = Cool_Id.read(fin)
        args    = read_lst(Cool_expr.read, fin)
        return Expr_SelfDispatch(kwargs["line"], m, args)
    def tostr(self):
        return "self_dispatch\n%s%s" % (self.method, elst_to_str(self.args))

class Expr_If(Cool_expr):
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
    def tostr(self):
        return "if\n%s%s%s" % (self.predicate, self.bt, self.bf)

class Expr_While(Cool_expr):
    def __init__(self, line, predicate, body):
        self.predicate = predicate
        self.body = body
        super().__init__(line)
    def read(fin, **kwargs):
        predicate = Cool_expr.read(fin)
        body      = Cool_expr.read(fin)
        return Expr_While(kwargs["line"], predicate, body)
    def tostr(self):
        return "while\n%s%s" % (self.predicate, self.body)


class Expr_Block(Cool_expr):
    def __init__(self, line, exprs):
        self.exprs = exprs
        super().__init__(line)
    def read(fin, **kwargs):
        exprs = read_lst(Cool_expr.read, fin)
        return Expr_Block(kwargs["line"], exprs)
    def tostr(self):
        return "block\n%s" % (elst_to_str(self.exprs))

class Expr_New(Cool_expr):
    def __init__(self, line, tname):
        self.tname = tname
        super().__init__(line)
    def read(fin, **kwargs):
        cname = Cool_Id.read(fin)
        return Expr_New(kwargs["line"], cname)
    def tostr(self):
        return "new\n%s" % (self.tname)

class Expr_Isvoid(Cool_expr):
    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        e = Cool_expr.read(fin)
        return Expr_Isvoid(kwargs["line"], e)
    def tostr(self):
        return "isvoid\n%s" % (self.expr)

class Expr_Arith(Cool_expr):
    def __init__(self, line, op, e1, e2):
        self.e1 = e1
        self.e2 = e2
        self.op = op
        super().__init__(line)
    def read(fin, **kwargs):
        e1 = Cool_expr.read(fin)
        e2 = Cool_expr.read(fin)
        return Expr_Arith(kwargs["line"], kwargs["ename"], e1, e2)
    def tostr(self):
        return "%s\n%s%s" % (self.op, self.e1, self.e2)

class Expr_Equal(Cool_expr):
    def __init__(self, line, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        super().__init__(line)
    def read(fin, **kwargs):
        lhs = Cool_expr.read(fin)
        rhs = Cool_expr.read(fin)
        return Expr_Equal(kwargs["line"], lhs, rhs)
    def tostr(self):
        return "eq\n%s%s" % (self.lhs, self.rhs)


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
    def tostr(self):
        return "%s\n%s%s" % (self.op, self.lhs, self.rhs)

class Expr_Not(Cool_expr):
    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        e = Cool_expr.read(fin)
        return Expr_Not(kwargs["line"], e)
    def tostr(self):
        return "not\n%s" % (self.expr)

class Expr_Negate(Cool_expr):
    def __init__(self, line, expr):
        self.expr = expr
        super().__init__(line)
    def read(fin, **kwargs):
        e = Cool_expr.read(fin)
        return Expr_Negate(kwargs["line"], e)
    def tostr(self):
        return "negate\n%s" % (self.expr)

class Expr_Integer(Cool_expr):
    def __init__(self, line, int_value):
        self.int_value = int_value
        super().__init__(line)
    def read(fin, **kwargs):
        int_value = fin.readline()[:-1]
        return Expr_Integer(kwargs["line"], int_value)
    def tostr(self):
        return "integer\n%s\n" % (self.int_value)

class Expr_String(Cool_expr):
    def __init__(self, line, str_value):
        self.str_value = str_value
        super().__init__(line)
    def read(fin, **kwargs):
        s = fin.readline()[:-1]
        return Expr_String(kwargs["line"], s)
    def tostr(self):
        return "string\n%s\n" % (self.str_value)

class Expr_Id(Cool_expr):
    def __init__(self, line, cool_id):
        self.cool_id = cool_id
        super().__init__(line)
    def read(fin, **kwargs):
        i = Cool_Id.read(fin)
        return Expr_Id(kwargs["line"], i)
    def tostr(self):
        return "identifier\n%s" % (self.cool_id)

class Expr_Bool(Cool_expr):
    def __init__(self, line, bool_value):
        self.bool_value = bool_value
        super().__init__(line)
    def read(fin, **kwargs):
        return Expr_Bool(kwargs["line"], kwargs["ename"])
    def tostr(self):
        return "%s\n" % (self.bool_value)

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
            if init == "let_binding_no_init":
                init = None
            elif init == "let_binding_init":
                init = Cool_expr.read(fin)
                # LET error line number
            return Expr_Let.Binding(name, btype, init)
        def get_name(self):
            return self.name.get_name()
        def get_type(self):
            return self.btype.get_name()
        def get_expr(self):
            return self.expr
        def __str__(self):
            if self.expr:
                return "let_binding_init\n%s%s%s" % (self.name, self.btype, self.expr)
            return "let_binding_no_init\n%s%s" % (self.name, self.btype)

    def __init__(self, line, bindings, body):
        self.bindings = bindings
        self.body = body
        super().__init__(line)
    def read(fin, **kwargs):
        bindings = read_lst(Expr_Let.Binding.read, fin)
        body     = Cool_expr.read(fin)
        return Expr_Let(kwargs["line"], bindings, body)
    def tostr(self):
        return "let\n%s%s" % (elst_to_str(self.bindings), self.body)

class Expr_Case(Cool_expr):
    class CaseElement(Cool_expr):
        def typeCheck(self, env):
            env = env.copy()
            vname = self.name.get_name()
            vtype = self.ctype.get_name()
            expr  = self.expr
            if vname == "self":
                error(  self.name.line,
                        "binding self in a case expression is not allowed")
            if vtype == "SELF_TYPE":
                error(  self.ctype.line,
                        "using SELF_TYPE as a case branch type is not allowed")
            env.add_var(vname, Cool_type(vtype))
            return expr.flush_types(env)
        def __init__(self, name, ctype, expr):
            self.name = name
            self.ctype= ctype
            self.expr = expr
        def read(fin):
            var     = Cool_Id.read(fin)
            vtype   = Cool_Id.read(fin)
            body    = Cool_expr.read(fin)
            return Expr_Case.CaseElement(var, vtype, body)
        def __str__(self):
            return "%s%s%s" % (self.name, self.ctype, self.expr)
    def __init__(self, line, expr, elements):
        self.expr = expr
        self.elements = elements
        super().__init__(line)
    def read(fin, **kwargs):
        expr     = Cool_expr.read(fin)
        elements = read_lst(Expr_Case.CaseElement.read, fin)
        return Expr_Case(kwargs["line"], expr, elements)
    def tostr(self):
        return "case\n%s%s" % (self.expr, elst_to_str(self.elements))

class Expr_Internal(Cool_expr):
    def __init__(self, stype, details):
        self.details = details
        self.stype = Cool_type(stype)
        super().__init__(0)
    def tostr(self):
        return "internal\n%s\n" % (self.details)

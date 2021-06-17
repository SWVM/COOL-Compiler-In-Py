from Helpers import *
from Cool_expr import *
# will have to pass typing enviroment as OJB


class Cool_prog():
    def __init__(self, fname):
        self.inheritance = Pedigree()
        self.classes = {}

        fin = open(fname, "r")
        cls = [OBJECT, STRING, INT, BOOL, IO] + read_lst(Cool_class.read, fin)
        for c in cls:
            self.add_class(c)


    def add_class(self, c):
        if c.get_name() in self.classes:
            error(  c.get_line(),
                    "class %s redifined" % (c.get_name()))
        if c.parent:
            self.inheritance.add_edge(c.parent.get_name(), c.get_name())
        self.classes[c.get_name()] = c
        c.set_prog(self)

    def tc_pre_check(self):
        cycle = self.inheritance.get_cycle()
        if cycle:
            error(  "0",
                    "inheritance cycle: %s" % (cycle))
        self.check_main()

    def tc_class_map(self):
        print("class_map")
        print(len(self.classes))
        for c in sorted(self.classes.keys()):
            self.classes[c].tc_attris(self.inheritance)

    def tc_imp_map(self):
        print("implementation_map")
        print(len(self.classes))
        for c in sorted(self.classes.keys()):
            self.classes[c].tc_methods(self.inheritance)

    def fetch_class(self, cname):
        try:
            return self.classes[cname.name]
        except:
            raise Exception("class not found: " + str(cname))

    def get_method_env(self):
        method_env = {}
        for c in self.classes.values():
            for m in c.get_methods().values():
                method_env[(c.get_name(), m.get_name())] = m
        return method_env

    def check_main(self):
        try:
            class_Main = self.classes["Main"]
        except:
            error(  "0",
                    "class Main not found")
        try:
            method_main= class_Main.get_methods()["main"]
        except:
            error(  "0",
                    "class Main method main not found")
        try:
            assert len(method_main.formals) == 0
        except:
            error(  "0",
                    "class Main method main with 0 parameters not found")


class Cool_class():
    DEFAULT_PARENT = Cool_Id("Object", "0")
    NON_INHERITABLE = ["Int", "Bool", "String"]

    def get_init_env(self, inheritance):
        return   Typing_env(o = self.get_init_obj_env(),
                            m = self.prog.get_method_env(),
                            c = Cool_type(self.get_name(), selftype = True),
                            inheritance = inheritance)

    def tc_methods(self, inheritance):
        methods = self.get_methods().values()
        env     = self.get_init_env(inheritance)
        print(self.name.get_name())
        print(len(methods))
        for m in methods:
            m.typeCheck(env)
            print(m)

    def tc_attris(self, inheritance):
        attris = self.get_attris().values()
        env     = self.get_init_env(inheritance)
        print(self.name.get_name())
        print(len(attris))
        for a in attris:
            a.typeCheck(env)
            print(a)

    # read a class from .cl-ast file
    def read(fin):
        cname   = Cool_Id.read(fin)
        inherit = fin.readline()[:-1]
        if inherit == "inherits":
            parent = Cool_Id.read(fin)
        else:
            parent = Cool_class.DEFAULT_PARENT
        features = read_lst(Cool_feature.read, fin, args=[cname])
        return Cool_class(cname, parent = parent, features = features)

    def __init__(self, name, parent = DEFAULT_PARENT, features = [], prog = None):
        if parent != None and parent.name in Cool_class.NON_INHERITABLE:
            error(  self.get_line(),
                    "class %s inherits from %s" % (self.name, self.parent.name))
        if name.get_name() == "SELF_TYPE":
            error(  self.get_line(),
                    "class named SELF_TYPE")

        self.name = name
        self.prog = prog
        self.parent = parent
        self.attributes = {}
        self.methods = {}
        for f in  features:
            if isinstance(f, Cool_method):
                self.add_method(f)
            elif isinstance(f, Cool_attri):
                self.add_attris(f)
        self.PulledFromParents = False

    def get_init_obj_env(self):
        o = {}
        o["self"] = Cool_type(self.get_name(), selftype = True)
        for a in self.get_attris().values():
            o[a.get_name()] = Cool_type(a.get_type())
        return o

    def set_prog(self, prog):
        self.prog = prog

    def get_name(self):
        return self.name.get_name()

    def get_line(self):
        return self.name.get_line()

    def add_attris(self, a):
        if a.get_name() == "self":
            error(  a.get_line(),
                    "class %s has an attribute named self" % (self.name))
        if a.get_name() in self.attributes:
            error(  a.get_line(),
                    "class %s redefines attribute %s" % (self.name, a.name))
        self.attributes[a.get_name()] = a

    def add_method(self, m):
        # will only be called by __init__
        # only throws error only when a method defined twice in the same class
        if m.get_name() in self.methods:
            error(  m.get_line(),
                    "class %s redefines method %s" % (self.name, m.name))
        self.methods[m.get_name()] = m

    def pull_from_parent(self):
        self.PulledFromParents = True
        if self.parent == None:
            return

        try:
            parent = self.prog.fetch_class(self.parent)
        except:
            error(  self.parent.get_line(),
                    "class %s inherits from unknown class %s" % (self.name, self.parent))

        inherited_m = parent.get_methods()
        for k in self.methods.keys():
            if k in inherited_m:
                self.methods[k].override_check(inherited_m[k])
                inherited_m.pop(k)   # pop then insert to maintain the order
            inherited_m[k] = self.methods[k]
        self.methods = inherited_m

        inherited_attris  = parent.get_attris()
        for k in self.attributes.keys():
            if k in inherited_attris:
                error(  self.attributes[k].get_line(),
                        "class %s redefines attribute %s"
                        % (self.name, k))
            inherited_attris[k] = self.attributes[k]
        self.attributes = inherited_attris

    def get_methods(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return copy(self.methods)
    def get_attris(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return copy(self.attributes)


class Cool_feature():
    def read(fin, owner):
        ftype = fin.readline()[:-1]
        if ftype == "method":
            name    = Cool_Id.read(fin)
            formals = []
            count   = int(fin.readline())
            for i in range(count):
                formals.append(Cool_formal.read(fin))
            declared_type = Cool_Id.read(fin)
            expr = Cool_expr.read(fin)
            f = Cool_method(name, formals, declared_type, expr, owner)
        elif ftype == "attribute_init":
            name = Cool_Id.read(fin)
            atype = Cool_Id.read(fin)
            expr = Cool_expr.read(fin)
            f =  Cool_attri(name, atype, owner, expr)
        elif ftype == "attribute_no_init":
            name = Cool_Id.read(fin)
            atype = Cool_Id.read(fin)
            f =  Cool_attri(name, atype, owner)
        return f

    def __init__(self, name, declared_type, owner):
        self.name = name
        self.declared_type = declared_type
        self.owner = owner

    def typeCheck(self, env):
        raise Exception("to be override")
    def get_name(self):
        return  self.name.get_name()
    def get_line(self):
        return self.name.get_line()
    def get_type(self):
        return self.declared_type.get_name()


class Cool_attri(Cool_feature):
    def typeCheck(self, env):
        declared_type = Cool_type(self.declared_type.get_name())
        if declared_type == "SELF_TYPE":
            declared_type = env.get_selftype()
        if not env.has_type(declared_type):
            error(  self.declared_type.get_line(),
                    "class %s has attribute %s with unknown type %s"
                    % (self.owner, self.name, declared_type))

        if self.init_expr:
            init_type = self.init_expr.tc(env)
            if not env.is_parent_child(declared_type, init_type):
                error(  self.get_line(),
                        "%s does not conform to %s in initialized attribute"
                        % (init_type, declared_type))
        return declared_type

    def __init__(self, name, declared_type, owner, init_expr = None):
        self.init_expr = init_expr
        super().__init__(name, declared_type, owner)
    def __str__(self):
        if self.init_expr:
            return "initializer\n%s\n%s\n%s" % (self.name.get_name(), self.declared_type.get_name(), self.init_expr)
        return "no_initializer\n%s\n%s" % (self.name.get_name(), self.declared_type.get_name())



class Cool_method(Cool_feature):
    def typeCheck(self, env):
        # TODO: WHERE YOU LEFT
        env = env.copy()
        formal_vars = {}
        for f in self.formals:
            fname = f.get_name()
            ftype = Cool_type(f.get_type())
            if fname == "self":
                error(  f.get_line(),
                        "class %s has method %s with formal parameter named self"
                        % (self.owner, self.name))
            if not env.has_type(ftype):
                error(  f.declared_type.get_line(),
                        "class %s has method %s with formal parameter of unknown type %s"
                        % (self.owner, self.name, f.get_type()))
            if fname in formal_vars:
                error(  f.get_line(),
                        "class %s has method %s with duplicate formal parameter named %s"
                        % (self.owner, self.name, f.name))
            formal_vars[fname] = ftype
        env.add_vars(formal_vars)
        rtype = Cool_type(self.declared_type.get_name())
        if rtype == "SELF_TYPE":
            rtype = env.get_selftype()
        if not env.has_type(rtype):
            error(  self.declared_type.get_line(),
                    "class %s has method %s with unknown return type %s"
                    % (self.owner, self.name, rtype))
        expr_type     = self.body_expr.tc(env)
        if not env.is_parent_child(rtype, expr_type):
            error(  self.get_line(),
                    "%s does not conform to %s in method %s"
                    % (expr_type, rtype, self.name))
        return rtype

    def __init__(self, name, formals, declared_type, body_expr, owner):
        self.formals = formals
        self.declared_type = declared_type
        self.signiture = list(map(lambda x: Cool_type(x.get_type()), self.formals))
        self.return_type   = Cool_type(declared_type.get_name())
        self.body_expr = body_expr
        super().__init__(name, declared_type, owner)

    def override_check(self, pm):
        sfs = self.get_formals()
        pfs = pm.get_formals()
        if len(sfs) != len(pfs):
            error(  self.get_line(),
                    "class %s redefines method %s and changes number of formals"
                    % (self.owner, self.name))
        if self.return_type != pm.return_type:
            error(  self.declared_type.get_line(),
                    "class %s redefines method %s and changes return type (from %s to %s)"
                    % (self.owner, self.name, pm.return_type, self.return_type))
        for i in range(len(sfs)):
            if sfs[i].get_type() != pfs[i].get_type:
                error(  sfs[i].get_line(),
                        "class %s redefines method %s and changes type of formal %s"
                        % (self.owner, self.get_name(), sfs[i].get_name()))


    def get_sig_lines(self):
        return list(map(lambda x: x.get_line(), self.formals))
    def get_ret_line(self):
        return self.declared_type.get_line()

    def get_formals(self):
        return self.formals

    def get_name(self):
        return self.name.get_name()
    def get_line(self):
        return self.name.get_line()
    def __str__(self):
        return "%s%s%s%s" % (self.name, elst_to_str(self.formals), self.owner, self.body_expr)


class Cool_formal():
    def read(fin):
        name = Cool_Id.read(fin)
        declared_type = Cool_Id.read(fin)
        return Cool_formal(name, declared_type)

    def __init__(self, name, declared_type):
        self.name = name
        self.declared_type = declared_type
    def get_type(self):
        return self.declared_type.get_name()
    def get_name(self):
        return self.name.get_name()
    def get_line(self):
        return self.declared_type.get_line()
    def __str__(self):
        return "%s" % (self.name)



M_abort = Cool_method(  Cool_Id("abort","0"),
                        [],
                        Cool_Id("Object","0"),
                        Expr_Internal(  "Object",
                                        "Object.abort"),
                        "Object"
)
M_copy = Cool_method(  Cool_Id("copy","0"),
                        [],
                        Cool_Id("SELF_TYPE","0"),
                        Expr_Internal(  "SELF_TYPE",
                                        "Object.copy"),
                        "Object"
)
M_type_name = Cool_method(  Cool_Id("type_name","0"),
                        [],
                        Cool_Id("String","0"),
                        Expr_Internal(  "String",
                                        "Object.type_name"),
                        "Object"
)
OBJECT = Cool_class( Cool_Id("Object","0"), parent = None,   features = [M_abort ,M_copy, M_type_name] )

M_out_string = Cool_method(  Cool_Id("out_string","0"),
                             [
                                Cool_formal( Cool_Id("x", "0"), Cool_Id("String", "0"))
                             ],
                             Cool_Id("SELF_TYPE","0"),
                             Expr_Internal(  "SELF_TYPE",
                                            "IO.out_string"),
                            "IO"
)
M_out_int    = Cool_method(  Cool_Id("out_int","0"),
                             [
                                Cool_formal( Cool_Id("x", "0"), Cool_Id("Int", "0"))
                             ],
                             Cool_Id("SELF_TYPE","0"),
                             Expr_Internal(  "SELF_TYPE",
                                            "IO.out_int"),
                            "IO"
)
M_in_string  = Cool_method(  Cool_Id("in_string","0"),
                             [],
                             Cool_Id("String","0"),
                             Expr_Internal(  "String",
                                            "IO.in_string"),
                            "IO"
)
M_in_int     = Cool_method(  Cool_Id("in_int","0"),
                             [],
                             Cool_Id("Int","0"),
                             Expr_Internal(  "Int",
                                            "IO.in_int"),
                            "IO"
)
IO = Cool_class(    Cool_Id("IO","0"),
                    features=[M_out_string, M_out_int, M_in_string, M_in_int]
                )

INT = Cool_class(   Cool_Id("Int","0"),
                    features=[]
                )

M_length    = Cool_method(  Cool_Id("length","0"),
                             [],
                             Cool_Id("Int","0"),
                             Expr_Internal(  "Int",
                                            "String.length"),
                            "String"
)
M_concat    = Cool_method(  Cool_Id("concat","0"),
                             [
                                Cool_formal( Cool_Id("s", "0"), Cool_Id("String", "0"))
                             ],
                             Cool_Id("String","0"),
                             Expr_Internal(  "String",
                                            "String.concat"),
                            "String"
)
M_substr    = Cool_method(  Cool_Id("substr","0"),
                             [
                                Cool_formal( Cool_Id("i", "0"), Cool_Id("Int", "0")),
                                Cool_formal( Cool_Id("l", "0"), Cool_Id("Int", "0"))
                             ],
                             Cool_Id("String","0"),
                             Expr_Internal(  "String",
                                            "String.substr"),
                            "String"
)
STRING = Cool_class(    Cool_Id("String","0"),
                        features=[M_length, M_concat, M_substr]
                    )

BOOL = Cool_class(      Cool_Id("Bool","0"),
                        features=[]
                    )

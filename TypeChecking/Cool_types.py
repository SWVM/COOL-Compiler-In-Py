from Helpers import *
from Cool_expr import *
from io import StringIO
# will have to pass typing enviroment as OJB


class Cool_prog():
    ###
    # initializer and helper codes
    ###
    def __init__(self, fname):
        self.inheritance = Pedigree()
        self.classes = {}

        fin = open(fname, "r")
        self.user_cls = read_lst(Cool_class.read, fin)
        cls = [OBJECT, STRING, INT, BOOL, IO] + self.user_cls
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

    ###
    # TypeCheckings
    ###
    def tc_pre_check(self):
        cycle = self.inheritance.get_cycle()
        if cycle:
            error(  "0",
                    "inheritance cycle: %s" % (cycle))
        self.check_main()

    def tc_class_map(self):
        buffer = StringIO()
        buffer.write("class_map\n")
        buffer.write( "%d\n" % len(self.classes) )
        for c in sorted(self.classes.keys()):
            s = self.classes[c].tc_attris(self.inheritance)
            buffer.write(s)
        return buffer.getvalue()

    def tc_imp_map(self):
        buffer = StringIO()
        buffer.write("implementation_map\n")
        buffer.write( "%d\n" % len(self.classes) )
        for c in sorted(self.classes.keys()):
            s = self.classes[c].tc_methods(self.inheritance)
            buffer.write(s)
        return buffer.getvalue()

    def tc_parent_map(self):
        buffer = StringIO()
        buffer.write("parent_map\n")
        buffer.write( "%d\n" % (len(self.classes)-1) )
        for c in sorted(self.classes.keys()):
            cl = self.classes[c]
            if cl.parent:
                buffer.write("%s\n%s\n"  % (cl.get_name(), cl.parent.get_name()) )
        return buffer.getvalue()

    def annotated_AST(self):
        buffer = StringIO()
        buffer.write( "%d\n" % (len(self.user_cls)) )
        for c in self.user_cls:
            buffer.write( c.annotated_AST() )
        return buffer.getvalue()


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
    ###
    # Constants
    ###
    DEFAULT_PARENT = Cool_Id("Object", "0")
    NON_INHERITABLE = ["Int", "Bool", "String"]

    ###
    # initializer and helper
    ###
    def __init__(self, name, parent = DEFAULT_PARENT, features = [], prog = None, usr_inherit = None):
        self.name = name
        self.prog = prog
        self.parent = parent
        self.usr_inherit = usr_inherit
        self.features = features
        self.attributes = {}
        self.methods = {}
        for f in  features:
            if isinstance(f, Cool_method):
                self.add_method(f)
            elif isinstance(f, Cool_attri):
                self.add_attris(f)
        self.PulledFromParents = False

    def annotated_AST(self):
        if self.usr_inherit == "inherits":
            return "%s%s\n%s%s" % (self.name, self.usr_inherit, self.parent, lst_to_str(Cool_feature.annotated_AST, self.features))
        elif self.usr_inherit == "no_inherits":
            return "%s%s\n%s" % (self.name, self.usr_inherit, lst_to_str(Cool_feature.annotated_AST, self.features))

    def read(fin):
        cname   = Cool_Id.read(fin)
        inherit = fin.readline()[:-1]

        if inherit == "inherits":
            parent = Cool_Id.read(fin)
        else:
            parent = Cool_class.DEFAULT_PARENT

        if cname.get_name() == "SELF_TYPE":
            error(  cname.get_line(),
                    "class named SELF_TYPE")
        if parent != None and parent.name in Cool_class.NON_INHERITABLE:
            error(  parent.get_line(),
                    "class %s inherits from %s" % (cname.get_name(), parent.get_name()))

        features = read_lst(Cool_feature.read, fin, args=[cname.get_name()])
        return Cool_class(cname, parent = parent, features = features, usr_inherit = inherit)

    def pull_from_parent(self):
        self.PulledFromParents = True
        if self.parent == None:
            return
        try:
            parent = self.prog.fetch_class(self.parent)
        except:
            error(  self.parent.get_line(),
                    "class %s inherits from unknown class %s" % (self.get_name(), self.parent.get_name()))

        inherited_m = parent.get_methods()
        for k in self.methods.keys():
            if k in inherited_m:
                self.methods[k].override_check(inherited_m[k])
            inherited_m[k] = self.methods[k]
        self.methods = inherited_m

        temp = self.attributes
        self.attributes = parent.get_attris()
        for a in temp.values():
            self.add_attris(a)
        # inherited_attris  = parent.get_attris()
        # for k in self.attributes.keys():
        #     if k in inherited_attris:
        #         print("loc B")
        #         error(  self.attributes[k].get_line(),
        #                 "class %s redefines attribute %s"
        #                 % (self.name, k))
        #     inherited_attris[k] = self.attributes[k]
        # self.attributes = inherited_attris

    ###
    # getter and setters
    ###
    def get_methods(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return copy(self.methods)
    def get_attris(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return copy(self.attributes)
    def set_prog(self, prog):
        self.prog = prog
    def get_name(self):
        return self.name.get_name()
    def get_line(self):
        return self.name.get_line()
    def add_attris(self, a):
        if a.get_name() in self.attributes:
            error(  a.get_line(),
                    "class %s redefines attribute %s" % (self.get_name(), a.get_name()))
        self.attributes[a.get_name()] = a
    def add_method(self, m):
        if m.get_name() in self.methods:
            error(  m.get_line(),
                    "class %s redefines method %s" % (self.get_name(), m.get_name()))
        self.methods[m.get_name()] = m


    ###
    # TC methods
    ###
    def tc_methods(self, inheritance):
        buffer = StringIO()
        methods = self.get_methods().values()
        env     = self.get_init_env(inheritance)
        buffer.write("%s\n" % (self.name.get_name()))
        buffer.write("%d\n" % len(methods) )
        for m in methods:
            buffer.write(m.get_ast(env))
        return buffer.getvalue()

    def tc_attris(self, inheritance):
        buffer = StringIO()
        attris = self.get_attris().values()
        env     = self.get_init_env(inheritance)
        buffer.write("%s\n" % (self.name.get_name()))
        buffer.write("%d\n" % len(attris) )
        for a in attris:
            buffer.write(a.get_ast(env))
        return buffer.getvalue()

    def get_init_obj_env(self):
        o = {}
        o["self"] = Cool_type(self.get_name(), selftype = True)
        for a in self.get_attris().values():
            o[a.get_name()] = Cool_type(a.get_type())
        return o

    def get_init_env(self, inheritance):
        return   Typing_env(o = self.get_init_obj_env(),
                            m = self.prog.get_method_env(),
                            c = Cool_type(self.get_name(), selftype = True),
                            inheritance = inheritance)



class Cool_feature():
    def __init__(self, name, declared_type, owner):
        self.name = name
        self.declared_type = declared_type
        self.owner = owner
        self.ast = None
    def __str__(self):
        return self.ast
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
        else:
            name = Cool_Id.read(fin)
            atype = Cool_Id.read(fin)
            if name.get_name() == "self":
                error(  name.get_line(),
                        "class %s has an attribute named self" % (owner.get_name()))
            if ftype == "attribute_init":
                expr = Cool_expr.read(fin)
                f = Cool_attri(name, atype, owner, expr)
            elif ftype == "attribute_no_init":
                f = Cool_attri(name, atype, owner)
        return f

    def get_ast(self, env):
        if not self.ast:
            self.tc_feature(env)
        return self.ast
    def tc_feature(self, env):
        self.typeCheck(env)
        self.ast = str(self)
    def typeCheck(self, env):
        raise Exception("to be override")
    def get_name(self):
        return  self.name.get_name()
    def get_line(self):
        return self.name.get_line()
    def get_type(self):
        return self.declared_type.get_name()
    def annotated_AST(self):
        return self.annotated_AST()


class Cool_attri(Cool_feature):
    def __init__(self, name, declared_type, owner, init_expr = None):
        self.init_expr = init_expr
        super().__init__(name, declared_type, owner)

    def __str__(self):
        if self.init_expr:
            return "initializer\n%s\n%s\n%s\n" % (self.name.get_name(), self.declared_type.get_name(), self.init_expr)
        return "no_initializer\n%s\n%s\n" % (self.name.get_name(), self.declared_type.get_name())

    def annotated_AST(self):
        if self.init_expr:
            return "attribute_init\n%s%s%s" % (self.name, self.declared_type, self.init_expr)
        return "attribute_no_init\n%s%s" % (self.name, self.declared_type)

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


class Cool_method(Cool_feature):
    def __init__(self, name, formals, declared_type, body_expr, owner):
        self.formals = formals
        self.declared_type = declared_type
        self.signiture = list(map(lambda x: Cool_type(x.get_type()), self.formals))
        self.return_type   = Cool_type(declared_type.get_name())
        self.body_expr = body_expr
        super().__init__(name, declared_type, owner)
    def __str__(self):
        return "%s\n%s%s\n%s" % (self.get_name(), elst_to_str(self.formals), self.owner, self.body_expr)
    def annotated_AST(self):
        return "method\n%s%s%s%s" % (self.name, lst_to_str(Cool_formal.annotated_AST ,self.formals), self.declared_type, self.body_expr)
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

    def typeCheck(self, env):
        env = env.copy()
        formal_vars = {}
        for f in self.formals:
            fname = f.get_name()
            ftype = Cool_type(f.get_type())
            if fname == "self":
                error(  f.get_line(),
                        "class %s has method %s with formal parameter named self"
                        % (self.owner.get_name(), self.name.get_name()))
            if not env.has_type(ftype):
                error(  f.declared_type.get_line(),
                        "class %s has method %s with formal parameter of unknown type %s"
                        % (self.owner.get_name(), self.name.get_name(), f.get_type()))
            if fname in formal_vars:
                error(  f.get_line(),
                        "class %s has method %s with duplicate formal parameter named %s"
                        % (self.owner.get_name(), self.get_name(), f.get_name()))
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
                        % (self.owner.get_name(), self.get_name(), sfs[i].get_name()))


class Cool_formal():
    def __init__(self, name, declared_type):
        self.name = name
        self.declared_type = declared_type
    def __str__(self):
        return "%s\n" % (self.get_name())
    def annotated_AST(self):
        return "%s%s" % (self.name, self.declared_type)
    def read(fin):
        name = Cool_Id.read(fin)
        declared_type = Cool_Id.read(fin)
        return Cool_formal(name, declared_type)
    def get_type(self):
        return self.declared_type.get_name()
    def get_name(self):
        return self.name.get_name()
    def get_line(self):
        return self.declared_type.get_line()




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
                    features=[M_in_int, M_in_string, M_out_int, M_out_string]
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
                        features=[M_concat, M_length, M_substr]
                    )

BOOL = Cool_class(      Cool_Id("Bool","0"),
                        features=[]
                    )

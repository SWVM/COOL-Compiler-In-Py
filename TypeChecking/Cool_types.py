from Helpers import *
from Cool_expr import *
# will have to pass typing enviroment as OJB


class Cool_prog():
    def __init__(self, fname):
        fin = open(fname, "r")
        self.inheritance = Pedigree()
        self.classes = {}
        cls = [OBJECT, STRING, INT, BOOL, IO] + read_lst(Cool_class.read, fin)

        for c in cls:
            self.add_class(c)


    def add_class(self, c):
        if c.get_name() in self.classes:
            raise Exception("redefinition of class: " + name.name)
        if c.parent: self.inheritance.add_edge(c.parent.get_name(), c.get_name())
        self.classes[c.get_name()] = c
        c.set_prog(self)

    def fetch_class(self, cname):
        try:
            return self.classes[cname.name]
        except:
            raise Exception("class not found: " + str(cname))

    def typeCheck(self):
        cycle = self.inheritance.get_cycle()
        if cycle:
            raise Exception("inheritance cycle: "+ str(cycle))

        for c in self.classes.values():
            c.typeCheck()

    def get_method_env(self):
        m = {}
        for c in self.classes.values():
            for m in c.get_methods():
                m[(c.get_name(), m.get_name())] = m
        return m


    def check_main(self):
        try:
            class_Main = self.classes["Main"]
        except:
            raise Exception("ERROR: 0: Type-Check: class Main not found")
        try:
            method_main= class_Main.get_methods["main"]
        except:
            raise Exception("ERROR: 0: Type-Check: class Main method main not found")
        try:
            assert len(method_main.formals) == 0
        except:
            raise Exception("ERROR: 0: Type-Check: class Main method main with 0 parameters not found")


class Cool_class():
    DEFAULT_PARENT = Cool_Id("Object", "0")
    NON_INHERITABLE = ["Int", "Bool", "String"]

    def typeCheck(self):
        # care about yourself
        attris = self.get_attris()
        methods = self.get_methods()
        env = Typing_env(   o = self.get_init_obj_env(),
                            m = self.prog.get_method_env(),
                            c = self.get_name())
        for a in attris:
            a.typeCheck(env)
        for m in methods:
            m.typeCheck(env)
        # TODO: handle the rest





        raise Exception("not yet")

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
            raise Exception("inherits from forbidden class" + parent.name)
        if name.get_name() == "SELF_TYPE":
            raise Exception("class named SELF_TYPE")

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
        ## TODO: get attris, without initalizer.
        o = {}
        o = []
        for a in self.get_attris():
            o[a.get_name()] = a.get_type()
        return o

    def set_prog(self, prog):
        self.prog = prog

    def get_name(self):
        return self.name.get_name()

    def add_attris(self, a):
        if a.get_name() == self:
            raise Exception("xx has attri named self")
        if a.get_name() in self.attributes:
            raise Exception("redefinition of attribute: " + a.name)
        self.attributes[a.get_name()] = a

    def add_method(self, m):
        # will only be called by __init__
        # only throws error only when a method defined twice in the same class
        if m.get_name() in self.methods:
            raise Exception("redefinition of method: " + m.get_name())
        self.methods[m.get_name()] = m

    def pull_from_parent(self):
        self.PulledFromParents = True
        if self.parent == None:
            return

        parent = self.prog.fetch_class(self.parent)

        inherited_m = parent.get_methods()
        for k in self.methods.keys():
            if k in inherited_m:
                if inherited_m[k].signiture   !=  self.methods[k].signiture:
                    raise Exception("override parent method but change signiture")
                if inherited_m[k].return_type !=  self.methods[k].return_type:
                    raise Exception("override parent method but change return type")
                inherited_m.pop(k)   # pop then insert to maintain the order
            inherited_m[k] = self.methods[k]
        self.methods = inherited_m

        inherited_attris  = parent.get_attris()
        for k in self.attributes.keys():
            if k in inherited_attris:
                raise Exception("redefinition of attribute: " + k)
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

    def __str__(self):
        return "=======\nclass: %s\nPARENT: %s\n ATTRI: \n%s\nMETHODS: %s\n=======" % (self.name, "self.parent.name", self.attributes, self.methods)


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
            f =  Cool_attri(name, atype, expr)
        elif ftype == "attribute_no_init":
            name = Cool_Id.read(fin)
            atype = Cool_Id.read(fin)
            f =  Cool_attri(name, atype)
        else:
            raise Exception("unknown feature: " + ftype)
        return f

    def __init__(self, name, declared_type):
        self.name = name
        self.declared_type = declared_type

    def get_name(self):
        return  self.name.get_name()
    def get_type(self):
        return self.declared_type.get_name()


class Cool_attri(Cool_feature):
    def __init__(self, name, declared_type, init_expr = None):
        self.init_expr = init_expr
        super().__init__(name, declared_type)
    def __str__(self):
        if self.init_expr:
            return "ATTRI_INIT: "+str(self.name.name) + str(self.declared_type.name) + str(self.init_expr) +"\n"
        return "ATTRI_NO_INIT: "+str(self.name.name) + str(self.declared_type.name) + "\n"
    def __repr__(self):
        return self.__str__()



class Cool_method(Cool_feature):
    def __init__(self, name, formals, declared_type, body_expr, owner = None):
        self.formals = formals
        self.declared_type = declared_type
        self.signiture = list(map(lambda x: x.get_type(), self.formals))
        self.return_type   = declared_type.get_name()
        self.body_expr = body_expr
        self.owner = owner
        super().__init__(name, declared_type)

    def get_name(self):
        return self.name.get_name()
    def __str__(self):
        return "METHOD: "+str(self.name) + str(self.declared_type) + str(self.formals)+str(self.body_expr) + str(self.owner)
    def __repr__(self):
        return self.__str__()


class Cool_formal():
    def read(fin):
        name = Cool_Id.read(fin)
        declared_type = Cool_Id.read(fin)
        return Cool_formal(name, declared_type)

    def __init__(self, name, declared_type):
        self.name = name
        self.declared_type = declared_type
    def __str__(self):
        return "FORMALS: "+str(self.name) + str(self.declared_type)
    def __repr__(self):
        return self.__str__()

    def get_type(self):
        return self.declared_type.get_name()
    def get_name(self):
        return self.name.get_name()



M_abort = Cool_method(  Cool_Id("abort","0"),
                        [],
                        Cool_Id("Object","0"),
                        Expr_Internal(  Cool_Id("Object",0),
                                        "Object.abort")
)
M_copy = Cool_method(  Cool_Id("copy","0"),
                        [],
                        Cool_Id("SELF_TYPE","0"),
                        Expr_Internal(  Cool_Id("SELF_TYPE",0),
                                        "Object.copy")
)
M_type_name = Cool_method(  Cool_Id("type_name","0"),
                        [],
                        Cool_Id("String","0"),
                        Expr_Internal(  Cool_Id("String",0),
                                        "Object.type_name")
)
OBJECT = Cool_class( Cool_Id("Object","0"), parent = None,   features = [M_abort ,M_copy, M_type_name] )

M_out_string = Cool_method(  Cool_Id("out_string","0"),
                             [
                                Cool_formal( Cool_Id("x", "0"), Cool_Id("String", "0"))
                             ],
                             Cool_Id("SELF_TYPE","0"),
                             Expr_Internal(  Cool_Id("SELF_TYPE",0),
                                            "IO.out_string")
)
M_out_int    = Cool_method(  Cool_Id("out_int","0"),
                             [
                                Cool_formal( Cool_Id("x", "0"), Cool_Id("Int", "0"))
                             ],
                             Cool_Id("SELF_TYPE","0"),
                             Expr_Internal(  Cool_Id("SELF_TYPE",0),
                                            "IO.out_int")
)
M_in_string  = Cool_method(  Cool_Id("in_string","0"),
                             [],
                             Cool_Id("String","0"),
                             Expr_Internal(  Cool_Id("String",0),
                                            "IO.in_string")
)
M_in_int     = Cool_method(  Cool_Id("in_int","0"),
                             [],
                             Cool_Id("Int","0"),
                             Expr_Internal(  Cool_Id("Int",0),
                                            "IO.in_int")
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
                             Expr_Internal(  Cool_Id("Int",0),
                                            "String.length")
)
M_concat    = Cool_method(  Cool_Id("concat","0"),
                             [
                                Cool_formal( Cool_Id("s", "0"), Cool_Id("String", "0"))
                             ],
                             Cool_Id("String","0"),
                             Expr_Internal(  Cool_Id("String",0),
                                            "String.concat")
)
M_substr    = Cool_method(  Cool_Id("substr","0"),
                             [
                                Cool_formal( Cool_Id("i", "0"), Cool_Id("Int", "0")),
                                Cool_formal( Cool_Id("l", "0"), Cool_Id("Int", "0"))
                             ],
                             Cool_Id("String","0"),
                             Expr_Internal(  Cool_Id("String",0),
                                            "String.substr")
)
STRING = Cool_class(    Cool_Id("String","0"),
                        features=[M_length, M_concat, M_substr]
                    )

BOOL = Cool_class(      Cool_Id("Bool","0"),
                        features=[]
                    )

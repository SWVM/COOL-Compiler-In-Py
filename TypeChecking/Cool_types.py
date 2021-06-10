from copy import deepcopy, copy
from Helpers import *
from Cool_expr import *
# will have to pass typing enviroment as OJB


class Cool_class():
    ID_OBJECT = Cool_Id("Object", "0")
    NON_INHERITALE = ["Int", "Bool", "String"]
    classes = {} # hash map that holds all classes


    def check_main():
        try:
            class_Main = classes["Main"]
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


    def fetch_class(cname):
        print(type(cname))
        try:
            return Cool_class.classes[cname.name]
        except:
            raise Exception("class not found: " + str(cname))


    # read a class from .cl-ast file
    def read(fin):
        cname   = Cool_Id.read(fin)
        inherit = fin.readline()[:-1]
        if inherit == "inherits":
            parent = Cool_Id.read(fin)
        else:
            parent = Cool_class.ID_OBJECT
        features = read_lst(Cool_feature.read, fin, args=[cname])
        return Cool_class(cname, parent, features)


    def __init__(self, name, parent = ID_OBJECT, features = []):
        if name.name in Cool_class.classes:
            raise Exception("redefinition of class: " + name.name)
        if (parent != None and parent.name) in Cool_class.NON_INHERITALE:
            raise Exception("inherits from forbidden class" + parent.name)

        self.name = name
        self.parent = parent
        self.attributes = {}
        self.methods = {}
        for f in  features:
            if isinstance(f, Cool_method):
                self.add_method(f)
            elif isinstance(f, Cool_attri):
                self.add_attris(f)
        self.PulledFromParents = False
        Cool_class.classes[name.name] = self

    def add_attris(self, a):
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

        parent = Cool_class.fetch_class(self.parent)

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
        return  self.name.name
    def get_type(self):
        return self.declared_type.name

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
        self.return_type   = declared_type.get_name
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

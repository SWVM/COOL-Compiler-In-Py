from copy import deepcopy, copy
from Helpers import *
from Cool_expr import *

# will have to pass typing enviroment as OJB
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



class Cool_class():
    ID_OBJECT = Cool_Id("Object", "0")
    # TODO: BASES CLASSES
    classes = {} # hash map that holds all classes
    def fetch_class(cname):
        try:
            return Cool_class.classes[cname.name]
        except:
            raise Exception("class not found: " + str(cname))

    def update_parent_mapping():
        for cl in Cool_class.classes.values():
            if isinstance(cl.parent, Cool_Id):
                cl.parent = Cool_class.fetch_class(cl.parent)

    def read(fin):
        cname   = Cool_Id.read(fin)
        inherit = fin.readline()[:-1]
        if inherit == "inherits":
            parent = Cool_Id.read(fin)
        else:
            parent = Cool_class.ID_OBJECT
        features = read_lst(Cool_feature.read, fin, args=[cname])
        return Cool_class(cname, parent, features)

    # name, parent, methods, attributes
    def __init__(self, name, parent, features = []):
        if name.name in Cool_class.classes:
            raise Exception("redefinition of class: " + name.name)
        self.name = name
        self.parent = parent
        self.attributes = {}
        self.methods = {}
        for f in  features:
            if isinstance(f, Cool_method):
                self.add_method(f)
            elif isinstance(f, Cool_attri):
                self.add_attris(f)

        Cool_class.classes[name.name] = self
        self.PulledFromParents = False

    def add_attris(self, a):
        if a.name in self.attributes:
            raise Exception("redefinition of attribute: " + a.name)
        self.attributes[a.name] = a
    def add_method(self, m):
        if m.name in self.methods:
            raise Exception("redefinition of method: " + m.name)
        self.methods[m.name] = m
    def pull_from_parent(self):
        if self.PulledFromParents or self.parent == None:
            return
        inherited_methods = self.parent.get_methods()
        for k in self.methods.keys():
            if k in inherited_methods:
                if not inherited_methods[k].get_signiture() == self.methods[k].get_signiture():
                    raise Exception("override parent method but change signiture")
                inherited_methods.pop(k)   # pop then insert to maintain the order
            inherited_methods[k] = self.methods[k]
        self.methods = inherited_methods

        inherited_attris  = self.parent.get_attris()
        for k in self.attributes.keys():
            if k in inherited_attris:
                raise Exception("redefinition of attribute: " + k.name)
            inherited_attris[k] = self.attributes[k]
        self.attributes = inherited_attris

        self.PulledFromParents = True
    def get_methods(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return copy(self.methods)
    def get_attris(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return copy(self.attributes)

    def __str__(self):
        return "class: %s\n\tparent: %s\n \tattributes: \n%s\n" % (self.name, self.parent.name, self.attributes)


class Cool_feature():
    def read(fin, owner):
        ftype = fin.readline()[:-1]
        if ftype == "method":
            name    = read(fin)
            formals = []
            count   = int(fin.readline())
            for i in range(count):
                formals.append(Cool_formal.read(fin))
            declared_type = read(fin)
            expr = Cool_expr.read()
            f = Cool_method(name, formals, declared_type, expr, owner)
        elif ftype == "attribute_init":
            name = Cool_Id.read(fin)
            type = Cool_Id.read(fin)
            expr = Cool_expr.read(fin)
            f =  Cool_attri(name, type, expr)
        elif ftype == "attribute_no_init":
            name = Cool_Id.read(fin)
            type = Cool_Id.read(fin)
            f =  Cool_attri(name, type)
        else:
            raise Exception("unknown feature: " + ftype)
        return f

    def __init__(self, name, declared_type):
        self.name = name
        self.declared_type = declared_type

class Cool_attri(Cool_feature):
    def __init__(self, name, declared_type, init_expr = None):
        self.init_expr = init_expr
        super().__init__(name, declared_type)
    def __str__(self):
        return str(self.name) + str(self.declared_type)
    def __repr__(self):
        return self.__str__()

class Cool_method(Cool_feature):
    def __init__(self, name, formals, declared_type, body_expr, owner = None):
        self.formals = formals
        self.declared_type = declared_type
        self.body_expr = body_expr
        self.owner = owner
        super.__init__(name, declared_type)

class Cool_formal():
    def __init__(self, name, declared_type):
        self.name = name
        self.declared_type = declared_type
    def read(fin):
        name = read(fin)
        declared_type = read(fin)
        return Cool_formal(name, declared_type)

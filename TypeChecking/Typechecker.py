from copy import deepcopy


# will have to pass typing enviroment as OJB
class Typing_env():
    def __init__(self, debug == False):
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
    def set_class(self. cname):
        pass

class Cool_class():
    # TODO: BASES CLASSES
    classes = {} # hash map that holds all classes
    def fetch_class(cname):
        try:
            return classes[cname]
        except:
            raise Exception("class not found: " + cname)
    def update_parent_mapping():
        for cl in classes.values():
            if isinstance(cl.parent, str):
                cl.parent = fetch_class(cl.parent)
    # name, parent, methods, attributes
    def __init__(self, name, parent = "Object", attributes = [], methods = []):
        if name in classes:
            raise Exception("redefinition of class: " + name)
        self.name = name
        self.parent = parent
        self.attributes = attributes
        self.methods = methods
        self.PulledFromParents = False

    def add_attris(self, a):
        self.attributes.append(a)
    def add_method(self, m):
        self.methods.append(a)
    def pull_from_parent(self):
        # TODO: PULL FROM PARENT
        # check for
        self.PulledFromParents = True
    def get_methods(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return self.methods
    def get_attris(self):
        if not self.PulledFromParents:
            self.pull_from_parent()
        return self.attributes

class Cool_stuff():
    # abstract class for stuff that has a static type
    def __init__(self, static_type = None):
        self.static_type = static_type
    def get_type(self, env):
        return self.static_type if self.static_type else self.eval()
    def eval(self, env):
        print("EVAL: should be overriden")
        exit(1)
    def __str__(self, env):
        print("__STR__: should be overriden")
        exit(1)

class Cool_attri(Cool_stuff):
    def __init__(self, name, decalred_type, init_expr = None):
        self.name = name
        self.decalred_type = decalred_type
        self.init_expr = init_expr
        super.__init__()

class Cool_method(Cool_stuff):
    def __init__(self, name, formals, decalred_type, body_expr, owner):
        self.name = name
        self.formals = formals
        self.decalred_type = decalred_type
        self.body_expr = body_expr
        super.__init__()

class Cool_expr_assign():

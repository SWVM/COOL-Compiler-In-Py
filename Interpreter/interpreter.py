class Cool_Id():
    def __init__(self, name, line):
        self.name = name
        self.line = line

class Env():
    def __init__(self):
        self.e = {}
        self.s = {}

    def epop(self, k):
        assert k in self.e
        if len(self.e[k]) == 1:
            self.e.pop(k)
        else:
            self.e.k = self.e.k[1:]

    def spop(self, k):
        # Not needed?
        pass

    def eadd(self, k, v):
        if k in self.e:
            self.e[k].insert(0, v)
        else:
            self.e[k] = [v]

    def sadd(self, k, v):
        self.s[k] = v

class Cool_value():
    def __init__(self, type, value):
        self.type = type
        self.value= value

class Cool_int(Cool_value):
    def __init__(self, value = 0):
        super(self).__init__("Int", value)

class Cool_string(Cool_value):
    def __init__(self, value = ""):
        self.length = len(value)
        super(self).__init__("String", value)

class Cool_bool(Cool_value):
    def __init__(self, value = False):
        super(self).__init__("Bool", value)

class Cool_obj(Cool_value):
    def __init__(self, type, attris):
        super(self).__init__(type, attris)

class Cool_void(Cool_value):
    def __init__(self):
        super(self).__init__("void", None)


class Cool_Prog():
    def __init__(self, fname):
        self.fin = open(fname, "r")
        self.cmap = {}
        self.imap = {}
        self.pmap = {}

    def read_class_map(self, fin):
        assert fin.readline() == "class_map\n"
        # TODO: class map
    def read_imp_map(self, fin):
        assert fin.readline() == "implementation_map\n"
        # TODO: imp map
    def read_parent_map(self, fin):
        assert fin.readline() == "parent_map\n"
        # TODO: parent map


class Cool_attri():
    def read(fin):
        init = fin.readline()[:-1]
        name = fin.readline()[:-1]
        type = fin.readline()[:-1]
        if init == "initializer":
            init = Cool_Expr.read()
            return Cool_attri(name, type, init)
        return Cool_attri(name, type)

    def __init__(self, name, type, init = None):
        self.name = name
        self.type = type
        self.init = init


class Cool_method():
    def read(fin):
        name = fin.readline()[:-1]


    def __init__(self, name, formals, body):
        self.name = name
        self.formals = formals
        self.body = body





class Cool_Expr():
    def __init__(self):
        pass
    def read_file():

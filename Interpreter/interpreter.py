

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

class Cool_obj():
    def __init__(self, type, init):
        self.type = type
        # TODO: INIT object vars

class Cool_base_class_obj(Cool_obj):
    # TODO: seperate base classes or as one py class?
    def __init__(self, type, v):
        self.type = type
        self.v    = v
        if type == "String":
            self.len = len(v)

class Cool_Prog():

class Cool_Expr():
    def __init__(self):
        pass
    def read_file():

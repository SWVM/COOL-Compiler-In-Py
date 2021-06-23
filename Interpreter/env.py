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

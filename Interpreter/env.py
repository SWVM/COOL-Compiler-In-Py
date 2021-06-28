class Store():
    MALLOC_COUNTER = 10000
    def __init__(self):
        self.map = {}

    def malloc(self):
        Store.MALLOC_COUNTER += 1
        return Store.MALLOC_COUNTER

    def add(self, add, val):
        self.map[add] = val

    def get(self, add):
        assert add in self.map
        return self.map[add]

class Env():
    def __init__(self, map={}):
        self.map = map

    def add(self, var, add):
        self.map[var] = add

    def copy(self):
        return Env(self.map.copy())



class Cool_value():
    def __init__(self, type, value):
        self.type = type
        self.value= value
    def get_type(self):
        return self.type

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

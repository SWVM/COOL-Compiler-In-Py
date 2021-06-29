class Store():
    MALLOC_COUNTER = 10000
    def __init__(self):
        self.map = {}

    def malloc(self):
        Store.MALLOC_COUNTER += 1
        return Store.MALLOC_COUNTER

    def set(self, add, val):
        self.map[add] = val

    def update(self, dict):
        self.map.update(dict)

    def __getitem__(self, key):
        assert key in self.map
        return self.map[key]

class Env():
    def __init__(self, map={}):
        self.map = map

    def add(self, var, add):
        self.map[var] = add

    def copy(self):
        return Env(self.map.copy())

class Cool_value():
    def init_for(cname):
        if cname == "Int":
            return Cool_int()
        elif cname == "String":
            return Cool_string()
        elif cname == "Bool":
            return Cool_bool()
        else:
            return Cool_void()

    def __init__(self, type, value):
        self.type = type
        self.value= value
    def get_type(self):
        return self.type
    def get_attris(self):
        if isinstance(self, Cool_obj):
            return self.value
        else:
            return {}

class Cool_int(Cool_value):
    def __init__(self, value = 0):
        super().__init__("Int", value)
    def __add__(self, o):
        return self.value + o.value
    def __mul__(self, o):
        return self.value * o.value
    def __truediv__(self, o):
        return self.value / o.value
    def __sub__(self, o):
        return self.value - o.value

class Cool_string(Cool_value):
    def __init__(self, value = ""):
        self.length = len(value)
        super().__init__("String", value)

class Cool_bool(Cool_value):
    def __init__(self, value = False):
        super().__init__("Bool", value in ["true", True])

class Cool_obj(Cool_value):
    def __init__(self, type, attris):
        super().__init__(type, attris)

class Cool_void(Cool_value):
    def __init__(self):
        super().__init__("void", None)

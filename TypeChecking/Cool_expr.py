from copy import deepcopy, copy
from Helpers import *

class Cool_expr():
    def read(fin):
        line = fin.readline()[:-1]
        ename= fin.readline()[:-1]
        if ename == "assign":
            var = read_Id(fin)
            expr= read_Expr(fin)
            return Expr_Assign(line, var, expr)
        elif ename == "integer":
            int_value = fin.readline()[:-1]
            return Expr_Integer(line, int_value)
        else:
            raise Exception("expr not yet implemented")

    def __init__(self, line, static_type = None):
        self.static_type = static_type
        self.line   = line

    def get_type(self, env):
        return self.static_type if self.static_type else self.eval()

    def eval():
        raise Exception("eval not overriden")

class Expr_Assign(Cool_expr):
    def __init__(self, line, var, expr):
        self.var = var
        self.expr = expr
        super().__init__(line)

class Expr_Integer(Cool_expr):
    def __init__(self, line, int_value):
        self.int_value = int_value
        super().__init__(line)

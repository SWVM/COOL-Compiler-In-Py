from Cool_types import *
from Helpers import *


if __name__ == '__main__':
    import sys
    prog = Cool_prog(sys.argv[1])
    prog.tc_pre_check()
    out = open(sys.argv[1][:-3] + "type-test", "w")
    out.write(prog.tc_class_map())
    out.write(prog.tc_imp_map())
    out.write(prog.tc_parent_map())
    out.write(prog.annotated_AST())

from Cool_types import *
from Helpers import *


if __name__ == '__main__':
    import sys
    prog = Cool_prog(sys.argv[1])
    prog.tc_class_map()
    prog.tc_imp_map()
    # prog.typeCheck()

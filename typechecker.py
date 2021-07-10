from io import StringIO
from Cool_types import *
from Helpers import *

def init_prog(inStream):
    prog = Cool_prog(inStream)
    prog.tc_pre_check()
    return prog

def get_type_checked_ast(inStream, opt = "ALL"):
    prog = init_prog(inStream)
    out_buffer = StringIO()
    if opt in [ "class_map", "ALL" ]:
        prog.tc_class_map(out_buffer)
    else:
        prog.tc_class_map()

    if opt in [ "imp_map", "ALL" ]:
        prog.tc_imp_map(out_buffer)
    else:
        prog.tc_imp_map()

    if opt in [ "parent_map", "ALL" ]:
        prog.tc_parent_map(out_buffer)
    else:
        prog.tc_parent_map()

    if opt in [ "anootated_ast", "ALL" ]:
        prog.annotated_AST(out_buffer)
    else:
        prog.annotated_AST()

    out_buffer.seek(0)
    return out_buffer



if __name__ == '__main__':
    import sys
    fin = open(sys.argv[1], "r")
    ast = get_type_checked_ast(fin).getvalue()
    fin.close()

    out = open(sys.argv[1][:-3] + "type-test", "w")
    out.write(ast)
    out.close()

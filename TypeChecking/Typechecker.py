from Cool_types import *
from Helpers import *

OBJECT = Cool_class(Cool_Id("Object","0"),  None,   [])
IO = Cool_class(    Cool_Id("IO","0"),      OBJECT, [])
INT = Cool_class(   Cool_Id("Int","0"),     OBJECT, [])
STRING = Cool_class(Cool_Id("String","0"),  OBJECT, [])
BOOL = Cool_class(  Cool_Id("Bool","0"),    OBJECT, [])

if __name__ == '__main__':
    import sys
    fin = open(sys.argv[1], "r")
    cls  = read_lst(Cool_class.read, fin)
    Cool_class.update_parent_mapping()
    for c in cls:
        c.get_methods()
        print(c)

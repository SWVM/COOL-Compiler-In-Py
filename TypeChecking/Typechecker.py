from Cool_types import *
from Helpers import *


M_abort = Cool_method(  Cool_Id("abort","0"),
                        [],
                        Cool_Id("Object","0"),
                        Expr_Internal(  Cool_Id("Object",0),
                                        "Object.abort")
)
M_copy = Cool_method(  Cool_Id("copy","0"),
                        [],
                        Cool_Id("SELF_TYPE","0"),
                        Expr_Internal(  Cool_Id("SELF_TYPE",0),
                                        "Object.copy")
)
M_type_name = Cool_method(  Cool_Id("type_name","0"),
                        [],
                        Cool_Id("String","0"),
                        Expr_Internal(  Cool_Id("String",0),
                                        "Object.type_name")
)
OBJECT = Cool_class( Cool_Id("Object","0"),  None,   [M_abort ,M_copy, M_type_name] )

M_out_string = Cool_method(  Cool_Id("out_string","0"),
                             [
                                Cool_formal( Cool_Id("x", "0"), Cool_Id("String", "0"))
                             ],
                             Cool_Id("SELF_TYPE","0"),
                             Expr_Internal(  Cool_Id("SELF_TYPE",0),
                                            "IO.out_string")
)
M_out_int    = Cool_method(  Cool_Id("out_int","0"),
                             [
                                Cool_formal( Cool_Id("x", "0"), Cool_Id("Int", "0"))
                             ],
                             Cool_Id("SELF_TYPE","0"),
                             Expr_Internal(  Cool_Id("SELF_TYPE",0),
                                            "IO.out_int")
)
M_in_string  = Cool_method(  Cool_Id("in_string","0"),
                             [],
                             Cool_Id("String","0"),
                             Expr_Internal(  Cool_Id("String",0),
                                            "IO.in_string")
)
M_in_int     = Cool_method(  Cool_Id("in_int","0"),
                             [],
                             Cool_Id("Int","0"),
                             Expr_Internal(  Cool_Id("Int",0),
                                            "IO.in_int")
)
IO = Cool_class(    Cool_Id("IO","0"),
                    features=[M_out_string, M_out_int, M_in_string, M_in_int]
                )

INT = Cool_class(   Cool_Id("Int","0"),
                    features=[]
                )

M_length    = Cool_method(  Cool_Id("length","0"),
                             [],
                             Cool_Id("Int","0"),
                             Expr_Internal(  Cool_Id("Int",0),
                                            "String.length")
)
M_concat    = Cool_method(  Cool_Id("concat","0"),
                             [
                                Cool_formal( Cool_Id("s", "0"), Cool_Id("String", "0"))
                             ],
                             Cool_Id("String","0"),
                             Expr_Internal(  Cool_Id("String",0),
                                            "String.concat")
)
M_substr    = Cool_method(  Cool_Id("substr","0"),
                             [
                                Cool_formal( Cool_Id("i", "0"), Cool_Id("Int", "0")),
                                Cool_formal( Cool_Id("l", "0"), Cool_Id("Int", "0"))
                             ],
                             Cool_Id("String","0"),
                             Expr_Internal(  Cool_Id("String",0),
                                            "String.substr")
)
STRING = Cool_class(    Cool_Id("String","0"),
                        features=[M_length, M_concat, M_substr]
                    )

BOOL = Cool_class(      Cool_Id("Bool","0"),
                        features=[]
                    )

if __name__ == '__main__':
    import sys
    fin = open(sys.argv[1], "r")
    cls  = read_lst(Cool_class.read, fin)
    cls  = Cool_class.classes
    for c in cls.values():
        c.pull_from_parent()
        print(c)

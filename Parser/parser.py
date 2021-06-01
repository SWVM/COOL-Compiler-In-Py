# Yacc example

import ply.yacc as yacc
# Get the token map from the lexer.  This is required.
from lex import tokens

precedence = (
    ("left", "LARROW"),
    ("left", "NOT"),
    ("nonassoc", "LE", "LT", "EQUALS"),
    ("left", "PLUS", "MINUS"),
    ("left", "TIMES", "DIVIDE"),
    ("left", "ISVOID"),
    ("left", "TILDE"),
    ("left", "AT"),
    ("left", "DOT"),
)


def p_cool_prog(p):
    '''
    cool_prog   : cool_class SEMI cool_prog
                |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]

def p_cool_class(p):
    '''
    cool_class  : CLASS TYPE INHERITS TYPE LBRACE feature_list RBRACE
                | CLASS TYPE LBRACE feature_list RBRACE
    '''
    if len(p) == 8:
        p[0] = ("inherits", (p[2],p.lineno(2)), (p[4],p.lineno(4)), p[6])
    else:
        p[0] = ("no_inherits", (p[2],p.lineno(2)), None, p[4])

def p_feature_list(p):
    '''
    feature_list : feature SEMI feature_list
                 |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]


def p_feature_method(p):
    '''
    feature : IDENTIFIER LPAREN formal_list RPAREN COLON TYPE LBRACE expression RBRACE
    '''
    p[0] = ("method", (p[1],p.lineno(1)), p[3], (p[6],p.lineno(6)), p[8])

def p_feature_attri_init(p):
    '''
    feature : IDENTIFIER COLON TYPE LARROW expression
    '''
    p[0] = ("attribute_init", (p[1],p.lineno(1)), (p[3],p.lineno(3)), p[5])

def p_feature_attri_no_init(p):
    '''
    feature : IDENTIFIER COLON TYPE
    '''
    p[0] = ("attribute_no_init", (p[1],p.lineno(1)), (p[3],p.lineno(3)))

def p_formal_list(p):
    '''
    formal_list : formal formal_tail
                |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_formal_tail(p):
    '''
    formal_tail : COMMA formal formal_tail
                |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[2]] + p[3]

def p_formal(p):
    '''
    formal : IDENTIFIER COLON TYPE
    '''
    p[0] = ((p[1],p.lineno(1)), (p[3],p.lineno(3)))

def p_expression_assign(p):
    '''
    expression : IDENTIFIER LARROW expression
    '''
    p[0] = ("assign", (p[1],p.lineno(1)), p[3], p.lineno(1))

def p_expression_static_dispatch(p):
    '''
    expression : expression AT TYPE DOT IDENTIFIER LPAREN arg_list RPAREN
    '''
    p[0] = ("static_dispatch", p[1], (p[3],p.lineno(3)), (p[5],p.lineno(5)), p[7], p[1][-1])

def p_expression_dynamic_dispatch(p):
    '''
    expression : expression DOT IDENTIFIER LPAREN arg_list RPAREN
    '''
    p[0] = ("dynamic_dispatch", p[1], (p[3],p.lineno(3)), p[5], p[1][-1])

def p_expression_self_dispatch(p):
    '''
    expression : IDENTIFIER LPAREN arg_list RPAREN
    '''
    p[0] = ("self_dispatch", (p[1],p.lineno(1)), p[3], p.lineno(1))

def p_expression_if(p):
    '''
    expression : IF expression THEN expression ELSE expression FI
    '''
    p[0] = ("if", p[2], p[4], p[6], p.lineno(1))

def p_expression_while(p):
    '''
    expression : WHILE expression LOOP expression POOL
    '''
    p[0] = ("while", p[2], p[4], p.lineno(1))

def p_expression_block(p):
    '''
    expression  : LBRACE block RBRACE
    '''
    p[0] = ("block", p[2], p.lineno(1))

def p_expression_let(p):
    '''
    expression : LET binding_list IN expression
    '''
    p[0] = ("let", p[2], p[4], p.lineno(1))

def p_expression_case(p):
    '''
    expression : CASE expression OF case_list ESAC
    '''
    p[0] = ("case", p[2], p[4], p.lineno(1))

def p_expression_new(p):
    '''
    expression : NEW TYPE
    '''
    p[0] = ("new", (p[2],p.lineno(2)), p.lineno(1))

def p_expression_isvoid(p):
    '''
    expression : ISVOID expression
    '''
    p[0] = ("isvoid", p[2], p.lineno(1))

def p_expression_arith(p):
    '''
    expression  : expression PLUS expression
                | expression MINUS expression
                | expression TIMES expression
                | expression DIVIDE expression
    '''
    #p[2].value is the name of the operation (plus, minus, times, divide)
    tbl = {'+':"plus", '-':"minus", '*':"times", '/':"divide"}
    p[0] = (tbl[p[2]], p[1], p[3], p[1][-1])

def p_expression_negate(p):
    '''
    expression : TILDE expression
    '''
    p[0] = ("negate", p[2], p.lineno(1))

def p_expression_lt(p):
    '''
    expression : expression LT expression
    '''
    p[0] = ("lt", p[1], p[3], p[1][-1])

def p_expression_LE(p):
    '''
    expression : expression LE expression
    '''
    p[0] = ("le", p[1], p[3], p[1][-1])

def p_expression_eqals(p):
    '''
    expression : expression EQUALS expression
    '''
    p[0] = ("eq", p[1], p[3], p[1][-1])

def p_expression_not(p):
    '''
    expression : NOT expression
    '''
    p[0] = ("not", p[2], p.lineno(1))

def p_expression_paran(p):
    '''
    expression : LPAREN expression RPAREN
    '''
    # the last element of the tuple is the line number
    # so here we just change the lineno of the inner expression to the lineno of LPAREN
    p[0] = p[2][:-1] + (p.lineno(1),)

def p_expression_id(p):
    '''
    expression : IDENTIFIER
    '''
    p[0] = ("identifier", (p[1],p.lineno(1)), p.lineno(1))

def p_expression_int(p):
    '''
    expression : INTEGER
    '''
    p[0] = ("integer", p[1], p.lineno(1))

def p_expression_str(p):
    '''
    expression : STRING
    '''
    p[0] = ("string", p[1], p.lineno(1))

def p_expression_true(p):
    '''
    expression : TRUE
    '''
    p[0] = ("true", p.lineno(1))

def p_expression_false(p):
    '''
    expression : FALSE
    '''
    p[0] = ("false", p.lineno(1))



def p_arg_list(p):
    '''
    arg_list : expression arg_list_tail
             |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[2]

def p_arg_list_tail(p):
    '''
    arg_list_tail : COMMA expression arg_list_tail
                  |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[2]] + p[3]

def p_block(p):
    '''
    block : expression SEMI block
          |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[1]] + p[3]

def p_binding_list(p):
    '''
    binding_list : binding binding_list_tail
    '''
    p[0] = [p[1]] + p[2]

def p_binding_list_tail(p):
    '''
    binding_list_tail : COMMA binding binding_list_tail
                      |
    '''
    if len(p) == 1:
        p[0] = []
    else:
        p[0] = [p[2]] + p[3]

def p_binding(p):
    '''
    binding : IDENTIFIER COLON TYPE LARROW expression
            | IDENTIFIER COLON TYPE
    '''
    if len(p) == 4:
        p[0] = ("let_binding_no_init", (p[1],p.lineno(1)), (p[3],p.lineno(3)))
    else:
        p[0] = ("let_binding_init", (p[1],p.lineno(1)), (p[3],p.lineno(3)), p[5])

def p_case_list(p):
    '''
    case_list : case_element
              | case_element case_list
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_case_element(p):
    '''
    case_element : IDENTIFIER COLON TYPE RARROW expression SEMI
    '''
    p[0] = ((p[1],p.lineno(1)), (p[3],p.lineno(3)), p[5])

# Error rule for syntax errors
def p_error(p):
    print("ERROR: %d: Parser: syntax error near %s" % (p.lineno, p.value) )
    exit(1)

# Build the parser
parser = yacc.yacc()


if __name__ == '__main__':
    from io import StringIO
    out_buffer = StringIO()

    def print_lst(func, lst):
        out_buffer.write(str(len(lst)))
        out_buffer.write("\n")
        for item in lst:
            func(item)

    def print_id(i):
        out_buffer.write(str(i[-1]))
        out_buffer.write("\n")
        out_buffer.write(i[0])
        out_buffer.write("\n")

    def print_formal(f):
        print_id(f[0])
        print_id(f[1])

    def print_feature(f):
        if f[0] == "method":
            out_buffer.write(f[0])
            out_buffer.write("\n")
            print_id(f[1])
            print_lst(print_formal, f[2])
            print_id(f[3])
            print_expr(f[4])
        elif f[0] == "attribute_init":
            out_buffer.write(f[0])
            out_buffer.write("\n")
            print_id(f[1])
            print_id(f[2])
            print_expr(f[3])
        elif f[0] == "attribute_no_init":
            out_buffer.write(f[0])
            out_buffer.write("\n")
            print_id(f[1])
            print_id(f[2])

    def print_binding(b):
        if b[0] == "let_binding_no_init":
            out_buffer.write(b[0])
            out_buffer.write("\n")
            print_id(b[1])
            print_id(b[2])
        elif b[0] == "let_binding_init":
            out_buffer.write(b[0])
            out_buffer.write("\n")
            print_id(b[1])
            print_id(b[2])
            print_expr(b[3])

    def print_case(c):
        print_id(c[0])
        print_id(c[1])
        print_expr(c[2])

    def print_expr(e):
        out_buffer.write(str(e[-1]))
        out_buffer.write("\n")
        out_buffer.write(e[0])
        out_buffer.write("\n")
        if e[0] == "assign":
            print_id(e[1])
            print_expr(e[2])
        elif e[0] == "static_dispatch":
            print_expr(e[1])
            print_id(e[2])
            print_id(e[3])
            print_lst(print_expr, e[4])
        elif e[0] == "dynamic_dispatch":
            print_expr(e[1])
            print_id(e[2])
            print_lst(print_expr, e[3])
        elif e[0] == "self_dispatch":
            print_id(e[1])
            print_lst(print_expr, e[2])
        elif e[0] == "if":
            print_expr(e[1])
            print_expr(e[2])
            print_expr(e[3])
        elif e[0] == "while":
            print_expr(e[1])
            print_expr(e[2])
        elif e[0] == "block":
            print_lst(print_expr, e[1])
        elif e[0] == "let":
            print_lst(print_binding, e[1])
            print_expr(e[2])
        elif e[0] == "case":
            print_expr(e[1])
            print_lst(print_case, e[2])
        elif e[0] == "new":
            print_id(e[1])
        elif e[0] == "isvoid":
            print_expr(e[1])
        elif e[0] in ["plus","minus","times","divide"]:
            print_expr(e[1])
            print_expr(e[2])
        elif e[0] == "negate":
            print_expr(e[1])
        elif e[0] == "lt":
            print_expr(e[1])
            print_expr(e[2])
        elif e[0] == "le":
            print_expr(e[1])
            print_expr(e[2])
        elif e[0] == "eq":
            print_expr(e[1])
            print_expr(e[2])
        elif e[0] == "not":
            print_expr(e[1])
        elif e[0] == "identifier":
            print_id(e[1])
        elif e[0] == "integer":
            out_buffer.write(e[1])
            out_buffer.write("\n")
        elif e[0] == "string":
            out_buffer.write(e[1])
            out_buffer.write("\n")
        elif e[0] in ["true", "false"]:
            pass
        else:
            raise TypeError("unknown expression type" + e[0])

    def print_class(cl):
        print_id(cl[1])
        out_buffer.write(cl[0])
        out_buffer.write("\n")
        if cl[2]:
            print_id(cl[2])
        print_lst(print_feature, cl[3])

    import sys
    f = open(sys.argv[1], "r")
    result = parser.parse(f.read())
    print_lst(print_class, result)
    f_out = open(sys.argv[1] + "-ast-test","w")
    f_out.write(out_buffer.getvalue())
    f_out.close()

from TypeChecker.typechecker import get_type_checked_ast
from Interpreter.interpreter import evaluate_cl_type
import argparse
import os
from Lexing.lex import get_toks_stream
from Parser.parser import get_ast_stream

arg_parser = argparse.ArgumentParser(description="Cool Interpretor")
arg_parser.add_argument("input_file", type=str, nargs=1,
                        help="path of the input file")
arg_parser.add_argument("--lex", action="store_true",
                        help="emit cl-lex file(tokenized input)")
arg_parser.add_argument("--parse", action="store_true",
                        help="emit cl-ast file(cool abstract syntax tree)")
arg_parser.add_argument("--type", action="store_true",
                        help="emit cl-type file(type checked ast)")
arg_parser.add_argument("--class-map", action="store_true",
                        help="emit cl-type file(classes & attributes)")
arg_parser.add_argument("--imp-map", action="store_true",
                        help="emit cl-type file(classes & methods)")
arg_parser.add_argument("--parent-map", action="store_true",
                        help="emit cl-type file(classes & inheritance)")

# args = arg_parser.parse_args()
args = arg_parser.parse_args( ["~/Documents/Git/COOL-Compiler-In-Py/Interpreter/test.cl-type"] )
fname, fext = os.path.splitext(args.input_file[0])
# args.lex

if fext == ".cl":
    IO_source = open(fname+".cl", "r")
elif fext == ".cl-lex":
    IO_lex = open(fname+".cl-lex", "r")
elif fext == ".cl-ast":
    IO_ast = open(fname+".cl-ast", "r")
elif fext == ".cl-type":
    IO_type = open(fname+".cl-type", "r")
else:
    raise Exception("Error: unknown file type...")

IO_lex = get_toks_stream(IO_source)
IO_ast = get_ast_stream(IO_lex)
IO_type= get_type_checked_ast(IO_ast)
evaluate_cl_type(IO_type)



print(args)


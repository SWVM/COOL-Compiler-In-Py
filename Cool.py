import argparse

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
args = arg_parser.parse_args( ["--lex","--lex","--lex","fasd"] )
fname= args.input_file[0]
# args.lex



print(args)


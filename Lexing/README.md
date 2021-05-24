# Lexer
## To run
- py lex.py input_file.cl
- py test_cases/test_script.py


## known issues
- it seems like python's read() method cannot tell the differences between \r and \n, which caused failure of /good/whitespace.cl
- the test script does not remove garbage!
- out put are saved into filename.cl-lex-test
- test script for windows only

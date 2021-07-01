class Main inherits IO {
  a : Object ; 
  b : Object ; 

  main() : Object { {
    out_string(
      if not (self = b) then 
      "Hello, World.\n"
      else "wrong-o" fi 
      ) ; 
  } } ;
} ; 

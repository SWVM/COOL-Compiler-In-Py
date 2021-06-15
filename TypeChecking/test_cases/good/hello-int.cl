class Main inherits IO {
  main() : Object { 
    (* integer wraparound in action! *) 
    { out_int(~2147483647 - 2) ;
      out_string("\n") ;
    } 
  } ;
} ; 

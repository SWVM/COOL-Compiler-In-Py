class Main inherits IO {
  foo(x : Main, y : Main) : Int { 
    let total : Int <- ~ 1 in 
    { x.set_x(5) ; 
    total <- total + x.get_x() + y.get_x() ;
    y.set_x(7) ; 
    total <- total + x.get_x() + y.get_x() ;
    total ; } 
  } ; 
  get_x() : Int { x } ;
  set_x(new_x : Int ) : SELF_TYPE { { x <- new_x ; self ; } } ;
  x : Int ; 
  main():IO {
    out_int (foo(self,self) ) -- 23 
  };
};

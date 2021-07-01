class Main {
  main():Object { {
    (new IO).out_string("hello, world!\n") ;
    let x :Int <- (new IO).in_int() in 
    let y : Int <- (new IO).in_int() in
    let z :  Int <- x + y in
    { y <- y + ((new IO).in_int ()) ;
    (new IO).out_int(x);
    (new IO).out_string(" --\n__");
    (new IO).out_string(x.type_name()); 
    (new IO).out_string(" --\n__");
    (new IO).out_int(y);
    (new IO).out_string(" --\n__");
    (new IO).out_int(z);
    (new IO).out_string(" --\n__\n");
    } ;
  } };
};

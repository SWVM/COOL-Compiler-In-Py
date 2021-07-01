class Main {
  main():Object { {
    (new IO).out_string("hello, world!\n") ;
    let x : String <- (new IO).in_string() in 
    let y : String <- (new IO).in_string() in
    let z : String <- (new IO).in_string() in
    let w : String <- (new IO).in_string() in
    { 
    (new IO).out_string(x); 
    (new IO).out_string("_\n");
    (new IO).out_string(z); 
    (new IO).out_string("_\n");
    (new IO).out_string(y); 
    (new IO).out_string("_\n");
    (new IO).out_string(w); 
    (new IO).out_string("_\n");
    (new IO).out_string(y.type_name()); 
    (new IO).out_string("_\n");
    y <- "foozle" ; 
    (new IO).out_string(y.concat(x.concat(z))); 
    (new IO).out_string("_\n");
    } ;
  } };
};

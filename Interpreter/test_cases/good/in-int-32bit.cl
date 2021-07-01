class Main {
  main():Object { {
    (new IO).out_string("hello, world!\n") ;
    let x :Int <- (new IO).in_int() in 
    let y :Int <- (new IO).in_int() in 
    let z :Int <- (new IO).in_int() in 
    let w :Int <- (new IO).in_int() in 
    { 
    (new IO).out_int(x);
    (new IO).out_string(" **\n");
    (new IO).out_int(y); 
    (new IO).out_string(" **\n");
    (new IO).out_int(z); 
    (new IO).out_string(" **\n");
    (new IO).out_int(w); 
    (new IO).out_string(" **\n");
} ;
  } };
};

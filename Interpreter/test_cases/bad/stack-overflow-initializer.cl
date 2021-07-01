class Foo { 
  x : Object <- 
        new Foo ; 
} ;

class Main inherits IO {
    y : Foo <- new Foo ; 
    main() : Object {
        out_string("Hello, world\n")
    };
}; 

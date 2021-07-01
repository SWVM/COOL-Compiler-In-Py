class Foo { 
  x : Object <- new Foo ; 
} ;

class Main inherits IO {
    mymeth() : Int { { 
        mymeth()  ; 5 ; } } ;
    main() : Object { {
        out_int(mymeth()); 
        out_string("Hello, world\n");
    } };
}; 

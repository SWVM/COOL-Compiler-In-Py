class Foo { 
  x : Object <- new Foo ; 
} ;

class Main inherits IO {
    mymeth(count : Int ) : Int { { 
        if not (count < 0) then
                mymeth(count - 1)  
        else 5 fi ; } } ;
    main() : Object { {
        out_int(mymeth(995)); 
        out_string("Hello, world\n");
    } };
}; 

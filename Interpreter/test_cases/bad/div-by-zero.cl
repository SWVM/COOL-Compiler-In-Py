class Main inherits IO {
    main() : Object { {
        out_string("Hello, world\n" . substr(7/0,9) ) ;
        out_string("\n") ; 
    } };
}; 

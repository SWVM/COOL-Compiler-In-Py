class Foo {
    bad1 : Int 0;
    good1 : Int <- 0;
    bad2(x:Int) : Int {
        x * 3 2
    };
    good2(x:Int) : Int {
        x * 3 + 2
    };
    bad3(x:Int,y:Int : Int {
        0
    };
    good3(x:Int,y:Int) : Int {
        0
    };
    bad4() : Int {
        0
    }
    good4() : Int {
        0
    };
    good5() : Int {
        0
    };
};

class Bar {
    good1 : Int;
};

class Baz {
    bad1() : Int {
        {
            Bad1;
            good1 <- 0;
            good2 <- 0;
            Bad2;
        }
    };
};

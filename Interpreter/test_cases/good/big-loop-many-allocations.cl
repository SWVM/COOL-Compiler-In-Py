--stress garbage collection by generating lots of new objects, 
--some are garbage, some stay around for a while

class Main inherits IO {
    ctr : Int <- 0;
    getctr() : Int { ctr };
    outctr() : Object {{ out_string("main ctr"); out_int(ctr); out_string("\n"); }};
   
    divides(x:Int, n:Int) : Bool { (x/n) * n = x };
    div2() : Bool { divides(ctr,2) };
    div3() : Bool { divides(ctr,3) };
    div5() : Bool { divides(ctr,5) };
    div7() : Bool { divides(ctr,7) };
    div11() : Bool { divides(ctr,11) };
    div13() : Bool { divides(ctr,13) };
    div41() : Bool { divides(ctr,41) };

    big : Big;
    main() : Object {{
        big <- new Big;
        big.setctr(0);
        ctr <- 0;
        while (ctr < 10000) loop
           let nb : Big <- new Big, v : Big, n : Big <- new Big in {
               n.setctr(~ctr);
               nb.setctr(ctr);

               big.abc( if div13() then n else big.geta() fi,
                        if div11() then n else big.getb() fi,
                        if div7() then n else big.getc() fi );

               nb.abc( if div5() then n else big fi,
                       if div3() then n else big fi,
                       if div2() then n else big fi );
	
--               if div2()  then big <- nb else 0 fi;
--               if div3()  then big <- nb else 0 fi;
--               if div5()  then big <- nb else 0 fi;
               big <- nb;

               if div41() then big.abc(big.getb(), big.getc(), big.geta()) else 0 fi;

               ctr <- ctr+1;
           }  
        pool;
        big.outctr();
   }};
};



class Big inherits IO {
    ctr : Int;
    setctr(cc : Int) : Int { ctr <- cc };
    outctr() : Object { outctr2(0) };
    outctr2(depth : Int) : Object {{ 
        { let ii:Int<-0 in while(ii<depth) loop { out_string(" "); ii<-ii+1; } pool; };
        out_int(ctr); 
        out_string("\n"); 
        if (not isvoid s) then s.outctr2(depth+1) else 0 fi;
        if (not isvoid f) then f.outctr2(depth+1) else 0 fi;
        if (not isvoid g) then g.outctr2(depth+1) else 0 fi;
    }};

    abc(aa : Big, bb : Big, cc : Big) : Big {{ s<-aa; f<-bb; g<-cc; self; }};
    geta() : Big {s};
    getb() : Big {f};
    getc() : Big {g};
    a : Big;
    b : Big;
    c : Big;
    d : Int;
    e : Int;
    f : Big;
    g : Big;
    h : Int;
    i : Int;
    j : Int;
    k : Int;
    l : Int;
    m : Int;
    n : Int;
    o : Int;
    p : Int;
    q : Int;
    r : Int;
    s : Big;
    t : Int;
    u : Int;
    v : Int;
    w : Int;
    x : Int;
    y : Int;
    z : Int;
};








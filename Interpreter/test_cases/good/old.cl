class ListNode {
  next: ListNode;
  name: String;
  getNext():ListNode{ next};
  setNext(n:ListNode):ListNode{next <- n};
  getName():String{name};
  setName(n:String):String{name <- n};
};

class Main inherits IO {
      n1:ListNode;

      i:Int <- 0;
      garbage_amount:Int <- 5000; -- matth: something's wrong with the reference compiler when this is 100000

      main() : Object {{
             n1 <- new ListNode;
             let n2:ListNode <- new ListNode in {
                 out_string("List nodes allocated, now generating garbage\n");
                 while(i < garbage_amount) loop i <- i + 1 pool;
                 out_string("Garbage creation complete\n");
                 n1.setNext(new ListNode);
                 n2.setNext(new ListNode);
                 n1.getNext().setName("n1's next");
                 n2.getNext().setName("n2's next");
                 out_string("Now creating more garbage\n");
                 i <- 0;
                 while(i < garbage_amount) loop i <- i + 1 pool;
                 out_string("Garbage creation complete, now testing\n");
                 out_string("N1's next is \"");
                 out_string(n1.getNext().getName());
                 out_string("\"\n");
                 out_string("N2's next is \"");
                 out_string(n2.getNext().getName());
                 out_string("\"\n");

             };
          out_string("Test Complete\n");
   }};
};



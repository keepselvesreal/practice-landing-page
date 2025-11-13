# 7.4 Dependency via class constructor or value via method parameter? (pp.189-191)

---
**Page 189**

189
Dependency via class constructor or value via method parameter?
Again, do not take this example literally. Just remember that small design changes
that improve your testability are fine. Sometimes it can be hard to tell whether a
change will make the code design bad. Try it, and if you don’t like it, discard it. Prag-
matism is key. 
7.4
Dependency via class constructor or value via 
method parameter?
A very common design decision is whether to pass a dependency to the class via con-
structor (so the class uses the dependency to get a required value) or pass that value
directly to the method. As always, there is no right or wrong way. However, there is a
trade-off you must understand to make the best decision.
 Let’s use the ChristmasDiscount example, as it fits this discussion perfectly. The
following listing shows the code again.
public class ChristmasDiscount {
  private final Clock clock;
  public ChristmasDiscount(Clock clock) { 
    this.clock = clock;
  }
  public double applyDiscount(double rawAmount) {
    LocalDate today = clock.now(); 
    double discountPercentage = 0;
    boolean isChristmas = today.getMonth()== Month.DECEMBER
                && today.getDayOfMonth()==25;
    if(isChristmas)
      discountPercentage = 0.15;
    return rawAmount - (rawAmount * discountPercentage);
  }
}
The ChristmasDiscount class needs the current date so it knows whether it is
Christmas and whether to apply the Christmas discount. To get the date, the class
uses another dependency, which knows how to get the current date: the Clock
class. Testing ChristmasDiscount is easy because we can stub Clock and simulate
any date we want.
 But having to stub one class is more complex than not having to stub one class.
Another way to model this class and its expected behavior is to avoid the dependency
on Clock and receive the data as a parameter of the method. This other implementa-
tion is shown in listing 7.14. Now the applyDiscount() method receives two parame-
ters: rawAmount and today, which is today’s date.
Listing 7.13
ChristmasDiscount class, one more time
We can inject a stubbed 
version of Clock here.
Calls the now() method 
to get the current date


---
**Page 190**

190
CHAPTER 7
Designing for testability
public class ChristmasDiscount {
  public double applyDiscount(double rawAmount, LocalDate today) { 
    double discountPercentage = 0;
    boolean isChristmas = today.getMonth()== Month.DECEMBER
                && today.getDayOfMonth()==25;
    if(isChristmas)
      discountPercentage = 0.15;
    return rawAmount - (rawAmount * discountPercentage);
  }
}
This method is also easily testable. We do not even need mocks to test it, as we can pass
any LocalDate object to this method. So, if it is easier to pass the value via method
parameter rather than a dependency via its constructor, why do we do it?
 First, let’s explore the pros and cons of passing the value we want directly via a
method parameter, avoiding all the dependencies. This is often the simplest solution in
terms of both implementation (no need for dependencies via constructor) and testing
(passing different values via method calls). But the downside is that all the callers of this
class will need to provide this parameter. In this example, ChristmasDiscount expects
today to be passed as a parameter. This means the clients of the applyDiscount()
method must pass the current date. How do we get the current date in this code base?
Using the Clock class. So, while ChristmasDiscount no longer depends on Clock, its
callers will depend on it. In a way, we pushed the Clock dependency up one level. The
question is, is this dependency better in the class we are modeling now or in its callers?
 Now, let’s explore the idea of passing a dependency that knows how to get the
required parameter. We did this in the first implementation of the ChristmasDiscount
class, which depends on Clock; the applyDiscount() method invokes clock.now()
whenever it needs the current date. While this solution is more complicated than the
previous one, it enables us to easily stub the dependency as we did in chapter 6.
 It is also simple to write tests for the classes that depend on ChristmasDiscount.
These classes will mock ChristmasDiscount’s applyDiscount(double rawAmount)
method without requiring the Clock. The next listing shows a generic consumer
that receives the ChristmasDiscount class via the constructor, so you can stub it
during testing.
public class SomeBusinessService {
  private final ChristmasDiscount discount;
  public SomeBusinessService(ChristmasDiscount discount) { 
    this.discount = discount;
  }
Listing 7.14
ChristmasDiscount without depending on Clock
Listing 7.15
Generic consumer of the ChristmasDiscount class
The method
receives one
more parameter:
a LocalDate.
We inject a
ChristmasDiscount stub here.


---
**Page 191**

191
Designing for testability in the real world
  public void doSomething() {
    // ... some business logic here ...
    discount.applyDiscount(100.0);
    // continue the logic here...
  }
}
Listing 7.16 shows the tests for this SomeBusinessService class. We stub the Christmas-
Discount class. Note that this test does not need to handle Clock. Although Clock is a
dependency of the concrete implementation of ChristmasDiscount, we do not care
about that when stubbing. So, in a way, the ChristmasDiscount class gets more com-
plicated, but we simplify testing its consumers.
@Test
void test() {
  ChristmasDiscount discount = Mockito.mock(ChristmasDiscount.class); 
  SomeBusinessService service = new SomeBusinessService(discount);
  service.doSomething();
  // ... test continues ...
}
Receiving a dependency via constructor adds a little complexity to the overall class
and its tests but simplifies its client classes. Receiving the data via method parameter
simplifies the class and its tests but adds a little complexity to the clients. Software
engineering is all about trade-offs.
 As a rule of thumb, I try to simplify the work of the callers of my class. If I must
choose between simplifying the class I am testing now (such as making Christmas-
Discount receive the date via parameter) but complicating the life of all its callers
(they all must get the date of today themselves) or the other way around (Christmas-
Discount gets more complicated and depends on Clock, but the callers do not need
anything else), I always pick the latter. 
7.5
Designing for testability in the real world
Writing tests offers a significant advantage during development: if you pay attention to
them (or listen to them, as many developers say), they may give you hints about the
design of the code you are testing. Achieving good class design is a challenge in com-
plex object-oriented systems. The more help we get, the better.
 The buzz about tests giving feedback about the design of the code comes from the
fact that all your test code does is exercise the production class:
1
It instantiates the class under test. It can be as simple as a new A() or as compli-
cated as A(dependency1, dependency2, …). If a class needs dependencies, the
test should also instantiate them.
Listing 7.16
Example of the test for the generic consumer class
Mocks ChristmasDiscount. Note
that we do not need to mock
or do anything with Clock.



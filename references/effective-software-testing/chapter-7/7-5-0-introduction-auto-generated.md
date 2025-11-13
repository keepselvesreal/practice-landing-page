# 7.5.0 Introduction [auto-generated] (pp.191-192)

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


---
**Page 192**

192
CHAPTER 7
Designing for testability
2
It invokes the method under test. It can be as simple as a.method() or as com-
plicated as a.precall1(); a.precall2(); a.method(param1, param2, …);. If a
method has pre-conditions before being invoked and/or receiving parameters,
the test should also be responsible for those.
3
It asserts that the method behaves as expected. It can be as simple as assert-
That(return).isEqualTo(42); or as complicated as dozens of lines to
observe what has happened in the system. Again, your test code is responsible
for all the assertions.
You should constantly monitor how hard it is to perform each of these steps. Is it dif-
ficult to instantiate the class under test? Maybe there is a way to design it with fewer
dependencies. Is it hard to invoke the method under test? Maybe there is a way to
design it so its pre-conditions are easier to handle. Is it difficult to assert the out-
come of the method? Maybe there is a way to design it so it is easier to observe what
the method does.
 Next, I will describe some things I pay attention to when writing tests. They give me
feedback about the design and testability of the class I am testing.
7.5.1
The cohesion of the class under test
Cohesion is about a module, a class, a method, or any element in your architecture
having only a single responsibility. Classes with multiple responsibilities are naturally
more complex and harder to comprehend than classes with fewer responsibilities. So,
strive for classes and methods that do one thing. Defining what a single responsibility
means is tricky and highly context-dependent. Nevertheless, sometimes it can be easy
to detect multiple responsibilities in a single element, such as a method that calculates
a specific tax and updates the values of all its invoices.
 Let’s give you some ideas about what you can observe in a test. Note that these tips
are symptoms or indications that something may be wrong with the production code.
It is up to you to make the final decision. Also, note that these tips are solely based on
my experience as a developer and are not scientifically validated:
Non-cohesive classes have very large test suites. They contain a lot of behavior that
needs to be tested. Pay attention to the number of tests you write for a single
class and/or method. If the number of tests grows beyond what you consider
reasonable, maybe it is time to re-evaluate the responsibilities of that class or
method. A common refactoring strategy is to break the class in two.
Non-cohesive classes have test suites that never stop growing. You expect the class to
reach a more stable status at some point. However, if you notice that you are
always going back to the same test class and adding new tests, this may be a bad
design. It is usually related to the lack of a decent abstraction.
– A class that never stops growing breaks both the Single Responsibility (SRP)
and the Open Closed (OCP) principles from the SOLID guidelines. A com-
mon refactoring strategy is to create an abstraction to represent the different



# 7.2 Dependency injection and controllability (pp.181-184)

---
**Page 181**

181
Dependency injection and controllability
This idea of separating infrastructure from domain code appears not only in Cock-
burn’s Hexagonal Architecture but also in many other interesting works on software
design, such as the well-known Domain-Driven Design by Evans (2004) and Martin’s
Clean Architecture (2018). This principle is pervasive among those who talk about soft-
ware design and testability. I agree with all these authors.
 A common question for those new to the Hexagonal Architecture (or domain-
driven design, or clean architecture) is, “Do I need to create interfaces for every
port?” I hope to convince you that there are no rights and wrongs, that everything
depends, and that being pragmatic is key. Of course you do not have to create inter-
faces for everything in your software system. I create interfaces for ports where I see
more than one implementation. Even if I do not create an interface to represent an
abstract behavior, I make sure the concrete implementation does not leak any of its
implementation details. Context and pragmatism are kings.
 To sum up, the main “design for testability” principle I follow at the architectural
level is to separate infrastructure from business code. Do not be tempted to think,
for instance, “This is a simple call to the database. Look how easy it is to implement
here!” It is always easier to write untestable code, but doing so will bite you in the
future. 
7.2
Dependency injection and controllability
At the architectural level, we saw that an important concern is to ensure that application
(or domain) code is fully separated from the infrastructure code. At the class level, the
most important recommendation I can give you is to ensure that classes are fully control-
lable (that is, you can easily control what the class under test does) and observable (you
can see what is going on with the class under test and inspect its outcome).
 For controllability, the most common implementation strategy I apply is the one
we used in chapter 6: if a class depends on another class, make it so the dependency can
easily be replaced by a mock, fake, or stub. Look back at the PaidShoppingCartsBatch
class (listing 7.2). It depends on four other classes. The PaidShoppingCartsBatch class
receives all its dependencies via constructor, so we can easily inject mocks. The version
of PaidShoppingCartsBatch in listing 7.6 does not receive its dependencies but
instead instantiates them directly. How can we test this class without depending on
databases, web services, and so on? It is almost the same implementation but much
harder to test. It is that easy to write untestable code.
public class VeryBadPaidShoppingCartsBatch {
  public void processAll() {
    ShoppingCartHibernateDao db = new ShoppingCartHibernateDao(); 
    List<ShoppingCart> paidShoppingCarts = db.cartsPaidToday();
    for (ShoppingCart cart : paidShoppingCarts) {
Listing 7.6
A badly implemented PaidShoppingCartsBatch
Instantiates the database
adapter. Bad for testability!


---
**Page 182**

182
CHAPTER 7
Designing for testability
      DeliveryCenterRestApi deliveryCenter =
        new DeliveryCenterRestApi();   
      LocalDate estimatedDayOfDelivery = deliveryCenter.deliver(cart);
      cart.markAsReadyForDelivery(estimatedDayOfDelivery); 
      db.persist(cart);                                    
      SMTPCustomerNotifier notifier = new SMTPCustomerNotifier(); 
      notifier.sendEstimatedDeliveryNotification(cart);
      SAPSoapWebService sap = new SAPSoapWebService();   
      sap.cartReadyForDelivery(cart);
    }
  }
}
Traditional code tends to be responsible for instantiating its dependencies. But this
hinders our ability to control the internals of the class and use mocks to write unit
tests. For our classes to be testable, we must allow their dependencies (especially the
ones we plan to stub during testing) to be injected.
 In the implementation, this can be as simple as receiving the dependencies via
constructor or, in more complex cases, via setters. Making sure dependencies can be
injected (the term dependency injection is commonly used to refer to this idea; I also
describe it in chapter 6) improves our code in many ways:
It enables us to mock or stub the dependencies during testing, increasing our
productivity during the testing phase.
It makes all the dependencies more explicit. They all need to be injected (via
constructor, for example).
It offers better separation of concerns: classes do not need to worry about how
to build their dependencies, as the dependencies are injected into them.
The class becomes more extensible. This point is not related to testing, but as a
client of the class, you can pass any dependency via the constructor.
NOTE
A Java developer may recognize several frameworks and libraries con-
nected to dependency injection, such as the well-known Spring framework
and Google Guice. If your classes allow dependencies to be injected, Spring
and Guice will automatically help you instantiate those classes and their tree
of dependencies. While such frameworks are not needed at testing time (we
usually pass the mocked dependencies manually to the classes under test),
this approach is particularly useful to instantiate classes and their dependen-
cies at production time. I suggest learning more about such frameworks!
By devising interfaces that represent the abstract interactions that domains and infra-
structure classes will have with each other (the ports), we better separate the con-
cerns, reduce the coupling between layers, and devise simpler flows of interactions
between layers. In our example, the PaidShoppingCartsBatch domain class does not
depend on the adapters directly. Rather, it depends on an interface that defines what
Notifies the
delivery system
about the delivery.
But first, we need
to instantiate its
adapter. Bad for
testability!
Marks as ready 
for delivery and 
persist
Sends a notification
using the adapter
directly. Bad for
testability!
Notifies SAP
using the
adapter
directly. Bad
for testability!


---
**Page 183**

183
Dependency injection and controllability
the adapters should do abstractly. The SAP port interface knows nothing about how
the real SAP works. It provides a cartReadyForDelivery method to the domain
classes. This completely decouples the domain code from details of how the external
infrastructure works.
 The dependency inversion principle (note the word inversion, not injection) helps us
formalize these concepts:
High-level modules (such as our business classes) should not depend on low-
level modules. Both should depend on abstractions (such as interfaces).
Abstractions should not depend on details. Details (concrete implementations)
should depend on abstractions.
Figure 7.3 illustrates the principle. The domain objects, which are considered high-
level classes, do not depend on low-level details such as a database or web service com-
munication. Instead, they depend on abstractions of those low-level details. In the fig-
ure, the abstractions are represented by the interfaces.
Note the pattern: our code should always depend as much as possible on abstractions
and as little as possible on details. The advantage of always depending on abstractions
and not on low-level details is that abstractions are less fragile and less prone to
change than low-level details. You probably do not want to change your code when-
ever a low-level detail changes.
 Again, coming up with interfaces for everything is too much work. I prefer to make
sure all of my classes offer a clear interface to their consumers—one that does not
leak internal details. For those more familiar with object-oriented programming con-
cepts, I am talking about proper encapsulation.
 How does depending on an abstraction help with testing? When you unit-test a
class, you probably mock and stub its dependencies. When you mock, you naturally
High-level class
(e.g., domain object)
High-level class
Interface
Interface
Low-level class
(e.g., database
adapter)
Low-level class
Low-level class
High-level modules
Low-level modules
High-level modules and low-level
modules do not know each other;
they all depend on interfaces.
Figure 7.3
An illustration of the dependency inversion principle


---
**Page 184**

184
CHAPTER 7
Designing for testability
depend on what the mocked class offers as a contract. The more complex the class
you are mocking, the harder it is to write the test. When you have ports, adapters, and
the dependency inversion principle in mind, the interface of a port is naturally sim-
ple. The methods that ports offer are usually cohesive and straight to the point.
 In the example, the ShoppingCartRepository class has a List<ShoppingCart>
cartsPaidToday() method. It is clear what this method does: it returns a list of shop-
ping carts that were paid today. Mocking this method is trivial. Its concrete adapter
implementation is probably complicated, full of database-related code and SQL que-
ries. The interface removes all this complexity from testing the PaidShoppingCarts-
Batch class. Therefore, designing the ports in a simple way also makes your code
easier to test. Complex ports and interfaces require more work.
 When things become more complicated, making sure dependencies are always
injected may not be as straightforward as I have made it seem. It is much easier not to do
this. But you must convince yourself that the extra effort will pay off later during testing.
NOTE
This chapter is a quick introduction to the Hexagonal Architecture
and to the Dependency Inversion Priniciple. I suggest you dive into the
related literature, including the books by Martin (2014) and Freeman and
Pryce (2009), for more details. I also recommend Schuchert’s guest post on
dependency inversion in the wild in Fowler’s wiki (2013); he explains the dif-
ference between dependency inversion and dependency injection and gives
lots of examples of how he applied the principle in real-world situations. 
7.3
Making your classes and methods observable
Observability, at the class level, is about how easy it is to assert that the behavior of the
functionality went as expected. My main advice is to ensure that your classes provide
developers with simple and easy ways to assert their state. Does a class produce a list of
objects you need to assert one by one? Create a getListOfSomething in that class,
which the test can use to get the generated list of objects. Does a class make calls to
other classes? Make sure these dependencies can be mocked and your test can assert
their interaction. Does a class make internal changes in its attributes, but the class can-
not or does not offer getters to each of them? Make the class offer a simple isValid
method that returns whether the class is in a valid state.
 It has to be easy for the test code to inspect the class behavior. Whenever it is difficult
to observe whether the program behaves as expected, reflect on how observable the
classes are. Do not be afraid to introduce simple getters or simple solutions to facilitate
your testing. Behavior that is easy to observe will make the test code much easier! Let’s
look at two pragmatic changes I make in my code so it is more observable.
7.3.1
Example 1: Introducing methods to facilitate assertions
Take another look at the processAll() method and its test, in listings 7.2 and 7.5. Most
of what its test asserts is the interaction with the ports. Such assertions are easily done,
and we did not need much more than basic Mockito. Now, let’s look closer at one specific
assertion: verify(someCart).markAsReadyForDelivery(someDate);. The someCart



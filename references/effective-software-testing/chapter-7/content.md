# Designing for testability (pp.172-198)

---
**Page 172**

172
Designing for testability
I usually say that every software system can be tested. However, some systems are more
testable than others. Imagine that for a single test case, we need to set up three differ-
ent web services, create five different files in different folders, and put the database
in a specific state. After all that, we exercise the feature under test and, to assert the
correct behavior, again need to see if the three web services were invoked, the five
files were consumed correctly, and the database is now in a different state. All those
steps are doable. But couldn’t this process be simpler?
 Software systems are sometimes not ready for or designed to be tested. In this
chapter, we discuss some of the main ideas behind systems that have high testability.
Testability is how easy it is to write automated tests for the system, class, or method
under test. In chapter 6, we saw that by allowing dependencies to be injected, we
This chapter covers
Designing testable code at the architectural, 
design, and implementation levels
Understanding the Hexagonal Architecture, 
dependency injection, observability, and 
controllability
Avoiding testability pitfalls


---
**Page 173**

173
Separating infrastructure code from domain code
could stub the dependency. This chapter is about other strategies you can use to make
testing easier.
 The topic of design for testability deserves an entire book. In this chapter, I cover
several design principles that solve most of the problems I face. When presenting
these principles, I will discuss the underlying ideas so you can apply them even if the
code changes you must make differ from my examples.
 Design for testability is fundamental if our goal is to achieve systematic testing—if
your code is hard to test, you probably won’t test it. When do I design for testability?
What is the right moment to think about testability? All the time. Much of it happens
while I am implementing a feature.
 You should design for testability from the very beginning, which is why I put it in the
“testing to guide development” part of the flow back in chapter 1, figure 1.4. Sometimes
I cannot see the untestable part during the implementation phase, and it haunts me
during the test phase. When that happens, I go back to my code and refactor it.
 Some developers argue that designing for testability is harder and costs too many
extra lines of code. This may be true. Writing spaghetti code is easier than develop-
ing cohesive classes that collaborate and are easily tested. One of the goals of this
chapter is to convince you that the extra effort of designing for testability will pay
off. Good, testable code costs more than bad code, but it is the only way to ensure
quality.
7.1
Separating infrastructure code from domain code
I could spend pages discussing architectural patterns that enable testability. Instead,
I will focus on what I consider the most important advice: separate infrastructure code
from domain code.
 The domain is where the core of the system lies: that is, where all the business rules,
logic, entities, services, and similar elements reside. Entities like Invoice and services
such as ChristmasDiscount are examples of domain classes. Infrastructure relates to all
code that handles an external dependency: for example, pieces of code that handle
database queries (in this case, the database is an external dependency) or web service
calls or file reads and writes. In our previous examples, all of our data access objects
(DAOs) are part of the infrastructure code.
 In practice, when domain code and infrastructure code are mixed, the system
becomes harder to test. You should separate them as much as possible so the infra-
structure does not get in the way of testing. Let’s start with InvoiceFilter example,
now containing the SQL logic instead of depending on a DAO.
public class InvoiceFilter {
  private List<Invoice> all() { 
    try {
      Connection connection =
Listing 7.1
InvoiceFilter that mixes domain and infrastructure
This method gets all the invoices 
directly from the database. Note that it 
resides in the InvoiceFilter class, unlike 
in previous examples.


---
**Page 174**

174
CHAPTER 7
Designing for testability
        DriverManager.getConnection("db", "root", ""); 
      PreparedStatement ps =
        connection.prepareStatement("select * from invoice"));
      Result rs = ps.executeQuery();
      List<Invoice> allInvoices = new ArrayList<>();
      while (rs.next()) {
        allInvoices.add(new Invoice(
          rs.getString("name"), rs.getInt("value")));
      }
      ps.close();
      connection.close();
      return allInvoices;
    } catch(Exception e) { 
      // handle the exception
    }
  }
}
public List<Invoice> lowValueInvoices() { 
  List<Invoice> issuedInvoices = all();
  return issuedInvoices.all().stream()
    .filter(invoice -> invoice.value < 100)
    .collect(toList());
 }
}
We can make the following observations about this class:
Domain code and infrastructure code are mixed. This means we will not be able to
avoid database access when testing the low-value invoices rule. How would you
stub the private method while exercising the public method? Because we can-
not easily stub the database part, we must consider it when writing the tests. As
we have seen many times already, this is more complex.
The more responsibilities, the more complexity, and the more chances for bugs. Classes
that are less cohesive contain more code. More code means more opportunities
for bugs. This example class may have bugs related to SQL and the business
logic, for example. Empirical research shows that longer methods and classes
are more prone to defects (see the 2006 paper by Shatnawi and Li).
Infrastructure is not the only external influence our code may suffer from. User inter-
faces are often mixed with domain code, which is usually a bad idea for testability. You
should not need the user interface to exercise your system’s business rules.
 Besides the hassle of handling infrastructure when writing tests, extra cognitive
effort is often required to engineer the test cases. Speaking from experience, it is
much easier to test a class that has a single responsibility and no infrastructure than it
is to test a non-cohesive class that handles business rules and, for example, database
JDBC code to execute a
simple SELECT query. If
you are not a Java
developer, there is no
need to know what
PreparedStatement
and Result are.
Database APIs often 
throw exceptions that 
we need to handle.
The same lowValueInvoices method 
we’ve seen before, but now it calls 
a method in the same class to get 
the invoices from the database.


---
**Page 175**

175
Separating infrastructure code from domain code
access. Simpler code also has fewer possibilities and corner cases to see and explore.
On the other hand, the more complex the code is, or the more responsibilities it has,
the more we must think about test cases and possible interactions between features
that are implemented in one place. In the example, the interaction between the infra-
structure code and the business rule is simple: the method returns invoices from the
database. But classes that do more complex things and handle more complex infra-
structure can quickly become a nightmare during testing and maintenance.
 The architecture of the software system under development needs to enforce a
clear separation of responsibilities. The simplest way to describe it is by explaining the
Ports and Adapters (or Hexagonal Architecture) pattern. As Alistair Cockburn proposed
(2005), the domain (business logic) depends on ports rather than directly on the infra-
structure. These ports are interfaces that define what the infrastructure can do and
enable the application to get information from or send information to something
else. They are completely separated from the implementation of the infrastructure.
On the other hand, the adapters are very close to the infrastructure. They are the
implementations of the ports that talk to the database, web service, and so on. They
know how the infrastructure works and how to communicate with it.
 Figure 7.1 illustrates a hexagonal architecture. The inside of the hexagon represents
the application and all its business logic. The code is related to the application’s business
logic and functional requirements. It knows nothing about external systems or required
infrastructure. However, the application will require information or interaction with the
external world at some point. For that, the application does not interact directly with the
external system: instead, it communicates with a port. The port should be agnostic of the
technology and, from the application’s perspective, abstract away details of how commu-
nication happens. Finally, the adapter is coupled to the external infrastructure. The
Database
adapter
Feature 2
Feature N
Feature 1
Some system
adapter
UI adapter
Some other
system adapter
Port
Port
Port
Port
Figure 7.1
An illustration of the Hexagonal Architecture (or Ports and Adapters) pattern


---
**Page 176**

176
CHAPTER 7
Designing for testability
adapter knows how to send or retrieve messages from the external infrastructure and
sends them back to the application in the format defined by the port.
 Let’s cook up a simple example that illustrates these concepts in practice. Suppose
an online web shop has the following requirements:
For all the shopping carts that were paid today, the system should
Set the status of the shopping cart as ready for delivery, and persist its new
state in the database.
Notify the delivery center, and let them know they should send the goods
to the customer.
Notify the SAP system.
Send an e-mail to the customer confirming that the payment was success-
ful. The e-mail should contain an estimate of when delivery will happen.
The information is available via the delivery center API.
The first step is identifying what belongs to the application (the hexagon) and what
does not. It is clear that any business rule related to ShoppingCart, such as changing
its state, as well as the entire workflow the shopping cart goes through once it’s paid,
belongs inside the hexagon. However, a service that provides e-mail capabilities, a ser-
vice that communicates with the SAP, a service that communicates with the delivery
center API (which is probably offered as a web service), and a service that can commu-
nicate with the database are all handled by external systems. For those, we need to
devise a clear interface for the application to communicate with (the ports) together
with a concrete implementation that can handle communication with the external sys-
tem (the adapters). Figure 7.2 illustrates the concrete application of the Ports and
Adapters pattern to this example.
 A natural implementation for the PaidShoppingCartsBatch class would be the
code in listing 7.2. It does not contain a single detail regarding infrastructure. This
entire class could easily be unit-tested if we stubbed its dependencies. Does it need a
list of paid shopping carts, normally returned by cartsPaidToday()? We stub it. Does
it notify the SAP via the cartReadyForDelivery() method? We mock SAP and later
assert the interaction with this method.
 When we put everything together in production, the method will communicate
with databases and web services. But at unit testing time, we do not care about that.
The same testing philosophy we discussed in chapter 6 applies here: when (unit) test-
ing the PaidShoppingCartsBatch class, we should focus on PaidShoppingCartsBatch
and not its dependencies. This is possible here because (1) we receive its dependen-
cies via the constructor (which enables us to pass mocks and stubs to the class), and
(2) this class is only about business and has no lines of infrastructure code.
 
 
 


---
**Page 177**

177
Separating infrastructure code from domain code
public class PaidShoppingCartsBatch {
  private ShoppingCartRepository db;
  private DeliveryCenter deliveryCenter;
  private CustomerNotifier notifier;
  private SAP sap;
  public PaidShoppingCartsBatch(ShoppingCartRepository db,
    ➥ DeliveryCenter deliveryCenter,
                 CustomerNotifier notifier, SAP sap) { 
    this.db = db;
    this.deliveryCenter = deliveryCenter;
    this.notifier = notifier;
    this.sap = sap;
  }
  public void processAll() {
    List<ShoppingCart> paidShoppingCarts = db.cartsPaidToday();
Listing 7.2
PaidShoppingCartsBatch implementation
SMTPEmailSender
EmailService
DeliveryCenter
CartRepository
SAP
SAPSoapWebService
DeliveryCenter
RestApi
CartHibernateDao
ShoppingCart
DeliveryCenter
web service
SAP web
service
SMTP
server
MySQL
database
These are domain objects. They only know about
business. They use the ports whenever they
need something outside their boundaries.
Ports abstract away the
infrastructure details. They
speak “business language.”
Adapters implement the port
interface and handle the
external infrastructure.
PaidShoppingCarts
Batch
Figure 7.2
A concrete implementation of the Hexagonal Architecture (or Ports and Adapters) pattern for the 
shopping carts example
All dependencies are 
injected, which means we 
can pass stubs and mocks 
during testing.


---
**Page 178**

178
CHAPTER 7
Designing for testability
    for (ShoppingCart cart : paidShoppingCarts) { 
      LocalDate estimatedDayOfDelivery = deliveryCenter.deliver(cart); 
      cart.markAsReadyForDelivery(estimatedDayOfDelivery); 
      db.persist(cart);                                    
      notifier.sendEstimatedDeliveryNotification(cart); 
      sap.cartReadyForDelivery(cart);   
    }
  }
}
Look at the class’s four dependencies: ShoppingCartRepository, DeliveryCenter,
CustomerNotifier, and SAP. These are interfaces and, in the Hexagonal Architec-
ture, ports. They establish a protocol for communication between the application
and the external world. These interfaces are completely agnostic of technology and
infrastructure details. In other words, they abstract all the complexity of the infra-
structure away from the domain code. As a result, the interfaces do not depend on
anything strange, such as database or web service classes. They do depend on other
domain classes, such as ShoppingCart, and that is fine. The following listing con-
tains the interface declarations of all the ports.
public interface DeliveryCenter { 
  LocalDate deliver(ShoppingCart cart);
}
public interface CustomerNotifier { 
  void sendEstimatedDeliveryNotification(ShoppingCart cart);
}
public interface SAP {
  void cartReadyForDelivery(ShoppingCart cart);
}
public interface ShoppingCartRepository { 
  List<ShoppingCart> cartsPaidToday();
  void persist(ShoppingCart cart);
}
We are now only missing the implementation of the adapters. This code is out of the
scope of this book, but in terms of implementation, these adapters are classes that
implement the ports’ interfaces. The next listing provides some skeleton code to give
you an idea what the adapters will look like.
Listing 7.3
Interface declarations of all the ports
For each 
paid cart …
… notify
the delivery
system about
the delivery
… mark it 
as ready for 
delivery and 
persist that to 
the database
… send a notification
to the customer
… and notify
the SAP.
The DeliveryCenter interface’s concrete 
implementation will probably consume a very 
complex web service, but the port abstracts 
this away. Ports speak business language and 
do not let infrastructure details leak.
The same thing happens for CustomerNotifier 
and all other interfaces/ports.
This one does not even 
have “database” in the 
name. “Repository” is a 
more business-like term.


---
**Page 179**

179
Separating infrastructure code from domain code
public class DeliveryCenterRestApi implements DeliveryCenter {
  @Override
  public LocalDate deliver(ShoppingCart cart) {
    // all the code required to communicate
    // with the delivery API
    // and returns a LocalDate
  }
}
public class SMTPCustomerNotifier implements CustomerNotifier {
  @Override
  public void sendEstimatedDeliveryNotification(ShoppingCart cart) {
    // all the required code to
    // send an email via SMTP
  }
}
public class SAPSoapWebService implements SAP {
  @Override
  public void cartReadyForDelivery(ShoppingCart cart) {
    // all the code required to send the
    // cart to SAP's SOAP web service
  }
}
public class ShoppingCartHibernateDao
 implements ShoppingCartRepository {
  @Override
  public List<ShoppingCart> cartsPaidToday() {
    // a Hibernate query to get the list of all
    // invoices that were paid today
  }
  @Override
  public void persist(ShoppingCart cart) {
    // a hibernate code to persist the cart
    // in the database
  }
}
Why does this pattern improve testability? If our domain classes depend only on
ports, we can easily exercise all the behavior of the domain logic by stubbing and
mocking the ports. In the PaidShoppingCartsBatch example, we can stub and mock
the ShoppingCartRepository, DeliveryCenter, CustomerNotifier, and SAP ports
and focus on testing the main behavior of the PaidShoppingCartsBatch class.
Again, we do not care if the DeliveryCenter adapter does its job properly. That one
will be exercised in its own test suite.
 Listing 7.5 shows an example test of PaidShoppingCartsBatch. This is a single
test. As a developer, you should apply all the testing techniques and devise several
Listing 7.4
Simplified implementation of the adapters


---
**Page 180**

180
CHAPTER 7
Designing for testability
test cases for any behavior and corner cases you see. Even exceptional behaviors can
be easily exercised.
import static org.mockito.Mockito.*;
@ExtendWith(MockitoExtension.class) 
public class PaidShoppingCartsBatchTest {
  @Mock ShoppingCartRepository db;
  @Mock private DeliveryCenter deliveryCenter;
  @Mock private CustomerNotifier notifier;
  @Mock private SAP sap;
  @Test
  void theWholeProcessHappens() {
    PaidShoppingCartsBatch batch = new PaidShoppingCartsBatch(db,
      ➥ deliveryCenter, notifier, sap);         
    ShoppingCart someCart = spy(new ShoppingCart());   
    LocalDate someDate = LocalDate.now();
    when(db.cartsPaidToday()).thenReturn(Arrays.asList(someCart));
    when(deliveryCenter.deliver(someCart)).thenReturn(someDate);
    batch.processAll();
    verify(deliveryCenter).deliver(someCart); 
    verify(notifier).sendEstimatedDeliveryNotification(someCart);
    verify(db).persist(someCart);
    verify(sap).cartReadyForDelivery(someCart);
    verify(someCart).markAsReadyForDelivery(someDate);
  }
}
Although we only tested the application code, the code from the adapters should also
be tested. The real implementation of the ShoppingCartRepository—let’s call it
ShoppingCartHibernateDao (because it uses the Hibernate framework)—will contain
SQL queries that are complex and prone to bugs, so it deserves a dedicated test suite.
The real SAPSoapWebService class will have complex code to call the SOAP-like web
service and should also be exercised. Those classes require integration testing, follow-
ing our discussion of the testing pyramid in chapter 1. Later in this book, I show how
to write some of those integration tests.
NOTE
Although I could also have mocked the ShoppingCart class, I followed
the advice I gave in chapter 6: do not mock entities unless they are complex. I
preferred to spy on them rather than mock them.
Listing 7.5
Test for PaidShoppingCartsBatchTest, mocking the ports
The @ExtendWith and @Mock 
annotations are extensions provided 
by Mockito. We do not even need to 
write Mockito.mock(…). The framework 
instantiates a mock for us in these fields.
Instantiates the class 
under test and passes the 
mocks as dependencies
The ShoppingCart is a simple entity, so we do not 
need to mock it. Nevertheless, let’s spy on it to 
assert its interactions later.
Verifies that interactions 
with the dependencies 
happened as expected


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


---
**Page 185**

185
Making your classes and methods observable
instance of ShoppingCart is not a mock but a spy. To ensure that the cart was marked as
ready for delivery, we had to spy on the object. Mockito’s API enables us to spy objects
with a single line of code. However, whenever we need a spy to assert the behavior, we
must ask ourselves why we need a spy. Isn’t there an easier way?
 In this particular case, we need to check whether ShoppingCart is marked as ready
for delivery after processing (listing 7.7). We can increase the observability of the
ShoppingCart class (in other words, we can make it simpler to observe the expected
behavior of the shopping cart) by making it provide a method that indicates whether
it is ready for delivery: isReadyForDelivery.
public class ShoppingCart {
    private boolean readyForDelivery = false;
    // more info about the shopping cart...
    public void markAsReadyForDelivery(Calendar estimatedDayOfDelivery) {
        this.readyForDelivery = true;
        // ...
    }
    public boolean isReadyForDelivery() { 
        return readyForDelivery;
    }
}
Because we can now easily ask ShoppingCart whether it is ready for delivery, our test
no longer requires a spy. A vanilla assertion should do. Here is the new test.
@Test
void theWholeProcessHappens() {
  PaidShoppingCartsBatch batch = new PaidShoppingCartsBatch(db,
    ➥ deliveryCenter, notifier, sap);
  ShoppingCart someCart = new ShoppingCart(); 
  assertThat(someCart.isReadyForDelivery()).isFalse();
  Calendar someDate = Calendar.getInstance();
  when(db.cartsPaidToday()).thenReturn(Arrays.asList(someCart));
  when(deliveryCenter.deliver(someCart)).thenReturn(someDate);
  batch.processAll();
  verify(deliveryCenter).deliver(someCart);
  verify(notifier).sendEstimatedDeliveryNotification(someCart);
  verify(db).persist(someCart);
  verify(sap).cartReadyForDelivery(someCart);
  assertThat(someCart.isReadyForDelivery()).isTrue(); 
}
Listing 7.7
Improving the observability of the ShoppingCart class
Listing 7.8
Avoiding the spy when testing PaidShoppingCartsBatch
The new isReadyForDelivery 
method is here to improve 
the observability of the class.
No need for a spy 
anymore, as it is now easy 
to observe the behavior.
Uses a simple vanilla 
assertion instead of a 
Mockito assertion


---
**Page 186**

186
CHAPTER 7
Designing for testability
I urge you not to take this particular code change (the addition of a getter) as the
solution for all observability issues. Rather, abstract away what we did here: we noticed
that asserting that the shopping cart was marked as ready for delivery was not straight-
forward, as it required a spy. We then re-evaluated our code and looked for a simple
way to let the test know that the shopping cart was marked as ready for delivery. In this
case, a getter was the easy implementation. 
7.3.2
Example 2: Observing the behavior of void methods
When a method returns an object, it is natural to think that assertions will check
whether the returned object is as expected. However, this does not happen naturally
in void methods. If your method does not return anything, what will you assert? It is
even more complicated if what you need to assert stays within the method. As an
example, the following method creates a set of Installments based on a Shopping-
Cart.
public class InstallmentGenerator {
  private InstallmentRepository repository;
  public InstallmentGenerator(InstallmentRepository repository) { 
    this.repository = repository;
  }
  public void generateInstallments(ShoppingCart cart,
    ➥ int numberOfInstallments) {
    LocalDate nextInstallmentDueDate = LocalDate.now(); 
    double amountPerInstallment = cart.getValue() / numberOfInstallments; 
    for(int i = 1; i <= numberOfInstallments; i++) { 
      nextInstallmentDueDate =
        nextInstallmentDueDate.plusMonths(1);   
      Installment newInstallment =
        new Installment(nextInstallmentDueDate, amountPerInstallment);
      repository.persist(newInstallment); 
    }
  }
}
To test this method, we need to check whether the newly created Installments are set
with the right value and date. The question is, how can we get the Installments eas-
ily? The Installment classes are instantiated within the method and sent to the repos-
itory for persistence, and that is it. If you know Mockito well, you know there is a way
to get all the instances passed to a mock: an ArgumentCaptor. The overall idea is that
we ask the mock, “Can you give me all the instances passed to you during the test?” We
Listing 7.9
InstallmentGenerator 
We can inject a stub of
InstallmentRepository.
Creates a variable to store the
last installment date
Calculates the
amount per
installment
Creates a sequence 
of installments, one 
month apart
Adds 1 to
the month
Creates and persists 
the installment


---
**Page 187**

187
Making your classes and methods observable
then make assertions about them. In this case, we can ask the repository mock
whether all the Installments were passed to the persist method.
 The test in listing 7.10 creates a shopping cart with value 100 and asks the genera-
tor for 10 installments. Therefore, it should create 10 installments of 10.0 each. That is
what we want to assert. After the method under test is executed, we collect all the install-
ments using an ArgumentCaptor. See the calls for capture() and getAllValues(). With
the list available, we use traditional AssertJ assertions.
public class InstallmentGeneratorTest {
    @Mock private InstallmentRepository repository; 
    @Test
    void checkInstallments() {
      InstallmentGenerator generator =
        new InstallmentGenerator(repository); 
      ShoppingCart cart = new ShoppingCart(100.0);
      generator.generateInstallments(cart, 10); 
      ArgumentCaptor<Installment> captor =
        ArgumentCaptor.forClass(Installment.class); 
      verify(repository,times(10)).persist(captor.capture());     
      List<Installment> allInstallments = captor.getAllValues();  
      assertThat(allInstallments)
          .hasSize(10)
          .allMatch(i -> i.getValue() == 10); 
      for(int month = 1; month <= 10; month++) { 
        final LocalDate dueDate = LocalDate.now().plusMonths(month);
        assertThat(allInstallments)
            .anyMatch(i -> i.getDate().equals(dueDate));
      }
    }
}
The ArgumentCaptor makes writing the test possible. ArgumentCaptors are handy
whenever we test methods that return void.
 If we apply the idea of simplicity, you may wonder if there is a way to avoid the
ArgumentCaptor. It would be much simpler if there were a “get all generated install-
ments” method. If we make the generateInstallments method return the list of all
newly generated Installments, the test becomes even simpler. The change required
in InstallmentGenerator is small: as all we need to do is keep track of the install-
ments in a list. The following listing shows the new implementation.
Listing 7.10
Tests for InstallmentGenerator using ArgumentCaptor
Creates a mock of 
the repository
Instantiates the class
under test, passing the
mock as a dependency
Calls the method 
under test. Note that 
the method returns 
void, so we need 
something smarter to 
assert its behavior.
Creates an
ArgumentCaptor
Using the captor, we
get all the installments
passed to the repository.
Asserts that the installments 
are correct. All of them should 
have a value of 10.0.
Also asserts that
the installments
should be one
month apart


---
**Page 188**

188
CHAPTER 7
Designing for testability
public List<Installment> generateInstallments(ShoppingCart cart,
  ➥ int numberOfInstallments) {
  List<Installment> generatedInstallments = new ArrayList<Installment>(); 
  LocalDate nextInstallmentDueDate = LocalDate.now();
  double amountPerInstallment = cart.getValue() / numberOfInstallments;
  for(int i = 1; i <= numberOfInstallments; i++) {
    nextInstallmentDueDate = nextInstallmentDueDate.plusMonths(1);
    Installment newInstallment =
      new Installment(nextInstallmentDueDate, amountPerInstallment);
    repository.persist(newInstallment);
    generatedInstallments.add(newInstallment); 
  }
  return generatedInstallments; 
}
Now we can avoid the ArgumentCaptor completely in the test code.
public class InstallmentGeneratorTest {
    @Mock
    private InstallmentRepository repository;
    @Test
    void checkInstallments() {
      ShoppingCart cart = new ShoppingCart(100.0);
      InstallmentGenerator generator =
        new InstallmentGenerator(repository);
      List<Installment> allInstallments =
        generator.generateInstallments(cart, 10); 
      assertThat(allInstallments)
          .hasSize(10)
          .allMatch(i -> i.getValue() == 10); 
      for(int month = 1; month <= 10; month++) {
        final LocalDate dueDate = LocalDate.now().plusMonths(month);
        assertThat(allInstallments)
            .anyMatch(i -> i.getDate().equals(dueDate));
      }
    }
}
Listing 7.11
InstallmentGenerator returning the list of installments
Listing 7.12
InstallmentGeneratorTest without the ArgumentCaptor
Creates a
list that will
keep track
of all the
generated
installments
Stores each of 
the generated 
installments
Returns the list 
of installments
The method under 
test returns the list of 
installments. No need 
for ArgumentCaptor.
Same assertions 
as before


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


---
**Page 193**

193
Designing for testability in the real world
roles and move each calculation rule to its own class. Google the Strategy
design pattern to see code examples. 
7.5.2
The coupling of the class under test
In a world of cohesive classes, we combine different classes to build large behaviors.
But doing so may lead to a highly coupled design. Excessive coupling may harm evolu-
tion, as changes in one class may propagate to other classes in ways that are not clear.
Therefore, we should strive for classes that are coupled as little as possible.
 Your test code can help you detect highly coupled classes:
If the production class requires you to instantiate many dependencies in your
test code, this may be a sign. Consider redesigning the class. There are different
refactoring strategies you can employ. Maybe the large behavior that the class
implements can be broken into two steps.
– Sometimes coupling is unavoidable, and the best we can do is manage it bet-
ter. Breaking a class enables developers to test it more easily. I will give more
concrete examples of such cases in the following chapters.
Another sign is if you observe a test failing in class ATest (supposedly testing the
behavior of class A), but when you debug it, you find the problem in class B. This
is a clear issue with dependencies: a problem in class B somehow leaked to class A.
It is time to re-evaluate how these classes are coupled and how they interact and
see if such leakages can be prevented in future versions of the system. 
7.5.3
Complex conditions and testability
We have seen in previous chapters that very complex conditions (such as an if state-
ment composed of multiple boolean operations) require considerable effort from tes-
ters. For example, we may devise too many tests after applying boundary testing or
condition + branch coverage criteria. Reducing the complexity of such conditions by,
for example, breaking them into multiple smaller conditions will not reduce the over-
all complexity of the problem but will at least spread it out. 
7.5.4
Private methods and testability
A common question among developers is whether to test private methods. In princi-
ple, testers should test private methods only through their public methods. However,
testers often feel the urge to test a particular private method in isolation.
 A common reason for this feeling is the lack of cohesion or the complexity of the
private method. In other words, this method does something so different from the
public method, and/or its task is so complicated, that it must be tested separately. This
is a good example of the test speaking to us. In terms of design, this may mean the pri-
vate method does not belong in its current place. A common refactoring is to extract
the method, perhaps to a brand new class. There, the former private method, now a
public method, can be tested normally. The original class, where the private method
used to be, should now depend on this new class. 


---
**Page 194**

194
CHAPTER 7
Designing for testability
7.5.5
Static methods, singletons, and testability
As we have seen, static methods adversely affect testability. Therefore, a good rule of
thumb is to avoid creating static methods whenever possible. Exceptions to this rule are
utility methods, which are often not mocked. If your system has to depend on a specific
static method, perhaps because it comes with the framework your software depends on,
adding an abstraction on top of it—similar to what we did with the LocalDate class in
the previous chapter—may be a good decision to facilitate testability.
 The same recommendation applies when your system needs code from others or
external dependencies. Again, creating layers and classes that abstract away the
dependency may help you increase testability. Don’t be afraid to create these extra lay-
ers: although it may seem that they will increase the overall complexity of the design,
the increased testability pays off.
 Using the Singleton design pattern also harms testability. This approach ensures
that there is only one instance of a class throughout the entire system. Whenever you
need an instance of that class, you ask the singleton, and the singleton returns the
same one. A singleton makes testing difficult because it is like having a global variable
that is persistent throughout the program’s life cycle. When testing software systems
that use singletons, we often have to write extra code in the test suite to reset or
replace the singleton in the different test cases. Singletons also bring other disadvan-
tages to maintainability in general. If you are not familiar with this pattern, I suggest
reading about it. 
7.5.6
The Hexagonal Architecture and mocks as a design technique
Now that you know about the Hexagonal Architecture and the idea of ports and
adapters, we can talk about mocks as a design technique. In a nutshell, whenever
mockists develop a feature (or a domain object) and notice that they need something
from another place, they let a port emerge. As we saw, the port is an interface that
allows the mockist to develop the remainder of the feature without being bothered by
the concrete implementation of the adapter. The mockist takes this as a design activ-
ity: they reflect on the contract that the port should offer to the core of the applica-
tion and model the best interface possible.
 Whenever I am coding a class (or set of classes) and notice that I need something
else, I let an interface emerge that represents this “something else.” I reflect on what the
class under development needs from it, model the best interface, and continue develop-
ing the class. Only later do I implement the concrete adapter. I enjoy this approach as it
lets me focus on the class I am implementing by giving me a way to abstract things that I
do not care about right now, like the implementation of adapters. 
 
 


---
**Page 195**

195
Exercises
7.5.7
Further reading about designing for testability
Entire books can be written about this topic. In fact, entire books have been written
about it:
Michael Feathers’s Working Effectively with Legacy Code (2004) is about working
with legacy systems, but a huge part of it is about untestable code (common in
legacy) and how to make it testable. Feathers also has a nice talk on YouTube
about the “deep synergy between well-designed production code and testabil-
ity,” as he calls it (2013).
Steve Freeman and Nat Pryce’s book Growing-Object Oriented Systems Guided by
Tests (2009) is also a primer for writing classes that are easy to test.
Robert Martin’s Clean Architecture ideas (2018) align with the ideas discussed here. 
Exercises
7.1
Observability and controllability are two important concepts of software testing.
Three developers could benefit from improving either the observability or the
controllability of the system/class they are testing, but each developer encoun-
ters a problem.
State whether each of the problems relates to observability or controllability.
A Developer 1: “I can’t assert whether the method under test worked well.”
B Developer 2: “I need to make sure this class starts with a boolean set to
false, but I can’t do it.”
C Developer 3: “I instantiated the mock object, but there’s no way to inject it
into the class.”
7.2
Sarah has joined a mobile app team that has been trying to write automated
tests for a while. The team wants to write unit tests for part of their code, but
they tell Sarah, “It’s hard.” After some code review, the developers list the fol-
lowing problems in their code base:
A Many classes mix infrastructure and business rules.
B The database has large tables and no indexes.
C There are lots of calls to libraries and external APIs.
D Some classes have too many attributes/fields.
To increase testability, the team has a budget to work on two of these four
issues. Which items should Sarah recommend that they tackle first?
Note: All four issues should be fixed, but try to prioritize the two most
important ones. Which influences testability the most?
7.3
How can you improve the testability of the following OrderDeliveryBatch class?
public class OrderDeliveryBatch {
  public void runBatch() {


---
**Page 196**

196
CHAPTER 7
Designing for testability
    OrderDao dao = new OrderDao();
    DeliveryStartProcess delivery = new DeliveryStartProcess();
    List<Order> orders = dao.paidButNotDelivered();
    for (Order order : orders) {
      delivery.start(order);
      if (order.isInternational()) {
        order.setDeliveryDate("5 days from now");
      } else {
        order.setDeliveryDate("2 days from now");
      }
    }
  }
}
class OrderDao {
  // accesses a database
}
class DeliveryStartProcess {
  // communicates with a third-party web service
}
7.4
Consider the KingsDayDiscount class below:
public class KingsDayDiscount {
  public double discount(double value) {
    Calendar today = Calendar.getInstance();
    boolean isKingsDay = today.get(MONTH) == Calendar.APRIL
        && today.get(DAY_OF_MONTH) == 27;
    return isKingsDay ? value * 0.15 : 0;
  }
}
What would you do to make this class more testable?
7.5
Think about your current project. Are parts of it hard to test? Can you explain
why? What can you do to make it more testable?
Summary
Writing tests can be easy or hard. Untestable code makes our lives harder. Strive
for code that is easy (or at least easier) to test.
Separate infrastructure from domain code. Infrastructure makes it harder to
write tests. Separating domain from infrastructure enables us to write unit tests
for the domain logic much more cheaply.


---
**Page 197**

197
Summary
Ensure that classes are easily controllable and observable. Controllability is usu-
ally achieved by ensuring that we can control the dependencies of the class
under test. Observability is achieved by ensuring that the class provides easy
ways for the test to assert expected behavior.
While you should not change your code in ways you do not believe in, you
should also be pragmatic. I am all in favor of changing the production code to
facilitate testing.


---
**Page 198**

198
Test-driven development
Software developers are pretty used to the traditional development process. First,
they implement. Then, and only then, they test. But why not do it the other way
around? In other words, why not write a test first and then implement the produc-
tion code?
 In this chapter, we discuss this well-known approach: test-driven development (TDD).
In a nutshell, TDD challenges our traditional way of coding, which has always been
“write some code and then test it.” With TDD, we start by writing a test representing
the next small feature we want to implement. This test naturally fails, as the feature
has not yet been implemented! We then make the test pass by writing some code.
With the test now green, and knowing that the feature has been implemented, we
go back to the code we wrote and refactor it.
 TDD is a popular practice, especially among Agile practitioners. Before I dive
into the advantages of TDD and pragmatic questions about working this way, let’s
look at a small example.
This chapter covers
Understanding test-driven development
Being productive with TDD
When not to use TDD



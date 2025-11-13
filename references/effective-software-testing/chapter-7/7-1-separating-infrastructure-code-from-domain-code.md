# 7.1 Separating infrastructure code from domain code (pp.173-181)

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



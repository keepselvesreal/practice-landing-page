# 6.2.1 Stubbing dependencies (pp.145-150)

---
**Page 145**

145
An introduction to mocking frameworks
 Spies are used in very specific contexts, such as when it is much easier to use the
real implementation than a mock but you still want to assert how the method under
test interacts with the dependency. Spies are less common in the wild. 
6.2
An introduction to mocking frameworks
Mocking frameworks are available for virtually all programming languages. While they
may differ in their APIs, the underlying idea is the same. Here, I will use Mockito
(https://site.mockito.org), one of the most popular stubbing and mocking libraries
for Java. Mockito offers a simple API, enabling developers to set up stubs and define
expectations in mock objects with just a few lines of code. (Mockito is an extensive
framework, and we cover only part of it in this chapter. To learn more, take a look at
its documentation.)
 Mockito is so simple that knowing the following three methods is often enough:

mock(<class>)—Creates a mock object/stub of a given class. The class can be
specified by <ClassName>.class.

when(<mock>.<method>).thenReturn(<value>)—A chain of method calls that
defines the (stubbed) behavior of the method. In this case <value> is returned.
For example, to make the all method of an issuedInvoices mock return a list
of invoices, we write when(issuedInvoices.all()).thenReturn(someList-
Here).

verify(<mock>).<method>—Asserts that the interactions with the mock object
happened in the expected way. For example, if we want to ensure that the
method all of an issuedInvoices mock was invoked, we use verify(issued-
Invoices).all().
Let’s dive into concrete examples to illustrate Mockito’s main features and show you
how developers use mocking frameworks in practice. If you are already familiar with
Mockito, you can skip this section.
6.2.1
Stubbing dependencies
Let’s learn how to use Mockito and set up stubs with a practical example. Suppose we
have the following requirement:
The program must return all the issued invoices with values smaller than 100.
The collection of invoices can be found in our database. The class Issued-
Invoices already contains a method that retrieves all the invoices.
The code in listing 6.1 is a possible implementation of this requirement. Note that
IssuedInvoices is a class responsible for retrieving all the invoices from a real data-
base (for example, MySQL). For now, suppose it has a method all() (not shown) that
returns all the invoices in the database. The class sends SQL queries to the database
and returns invoices. You can check the (naive) implementation in the book’s code
repository.


---
**Page 146**

146
CHAPTER 6
Test doubles and mocks
import java.util.List;
import static java.util.stream.Collectors.toList;
public class InvoiceFilter {
  public List<Invoice> lowValueInvoices() {
    DatabaseConnection dbConnection = new DatabaseConnection();        
    IssuedInvoices issuedInvoices = new IssuedInvoices(dbConnection);  
    try {
      List<Invoice> all = issuedInvoices.all();   
      return all.stream()
              .filter(invoice -> invoice.getValue() < 100)
              .collect(toList());       
    } finally {
      dbConnection.close();   
    }
  }
}
Without stubbing the IssuedInvoices class, testing the InvoiceFilter class means
having to set up a database. It also means having invoices in the database so the SQL
query can return them. This is a lot of work, as you can see from the (simplified) test
method in listing 6.2, which exercises InvoiceFilter together with the concrete
IssuedInvoices class and the database. Because the tests need a populated database
up and running, we first create a connection to the database and clean up any old
data it may contain. Then, in the test method, we persist a set of invoices to the data-
base. Finally, when the test is over, we close the connection with the database, as we do
not want hanging connections.
public class InvoiceFilterTest {
  private IssuedInvoices invoices;
  private DatabaseConnection dbConnection;
  @BeforeEach         
  public void open() {
    dbConnection = new DatabaseConnection();
    invoices = new IssuedInvoices(dbConnection);
    dbConnection.resetDatabase();    
  }
  @AfterEach             
  public void close() {
    if (dbConnection != null)
Listing 6.1
InvoiceFilter class
Listing 6.2
Tests for InvoiceFilter
Instantiates the IssuedInvoices
dependency. It needs a
DatabaseConnection, so we
also instantiate one of those.
Gets all the invoices 
from the database
Picks all the invoices with 
a value smaller than 100
Closes the connection with the database. You would 
probably handle it better, but this is here to remind 
you of all the things you need to handle when dealing 
with databases.
BeforeEach methods are executed 
before every test method.
Cleans up the tables to make sure 
old data in the database does not 
interfere with the test
AfterEach methods are 
executed after every 
test method.


---
**Page 147**

147
An introduction to mocking frameworks
      dbConnection.close();   
  }
  @Test
  void filterInvoices() {
    Invoice mauricio = new Invoice("Mauricio", 20);  
    Invoice steve = new Invoice("Steve", 99);  
    Invoice frank = new Invoice("Frank", 100); 
    invoices.save(mauricio);       
    invoices.save(steve);          
    invoices.save(frank);          
    InvoiceFilter filter = new InvoiceFilter();   
    assertThat(filter.lowValueInvoices())
        .containsExactlyInAnyOrder(mauricio, steve);    
  }
}
NOTE
Did you notice the assertThat…containsExactlyInAnyOrder asser-
tion? This ensures that the list contains exactly the objects we pass, in any
order. Such assertions do not come with JUnit 5. Without AssertJ, we would
have to write a lot of code for that assertion to happen. You should get famil-
iar with AssertJ’s assertions; they are handy.
This is a small example. Imagine a larger business class with a much more complex
database structure. Imagine that instead of persisting a bunch of invoices, you need to
persist invoices, customers, items, shopping carts, products, and so on. This can
become tedious and expensive.
 Let’s rewrite the test. This time we will stub the IssuedInvoices class and avoid the
hassle with the database. First, we need a way to inject the InvoiceFilter stub into
the class under test. Its current implementation creates an instance of Issued-
Invoices internally (see the first lines in the lowValueInvoices method). This means
there is no way for this class to use the stub during the test: whenever this method is
invoked, it instantiates the concrete database-dependent class.
 We must change our production code to make testing easier (get used to the idea
of changing the production code to facilitate testing). The most direct way to do this
is to have IssuedInvoices passed in as an explicit dependency through the class
constructor, as shown in listing 6.3. The class no longer instantiates the Database-
Connection and IssuedInvoices classes. Rather, it receives IssuedInvoices via con-
structor. Note that there is no need for the DatabaseConnection class to be injected,
as InvoiceFilter does not need it. This is good: the less we need to do in our test
code, the better. The new implementation works for both our tests (because we can
inject an IssueInvoices stub) and production (because we can inject the concrete
IssueInvoices, which will go to the database, as we expect in production).
 
 
Closes the database 
connection after every test
Creates in-memory 
invoices as we have 
been doing so far
99 and 100,
boundary
testing!
However, we must persist 
them in the database!
Instantiates 
InvoiceFilter, knowing 
it will connect to the 
database
Asserts that the method 
only returns the low-
value invoices


---
**Page 148**

148
CHAPTER 6
Test doubles and mocks
public class InvoiceFilter {
  private final IssuedInvoices issuedInvoices;   
  public InvoiceFilter(IssuedInvoices issuedInvoices) {   
    this.issuedInvoices = issuedInvoices;
  }
  public List<Invoice> lowValueInvoices() {
    List<Invoice> all = issuedInvoices.all();   
    return all.stream()
        .filter(invoice -> invoice.getValue() < 100)
        .collect(toList());
  }
}
Let’s change our focus to the unit test of InvoiceFilter. The test is very similar to the
one we wrote earlier, but now we do not handle the database. Instead, we configure
the IssuedInvoices stub as shown in the next listing. Note how easy it is to write this
test: full control over the stub enables us to try different cases (even exceptional ones)
quickly.
public class InvoiceFilterTest {
  @Test
  void filterInvoices() {
    IssuedInvoices issuedInvoices = mock(IssuedInvoices.class);   
    Invoice mauricio = new Invoice("Mauricio", 20);   
    Invoice steve = new Invoice("Steve", 99);         
    Invoice frank = new Invoice("Frank", 100);        
    List<Invoice> listOfInvoices = Arrays.asList(mauricio, steve, frank);
    when(issuedInvoices.all()).thenReturn(listOfInvoices);   
    InvoiceFilter filter = new InvoiceFilter(issuedInvoices);   
    assertThat(filter.lowValueInvoices())
        .containsExactlyInAnyOrder(mauricio, steve);   
  }
}
NOTE
This idea of classes not instantiating their dependencies by themselves
but instead receiving them is a popular design technique. It allows us to inject
mocks and also makes the production code more flexible. This idea is also
Listing 6.3
InvoiceFilter class receiving IssueInvoices via constructor
Listing 6.4
Tests for InvoiceFilter, stubbing IssuedInvoices
Creates a field in the 
class to store the 
dependency
IssuedInvoices 
is now passed in 
the constructor.
We no longer instantiate 
the IssuedInvoices database 
class. We received it as a 
dependency, and we use it.
Instantiates a stub for the
IssuedInvoices class, using
Mockito’s mock method
Creates invoices as 
we did before
Makes the
stub return the
predefined list
of invoices if
all() is called
Instantiates the class under test,
and passes the stub as a dependency
(instead of the concrete database class)
Asserts that the behavior is as expected


---
**Page 149**

149
An introduction to mocking frameworks
known as dependency injection. If you want to dive into the topic, I suggest
Dependency Injection: Principles, Practices, and Patterns by Steven van Deursen
and Mark Seemann (2019).
Note how we set up the stub using Mockito’s when() method. In this example, we tell
the stub to return a list containing mauricio, frank, and steve, the three invoices
we instantiate as part of the test case. The test then invokes the method under test,
filter.lowValueInvoices(). Consequently, the method under test invokes issued-
Invoices.all(). However, at this point, issuedInvoices is a stub that returns the list
with the three invoices. The method under test continues its execution and returns a
new list with only the two invoices that are below 100, causing the assertion to pass.
 Besides making the test easier to write, stubs also made the test class more cohesive
and less prone to change if something other than InvoiceFilter changes. If Issued-
Invoices changes—or, more specifically, if its contracts change—we may have to
propagate it to the tests of InvoiceFilter, too. Our discussion of contracts in chap-
ter 4 also makes sense when talking about mocks. Now InvoiceFilterTest only tests
the InvoiceFilter class. It does not test the IssuedInvoices class. IssuedInvoices
deserves to be tested, but in another place, using an integration test (which we’ll dis-
cuss in chapter 9).
 A cohesive test also has fewer chances of failing for another reason. In the old ver-
sion, the filterInvoices test could fail because of a bug in the InvoiceFilter class
or a bug in the IssuedInvoices class (imagine a bug in the SQL query that retrieves
the invoices from the database). The new tests can only fail because of a bug in
InvoiceFilter, never because of IssuedInvoices. This is handy, as a developer will
spend less time debugging if this test fails. Our new approach for testing Invoice-
Filter is faster, easier to write, and more cohesive.
NOTE
This part of the book does not focus on systematic testing. But that is
what you should do, regardless of whether you are using mocks. Look at the
filterInvoices test method. Its goal is to filter invoices that are below 100.
In our (currently only) test case, we ensure that this works, and we even
exercise the 100 boundary. You may want to exercise other cases, such as
empty lists, or lists with a single element, or other test cases that emerge
during specification-based and structural testing. I don’t do that in this
chapter, but you should remember all the techniques discussed in the previ-
ous chapters.
In a real software system, the business rule implemented by InvoiceFilter would
probably be best executed in the database. A simple SQL query would do the job
with a much better performance. Try to abstract away from this simple example:
whenever you have a dependency that is expensive to use during testing, stubs may
come in handy. 


---
**Page 150**

150
CHAPTER 6
Test doubles and mocks
6.2.2
Mocks and expectations
Next, let’s discuss mocks. Suppose our current system has a new requirement:
All low-valued invoices should be sent to our SAP system (a software that man-
ages business operations). SAP offers a sendInvoice web service that receives
invoices.
You know you probably want to test the new class without depending on a real full-
blown SAP web service. So, the SAPInvoiceSender class (which contains the main
logic of the feature) receives, via its constructor, a class that communicates with SAP.
For simplicity, suppose there is a SAP interface. The SAPInvoiceSender’s main method,
sendLowValuedInvoices, gets all the low-valued invoices using the InvoiceFilter
class discussed in the previous section and then passes the resulting invoices to SAP.
public interface SAP {   
  void send(Invoice invoice);
}
public class SAPInvoiceSender {
  private final InvoiceFilter filter;  
  private final SAP sap;               
  public SAPInvoiceSender(InvoiceFilter filter, SAP sap) {  
    this.filter = filter;
    this.sap = sap;
  }
  public void sendLowValuedInvoices() {  
    List<Invoice> lowValuedInvoices = filter.lowValueInvoices();
    for(Invoice invoice : lowValuedInvoices) {
      sap.send(invoice);
    }
  }
}
Let’s test the SAPInvoiceSender class (see listing 6.6 for the implementation of the
test suite). For this test, we stub the InvoiceFilter class. For SAPInvoiceSender,
InvoiceFilter is a class that returns a list of invoices. It is not the goal of the current
test to test InvoiceFilter, so we should stub this class to facilitate testing the method
we do want to test. The stub returns a list of low-valued invoices.
 The main purpose of this test is to ensure that every low-valued invoice is sent to
SAP. How can we assert that this is happening without having the real SAP? It is sim-
ple: we ensure that the call to SAP’s send() method happened. How do we do that?
 Mockito, behind the scenes, records all the interactions with its mocks. This means
if we mock the SAP interface and pass it to the class under test, at the end of the test,
Listing 6.5
SAPInvoiceSender class
This interface encapsulates the communication 
with SAP. Note that it does not matter how the 
concrete implementation will work.
We have fields for both the 
required dependencies.
The two
dependencies
are required
by the
constructor
of the class.
The logic of the method is straightforward. 
We first get the low-value invoices from 
the InvoiceFilter. Then we pass each of 
them to SAP.



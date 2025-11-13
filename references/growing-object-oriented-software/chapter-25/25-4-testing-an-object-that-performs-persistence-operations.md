# 25.4 Testing an Object That Performs Persistence Operations (pp.294-297)

---
**Page 294**

The techniques we describe in this chapter are compatible with this kind of
framework.We have used them to test applications built within Java EE and Spring,
and with “plain old” Java programs that use JPA, Hibernate, or JDBC directly.
The frameworks wrap transaction management around the objects that make
use of transactional resources, so there’s nothing in their code to mark the appli-
cation’s transaction boundaries. The tests for those objects, however, need to
manage transactions explicitly—which is what a transactor is for.
In the tests, the transactor uses the same transaction manager as the application,
conﬁgured in the same way. This ensures that the tests and the full application
run the same transactional code. It should make no difference whether a trans-
action is controlled by a block wrapped around our code by the framework, or by
a transactor in our tests. But if we’ve made a mistake and it does make a difference,
our end-to-end tests should catch such failures by exercising the application code
in the container.
Testing an Object That Performs Persistence Operations
Now that we’ve got some test scaffolding we can write tests for an object that
performs persistence.
In our domain model, a customer base represents all the customers we know
about. We can add customers to our customer base and ﬁnd customers that match
certain criteria. For example, we need to ﬁnd customers with credit cards that
are about to expire so that we can send them a reminder to update their payment
details.
public interface CustomerBase {  […]
  void addCustomer(Customer customer);
  List<Customer> customersWithExpiredCreditCardsAt(Date deadline);
}
When unit-testing code that calls a CustomerBase to ﬁnd and notify the
relevant customers, we can mock the interface. In a deployed system, however,
this code will call a real implementation of CustomerBase that is backed by JPA
to save and load customer information from a database. We must also test that
this persistent implementation works correctly—that the queries it makes and
the object/relational mappings are correct. For example, below is a test of the
customersWithExpiredCreditCardsAt() query. There are two helper methods
that interact with customerBase within a transaction: addCustomer() adds a set
of example customers, and assertCustomersExpiringOn() queries for customers
with expired cards.
Chapter 25
Testing Persistence
294


---
**Page 295**

public class PersistentCustomerBaseTest { […]
  final PersistentCustomerBase customerBase = 
                                 new PersistentCustomerBase(entityManager);
  @Test
  @SuppressWarnings("unchecked")
  public void findsCustomersWithCreditCardsThatAreAboutToExpire() throws Exception {
    final String deadline = "6 Jun 2009";
    addCustomers(
      aCustomer().withName("Alice (Expired)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date("1 Jan 2009"))),
      aCustomer().withName("Bob (Expired)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date("5 Jun 2009"))),
      aCustomer().withName("Carol (Valid)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date(deadline))),
      aCustomer().withName("Dave (Valid)")
        .withPaymentMethods(aCreditCard().withExpiryDate(date("7 Jun 2009")))
    );
    assertCustomersExpiringOn(date(deadline), 
                              containsInAnyOrder(customerNamed("Alice (Expired)"), 
                                                 customerNamed("Bob (Expired)")));
  }
  private void addCustomers(final CustomerBuilder... customers) throws Exception {
transactor.perform(new UnitOfWork() {
      public void work() throws Exception {
        for (CustomerBuilder customer : customers) { 
customerBase.addCustomer(customer.build());
        }
      }
    });
  }
  private void assertCustomersExpiringOn(final Date date, 
                                         final Matcher<Iterable<Customer>> matcher)
    throws Exception 
  {
transactor.perform(new UnitOfWork() {
      public void work() throws Exception {
        assertThat(customerBase.customersWithExpiredCreditCardsAsOf(date), matcher);
      }
    });
  }
}
We call addCustomers() with CustomerBuilders set up to include a name and
an expiry date for the credit card. The expiry date is the signiﬁcant ﬁeld for this
test, so we create customers with expiry dates before, on, and after the deadline to
demonstrate the boundary condition. We also set the name of each customer
to identify the instances in a failure (notice that the names self-describe the relevant
status of each customer). An alternative to matching on name would have been
to use each object’s persistence identiﬁer, which is assigned by JPA. That would
have been more complex to work with (it’s not exposed as a property on
Customer), and would not be self-describing.
295
Testing an Object That Performs Persistence Operations


---
**Page 296**

The assertCustomersExpiringOn() method runs the query we’re testing for
the given deadline and checks that the result conforms to the Hamcrest matcher
we pass in. The containsInAnyOrder() method returns a matcher that checks
that there’s a sub-matcher for each of the elements in a collection. We’ve written
a customerNamed() method to return a custom matcher that tests whether an
object is a Customer with a given name (there’s more on custom matchers in
Appendix B). So, this test says that we expect to receive back exactly two Customer
objects, named "Alice (Expired)" and "Bob (Expired)".
The test implicitly exercises CustomerBase.addCustomer() by calling it to set
up the database for the query. Thinking further, what we actually care about is
the relationship between the result of calling addCustomer() and subsequent
queries, so we probably won’t test addCustomer() independently. If there’s an
effect of addCustomer() that is not visible through some feature of the system,
then we’d have to ask some hard questions about its purpose before writing a
special test query to cover it.
Better Test Structure with Matchers
This test includes a nice example of using Hamcrest to create a clean test structure.
The test method constructs a matcher, which gives a concise description of a valid
result for the query. It passes the matcher to assertCustomersExpiringOn(),
which just runs the query and passes the result to the matcher. We have a clean
separation between the test method, which knows what is expected to be retrieved,
and the query/assert method, which knows how to make a query and can be used
in other tests.
Here is an implementation of PersistentCustomerBase that passes the test:
public class PersistentCustomerBase implements CustomerBase {
  private final EntityManager entityManager;
  public PersistentCustomerBase(EntityManager entityManager) {
    this.entityManager = entityManager;
  }
  public void addCustomer(Customer customer) {
    entityManager.persist(customer);
  }
  public List<Customer> customersWithExpiredCreditCardsAt(Date deadline) {
    Query query = entityManager.createQuery(
        "select c from Customer c, CreditCardDetails d " +
        "where d member of c.paymentMethods " +
        "  and d.expiryDate < :deadline");
    query.setParameter("deadline", deadline);
    return query.getResultList();
  }
}
Chapter 25
Testing Persistence
296


---
**Page 297**

This implementation looks trivial—it’s so much shorter than its test—but it
relies on a lot of XML conﬁguration that we haven’t included and on a third-party
framework that implements the EntityManager’s simple API.
On Patterns and Type Names
The CustomerBase interface and PersistentCustomerBase class implement the
repository or data access object pattern (often abbreviated to DAO).We have not
used the terms “Repository,” “DataAccessObject,” or “DAO” in the name of the
interface or class that implements it because:
•
Using such terms leaks knowledge about the underlying technology layers
(persistence) into the application domain, and so breaks the “ports and
adapters” architecture.The objects that use a CustomerBase are persistence-
agnostic: they do not care whether the Customer objects they interact with
are written to disk or not.The Customer objects are also persistence-agnostic:
a program does not need to have a database to create and use Customer
objects. Only PersistentCustomerBase knows how it maps Customer objects
in and out of persistent storage.
•
We prefer not to name classes or interfaces after patterns; what matters
to us is their relationship to other classes in the system. The clients of
CustomerBase do not care what patterns it uses. As the system evolves, we
might make the CustomerBase class work in some other way and the name
would then be misleading.
•
We avoid generic words like “data,” “object,” or “access” in type names.We
try to give each class a name that identiﬁes a concept within its domain or
expresses how it bridges between the application and technical domains.
Testing That Objects Can Be Persisted
The PersistentCustomerBase relies on so much conﬁguration and underlying
third-party code that the error messages from its test can be difﬁcult to diagnose.
A test failure could be caused by a defect in a query, the mapping of the Customer
class, the mapping of any of the classes that it uses, the conﬁguration of the ORM,
invalid database connection parameters, or a misconﬁguration of the database
itself.
We can write more tests to help us pinpoint the cause of a persistence failure
when it occurs. A useful test is to “round-trip” instances of all persistent entity
types through the database to check that the mappings are conﬁgured correctly
for each class.
Round-trip tests are useful whenever we reﬂectively translate objects to and
from other forms. Many serialization and mapping technologies have the same
advantages and difﬁculties as ORM. The mapping can be deﬁned by compact,
297
Testing That Objects Can Be Persisted



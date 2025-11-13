# 25.3 Make Tests Transaction Boundaries Explicit (pp.292-294)

---
**Page 292**

We use an array, ENTITY_TYPES, to ensure that the entity types (and, therefore,
database tables) are cleaned in an order that does not violate referential integrity
when rows are deleted from the database.3 We add DatabaseCleaner to a setup
method, to initialize the database before each test. For example:
public class ExamplePersistenceTest {
  final EntityManagerFactory factory = 
                                Persistence.createEntityManagerFactory("example");
  final EntityManager entityManager = factory.createEntityManager();
  @Before
  public void cleanDatabase() throws Exception {
new DatabaseCleaner(entityManager).clean();
  }
[…]
}
For brevity, we won’t show this cleanup in the test examples. You should assume
that every persistence test starts with the database in a known, clean state.
Make Tests Transaction Boundaries Explicit
A common technique to isolate tests that use a transactional resource (such as a
database) is to run each test in a transaction which is then rolled back at the end
of the test. The idea is to leave the persistent state the same after the test as before.
The problem with this technique is that it doesn’t test what happens on commit,
which is a signiﬁcant event. The ORM ﬂushes the state of the objects it is man-
aging in memory to the database. The database, in turn, checks its integrity
constraints. A test that never commits does not fully exercise how the code under
test interacts with the database. Neither can it test interactions between distinct
transactions. Another disadvantage of rolling back is that the test discards data
that might be useful for diagnosing failures.
Tests should explicitly delineate transactions. We also prefer to make transac-
tion boundaries stand out, so they’re easy to see when reading the test. We usu-
ally extract transaction management into a subordinate object, called a transactor,
that runs a unit of work within a transaction. In this case, the transactor will
coordinate JPA transactions, so we call it a JPATransactor.4
3. We’ve left entityNameOf() out of this code excerpt. The JPA says the the name of an
entity is derived from its related Java class but doesn’t provide a standard API to do
so. We implemented just enough of this mapping to allow DatabaseCleaner to work.
4. In other systems, tests might also use a JMSTransactor for coordinating transactions
in a Java Messaging Service (JMS) broker, or a JTATransactor for coordinating
distributed transactions via the standard Java Transaction API (JTA).
Chapter 25
Testing Persistence
292


---
**Page 293**

public interface UnitOfWork {
  void work() throws Exception;
}
public class JPATransactor { 
  private final EntityManager entityManager;
  public JPATransactor(EntityManager entityManager) { 
    this.entityManager = entityManager; 
  } 
  public void perform(UnitOfWork unitOfWork) throws Exception { 
    EntityTransaction transaction = entityManager.getTransaction();
    transaction.begin(); 
    try { 
      unitOfWork.work(); 
      transaction.commit(); 
    } 
    catch (PersistenceException e) { 
      throw e; 
    } 
    catch (Exception e) { 
      transaction.rollback(); 
      throw e; 
    } 
  } 
}
The transactor is called by passing in a UnitOfWork, usually created as an
anonymous class:
transactor.perform(new UnitOfWork() { 
  public void work() throws Exception {
    customers.addCustomer(aNewCustomer());
  }
});
This pattern is so useful that we regularly use it in our production code as well.
We’ll show more of how the transactor is used in the next section.
“Container-Managed” Transactions
Many Java applications use declarative container-managed transactions, where
the application framework manages the application’s transaction boundaries.The
framework starts each transaction when it receives a request to an application
component, includes the application’s transactional resources in transaction, and
commits or rolls back the transaction when the request succeeds or fails. Java EE
is the canonical example of such frameworks in the Java world.
293
Make Tests Transaction Boundaries Explicit


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



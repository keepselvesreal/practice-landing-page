# 25.2 Isolate Tests That Affect Persistent State (pp.290-292)

---
**Page 290**

An Example Scenario
The examples in this chapter will all use the same scenario. We now have a web
service that performs auction sniping on behalf of our customers.
A customer can log in to different auction sites and has one or more payment
methods by which they pay for our service and the lots they bid for. The system
supports two payment methods: credit cards and an online payment service called
PayMate. A customer has a contact address and, if they have a credit card, the
card has a billing address.
This domain model is represented in our system by the persistent entities shown
in Figure 25.1 (which only includes the ﬁelds that show what the purpose of the
entity is.)
Figure 25.1
Persistent entities
Isolate Tests That Affect Persistent State
Since persistent data hangs around from one test to the next, we have to take
extra care to ensure that persistence tests are isolated from one another. JUnit
cannot do this for us, so the test ﬁxture must ensure that the test starts with its
persistent resources in a known state.
For database code, this means deleting rows from the database tables before
the test starts. The process of cleaning the database depends on the database’s
integrity constraints. It might only be possible to clear tables in a strict order.
Furthermore, if some tables have foreign key constraints between them that
cascade deletes, cleaning one table will automatically clean others.
Chapter 25
Testing Persistence
290


---
**Page 291**

Clean Up Persistent Data at the Start of a Test, Not at the End
Each test should initialize the persistent store to a known state when it starts.When
a test is run individually, it will leave data in the persistent store that can help you
diagnose test failures. When it is run as part of a suite, the next test will clean up
the persistent state ﬁrst, so tests will be isolated from each other. We used this
technique in “Recording the Failure” (page 221) when we cleared the log before
starting the application at the start of the test.
The order in which tables must be cleaned up should be captured in one place
because it must be kept up-to-date as the database schema evolves. It’s an ideal
candidate to be extracted into a subordinate object to be used by any test that
uses the database:
public class DatabaseCleaner {
  private static final Class<?>[] ENTITY_TYPES = { 
    Customer.class, 
    PaymentMethod.class,
    AuctionSiteCredentials.class,
    AuctionSite.class,
    Address.class
  };
  private final EntityManager entityManager;
  public DatabaseCleaner(EntityManager entityManager) {
    this.entityManager = entityManager;
  }
  public void clean() throws SQLException {
    EntityTransaction transaction = entityManager.getTransaction();
    transaction.begin();
    for (Class<?> entityType : ENTITY_TYPES) {
      deleteEntities(entityType);
    }
    transaction.commit();
  }
  private void deleteEntities(Class<?> entityType) {
    entityManager
      .createQuery("delete from " + entityNameOf(entityType)) 
      .executeUpdate();
  }
}
291
Isolate Tests That Affect Persistent State


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



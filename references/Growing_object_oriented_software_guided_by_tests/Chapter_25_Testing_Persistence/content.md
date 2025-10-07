Line 1: 
Line 2: --- 페이지 314 ---
Line 3: Chapter 25
Line 4: Testing Persistence
Line 5: It is always during a passing state of mind that we make lasting
Line 6: resolutions.
Line 7: —Marcel Proust
Line 8: Introduction
Line 9: As we saw in Chapter 8, when we deﬁne an abstraction in terms of a third-party
Line 10: API, we have to test that our abstraction behaves as we expect when integrated
Line 11: with that API, but cannot use our tests to get feedback about its design.
Line 12: A common example is an abstraction implemented using a persistence mecha-
Line 13: nism, such as Object/Relational Mapping (ORM). ORM hides a lot of sophisti-
Line 14: cated functionality behind a simple API. When we build an abstraction upon an
Line 15: ORM, we need to test that our implementation sends correct queries, has correctly
Line 16: conﬁgured the mappings between our objects and the relational schema, uses a
Line 17: dialect of SQL that is compatible with the database, performs updates and deletes
Line 18: that are compatible with the integrity constraints of the database, interacts
Line 19: correctly with the transaction manager, releases external resources in a timely
Line 20: manner, does not trip over any bugs in the database driver, and much more.
Line 21: When testing persistence code, we also have more to worry about with respect
Line 22: to the quality of our tests. There are components running in the background that
Line 23: the test must set up correctly. Those components have persistent state that could
Line 24: make tests interfere with each other. Our test code has to deal with all this extra
Line 25: complexity. We need to spend additional effort to ensure that our tests remain
Line 26: readable and to generate reasonable diagnostics that pinpoint why tests fail—to
Line 27: tell us in which component the failure occurred and why.
Line 28: This chapter describes some techniques for dealing with this complexity. The
Line 29: example code uses the standard Java Persistence API (JPA), but the techniques
Line 30: will work just as well with other persistence mechanisms, such as Java Data
Line 31: Objects (JDO), open source ORM technologies like Hibernate, or even when
Line 32: dumping objects to ﬁles using a data-mapping mechanism such as XStream1 or
Line 33: the standard Java API for XML Binding (JAXB).2
Line 34: 1. http://xstream.codehaus.org
Line 35: 2. Apologies for all the acronyms. The Java standardization process does not require
Line 36: standards to have memorable names.
Line 37: 289
Line 38: 
Line 39: --- 페이지 315 ---
Line 40: An Example Scenario
Line 41: The examples in this chapter will all use the same scenario. We now have a web
Line 42: service that performs auction sniping on behalf of our customers.
Line 43: A customer can log in to different auction sites and has one or more payment
Line 44: methods by which they pay for our service and the lots they bid for. The system
Line 45: supports two payment methods: credit cards and an online payment service called
Line 46: PayMate. A customer has a contact address and, if they have a credit card, the
Line 47: card has a billing address.
Line 48: This domain model is represented in our system by the persistent entities shown
Line 49: in Figure 25.1 (which only includes the ﬁelds that show what the purpose of the
Line 50: entity is.)
Line 51: Figure 25.1
Line 52: Persistent entities
Line 53: Isolate Tests That Affect Persistent State
Line 54: Since persistent data hangs around from one test to the next, we have to take
Line 55: extra care to ensure that persistence tests are isolated from one another. JUnit
Line 56: cannot do this for us, so the test ﬁxture must ensure that the test starts with its
Line 57: persistent resources in a known state.
Line 58: For database code, this means deleting rows from the database tables before
Line 59: the test starts. The process of cleaning the database depends on the database’s
Line 60: integrity constraints. It might only be possible to clear tables in a strict order.
Line 61: Furthermore, if some tables have foreign key constraints between them that
Line 62: cascade deletes, cleaning one table will automatically clean others.
Line 63: Chapter 25
Line 64: Testing Persistence
Line 65: 290
Line 66: 
Line 67: --- 페이지 316 ---
Line 68: Clean Up Persistent Data at the Start of a Test, Not at the End
Line 69: Each test should initialize the persistent store to a known state when it starts.When
Line 70: a test is run individually, it will leave data in the persistent store that can help you
Line 71: diagnose test failures. When it is run as part of a suite, the next test will clean up
Line 72: the persistent state ﬁrst, so tests will be isolated from each other. We used this
Line 73: technique in “Recording the Failure” (page 221) when we cleared the log before
Line 74: starting the application at the start of the test.
Line 75: The order in which tables must be cleaned up should be captured in one place
Line 76: because it must be kept up-to-date as the database schema evolves. It’s an ideal
Line 77: candidate to be extracted into a subordinate object to be used by any test that
Line 78: uses the database:
Line 79: public class DatabaseCleaner {
Line 80:   private static final Class<?>[] ENTITY_TYPES = { 
Line 81:     Customer.class, 
Line 82:     PaymentMethod.class,
Line 83:     AuctionSiteCredentials.class,
Line 84:     AuctionSite.class,
Line 85:     Address.class
Line 86:   };
Line 87:   private final EntityManager entityManager;
Line 88:   public DatabaseCleaner(EntityManager entityManager) {
Line 89:     this.entityManager = entityManager;
Line 90:   }
Line 91:   public void clean() throws SQLException {
Line 92:     EntityTransaction transaction = entityManager.getTransaction();
Line 93:     transaction.begin();
Line 94:     for (Class<?> entityType : ENTITY_TYPES) {
Line 95:       deleteEntities(entityType);
Line 96:     }
Line 97:     transaction.commit();
Line 98:   }
Line 99:   private void deleteEntities(Class<?> entityType) {
Line 100:     entityManager
Line 101:       .createQuery("delete from " + entityNameOf(entityType)) 
Line 102:       .executeUpdate();
Line 103:   }
Line 104: }
Line 105: 291
Line 106: Isolate Tests That Affect Persistent State
Line 107: 
Line 108: --- 페이지 317 ---
Line 109: We use an array, ENTITY_TYPES, to ensure that the entity types (and, therefore,
Line 110: database tables) are cleaned in an order that does not violate referential integrity
Line 111: when rows are deleted from the database.3 We add DatabaseCleaner to a setup
Line 112: method, to initialize the database before each test. For example:
Line 113: public class ExamplePersistenceTest {
Line 114:   final EntityManagerFactory factory = 
Line 115:                                 Persistence.createEntityManagerFactory("example");
Line 116:   final EntityManager entityManager = factory.createEntityManager();
Line 117:   @Before
Line 118:   public void cleanDatabase() throws Exception {
Line 119: new DatabaseCleaner(entityManager).clean();
Line 120:   }
Line 121: […]
Line 122: }
Line 123: For brevity, we won’t show this cleanup in the test examples. You should assume
Line 124: that every persistence test starts with the database in a known, clean state.
Line 125: Make Tests Transaction Boundaries Explicit
Line 126: A common technique to isolate tests that use a transactional resource (such as a
Line 127: database) is to run each test in a transaction which is then rolled back at the end
Line 128: of the test. The idea is to leave the persistent state the same after the test as before.
Line 129: The problem with this technique is that it doesn’t test what happens on commit,
Line 130: which is a signiﬁcant event. The ORM ﬂushes the state of the objects it is man-
Line 131: aging in memory to the database. The database, in turn, checks its integrity
Line 132: constraints. A test that never commits does not fully exercise how the code under
Line 133: test interacts with the database. Neither can it test interactions between distinct
Line 134: transactions. Another disadvantage of rolling back is that the test discards data
Line 135: that might be useful for diagnosing failures.
Line 136: Tests should explicitly delineate transactions. We also prefer to make transac-
Line 137: tion boundaries stand out, so they’re easy to see when reading the test. We usu-
Line 138: ally extract transaction management into a subordinate object, called a transactor,
Line 139: that runs a unit of work within a transaction. In this case, the transactor will
Line 140: coordinate JPA transactions, so we call it a JPATransactor.4
Line 141: 3. We’ve left entityNameOf() out of this code excerpt. The JPA says the the name of an
Line 142: entity is derived from its related Java class but doesn’t provide a standard API to do
Line 143: so. We implemented just enough of this mapping to allow DatabaseCleaner to work.
Line 144: 4. In other systems, tests might also use a JMSTransactor for coordinating transactions
Line 145: in a Java Messaging Service (JMS) broker, or a JTATransactor for coordinating
Line 146: distributed transactions via the standard Java Transaction API (JTA).
Line 147: Chapter 25
Line 148: Testing Persistence
Line 149: 292
Line 150: 
Line 151: --- 페이지 318 ---
Line 152: public interface UnitOfWork {
Line 153:   void work() throws Exception;
Line 154: }
Line 155: public class JPATransactor { 
Line 156:   private final EntityManager entityManager;
Line 157:   public JPATransactor(EntityManager entityManager) { 
Line 158:     this.entityManager = entityManager; 
Line 159:   } 
Line 160:   public void perform(UnitOfWork unitOfWork) throws Exception { 
Line 161:     EntityTransaction transaction = entityManager.getTransaction();
Line 162:     transaction.begin(); 
Line 163:     try { 
Line 164:       unitOfWork.work(); 
Line 165:       transaction.commit(); 
Line 166:     } 
Line 167:     catch (PersistenceException e) { 
Line 168:       throw e; 
Line 169:     } 
Line 170:     catch (Exception e) { 
Line 171:       transaction.rollback(); 
Line 172:       throw e; 
Line 173:     } 
Line 174:   } 
Line 175: }
Line 176: The transactor is called by passing in a UnitOfWork, usually created as an
Line 177: anonymous class:
Line 178: transactor.perform(new UnitOfWork() { 
Line 179:   public void work() throws Exception {
Line 180:     customers.addCustomer(aNewCustomer());
Line 181:   }
Line 182: });
Line 183: This pattern is so useful that we regularly use it in our production code as well.
Line 184: We’ll show more of how the transactor is used in the next section.
Line 185: “Container-Managed” Transactions
Line 186: Many Java applications use declarative container-managed transactions, where
Line 187: the application framework manages the application’s transaction boundaries.The
Line 188: framework starts each transaction when it receives a request to an application
Line 189: component, includes the application’s transactional resources in transaction, and
Line 190: commits or rolls back the transaction when the request succeeds or fails. Java EE
Line 191: is the canonical example of such frameworks in the Java world.
Line 192: 293
Line 193: Make Tests Transaction Boundaries Explicit
Line 194: 
Line 195: --- 페이지 319 ---
Line 196: The techniques we describe in this chapter are compatible with this kind of
Line 197: framework.We have used them to test applications built within Java EE and Spring,
Line 198: and with “plain old” Java programs that use JPA, Hibernate, or JDBC directly.
Line 199: The frameworks wrap transaction management around the objects that make
Line 200: use of transactional resources, so there’s nothing in their code to mark the appli-
Line 201: cation’s transaction boundaries. The tests for those objects, however, need to
Line 202: manage transactions explicitly—which is what a transactor is for.
Line 203: In the tests, the transactor uses the same transaction manager as the application,
Line 204: conﬁgured in the same way. This ensures that the tests and the full application
Line 205: run the same transactional code. It should make no difference whether a trans-
Line 206: action is controlled by a block wrapped around our code by the framework, or by
Line 207: a transactor in our tests. But if we’ve made a mistake and it does make a difference,
Line 208: our end-to-end tests should catch such failures by exercising the application code
Line 209: in the container.
Line 210: Testing an Object That Performs Persistence Operations
Line 211: Now that we’ve got some test scaffolding we can write tests for an object that
Line 212: performs persistence.
Line 213: In our domain model, a customer base represents all the customers we know
Line 214: about. We can add customers to our customer base and ﬁnd customers that match
Line 215: certain criteria. For example, we need to ﬁnd customers with credit cards that
Line 216: are about to expire so that we can send them a reminder to update their payment
Line 217: details.
Line 218: public interface CustomerBase {  […]
Line 219:   void addCustomer(Customer customer);
Line 220:   List<Customer> customersWithExpiredCreditCardsAt(Date deadline);
Line 221: }
Line 222: When unit-testing code that calls a CustomerBase to ﬁnd and notify the
Line 223: relevant customers, we can mock the interface. In a deployed system, however,
Line 224: this code will call a real implementation of CustomerBase that is backed by JPA
Line 225: to save and load customer information from a database. We must also test that
Line 226: this persistent implementation works correctly—that the queries it makes and
Line 227: the object/relational mappings are correct. For example, below is a test of the
Line 228: customersWithExpiredCreditCardsAt() query. There are two helper methods
Line 229: that interact with customerBase within a transaction: addCustomer() adds a set
Line 230: of example customers, and assertCustomersExpiringOn() queries for customers
Line 231: with expired cards.
Line 232: Chapter 25
Line 233: Testing Persistence
Line 234: 294
Line 235: 
Line 236: --- 페이지 320 ---
Line 237: public class PersistentCustomerBaseTest { […]
Line 238:   final PersistentCustomerBase customerBase = 
Line 239:                                  new PersistentCustomerBase(entityManager);
Line 240:   @Test
Line 241:   @SuppressWarnings("unchecked")
Line 242:   public void findsCustomersWithCreditCardsThatAreAboutToExpire() throws Exception {
Line 243:     final String deadline = "6 Jun 2009";
Line 244:     addCustomers(
Line 245:       aCustomer().withName("Alice (Expired)")
Line 246:         .withPaymentMethods(aCreditCard().withExpiryDate(date("1 Jan 2009"))),
Line 247:       aCustomer().withName("Bob (Expired)")
Line 248:         .withPaymentMethods(aCreditCard().withExpiryDate(date("5 Jun 2009"))),
Line 249:       aCustomer().withName("Carol (Valid)")
Line 250:         .withPaymentMethods(aCreditCard().withExpiryDate(date(deadline))),
Line 251:       aCustomer().withName("Dave (Valid)")
Line 252:         .withPaymentMethods(aCreditCard().withExpiryDate(date("7 Jun 2009")))
Line 253:     );
Line 254:     assertCustomersExpiringOn(date(deadline), 
Line 255:                               containsInAnyOrder(customerNamed("Alice (Expired)"), 
Line 256:                                                  customerNamed("Bob (Expired)")));
Line 257:   }
Line 258:   private void addCustomers(final CustomerBuilder... customers) throws Exception {
Line 259: transactor.perform(new UnitOfWork() {
Line 260:       public void work() throws Exception {
Line 261:         for (CustomerBuilder customer : customers) { 
Line 262: customerBase.addCustomer(customer.build());
Line 263:         }
Line 264:       }
Line 265:     });
Line 266:   }
Line 267:   private void assertCustomersExpiringOn(final Date date, 
Line 268:                                          final Matcher<Iterable<Customer>> matcher)
Line 269:     throws Exception 
Line 270:   {
Line 271: transactor.perform(new UnitOfWork() {
Line 272:       public void work() throws Exception {
Line 273:         assertThat(customerBase.customersWithExpiredCreditCardsAsOf(date), matcher);
Line 274:       }
Line 275:     });
Line 276:   }
Line 277: }
Line 278: We call addCustomers() with CustomerBuilders set up to include a name and
Line 279: an expiry date for the credit card. The expiry date is the signiﬁcant ﬁeld for this
Line 280: test, so we create customers with expiry dates before, on, and after the deadline to
Line 281: demonstrate the boundary condition. We also set the name of each customer
Line 282: to identify the instances in a failure (notice that the names self-describe the relevant
Line 283: status of each customer). An alternative to matching on name would have been
Line 284: to use each object’s persistence identiﬁer, which is assigned by JPA. That would
Line 285: have been more complex to work with (it’s not exposed as a property on
Line 286: Customer), and would not be self-describing.
Line 287: 295
Line 288: Testing an Object That Performs Persistence Operations
Line 289: 
Line 290: --- 페이지 321 ---
Line 291: The assertCustomersExpiringOn() method runs the query we’re testing for
Line 292: the given deadline and checks that the result conforms to the Hamcrest matcher
Line 293: we pass in. The containsInAnyOrder() method returns a matcher that checks
Line 294: that there’s a sub-matcher for each of the elements in a collection. We’ve written
Line 295: a customerNamed() method to return a custom matcher that tests whether an
Line 296: object is a Customer with a given name (there’s more on custom matchers in
Line 297: Appendix B). So, this test says that we expect to receive back exactly two Customer
Line 298: objects, named "Alice (Expired)" and "Bob (Expired)".
Line 299: The test implicitly exercises CustomerBase.addCustomer() by calling it to set
Line 300: up the database for the query. Thinking further, what we actually care about is
Line 301: the relationship between the result of calling addCustomer() and subsequent
Line 302: queries, so we probably won’t test addCustomer() independently. If there’s an
Line 303: effect of addCustomer() that is not visible through some feature of the system,
Line 304: then we’d have to ask some hard questions about its purpose before writing a
Line 305: special test query to cover it.
Line 306: Better Test Structure with Matchers
Line 307: This test includes a nice example of using Hamcrest to create a clean test structure.
Line 308: The test method constructs a matcher, which gives a concise description of a valid
Line 309: result for the query. It passes the matcher to assertCustomersExpiringOn(),
Line 310: which just runs the query and passes the result to the matcher. We have a clean
Line 311: separation between the test method, which knows what is expected to be retrieved,
Line 312: and the query/assert method, which knows how to make a query and can be used
Line 313: in other tests.
Line 314: Here is an implementation of PersistentCustomerBase that passes the test:
Line 315: public class PersistentCustomerBase implements CustomerBase {
Line 316:   private final EntityManager entityManager;
Line 317:   public PersistentCustomerBase(EntityManager entityManager) {
Line 318:     this.entityManager = entityManager;
Line 319:   }
Line 320:   public void addCustomer(Customer customer) {
Line 321:     entityManager.persist(customer);
Line 322:   }
Line 323:   public List<Customer> customersWithExpiredCreditCardsAt(Date deadline) {
Line 324:     Query query = entityManager.createQuery(
Line 325:         "select c from Customer c, CreditCardDetails d " +
Line 326:         "where d member of c.paymentMethods " +
Line 327:         "  and d.expiryDate < :deadline");
Line 328:     query.setParameter("deadline", deadline);
Line 329:     return query.getResultList();
Line 330:   }
Line 331: }
Line 332: Chapter 25
Line 333: Testing Persistence
Line 334: 296
Line 335: 
Line 336: --- 페이지 322 ---
Line 337: This implementation looks trivial—it’s so much shorter than its test—but it
Line 338: relies on a lot of XML conﬁguration that we haven’t included and on a third-party
Line 339: framework that implements the EntityManager’s simple API.
Line 340: On Patterns and Type Names
Line 341: The CustomerBase interface and PersistentCustomerBase class implement the
Line 342: repository or data access object pattern (often abbreviated to DAO).We have not
Line 343: used the terms “Repository,” “DataAccessObject,” or “DAO” in the name of the
Line 344: interface or class that implements it because:
Line 345: •
Line 346: Using such terms leaks knowledge about the underlying technology layers
Line 347: (persistence) into the application domain, and so breaks the “ports and
Line 348: adapters” architecture.The objects that use a CustomerBase are persistence-
Line 349: agnostic: they do not care whether the Customer objects they interact with
Line 350: are written to disk or not.The Customer objects are also persistence-agnostic:
Line 351: a program does not need to have a database to create and use Customer
Line 352: objects. Only PersistentCustomerBase knows how it maps Customer objects
Line 353: in and out of persistent storage.
Line 354: •
Line 355: We prefer not to name classes or interfaces after patterns; what matters
Line 356: to us is their relationship to other classes in the system. The clients of
Line 357: CustomerBase do not care what patterns it uses. As the system evolves, we
Line 358: might make the CustomerBase class work in some other way and the name
Line 359: would then be misleading.
Line 360: •
Line 361: We avoid generic words like “data,” “object,” or “access” in type names.We
Line 362: try to give each class a name that identiﬁes a concept within its domain or
Line 363: expresses how it bridges between the application and technical domains.
Line 364: Testing That Objects Can Be Persisted
Line 365: The PersistentCustomerBase relies on so much conﬁguration and underlying
Line 366: third-party code that the error messages from its test can be difﬁcult to diagnose.
Line 367: A test failure could be caused by a defect in a query, the mapping of the Customer
Line 368: class, the mapping of any of the classes that it uses, the conﬁguration of the ORM,
Line 369: invalid database connection parameters, or a misconﬁguration of the database
Line 370: itself.
Line 371: We can write more tests to help us pinpoint the cause of a persistence failure
Line 372: when it occurs. A useful test is to “round-trip” instances of all persistent entity
Line 373: types through the database to check that the mappings are conﬁgured correctly
Line 374: for each class.
Line 375: Round-trip tests are useful whenever we reﬂectively translate objects to and
Line 376: from other forms. Many serialization and mapping technologies have the same
Line 377: advantages and difﬁculties as ORM. The mapping can be deﬁned by compact,
Line 378: 297
Line 379: Testing That Objects Can Be Persisted
Line 380: 
Line 381: --- 페이지 323 ---
Line 382: declarative code or conﬁguration, but misconﬁguration creates defects that are
Line 383: difﬁcult to diagnose. We use round-trip tests so we can quickly identify the cause
Line 384: of such defects.
Line 385: Round-Tripping Persistent Objects
Line 386: We can use a list of “test data builders” (page 257) to represent the persistent
Line 387: entity types. This makes it easy for the test to instantiate each instance. We can
Line 388: also use builder types more than once, with differing set-ups, to create entities
Line 389: for round-tripping in different states or with different relationships to other
Line 390: entities.
Line 391: This test loops through a list of builders (we’ll show how we create
Line 392: the list in a moment). For each builder, it creates and persists an entity in
Line 393: one transaction, and retrieves and compares the result in another. As in the
Line 394: last test, we have two
Line 395: transactor methods that perform transactions.
Line 396: The setup method is persistedObjectFrom() and the query method is
Line 397: assertReloadsWithSameStateAs().
Line 398: public class PersistabilityTest { […]
Line 399:   final List<? extends Builder<?>> persistentObjectBuilders = […]
Line 400:   @Test public void roundTripsPersistentObjects() throws Exception {
Line 401:     for (Builder<?> builder : persistentObjectBuilders) {
Line 402:       assertCanBePersisted(builder);
Line 403:     }
Line 404:   }
Line 405:   private void assertCanBePersisted(Builder<?> builder) throws Exception {
Line 406:     try {
Line 407:       assertReloadsWithSameStateAs(persistedObjectFrom(builder));
Line 408:     } catch (PersistenceException e) {
Line 409:       throw new PersistenceException("could not round-trip " + typeNameFor(builder), e);
Line 410:     }
Line 411:   }
Line 412:   private Object persistedObjectFrom(final Builder<?> builder) throws Exception {
Line 413:     return transactor.performQuery(new QueryUnitOfWork() {
Line 414:       public Object query() throws Exception {
Line 415:         Object original = builder.build(); 
Line 416:         entityManager.persist(original); 
Line 417:         return original; 
Line 418:       }
Line 419:     });
Line 420:   }
Line 421:   private void assertReloadsWithSameStateAs(final Object original) throws Exception {
Line 422: transactor.perform(new UnitOfWork() {
Line 423:       public void work() throws Exception {
Line 424:         assertThat(entityManager.find(original.getClass(), idOf(original));  
Line 425:                    hasSamePersistenFieldsAs(original)); 
Line 426:       }
Line 427:     });
Line 428:   }
Line 429: Chapter 25
Line 430: Testing Persistence
Line 431: 298
Line 432: 
Line 433: --- 페이지 324 ---
Line 434:   private String typeNameFor(Builder<?> builder) {
Line 435:     return builder.getClass().getSimpleName().replace("Builder", "");
Line 436:   }
Line 437: }
Line 438: The persistedObjectFrom() method asks its given builder to create an entity
Line 439: instance which it persists within a transaction. Then it returns the new instance
Line 440: to the test, for later comparison; QueryUnitOfWork is a variant of UnitOfWork that
Line 441: allows us to return a value from a transaction.
Line 442: The assertReloadsWithSameStateAs() method extracts the persistence identiﬁer
Line 443: that the EntityManager assigned to the expected object (using reﬂection), and
Line 444: uses that identiﬁer to ask the EntityManager to retrieve another copy of the entity
Line 445: from the database. Then it calls a custom matcher that uses reﬂection to check
Line 446: that the two copies of the entity have the same values in their persistent ﬁelds.
Line 447: On the Use of Reﬂection
Line 448: We have repeatedly stated that we should test through an object’s public API, so
Line 449: that our tests give us useful feedback about the design of that API. So, why are
Line 450: we using reﬂection here to bypass our objects’ encapsulation boundaries and
Line 451: reach into their private state? Why are we using the persistence API in a way we
Line 452: wouldn’t do in production code?
Line 453: We’re using these round-trip tests to test-drive the conﬁguration of the ORM, as
Line 454: it maps our objects into the database. We’re not test-driving the design of the ob-
Line 455: jects themselves. The state of our objects is encapsulated and hidden from other
Line 456: objects in the system. The ORM uses reﬂection to save that state to, and retrieve
Line 457: it from, the database—so here, we use the same technique as the ORM does to
Line 458: verify its behavior.
Line 459: Round-Tripping Related Entities
Line 460: Creating a list of builders is complicated when there are relationships between
Line 461: entities, and saving of one entity is not cascaded to its related entities. This is the
Line 462: case when an entity refers to reference data that is never created during a
Line 463: transaction.
Line 464: For example, our system knows about a limited number of auction sites. Cus-
Line 465: tomers have AuctionSiteCredentials that refer to those sites. When the system
Line 466: creates a Customer entity, it associates it with existing AuctionSites that it loads
Line 467: from the database. Saving the Customer will save its AuctionSiteCredentials,
Line 468: but won’t save the referenced AuctionSites because they should already exist in
Line 469: the database. At the same time, we must associate a new AuctionSiteCredentials
Line 470: with an AuctionSite that is already in the database, or we will violate referential
Line 471: integrity constraints when we save.
Line 472: 299
Line 473: Testing That Objects Can Be Persisted
Line 474: 
Line 475: --- 페이지 325 ---
Line 476: The ﬁx is to make sure that there’s a persisted AuctionSite before we save a
Line 477: new AuctionSiteCredentials. The AuctionSiteCredentialsBuilder delegates
Line 478: to another builder to create the AuctionSite for the AuctionSiteCredentials
Line 479: under construction (see “Combining Builders” on page 261). We ensure referential
Line 480: integrity by wrapping the AuctionSite builder in a Decorator [Gamma94] that
Line 481: persists the AuctionSite before it is associated with the AuctionSiteCredentials.
Line 482: This is why we call the entity builder within a transaction—some of the related
Line 483: builders will perform database operations that require an active transaction.
Line 484: public class PersistabilityTest { […]
Line 485:   final List<? extends Builder<?>> persistentObjectBuilders = Arrays.asList(
Line 486:   new AddressBuilder(),
Line 487:   new PayMateDetailsBuilder(),
Line 488:   new CreditCardDetailsBuilder(),
Line 489:   new AuctionSiteBuilder(),
Line 490:   new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())),
Line 491:   new CustomerBuilder()
Line 492:     .usingAuctionSites(
Line 493:       new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())))
Line 494:     .withPaymentMethods(
Line 495:       new CreditCardDetailsBuilder(),
Line 496:       new PayMateDetailsBuilder()));
Line 497:   private <T> Builder<T> persisted(final Builder<T> builder) {
Line 498:     return new Builder<T>() {
Line 499:       public T build() {
Line 500:         T entity = builder.build();
Line 501:         entityManager.persist(entity);
Line 502:         return entity;
Line 503:       }
Line 504:     };    
Line 505:   }
Line 506: }
Line 507: But Database Tests Are S-l-o-w!
Line 508: Tests that run against realistic infrastructure are much slower than unit tests that
Line 509: run everything in memory. We can unit-test our code by deﬁning a clean interface
Line 510: to the persistence infrastructure (deﬁned in terms of our code’s domain) and using
Line 511: a mock persistence implementation—as we described in “Only Mock Types That
Line 512: You Own” (page 69). We then test the implementation of this interface with
Line 513: ﬁne-grained integration tests so we don’t have to bring up the entire system to
Line 514: test the technical layers.
Line 515: This lets us organize our tests into a chain of phases: unit tests that run very
Line 516: quickly in memory; slower integration tests that reach outside the process, usually
Line 517: through third-party APIs, and that depend on the conﬁguration of external services
Line 518: such as databases and messaging brokers; and, ﬁnally, end-to-end tests that run
Line 519: against a system packaged and deployed into a production-like environment.
Line 520: This gives us rapid feedback if we break the application’s core logic, and incre-
Line 521: mental feedback about integration at increasingly coarse levels of granularity.
Line 522: Chapter 25
Line 523: Testing Persistence
Line 524: 300
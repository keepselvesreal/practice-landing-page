# 25.5 Testing That Objects Can Be Persisted (pp.297-300)

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


---
**Page 298**

declarative code or conﬁguration, but misconﬁguration creates defects that are
difﬁcult to diagnose. We use round-trip tests so we can quickly identify the cause
of such defects.
Round-Tripping Persistent Objects
We can use a list of “test data builders” (page 257) to represent the persistent
entity types. This makes it easy for the test to instantiate each instance. We can
also use builder types more than once, with differing set-ups, to create entities
for round-tripping in different states or with different relationships to other
entities.
This test loops through a list of builders (we’ll show how we create
the list in a moment). For each builder, it creates and persists an entity in
one transaction, and retrieves and compares the result in another. As in the
last test, we have two
transactor methods that perform transactions.
The setup method is persistedObjectFrom() and the query method is
assertReloadsWithSameStateAs().
public class PersistabilityTest { […]
  final List<? extends Builder<?>> persistentObjectBuilders = […]
  @Test public void roundTripsPersistentObjects() throws Exception {
    for (Builder<?> builder : persistentObjectBuilders) {
      assertCanBePersisted(builder);
    }
  }
  private void assertCanBePersisted(Builder<?> builder) throws Exception {
    try {
      assertReloadsWithSameStateAs(persistedObjectFrom(builder));
    } catch (PersistenceException e) {
      throw new PersistenceException("could not round-trip " + typeNameFor(builder), e);
    }
  }
  private Object persistedObjectFrom(final Builder<?> builder) throws Exception {
    return transactor.performQuery(new QueryUnitOfWork() {
      public Object query() throws Exception {
        Object original = builder.build(); 
        entityManager.persist(original); 
        return original; 
      }
    });
  }
  private void assertReloadsWithSameStateAs(final Object original) throws Exception {
transactor.perform(new UnitOfWork() {
      public void work() throws Exception {
        assertThat(entityManager.find(original.getClass(), idOf(original));  
                   hasSamePersistenFieldsAs(original)); 
      }
    });
  }
Chapter 25
Testing Persistence
298


---
**Page 299**

  private String typeNameFor(Builder<?> builder) {
    return builder.getClass().getSimpleName().replace("Builder", "");
  }
}
The persistedObjectFrom() method asks its given builder to create an entity
instance which it persists within a transaction. Then it returns the new instance
to the test, for later comparison; QueryUnitOfWork is a variant of UnitOfWork that
allows us to return a value from a transaction.
The assertReloadsWithSameStateAs() method extracts the persistence identiﬁer
that the EntityManager assigned to the expected object (using reﬂection), and
uses that identiﬁer to ask the EntityManager to retrieve another copy of the entity
from the database. Then it calls a custom matcher that uses reﬂection to check
that the two copies of the entity have the same values in their persistent ﬁelds.
On the Use of Reﬂection
We have repeatedly stated that we should test through an object’s public API, so
that our tests give us useful feedback about the design of that API. So, why are
we using reﬂection here to bypass our objects’ encapsulation boundaries and
reach into their private state? Why are we using the persistence API in a way we
wouldn’t do in production code?
We’re using these round-trip tests to test-drive the conﬁguration of the ORM, as
it maps our objects into the database. We’re not test-driving the design of the ob-
jects themselves. The state of our objects is encapsulated and hidden from other
objects in the system. The ORM uses reﬂection to save that state to, and retrieve
it from, the database—so here, we use the same technique as the ORM does to
verify its behavior.
Round-Tripping Related Entities
Creating a list of builders is complicated when there are relationships between
entities, and saving of one entity is not cascaded to its related entities. This is the
case when an entity refers to reference data that is never created during a
transaction.
For example, our system knows about a limited number of auction sites. Cus-
tomers have AuctionSiteCredentials that refer to those sites. When the system
creates a Customer entity, it associates it with existing AuctionSites that it loads
from the database. Saving the Customer will save its AuctionSiteCredentials,
but won’t save the referenced AuctionSites because they should already exist in
the database. At the same time, we must associate a new AuctionSiteCredentials
with an AuctionSite that is already in the database, or we will violate referential
integrity constraints when we save.
299
Testing That Objects Can Be Persisted


---
**Page 300**

The ﬁx is to make sure that there’s a persisted AuctionSite before we save a
new AuctionSiteCredentials. The AuctionSiteCredentialsBuilder delegates
to another builder to create the AuctionSite for the AuctionSiteCredentials
under construction (see “Combining Builders” on page 261). We ensure referential
integrity by wrapping the AuctionSite builder in a Decorator [Gamma94] that
persists the AuctionSite before it is associated with the AuctionSiteCredentials.
This is why we call the entity builder within a transaction—some of the related
builders will perform database operations that require an active transaction.
public class PersistabilityTest { […]
  final List<? extends Builder<?>> persistentObjectBuilders = Arrays.asList(
  new AddressBuilder(),
  new PayMateDetailsBuilder(),
  new CreditCardDetailsBuilder(),
  new AuctionSiteBuilder(),
  new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())),
  new CustomerBuilder()
    .usingAuctionSites(
      new AuctionSiteCredentialsBuilder().forSite(persisted(new AuctionSiteBuilder())))
    .withPaymentMethods(
      new CreditCardDetailsBuilder(),
      new PayMateDetailsBuilder()));
  private <T> Builder<T> persisted(final Builder<T> builder) {
    return new Builder<T>() {
      public T build() {
        T entity = builder.build();
        entityManager.persist(entity);
        return entity;
      }
    };    
  }
}
But Database Tests Are S-l-o-w!
Tests that run against realistic infrastructure are much slower than unit tests that
run everything in memory. We can unit-test our code by deﬁning a clean interface
to the persistence infrastructure (deﬁned in terms of our code’s domain) and using
a mock persistence implementation—as we described in “Only Mock Types That
You Own” (page 69). We then test the implementation of this interface with
ﬁne-grained integration tests so we don’t have to bring up the entire system to
test the technical layers.
This lets us organize our tests into a chain of phases: unit tests that run very
quickly in memory; slower integration tests that reach outside the process, usually
through third-party APIs, and that depend on the conﬁguration of external services
such as databases and messaging brokers; and, ﬁnally, end-to-end tests that run
against a system packaged and deployed into a production-like environment.
This gives us rapid feedback if we break the application’s core logic, and incre-
mental feedback about integration at increasingly coarse levels of granularity.
Chapter 25
Testing Persistence
300



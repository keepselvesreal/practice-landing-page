# 25.6 But Database Tests Are S-l-o-w! (pp.300-301)

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


---
**Page 301**

Chapter 26
Unit Testing and Threads
It is decreed by a merciful Nature that the human brain cannot think
of two things simultaneously.
—Sir Arthur Conan Doyle
Introduction
There’s no getting away from it: concurrency complicates matters. It is a challenge
when doing test-driven development. Unit tests cannot give you as much
conﬁdence in system quality because concurrency and synchronization are system-
wide concerns. When writing tests, you have to worry about getting the synchro-
nization right within the system and between the test and the system. Test failures
are harder to diagnose because exceptions may be swallowed by background
threads or tests may just time out with no clear explanation.
It’s hard to diagnose and correct synchronization problems in existing code,
so it’s worth thinking about the system’s concurrency architecture ahead of
time. You don’t need to design it in great detail, just decide on a broad-brush
architecture and principles by which the system will cope with concurrency.
This design is often prescribed by the frameworks or libraries that an
application uses. For example:
•
Swing dispatches user events on its own thread. If an event handler runs
for a long time, the user interface becomes unresponsive because Swing
does not process user input while the event handler is running. Event call-
backs must spawn “worker” threads to perform long-running tasks, and
those worker threads must synchronize with the event dispatch thread to
update the user interface.
•
A servlet container has a pool of threads that receive HTTP requests and
pass them to servlets for processing. Many threads can be active in the same
servlet instance at once.
•
Java EE containers manage all the threading in the application. The contain-
er guarantees that only one thread will call into a component at a time.
Components cannot start their own threads.
•
The Smack library used by the Auction Sniper application starts a daemon
thread to receive XMPP messages. It will deliver messages on a single thread,
301



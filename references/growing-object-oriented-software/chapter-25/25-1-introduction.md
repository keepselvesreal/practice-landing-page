# 25.1 Introduction (pp.289-290)

---
**Page 289**

Chapter 25
Testing Persistence
It is always during a passing state of mind that we make lasting
resolutions.
—Marcel Proust
Introduction
As we saw in Chapter 8, when we deﬁne an abstraction in terms of a third-party
API, we have to test that our abstraction behaves as we expect when integrated
with that API, but cannot use our tests to get feedback about its design.
A common example is an abstraction implemented using a persistence mecha-
nism, such as Object/Relational Mapping (ORM). ORM hides a lot of sophisti-
cated functionality behind a simple API. When we build an abstraction upon an
ORM, we need to test that our implementation sends correct queries, has correctly
conﬁgured the mappings between our objects and the relational schema, uses a
dialect of SQL that is compatible with the database, performs updates and deletes
that are compatible with the integrity constraints of the database, interacts
correctly with the transaction manager, releases external resources in a timely
manner, does not trip over any bugs in the database driver, and much more.
When testing persistence code, we also have more to worry about with respect
to the quality of our tests. There are components running in the background that
the test must set up correctly. Those components have persistent state that could
make tests interfere with each other. Our test code has to deal with all this extra
complexity. We need to spend additional effort to ensure that our tests remain
readable and to generate reasonable diagnostics that pinpoint why tests fail—to
tell us in which component the failure occurred and why.
This chapter describes some techniques for dealing with this complexity. The
example code uses the standard Java Persistence API (JPA), but the techniques
will work just as well with other persistence mechanisms, such as Java Data
Objects (JDO), open source ORM technologies like Hibernate, or even when
dumping objects to ﬁles using a data-mapping mechanism such as XStream1 or
the standard Java API for XML Binding (JAXB).2
1. http://xstream.codehaus.org
2. Apologies for all the acronyms. The Java standardization process does not require
standards to have memorable names.
289


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



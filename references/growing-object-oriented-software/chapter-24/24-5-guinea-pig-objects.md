# 24.5 "Guinea Pig" Objects (pp.284-289)

---
**Page 284**

“Guinea Pig” Objects
In the “ports and adapters” architecture we described in “Designing for
Maintainability” (page 47), the adapters map application domain objects onto
the system’s technical infrastructure. Most of the adapter implementations we
see are generic; for example, they often use reﬂection to move values between
domains. We can apply such mappings to any type of object, which means we
can change our domain model without touching the mapping code.
The easiest approach when writing tests for the adapter code is to use types
from the application domain model, but this makes the test brittle because it
binds together the application and adapter domains. It introduces a risk of mis-
leadingly breaking tests when we change the application model, because we
haven’t separated the concerns.
Here’s an example. A system uses an XmlMarshaller to marshal objects to and
from XML so they can be sent across a network. This test exercises XmlMarshaller
by round-tripping an AuctionClosedEvent object: a type that the production
system really does send across the network.
public class XmlMarshallerTest {
  @Test public void 
marshallsAndUnmarshallsSerialisableFields() {
    XMLMarshaller marshaller = new XmlMarshaller();
    AuctionClosedEvent original = new AuctionClosedEventBuilder().build();
    String xml = marshaller.marshall(original);
    AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
    assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
  }
}
Later we decide that our system won’t send an AuctionClosedEvent after all,
so we should be able to delete the class. Our refactoring attempt will fail because
AuctionClosedEvent is still being used by the XmlMarshallerTest. The irrelevant
coupling will force us to rework the test unnecessarily.
There’s a more signiﬁcant (and subtle) problem when we couple tests to domain
types: it’s harder to see when test assumptions have been broken. For example,
our XmlMarshallerTest also checks how the marshaller handles transient and
non-transient ﬁelds. When we wrote the tests, AuctionClosedEvent included both
kind of ﬁelds, so we were exercising all the paths through the marshaller. Later,
we removed the transient ﬁelds from AuctionClosedEvent, which means that we
have tests that are no longer meaningful but do not fail. Nothing is alerting us
that we have tests that have stopped working and that important features are
not being covered.
Chapter 24
Test Flexibility
284


---
**Page 285**

We should test the XmlMarshaller with speciﬁc types that are clear about the
features that they represent, unrelated to the real system. For example, we can
introduce helper classes in the test:
public class XmlMarshallerTest {
  public static class MarshalledObject {
    private String privateField = "private";
    public final String publicFinalField = "public final";
    public int primitiveField;
// constructors, accessors for private field, etc.
  }
  public static class WithTransient extends MarshalledObject {
    public transient String transientField = "transient";
  }  
  @Test public void 
marshallsAndUnmarshallsSerialisableFields() {
    XMLMarshaller marshaller = new XmlMarshaller();
WithTransient original = new WithTransient();
    String xml = marshaller.marshall(original);
    AuctionClosedEvent unmarshalled = marshaller.unmarshall(xml);
    assertThat(unmarshalled, hasSameSerialisableFieldsAs(original));
  }
} 
The WithTransient class acts as a “guinea pig,” allowing us to exhaustively
exercise the behavior of our XmlMarshaller before we let it loose on our produc-
tion domain model. WithTransient also makes our test more readable because
the class and its ﬁelds are examples of “Self-Describing Value” (page 269), with
names that reﬂect their roles in the test.
285
Guinea Pig Objects


---
**Page 286**

This page intentionally left blank 


---
**Page 287**

Part V
Advanced Topics
In this part, we cover some topics that regularly cause teams to
struggle with test-driven development. What’s common to these
topics is that they cross the boundary between feature-level and
system-level design. For example, when we look at multi-
threaded code, we need to test both the behavior that runs
within a thread and the way different threads interact.
Our experience is that such code is difﬁcult to test when we’re
not clear about which aspect we’re addressing. Lumping every-
thing together produces tests that are confusing, brittle, and
sometimes misleading. When we take the time to listen to these
“test smells,” they often lead us to a better design with a clearer
separation of responsibilities.


---
**Page 288**

This page intentionally left blank 


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



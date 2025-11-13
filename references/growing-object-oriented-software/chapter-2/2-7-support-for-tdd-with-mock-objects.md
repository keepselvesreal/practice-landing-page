# 2.7 Support for TDD with Mock Objects (pp.19-21)

---
**Page 19**

Figure 2.4
Unit-testing an object in isolation
Figure 2.5
Testing an object with mock objects
have been called as expected; they also implement any stubbed behavior needed
to make the rest of the test work.
With this infrastructure in place, we can change the way we approach TDD.
Figure 2.5 implies that we’re just trying to test the target object and that we al-
ready know what its neighbors look like. In practice, however, those collaborators
don’t need to exist when we’re writing a unit test. We can use the test to help us
tease out the supporting roles our object needs, deﬁned as Java interfaces, and
ﬁll in real implementations as we develop the rest of the system. We call this in-
terface discovery; you’ll see an example when we extract an AuctionEventListener
in Chapter 12.
Support for TDD with Mock Objects
To support this style of test-driven programming, we need to create mock in-
stances of the neighboring objects, deﬁne expectations on how they’re called and
then check them, and implement any stub behavior we need to get through the
test. In practice, the runtime structure of a test with mock objects usually looks
like Figure 2.6.
19
Support for TDD with Mock Objects


---
**Page 20**

Figure 2.6
Testing an object with mock objects
We use the term mockery2 for the object that holds the context of a test, creates
mock objects, and manages expectations and stubbing for the test. We’ll show
the practice throughout Part III, so we’ll just touch on the basics here. The
essential structure of a test is:
•
Create any required mock objects.
•
Create any real objects, including the target object.
•
Specify how you expect the mock objects to be called by the target object.
•
Call the triggering method(s) on the target object.
•
Assert that any resulting values are valid and that all the expected calls have
been made.
The unit test makes explicit the relationship between the target object and its
environment. It creates all the objects in the cluster and makes assertions about
the interactions between the target object and its collaborators. We can code this
infrastructure by hand or, these days, use one of the multiple mock object
frameworks that are available in many languages. The important point, as we
stress repeatedly throughout this book, is to make clear the intention of every
test, distinguishing between the tested functionality, the supporting infrastructure,
and the object structure.
2. This is a pun by Ivan Moore that we adopted in a ﬁt of whimsy.
Chapter 2
Test-Driven Development with Objects
20


---
**Page 21**

Chapter 3
An Introduction to the Tools
Man is a tool-using animal. Without tools he is nothing, with tools he
is all.
—Thomas Carlyle
Stop Me If You’ve Heard This One Before
This book is about the techniques of using tests to guide the development of
object-oriented software, not about speciﬁc technologies. To demonstrate the
techniques in action, however, we’ve had to pick some technologies for our ex-
ample code. For the rest of the book we’re going to use Java, with the JUnit 4,
Hamcrest, and jMock2 frameworks. If you’re using something else, we hope
we’ve been clear enough so that you can apply these ideas in your environment.
In this chapter we brieﬂy describe the programming interfaces for these three
frameworks, just enough to help you make sense of the code examples in the rest
of the book. If you already know how to use them, you can skip this chapter.
A Minimal Introduction to JUnit 4
We use JUnit 4 (version 4.6 at the time of writing) as our Java test framework.1
In essence, JUnit uses reﬂection to walk the structure of a class and run whatever
it can ﬁnd in that class that represents a test. For example, here’s a test that
exercises a Catalog class which manages a collection of Entry objects:
public class CatalogTest {
  private final Catalog catalog = new Catalog();
  @Test public void containsAnAddedEntry() { 
    Entry entry = new Entry("fish", "chips");
    catalog.add(entry);
    assertTrue(catalog.contains(entry));
  }
  @Test public void indexesEntriesByName() {
    Entry entry = new Entry("fish", "chips");
    catalog.add(entry);
    assertEquals(entry, catalog.entryFor("fish"));  
    assertNull(catalog.entryFor("missing name"));  
  }
}
1. JUnit is bundled with many Java IDEs and is available at www.junit.org.
21



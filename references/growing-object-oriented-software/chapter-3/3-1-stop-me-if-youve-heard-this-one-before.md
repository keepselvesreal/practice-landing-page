# 3.1 Stop Me If You've Heard This One Before (pp.21-21)

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



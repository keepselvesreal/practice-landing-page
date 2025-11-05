# 21.5 Assertions and Expectations (pp.254-255)

---
**Page 254**

@Test public void expandsMacrosSurroundedWithBraces() {
  StringTemplate template = new StringTemplate("{a}{b}");
  try {
    String expanded = template.expand(macros);
    assertThat(expanded, equalTo("AB"));
  } catch (TemplateFormatException e) {
    fail("Template failed: " + e);
  }
}
If this test is intended to pass, then converting the exception actually drops infor-
mation from the stack trace. The simplest thing to do is to let the exception
propagate for the test runtime to catch. We can add arbitrary exceptions to the
test method signature because it’s only called by reﬂection. This removes at least
half the lines of the test, and we can compact it further to be:
@Test public void expandsMacrosSurroundedWithBraces() throws Exception {
  assertThat(new StringTemplate("{a}{b}").expand(macros),
             equalTo("AB"));
}
which tells us just what is supposed to happen and ignores everything else.
Delegate to Subordinate Objects
Sometimes helper methods aren’t enough and we need helper objects to support
the tests. We saw this in the test rig we built in Chapter 11. We developed the
ApplicationRunner, AuctionSniperDriver, and FakeAuctionServer classes so we
could write tests in terms of auctions and Snipers, not in terms of Swing and
messaging.
A more common technique is to write test data builders to build up complex
data structures with just the appropriate values for a test; see Chapter 22 for
more detail. Again, the point is to include in the test just the values that are rele-
vant, so that the reader can understand the intent; everything else can be defaulted.
There are two approaches to writing subordinate objects. In Chapter 11 we
started by writing the test we wanted to see and then ﬁlling in the supporting
objects: start from a statement of the problem and see where it goes. The alterna-
tive is to write the code directly in the tests, and then refactor out any clusters
of behavior. This is the origin of the WindowLicker framework, which started
out as helper code in JUnit tests for interacting with the Swing event dispatcher
and eventually grew into a separate project.
Assertions and Expectations
The assertions and expectations of a test should communicate precisely what
matters in the behavior of the target code. We regularly see code where tests assert
Chapter 21
Test Readability
254


---
**Page 255**

too much detail, which makes them difﬁcult to read and brittle when things
change; we discuss what this might mean in “Too Many Expectations” (page 242).
For the expectations and assertions we write, we try to keep them as narrowly
deﬁned as possible. For example, in the “instrument with price” assertion above,
we check only the strike price and ignore the rest of the values as irrelevant in
that test. In other cases, we’re not interested in all of the arguments to a method,
so we ignore them in the expectation. In Chapter 19, we deﬁne an expectation
that says that we care about the Sniper identiﬁer and message, but that any
RuntimeException object will do for the third argument:
oneOf(failureReporter).cannotTranslateMessage(
                         with(SNIPER_ID), with(badMessage),
                         with(any(RuntimeException.class)));
If you learned about pre- and postconditions in college, this is when that training
will come in useful.
Finally, a word of caution on assertFalse(). The combination of the failure
message and negation makes it easy to read this as meaning that the two dates
should not be different:
assertFalse("end date", first.endDate().equals(second.endDate()));
We could use assertTrue() and add a “!” to the result but, again, the single
character is easy to miss. That’s why we prefer to use matchers to make the code
more explicit:
assertThat("end date", first.endDate(), not(equalTo(second.endDate())));
which also has the advantage of showing the actual date received in the failure
report:
java.lang.AssertionError: end date
Expected: not <Thu Jan 01 02:34:38 GMT 1970>
     but: was <Thu Jan 01 02:34:38 GMT 1970>
Literals and Variables
One last point. As we wrote in the introduction to this chapter, test code tends
to be more concrete than production code, which means it has more literal values.
Literal values without explanation can be difﬁcult to understand because the
programmer has to interpret whether a particular value is signiﬁcant (e.g. just
outside the allowed range) or just an arbitrary placeholder to trace behavior (e.g.
should be doubled and passed on to a peer). A literal value does not describe its
role, although there are some techniques for doing so that we will show in
Chapter 23
One solution is to allocate literal values to variables and constants with names
that describe their function. For example, in Chapter 12 we declared
255
Literals and Variables



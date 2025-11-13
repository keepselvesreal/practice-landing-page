# 21.4 Streamline the Test Code (pp.252-254)

---
**Page 252**

  @Test public void writesMessageTranslationFailureToLog() {
    Exception exception = new Exception("an exception");
    context.checking(new Expectations() {{          // Expect
      oneOf(logger).severe( expected log message here);
    }});
    reporter.cannotTranslateMessage("auction id",   // Execute
                                    "failed message", exception); 
// implicitly check expectations are satisfied
// Assert
  }
  @AfterClass public static void resetLogging() {   // Teardown
    LogManager.getLogManager().reset();
  }  
}
Write Tests Backwards
Although we stick to a canonical format for test code, we don’t necessarily write
tests from top to bottom. What we often do is: write the test name, which helps us
decide what we want to achieve; write the call to the target code, which is the entry
point for the feature; write the expectations and assertions, so we know what effects
the feature should have; and, write the setup and teardown to deﬁne the context
for the test. Of course, there may be some blurring of these steps to help the
compiler, but this sequence reﬂects how we tend to think through a new unit test.
Then we run it and watch it fail.
How Many Assertions in a Test Method?
Some TDD practitioners suggest that each test should only contain one expectation
or assertion.This is useful as a training rule when learning TDD, to avoid asserting
everything the developer can think of, but we don’t ﬁnd it practical. A better rule
is to think of one coherent feature per test, which might be represented by up to
a handful of assertions. If a single test seems to be making assertions about
different features of a target object, it might be worth splitting up. Once again,
expressiveness is the key: as a reader of this test, can I ﬁgure out what’s
signiﬁcant?
Streamline the Test Code
All code should emphasize “what” it does over “how,” including test code; the
more implementation detail is included in a test method, the harder it is for
the reader to understand what’s important. We try to move everything out
of the test method that doesn’t contribute to the description, in domain
terms, of the feature being exercised. Sometimes that involves restructuring the
code, sometimes just ignoring the syntax noise.
Chapter 21
Test Readability
252


---
**Page 253**

Use Structure to Explain
As you’ll have seen throughout Part III, we make a point of following “Small
Methods to Express Intent” (page 226), even to the extent of writing a tiny
method like translatorFor() just to reduce the Java syntax noise. This ﬁts
nicely into the Hamcrest approach, where the assertThat() and jMock expecta-
tion syntaxes are designed to allow developers to compose small features into a
(more or less) readable description of an assertion. For example,
assertThat(instruments, hasItem(instrumentWithPrice(greaterThan(81))));
checks whether the collection instruments has at least one Instrument with a
strikePrice property greater than 81. The assertion line expresses our intent,
the helper method creates a matcher that checks the value:
private Matcher<? super Instrument> 
instrumentWithPrice(Matcher<? super Integer> priceMatcher) {
  return new FeatureMatcher<Instrument, Integer>(
               priceMatcher, "instrument at price", "price") {
    @Override protected Integer featureValueOf(Instrument actual) {
      return actual.getStrikePrice();
    }
  };
}
This may create more program text in the end, but we’re prioritizing expressive-
ness over minimizing the source lines.
Use Structure to Share
We also extract common features into methods that can be shared between tests
for setting up values, tearing down state, making assertions, and occasionally
triggering the event. For example, in Chapter 19, we exploited jMock’s facility
for setting multiple expectation blocks to write a expectSniperToFailWhenItIs()
method that wraps up repeated behavior behind a descriptive name.
The only caution with factoring out test structure is that, as we said in the in-
troduction to this chapter, we have to be careful not to make a test so abstract
that we cannot see what it does any more. Our highest concern is making the
test describe what the target code does, so we refactor enough to be able to see
its ﬂow, but we don’t always refactor as hard as we would for production code.
Accentuate the Positive
We only catch exceptions in a test if we want to assert something about them. We
sometimes see tests like this:
253
Streamline the Test Code


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



# 21.3 Canonical Test Structure (pp.251-252)

---
**Page 251**

Canonical Test Structure
We ﬁnd that if we write our tests in a standard form, they’re easier to
understand. We can skim-read to ﬁnd expectations and assertions quickly and
see how they relate to the code under test. If we’re ﬁnding it difﬁcult to write a
test in a standard form, that’s often a hint that the code is too complicated or
that we haven’t quite clariﬁed our ideas.
The most common form for a test is:
1.
Setup: prepare the context of the test, the environment in which the target
code will run;
2.
Execute: call the target code, triggering the tested behavior;
3.
Verify: check for a visible effect that we expect from the behavior; and,
4.
Teardown: clean up any leftover state that might corrupt other tests.
There are other versions of this form, such as “Arrange, Act, Assert,” which
collapse some of the stages.
For example:
public class StringTemplateTest {
  @Test public void expandsMacrosSurroundedWithBraces() {
    StringTemplate template = new StringTemplate("{a}{b}"); // Setup
    HashMap<String,Object> macros = new HashMap<String,Object>();
    macros.put("a", "A");
    macros.put("b", "B");
    String expanded = template.expand(macros);              // Execute
    assertThat(expanded, equalTo("AB"));                    // Assert
  }                                                         // No Teardown
}
Tests that set expectations on mock objects use a variant of this structure where
some of the assertions are declared before the execute stage and are implicitly
checked afterwards—for example, in LoggingXMPPFailureReporterTest from
Chapter 19:
@RunWith(JMock.class)
public class LoggingXMPPFailureReporterTest {
  private final Mockery context = new Mockery() {{  // Setup
   setImposteriser(ClassImposteriser.INSTANCE); 
  }};
  final Logger logger = context.mock(Logger.class);
  final LoggingXMPPFailureReporter reporter = new LoggingXMPPFailureReporter(logger);
251
Canonical Test Structure


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



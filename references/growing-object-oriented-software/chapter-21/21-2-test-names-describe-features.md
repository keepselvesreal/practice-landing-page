# 21.2 Test Names Describe Features (pp.248-251)

---
**Page 248**

Could Do Better1
We’ve seen many unit test suites that could be much more effective given a
little extra attention. They have too many “test smells” of the kind cataloged in
[Meszaros07], as well as in our own Chapters 20 and 24.When cleaning up tests,
or just trying to write new ones, the readability problems we watch out for are:
•
Test names that do not clearly describe the point of each test case and its
differences from the other test cases;
•
Single test cases that seem to be exercising multiple features;
•
Tests with different structure, so the reader cannot skim-read them to
understand their intention;
•
Tests with lots of code for setting up and handling exceptions, which buries
their essential logic; and,
•
Tests that use literal values (“magic numbers”) but are not clear about what,
if anything, is signiﬁcant about those values.
Test Names Describe Features
The name of the test should be the ﬁrst clue for a developer to understand what
is being tested and how the target object is supposed to behave.
Not every team we’ve worked with follows this principle. Some naive developers
use names that don’t mean anything at all:
public class TargetObjectTest {
  @Test public void test1() { […]
  @Test public void test2() { […]
  @Test public void test3() { […]
We don’t see many of these nowadays; the world has moved on. A common
approach is to name a test after the method it’s exercising:
public class TargetObjectTest {
  @Test public void isReady() { […]
  @Test public void choose() { […]
  @Test public void choose1() { […]
public class TargetObject  {
  public void isReady() { […]
  public void choose(Picker picker) { […]
perhaps with multiple tests for different paths through the same method.
1. This is (or was) a common phrase in UK school reports for children whose schoolwork
isn’t as good as it could be.
Chapter 21
Test Readability
248


---
**Page 249**

At best, such names duplicate the information a developer could get just by
looking at the target class; they break the “Don’t Repeat Yourself” principle
[Hunt99]. We don’t need to know that TargetObject has a choose() method—we
need to know what the object does in different situations, what the method is for.
A better alternative is to name tests in terms of the features that the target
object provides. We use a TestDox convention (invented by Chris Stevenson)
where each test name reads like a sentence, with the target class as the implicit
subject. For example,
•
A List holds items in the order they were added.
•
A List can hold multiple references to the same item.
•
A List throws an exception when removing an item it doesn’t hold.
We can translate these directly to method names:
public class ListTests {
  @Test public void holdsItemsInTheOrderTheyWereAdded() { […]
  @Test public void canHoldMultipleReferencesToTheSameItem() { […]
  @Test public void throwsAnExceptionWhenRemovingAnItemItDoesntHold() { […]
These names can be as long as we like because they’re only called through
reﬂection—we never have to type them in to call them.
The point of the convention is to encourage the developer to think in terms of
what the target object does, not what it is. It’s also very compatible with our in-
cremental approach of adding a feature at a time to an existing codebase. It gives
us a consistent style of naming all the way from user stories, through tasks and
acceptance tests, to unit tests—as you saw in Part III.
As a matter of style, the test name should say something about the expected
result, the action on the object, and the motivation for the scenario. For example,
if we were testing a ConnectionMonitor class, then
pollsTheServersMonitoringPort()
doesn’t tell us enough: why does it poll, what happens when it gets a result? On
the other hand,
notifiesListenersThatServerIsUnavailableWhenCannotConnectToItsMonitoringPort()
explains both the scenario and the expected behavior. We’ll show later how this
style of naming maps onto our standard test structures.
249
Test Names Describe Features


---
**Page 250**

Test Name First or Last?
We’ve noticed that some developers start with a placeholder name, ﬁll out the body
of the test, and then decide what to call it. Others (such as Steve) like to decide
the test name ﬁrst, to clarify their intentions, before writing any test code. Both ap-
proaches work as long as the developer follows through and makes sure that the
test is, in the end, consistent and expressive.
The TestDox format fulﬁlls the early promise of TDD—that the tests should
act as documentation for the code. There are tools and IDE plug-ins that unpack
the “camel case” method names and link them to the class under test, such
as the TestDox plug-in for the IntelliJ IDE; Figure 21.1 shows the automatic
documentation for a KeyboardLayout class.
Figure 21.1
The TestDox IntelliJ plug-in
Regularly Read Documentation Generated from Tests
We ﬁnd that such generated documentation gives us a fresh perspective on the
test names, highlighting the problems we’re too close to the code to see. For
example, when generating the screenshot for Figure 21.1, Nat noticed that the
name of the ﬁrst test is unclear—it should be “translates numbers to key strokes
in all known layouts.”
We make an effort to at least skim-read the documentation regularly during
development.
Chapter 21
Test Readability
250


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



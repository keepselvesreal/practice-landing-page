# 3.4 jMock2: Mock Objects (pp.25-31)

---
**Page 25**

assertThat(s, not(containsString("bananas"));
the failure report is:
java.lang.AssertionError: 
Expected: not a string containing "bananas"
     got: "Yes, we have no bananas"
Instead of writing code to explicitly check a condition and to generate an in-
formative error message, we can pass a matcher expression to assertThat() and
let it do the work.
Hamcrest is also user-extensible. If we need to check a speciﬁc condition,
we can write a new matcher by implementing the Matcher interface and an
appropriately-named factory method, and the result will combine seamlessly with
the existing matcher expressions. We describe how to write custom Hamcrest
matchers in Appendix B.
jMock2: Mock Objects
jMock2 plugs into JUnit (and other test frameworks) providing support for the
mock objects testing style introduced in Chapter 2. jMock creates mock objects
dynamically, so you don’t have to write your own implementations of the types
you want to mock. It also provides a high-level API for specifying how the object
under test should invoke the mock objects it interacts with, and how the mock
objects will behave in response.
Understanding jMock
jMock is designed to make the expectation descriptions as clear as possible. We
used some unusual Java coding practices to do so, which can appear surprising
at ﬁrst. jMock’s design was motivated by the ideas presented in this book, backed
by many years of experience in real projects. If the examples don’t make sense to
you, there’s more description in Appendix A and at www.jmock.org.We (of course)
believe that it’s worth suspending your judgment until you’ve had a chance to work
through some of the examples.
The core concepts of the jMock API are the mockery, mock objects, and expec-
tations. A mockery represents the context of the object under test, its neighboring
objects; mock objects stand in for the real neighbors of the object under test while
the test runs; and expectations describe how the object under test should invoke
its neighbors during the test.
An example will show how these ﬁt together. This test asserts that an
AuctionMessageTranslator will parse a given message text to generate
an auctionClosed() event. For now, just concentrate on the structure; the test
will turn up again in context in Chapter 12.
25
jMock2: Mock Objects


---
**Page 26**

@RunWith(JMock.class) 1
public class AuctionMessageTranslatorTest {
  private final Mockery context = new JUnit4Mockery(); 2
  private final AuctionEventListener listener =  
                              context.mock(AuctionEventListener.class); 3
  private final AuctionMessageTranslator translator = 
                                new AuctionMessageTranslator(listener); 4
  @Test public void
notifiesAuctionClosedWhenCloseMessageReceived() {
    Message message = new Message();
    message.setBody("SOLVersion: 1.1; Event: CLOSE;"); 5
    context.checking(new Expectations() {{ 6
      oneOf(listener).auctionClosed(); 7
    }});
    translator.processMessage(UNUSED_CHAT, message); 8
  } 9
}
1
The @RunWith(JMock.class) annotation tells JUnit to use the jMock test
runner, which automatically calls the mockery at the end of the test to check
that all mock objects have been invoked as expected.
2
The test creates the Mockery. Since this is a JUnit 4 test, it creates a
JUnit4Mockery which throws the right type of exception to report test failures
to JUnit 4. By convention, jMock tests hold the mockery in a ﬁeld named
context, because it represents the context of the object under test.
3
The test uses the mockery to create a mock AuctionEventListener that will
stand in for a real listener implementation during this test.
4
The test instantiates the object under test, an AuctionMessageTranslator,
passing the mock listener to its constructor. The AuctionMessageTranslator
does not distinguish between a real and a mock listener: It communicates
through the AuctionEventListener interface and does not care how that
interface is implemented.
5
The test sets up further objects that will be used in the test.
6
The test then tells the mockery how the translator should invoke its neighbors
during the test by deﬁning a block of expectations. The Java syntax we use
to do this is obscure, so if you can bear with us for now we explain it in
more detail in Appendix A.
7
This is the signiﬁcant line in the test, its one expectation. It says that, during
the action, we expect the listener’s auctionClosed() method to be called
exactly once. Our deﬁnition of success is that the translator will notify its
Chapter 3
An Introduction to the Tools
26


---
**Page 27**

listener that an auctionClosed() event has happened whenever it receives a
raw Close message.
8
This is the call to the object under test, the outside event that triggers the
behavior we want to test. It passes a raw Close message to the translator
which, the test says, should make the translator call auctionClosed() once
on the listener. The mockery will check that the mock objects are invoked
as expected while the test runs and fail the test immediately if they are
invoked unexpectedly.
9
Note that the test does not require any assertions. This is quite common in
mock object tests.
Expectations
The example above speciﬁes one very simple expectation. jMock’s expectation
API is very expressive. It lets you precisely specify:
•
The minimum and maximum number of times an invocation is expected;
•
Whether an invocation is expected (the test should fail if it is not received)
or merely allowed to happen (the test should pass if it is not received);
•
The parameter values, either given literally or constrained by Hamcrest
matchers;
•
The ordering constraints with respect to other expectations; and,
•
What should happen when the method is invoked—a value to return, an
exception to throw, or any other behavior.
An expectation block is designed to stand out from the test code that surrounds
it, making an obvious separation between the code that describes how neighboring
objects should be invoked and the code that actually invokes objects and tests
the results. The code within an expectation block acts as a little declarative
language that describes the expectations; we’ll return to this idea in “Building
Up to Higher-Level Programming” (page 65).
There’s more to the jMock API which we don’t have space for in this chapter;
we’ll describe more of its features in examples in the rest of the book, and there’s
a summary in Appendix A. What really matters, however, is not the implementa-
tion we happened to come up with, but its underlying concepts and motivations.
We will do our best to make them clear.
27
jMock2: Mock Objects


---
**Page 28**

This page intentionally left blank 


---
**Page 29**

Part II
The Process of Test-Driven
Development
So far we’ve presented a high-level introduction to the concept
of, and motivation for, incremental test-driven development. In
the rest of the book, we’ll ﬁll in the practical details that actually
make it work.
In this part we introduce the concepts that deﬁne our ap-
proach. These boil down to two core principles: continuous
incremental development and expressive code.


---
**Page 30**

This page intentionally left blank 


---
**Page 31**

Chapter 4
Kick-Starting the Test-Driven
Cycle
We should be taught not to wait for inspiration to start a thing. Action
always generates inspiration. Inspiration seldom generates action.
—Frank Tibolt
Introduction
The TDD process we described in Chapter 1 assumes that we can grow the system
by just slotting the tests for new features into an existing infrastructure. But what
about the very ﬁrst feature, before we have this infrastructure? As an acceptance
test, it must run end-to-end to give us the feedback we need about the system’s
external interfaces, which means we must have implemented a whole automated
build, deploy, and test cycle. This is a lot of work to do before we can even see
our ﬁrst test fail.
Deploying and testing right from the start of a project forces the team to un-
derstand how their system ﬁts into the world. It ﬂushes out the “unknown
unknown” technical and organizational risks so they can be addressed while
there’s still time. Attempting to deploy also helps the team understand who they
need to liaise with, such as system administrators or external vendors, and start
to build those relationships.
Starting with “build, deploy, and test” on a nonexistent system sounds odd,
but we think it’s essential. The risks of leaving it to later are just too high. We
have seen projects canceled after months of development because they could not
reliably deploy their system. We have seen systems discarded because new features
required months of manual regression testing and even then the error rates were
too high. As always, we view feedback as a fundamental tool, and we want to
know as early as possible whether we’re moving in the right direction. Then,
once we have our ﬁrst test in place, subsequent tests will be much quicker to write.
31



# 3.3 Hamcrest Matchers and assertThat() (pp.24-25)

---
**Page 24**

annotation.2 JUnit provides a small library of test runners. For example, the
Parameterized test runner lets you write data-driven tests in which the same test
methods are run for many different data values returned from a static method.
As we’ll see below, the jMock library uses a custom test runner to automatically
verify mock objects at the end of the test, before the test ﬁxture is torn down.
Hamcrest Matchers and assertThat()
Hamcrest is a framework for writing declarative match criteria. While not a
testing framework itself, Hamcrest is used by several testing frameworks, including
JUnit, jMock, and WindowLicker, which we use in the example in Part III.
A Hamcrest matcher reports whether a given object matches some criteria, can
describe its criteria, and can describe why an object does not meet its criteria.
For example, this code creates matchers for strings that contain a given substring
and uses them to make some assertions:
String s = "yes we have no bananas today";
Matcher<String> containsBananas = new StringContains("bananas");
Matcher<String> containsMangoes = new StringContains("mangoes");
assertTrue(containsBananas.matches(s));
assertFalse(containsMangoes.matches(s));
Matchers are not usually instantiated directly. Instead, Hamcrest provides
static factory methods for all of its matchers to make the code that creates
matchers more readable. For example:
assertTrue(containsString("bananas").matches(s));
assertFalse(containsString("mangoes").matches(s));
In practice, however, we use matchers in combination with JUnit’s
assertThat(), which uses matcher’s self-describing features to make clear exactly
what went wrong when an assertion fails.3 We can rewrite the assertions as:
assertThat(s, containsString("bananas"));
assertThat(s, not(containsString("mangoes"));
The second assertion demonstrates one of Hamcrest’s most useful features:
deﬁning new criteria by combining existing matchers. The not() method is a
factory function that creates a matcher that reverses the sense of any matcher
passed to it. Matchers are designed so that when they’re combined, both the code
and the failure messages are self-explanatory. For example, if we change the
second assertion to fail:
2. By the time of publication, JUnit will also have a Rule annotation for ﬁelds to support
objects that can “intercept” the lifecycle of a test run.
3. The assertThat() method was introduced in JUnit 4.5.
Chapter 3
An Introduction to the Tools
24


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



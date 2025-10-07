Line 1: 
Line 2: --- 페이지 46 ---
Line 3: Chapter 3
Line 4: An Introduction to the Tools
Line 5: Man is a tool-using animal. Without tools he is nothing, with tools he
Line 6: is all.
Line 7: —Thomas Carlyle
Line 8: Stop Me If You’ve Heard This One Before
Line 9: This book is about the techniques of using tests to guide the development of
Line 10: object-oriented software, not about speciﬁc technologies. To demonstrate the
Line 11: techniques in action, however, we’ve had to pick some technologies for our ex-
Line 12: ample code. For the rest of the book we’re going to use Java, with the JUnit 4,
Line 13: Hamcrest, and jMock2 frameworks. If you’re using something else, we hope
Line 14: we’ve been clear enough so that you can apply these ideas in your environment.
Line 15: In this chapter we brieﬂy describe the programming interfaces for these three
Line 16: frameworks, just enough to help you make sense of the code examples in the rest
Line 17: of the book. If you already know how to use them, you can skip this chapter.
Line 18: A Minimal Introduction to JUnit 4
Line 19: We use JUnit 4 (version 4.6 at the time of writing) as our Java test framework.1
Line 20: In essence, JUnit uses reﬂection to walk the structure of a class and run whatever
Line 21: it can ﬁnd in that class that represents a test. For example, here’s a test that
Line 22: exercises a Catalog class which manages a collection of Entry objects:
Line 23: public class CatalogTest {
Line 24:   private final Catalog catalog = new Catalog();
Line 25:   @Test public void containsAnAddedEntry() { 
Line 26:     Entry entry = new Entry("fish", "chips");
Line 27:     catalog.add(entry);
Line 28:     assertTrue(catalog.contains(entry));
Line 29:   }
Line 30:   @Test public void indexesEntriesByName() {
Line 31:     Entry entry = new Entry("fish", "chips");
Line 32:     catalog.add(entry);
Line 33:     assertEquals(entry, catalog.entryFor("fish"));  
Line 34:     assertNull(catalog.entryFor("missing name"));  
Line 35:   }
Line 36: }
Line 37: 1. JUnit is bundled with many Java IDEs and is available at www.junit.org.
Line 38: 21
Line 39: 
Line 40: --- 페이지 47 ---
Line 41: Test Cases
Line 42: JUnit treats any method annotated with @Test as a test case; test methods must
Line 43: have neither a return value nor parameters. In this case, CatalogTest deﬁnes two
Line 44: tests, called containsAnAddedEntry() and indexesEntriesByName().
Line 45: To run a test, JUnit creates a new instance of the test class and calls the relevant
Line 46: test method. Creating a new test object each time ensures that the tests are isolated
Line 47: from each other, because the test object’s ﬁelds are replaced before each test.
Line 48: This means that a test is free to change the contents of any of the test object ﬁelds.
Line 49: NUnit Behaves Differently from JUnit
Line 50: Those working in .Net should note that NUnit reuses the same instance of the test
Line 51: object for all the test methods, so any values that might change must either be
Line 52: reset in [Setup] and [TearDown] methods (if they’re ﬁelds) or made local to the
Line 53: test method.
Line 54: Assertions
Line 55: A JUnit test invokes the object under test and then makes assertions about the
Line 56: results, usually using assertion methods deﬁned by JUnit which generate useful
Line 57: error messages when they fail.
Line 58: CatalogTest, for example, uses three of JUnit’s assertions: assertTrue()
Line 59: asserts that an expression is true; assertNull() asserts that an object reference
Line 60: is null; and assertEquals() asserts that two values are equal. When it fails,
Line 61: assertEquals() reports the expected and actual values that were compared.
Line 62: Expecting Exceptions
Line 63: The @Test annotation supports an optional parameter expected that declares
Line 64: that the test case should throw an exception. The test fails if it does not throw
Line 65: an exception or if it throws an exception of a different type.
Line 66: For example, the following test checks that a Catalog throws an
Line 67: IllegalArgumentException when two entries are added with the same name:
Line 68: @Test(expected=IllegalArgumentException.class)
Line 69: public void cannotAddTwoEntriesWithTheSameName() {
Line 70:   catalog.add(new Entry("fish", "chips");
Line 71:   catalog.add(new Entry("fish", "peas");
Line 72: }
Line 73: Chapter 3
Line 74: An Introduction to the Tools
Line 75: 22
Line 76: 
Line 77: --- 페이지 48 ---
Line 78: Test Fixtures
Line 79: A test ﬁxture is the ﬁxed state that exists at the start of a test. A test ﬁxture ensures
Line 80: that a test is repeatable—every time a test is run it starts in the same state so it
Line 81: should produce the same results. A ﬁxture may be set up before the test runs and
Line 82: torn down after it has ﬁnished.
Line 83: The ﬁxture for a JUnit test is managed by the class that deﬁnes the test and is
Line 84: stored in the object’s ﬁelds. All tests deﬁned in the same class start with an iden-
Line 85: tical ﬁxture and may modify that ﬁxture as they run. For CatalogTest, the ﬁxture
Line 86: is the empty Catalog object held in its catalog ﬁeld.
Line 87: The ﬁxture is usually set up by ﬁeld initializers. It can also be set up by the
Line 88: constructor of the test class or instance initializer blocks. JUnit also lets you
Line 89: identify methods that set up and tear down the ﬁxture with annotations. JUnit
Line 90: will run all methods annotated with @Before before running the tests, to set up
Line 91: the ﬁxture, and those annotated by @After after it has run the test, to tear
Line 92: down the ﬁxture. Many JUnit tests do not need to explicitly tear down the ﬁxture
Line 93: because it is enough to let the JVM garbage collect any objects created when it
Line 94: was set up.
Line 95: For example, all the tests in CatalogTest initialize the catalog with the same
Line 96: entry. This common initialization can be moved into a ﬁeld initializer and @Before
Line 97: method:
Line 98: public class CatalogTest {
Line 99:   final Catalog catalog = new Catalog();
Line 100: final Entry entry = new Entry("fish", "chips");
Line 101: @Before public void fillTheCatalog() {
Line 102:     catalog.add(entry);
Line 103:   }
Line 104:   @Test public void containsAnAddedEntry() {
Line 105:     assertTrue(catalog.contains(entry));
Line 106:   }
Line 107:   @Test public void indexesEntriesByName() {
Line 108:     assertEquals(equalTo(entry), catalog.entryFor("fish"));  
Line 109:     assertNull(catalog.entryFor("missing name"));  
Line 110:   }
Line 111:   @Test(expected=IllegalArgumentException.class)
Line 112:   public void cannotAddTwoEntriesWithTheSameName() {
Line 113:     catalog.add(new Entry("fish", "peas");
Line 114:   }
Line 115: }
Line 116: Test Runners
Line 117: The way JUnit reﬂects on a class to ﬁnd tests and then runs those tests is controlled
Line 118: by a test runner. The runner used for a class can be conﬁgured with the @RunWith
Line 119: 23
Line 120: A Minimal Introduction to JUnit 4
Line 121: 
Line 122: --- 페이지 49 ---
Line 123: annotation.2 JUnit provides a small library of test runners. For example, the
Line 124: Parameterized test runner lets you write data-driven tests in which the same test
Line 125: methods are run for many different data values returned from a static method.
Line 126: As we’ll see below, the jMock library uses a custom test runner to automatically
Line 127: verify mock objects at the end of the test, before the test ﬁxture is torn down.
Line 128: Hamcrest Matchers and assertThat()
Line 129: Hamcrest is a framework for writing declarative match criteria. While not a
Line 130: testing framework itself, Hamcrest is used by several testing frameworks, including
Line 131: JUnit, jMock, and WindowLicker, which we use in the example in Part III.
Line 132: A Hamcrest matcher reports whether a given object matches some criteria, can
Line 133: describe its criteria, and can describe why an object does not meet its criteria.
Line 134: For example, this code creates matchers for strings that contain a given substring
Line 135: and uses them to make some assertions:
Line 136: String s = "yes we have no bananas today";
Line 137: Matcher<String> containsBananas = new StringContains("bananas");
Line 138: Matcher<String> containsMangoes = new StringContains("mangoes");
Line 139: assertTrue(containsBananas.matches(s));
Line 140: assertFalse(containsMangoes.matches(s));
Line 141: Matchers are not usually instantiated directly. Instead, Hamcrest provides
Line 142: static factory methods for all of its matchers to make the code that creates
Line 143: matchers more readable. For example:
Line 144: assertTrue(containsString("bananas").matches(s));
Line 145: assertFalse(containsString("mangoes").matches(s));
Line 146: In practice, however, we use matchers in combination with JUnit’s
Line 147: assertThat(), which uses matcher’s self-describing features to make clear exactly
Line 148: what went wrong when an assertion fails.3 We can rewrite the assertions as:
Line 149: assertThat(s, containsString("bananas"));
Line 150: assertThat(s, not(containsString("mangoes"));
Line 151: The second assertion demonstrates one of Hamcrest’s most useful features:
Line 152: deﬁning new criteria by combining existing matchers. The not() method is a
Line 153: factory function that creates a matcher that reverses the sense of any matcher
Line 154: passed to it. Matchers are designed so that when they’re combined, both the code
Line 155: and the failure messages are self-explanatory. For example, if we change the
Line 156: second assertion to fail:
Line 157: 2. By the time of publication, JUnit will also have a Rule annotation for ﬁelds to support
Line 158: objects that can “intercept” the lifecycle of a test run.
Line 159: 3. The assertThat() method was introduced in JUnit 4.5.
Line 160: Chapter 3
Line 161: An Introduction to the Tools
Line 162: 24
Line 163: 
Line 164: --- 페이지 50 ---
Line 165: assertThat(s, not(containsString("bananas"));
Line 166: the failure report is:
Line 167: java.lang.AssertionError: 
Line 168: Expected: not a string containing "bananas"
Line 169:      got: "Yes, we have no bananas"
Line 170: Instead of writing code to explicitly check a condition and to generate an in-
Line 171: formative error message, we can pass a matcher expression to assertThat() and
Line 172: let it do the work.
Line 173: Hamcrest is also user-extensible. If we need to check a speciﬁc condition,
Line 174: we can write a new matcher by implementing the Matcher interface and an
Line 175: appropriately-named factory method, and the result will combine seamlessly with
Line 176: the existing matcher expressions. We describe how to write custom Hamcrest
Line 177: matchers in Appendix B.
Line 178: jMock2: Mock Objects
Line 179: jMock2 plugs into JUnit (and other test frameworks) providing support for the
Line 180: mock objects testing style introduced in Chapter 2. jMock creates mock objects
Line 181: dynamically, so you don’t have to write your own implementations of the types
Line 182: you want to mock. It also provides a high-level API for specifying how the object
Line 183: under test should invoke the mock objects it interacts with, and how the mock
Line 184: objects will behave in response.
Line 185: Understanding jMock
Line 186: jMock is designed to make the expectation descriptions as clear as possible. We
Line 187: used some unusual Java coding practices to do so, which can appear surprising
Line 188: at ﬁrst. jMock’s design was motivated by the ideas presented in this book, backed
Line 189: by many years of experience in real projects. If the examples don’t make sense to
Line 190: you, there’s more description in Appendix A and at www.jmock.org.We (of course)
Line 191: believe that it’s worth suspending your judgment until you’ve had a chance to work
Line 192: through some of the examples.
Line 193: The core concepts of the jMock API are the mockery, mock objects, and expec-
Line 194: tations. A mockery represents the context of the object under test, its neighboring
Line 195: objects; mock objects stand in for the real neighbors of the object under test while
Line 196: the test runs; and expectations describe how the object under test should invoke
Line 197: its neighbors during the test.
Line 198: An example will show how these ﬁt together. This test asserts that an
Line 199: AuctionMessageTranslator will parse a given message text to generate
Line 200: an auctionClosed() event. For now, just concentrate on the structure; the test
Line 201: will turn up again in context in Chapter 12.
Line 202: 25
Line 203: jMock2: Mock Objects
Line 204: 
Line 205: --- 페이지 51 ---
Line 206: @RunWith(JMock.class) 1
Line 207: public class AuctionMessageTranslatorTest {
Line 208:   private final Mockery context = new JUnit4Mockery(); 2
Line 209:   private final AuctionEventListener listener =  
Line 210:                               context.mock(AuctionEventListener.class); 3
Line 211:   private final AuctionMessageTranslator translator = 
Line 212:                                 new AuctionMessageTranslator(listener); 4
Line 213:   @Test public void
Line 214: notifiesAuctionClosedWhenCloseMessageReceived() {
Line 215:     Message message = new Message();
Line 216:     message.setBody("SOLVersion: 1.1; Event: CLOSE;"); 5
Line 217:     context.checking(new Expectations() {{ 6
Line 218:       oneOf(listener).auctionClosed(); 7
Line 219:     }});
Line 220:     translator.processMessage(UNUSED_CHAT, message); 8
Line 221:   } 9
Line 222: }
Line 223: 1
Line 224: The @RunWith(JMock.class) annotation tells JUnit to use the jMock test
Line 225: runner, which automatically calls the mockery at the end of the test to check
Line 226: that all mock objects have been invoked as expected.
Line 227: 2
Line 228: The test creates the Mockery. Since this is a JUnit 4 test, it creates a
Line 229: JUnit4Mockery which throws the right type of exception to report test failures
Line 230: to JUnit 4. By convention, jMock tests hold the mockery in a ﬁeld named
Line 231: context, because it represents the context of the object under test.
Line 232: 3
Line 233: The test uses the mockery to create a mock AuctionEventListener that will
Line 234: stand in for a real listener implementation during this test.
Line 235: 4
Line 236: The test instantiates the object under test, an AuctionMessageTranslator,
Line 237: passing the mock listener to its constructor. The AuctionMessageTranslator
Line 238: does not distinguish between a real and a mock listener: It communicates
Line 239: through the AuctionEventListener interface and does not care how that
Line 240: interface is implemented.
Line 241: 5
Line 242: The test sets up further objects that will be used in the test.
Line 243: 6
Line 244: The test then tells the mockery how the translator should invoke its neighbors
Line 245: during the test by deﬁning a block of expectations. The Java syntax we use
Line 246: to do this is obscure, so if you can bear with us for now we explain it in
Line 247: more detail in Appendix A.
Line 248: 7
Line 249: This is the signiﬁcant line in the test, its one expectation. It says that, during
Line 250: the action, we expect the listener’s auctionClosed() method to be called
Line 251: exactly once. Our deﬁnition of success is that the translator will notify its
Line 252: Chapter 3
Line 253: An Introduction to the Tools
Line 254: 26
Line 255: 
Line 256: --- 페이지 52 ---
Line 257: listener that an auctionClosed() event has happened whenever it receives a
Line 258: raw Close message.
Line 259: 8
Line 260: This is the call to the object under test, the outside event that triggers the
Line 261: behavior we want to test. It passes a raw Close message to the translator
Line 262: which, the test says, should make the translator call auctionClosed() once
Line 263: on the listener. The mockery will check that the mock objects are invoked
Line 264: as expected while the test runs and fail the test immediately if they are
Line 265: invoked unexpectedly.
Line 266: 9
Line 267: Note that the test does not require any assertions. This is quite common in
Line 268: mock object tests.
Line 269: Expectations
Line 270: The example above speciﬁes one very simple expectation. jMock’s expectation
Line 271: API is very expressive. It lets you precisely specify:
Line 272: •
Line 273: The minimum and maximum number of times an invocation is expected;
Line 274: •
Line 275: Whether an invocation is expected (the test should fail if it is not received)
Line 276: or merely allowed to happen (the test should pass if it is not received);
Line 277: •
Line 278: The parameter values, either given literally or constrained by Hamcrest
Line 279: matchers;
Line 280: •
Line 281: The ordering constraints with respect to other expectations; and,
Line 282: •
Line 283: What should happen when the method is invoked—a value to return, an
Line 284: exception to throw, or any other behavior.
Line 285: An expectation block is designed to stand out from the test code that surrounds
Line 286: it, making an obvious separation between the code that describes how neighboring
Line 287: objects should be invoked and the code that actually invokes objects and tests
Line 288: the results. The code within an expectation block acts as a little declarative
Line 289: language that describes the expectations; we’ll return to this idea in “Building
Line 290: Up to Higher-Level Programming” (page 65).
Line 291: There’s more to the jMock API which we don’t have space for in this chapter;
Line 292: we’ll describe more of its features in examples in the rest of the book, and there’s
Line 293: a summary in Appendix A. What really matters, however, is not the implementa-
Line 294: tion we happened to come up with, but its underlying concepts and motivations.
Line 295: We will do our best to make them clear.
Line 296: 27
Line 297: jMock2: Mock Objects
Line 298: 
Line 299: --- 페이지 53 ---
Line 300: This page intentionally left blank 
Line 1: 
Line 2: --- 페이지 272 ---
Line 3: Chapter 21
Line 4: Test Readability
Line 5: To design is to communicate clearly by whatever means you can control
Line 6: or master.
Line 7: —Milton Glaser
Line 8: Introduction
Line 9: Teams that adopt TDD usually see an early boost in productivity because the
Line 10: tests let them add features with conﬁdence and catch errors immediately. For
Line 11: some teams, the pace then slows down as the tests themselves become a mainte-
Line 12: nance burden. For TDD to be sustainable, the tests must do more than verify the
Line 13: behavior of the code; they must also express that behavior clearly—they must
Line 14: be readable. This matters for the same reason that code readability matters: every
Line 15: time the developers have to stop and puzzle through a test to ﬁgure out what it
Line 16: means, they have less time left to spend on creating new features, and the team
Line 17: velocity drops.
Line 18: We take as much care about writing our test code as about production code,
Line 19: but with differences in style since the two types of code serve different purposes.
Line 20: Test code should describe what the production code does. That means that it
Line 21: tends to be concrete about the values it uses as examples of what results to expect,
Line 22: but abstract about how the code works. Production code, on the other hand,
Line 23: tends to be abstract about the values it operates on but concrete about how it
Line 24: gets the job done. Similarly, when writing production code, we have to consider
Line 25: how we will compose our objects to make up a working system, and manage
Line 26: their dependencies carefully. Test code, on the other hand, is at the end of the
Line 27: dependency chain, so it’s more important for it to express the intention of its
Line 28: target code than to plug into a web of other objects. We want our test code to
Line 29: read like a declarative description of what is being tested.
Line 30: In this chapter, we’ll describe some practices that we’ve found helpful to keep
Line 31: our tests readable and expressive.
Line 32: 247
Line 33: 
Line 34: --- 페이지 273 ---
Line 35: Could Do Better1
Line 36: We’ve seen many unit test suites that could be much more effective given a
Line 37: little extra attention. They have too many “test smells” of the kind cataloged in
Line 38: [Meszaros07], as well as in our own Chapters 20 and 24.When cleaning up tests,
Line 39: or just trying to write new ones, the readability problems we watch out for are:
Line 40: •
Line 41: Test names that do not clearly describe the point of each test case and its
Line 42: differences from the other test cases;
Line 43: •
Line 44: Single test cases that seem to be exercising multiple features;
Line 45: •
Line 46: Tests with different structure, so the reader cannot skim-read them to
Line 47: understand their intention;
Line 48: •
Line 49: Tests with lots of code for setting up and handling exceptions, which buries
Line 50: their essential logic; and,
Line 51: •
Line 52: Tests that use literal values (“magic numbers”) but are not clear about what,
Line 53: if anything, is signiﬁcant about those values.
Line 54: Test Names Describe Features
Line 55: The name of the test should be the ﬁrst clue for a developer to understand what
Line 56: is being tested and how the target object is supposed to behave.
Line 57: Not every team we’ve worked with follows this principle. Some naive developers
Line 58: use names that don’t mean anything at all:
Line 59: public class TargetObjectTest {
Line 60:   @Test public void test1() { […]
Line 61:   @Test public void test2() { […]
Line 62:   @Test public void test3() { […]
Line 63: We don’t see many of these nowadays; the world has moved on. A common
Line 64: approach is to name a test after the method it’s exercising:
Line 65: public class TargetObjectTest {
Line 66:   @Test public void isReady() { […]
Line 67:   @Test public void choose() { […]
Line 68:   @Test public void choose1() { […]
Line 69: public class TargetObject  {
Line 70:   public void isReady() { […]
Line 71:   public void choose(Picker picker) { […]
Line 72: perhaps with multiple tests for different paths through the same method.
Line 73: 1. This is (or was) a common phrase in UK school reports for children whose schoolwork
Line 74: isn’t as good as it could be.
Line 75: Chapter 21
Line 76: Test Readability
Line 77: 248
Line 78: 
Line 79: --- 페이지 274 ---
Line 80: At best, such names duplicate the information a developer could get just by
Line 81: looking at the target class; they break the “Don’t Repeat Yourself” principle
Line 82: [Hunt99]. We don’t need to know that TargetObject has a choose() method—we
Line 83: need to know what the object does in different situations, what the method is for.
Line 84: A better alternative is to name tests in terms of the features that the target
Line 85: object provides. We use a TestDox convention (invented by Chris Stevenson)
Line 86: where each test name reads like a sentence, with the target class as the implicit
Line 87: subject. For example,
Line 88: •
Line 89: A List holds items in the order they were added.
Line 90: •
Line 91: A List can hold multiple references to the same item.
Line 92: •
Line 93: A List throws an exception when removing an item it doesn’t hold.
Line 94: We can translate these directly to method names:
Line 95: public class ListTests {
Line 96:   @Test public void holdsItemsInTheOrderTheyWereAdded() { […]
Line 97:   @Test public void canHoldMultipleReferencesToTheSameItem() { […]
Line 98:   @Test public void throwsAnExceptionWhenRemovingAnItemItDoesntHold() { […]
Line 99: These names can be as long as we like because they’re only called through
Line 100: reﬂection—we never have to type them in to call them.
Line 101: The point of the convention is to encourage the developer to think in terms of
Line 102: what the target object does, not what it is. It’s also very compatible with our in-
Line 103: cremental approach of adding a feature at a time to an existing codebase. It gives
Line 104: us a consistent style of naming all the way from user stories, through tasks and
Line 105: acceptance tests, to unit tests—as you saw in Part III.
Line 106: As a matter of style, the test name should say something about the expected
Line 107: result, the action on the object, and the motivation for the scenario. For example,
Line 108: if we were testing a ConnectionMonitor class, then
Line 109: pollsTheServersMonitoringPort()
Line 110: doesn’t tell us enough: why does it poll, what happens when it gets a result? On
Line 111: the other hand,
Line 112: notifiesListenersThatServerIsUnavailableWhenCannotConnectToItsMonitoringPort()
Line 113: explains both the scenario and the expected behavior. We’ll show later how this
Line 114: style of naming maps onto our standard test structures.
Line 115: 249
Line 116: Test Names Describe Features
Line 117: 
Line 118: --- 페이지 275 ---
Line 119: Test Name First or Last?
Line 120: We’ve noticed that some developers start with a placeholder name, ﬁll out the body
Line 121: of the test, and then decide what to call it. Others (such as Steve) like to decide
Line 122: the test name ﬁrst, to clarify their intentions, before writing any test code. Both ap-
Line 123: proaches work as long as the developer follows through and makes sure that the
Line 124: test is, in the end, consistent and expressive.
Line 125: The TestDox format fulﬁlls the early promise of TDD—that the tests should
Line 126: act as documentation for the code. There are tools and IDE plug-ins that unpack
Line 127: the “camel case” method names and link them to the class under test, such
Line 128: as the TestDox plug-in for the IntelliJ IDE; Figure 21.1 shows the automatic
Line 129: documentation for a KeyboardLayout class.
Line 130: Figure 21.1
Line 131: The TestDox IntelliJ plug-in
Line 132: Regularly Read Documentation Generated from Tests
Line 133: We ﬁnd that such generated documentation gives us a fresh perspective on the
Line 134: test names, highlighting the problems we’re too close to the code to see. For
Line 135: example, when generating the screenshot for Figure 21.1, Nat noticed that the
Line 136: name of the ﬁrst test is unclear—it should be “translates numbers to key strokes
Line 137: in all known layouts.”
Line 138: We make an effort to at least skim-read the documentation regularly during
Line 139: development.
Line 140: Chapter 21
Line 141: Test Readability
Line 142: 250
Line 143: 
Line 144: --- 페이지 276 ---
Line 145: Canonical Test Structure
Line 146: We ﬁnd that if we write our tests in a standard form, they’re easier to
Line 147: understand. We can skim-read to ﬁnd expectations and assertions quickly and
Line 148: see how they relate to the code under test. If we’re ﬁnding it difﬁcult to write a
Line 149: test in a standard form, that’s often a hint that the code is too complicated or
Line 150: that we haven’t quite clariﬁed our ideas.
Line 151: The most common form for a test is:
Line 152: 1.
Line 153: Setup: prepare the context of the test, the environment in which the target
Line 154: code will run;
Line 155: 2.
Line 156: Execute: call the target code, triggering the tested behavior;
Line 157: 3.
Line 158: Verify: check for a visible effect that we expect from the behavior; and,
Line 159: 4.
Line 160: Teardown: clean up any leftover state that might corrupt other tests.
Line 161: There are other versions of this form, such as “Arrange, Act, Assert,” which
Line 162: collapse some of the stages.
Line 163: For example:
Line 164: public class StringTemplateTest {
Line 165:   @Test public void expandsMacrosSurroundedWithBraces() {
Line 166:     StringTemplate template = new StringTemplate("{a}{b}"); // Setup
Line 167:     HashMap<String,Object> macros = new HashMap<String,Object>();
Line 168:     macros.put("a", "A");
Line 169:     macros.put("b", "B");
Line 170:     String expanded = template.expand(macros);              // Execute
Line 171:     assertThat(expanded, equalTo("AB"));                    // Assert
Line 172:   }                                                         // No Teardown
Line 173: }
Line 174: Tests that set expectations on mock objects use a variant of this structure where
Line 175: some of the assertions are declared before the execute stage and are implicitly
Line 176: checked afterwards—for example, in LoggingXMPPFailureReporterTest from
Line 177: Chapter 19:
Line 178: @RunWith(JMock.class)
Line 179: public class LoggingXMPPFailureReporterTest {
Line 180:   private final Mockery context = new Mockery() {{  // Setup
Line 181:    setImposteriser(ClassImposteriser.INSTANCE); 
Line 182:   }};
Line 183:   final Logger logger = context.mock(Logger.class);
Line 184:   final LoggingXMPPFailureReporter reporter = new LoggingXMPPFailureReporter(logger);
Line 185: 251
Line 186: Canonical Test Structure
Line 187: 
Line 188: --- 페이지 277 ---
Line 189:   @Test public void writesMessageTranslationFailureToLog() {
Line 190:     Exception exception = new Exception("an exception");
Line 191:     context.checking(new Expectations() {{          // Expect
Line 192:       oneOf(logger).severe( expected log message here);
Line 193:     }});
Line 194:     reporter.cannotTranslateMessage("auction id",   // Execute
Line 195:                                     "failed message", exception); 
Line 196: // implicitly check expectations are satisfied
Line 197: // Assert
Line 198:   }
Line 199:   @AfterClass public static void resetLogging() {   // Teardown
Line 200:     LogManager.getLogManager().reset();
Line 201:   }  
Line 202: }
Line 203: Write Tests Backwards
Line 204: Although we stick to a canonical format for test code, we don’t necessarily write
Line 205: tests from top to bottom. What we often do is: write the test name, which helps us
Line 206: decide what we want to achieve; write the call to the target code, which is the entry
Line 207: point for the feature; write the expectations and assertions, so we know what effects
Line 208: the feature should have; and, write the setup and teardown to deﬁne the context
Line 209: for the test. Of course, there may be some blurring of these steps to help the
Line 210: compiler, but this sequence reﬂects how we tend to think through a new unit test.
Line 211: Then we run it and watch it fail.
Line 212: How Many Assertions in a Test Method?
Line 213: Some TDD practitioners suggest that each test should only contain one expectation
Line 214: or assertion.This is useful as a training rule when learning TDD, to avoid asserting
Line 215: everything the developer can think of, but we don’t ﬁnd it practical. A better rule
Line 216: is to think of one coherent feature per test, which might be represented by up to
Line 217: a handful of assertions. If a single test seems to be making assertions about
Line 218: different features of a target object, it might be worth splitting up. Once again,
Line 219: expressiveness is the key: as a reader of this test, can I ﬁgure out what’s
Line 220: signiﬁcant?
Line 221: Streamline the Test Code
Line 222: All code should emphasize “what” it does over “how,” including test code; the
Line 223: more implementation detail is included in a test method, the harder it is for
Line 224: the reader to understand what’s important. We try to move everything out
Line 225: of the test method that doesn’t contribute to the description, in domain
Line 226: terms, of the feature being exercised. Sometimes that involves restructuring the
Line 227: code, sometimes just ignoring the syntax noise.
Line 228: Chapter 21
Line 229: Test Readability
Line 230: 252
Line 231: 
Line 232: --- 페이지 278 ---
Line 233: Use Structure to Explain
Line 234: As you’ll have seen throughout Part III, we make a point of following “Small
Line 235: Methods to Express Intent” (page 226), even to the extent of writing a tiny
Line 236: method like translatorFor() just to reduce the Java syntax noise. This ﬁts
Line 237: nicely into the Hamcrest approach, where the assertThat() and jMock expecta-
Line 238: tion syntaxes are designed to allow developers to compose small features into a
Line 239: (more or less) readable description of an assertion. For example,
Line 240: assertThat(instruments, hasItem(instrumentWithPrice(greaterThan(81))));
Line 241: checks whether the collection instruments has at least one Instrument with a
Line 242: strikePrice property greater than 81. The assertion line expresses our intent,
Line 243: the helper method creates a matcher that checks the value:
Line 244: private Matcher<? super Instrument> 
Line 245: instrumentWithPrice(Matcher<? super Integer> priceMatcher) {
Line 246:   return new FeatureMatcher<Instrument, Integer>(
Line 247:                priceMatcher, "instrument at price", "price") {
Line 248:     @Override protected Integer featureValueOf(Instrument actual) {
Line 249:       return actual.getStrikePrice();
Line 250:     }
Line 251:   };
Line 252: }
Line 253: This may create more program text in the end, but we’re prioritizing expressive-
Line 254: ness over minimizing the source lines.
Line 255: Use Structure to Share
Line 256: We also extract common features into methods that can be shared between tests
Line 257: for setting up values, tearing down state, making assertions, and occasionally
Line 258: triggering the event. For example, in Chapter 19, we exploited jMock’s facility
Line 259: for setting multiple expectation blocks to write a expectSniperToFailWhenItIs()
Line 260: method that wraps up repeated behavior behind a descriptive name.
Line 261: The only caution with factoring out test structure is that, as we said in the in-
Line 262: troduction to this chapter, we have to be careful not to make a test so abstract
Line 263: that we cannot see what it does any more. Our highest concern is making the
Line 264: test describe what the target code does, so we refactor enough to be able to see
Line 265: its ﬂow, but we don’t always refactor as hard as we would for production code.
Line 266: Accentuate the Positive
Line 267: We only catch exceptions in a test if we want to assert something about them. We
Line 268: sometimes see tests like this:
Line 269: 253
Line 270: Streamline the Test Code
Line 271: 
Line 272: --- 페이지 279 ---
Line 273: @Test public void expandsMacrosSurroundedWithBraces() {
Line 274:   StringTemplate template = new StringTemplate("{a}{b}");
Line 275:   try {
Line 276:     String expanded = template.expand(macros);
Line 277:     assertThat(expanded, equalTo("AB"));
Line 278:   } catch (TemplateFormatException e) {
Line 279:     fail("Template failed: " + e);
Line 280:   }
Line 281: }
Line 282: If this test is intended to pass, then converting the exception actually drops infor-
Line 283: mation from the stack trace. The simplest thing to do is to let the exception
Line 284: propagate for the test runtime to catch. We can add arbitrary exceptions to the
Line 285: test method signature because it’s only called by reﬂection. This removes at least
Line 286: half the lines of the test, and we can compact it further to be:
Line 287: @Test public void expandsMacrosSurroundedWithBraces() throws Exception {
Line 288:   assertThat(new StringTemplate("{a}{b}").expand(macros),
Line 289:              equalTo("AB"));
Line 290: }
Line 291: which tells us just what is supposed to happen and ignores everything else.
Line 292: Delegate to Subordinate Objects
Line 293: Sometimes helper methods aren’t enough and we need helper objects to support
Line 294: the tests. We saw this in the test rig we built in Chapter 11. We developed the
Line 295: ApplicationRunner, AuctionSniperDriver, and FakeAuctionServer classes so we
Line 296: could write tests in terms of auctions and Snipers, not in terms of Swing and
Line 297: messaging.
Line 298: A more common technique is to write test data builders to build up complex
Line 299: data structures with just the appropriate values for a test; see Chapter 22 for
Line 300: more detail. Again, the point is to include in the test just the values that are rele-
Line 301: vant, so that the reader can understand the intent; everything else can be defaulted.
Line 302: There are two approaches to writing subordinate objects. In Chapter 11 we
Line 303: started by writing the test we wanted to see and then ﬁlling in the supporting
Line 304: objects: start from a statement of the problem and see where it goes. The alterna-
Line 305: tive is to write the code directly in the tests, and then refactor out any clusters
Line 306: of behavior. This is the origin of the WindowLicker framework, which started
Line 307: out as helper code in JUnit tests for interacting with the Swing event dispatcher
Line 308: and eventually grew into a separate project.
Line 309: Assertions and Expectations
Line 310: The assertions and expectations of a test should communicate precisely what
Line 311: matters in the behavior of the target code. We regularly see code where tests assert
Line 312: Chapter 21
Line 313: Test Readability
Line 314: 254
Line 315: 
Line 316: --- 페이지 280 ---
Line 317: too much detail, which makes them difﬁcult to read and brittle when things
Line 318: change; we discuss what this might mean in “Too Many Expectations” (page 242).
Line 319: For the expectations and assertions we write, we try to keep them as narrowly
Line 320: deﬁned as possible. For example, in the “instrument with price” assertion above,
Line 321: we check only the strike price and ignore the rest of the values as irrelevant in
Line 322: that test. In other cases, we’re not interested in all of the arguments to a method,
Line 323: so we ignore them in the expectation. In Chapter 19, we deﬁne an expectation
Line 324: that says that we care about the Sniper identiﬁer and message, but that any
Line 325: RuntimeException object will do for the third argument:
Line 326: oneOf(failureReporter).cannotTranslateMessage(
Line 327:                          with(SNIPER_ID), with(badMessage),
Line 328:                          with(any(RuntimeException.class)));
Line 329: If you learned about pre- and postconditions in college, this is when that training
Line 330: will come in useful.
Line 331: Finally, a word of caution on assertFalse(). The combination of the failure
Line 332: message and negation makes it easy to read this as meaning that the two dates
Line 333: should not be different:
Line 334: assertFalse("end date", first.endDate().equals(second.endDate()));
Line 335: We could use assertTrue() and add a “!” to the result but, again, the single
Line 336: character is easy to miss. That’s why we prefer to use matchers to make the code
Line 337: more explicit:
Line 338: assertThat("end date", first.endDate(), not(equalTo(second.endDate())));
Line 339: which also has the advantage of showing the actual date received in the failure
Line 340: report:
Line 341: java.lang.AssertionError: end date
Line 342: Expected: not <Thu Jan 01 02:34:38 GMT 1970>
Line 343:      but: was <Thu Jan 01 02:34:38 GMT 1970>
Line 344: Literals and Variables
Line 345: One last point. As we wrote in the introduction to this chapter, test code tends
Line 346: to be more concrete than production code, which means it has more literal values.
Line 347: Literal values without explanation can be difﬁcult to understand because the
Line 348: programmer has to interpret whether a particular value is signiﬁcant (e.g. just
Line 349: outside the allowed range) or just an arbitrary placeholder to trace behavior (e.g.
Line 350: should be doubled and passed on to a peer). A literal value does not describe its
Line 351: role, although there are some techniques for doing so that we will show in
Line 352: Chapter 23
Line 353: One solution is to allocate literal values to variables and constants with names
Line 354: that describe their function. For example, in Chapter 12 we declared
Line 355: 255
Line 356: Literals and Variables
Line 357: 
Line 358: --- 페이지 281 ---
Line 359: public static final Chat UNUSED_CHAT = null;
Line 360: to show that we were using null to represent an argument that was unused in
Line 361: the target code. We weren’t expecting the code to receive null in production,
Line 362: but it turns out that we don’t care and it makes testing easier. Similarly, a team
Line 363: might develop conventions for naming common values, such as:
Line 364: public final static INVALID_ID = 666;
Line 365: We name variables to show the roles these values or objects play in the test and
Line 366: their relationships to the target object.
Line 367: Chapter 21
Line 368: Test Readability
Line 369: 256
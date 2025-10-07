Line 1: 
Line 2: --- 페이지 79 ---
Line 3: Chapter 5. Mocks, Stubs, and Dummies
Line 4: No man is an island.
Line 5: — John Donne Devotions upon Emergent Occasions (1624)
Line 6: Classes are like people: only some of them thrive living in solitude. Earlier in this book, we made the
Line 7: very unrealistic assumption that the classes we test all live their separate lives. It is now time to get
Line 8: real and dive into the troubled waters of relationships. As you will see, this has a serious impact on the
Line 9: testing techniques we will use.
Line 10: Things are going to get interesting from now on. Pessimists will probably complain about things
Line 11: getting much harder, while optimists will be thrilled at the prospect of new, exciting challenges.
Line 12: Whichever you are, read carefully, question what you learn, and practise a lot, because this is where
Line 13: the real challenges of unit testing begin.
Line 14: Figure 5.1. Types of collaboration with an SUT
Line 15: In Section 2.2 we discussed various types of interactions between an SUT and DOCs. Up till now, we
Line 16: have been focusing solely on direct inputs and outputs. We have been checking the returned values
Line 17: or the state of the SUT. Now it is time to venture into the realm of indirect interactions between the
Line 18: SUT and its collaborators.
Line 19: Why we are doing this? Why aren’t we respecting the internals of the SUT? As discussed previously,
Line 20: not every important operation performed by the SUT leaves easily observable traces and thus can’t
Line 21: be verified using state testing. We have already discussed a cache example (see Section 2.2.2) and in
Line 22: this chapter we will encounter a few more situations where state testing is not good enough.
Line 23: The ability to verify interactions between the SUT and collaborators comes at a cost. We are starting
Line 24: to demand that certain methods of collaborators be executed. This makes our tests very much linked
Line 25: to production code, which in turn spells trouble, as it makes them fragile - if the implementation of
Line 26: the SUT changes, our tests will need to be rewritten. The rule of thumb to follow here is: write an
Line 27: interactions test only if some of the SUT’s features cannot be tested using state testing.
Line 28: 5.1. Test Doubles
Line 29: Test doubles are used to replace collaborators of the SUT. They pretend to be real and fool SUT into
Line 30: thinking so. This allows us to:
Line 31: • gain full control over the environment in which the SUT is running,
Line 32: 64
Line 33: 
Line 34: --- 페이지 80 ---
Line 35: Chapter 5. Mocks, Stubs, and Dummies
Line 36: • move beyond state testing and verify interactions between the SUT and its collaborators.
Line 37: There are several types of test doubles, but for the start we will concentrate on two of them: mock and
Line 38: stub.
Line 39: Figure 5.2. Test doubles covering inputs and outputs
Line 40: As shown in the image mocks and stubs play different roles in testing. Mocks are used to verify
Line 41: indirect outputs, which means they will help us to discover whether the SUT sends the expected
Line 42: messages to its collaborator. Stubs, on the other hand, will help us to deal with indirect inputs. We
Line 43: will use them to feed the SUT with prepared values, so that certain actions of the SUT are invoked.
Line 44: Enough theory: let us make it all clear with an example. We will use the Mockito framework to create
Line 45: and use test doubles.
Line 46: As was the case with JUnit, this chapter introduces Mockito, but does not aim at being a
Line 47: complete reference source for this framework. Please consult the original documentation of
Line 48: Mockito to learn about all of its features.
Line 49: Fortunately, the syntax of Mockito is very simple to understand, so we can avoid lengthy
Line 50: explanations and simply enjoy its readability. Later on we will be learning more about it, but
Line 51: right now let us look at, and briefly explain, some code snippets.
Line 52: 5.2. Stubbing & verification
Line 53: First, let us discuss a few lines of code, which will be used to demonstrate the role of test doubles in
Line 54: testing.
Line 55: The code in Listing 5.1 is responsible for the sending of messages. It retrieves some data (i.e. the
Line 56: email of a client) from the parameters of sendMessage() method, then it tells its collaborators to
Line 57: perform certain actions. The code is trivial, yet quite close to reality (the real code would probably
Line 58: include some argument checking and exception handling - we will skip both of these for the sake of
Line 59: simplicity).
Line 60: Listing 5.1. Class to be tested with test doubles
Line 61: public class Messenger {
Line 62:     private TemplateEngine templateEngine; 
Line 63:     private MailServer mailServer; 
Line 64: 65
Line 65: 
Line 66: --- 페이지 81 ---
Line 67: Chapter 5. Mocks, Stubs, and Dummies
Line 68:     public Messenger(MailServer mailServer,
Line 69:              TemplateEngine templateEngine) { 
Line 70:         this.mailServer = mailServer;
Line 71:         this.templateEngine = templateEngine;
Line 72:     }
Line 73:     public void sendMessage(Client client, Template template) { 
Line 74:         String msgContent =
Line 75:             templateEngine.prepareMessage(template, client); 
Line 76:         mailServer.send(client.getEmail(), msgContent); 
Line 77:     }
Line 78: }
Line 79: Both collaborators of our SUT injected via constructor.
Line 80: This method returns void, and does not change the state of any object involved (neither
Line 81: Messenger nor client or template), which means there is no way we can test it using the state
Line 82: testing approach. We need test doubles!
Line 83: This is what we are really interested in: the cooperation between the Messenger and its
Line 84: collaborators. Our SUT invokes some methods on each of its collaborators and also retrieves
Line 85: some data from the client parameter of the sendMessage() method.
Line 86: This code is a pretty good illustration of our previous description of OO systems. The Messenger
Line 87: class takes care of transforming and passing messages rather than of any real work. According to the
Line 88: previous discussion, our class is a manager, as it tells others what to do rather than getting its own
Line 89: hands dirty.
Line 90: Right now our goal is to test this class in isolation, so we need to think about something other than
Line 91: integration tests. If only we could verify the interactions of the SUT and its collaborators… Then we
Line 92: could make sure that it works as expected. Well, thanks to test doubles this is possible.
Line 93: Let us consider the Messenger class and see what kind of collaboration happens there. The following
Line 94: picture illustrates this.
Line 95: Figure 5.3. Interactions of Messenger with the test class and DOCs
Line 96: As you can see:
Line 97: • There is no direct output (the method’s return type is void)
Line 98: • There are two arguments passed as direct inputs (client and template).
Line 99: • Our SUT asks the templateEngine engine to perform some computations for it (indirect input) so
Line 100: that…
Line 101: 66
Line 102: 
Line 103: --- 페이지 82 ---
Line 104: Chapter 5. Mocks, Stubs, and Dummies
Line 105: • …the SUT can ask mailServer to do something for it - this is the indirect output of this method.
Line 106: What we want to verify is the indirect output, that is, whether our SUT calls the right method of the
Line 107: mailServer with the right arguments.
Line 108: OK then, let us do it. We will move in really small steps, as each one we take will need some
Line 109: explanation.
Line 110: A mixture of unit, integration and end-to-end tests
Line 111: But before we go any further with our unit tests, a few words of warning.
Line 112: In this section we focus on unit tests solely. But let us not forget the usefulness of using
Line 113: various types of tests! In real life, it would be advisable to use a mixture of unit and
Line 114: integration tests to cover this functionality1.
Line 115: The unit tests can assure us that all the small building blocks are working as expected. They
Line 116: also allow us to simulate situations which are troublesome to prepare with integration tests -
Line 117: e.g. that database returns a certain error or that the mail server times out. But they won’t tell
Line 118: us if all configuration is as it should be, and they won’t test what happens when we upgrade
Line 119: our database from version X1 to X2. Each type of tests is suitable for some areas, and none is
Line 120: powerful enough to be the only one used for such a scenario.
Line 121: Only with a sound mixture of unit, integration and end-to-end tests can one sleep peacefully
Line 122: and rest assured that everything is fine with the code.
Line 123: 5.2.1. Creating Test Doubles
Line 124: You can think about a test double just as you would about a normal Java object. Its uniqueness results
Line 125: from the fact that it pretends to be something else: i.e. an object of some specific type2.
Line 126: To create a test double we need to use the Mockito.mock() method3. It takes a class as an argument,
Line 127: and returns an object of this type:
Line 128: MyClass myObject = Mockito.mock(MyClass.class);
Line 129: If you were to try checking the type of the object created by means of the instanceOf operator, you
Line 130: would learn that these objects are legal instances of requested types. This works both for classes and
Line 131: interfaces.
Line 132: Listing 5.2 demonstrates this using classes of collaborators of our Messenger SUT.
Line 133: Listing 5.2. Creation of test doubles
Line 134: import static org.mockito.Mockito.mock; 
Line 135: @Test
Line 136: 1See Section 1.2 for a reminder on the differences between unit, integration and end-to-end test.
Line 137: 2I use the term type to denote both classes and interfaces.
Line 138: 3We will learn more about creating test doubles in Section 10.5.2.
Line 139: 67
Line 140: 
Line 141: --- 페이지 83 ---
Line 142: Chapter 5. Mocks, Stubs, and Dummies
Line 143: void mockitoCreatesInstanesOfRequestedTypes() {
Line 144:         MailServer mailServer = mock(MailServer.class); 
Line 145:         TemplateEngine templateEngine = mock(TemplateEngine.class);
Line 146:         assertThat(templateEngine).isInstanceOf(TemplateEngine.class); 
Line 147:         assertThat(mailServer).isInstanceOf(MailServer.class);
Line 148: }
Line 149: We use a static mock() method provided by the Mockito class to create a test double.
Line 150: As this test proves, test-double objects are instances of the requested types.
Line 151: Mockito uses the same method - mock() - to create all types of test double. No distinction
Line 152: between them is made when they are being created. You, as a programmer, decide what
Line 153: role they play, by expressing their expected behaviour and verifying (or not verifying) their
Line 154: actions.
Line 155: To mock
Line 156: Long story short, it is very common that devs use term "mocks" when they really mean "test
Line 157: doubles". Similarly, you will often hear that "X was mocked" instead of saying that "a test
Line 158: double of type X was created". I also follow this trend in the book, and if I write that I "mock"
Line 159: some object, I mean that this happened:
Line 160: MyClass myObject = Mockito.mock(MyClass.class);
Line 161: 5.2.2. Stubbing
Line 162:  The point of having a test double is to tell it what it should do. Let us remind the code of the
Line 163: sendMessage() method we plan to test:
Line 164: public void sendMessage(Client client, Template template) {
Line 165:     String msgContent =
Line 166:         templateEngine.prepareMessage(template, client);
Line 167:     mailServer.send(client.getEmail(), msgContent);
Line 168: }
Line 169: We need to instruct our test double of templateEngine type that it should return some message
Line 170: content (msgContent). This is how we do it using Mockito’s when() method.
Line 171: This is a small snippet that only illustrates the work of the when() method - the whole test
Line 172: will be presented soon in Section 5.2.4.
Line 173: Listing 5.3. Stubbing
Line 174: import static org.mockito.Mockito.mock; 
Line 175: import static org.mockito.Mockito.when; 
Line 176: TemplateEngine templateEngine = mock(TemplateEngine.class); 
Line 177: when(templateEngine.prepareMessage(template, client)) 
Line 178: 68
Line 179: 
Line 180: --- 페이지 84 ---
Line 181: Chapter 5. Mocks, Stubs, and Dummies
Line 182:     .thenReturn("Important message"); 
Line 183: Creation of test doubles. Nothing new here.
Line 184: This line says: "when the prepareMessage() method of templateEngine is called with exactly
Line 185: these two parameters"…
Line 186: …"then it should return [Important message]".
Line 187: The last two lines instruct templateEngine test double how it should behave when its
Line 188: prepareMessage() method is called with certain arguments. By doing so, we turned our undefined
Line 189: test double into a stub that will feed our SUT with indirect input when requested.
Line 190: Have you noticed how very readable the line with expectations is? "When X happens, then
Line 191: do Y, please" - it reads almost like natural language, would you agree?
Line 192: In the case shown in Listing 5.3, no matter how many times we called the prepareMessage() method
Line 193: of our templateEngine stub, it would always return the same "Important message" string. Mockito
Line 194: allows us to make our stub return different values in consecutive calls. This is as simple as the next
Line 195: listing shows:
Line 196: when(templateEngine.prepareMessage(template, client))
Line 197:   .thenReturn("first message", "second message", "third message");
Line 198: What about client?
Line 199: Look at the last line of the code we are trying to test:
Line 200: mailServer.send(client.getEmail(), msgContent);
Line 201: It seems we should also take care of the client variable and instruct it to return some
Line 202: reasonable value. Yes, we should, and we will do it soon.
Line 203: P.S. Congratulations if you thought about it!
Line 204: 5.2.3. Verification
Line 205:  So we know how to instruct test doubles to pass the requested values to the SUT. Now we will learn
Line 206: how to verify whether the collaborators' methods were called as expected. Once again, the code we
Line 207: are trying to test:
Line 208: public void sendMessage(Client client, Template template) {
Line 209:     String msgContent =
Line 210:         templateEngine.prepareMessage(template, client);
Line 211:     mailServer.send(client.getEmail(), msgContent);
Line 212: }
Line 213: We focus now on the last line. Is the send method of mailServer called? Is it called with the right
Line 214: arguments? We can find out using Mockito’s verify() method.
Line 215: This is a small snippet that only illustrates the work of the verify() method - the whole
Line 216: test will be presented soon in Section 5.2.4.
Line 217: 69
Line 218: 
Line 219: --- 페이지 85 ---
Line 220: Chapter 5. Mocks, Stubs, and Dummies
Line 221: Listing 5.4. Verification
Line 222: import static org.mockito.Mockito.verify; 
Line 223: MailServer mailServer = mock(MailServer.class);
Line 224: verify(mailServer).send("client@email.com", "Important message"); 
Line 225: Using the verify() method to check if the right method was called in the right way. And BTW.
Line 226: - by using this method we verify indirect outputs of our SUT turning our mailSender test
Line 227: double into a mock.
Line 228: The verify() method is like an assertion. We assume some behaviour (some method call) occurred,
Line 229: and we check it. If it didn’t, the test will fail, and we will be informed with an error message:
Line 230: Wanted but not invoked:
Line 231: mailServer.send(
Line 232:     "client@email.com",
Line 233:     "Important message"
Line 234: );
Line 235: If the method was called, but with different arguments than expected, it will also be considered a
Line 236: failure, and an appropriate message will inform us about that:
Line 237: Argument(s) are different! Wanted:
Line 238: mailServer.send(
Line 239:     "client@email.com",
Line 240:     "Important message"
Line 241: );
Line 242: -> at com.practicalunittesting.shouldSendEmail(MessengerTest.java:35)
Line 243: Actual invocation has different arguments:
Line 244: mailServer.send(
Line 245:     "different@email.com",
Line 246:     "Important message"
Line 247: );
Line 248: Again, the error message is quite clear. Mockito also provides detailed information on code lines, so
Line 249: finding the problem is rather simple.
Line 250: The number of method invocations also counts - in this case we expect the send() method
Line 251: to be executed exactly once (we will discuss this further in Section 5.4.3).
Line 252: 5.2.4. The whole test
Line 253: We can now combine our knowledge of stubbing and mocking to test the sendMessage() method of
Line 254: the Messenger class.
Line 255: As mentioned previously, this is only a single test, chosen from many other ones - unit,
Line 256: integration and end-to-end tests - which would have to be written to fully cover the
Line 257: functionality considered here.
Line 258: Listing 5.5. Testing the Messenger class
Line 259: import org.junit.jupiter.api.Test;
Line 260: 70
Line 261: 
Line 262: --- 페이지 86 ---
Line 263: Chapter 5. Mocks, Stubs, and Dummies
Line 264: import static org.mockito.Mockito.mock;
Line 265: import static org.mockito.Mockito.verify;
Line 266: import static org.mockito.Mockito.when;
Line 267: public class MessengerTest {
Line 268:     private static final String CLIENT_EMAIL = "client@email.com";
Line 269:     private static final String MSG_CONTENT = "Important message";
Line 270:     @Test
Line 271:     void shouldSendEmail() {
Line 272:         Template template = mock(Template.class); 
Line 273:         Client client = mock(Client.class);
Line 274:         MailServer mailServer = mock(MailServer.class);
Line 275:         TemplateEngine templateEngine = mock(TemplateEngine.class);
Line 276:         Messenger sut = new Messenger(mailServer, templateEngine); 
Line 277:         when(client.getEmail()).thenReturn(CLIENT_EMAIL); 
Line 278:         when(templateEngine.prepareMessage(template, client)) 
Line 279:                 .thenReturn(MSG_CONTENT);
Line 280:         sut.sendMessage(client, template); 
Line 281:         verify(mailServer).send(CLIENT_EMAIL, MSG_CONTENT); 
Line 282:     }
Line 283: }
Line 284: Creation of all test doubles. At this point they do not differ from each other (except for the type
Line 285: they are pretending to be).
Line 286: Creation of our SUT and injection of required collaborators (the SUT does not suspect anything
Line 287: - it thinks it is working with real objects!). No mock() method used here, we want to test the real
Line 288: one!
Line 289: Stubbing. This is how we expect our client and templateEngine stubs to behave.
Line 290: Execution of the sendMessage() method of the SUT. We are not interested in its outputs, as it
Line 291: has none (this method’s return type is void).
Line 292: Verification of the behaviour of the SUT: "was the send() method invoked on mailServer
Line 293: DOC with the same CLIENT_EMAIL and MSG_CONTENT that were obtained from other
Line 294: collaborators?"
Line 295: There are few more comments worth adding here.
Line 296: • As you noticed, I decided to mock not only the aforementioned templateEngine and mailSender,
Line 297: but also client and template. As for the client, the situation is quite obvious - at some point,
Line 298: I needed to instruct it how to behave when its getEmail() method was invoked. As for the
Line 299: template, I admit that there was no need to do that, and the test would still work if I used a null
Line 300: value instead of a test double there. What I gained by using a test double is that if null-checks
Line 301: are added to the sendMessage() method (which I think is quite likely), my test would still work
Line 302: instead of throwing a NullPointerException.
Line 303: • The assertions part look different from what we have seen so far. There are no AssertJ’s assertions,
Line 304: but all is done using Mockito’s verify() method.
Line 305: • The execution and verification part is many times smaller than the test fixture creation part.
Line 306: 71
Line 307: 
Line 308: --- 페이지 87 ---
Line 309: Chapter 5. Mocks, Stubs, and Dummies
Line 310: Default Values
Line 311:  If you tried using any of the test doubles created, you would discover they actually can do
Line 312: something without any intervention on your part. In particular, test doubles created by the
Line 313: Mockito.mock() method are able to return some canned (default) values when we call their
Line 314: methods.
Line 315: Consider this simple Car interface:
Line 316: Listing 5.6. Car interface
Line 317: public interface Car {
Line 318:     boolean needsFuel();
Line 319:     double getEngineTemperature();
Line 320: }
Line 321: The following test demonstrates how a test double responds to various calls. As you will
Line 322: notice, the default behaviour is to return a 0, false or null value.
Line 323: Listing 5.7. Returning default values
Line 324: public class MockitoDefaultValuesTest {
Line 325:     @Test
Line 326:     void testDefaultBehaviourOfTestDouble() {
Line 327:         Car car = mock(Car.class);
Line 328:         assertThat(car.needsFuel()).isFalse(); 
Line 329:         assertThat(car.getEngineTemperature()).isEqualTo(0.0); 
Line 330:         assertThat(car.getName()).isNull(); 
Line 331:     }
Line 332: }
Line 333: By default the test double returns false when asked for boolean value.
Line 334: By default the test double returns zero when asked for numerical value.
Line 335: null value returned when asked for a String.
Line 336: For complete information concerning default returned values, please refer to Mockito’s
Line 337: Javadocs of org.mockito.internal.stubbing.defaultanswers package.
Line 338: This feature of Mockito framework is heavily disputed, and might change in
Line 339: version 3.0!
Line 340: 5.2.5. Conclusions
Line 341: So far we have looked at a bit of Mockito, and we know that it can help us to write tests with test
Line 342: doubles. In particular, Mockito can create various test doubles which by default return some canned
Line 343: 72
Line 344: 
Line 345: --- 페이지 88 ---
Line 346: Chapter 5. Mocks, Stubs, and Dummies
Line 347: values. But we get to decide how they should behave ("when X happens then do Y"), so that we can
Line 348: ultimately verify that our SUT executed certain methods of collaborators ("verify that the a() method
Line 349: of collaborator B was executed with arguments C & D").
Line 350: For the sake of a more complete picture, we should mention here that Mockito also has
Line 351: some limitations. In particular, it will not help you when working with code which does
Line 352: not adhere to certain design standards (in particular, Mockito works well with loosely
Line 353: coupled code). This will be further discussed in Section 8.7.
Line 354: 5.3. Types of Test Double
Line 355: Right now we are going to take a little break from coding and to take a look at the various types of
Line 356: test doubles that can be used to replace the real collaborators of a class. You have already encountered
Line 357: some of them.
Line 358: • dummy object (dummy) - needs to exist, but no real collaboration is needed. This is the case of
Line 359: template object in the example we discussed. You won’t use dummies often and in some cases
Line 360: they can be replaced with null values (even though I don’t recommend doing it). 
Line 361: • test stub (stub) - used for passing some values (indirect inputs) to the SUT. Also used to throw
Line 362: certain exceptions (in such case some call it a saboteur).  
Line 363: • mock - used to verify if the SUT calls specific methods of the collaborator (indirect outputs). 
Line 364: • test spy (spy) - similar to mock, but instead of creating a new object, it wraps around existing
Line 365: collaborator and intercepts only selected calls to it. We will devote Section 8.7.4 to discuss the
Line 366: usefulness of spies. 
Line 367: Based on this, we may arrive at the following observations:
Line 368: • Dummies and stubs are used to prepare the environment for testing. They are not used for
Line 369: verification. A dummy is employed to be passed as a value (e.g. as a parameter of a direct method
Line 370: call), while a stub passes some data to the SUT, replacin one of its collaborators.
Line 371: • The purpose of test spies and mocks is to verify the correctness of the communication between
Line 372: the SUT and its collaborators.
Line 373: • No test double is used for the verification of direct outputs of the SUT, as they can be tested
Line 374: directly.
Line 375: • Even though in theory all test doubles have well-defined roles and responsibilities, this is not
Line 376: the case in real-life programming. You will often use mocks not only for verification but also to
Line 377: provide indirect inputs to the SUT.
Line 378: 73
Line 379: 
Line 380: --- 페이지 89 ---
Line 381: Chapter 5. Mocks, Stubs, and Dummies
Line 382: Fake
Line 383:  For the sake of completeness, let us describe another type of test double: a fake. A fake works
Line 384: almost as well as a real collaborator, but is somehow simpler and/or weaker (which makes it
Line 385: unsuitable for production use). It is also usually "cheaper" in use (i.e. faster or simpler to set
Line 386: up), which makes it well-suited for tests (which should run as fast as possible).
Line 387: A typical example is an in-memory database that is used instead of a full-blown database
Line 388: server. It can be used for some tests, as it serves SQL requests pretty well; however, you
Line 389: would not want to use it in a production environment. In tests, a fake plays a similar role to a
Line 390: dummy and a stub: it is a part of the environment (test fixture), not an object of verification.
Line 391: Fakes are used in integration tests rather than in unit tests, so we will not be discussing them
Line 392: any further.
Line 393: 5.4. Example: TDD with Test Doubles
Line 394: After a short break, during which we learned about a few test doubles we haven’t heard about before,
Line 395: we are back to coding. Let us now discuss an example which integrates two techniques we have
Line 396: already learned: TDD and test doubles.
Line 397: This example shows how we can test and implement a service whose role is to inform interested
Line 398: parties about the results of sport races. The idea of the implementation is pretty obvious. There is a
Line 399: notification service, which allows clients to subscribe. The service should send out messages to all of
Line 400: its subscribers. And, basically, that is it.
Line 401:  In general, it is a good thing to avoid tight coupling between components of the system. In line with
Line 402: this rule, we want to make sure that the subscribers know as little as possible about the service, and
Line 403: vice versa. To achieve this result, we can use a publish/subscribe design pattern4 which does exactly
Line 404: this: it decouples publisher(s) from subscribers.
Line 405: First, let us discuss some requirements for our class - RaceResultsService:
Line 406: • It should allow clients to subscribe (which means they start receiving messages),
Line 407: • It should allow subscribers to unsubscribe (which means they stop receiving messages),
Line 408: • Every time a new message comes, it should be sent to all subscribers.
Line 409: These simple requirements, along with some common sense, already furnish us with a lot of test cases.
Line 410: In the ensuing sections we will be implementing the following:
Line 411: • If the client is not subscribed, it should not receive any messages,
Line 412: • If client is subscribed, it should receive each incoming message once (and only once),
Line 413: • If multiple clients are subscribed, each of them should receive each incoming message,
Line 414: • Consecutive subscribe requests issued by the same client will be ignored (nothing happens),
Line 415: 4See http://en.wikipedia.org/wiki/Publish/subscribe.
Line 416: 74
Line 417: 
Line 418: --- 페이지 90 ---
Line 419: Chapter 5. Mocks, Stubs, and Dummies
Line 420: • If the client unsubscribes, then it should be the case that no more messages are sent to it.
Line 421: We shall test RaceResultsService (the SUT) and make sure it sends messages to the right
Line 422: subscribers (DOCs). At first glance, it seems like we must have at least three types to implement the
Line 423: discussed functionality. First of all, we have to have an object of class RaceResultsService (our
Line 424: SUT). Then, we must create a Client type which can subscribe, unsubscribe and receive messages
Line 425: (objects of this type will play the role of DOCs). We will also need a Message type, which will be
Line 426: being passed from the race results service to subscribed clients.
Line 427: We will follow the TDD approach to implementing this functionality. Along the way we will also
Line 428: learn a thing or two about Mockito.
Line 429: 5.4.1. First Test: Single Subscriber Receives
Line 430: Message
Line 431: The first test is meant to verify whether, if a single client has subscribed to the RaceResultsService,
Line 432: it receives messages.
Line 433: This test also plays another important role, as writing it helps us to set everything in its proper place.
Line 434: Before we do any real testing, writing some test code will allow us to come up with the basic structure
Line 435: of RaceResultsService and the interfaces of the DOCs. In fact, it will be some time before we are
Line 436: actually able to test anything.
Line 437: We begin our test with the creation of the SUT, as displayed below.
Line 438: Listing 5.8. Creation of an SUT
Line 439: public class RaceResultsServiceTest {
Line 440:     @Test
Line 441:     void subscribedClientShouldReceiveMessage() {
Line 442:         RaceResultsService raceResults = new RaceResultsService();
Line 443:     }
Line 444: }
Line 445: This simple test code results in the RaceResultsService class being (auto)generated by the IDE, as
Line 446: shown below:
Line 447: Listing 5.9. The RaceResultsService class autogenerated by IDE
Line 448: public class RaceResultsService {
Line 449: }
Line 450: To test the functionality under consideration, we must introduce the two remaining types: Client and
Line 451: Message:
Line 452: Listing 5.10. Creation of collaborators
Line 453: public class RaceResultsServiceTest {
Line 454:     @Test
Line 455:     void subscribedClientShouldReceiveMessage() {
Line 456: 75
Line 457: 
Line 458: --- 페이지 91 ---
Line 459: Chapter 5. Mocks, Stubs, and Dummies
Line 460:         RaceResultsService raceResults = new RaceResultsService();
Line 461:         Client client = mock(Client.class); 
Line 462:         Message message = mock(Message.class); 
Line 463:     }
Line 464: }
Line 465: Test doubles of client and message are both created using the Mockito.mock() method. At
Line 466: this point, their role is not yet defined - they could become dummies, stubs or mocks.
Line 467: At this juncture the IDE complains that Message and Client types do not exist yet, and suggests
Line 468: creating both types. The question is, should they be created as interfaces or as classes? Following the
Line 469: basic rule of "code to an interface, and not to a implementation" ([gof1994]), I would choose the first
Line 470: option. This results in the creation of two empty interfaces:
Line 471: Listing 5.11. Empty Client and Message interfaces
Line 472: public interface Client {
Line 473: }
Line 474: public interface Message {
Line 475: }
Line 476: Now it is time to write the actual test. I would like it to present the following functionality:
Line 477: • the client subscribes to the service,
Line 478: • the service sends a message to the subscribed client.
Line 479: We will use the Mockito.verify() method to check if the functionality works.
Line 480: Listing 5.12. Test: messages sent to a single subscribed client
Line 481: import static org.mockito.Mockito.verify;
Line 482: public class RaceResultsServiceTest {
Line 483:     @Test
Line 484:     void subscribedClientShouldReceiveMessage() {
Line 485:         RaceResultsService raceResults = new RaceResultsService();
Line 486:         Client client = mock(Client.class);
Line 487:         Message message = mock(Message.class);
Line 488:         raceResults.addSubscriber(client); 
Line 489:         raceResults.send(message); 
Line 490:         verify(client).receive(message); 
Line 491:     }
Line 492: }
Line 493: the client subscribes to the service,
Line 494: the race results service sends a message (to all subscribers),
Line 495: verification part: making sure that the subscribed client has received the message.
Line 496: The role of each test double is clear now. We verify if client received the right message from SUT
Line 497: - thus, client is a mock. Another test double - the message object - is a dummy. Its behaviour is
Line 498: 76
Line 499: 
Line 500: --- 페이지 92 ---
Line 501: Chapter 5. Mocks, Stubs, and Dummies
Line 502: not verified, and the SUT does not require message to return any information. It is only being passed
Line 503: between other objects.
Line 504: Once again, the code does not yet compile. Use IDE help to generate the required methods. You will
Line 505: end up with the following empty implementations of the RaceResultsService and Client types:
Line 506: Listing 5.13. Empty implementation of methods required for the first test
Line 507: public interface Client {
Line 508:     void receive(Message message);
Line 509: }
Line 510: public class RaceResultsService {
Line 511:     public void addSubscriber(Client client) {
Line 512:     }
Line 513:     public void send(Message message) {
Line 514:     }
Line 515: }
Line 516: The test compiles, so let us run it. The error message – presented below - clearly indicates that the
Line 517: functionality does not work. The client has not received any message.
Line 518: Listing 5.14. The first test has failed: the client has not received any message
Line 519: Wanted but not invoked:
Line 520: client.receive(
Line 521:     Mock for Message, hashCode: 20474136
Line 522: );
Line 523: -> at com.practicalunittesting.chp05.raceresults.RaceResultsServiceFirstTest
Line 524:     .subscribedClientShouldReceiveMessage(RaceResultsServiceFirstTest.java:25)
Line 525: Actually, there were zero interactions with this mock.
Line 526: Very good! This means we really are into the red phase of TDD. Following the TDD approach, let us
Line 527: implement "the simplest thing that works" to satisfy the failing test. Which leads us to the following
Line 528: code:
Line 529: Listing 5.15. The first test has passed: a single subscriber receives a message
Line 530: public class RaceResultsService {
Line 531:     private Client client;
Line 532:     public void addSubscriber(Client client) {
Line 533:         this.client = client;
Line 534:     }
Line 535:     public void send(Message message) {
Line 536:         client.receive(message);
Line 537:     }
Line 538: }
Line 539: Once again, even though I can imagine this code being changed, and can even suspect how it would
Line 540: be changed (e.g. using a collection of clients instead of a single client field), I do not make use of this
Line 541: 77
Line 542: 
Line 543: --- 페이지 93 ---
Line 544: Chapter 5. Mocks, Stubs, and Dummies
Line 545: knowledge. Coding it now would be an example of YAGNI. What I really need to do is make the test
Line 546: pass (move in small steps, remember?). And the implementation shown in Listing 5.15 achieves this
Line 547: goal. So, for the time being it counts as perfect and does not call for any changes.
Line 548: The execution of the test assures me that this implementation will be good enough for now.
Line 549: Before implementing the next test, I spend a bit of time refactoring and making the code more
Line 550: readable. In the case of the code written so far, there is not much to be done. The classes
Line 551: and interfaces are very short (no copied code fragments, etc.), and I like the current method
Line 552: and class names. At this point I would only suggest writing some Javadocs: namely, for the
Line 553: RaceResultsService class, as this is the crucial part of the code (from the business point of view)5.
Line 554: 5.4.2. The Second Test: Send a Message to
Line 555: Multiple Subscribers
Line 556:  The decision concerning which test to perform next comes naturally: since I know that a message has
Line 557: been sent to one single client, I now wish to test whether this functionality will also work for more
Line 558: than one subscriber. The test is shown in Listing 5.16.
Line 559: I created the second test method (allSubscribedClientsShouldRecieveMessages()) by
Line 560: copying the content of the first test method
Line 561: (subscribedClientShouldReceiveMessage()). Then I introduced some changes there.
Line 562: Copy & paste technique is potentially dangerous, so I must double-check that the test does
Line 563: what I intended it to do. 
Line 564: Listing 5.16. The second test: messages sent to multiple subscribed clients
Line 565: public class RaceResultsServiceFirstAndSecondTest {
Line 566:     @Test
Line 567:     void subscribedClientShouldReceiveMessage() { 
Line 568:         RaceResultsService raceResults = new RaceResultsService();
Line 569:         Client client = mock(Client.class);
Line 570:         Message message = mock(Message.class);
Line 571:         raceResults.addSubscriber(client);
Line 572:         raceResults.send(message);
Line 573:         verify(client).receive(message);
Line 574:     }
Line 575:     @Test
Line 576:     void messageShouldBeSentToAllSubscribedClients() { 
Line 577:         RaceResultsService raceResults = new RaceResultsService();
Line 578:         Client clientA = mock(Client.class, "clientA"); 
Line 579:         Client clientB = mock(Client.class, "clientB"); 
Line 580:         Message message = mock(Message.class);
Line 581:         raceResults.addSubscriber(clientA);
Line 582:         raceResults.addSubscriber(clientB);
Line 583: 5Please see the notes on writing Javadocs in Section 4.2.3
Line 584: 78
Line 585: 
Line 586: --- 페이지 94 ---
Line 587: Chapter 5. Mocks, Stubs, and Dummies
Line 588:         raceResults.send(message);
Line 589:         verify(clientA).receive(message);
Line 590:         verify(clientB).receive(message);
Line 591:     }
Line 592: }
Line 593: The old test (the one verifying the sending of messages to a single subscriber) is left untouched,
Line 594: even though it seems to be redundant. However, I am going to keep it, so I can always be sure
Line 595: that this functionality will work for a single subscriber.
Line 596: The second test verifies whether the service works for more than one subscriber.
Line 597: In order to implement the new test, I need more test doubles of the Client class. Please note
Line 598: the additional String parameter of the mock() method, which will help us to distinguish test
Line 599: doubles when things go wrong.
Line 600: As in the case of the test discussed earlier (see Listing 5.12), both clientA and clientB are mocks,
Line 601: and message is a dummy.
Line 602: This is one of this rare cases when I find the use of "numbered" variable names (clientA,
Line 603: clientB) justified. Usually I try to convey some information by naming all variables
Line 604: meaningfully (e.g. vipClient or clientWithZeroAccount) but this time all I want to say
Line 605: is that these are two different clients. Thus, clientA and clientB sound good to me.
Line 606: After the test has been run it prints the following error:
Line 607: Listing 5.17. Error - client has not received the message
Line 608: Wanted but not invoked:
Line 609: clientA.receive( 
Line 610:     Mock for Message, hashCode: 11746570
Line 611: );
Line 612: -> at com.practicalunittesting.chp05.raceresults.RaceResultsServiceTest
Line 613:     .allSubscribedClientsShouldReceiveMessages(RaceResultsServiceTest.java:39)
Line 614: Actually, there were zero interactions with this mock.
Line 615: Thanks to the additional String parameter, the failure message precisely tells us that it was
Line 616: clientA that should have been notified.
Line 617: Well, obviously the addSubscriber() and send() methods of the RaceResultsService class are
Line 618: not able to operate on more than one client. A possible fix is shown below.
Line 619: Listing 5.18. The second test passed: multiple subscribers receive the message
Line 620: public class RaceResultsService {
Line 621:     private Collection<Client> clients = new ArrayList<Client>(); 
Line 622:     public void addSubscriber(Client client) {
Line 623:         clients.add(client); 
Line 624:     }
Line 625:     public void send(Message message) {
Line 626:         for (Client client : clients) { 
Line 627: 79
Line 628: 
Line 629: --- 페이지 95 ---
Line 630: Chapter 5. Mocks, Stubs, and Dummies
Line 631:             client.receive(message);
Line 632:         }
Line 633:     }
Line 634: }
Line 635: This implementation uses a list of subscribers instead of one subscriber.
Line 636: The test passes now. The main functionality – that of sending messages to subscribers – works. Good.
Line 637: Refactoring
Line 638: The production code looks fine, but the test code could really use some refactoring. There is an
Line 639: obvious redundancy with the SUT and test doubles being created in every test method. We can
Line 640: leverage the execution model of JUnit (see Section 3.8.1) and create the SUT and all mocks as
Line 641: instance variables.
Line 642: Listing 5.19. SUT and collaborators created in one place
Line 643: public class RaceResultsServiceFirstAndSecondRefactoredTest {
Line 644:     private RaceResultsService raceResults = new RaceResultsService(); 
Line 645:     private Message message = mock(Message.class);
Line 646:     private Client clientA = mock(Client.class, "clientA");
Line 647:     private Client clientB = mock(Client.class, "clientB");
Line 648:     @Test
Line 649:     void subscribedClientShouldReceiveMessage() {
Line 650:         raceResults.addSubscriber(clientA);
Line 651:         raceResults.send(message);
Line 652:         verify(clientA).receive(message);
Line 653:     }
Line 654:     @Test
Line 655:     void allSubscribedClientsShouldReceiveMessages() {
Line 656:         raceResults.addSubscriber(clientA);
Line 657:         raceResults.addSubscriber(clientB);
Line 658:         raceResults.send(message);
Line 659:         verify(clientA).receive(message);
Line 660:         verify(clientB).receive(message);
Line 661:     }
Line 662: }
Line 663: The SUT and all mocks will be re-created before each test method execution.
Line 664: After this refactoring, the test methods are much thinner and the creation code is not repeated.
Line 665: 5.4.3. The Third Test: Send Messages to
Line 666: Subscribers Only
Line 667:   The next step is to make sure that clients who are not subscribed do not receive any messages.
Line 668: Looking at the code written so far, I suspect the test will pass instantly; still, it needs to be tested
Line 669: 80
Line 670: 
Line 671: --- 페이지 96 ---
Line 672: Chapter 5. Mocks, Stubs, and Dummies
Line 673: (so that later on, if some changes are made to the code, this functionality will not be broken). The
Line 674: implementation of such a test method is shown in Listing 5.20.
Line 675: Listing 5.20. The third test: clients not subscribed do not receive any messages
Line 676: import static org.mockito.Mockito.never;
Line 677: @Test
Line 678: void notSubscribedClientShouldNotReceiveMessage() {
Line 679:     raceResults.send(message);
Line 680:     verify(clientA, never()).receive(message); 
Line 681:     verify(clientB, never()).receive(message); 
Line 682: }
Line 683: This test presents a new feature of Mockito: its ability to check that something has not
Line 684: occurred. This is done using the static never() method. As usual with Mockito, the code is
Line 685: very readable ("verify that clientA has never received a message").
Line 686: As expected, the new test passes instantly.
Line 687: The fact that the last test passed instantly should make us feel just a little uneasy. This
Line 688: is a warning sign. It might mean that the test repeats what other tests have already
Line 689: verified. But in fact this is not the case here. Another possibility is that we are testing
Line 690: very "defensively". This means we are trying to protect ourselves from bad things which
Line 691: are really outside the scope of the original requirements. Testing whether the SUT does
Line 692: not make something is often questionable. In our case, there is no direct requirement that
Line 693: clients who are not subscribed should not receive the message; however, I find it logical to
Line 694: add this one, and in my opinion such a test is legitimate. But this is a subjective matter, and
Line 695: you might well hold a different view here.
Line 696: Now I spend some time looking at the test code. I see some kind of a pattern there. The consecutive
Line 697: tests verify what happens when there are one, two or no clients subscribed to the SUT. I have made
Line 698: this pattern more visible by rearranging the order of the tests, as displayed in Listing 5.21 (for the sake
Line 699: of brevity, only method signatures are shown).
Line 700: Listing 5.21. Refactored tests: order changed
Line 701: public class RaceResultsServiceTestBeforeCombining {
Line 702:     // zero subscribers
Line 703:     @Test
Line 704:     void notSubscribedClientShouldNotReceiveMessage() { ... }
Line 705:     // one subscriber
Line 706:     @Test
Line 707:     void subscribedClientShouldReceiveMessage() { ... }
Line 708:     // two subscribers
Line 709:     @Test
Line 710:     void allSubscribedClientsShouldReceiveMessages() { ... }
Line 711: }
Line 712: I like the new version better. It shows how things are progressing. Good.
Line 713: 81
Line 714: 
Line 715: --- 페이지 97 ---
Line 716: Chapter 5. Mocks, Stubs, and Dummies
Line 717: 5.4.4. The Fourth Test: Subscribe More Than Once
Line 718: Let us now verify the behaviour of the RaceResultsService when subscribers subscribe more than
Line 719: one time. This situation is a little bit outside of the "path of normal, reasonable usage (happy path)" of
Line 720: the SUT; however, it is possible, and should be tested.
Line 721: Listing 5.22 shows a test which verifies that a subscriber who subscribes again still receives only one
Line 722: message (only the new test method is shown, for the sake of simplicity – the rest of the test class has
Line 723: not changed).
Line 724: Listing 5.22. The fourth test: subscribed client subscribes again
Line 725: @Test
Line 726: void shouldSendOnlyOneMessageToMultiSubscriber() {
Line 727:     raceResults.addSubscriber(clientA);
Line 728:     raceResults.addSubscriber(clientA);
Line 729:     raceResults.send(message);
Line 730:     verify(clientA).receive(message); 
Line 731: }
Line 732: By default, Mockito verifies that the method has been invoked exactly once.
Line 733: After running the test, it transpires that our implementation is not behaving as expected.
Line 734: Listing 5.23. Error - client subscribed more than once
Line 735: org.mockito.exceptions.verification.TooManyActualInvocations:
Line 736: clientA.receive(
Line 737:     Mock for Message, hashCode: 29715552
Line 738: );
Line 739: Wanted 1 time:
Line 740: -> at com.practicalunittesting.chp05.raceresults.RaceResultsServiceTest
Line 741:     .shouldSendOnlyOneMessageToMultiSubscriber(RaceResultsServiceTest.java:55)
Line 742: But was 2 times. Undesired invocation:
Line 743: -> at com.practicalunittesting.chp05.raceresults.RaceResultsService
Line 744:     .send(RaceResultsService.java:23)
Line 745: This can be fixed by replacing List with Set within the RaceResultsService class, as shown in
Line 746: Listing 5.24.
Line 747: Listing 5.24. The fourth test has passed!
Line 748: public class RaceResultsService {
Line 749:     private Collection<Client> clients = new HashSet<Client>(); 
Line 750:     public void addSubscriber(Client client) {
Line 751:         clients.add(client);
Line 752:     }
Line 753:     public void send(Message message) {
Line 754:         for (Client client : clients) {
Line 755:             client.receive(message);
Line 756:         }
Line 757: 82
Line 758: 
Line 759: --- 페이지 98 ---
Line 760: Chapter 5. Mocks, Stubs, and Dummies
Line 761:     }
Line 762: }
Line 763: A set does not allow for duplicates. The older version - which used a list - did not work properly.
Line 764: Mockito: How Many Times?
Line 765:   Let us go back to Listing 5.22 for a minute, so that we can learn something new about Mockito.
Line 766: This code contains a single line, which verifies whether the receive() method of the client has been
Line 767: called. To be more precise, it makes Mockito verify whether this method has been called exactly once.
Line 768: verify(clientA).receive(message);
Line 769: If you want to specify another value, you could use another static method of the Mockito class:
Line 770: times(), e.g.:
Line 771: verify(clientA, times(3)).receive(message);
Line 772: 5.4.5. The Fifth Test: Remove a Subscriber
Line 773:   What remains is to make sure that once a client has unsubscribed, it will not receive any messages.
Line 774: Such a test can be built upon the existing tests - i.e. those tests that prove that a subscribed client does
Line 775: receive messages. Its implementation is presented in Listing 5.25.
Line 776: Listing 5.25. The fifth test: unsubscribed client stops receiving messages
Line 777: @Test
Line 778: void unsubscribedClientShouldNotReceiveMessages() {
Line 779:     raceResults.addSubscriber(clientA); 
Line 780:     raceResults.removeSubscriber(clientA); 
Line 781:     raceResults.send(message);
Line 782:     verify(clientA, never()).receive(message); 
Line 783: }
Line 784: We know that after this line of code clientA should start receiving messages. Our knowledge
Line 785: is based on other tests (i.e. subscribedClientShouldReceiveMessage()), which verify this
Line 786: behaviour.
Line 787: …but we want the removeSubscriber() method to alter this behaviour (we let IDE auto-
Line 788: generate this method),
Line 789: …so clientA will not receive any message. Again, this "negative" verification is done using the
Line 790: never() method.
Line 791: After we let the IDE create an empty implementation of the removeSubscriber() method of the
Line 792: RaceResultsService class, the test will fail:
Line 793: Listing 5.26. Error - unsubscribed client still receives messages
Line 794: org.mockito.exceptions.verification.NeverWantedButInvoked:
Line 795: clientA.receive(
Line 796:     Mock for Message, hashCode: 19653053
Line 797: 83
Line 798: 
Line 799: --- 페이지 99 ---
Line 800: Chapter 5. Mocks, Stubs, and Dummies
Line 801: );
Line 802: Never wanted here:
Line 803: -> at com.practicalunittesting.chp05.raceresults.RaceResultsServiceTest
Line 804:     .unsubscribedClientShouldNotReceiveMessages(RaceResultsServiceTest.java:63)
Line 805: But invoked here:
Line 806: -> at com.practicalunittesting.chp05.raceresults.RaceResultsService
Line 807:     .send(RaceResultsService.java:22)
Line 808: Yes, we need to implement the removeSubscriber() method properly. When we do that, the test
Line 809: passes.
Line 810: Listing 5.27. The fifth test has passed: client unsubscribes successfully
Line 811: public class RaceResultsService {
Line 812:     private Collection<Client> clients = new HashSet<Client>();
Line 813:     public void addSubscriber(Client client) {
Line 814:         clients.add(client);
Line 815:     }
Line 816:     public void send(Message message) {
Line 817:         for (Client client : clients) {
Line 818:             client.receive(message);
Line 819:         }
Line 820:     }
Line 821:     public void removeSubscriber(Client client) {
Line 822:         clients.remove(client); 
Line 823:     }
Line 824: }
Line 825: The client is removed from the subscribers list.
Line 826: This functionality completes the task in hand. All of the planned tests have been written, and all of
Line 827: them pass. It is time to summarize what we have learned.
Line 828: There are still some tests which ought to be written, but which have been omitted (on
Line 829: purpose, so this book does not end up being 1000 pages long). I would, nevertheless,
Line 830: encourage you to implement them as a practice exercise. Some of them are listed in the
Line 831: exercises part of Section 5.7.
Line 832: 5.4.6. TDD and Test Doubles - Conclusions
Line 833: The RaceResultsService example showed how to use test doubles to verify interactions between
Line 834: objects. By using them - i.e. by using the mocks - we were able to implement the given functionality.
Line 835: We followed the TDD approach by coding test-first and refactoring along the way. There are some
Line 836: comments to be made about the way we coded and the results of our efforts.
Line 837: More Test Code than Production Code
Line 838: One interesting thing is the amount of code written. We ended up with roughly twice as much test
Line 839: code as production code. With more tests written - and, as stated previously, it would be sensible to
Line 840: 84
Line 841: 
Line 842: --- 페이지 100 ---
Line 843: Chapter 5. Mocks, Stubs, and Dummies
Line 844: add a few additional ones - the result would be even more skewed towards test code. This is nothing
Line 845: unexpected. When coding test first, and testing thoroughly, you can expect this sort of test-to-code
Line 846: ratio. In fact, this is rather a good sign.
Line 847: The Interface is What Really Matters
Line 848:  An interesting fact about the code we have just written is that we did not implement any of the
Line 849: collaborating classes. Neither Message nor Client were implemented. This is kind of weird,
Line 850: considering the number of times they were used. However, we did just fine with only their interfaces.
Line 851: Now, this is important! It means that you can work on RaceResultsService while your teammates
Line 852: are coding the Message and Client classes in parallel – so long as you have agreed on the interfaces
Line 853: and stick to them. That need not mean you should necessarily spread such simple tasks between team
Line 854: members, but it is worth being aware of the fact that it opens up some possibilities of doing this sort
Line 855: of thing. It might not be a big deal when working on simple classes like Client and Message, but it
Line 856: surely helps to be able to code your services and DAO layers separately (even in parallel).
Line 857: Starting with an interface also brings with it another advantage: by analogy with road works, there
Line 858: is no danger of building two halves of a bridge that do not ultimately meet. In fact, you will have
Line 859: actually started out with a meeting point in place, so there can be no risk of such a situation arising.
Line 860: To conclude, we have done pretty well without any implementation of DOCs (the Client and
Line 861: Message classes) at all. That is because at this stage all that matters is their interfaces.
Line 862: Interactions Can Be Tested
Line 863: The example of RaceResultsService has proved – once more – that verification of interactions is
Line 864: possible. I even hope that it has demonstrated that they are not as scary as they might seem at first
Line 865: glance. :)
Line 866: In fact, we had no choice. There is nothing else we could have tested, as the RaceResultsService is
Line 867: all about interactions with other entities. There are simply no observable outputs of its activities. And
Line 868: remember, the Client class is still not implemented yet, so there is no way to verify the quality of the
Line 869: RaceResultsService implementation by looking at the behaviour of clients.
Line 870: Some Test Doubles are More Useful than Others
Line 871: In the case of the RaceResultsService tests, only two test doubles were used - a dummy and a test
Line 872: spy. There is nothing special about this: we have simply been using what was required, and this time
Line 873: there was no role that stubs could have played.
Line 874: We haven’t made any use of mock objects, either: because, as mentioned previously, they can be used
Line 875: interchangeably with test spies.
Line 876: Unit Tests are Green but…
Line 877: …but, the whole functionality is far from being implemented! We still need to write code for the
Line 878: Message and Client classes, and probably a few more. Have a look at this picture - what we did so
Line 879: far is finishing a few circles of the inner loop. The rest is still to be done.
Line 880: 85
Line 881: 
Line 882: --- 페이지 101 ---
Line 883: Chapter 5. Mocks, Stubs, and Dummies
Line 884: Figure 5.4. Unit Tests help us to deal with the inner loop
Line 885: 5.5. Always Use Test Doubles… or Maybe
Line 886: Not?
Line 887: One feature of a decent unit test is isolation (see Section 2.1). Testing in isolation allows one to find
Line 888: out whether the SUT behaves properly, independently of the implementation of other classes. This is
Line 889: an important property of unit tests, that should not be recklessly abandoned. In previous sections we
Line 890: have learned how to use test doubles to fully control the SUT’s collaborators.
Line 891: But does this mean that you should always create a test double for every collaborator of a class?
Line 892: If it should turn out that using a real collaborator means involving database connections, third-party
Line 893: frameworks or costly computations in the conducting of unit tests, then have no choice: you must
Line 894: use a test double – otherwise it will not be a unit test anymore6. Using a real class would make your
Line 895: (supposed) unit test depend on too many external components – ones that could, in turn, make the test
Line 896: fail unexpectedly, even if your code has worked fine. This is unacceptable for unit tests.
Line 897: But what if a collaborator is a very simple class with almost no logic? Is replacing it with a test double
Line 898: worth the effort? Let us look for an answer to this question by considering the example of two simple
Line 899: classes shown below.
Line 900: Listing 5.28. Phone class
Line 901: public class Phone {
Line 902:     private final boolean mobile;
Line 903:     private final String number;
Line 904:     public Phone(String number, boolean mobile) {
Line 905: 6However, it could still be a very important, useful and necessary test. Nevertheless, it would lack some of the properties of decent
Line 906: unit tests: namely, short execution time and good error localization.
Line 907: 86
Line 908: 
Line 909: --- 페이지 102 ---
Line 910: Chapter 5. Mocks, Stubs, and Dummies
Line 911:         this.number = number;
Line 912:         this.mobile = mobile;
Line 913:     }
Line 914:     public boolean isMobile() {
Line 915:         return mobile;
Line 916:     }
Line 917: }
Line 918: Listing 5.29. Client class
Line 919: public class Client {
Line 920:     private final List<Phone> phones = new ArrayList<Phone>();
Line 921:     public void addPhone(Phone phone) {
Line 922:         phones.add(phone);
Line 923:     }
Line 924:     public boolean hasMobile() { 
Line 925:         for (Phone phone : phones) {
Line 926:             if (phone.isMobile()) {
Line 927:                 return true;
Line 928:             }
Line 929:         }
Line 930:         return false;
Line 931:     }
Line 932: }
Line 933: This is the method that we will be testing in the sections below.
Line 934: As you can see, the Client class is tightly coupled with the Phone class. There is no interface that
Line 935: would shield Phone from Client.
Line 936: Now let us think about how we could test the hasMobile() method of the Client class. You would
Line 937: need a few test cases capable of verifying the following:
Line 938: • if the client has no phones, the hasMobile() method returns false,
Line 939: • if the client has only stationary (i.e. landline) phones, the hasMobile() method returns false,
Line 940: • if the client has one or more mobile phones (and any number of stationary phones), the
Line 941: hasMobile() method returns true.
Line 942: For our purposes, we shall limit the number of phones to one mobile and one stationary one. This will
Line 943: be sufficient to be illustrative of the case in point.
Line 944: 5.5.1. No Test Doubles
Line 945: In such a simple case you might be tempted to use the classes directly in your test code. The thing is,
Line 946: making Phone a mobile phone is very easy: simply pass true to its constructor. So you can create
Line 947: instances of the Phone class in test code, as shown in Listing 5.30.
Line 948: Listing 5.30. No test doubles used
Line 949: public class ClientTest {
Line 950: 87
Line 951: 
Line 952: --- 페이지 103 ---
Line 953: Chapter 5. Mocks, Stubs, and Dummies
Line 954:     final static String ANY_NUMBER = "999-888-777";
Line 955:     final static Phone MOBILE_PHONE = new Phone(ANY_NUMBER, true); 
Line 956:     final static Phone STATIONARY_PHONE = new Phone(ANY_NUMBER, false); 
Line 957:     Client client = new Client();
Line 958:     @Test
Line 959:     void shouldReturnTrueIfClientHasMobile() { 
Line 960:         client.addPhone(MOBILE_PHONE);
Line 961:         client.addPhone(STATIONARY_PHONE);
Line 962:         assertThat(client.hasMobile()).isTrue();
Line 963:     }
Line 964:     @Test
Line 965:     void shouldReturnFalseIfClientHasNoMobile() { 
Line 966:         client.addPhone(STATIONARY_PHONE);
Line 967:         assertThat(client.hasMobile()).isFalse();
Line 968:     }
Line 969: }
Line 970: Real objects are created to be used by the SUT.
Line 971: Both test methods use real objects of the Phone class, and both rely on its correctness.
Line 972: The test code shown in Listing 5.30 is clear and concise. The required DOCs are created using
Line 973: a +Phone+ class constructor with the appropriate boolean parameter - true for mobiles and false for
Line 974: stationary phones.
Line 975: 5.5.2. Using Test Doubles
Line 976: The alternative approach would be to use test doubles instead of real objects. This is shown in Listing
Line 977: 5.31.
Line 978: Listing 5.31. Test doubles
Line 979: public class ClientTest {
Line 980:     final static Phone MOBILE_PHONE = mock(Phone.class); 
Line 981:     final static Phone STATIONARY_PHONE = mock(Phone.class); 
Line 982:     Client client = new Client();
Line 983:     @Test
Line 984:     void shouldReturnTrueIfClientHasMobile() {
Line 985:         when(MOBILE_PHONE.isMobile()).thenReturn(true); 
Line 986:         client.addPhone(MOBILE_PHONE);
Line 987:         client.addPhone(STATIONARY_PHONE);
Line 988:         assertThat(client.hasMobile()).isTrue();
Line 989:     }
Line 990:     @Test
Line 991:     void shouldReturnFalseIfClientHasNoMobile() {
Line 992:         client.addPhone(STATIONARY_PHONE);
Line 993: 88
Line 994: 
Line 995: --- 페이지 104 ---
Line 996: Chapter 5. Mocks, Stubs, and Dummies
Line 997:         assertThat(client.hasMobile()).isFalse();
Line 998:     }
Line 999: }
Line 1000: Collaborators are created using Mockito’s mock() method. The creation of DOCs is completely
Line 1001: independent from constructor(s) of the Phone class.
Line 1002: In contrast to real objects of the Phone class, test doubles have no idea about how to behave, so
Line 1003: we need to instruct them. This is required for mobile phones (which should return true). For
Line 1004: stationary phones, there is no need to specify a returned value, as mocks created by Mockito
Line 1005: return false by default7.
Line 1006: The code in Listing 5.31 does not differ much from the previously shown Listing 5.30. Constructor
Line 1007: calls, which defined how objects of the Phone class should behave, were replaced with calls to
Line 1008: Mockito’s mock() and when() methods.
Line 1009: No Winner So Far
Line 1010: So far, so good. Both approaches seems fine. Using real classes in test code seems to be justified by
Line 1011: the close relationship between Client and Phone. Both test classes are concise and free of any logic.
Line 1012: Good.
Line 1013: 5.5.3. A More Complicated Example
Line 1014: But let us stir things up a little bit, where this very solid construction is concerned, by introducing
Line 1015: a small change to the Phone class: let us make it behave more intelligently. Phone constructor can
Line 1016: recognize if a number belongs to a mobile phone, using pattern matching. Because of this change,
Line 1017: there is no need for the constructor’s second boolean parameter, as shown in Listing 5.32.
Line 1018: Listing 5.32. Phone class constructor enhanced
Line 1019: public Phone(String number) {
Line 1020:     this.number = number;
Line 1021:     this.mobile = number.startsWith("+")
Line 1022:             && number.endsWith("9"); 
Line 1023: }
Line 1024: Do not do this at home! This is surely not a valid way to recognize mobile phone numbers!
Line 1025: After this change has been introduced, the test, which does not use mocks, needs to be updated. This
Line 1026: time, in order to create appropriate phones (mobile and stationary), a knowledge of the internals of the
Line 1027: Phone class is required. Without it there is no way a developer could construct a phone of the desired
Line 1028: type. The test starts to look as shown in Listing 5.33.
Line 1029: Listing 5.33. No test doubles used - enhanced Phone class version
Line 1030: public class ClientTest {
Line 1031:     private final static Phone MOBILE_PHONE = new Phone("+123456789"); 
Line 1032:     private final static Phone STATIONARY_PHONE = new Phone("123123123"); 
Line 1033:     private Client client = new Client();
Line 1034: 7See Section 5.2.1 for information concerning the default behaviour of Mockito’s test doubles.
Line 1035: 89
Line 1036: 
Line 1037: --- 페이지 105 ---
Line 1038: Chapter 5. Mocks, Stubs, and Dummies
Line 1039:     @Test
Line 1040:     void shouldReturnTrueIfClientHasMobile() {
Line 1041:         client.addPhone(MOBILE_PHONE);
Line 1042:         client.addPhone(STATIONARY_PHONE);
Line 1043:         assertThat(client.hasMobile()).isTrue();
Line 1044:     }
Line 1045:     @Test
Line 1046:     void shouldReturnFalseIfClientHasNoMobile() {
Line 1047:         client.addPhone(STATIONARY_PHONE);
Line 1048:         assertThat(client.hasMobile()).isFalse();
Line 1049:     }
Line 1050: }
Line 1051: The chosen phone numbers must follow the logic of the Phone's constructor.
Line 1052: This version of the ClientTest class is coupled with the implementation of the Phone class. If the
Line 1053: pattern-matching mechanism used in the Phone constructor changes, the test code will also need to
Line 1054: change. The SRP principle has clearly been breached, because this test class is also coupled with
Line 1055: the Client class implementation (so ClientTest has more than one reason to change). This is a
Line 1056: warning signal. The violation of SRP entails that the DRY principle has also been breached. Surely,
Line 1057: there must exist a PhoneTest class that will make sure that the Phone constructor and isMobile()
Line 1058: method works as expected! To test this functionality, PhoneTest needs to create identical (or almost
Line 1059: identical) instances of phones, as shown in Listing 5.33. If so, then a change in the Phone class will
Line 1060: entail changes in two tests - PhoneTest and ClientTest. This is bad.
Line 1061: Surprisingly (or, rather… perhaps not!), the test class based on test doubles remained unchanged. The
Line 1062: stubs did not even notice the change of algorithm within the Phone class or the difference in the values
Line 1063: of the arguments passed to the constructor, because they do not make use of either of these. They were
Line 1064: ordered to return certain values at certain points of execution, and they are still following those orders.
Line 1065: 5.5.4. Use Test Doubles or Not? - Conclusion
Line 1066: This issue is worth discussing only in the case of "real" objects: that is, objects that
Line 1067: have some business logic and offer some complex behaviour. In the case of DTOs8, or
Line 1068: Value Objects9, using a test double will be overkill. Similarly, creating a test double of a
Line 1069: java.util.ArrayList is not recommended.  
Line 1070: As has been confirmed in some of the preceding paragraphs, testing without test doubles is possible,
Line 1071: but carries some serious consequences. First of all, it may result in cluttering up your test code with
Line 1072: logic that belongs to collaborators. This results in tests failing unexpectedly, if and when the code of
Line 1073: the collaborators changes. Secondly, it makes you repeat the same code constructs (e.g. the creation
Line 1074: of the DOCs) across multiple tests. This brings it about that making just a single change to some class
Line 1075: or other has a ripple effect on your tests, with many of them then needing to be changed10. Thirdly,
Line 1076: it obliges you to develop classes in some specific order (e.g. the Phone class must be ready and fully
Line 1077: 8Simple containers for data with getters and setters only. See http://en.wikipedia.org/wiki/Data_transfer_object
Line 1078: 9Small simple objects like dates, money, strings. See http://c2.com/cgi/wiki?ValueObject
Line 1079: 10Another solution is to extract the DOCs creation parts of the code into some utility method. This solves the problem of multiple
Line 1080: changes, but reduces the readability of test code by forcing the reader to jump between different classes.
Line 1081: 90
Line 1082: 
Line 1083: --- 페이지 106 ---
Line 1084: Chapter 5. Mocks, Stubs, and Dummies
Line 1085: tested before you can start working on the Client class), and may lull you into being over-reliant
Line 1086: upon the existing implementation of the collaborators.
Line 1087: On the other hand, using test doubles in some situations might be considered overkill. For people who
Line 1088: are new to test doubles, writing new MyClass() instead of mock(MyClass.class) is much more
Line 1089: natural, especially if there is no instant gain in using test doubles.
Line 1090: In general, I would recommend using test doubles. The overheads related to their creation and the
Line 1091: setting of expectations might seem unjustified at first (especially if a collaborator is very simple).
Line 1092: However, when the design of your classes changes, you will benefit from the isolation, and your tests
Line 1093: will not break down unexpectedly. Also, current frameworks only call for you to write a very small
Line 1094: number of lines of code, so there is no decline in productivity. Using a test double makes it virtually
Line 1095: impossible to rely on the DOCs’ implementation, as it might not exist yet.
Line 1096: The only situations where I would consider using a real collaborator instead of a test double are the
Line 1097: following:
Line 1098: • the collaborator is very, very simple, preferably without any logic (e.g. some sort of "container"
Line 1099: class with only accessors and mutators methods),
Line 1100: • the collaborator’s logic is so simple that it is clear how to set it in the desired state (and its logic will
Line 1101: not be enhanced in the foreseeable future).
Line 1102: Even then, I would be highly cautious, as changes are inevitable – no matter how very unlikely they
Line 1103: may seem!
Line 1104: 5.6. Conclusions (with a Warning)
Line 1105: In this section we have discussed an essential – and probably the hardest – part of unit testing. We
Line 1106: have learned about the various types of test double, and started using Mockito to create and manage
Line 1107: them in tests. Working with an example has enabled us to acquire an overview of what it is like to
Line 1108: develop tests using the TDD approach with test doubles. Wow… really a lot of knowledge this time!
Line 1109: By introducing test doubles, and especially mocks, we have entered the realm of interaction testing.
Line 1110: Thanks to them, we can test much more than we would be able to with state testing alone. This is
Line 1111: definitely a good thing. However, there is always a price to pay, and this is indeed the case with test
Line 1112: doubles. So before we start putting our new testing abilities to use, we really ought to try to become
Line 1113: aware of the perils awaiting us.
Line 1114: In fact, we are in a trap, even if we have not yet seen it. The problem is as follows: as we already
Line 1115: know, if we just stick to state testing, we will not be able to test everything (as discussed in Section
Line 1116: 2.2.1). However, if we start testing interactions between objects, we will soon discover that even
Line 1117: seemingly innocent refactoring may result in broken-down tests. And why is that? Well, with
Line 1118: state testing all we attend to is the outcome (of some method calls), and this gives us the freedom
Line 1119: to refactor the code we are testing. With interaction testing things are different, because it is all
Line 1120: about methods being called on collaborators. Interaction testing makes some assumptions about the
Line 1121: implementation of an object, and thus makes it harder to change this implementation.
Line 1122: We can think about this using a black-box/white-box analogy. With state testing, the SUT is a black
Line 1123: box. We put some things inside, and verify what comes out. State testing respects the objects’ right
Line 1124: 91
Line 1125: 
Line 1126: --- 페이지 107 ---
Line 1127: Chapter 5. Mocks, Stubs, and Dummies
Line 1128: to privacy, and does not try to make any assumptions about "how" things work inside. It concentrates
Line 1129: only on "what" the results of actions amount to. With interaction testing the focus changes from
Line 1130: "what" to "how". The SUT is no longer a black box. On the contrary, we look inside the SUT
Line 1131: (contravening the "information hiding" principle11, along the way), and verify its internal parts. And,
Line 1132: as usual when breaking some sensible rules, we pay a price for this.
Line 1133: We will discuss issues pertaining to the manageability of tests as these relate to interaction
Line 1134: testing in Chapter 12, Test Quality.
Line 1135: 11See http://en.wikipedia.org/wiki/Information_hiding
Line 1136: 92
Line 1137: 
Line 1138: --- 페이지 108 ---
Line 1139: Chapter 5. Mocks, Stubs, and Dummies
Line 1140: 5.7. Exercises
Line 1141: The exercises presented in this section will allow you to practise your knowledge of testing with test
Line 1142: doubles by actually using them. They will also allow you to familiarize yourself with the Mockito
Line 1143: framework.
Line 1144: 5.7.1. User Service Tested
Line 1145: Write a happy-path test for the class presented below. Verify that the user gets his new password, and
Line 1146: that the updateUser() method of userDAO is called.
Line 1147: Listing 5.34. The UserServiceImpl class
Line 1148: public class UserServiceImpl {
Line 1149:     private UserDAO userDAO;
Line 1150:     private SecurityService securityService;
Line 1151:     public void assignPassword(User user) throws Exception {
Line 1152:         String passwordMd5 = securityService.md5(user.getPassword());
Line 1153:         user.setPassword(passwordMd5);
Line 1154:         userDAO.updateUser(user);
Line 1155:     }
Line 1156:     public UserServiceImpl(UserDAO dao, SecurityService security) {
Line 1157:         this.userDAO = dao;
Line 1158:         this.securityService = security;
Line 1159:     }
Line 1160: }
Line 1161: 5.7.2. Race Results Enhanced
Line 1162: Please enhance the Race Results example (see Section 5.4) with the following functionality:
Line 1163: • RaceResultsService should send messages with the results of different categories of race - e.g.
Line 1164: horse races, F1 races, boat-races, etc. Subscribers should be able to subscribe to selected categories.
Line 1165: Make sure they receive only messages related to the ones they have signed up for.
Line 1166: • Each message sent by RaceResultsService should be logged. Introduce a logging collaborator,
Line 1167: and make sure that the date and text of each message is logged. Do not implement the logging
Line 1168: mechanism: concentrate on the interactions between the service and its collaborator.
Line 1169: • In the tests implemented so far, RaceResultsService sends only one message. This is unrealistic!
Line 1170: Enhance the tests to ensure that subscribers will receive any number of sent messages.
Line 1171: • What should happen if a client that is not subscribed tries to unsubscribe? Make up your mind about
Line 1172: it, write a test which verifies this behaviour, and make RaceResultsService behave accordingly.
Line 1173: 5.7.3. Booking System Revisited
Line 1174: You have already written one booking system (see Section 4.11.3). This time, you are asked to
Line 1175: implement a similar application, but testing it using test doubles. Below, you will find a description
Line 1176: 93
Line 1177: 
Line 1178: --- 페이지 109 ---
Line 1179: Chapter 5. Mocks, Stubs, and Dummies
Line 1180: and some requirements that will help you to start coding. If some details are omitted, simply make
Line 1181: them up during the development.
Line 1182: This booking system allows classrooms to be booked. Each classroom has a certain capacity (e.g. for
Line 1183: 20 people), and can be equipped with an overhead projector, microphone and whiteboard. It also has
Line 1184: a unique name (ID, number, whatever you wish to call it…). The API of the system should allow one
Line 1185: to:
Line 1186: • list all existing classrooms,
Line 1187: • list all available classrooms (for a given day and hourly time slot),
Line 1188: • book a specific classroom by name (e.g. "I want to book classroom A1": book("A1")),
Line 1189: • book a specific classroom by specifying some constraints (e.g. "I want to book a classroom with a
Line 1190: projector for 20 people": book(20, Equipment.PROJECTOR)).
Line 1191: Here are some additional constraints, so the system is not too complex at first:
Line 1192: • only periodical booking is supported, which means you can book, for example, classroom A1 for
Line 1193: every Friday from 10 to 11 am, but not just for Friday the 13th of May.
Line 1194: • each booking lasts for 1 hour; no longer or shorter periods are allowed.
Line 1195: Once you have implemented the system specified above, use your imagination and add some more
Line 1196: complexity. For example:
Line 1197: • each booking operation should be written to logs12,
Line 1198: • each classroom has a "cleaning hour", when it is not available,
Line 1199: • the booking time is no longer limited to 1 hour
Line 1200: 5.7.4. Read, Read, Read!
Line 1201: This is not so much an exercise as a reminder: namely, that you really should read Mockito’s
Line 1202: documentation if you plan to use it. This book gives you a good understanding of what Mockito is
Line 1203: good for, and explains the core syntax, but does not try to discuss every detail of Mockito’s API.
Line 1204: Please, spend some time reading the official Mockito documentation and browsing Javadocs!
Line 1205: 12Please read http://www.mockobjects.com/2007/04/test-smell-logging-is-also-feature.html before implementing this feature.
Line 1206: 94
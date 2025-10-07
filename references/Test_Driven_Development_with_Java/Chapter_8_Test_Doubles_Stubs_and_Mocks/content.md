Line 1: 
Line 2: --- 페이지 142 ---
Line 3: 8
Line 4: Test Doubles – Stubs and Mocks
Line 5: In this chapter, we’re going to solve a common testing challenge. How do you test an object that 
Line 6: depends on another object? What do we do if that collaborator is difficult to set up with test data? 
Line 7: Several techniques are available to help us with this and they build on the SOLID principles we learned 
Line 8: previously. We can use the idea of dependency injection to enable us to replace collaborating objects 
Line 9: with ones specially written to help us write our test.
Line 10: These new objects are called test doubles, and we will learn about two important kinds of test double 
Line 11: in this chapter. We will learn when to apply each kind of test double and then learn two ways of 
Line 12: creating them in Java – both by writing the code ourselves and by using the popular library Mockito. 
Line 13: By the end of the chapter, we will have techniques that allow us to write tests for objects where it is 
Line 14: difficult or impossible to test them with the real collaborating objects in place. This allows us to use 
Line 15: TDD with complex systems.
Line 16: In this chapter, we’re going to cover the following main topics:
Line 17: •	 The problems of testing collaborators
Line 18: •	 The purpose of test doubles
Line 19: •	 Using stubs for pre-canned results
Line 20: •	 Using mocks to verify interactions
Line 21: •	 Understanding when test doubles are appropriate
Line 22: •	 Working with Mockito – a popular mocking library
Line 23: •	 Driving error handling code using stubs
Line 24: •	 Testing an error condition in Wordz
Line 25: Technical requirements
Line 26: The code for this chapter can be found at https://github.com/PacktPublishing/Test-
Line 27: Driven-Development-with-Java/tree/main/chapter08.
Line 28: 
Line 29: --- 페이지 143 ---
Line 30: Test Doubles – Stubs and Mocks
Line 31: 120
Line 32: The problems collaborators present for testing
Line 33: In this section, we will understand the challenges that arise as we grow our software into a larger code 
Line 34: base. We will review what is meant by a collaborating object, then we will take a look at two examples 
Line 35: of collaborations that are challenging to test.
Line 36: As we grow our software system, we will soon outgrow what can go in a single class (or function, 
Line 37: for that matter). We will split our code into multiple parts. If we pick a single object as our subject 
Line 38: under test, any other object that it depends on is a collaborator. Our TDD tests must account for the 
Line 39: presence of these collaborators. Sometimes, this is straightforward, as we’ve seen in earlier chapters.
Line 40: Unfortunately, things aren’t always that simple. Some collaborations make tests difficult – or impossible 
Line 41: – to write. These kinds of collaborators introduce either unrepeatable behaviors that we must contend 
Line 42: with or present errors that are difficult to trigger.
Line 43: Let’s review these challenges with some short examples. We’ll start with a common problem: a 
Line 44: collaborator that exhibits unrepeatable behavior.
Line 45: The challenges of testing unrepeatable behavior
Line 46: We’ve learned that the basic steps of a TDD test are Arrange, Act, and Assert. We ask the object to act and 
Line 47: then assert that an expected outcome happens. But what happens when that outcome is unpredictable?
Line 48: To illustrate, let’s review a class that rolls a die and presents a text string to say what we rolled:
Line 49: package examples;
Line 50: import java.util.random.RandomGenerator;
Line 51: public class DiceRoll {
Line 52:     private final int NUMBER_OF_SIDES = 6;
Line 53:     private final RandomGenerator rnd =
Line 54:                        RandomGenerator.getDefault();
Line 55:     public String asText() {
Line 56:         int rolled = rnd.nextInt(NUMBER_OF_SIDES) + 1;
Line 57:         return String.format("You rolled a %d", rolled);
Line 58:     }
Line 59: }
Line 60: 
Line 61: --- 페이지 144 ---
Line 62: The problems collaborators present for testing
Line 63: 121
Line 64: This is simple enough code, with only a handful of executable lines in it. Sadly, simple to write is not 
Line 65: always simple to test. How would we write a test for this? Specifically – how would we write the assert? 
Line 66: In previous tests, we’ve always known exactly what to expect in the assertion. Here, the assertion will be 
Line 67: some fixed text plus a random number. We don’t know in advance what that random number will be.
Line 68: The challenges of testing error handling
Line 69: Testing code that handles error conditions is another challenge. The difficulty here lies not in asserting 
Line 70: that the error was handled, but rather the challenge is how to trigger that error to happen inside the 
Line 71: collaborating object.
Line 72: To illustrate, let’s imagine a code to warn us when the battery in our portable device is getting low:
Line 73: public class BatteryMonitor {
Line 74:     public void warnWhenBatteryPowerLow() {
Line 75:         if (DeviceApi.getBatteryPercentage() < 10) {
Line 76:             System.out.println("Warning - Battery low");
Line 77:         }
Line 78:     }
Line 79: }
Line 80: The preceding code in BatteryMonitor features a DeviceApi class, which is a library class 
Line 81: that lets us read how much battery we have left on our phone. It provides a static method to do this, 
Line 82: called getBatteryPercentage(). This will return an integer in the range 0 to 100 percent. The 
Line 83: code that we want to write a TDD test for calls getBatteryPercentage() and will display a 
Line 84: warning message if it is less than 10 percent. But there’s a problem writing this test: how can we force 
Line 85: the getBatteryPercentage() method to return a number less than 10 as part of our Arrange 
Line 86: step? Would we discharge the battery somehow? How would we do this?
Line 87: BatteryMonitor provides an example of code that collaborates with another object, where it is 
Line 88: impossible to force a known response from that collaborator. We have no way to change the value 
Line 89: that getBatteryPercentage() will return. We would literally have to wait until the battery 
Line 90: had discharged before this test could pass. That’s not what TDD is about.
Line 91: Understanding why these collaborations are challenging
Line 92: When doing TDD, we want fast and repeatable tests. Any scenario that involves unpredictable behavior 
Line 93: or requires us to control a situation that we have no control over clearly causes problems for TDD.
Line 94: The best way to write tests in these cases is by eliminating the cause of the difficulty. Fortunately, a 
Line 95: simple solution exists. We can apply the Dependency Injection Principle we learned about in the previous 
Line 96: chapter, along with one new idea – the test double. We will review test doubles in the next section.
Line 97: 
Line 98: --- 페이지 145 ---
Line 99: Test Doubles – Stubs and Mocks
Line 100: 122
Line 101: The purpose of test doubles
Line 102: In this section, we’re going to learn techniques that allow us to test these challenging collaborations. 
Line 103: We will introduce the idea of test doubles. We will learn how to apply the SOLID principles to design 
Line 104: code flexible enough to use these test doubles.
Line 105: The challenges of the previous section are solved by using test doubles. A test double replaces one of 
Line 106: the collaborating objects in our test. By design, this test double avoids the difficulties of the replaced 
Line 107: object. Think of them as the stunt doubles in movies, replacing the real actors to help safely get an 
Line 108: action shot.
Line 109: A software test double is an object we have written specifically to be easy to use in our unit test. In 
Line 110: the test, we inject our test double into the SUT in the Arrange step. In production code, we inject in 
Line 111: the production object that our test double had replaced.
Line 112: Let’s reconsider our DiceRoll example earlier. How would we refactor that code to make it easier 
Line 113: to test?
Line 114: 1.	
Line 115: Create an interface that abstracts the source of random numbers:
Line 116: interface RandomNumbers {
Line 117:     int nextInt(int upperBoundExclusive);
Line 118: }
Line 119: 2.	
Line 120: Apply the Dependency Inversion Principle to class DiceRoll to make use of this abstraction:
Line 121: package examples;
Line 122: import java.util.random.RandomGenerator;
Line 123: public class DiceRoll {
Line 124:     private final int NUMBER_OF_SIDES = 6;
Line 125:     private final RandomNumbers rnd ;
Line 126:     public DiceRoll( RandomNumbers r ) {
Line 127:         this.rnd = r;
Line 128:     }
Line 129:     public String asText() {
Line 130:         int rolled = rnd.nextInt(NUMBER_OF_SIDES) + 1;
Line 131:         return String.format("You rolled a %d",
Line 132: 
Line 133: --- 페이지 146 ---
Line 134: The purpose of test doubles
Line 135: 123
Line 136:                              rolled);
Line 137:     }
Line 138: }
Line 139: We have inverted the dependency on the random number generator by replacing it with the 
Line 140: RandomNumbers interface. We added a constructor that allows a suitable RandomNumbers 
Line 141: implementation to be injected. We assign that to the rnd field. The asText() method now 
Line 142: calls the nextInt() method on whatever object we passed to the constructor.
Line 143: 3.	
Line 144: Write a test, using a test double to replace the RandomNumbers source:
Line 145: package examples;
Line 146: import org.junit.jupiter.api.Test;
Line 147: import static org.assertj.core.api.Assertions.assertThat;
Line 148: class DiceRollTest {
Line 149:     @Test
Line 150:     void producesMessage() {
Line 151:         var stub = new StubRandomNumbers();
Line 152:         var roll = new DiceRoll(stub);
Line 153:         var actual = roll.asText();
Line 154:         assertThat(actual).isEqualTo("You rolled a
Line 155:                                      5");
Line 156:     }
Line 157: }
Line 158: We see the usual Arrange, Act, and Assert sections in this test. The new idea here is class 
Line 159: StubRandomNumbers. Let’s look at the stub code:
Line 160: package examples;
Line 161: public class StubRandomNumbers implements RandomNumbers {
Line 162:     @Override
Line 163:     public int nextInt(int upperBoundExclusive) {
Line 164:         return 4;  // @see https://xkcd.com/221
Line 165:     }
Line 166: }
Line 167: 
Line 168: --- 페이지 147 ---
Line 169: Test Doubles – Stubs and Mocks
Line 170: 124
Line 171: There are a few things to notice about this stub. Firstly, it implements our RandomNumbers 
Line 172: interface, making it an LSP-compliant substitute for that interface. This allows us to inject it 
Line 173: into the constructor of DiceRoll, our SUT. The second most important aspect is that every 
Line 174: call to nextInt() will return the same number.
Line 175: By replacing the real RandomNumbers source with a stub that delivers a known value, we have 
Line 176: made our test assertion easy to write. The stub eliminates the problem of unrepeatable values from 
Line 177: the random generator.
Line 178: We can now see how the DiceRollTest works. We supply a test double to our SUT. The test double 
Line 179: always returns the same value. As a result, we can assert against a known outcome.
Line 180: Making the production version of the code
Line 181: To make class DiceRoll work properly in production, we would need to inject a genuine source 
Line 182: of random numbers. A suitable class would be the following:
Line 183: public class RandomlyGeneratedNumbers implements RandomNumbers 
Line 184: {
Line 185:     private final RandomGenerator rnd =
Line 186:                        RandomGenerator.getDefault();
Line 187:     @Override
Line 188:     public int nextInt(int upperBoundExclusive) {
Line 189:         return rnd.nextInt(upperBoundExclusive);
Line 190:     }
Line 191: }
Line 192: There isn’t much work to do here – the preceding code simply implements the nextInt() method 
Line 193: using the RandomGenerator library class built into Java.
Line 194: We can now use this to create our production version of the code.  We already changed our DiceRoll 
Line 195: class to allow us to inject in any suitable implementation of the RandomNumbers interface. For 
Line 196: our test code, we injected in a test double – an instance of the StubRandomNumbers class. For 
Line 197: our production code, we will instead inject in an instance of the RandomlyGeneratedNumbers 
Line 198: class. The production code will use that object to create real random numbers – and there will be no 
Line 199: code changes inside the DiceRoll class. We have used the Dependency Inversion Principle to make 
Line 200: class DiceRoll configurable by dependency injection. This means that class DiceRoll now 
Line 201: follows the Open/Closed Principle – it is open to new kinds of random number generation behavior 
Line 202: but closed to code changes inside the class itself.
Line 203: 
Line 204: --- 페이지 148 ---
Line 205: The purpose of test doubles
Line 206: 125
Line 207: Dependency inversion, dependency injection, and inversion of control
Line 208: The preceding example shows these three ideas in action. Dependency inversion is the design 
Line 209: technique where we create an abstraction in our code. Dependency injection is the runtime 
Line 210: technique where we supply an implementation of that abstraction to code that depends on it. 
Line 211: Together, these ideas are often termed Inversion of Control (IoC). Frameworks such as Spring 
Line 212: are sometimes called IoC containers because they provide tools to help you manage creating 
Line 213: and injecting dependencies in an application.
Line 214: The following code is an example of how we would use DiceRoll and RandomlyGeneratedNumbers 
Line 215: in production:
Line 216: public class DiceRollApp {
Line 217:     public static void main(String[] args) {
Line 218:         new DiceRollApp().run();
Line 219:     }
Line 220:     private void run() {
Line 221:         var rnd = new RandomlyGeneratedNumbers();
Line 222:         var roll = new DiceRoll(rnd);
Line 223:         System.out.println(roll.asText());
Line 224:     }
Line 225: }
Line 226: You can see in the previous code that we inject an instance of the production-version 
Line 227: RandomlyGeneratedNumbers class into the DiceRoll class. This process of creating and 
Line 228: injecting objects is often termed object wiring. Frameworks such as Spring (https://spring.
Line 229: io/), Google Guice (https://github.com/google/guice), and the built-in Java CDI 
Line 230: (https://docs.oracle.com/javaee/6/tutorial/doc/giwhl.html) provide ways 
Line 231: to minimize the boilerplate of creating dependencies and wiring them up, using annotations.
Line 232: Using DIP to swap a production object for a test double is a very powerful technique. This test double 
Line 233: is an example of a kind of double known as a stub. We’ll cover what a stub is along with when to use 
Line 234: one in the next section.
Line 235: 
Line 236: --- 페이지 149 ---
Line 237: Test Doubles – Stubs and Mocks
Line 238: 126
Line 239: Using stubs for pre-canned results
Line 240: The previous section explained that test doubles were a kind of object that could stand in for a 
Line 241: production object so that we could write a test more easily. In this section, we will take a closer look 
Line 242: at that test double and generalize it.
Line 243: In the preceding DiceRoll example, the test was simpler to write because we replaced the random 
Line 244: number generation with a known, fixed value. Our genuine random number generator made it difficult 
Line 245: to write an assertion, as we were never sure what the expected random number should be. Our test 
Line 246: double was an object that instead supplied a well-known value. We can then work out the expected 
Line 247: value for our assertion, making our test easy to write.
Line 248: A test double that supplies values like this is called a stub. Stubs always replace an object that we 
Line 249: cannot control with a test-only version that we can control. They always produce known data values 
Line 250: for our code under test to consume. Graphically, a stub looks like this:
Line 251: Figure 8.1 – Replacing a collaborator with a stub
Line 252: In the diagram, our test class is responsible for wiring up our SUT to an appropriate stub object in the 
Line 253: Arrange step. When the Act step asks our SUT to execute the code we want to test, that code will pull 
Line 254: the known data values from the stub. The Assert step can be written based on the expected behavior 
Line 255: that these known data values will cause.
Line 256: It is important to note why this works. One objection to this arrangement is that we are not testing 
Line 257: the real system. Our SUT is wired up to some object that will never be part of our production system. 
Line 258: That is true. But this works because our test is only testing the logic within the SUT. This test is not 
Line 259: testing the behavior of the dependencies themselves. Indeed, it must not attempt to do that. Testing 
Line 260: the test double is a classic anti-pattern for unit tests.
Line 261: Our SUT has used the Dependency Inversion Principle to fully isolate itself from the object the stub 
Line 262: is standing in for. It makes no difference to the SUT how it gets its data from its collaborator. That’s 
Line 263: why this testing approach is valid.
Line 264: 
Line 265: --- 페이지 150 ---
Line 266: Using mocks to verify interactions
Line 267: 127
Line 268: When to use stub objects
Line 269: Stubs are useful whenever our SUT uses a pull model of collaborating with a dependency. Some 
Line 270: examples of when using stubs makes sense are as follows:
Line 271: •	 Stubbing a repository interface/database: Using a stub instead of calling to a real database 
Line 272: for data access code
Line 273: •	 Stubbing reference data sources: Replacing properties files or web services containing reference 
Line 274: data with stub data
Line 275: •	 Providing application objects to code that converts to HTML or JSON formats: When testing 
Line 276: code that converts to HTML or JSON, supply input data with a stub
Line 277: •	 Stubbing the system clock to test time-dependent behavior: To get repeatable behavior out 
Line 278: of a time call, stub the call with known times
Line 279: •	 Stubbing random number generators to create predictability: Replace a call to a random 
Line 280: number generator with a call to a stub
Line 281: •	 Stubbing authentication systems to always allow a test user to log in: Replace calls to 
Line 282: authentication systems with simple “login succeeded” stubs
Line 283: •	 Stubbing responses from a third-party web service such as a payment provider: Replace 
Line 284: real calls to third-party services with calls to a stub
Line 285: •	 Stubbing a call to an operating system command: Replace a call to the OS to, for example, 
Line 286: list a directory with pre-canned stub data
Line 287: In this section, we have seen how using stubs allows us to control data that gets supplied to an SUT. 
Line 288: It supports a pull model of fetching objects from elsewhere. But that’s not the only mechanism by 
Line 289: which objects can collaborate. Some objects use a push model. In this case, when we call a method on 
Line 290: our SUT, we expect it to call another method on some other object. Our test must confirm that this 
Line 291: method call actually took place. This is something that stubs cannot help with and needs a different 
Line 292: approach. We will cover this approach in the next section.
Line 293: Using mocks to verify interactions
Line 294: In this section, we’ll take a look at another important kind of test double: the mock object. Mock 
Line 295: objects solve a slightly different problem than stub objects do, as we shall see in this section.
Line 296: Mock objects are a kind of test double that record interactions. Unlike stubs, which supply well-known 
Line 297: objects to the SUT, a mock will simply record interactions that the SUT has with the mock. It is the 
Line 298: perfect tool to answer the question, “Did the SUT call the method correctly?” This solves the problem 
Line 299: of push model interactions between the SUT and its collaborator. The SUT commands the collaborator 
Line 300: to do something rather than requesting something from it. A mock provides a way to verify that it 
Line 301: issued that command, along with any necessary parameters.
Line 302: 
Line 303: --- 페이지 151 ---
Line 304: Test Doubles – Stubs and Mocks
Line 305: 128
Line 306: The following UML object diagram shows the general arrangement:
Line 307: Figure 8.2 – Replace collaborator with mock
Line 308: We see our test code wiring up a mock object to the SUT. The Act step will make the SUT execute code 
Line 309: that we expect to interact with its collaborator. We have swapped out that collaborator for a mock, 
Line 310: which will record the fact that a certain method was called on it.
Line 311: Let’s look at a concrete example to make this easier to understand. Suppose our SUT is expected to 
Line 312: send an email to a user. Once again, we will use the Dependency Inversion Principle to create an 
Line 313: abstraction of our mail server as an interface:
Line 314: public interface MailServer {
Line 315:     void sendEmail(String recipient, String subject,
Line 316:                    String text);
Line 317: }
Line 318: The preceding code shows a simplified interface only suitable for sending a short text email. It is good 
Line 319: enough for our purposes. To test the SUT that called the sendEmail() method on this interface, 
Line 320: we would write a MockMailServer class:
Line 321: public class MockMailServer implements MailServer {
Line 322:     boolean wasCalled;
Line 323:     String actualRecipient;
Line 324:     String actualSubject;
Line 325:     String actualText;
Line 326:     @Override
Line 327:     public void sendEmail(String recipient, String subject,
Line 328:                           String text) {
Line 329:         wasCalled = true;
Line 330:         actualRecipient = recipient;
Line 331:         actualSubject = subject;
Line 332:         actualText = text;
Line 333: 
Line 334: --- 페이지 152 ---
Line 335: Using mocks to verify interactions
Line 336: 129
Line 337:     }
Line 338: }
Line 339: The preceding MockMailServer class implements the MailServer interface. It has a single 
Line 340: responsibility – to record the fact that the sendEmail() method was called and to capture the 
Line 341: actual parameter values sent to that method. It exposes these as simple fields with package-public 
Line 342: visibility. Our test code can use these fields to form the assertion. Our test simply has to wire up this 
Line 343: mock object to the SUT, cause the SUT to execute code that we expect to call the sendEmail() 
Line 344: method, and then check that it did do that:
Line 345: @Test
Line 346: public void sendsWelcomeEmail() {
Line 347:     var mailServer = new MockMailServer();
Line 348:     var notifications = new UserNotifications(mailServer);
Line 349:     notifications.welcomeNewUser();
Line 350:     assertThat(mailServer.wasCalled).isTrue();
Line 351:     assertThat(mailServer.actualRecipient)
Line 352:          .isEqualTo("test@example.com");
Line 353:     assertThat(mailServer.actualSubject)
Line 354:          .isEqualTo("Welcome!");
Line 355:     assertThat(mailServer.actualText)
Line 356:          .contains("Welcome to your account");
Line 357: }
Line 358: We can see that this test wires up the mock to our SUT, then causes the SUT to execute the 
Line 359: welcomeNewUser() method. We expect this method to call the sendEmail() method on the 
Line 360: MailServer object. Then, we need to write assertions to confirm that call was made with the correct 
Line 361: parameter values passed. We’re using the idea of four assert statements logically here and testing one 
Line 362: idea – effectively a single assert.
Line 363: The power of mock objects is that we can record interactions with objects that are difficult to control. 
Line 364: In the case of a mail server, such as the one seen in the preceding code block, we would not want 
Line 365: to be sending actual emails to anybody. We also would not want to write a test that waited around 
Line 366: monitoring the mailbox of a test user. Not only is this slow and can be unreliable, but it is also not what 
Line 367: we intend to test. The SUT only has the responsibility of making the call to sendEmail() – what 
Line 368: happens after that is out of the scope of the SUT. It is, therefore, out of scope for this test.
Line 369: 
Line 370: --- 페이지 153 ---
Line 371: Test Doubles – Stubs and Mocks
Line 372: 130
Line 373: As in the previous examples with other test doubles, the fact that we have used the Dependency 
Line 374: Inversion Principle means our production code is easy enough to create. We simply need to create 
Line 375: an implementation of MailServer that uses the SMTP protocol to talk to a real mail server. We 
Line 376: would most likely search for a library class that does that for us already, then we would need to make 
Line 377: a very simple adapter object that binds that library code to our interface.
Line 378: This section has covered two common kinds of test double, stubs, and mocks. But test doubles are 
Line 379: not always appropriate to use. In the next section, we’ll discuss some issues to be aware of when using 
Line 380: test doubles.
Line 381: Understanding when test doubles are appropriate
Line 382: Mock objects are a useful kind of test double, as we have seen. But they are not always the right 
Line 383: approach. There are some situations where we should actively avoid using mocks. These situations 
Line 384: include over-using mocks, using mocks for code you don’t own, and mocking value objects. We’ll look 
Line 385: at these situations next. Then, we’ll recap with general advice for where mocks are typically useful. 
Line 386: Let’s start by considering the problems caused when we overuse mock objects.
Line 387: Avoiding the overuse of mock objects
Line 388: At a first glance, using mock objects seems to solve a number of problems for us. Yet if used without 
Line 389: care, we can end up with very poor-quality tests. To understand why, let’s go back to our basic definition 
Line 390: of a TDD test. It is a test that verifies behaviors and is independent of implementations. If we use a 
Line 391: mock object to stand in for a genuine abstraction, then we are complying with that.
Line 392: The potential problem happens because it is all too easy to create a mock object for an implementation 
Line 393: detail, not an abstraction. If we do this, we end up locking our code into a specific implementation and 
Line 394: structure. Once a test is coupled to a specific implementation detail, then changing that implementation 
Line 395: requires a change to the test. If the new implementation has the same outcomes as the old one, the 
Line 396: test really should still pass. Tests that depend on specific implementation details or code structures 
Line 397: actively impede refactoring and adding new features.
Line 398: Don’t mock code you don’t own
Line 399: Another area where mocks should not be used is as a stand-in for a concrete class written outside 
Line 400: of your team. Suppose we are using a class called PdfGenerator from a library to create a PDF 
Line 401: document. Our code would call methods on the PdfGenerator class. We might think it would be 
Line 402: easy to test our code if we use a mock object to stand in for the PdfGenerator class.
Line 403: This approach has a problem that will only arise in the future. The class in the external library will 
Line 404: quite likely change. Let’s say that the PdfGenerator class removes one of the methods our code is 
Line 405: calling. We will be forced to update the library version at some point as part of our security policy if 
Line 406: nothing else. When we pull in the new version, our code will no longer compile against this changed 
Line 407: 
Line 408: --- 페이지 154 ---
Line 409: Understanding when test doubles are appropriate
Line 410: 131
Line 411: class – but our tests will still pass because the mock object still has the old method in it. This is a subtle 
Line 412: trap that we have laid for future maintainers of the code. It is best avoided. A reasonable approach is 
Line 413: to wrap the third-party library, and ideally place it behind an interface to invert the dependency on 
Line 414: it, isolating it fully.
Line 415: Don’t mock value objects
Line 416: A value object is an object that has no specific identity, it is defined only by the data it contains. Some 
Line 417: examples would include an integer or a string object. We consider two strings to be the same if they 
Line 418: contain the same text. They might be two separate string objects in memory, but if they hold the same 
Line 419: value, we consider them to be equal.
Line 420: The clue that something is a value object in Java is the presence of a customized equals() and 
Line 421: hashCode() method. By default, Java compares the equality of two objects using their identity – 
Line 422: it checks that two object references are referring to the same object instance in memory. We must 
Line 423: override the equals() and hashCode() methods to provide the correct behavior for value 
Line 424: objects, based on their content.
Line 425: A value object is a simple thing. It may have some complex behaviors inside its methods but, in 
Line 426: principle, value objects should be easy to create. There is no benefit in creating a mock object to stand 
Line 427: in for one of these value objects. Instead, create the value object and use it in your test.
Line 428: You can’t mock without dependency injection
Line 429: Test doubles can only be used where we can inject them. This is not always possible. If the code we 
Line 430: want to test creates a concrete class using the new keyword, then we cannot replace it with a double:
Line 431: package examples;
Line 432: public class UserGreeting {
Line 433:     private final UserProfiles profiles
Line 434:         = new UserProfilesPostgres();
Line 435:     public String formatGreeting(UserId id) {
Line 436:         return String.format("Hello and welcome, %s",
Line 437:                 profiles.fetchNicknameFor(id));
Line 438:     }
Line 439: }
Line 440: 
Line 441: --- 페이지 155 ---
Line 442: Test Doubles – Stubs and Mocks
Line 443: 132
Line 444: We see that the profiles field has been initialized using a concrete class UserProfilesPostgres(). 
Line 445: There is no direct way to inject a test double with this design. We could attempt to get around this, 
Line 446: using Java Reflection, but it is best to consider this as TDD feedback on a limitation of our design. The 
Line 447: solution is to allow the dependency to be injected, as we have seen in previous examples.
Line 448: This is often a problem with legacy code, which is simply code that has been written before we work 
Line 449: on it. If this code has created concrete objects – and the code cannot be changed – then we cannot 
Line 450: apply a test double.
Line 451: Don’t test the mock
Line 452: Testing the mock is a phrase used to describe a test with too many assumptions built into a test double. 
Line 453: Suppose we write a stub that stands in for some database access, but that stub contains hundreds of 
Line 454: lines of code to emulate detailed specific queries to that database. When we write the test assertions, 
Line 455: they will all be based on those detailed queries that we emulated in the stub.
Line 456: That approach will prove that the SUT logic responds to those queries. But our stub now assumes a 
Line 457: great deal about how the real data access code will work. The stub code and the real data access code 
Line 458: can quickly get out of step. This results in an invalid unit test that passes but with stubbed responses 
Line 459: that can no longer happen in reality.
Line 460: When to use mock objects
Line 461: Mocks are useful whenever our SUT is using a push model and requesting an action from some other 
Line 462: component, where there is no obvious response such as the following:
Line 463: •	 Requesting an action from a remote service, such as sending an email to a mail server
Line 464: •	 Inserting or deleting data from a database
Line 465: •	 Sending a command over a TCP socket or serial interface
Line 466: •	 Invalidating a cache
Line 467: •	 Writing logging information either to a log file or distributing logging endpoint
Line 468: We’ve learned some techniques in this section that allow us to verify that an action was requested. 
Line 469: We have seen how we can use the Dependency Inversion Principle once again to allow us to inject 
Line 470: a test double which we can query. We’ve also seen an example of hand-written code to do this. But 
Line 471: must we always write test doubles by hand? In the next section, we will cover a very useful library 
Line 472: that does most of the work for us.
Line 473: 
Line 474: --- 페이지 156 ---
Line 475: Working with Mockito – a popular mocking library
Line 476: 133
Line 477: Working with Mockito – a popular mocking library
Line 478: The previous sections have shown examples of using stubs and mocks to test code. We have been 
Line 479: writing these test doubles by hand. It’s obviously quite repetitive and time-consuming to do this. It 
Line 480: begs the question of if this repetitive boilerplate code can be automated away. Thankfully for us, it 
Line 481: can. This section will review the help available in the popular Mockito library.
Line 482: Mockito is a free-of-charge open source library under the MIT license. This license means we can use 
Line 483: this for commercial development work, subject to agreement by those we work for. Mockito provides 
Line 484: a large range of features aimed at creating test doubles with very little code. The Mockito website can 
Line 485: be found at https://site.mockito.org/.
Line 486: Getting started with Mockito
Line 487: Getting started with Mockito is straightforward. We pull in the Mockito library and an extension 
Line 488: library in our Gradle file. The extension library allows Mockito to integrate closely with JUnit5.
Line 489: The excerpt of build.gradle looks like this:
Line 490: dependencies {
Line 491:     testImplementation 'org.junit.jupiter:junit-jupiter-
Line 492: api:5.8.2'
Line 493:     testRuntimeOnly 'org.junit.jupiter:junit-jupiter-
Line 494: engine:5.8.2'
Line 495:     testImplementation 'org.assertj:assertj-core:3.22.0'
Line 496:     testImplementation 'org.mockito:mockito-core:4.8.0'
Line 497:     testImplementation 'org.mockito:mockito-junit-
Line 498: jupiter:4.8.0'
Line 499: }
Line 500: Writing a stub with Mockito
Line 501: Let’s see how Mockito helps us create a stub object. We’ll use TDD to create a UserGreeting class 
Line 502: that delivers a personalized greeting, after fetching our nickname from interface UserProfiles.
Line 503: Let’s write this using small steps, to see how TDD and Mockito work together:
Line 504: 1.	
Line 505: Write the basic JUnit5 test class and integrate it with Mockito:
Line 506: package examples
Line 507: import org.junit.jupiter.api.extension.ExtendWith;
Line 508: import org.mockito.junit.jupiter.MockitoExtension;
Line 509: 
Line 510: --- 페이지 157 ---
Line 511: Test Doubles – Stubs and Mocks
Line 512: 134
Line 513: @ExtendWith(MockitoExtension.class)
Line 514: public class UserGreetingTest {
Line 515: }
Line 516: @ExtendWith(MockitoExtension.class) marks this test as using Mockito. When 
Line 517: we run this JUnit5 test, the annotation ensures that the Mockito library code is run.
Line 518: 2.	
Line 519: Add a test confirming the expected behavior. We will capture this in an assertion:
Line 520: package examples;
Line 521: import org.junit.jupiter.api.Test;
Line 522: import org.junit.jupiter.api.extension.ExtendWith;
Line 523: import org.mockito.junit.jupiter.MockitoExtension;
Line 524: import static org.assertj.core.api.Assertions.assertThat;
Line 525: @ExtendWith(MockitoExtension.class)
Line 526: public class UserGreetingTest {
Line 527:     @Test
Line 528:     void formatsGreetingWithName() {
Line 529:         String actual = «»;
Line 530:         assertThat(actual)
Line 531:            .isEqualTo("Hello and welcome, Alan");
Line 532:     }
Line 533: }
Line 534: This is standard usage of the JUnit and AssertJ frameworks as we have seen before. If we run 
Line 535: the test now, it will fail.
Line 536: 3.	
Line 537: Drive out our SUT – the class we want to write – with an Act step:
Line 538: package examples;
Line 539: import org.junit.jupiter.api.Test;
Line 540: import org.junit.jupiter.api.extension.ExtendWith;
Line 541: import org.mockito.junit.jupiter.MockitoExtension;
Line 542: 
Line 543: --- 페이지 158 ---
Line 544: Working with Mockito – a popular mocking library
Line 545: 135
Line 546: import static org.assertj.core.api.Assertions.assertThat;
Line 547: @ExtendWith(MockitoExtension.class)
Line 548: public class UserGreetingTest {
Line 549:     private static final UserId USER_ID
Line 550:         = new UserId("1234");
Line 551:     @Test
Line 552:     void formatsGreetingWithName() {
Line 553:         var greeting = new UserGreeting();
Line 554:         String actual =
Line 555:             greeting.formatGreeting(USER_ID);
Line 556:         assertThat(actual)
Line 557:             .isEqualTo("Hello and welcome, Alan");
Line 558:     }
Line 559: }
Line 560: This step drives out the two new production code classes, as shown in the following steps.
Line 561: 4.	
Line 562: Add a class UserGreeting skeleton:
Line 563: package examples;
Line 564: public class UserGreeting {
Line 565:     public String formatGreeting(UserId id) {
Line 566:         throw new UnsupportedOperationException();
Line 567:     }
Line 568: }
Line 569: As usual, we add no code beyond what is required to make our test compile. The design decision 
Line 570: captured here shows that our behavior is provided by a formatGreeting()method, which 
Line 571: identifies a user by a UserId class.
Line 572: 
Line 573: --- 페이지 159 ---
Line 574: Test Doubles – Stubs and Mocks
Line 575: 136
Line 576: 5.	
Line 577: Add a class UserId skeleton:
Line 578: package examples;
Line 579: public class UserId {
Line 580:     public UserId(String id) {
Line 581:     }
Line 582: }
Line 583: Again, we get an empty shell just to get the test to compile. Then, we run the test and it still fails:
Line 584: Figure 8.3 – Test failure
Line 585: 6.	
Line 586: Another design decision to capture is that the UserGreeting class will depend on a 
Line 587: UserProfiles interface. We need to create a field, create the interface skeleton, and inject 
Line 588: the field in a new constructor for the SUT:
Line 589: package examples;
Line 590: import org.junit.jupiter.api.Test;
Line 591: import org.junit.jupiter.api.extension.ExtendWith;
Line 592: import org.mockito.junit.jupiter.MockitoExtension;
Line 593: import static org.assertj.core.api.Assertions.assertThat;
Line 594: @ExtendWith(MockitoExtension.class)
Line 595: public class UserGreetingTest {
Line 596:     private static final UserId USER_ID
Line 597:         = new UserId("1234");
Line 598: 
Line 599: --- 페이지 160 ---
Line 600: Working with Mockito – a popular mocking library
Line 601: 137
Line 602:     private UserProfiles profiles;
Line 603:     @Test
Line 604:     void formatsGreetingWithName() {
Line 605:         var greeting
Line 606:             = new UserGreeting(profiles);
Line 607:         String actual =
Line 608:             greeting.formatGreeting(USER_ID);
Line 609:         assertThat(actual)
Line 610:             .isEqualTo("Hello and welcome, Alan");
Line 611:     }
Line 612: }
Line 613: We continue by adding the bare minimum code to get the test to compile. If we run the test, it will still 
Line 614: fail. But we’ve progressed further so the failure is now an  UnsupportedOperationException 
Line 615: error. This confirms that formatGreeting() has been called:
Line 616: Figure 8.4 – Failure confirms method call
Line 617: 7.	
Line 618: Add behavior to the formatGreeting() method:
Line 619: package examples;
Line 620: public class UserGreeting {
Line 621:     private final UserProfiles profiles;
Line 622:     public UserGreeting(UserProfiles profiles) {
Line 623:         this.profiles = profiles;
Line 624:     }
Line 625: 
Line 626: --- 페이지 161 ---
Line 627: Test Doubles – Stubs and Mocks
Line 628: 138
Line 629:     public String formatGreeting(UserId id) {
Line 630:         return String.format("Hello and Welcome, %s",
Line 631:                 profiles.fetchNicknameFor(id));
Line 632:     }
Line 633: }
Line 634: 8.	
Line 635: Add fetchNicknameFor() to the UserProfiles interface:
Line 636: package examples;
Line 637: public interface UserProfiles {
Line 638:     String fetchNicknameFor(UserId id);
Line 639: }
Line 640: 9.	
Line 641: Run the test. It will fail with a null exception:
Line 642: Figure 8.5 – Null exception failure
Line 643: The test fails because we passed the profiles field as a dependency into our SUT, but that 
Line 644: field has never been initialized. This is where Mockito comes into play (finally).
Line 645: 10.	 Add the @Mock annotation to the profiles field:
Line 646: package examples;
Line 647: import org.junit.jupiter.api.Test;
Line 648: import org.junit.jupiter.api.extension.ExtendWith;
Line 649: import org.mockito.Mock;
Line 650: import org.mockito.junit.jupiter.MockitoExtension;
Line 651: import static org.assertj.core.api.Assertions.assertThat;
Line 652: @ExtendWith(MockitoExtension.class)
Line 653: public class UserGreetingTest {
Line 654: 
Line 655: --- 페이지 162 ---
Line 656: Working with Mockito – a popular mocking library
Line 657: 139
Line 658:     private static final UserId USER_ID = new
Line 659:     UserId("1234");
Line 660:     @Mock
Line 661:     private UserProfiles profiles;
Line 662:     @Test
Line 663:     void formatsGreetingWithName() {
Line 664:         var greeting = new UserGreeting(profiles);
Line 665:         String actual =
Line 666:                greeting.formatGreeting(USER_ID);
Line 667:         assertThat(actual)
Line 668:                 .isEqualTo("Hello and welcome, Alan");
Line 669:     }
Line 670: }
Line 671: Running the test now produces a different failure, as we have not yet configured the Mockito mock:
Line 672: Figure 8.6 – Added mock, not configured
Line 673: 11.	 Configure @Mock to return the correct stub data for our test:
Line 674: package examples;
Line 675: import org.junit.jupiter.api.Test;
Line 676: import org.junit.jupiter.api.extension.ExtendWith;
Line 677: import org.mockito.Mock;
Line 678: 
Line 679: --- 페이지 163 ---
Line 680: Test Doubles – Stubs and Mocks
Line 681: 140
Line 682: import org.mockito.Mockito;
Line 683: import org.mockito.junit.jupiter.MockitoExtension;
Line 684: import static org.assertj.core.api.Assertions.assertThat;
Line 685: import static org.mockito.Mockito.*;
Line 686: @ExtendWith(MockitoExtension.class)
Line 687: public class UserGreetingTest {
Line 688:     private static final UserId USER_ID = new
Line 689:     UserId("1234");
Line 690:     @Mock
Line 691:     private UserProfiles profiles;
Line 692:     @Test
Line 693:     void formatsGreetingWithName() {
Line 694:         when(profiles.fetchNicknameFor(USER_ID))
Line 695:            .thenReturn("Alan");
Line 696:         var greeting = new UserGreeting(profiles);
Line 697:         String actual =
Line 698:                greeting.formatGreeting(USER_ID);
Line 699:         assertThat(actual)
Line 700:                 .isEqualTo("Hello and welcome, Alan");
Line 701:     }
Line 702: }
Line 703: 12.	 If you run the test again, it will fail due to a mistake in the greeting text. Fix this and then 
Line 704: re-run the test, and it will pass:
Line 705: 
Line 706: --- 페이지 164 ---
Line 707: Working with Mockito – a popular mocking library
Line 708: 141
Line 709: Figure 8.7 – Test pass
Line 710: We’ve just created class UserGreeting, which accesses some stored nicknames for the user, 
Line 711: via interface UserProfiles. That interface used DIP to isolate UserGreeting from any 
Line 712: implementation details of that store. We used a stub implementation to write the test. We’ve followed 
Line 713: TDD and leveraged Mockito to write that stub for us.
Line 714: You’ll also notice that the test failed in the final step. I expected that step to pass. It didn’t because I 
Line 715: had typed the greeting message incorrectly. Once again, TDD came to my rescue.
Line 716: Writing a mock with Mockito
Line 717: Mockito can create mock objects just as easily as stubs. We can still use the @Mock annotation on a 
Line 718: field we wish to become a mock – perhaps making sense of the annotation, at last. We use the Mockito 
Line 719: verify() method to check that our SUT called an expected method on a collaborator.
Line 720: Let’s look at how a mock is used. We’ll write a test for some SUT code that we expect to send an email 
Line 721: via MailServer:
Line 722: @ExtendWith(MockitoExtension.class)
Line 723: class WelcomeEmailTest {
Line 724:     @Mock
Line 725:     private MailServer mailServer;
Line 726:     @Test
Line 727:     public void sendsWelcomeEmail() {
Line 728:         var notifications
Line 729:                  = new UserNotifications( mailServer );
Line 730:         notifications.welcomeNewUser("test@example.com");
Line 731:         verify(mailServer).sendEmail("test@example.com",
Line 732:                 "Welcome!",
Line 733: 
Line 734: --- 페이지 165 ---
Line 735: Test Doubles – Stubs and Mocks
Line 736: 142
Line 737:                 "Welcome to your account");
Line 738:     }
Line 739: }
Line 740: In this test, we see the @ExtendWith(MockitoExtension.class) annotation to initialize 
Line 741: Mockito, and the familiar Arrange, Act and Assert format of our test method. The new idea here 
Line 742: is in the assertion. We use the verify() method from the Mockito library to check that the 
Line 743: sendEmail() method was called correctly by our SUT. The check also verifies that it was called 
Line 744: with the correct parameter values.
Line 745: Mockito uses code generation to achieve all this. It wraps the interface we labeled with the @Mock 
Line 746: annotation and intercepts each and every call. It stores parameter values for each call. When we come 
Line 747: to using the verify() method to confirm that the method was called correctly, Mockito has all the 
Line 748: data it needs to do this.
Line 749: Beware Mockito’s when() and verify() syntax!
Line 750: Mockito has subtly different syntax for when() and verify():
Line 751: * when(object.method()).thenReturn(expected value);
Line 752: * verify(object).method();
Line 753: Blurring the distinction between stubs and mocks
Line 754: One thing to note about Mockito terminology is that it blurs the distinction between a stub and a 
Line 755: mock object. In Mockito, we create test doubles that are labeled as mock objects. But in our test, we 
Line 756: can use these doubles as either a stub, a mock, or even a mixture of both.
Line 757: Setting up a test double to be both a stub and a mock is a test code smell. It’s not wrong, but it’s worth 
Line 758: a pause for thought. We should consider if the collaborator that we are both mocking and stubbing 
Line 759: has mixed up some responsibilities. It may be beneficial to split that object up.
Line 760: Argument matchers – customizing behavior of test doubles
Line 761: So far, we have configured Mockito test doubles to respond to very specific inputs to the methods they 
Line 762: replace. The previous MailServer example checked for three specific parameter values being passed to 
Line 763: the sendEmail() method call. But we sometimes want more flexibility in our test doubles.
Line 764: Mockito provides library methods called argument matchers. These are static methods that are used 
Line 765: inside when() and verify() statements. Argument matchers are used to instruct Mockito to 
Line 766: respond to a range of parameter values – including nulls and unknown values – that might get passed 
Line 767: into a method under test.
Line 768: 
Line 769: --- 페이지 166 ---
Line 770: Working with Mockito – a popular mocking library
Line 771: 143
Line 772: The following test uses an argument matcher that accepts any value of UserId:
Line 773: package examples2;
Line 774: import examples.UserGreeting;
Line 775: import examples.UserId;
Line 776: import examples.UserProfiles;
Line 777: import org.junit.jupiter.api.Test;
Line 778: import org.junit.jupiter.api.extension.ExtendWith;
Line 779: import org.mockito.Mock;
Line 780: import org.mockito.junit.jupiter.MockitoExtension;
Line 781: import static org.assertj.core.api.Assertions.assertThat;
Line 782: import static org.mockito.ArgumentMatchers.any;
Line 783: import static org.mockito.Mockito.when;
Line 784: @ExtendWith(MockitoExtension.class)
Line 785: public class UserGreetingTest {
Line 786:     @Mock
Line 787:     private UserProfiles profiles;
Line 788:     @Test
Line 789:     void formatsGreetingWithName() {
Line 790:       when(profiles.fetchNicknameFor(any()))
Line 791:           .thenReturn("Alan");
Line 792:         var greeting = new UserGreeting(profiles);
Line 793:         String actual =
Line 794:           greeting.formatGreeting(new UserId(""));
Line 795:         assertThat(actual)
Line 796:           .isEqualTo("Hello and welcome, Alan");
Line 797:     }
Line 798: }
Line 799: 
Line 800: --- 페이지 167 ---
Line 801: Test Doubles – Stubs and Mocks
Line 802: 144
Line 803: We’ve added an any() argument matcher to the stubbing of the fetchNicknameFor() method. 
Line 804: This instructs Mockito to return the expected value Alan no matter what parameter value is passed 
Line 805: into fetchNicknameFor(). This is useful when writing tests to guide our readers and help them 
Line 806: to understand what is important and what is not for a particular test.
Line 807: Mockito offers a number of argument matchers, described in the Mockito official documentation. 
Line 808: These argument matchers are especially useful when creating a stub to simulate an error condition. 
Line 809: This is the subject of the next section.
Line 810: Driving error handling code with tests
Line 811: In this section, we’re going to look into a great use of stub objects, which is their role in testing 
Line 812: error conditions.
Line 813: As we create our code, we need to ensure that it handles error conditions well. Some error conditions 
Line 814: are easy to test. An example might be a user input validator. To test that it handles the error caused 
Line 815: by invalid data, we simply write a test that feeds it invalid data and then write an assertion to check it 
Line 816: successfully reported the data was invalid. But what about the code that uses it?
Line 817: If our SUT is code that responds to an error condition raised by one of its collaborators, we need to test 
Line 818: that error response. How we test it depends on the mechanism we chose to report that error. We may 
Line 819: be using a simple status code, in which case returning that error code from a stub will work very well.
Line 820: We may also have chosen to use Java exceptions to report this error. Exceptions are controversial. If 
Line 821: misused, they can lead to very unclear control flow in your code. We need to know how to test them, 
Line 822: however, as they appear in several Java libraries and in-house coding styles. Fortunately, there’s nothing 
Line 823: difficult about writing the test for exception-handling code.
Line 824: We start with creating a stub, using any of the approaches covered in this chapter. We then need to 
Line 825: arrange for the stub to throw the appropriate exception when we call a method. Mockito has a nice 
Line 826: feature to do this, so let’s see an example Mockito test that uses exceptions:
Line 827:     @Test
Line 828:     public void rejectsInvalidEmailRecipient() {
Line 829:         doThrow(new IllegalArgumentException())
Line 830:             .when(mailServer).sendEmail(any(),any(),any());
Line 831:         var notifications
Line 832:             = new UserNotifications( mailServer );
Line 833:         assertThatExceptionOfType(NotificationFailureException.
Line 834: class)
Line 835:                 .isThrownBy(()->notifications
Line 836: 
Line 837: --- 페이지 168 ---
Line 838: Testing an error condition in Wordz
Line 839: 145
Line 840:                     .welcomeNewUser("not-an-email-address"));
Line 841:     }
Line 842: At the start of this test, we use Mockito doThrow() to configure our mock object. This configures 
Line 843: the Mockito mock object mailServer to throw IllegalArgumentException whenever 
Line 844: we call sendEmail(), no matter what parameter values we send. This reflects a design decision 
Line 845: to make sendEmail() throw that exception as a mechanism to report that the email address 
Line 846: was not valid. When our SUT calls mailServer.sendEmail(), that method will throw 
Line 847: IllegalArgumentExeption. We can exercise the code that handles this.
Line 848: For this example, we decided to make the SUT wrap and rethrow IllegalArgumentException. 
Line 849: We choose to create a new exception that relates to the responsibility of user notifications. We 
Line 850: will call it NotificationFailureException. The assertion step of the test then uses the 
Line 851: AssertJ library feature assertThatExceptionOfType(). This performs the Act and Assert 
Line 852: steps together. We call our SUT welcomeNewUser() method and assert that it throws our 
Line 853: NotificationFailureException error.
Line 854: We can see how this is enough to trigger the exception-handling response in our SUT code. This 
Line 855: means we can write our test and then drive out the required code. The code we write will include a 
Line 856: catch handler for InvalidArgumentException. In this case, all the new code has to do is throw 
Line 857: a NotificationFailureException error. This is a new class that we will create that extends 
Line 858: RuntimeException. We do this to report that something went wrong by sending a notification. 
Line 859: As part of normal system layering considerations, we want to replace the original exception with a 
Line 860: more general one, which is better suited to this layer of code.
Line 861: This section has examined features of Mockito and AssertJ libraries that help us use TDD to drive out 
Line 862: exception-handling behavior. In the next section, let’s apply this to an error in our Wordz application.
Line 863: Testing an error condition in Wordz
Line 864: In this section, we will apply what we’ve learned by writing a test for a class that will choose a random word 
Line 865: for the player to guess, from a stored set of words. We will create an interface called WordRepository 
Line 866: to access stored words. We will do this through a fetchWordByNumber(wordNumber) method, 
Line 867: where wordNumber identifies a word. The design decision here is that every word is stored with a 
Line 868: sequential number starting from 1 to help us pick one at random.
Line 869: We will be writing a WordSelection class, which is responsible for picking a random number 
Line 870: and using that to fetch a word from storage that is tagged with that number. We will be using our 
Line 871: RandomNumbers interface from earlier. For this example, our test will cover the case where we 
Line 872: attempt to fetch a word from the WordRepository interface, but for some reason, it isn’t there.
Line 873: 
Line 874: --- 페이지 169 ---
Line 875: Test Doubles – Stubs and Mocks
Line 876: 146
Line 877: We can write the test as follows:
Line 878: @ExtendWith(MockitoExtension.class)
Line 879: public class WordSelectionTest {
Line 880:     @Mock
Line 881:     private WordRepository repository;
Line 882:     @Mock
Line 883:     private RandomNumbers random;
Line 884:     @Test
Line 885:     public void reportsWordNotFound() {
Line 886:         doThrow(new WordRepositoryException())
Line 887:                 .when(repository)
Line 888:                   .fetchWordByNumber(anyInt());
Line 889:         var selection = new WordSelection(repository,
Line 890:                                           random);
Line 891:         assertThatExceptionOfType(WordSelectionException.class)
Line 892:                 .isThrownBy(
Line 893:                         ()->selection.getRandomWord());
Line 894:     }
Line 895: }
Line 896: The test captures a few more design decisions relating to how we intend WordRepository and 
Line 897: WordSelection to work. Our fetchWordByNumber(wordNumber) repository method will 
Line 898: throw WordRepositoryException if there are any problems retrieving the word. Our intention 
Line 899: is to make WordSelection throw its own custom exception to report that it cannot complete the 
Line 900: getRandomWord() request.
Line 901: To set this situation up in the test, we first arrange for the repository to throw. This is done using 
Line 902: the Mockito doThrow() feature. Whenever the fetchWordByNumber() method is called, 
Line 903: whatever parameter we pass into it Mockito will throw the exception we asked it to throw, which is 
Line 904: WordRepositoryException. This allows us to drive out the code that handles this error condition.
Line 905: 
Line 906: --- 페이지 170 ---
Line 907: Summary
Line 908: 147
Line 909: Our Arrange step is completed by creating the WordSelection SUT class. We pass in two collaborators 
Line 910: to the constructor: the WordRepository instance and a RandomNumbers instance. We have 
Line 911: asked Mockito to create stubs for both interfaces by adding the @Mock annotation to test double the 
Line 912: repository and random fields.
Line 913: With the SUT now properly constructed, we are ready to write the Act and Assert steps of the test. We 
Line 914: are testing that an exception is thrown, so we need to use the assertThatExceptionOfType() 
Line 915: AssertJ facility to do this. We can pass in the class of the exception that we are expecting to be thrown, 
Line 916: which is WordSelectionException. We chain the isThrownBy() method to perform the 
Line 917: Act step and make our SUT code run. This is provided as a Java lambda function as a parameter to 
Line 918: the isThrownBy() method. This will call the getRandomWord() method, which we intend to 
Line 919: fail and throw an exception. The assertion will confirm that this has happened and that the expected 
Line 920: kind of exception class has been thrown. We will run the test, see it fail, and then add the necessary 
Line 921: logic to make the test pass.
Line 922: The test code shows us that we can use test doubles and verification of error conditions with test-first 
Line 923: TDD. It also shows that tests can become easily coupled to a specific implementation of a solution. 
Line 924: There are a lot of design decisions in this test about which exceptions happen and where they are used. 
Line 925: These decisions even include the fact that exceptions are being used at all to report errors. All that 
Line 926: said, this is still a reasonable way to split responsibilities and define contracts between components. 
Line 927: It is all captured in the test.
Line 928: Summary
Line 929: In this chapter, we’ve looked at how to solve the problem of testing problematic collaborators. We 
Line 930: have learned how to use stand-in objects for collaborators called test doubles. We’ve learned that this 
Line 931: gives us simple control over what those collaborators do inside our test code.
Line 932: Two kinds of test double are especially useful to us: the stub and the mock. Stubs return data. Mocks 
Line 933: verify that methods were called. We’ve learned how to use the Mockito library to create stubs and 
Line 934: mocks for us.
Line 935: We’ve used AssertJ to verify the SUT behaved correctly under the various conditions of our test 
Line 936: doubles. We’ve learned how to test error conditions that throw exceptions.
Line 937: These techniques have expanded our toolkit for writing tests.
Line 938: In the next chapter, we are going to cover a very useful system design technique that allows us to get most 
Line 939: of our code under FIRST unit test, and at the same time avoid the problems of testing collaborations 
Line 940: with external systems that we cannot control.
Line 941: 
Line 942: --- 페이지 171 ---
Line 943: Test Doubles – Stubs and Mocks
Line 944: 148
Line 945: Questions and answers
Line 946: 1.	
Line 947: Are the terms stub and mock used interchangeably?
Line 948: Yes, even though they have different meanings. In normal conversation, we tend to trade 
Line 949: precision for fluency, and that’s okay. It’s important to understand the different uses that each 
Line 950: kind of test double has. When speaking, it’s usually better to not be pedantic whenever a group 
Line 951: of people knows what is meant. So long as we stay aware that a test double is the proper general 
Line 952: term and that the specific types of doubles have different roles, all will be well.
Line 953: 2.	
Line 954: What is the problem known as “testing the mock”?
Line 955: This happens when the SUT has no real logic in it, yet we try to write a unit test anyway. We 
Line 956: wire up a test double to the SUT and write the test. What we will find is that the assertions 
Line 957: only check that the test double-returned the right data. It’s an indication that we have tested 
Line 958: at the wrong level. This kind of error can be driven by setting unwise code coverage targets or 
Line 959: forcing an equally unwise test-per-method rule. This test adds no value and should be removed.
Line 960: 3.	
Line 961: Can test doubles be used anywhere?
Line 962: No. This only works if you have designed your code using the Dependency Inversion Principle 
Line 963: so that a test double can be swapped in place of a production object. Using TDD certainly forces 
Line 964: us to think about this kind of design issue early.
Line 965: Writing tests later is made more difficult if there is insufficient access to inject test doubles where 
Line 966: they are needed. Legacy code is particularly difficult in this respect, and I recommend reading 
Line 967: the book Working Effectively with Legacy Code by Michael Feathers for techniques to aid in 
Line 968: adding tests to code that lacks the necessary test access points. (See the Further reading list.)
Line 969: Further reading
Line 970: •	 https://site.mockito.org/
Line 971: Mockito library home page
Line 972: •	 Working Effectively with Legacy Code, Michael C. Feathers ISBN 978-0131177055
Line 973: This book explains how you can work with legacy code written without Dependency Inversion 
Line 974: access points for test doubles. It shows a range of techniques to safely rework the legacy code 
Line 975: so that test doubles can be introduced.
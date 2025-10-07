Line 1: 
Line 2: --- 페이지 169 ---
Line 3: 141
Line 4: Test doubles and mocks
Line 5: Until now, we have been testing classes and methods that were isolated from each
Line 6: other. We passed the inputs to a single method call and asserted its output. Or,
Line 7: when a class was involved, we set up the state of the class, called the method under
Line 8: test, and asserted that the class was in the expected state.
Line 9:  But some classes depend on other classes to do their job. Exercising (or testing)
Line 10: many classes together may be desirable. We often break down complex behavior into
Line 11: multiple classes to improve maintainability, each with a small part of the business
Line 12: logic. We still want to ensure, however, that the whole thing works together; we will
Line 13: discuss this in chapter 9. This chapter focuses on testing that unit in an isolated fash-
Line 14: ion without caring too much about its dependencies. But why would we want that?
Line 15:  The answer is simple: because exercising the class under test together with its
Line 16: concrete dependencies might be too slow, too hard, or too much work. As an exam-
Line 17: ple, consider an application that handles invoices. This system has a class called
Line 18: This chapter covers
Line 19: Using stubs, fakes, and mocks to simplify testing
Line 20: Understanding what to mock, when to mock, and 
Line 21: when not to mock
Line 22: How to mock the unmockable
Line 23: 
Line 24: --- 페이지 170 ---
Line 25: 142
Line 26: CHAPTER 6
Line 27: Test doubles and mocks
Line 28: IssuedInvoices, which handles the database and contains lots of SQL queries. Other
Line 29: parts of the system (such as the InvoiceGenerationService class, which generates
Line 30: new invoices) depend on this IssuedInvoices class to persist the generated invoice in
Line 31: the database. This means that whenever we test InvoiceGenerationService, this class
Line 32: will consequently call IssuedInvoices, which will then communicate with a database.
Line 33:  In other words, the InvoiceGenerationService class indirectly depends on the
Line 34: database that stores the issued invoices. This means testing the InvoiceGeneration-
Line 35: Service requires setting up a database, making sure it contains all the right data, and
Line 36: so on. That is clearly much more work than writing tests that do not require a data-
Line 37: base. Figure 6.1 shows a more generic illustration of this problem. How do we test a
Line 38: class that depends on many other classes, some of which may involve databases and
Line 39: other complicated things?
Line 40: But when systematically testing the InvoiceGenerationService class, maybe we do
Line 41: not want to test whether the SQL query in the IssuedInvoices class is correct. We
Line 42: only want to ensure that, for example, the invoice is generated correctly or contains
Line 43: all the right values. Testing whether the SQL query works will be the responsibility of
Line 44: the IssuedInvoicesTest test suite, not InvoiceGenerationServiceTest. We will
Line 45: write integration tests for SQL queries in chapter 9.
Line 46:  We must figure out how to test a class that depends on another class without using
Line 47: that dependency. This is where test doubles come in handy. We create an object to
Line 48: mimic the behavior of component B (“it looks like B, but it is not B”). Within the test,
Line 49: we have full control over what this fake component B does, so we can make it behave
Line 50: as B would in the context of this test and thus cut the dependency on the real object.
Line 51:  In the previous example, suppose A is a plain Java class that depends on Issued-
Line 52: Invoices to retrieve values from a database. We can implement a fake IssuedInvoices
Line 53: that returns a hard-coded list of values rather than retrieving them from an external
Line 54: database. This means we can control the environment around A so we can check how
Line 55: A behaves without dealing with complex dependencies. I show examples of how this
Line 56: works later in the chapter.
Line 57: etc.
Line 58: B
Line 59: DB
Line 60: A
Line 61: C
Line 62: How do we write tests for A without
Line 63: depending on B, C, and all their
Line 64: transitive dependencies?
Line 65: Figure 6.1
Line 66: A simple illustration of the 
Line 67: challenges we face when testing a class 
Line 68: that depends on many other classes
Line 69: 
Line 70: --- 페이지 171 ---
Line 71: 143
Line 72: Dummies, fakes, stubs, spies, and mocks
Line 73:  Using objects that simulate the behavior of other objects has the following
Line 74: advantages:
Line 75: We have more control. We can easily tell these fake objects what to do. If we want a
Line 76: method to throw an exception, we tell the mock method to throw it. There is
Line 77: no need for complicated setups to force the dependency to throw the excep-
Line 78: tion. Think of how hard it is to force a class to throw an exception or return a
Line 79: fake date. This effort is close to zero when we simulate the dependencies with
Line 80: mock objects.
Line 81: Simulations are faster. Imagine a dependency that communicates with a web ser-
Line 82: vice or a database. A method in one of these classes might take a few seconds to
Line 83: process. On the other hand, if we simulate the dependency, it will no longer
Line 84: need to communicate with a database or web service and wait for a response.
Line 85: The simulation will return what it was configured to return, and it will cost
Line 86: nothing in terms of time.
Line 87: When used as a design technique, mocks enable developers to reflect on how
Line 88: classes should interact with each other, what their contracts should be, and the con-
Line 89: ceptual boundaries. Therefore, mocks can be used to make testing easier and
Line 90: support developers in designing code.
Line 91: NOTE
Line 92: While some of the schools of thought in testing prefer to see mocks as
Line 93: a design technique, in this book, I talk about stubs and mocks mostly from a
Line 94: testing perspective, as our goal is to use mocks to ease our lives when looking
Line 95: for bugs. If you are interested in mocking as a design technique, I strongly
Line 96: recommend Freeman and Pryce’s 2009 book, which is the canonical refer-
Line 97: ence for the subject.
Line 98: I sorted mocks into the unit testing section of my testing flow (go back to figure 1.4 in
Line 99: chapter 1) because our goal is to focus on a single unit without caring much about the
Line 100: other units of the system. Note, however, that we still care about the contracts of the
Line 101: dependencies, as our simulations must follow and do the same things that the simu-
Line 102: lated class promises.
Line 103: 6.1
Line 104: Dummies, fakes, stubs, spies, and mocks
Line 105: Before we dive into how to simulate objects, let’s first discuss the different types of sim-
Line 106: ulations we can create. Meszaros, in his book (2007), defines five different types:
Line 107: dummy objects, fake objects, stubs, spies, and mocks. Each makes sense in a specific
Line 108: situation.
Line 109: 6.1.1
Line 110: Dummy objects
Line 111: Dummy objects are passed to the class under test but never used. This is common in
Line 112: business applications where you need to fill a long list of parameters, but the test exer-
Line 113: cises only a few of them. Think of a unit test for a Customer class. Maybe this class
Line 114: depends on several other classes like Address, Email, and so on. Maybe a specific test
Line 115: 
Line 116: --- 페이지 172 ---
Line 117: 144
Line 118: CHAPTER 6
Line 119: Test doubles and mocks
Line 120: case A wants to exercise a behavior, and this behavior does not care which Address
Line 121: this Customer has. In this case, a tester can set up a dummy Address object and pass it
Line 122: to the Customer class. 
Line 123: 6.1.2
Line 124: Fake objects
Line 125: Fake objects have real working implementations of the class they simulate. However, they
Line 126: usually do the same task in a much simpler way. Imagine a fake database class that uses an
Line 127: array list instead of a real database. This fake object is simpler to control than the real
Line 128: database. A common example in real life is to use a simpler database during testing.
Line 129:  In the Java world, developers like to use HSQLDB (HyperSQL database, http://
Line 130: hsqldb.org), an in-memory database that is much faster and easier to set up in the test
Line 131: code than a real database. We will talk more about in-memory databases when we dis-
Line 132: cuss integration testing in chapter 9. 
Line 133: 6.1.3
Line 134: Stubs
Line 135: Stubs provide hard-coded answers to the calls performed during the test. Unlike fake
Line 136: objects, stubs do not have a working implementation. If the code calls a stubbed
Line 137: method getAllInvoices, the stub will return a hard-coded list of invoices.
Line 138:  Stubs are the most popular type of simulation. In most cases, all you need from a
Line 139: dependency is for it to return a value so the method under test can continue its execu-
Line 140: tion. If we were testing a method that depends on this getAllInvoices method, we
Line 141: could stub it to return an empty list, then return a list with one element, then return a
Line 142: list with many elements, and so on. This would enable us to assert how the method
Line 143: under test would work for lists of various lengths being returned from the database. 
Line 144: 6.1.4
Line 145: Mocks
Line 146: Mock objects act like stubs in the sense that you can configure how they reply if a
Line 147: method is called: for example, to return a list of invoices when getAllInvoices is
Line 148: called. However, mocks go beyond that. They save all the interactions and allow you to
Line 149: make assertions afterward. For example, maybe we only want the getAllInvoices
Line 150: method to be called once. If the method is called twice by the class under test, this is a
Line 151: bug, and the test should fail. At the end of our test, we can write an assertion along the
Line 152: lines of “verify that getAllInvoices was called just once.”
Line 153:  Mocking frameworks let you assert all sorts of interactions, such as “the method
Line 154: was never called with this specific parameter” or “the method was called twice with
Line 155: parameter A and once with parameter B.” Mocks are also popular in industry since
Line 156: they can provide insight into how classes interact. 
Line 157: 6.1.5
Line 158: Spies
Line 159: As the name suggests, spies spy on a dependency. They wrap themselves around the
Line 160: real object and observe its behavior. Strictly speaking, we are not simulating the object
Line 161: but rather recording all the interactions with the underlying object we are spying on.
Line 162: 
Line 163: --- 페이지 173 ---
Line 164: 145
Line 165: An introduction to mocking frameworks
Line 166:  Spies are used in very specific contexts, such as when it is much easier to use the
Line 167: real implementation than a mock but you still want to assert how the method under
Line 168: test interacts with the dependency. Spies are less common in the wild. 
Line 169: 6.2
Line 170: An introduction to mocking frameworks
Line 171: Mocking frameworks are available for virtually all programming languages. While they
Line 172: may differ in their APIs, the underlying idea is the same. Here, I will use Mockito
Line 173: (https://site.mockito.org), one of the most popular stubbing and mocking libraries
Line 174: for Java. Mockito offers a simple API, enabling developers to set up stubs and define
Line 175: expectations in mock objects with just a few lines of code. (Mockito is an extensive
Line 176: framework, and we cover only part of it in this chapter. To learn more, take a look at
Line 177: its documentation.)
Line 178:  Mockito is so simple that knowing the following three methods is often enough:
Line 179: 
Line 180: mock(<class>)—Creates a mock object/stub of a given class. The class can be
Line 181: specified by <ClassName>.class.
Line 182: 
Line 183: when(<mock>.<method>).thenReturn(<value>)—A chain of method calls that
Line 184: defines the (stubbed) behavior of the method. In this case <value> is returned.
Line 185: For example, to make the all method of an issuedInvoices mock return a list
Line 186: of invoices, we write when(issuedInvoices.all()).thenReturn(someList-
Line 187: Here).
Line 188: 
Line 189: verify(<mock>).<method>—Asserts that the interactions with the mock object
Line 190: happened in the expected way. For example, if we want to ensure that the
Line 191: method all of an issuedInvoices mock was invoked, we use verify(issued-
Line 192: Invoices).all().
Line 193: Let’s dive into concrete examples to illustrate Mockito’s main features and show you
Line 194: how developers use mocking frameworks in practice. If you are already familiar with
Line 195: Mockito, you can skip this section.
Line 196: 6.2.1
Line 197: Stubbing dependencies
Line 198: Let’s learn how to use Mockito and set up stubs with a practical example. Suppose we
Line 199: have the following requirement:
Line 200: The program must return all the issued invoices with values smaller than 100.
Line 201: The collection of invoices can be found in our database. The class Issued-
Line 202: Invoices already contains a method that retrieves all the invoices.
Line 203: The code in listing 6.1 is a possible implementation of this requirement. Note that
Line 204: IssuedInvoices is a class responsible for retrieving all the invoices from a real data-
Line 205: base (for example, MySQL). For now, suppose it has a method all() (not shown) that
Line 206: returns all the invoices in the database. The class sends SQL queries to the database
Line 207: and returns invoices. You can check the (naive) implementation in the book’s code
Line 208: repository.
Line 209: 
Line 210: --- 페이지 174 ---
Line 211: 146
Line 212: CHAPTER 6
Line 213: Test doubles and mocks
Line 214: import java.util.List;
Line 215: import static java.util.stream.Collectors.toList;
Line 216: public class InvoiceFilter {
Line 217:   public List<Invoice> lowValueInvoices() {
Line 218:     DatabaseConnection dbConnection = new DatabaseConnection();        
Line 219:     IssuedInvoices issuedInvoices = new IssuedInvoices(dbConnection);  
Line 220:     try {
Line 221:       List<Invoice> all = issuedInvoices.all();   
Line 222:       return all.stream()
Line 223:               .filter(invoice -> invoice.getValue() < 100)
Line 224:               .collect(toList());       
Line 225:     } finally {
Line 226:       dbConnection.close();   
Line 227:     }
Line 228:   }
Line 229: }
Line 230: Without stubbing the IssuedInvoices class, testing the InvoiceFilter class means
Line 231: having to set up a database. It also means having invoices in the database so the SQL
Line 232: query can return them. This is a lot of work, as you can see from the (simplified) test
Line 233: method in listing 6.2, which exercises InvoiceFilter together with the concrete
Line 234: IssuedInvoices class and the database. Because the tests need a populated database
Line 235: up and running, we first create a connection to the database and clean up any old
Line 236: data it may contain. Then, in the test method, we persist a set of invoices to the data-
Line 237: base. Finally, when the test is over, we close the connection with the database, as we do
Line 238: not want hanging connections.
Line 239: public class InvoiceFilterTest {
Line 240:   private IssuedInvoices invoices;
Line 241:   private DatabaseConnection dbConnection;
Line 242:   @BeforeEach         
Line 243:   public void open() {
Line 244:     dbConnection = new DatabaseConnection();
Line 245:     invoices = new IssuedInvoices(dbConnection);
Line 246:     dbConnection.resetDatabase();    
Line 247:   }
Line 248:   @AfterEach             
Line 249:   public void close() {
Line 250:     if (dbConnection != null)
Line 251: Listing 6.1
Line 252: InvoiceFilter class
Line 253: Listing 6.2
Line 254: Tests for InvoiceFilter
Line 255: Instantiates the IssuedInvoices
Line 256: dependency. It needs a
Line 257: DatabaseConnection, so we
Line 258: also instantiate one of those.
Line 259: Gets all the invoices 
Line 260: from the database
Line 261: Picks all the invoices with 
Line 262: a value smaller than 100
Line 263: Closes the connection with the database. You would 
Line 264: probably handle it better, but this is here to remind 
Line 265: you of all the things you need to handle when dealing 
Line 266: with databases.
Line 267: BeforeEach methods are executed 
Line 268: before every test method.
Line 269: Cleans up the tables to make sure 
Line 270: old data in the database does not 
Line 271: interfere with the test
Line 272: AfterEach methods are 
Line 273: executed after every 
Line 274: test method.
Line 275: 
Line 276: --- 페이지 175 ---
Line 277: 147
Line 278: An introduction to mocking frameworks
Line 279:       dbConnection.close();   
Line 280:   }
Line 281:   @Test
Line 282:   void filterInvoices() {
Line 283:     Invoice mauricio = new Invoice("Mauricio", 20);  
Line 284:     Invoice steve = new Invoice("Steve", 99);  
Line 285:     Invoice frank = new Invoice("Frank", 100); 
Line 286:     invoices.save(mauricio);       
Line 287:     invoices.save(steve);          
Line 288:     invoices.save(frank);          
Line 289:     InvoiceFilter filter = new InvoiceFilter();   
Line 290:     assertThat(filter.lowValueInvoices())
Line 291:         .containsExactlyInAnyOrder(mauricio, steve);    
Line 292:   }
Line 293: }
Line 294: NOTE
Line 295: Did you notice the assertThat…containsExactlyInAnyOrder asser-
Line 296: tion? This ensures that the list contains exactly the objects we pass, in any
Line 297: order. Such assertions do not come with JUnit 5. Without AssertJ, we would
Line 298: have to write a lot of code for that assertion to happen. You should get famil-
Line 299: iar with AssertJ’s assertions; they are handy.
Line 300: This is a small example. Imagine a larger business class with a much more complex
Line 301: database structure. Imagine that instead of persisting a bunch of invoices, you need to
Line 302: persist invoices, customers, items, shopping carts, products, and so on. This can
Line 303: become tedious and expensive.
Line 304:  Let’s rewrite the test. This time we will stub the IssuedInvoices class and avoid the
Line 305: hassle with the database. First, we need a way to inject the InvoiceFilter stub into
Line 306: the class under test. Its current implementation creates an instance of Issued-
Line 307: Invoices internally (see the first lines in the lowValueInvoices method). This means
Line 308: there is no way for this class to use the stub during the test: whenever this method is
Line 309: invoked, it instantiates the concrete database-dependent class.
Line 310:  We must change our production code to make testing easier (get used to the idea
Line 311: of changing the production code to facilitate testing). The most direct way to do this
Line 312: is to have IssuedInvoices passed in as an explicit dependency through the class
Line 313: constructor, as shown in listing 6.3. The class no longer instantiates the Database-
Line 314: Connection and IssuedInvoices classes. Rather, it receives IssuedInvoices via con-
Line 315: structor. Note that there is no need for the DatabaseConnection class to be injected,
Line 316: as InvoiceFilter does not need it. This is good: the less we need to do in our test
Line 317: code, the better. The new implementation works for both our tests (because we can
Line 318: inject an IssueInvoices stub) and production (because we can inject the concrete
Line 319: IssueInvoices, which will go to the database, as we expect in production).
Line 320:  
Line 321:  
Line 322: Closes the database 
Line 323: connection after every test
Line 324: Creates in-memory 
Line 325: invoices as we have 
Line 326: been doing so far
Line 327: 99 and 100,
Line 328: boundary
Line 329: testing!
Line 330: However, we must persist 
Line 331: them in the database!
Line 332: Instantiates 
Line 333: InvoiceFilter, knowing 
Line 334: it will connect to the 
Line 335: database
Line 336: Asserts that the method 
Line 337: only returns the low-
Line 338: value invoices
Line 339: 
Line 340: --- 페이지 176 ---
Line 341: 148
Line 342: CHAPTER 6
Line 343: Test doubles and mocks
Line 344: public class InvoiceFilter {
Line 345:   private final IssuedInvoices issuedInvoices;   
Line 346:   public InvoiceFilter(IssuedInvoices issuedInvoices) {   
Line 347:     this.issuedInvoices = issuedInvoices;
Line 348:   }
Line 349:   public List<Invoice> lowValueInvoices() {
Line 350:     List<Invoice> all = issuedInvoices.all();   
Line 351:     return all.stream()
Line 352:         .filter(invoice -> invoice.getValue() < 100)
Line 353:         .collect(toList());
Line 354:   }
Line 355: }
Line 356: Let’s change our focus to the unit test of InvoiceFilter. The test is very similar to the
Line 357: one we wrote earlier, but now we do not handle the database. Instead, we configure
Line 358: the IssuedInvoices stub as shown in the next listing. Note how easy it is to write this
Line 359: test: full control over the stub enables us to try different cases (even exceptional ones)
Line 360: quickly.
Line 361: public class InvoiceFilterTest {
Line 362:   @Test
Line 363:   void filterInvoices() {
Line 364:     IssuedInvoices issuedInvoices = mock(IssuedInvoices.class);   
Line 365:     Invoice mauricio = new Invoice("Mauricio", 20);   
Line 366:     Invoice steve = new Invoice("Steve", 99);         
Line 367:     Invoice frank = new Invoice("Frank", 100);        
Line 368:     List<Invoice> listOfInvoices = Arrays.asList(mauricio, steve, frank);
Line 369:     when(issuedInvoices.all()).thenReturn(listOfInvoices);   
Line 370:     InvoiceFilter filter = new InvoiceFilter(issuedInvoices);   
Line 371:     assertThat(filter.lowValueInvoices())
Line 372:         .containsExactlyInAnyOrder(mauricio, steve);   
Line 373:   }
Line 374: }
Line 375: NOTE
Line 376: This idea of classes not instantiating their dependencies by themselves
Line 377: but instead receiving them is a popular design technique. It allows us to inject
Line 378: mocks and also makes the production code more flexible. This idea is also
Line 379: Listing 6.3
Line 380: InvoiceFilter class receiving IssueInvoices via constructor
Line 381: Listing 6.4
Line 382: Tests for InvoiceFilter, stubbing IssuedInvoices
Line 383: Creates a field in the 
Line 384: class to store the 
Line 385: dependency
Line 386: IssuedInvoices 
Line 387: is now passed in 
Line 388: the constructor.
Line 389: We no longer instantiate 
Line 390: the IssuedInvoices database 
Line 391: class. We received it as a 
Line 392: dependency, and we use it.
Line 393: Instantiates a stub for the
Line 394: IssuedInvoices class, using
Line 395: Mockito’s mock method
Line 396: Creates invoices as 
Line 397: we did before
Line 398: Makes the
Line 399: stub return the
Line 400: predefined list
Line 401: of invoices if
Line 402: all() is called
Line 403: Instantiates the class under test,
Line 404: and passes the stub as a dependency
Line 405: (instead of the concrete database class)
Line 406: Asserts that the behavior is as expected
Line 407: 
Line 408: --- 페이지 177 ---
Line 409: 149
Line 410: An introduction to mocking frameworks
Line 411: known as dependency injection. If you want to dive into the topic, I suggest
Line 412: Dependency Injection: Principles, Practices, and Patterns by Steven van Deursen
Line 413: and Mark Seemann (2019).
Line 414: Note how we set up the stub using Mockito’s when() method. In this example, we tell
Line 415: the stub to return a list containing mauricio, frank, and steve, the three invoices
Line 416: we instantiate as part of the test case. The test then invokes the method under test,
Line 417: filter.lowValueInvoices(). Consequently, the method under test invokes issued-
Line 418: Invoices.all(). However, at this point, issuedInvoices is a stub that returns the list
Line 419: with the three invoices. The method under test continues its execution and returns a
Line 420: new list with only the two invoices that are below 100, causing the assertion to pass.
Line 421:  Besides making the test easier to write, stubs also made the test class more cohesive
Line 422: and less prone to change if something other than InvoiceFilter changes. If Issued-
Line 423: Invoices changes—or, more specifically, if its contracts change—we may have to
Line 424: propagate it to the tests of InvoiceFilter, too. Our discussion of contracts in chap-
Line 425: ter 4 also makes sense when talking about mocks. Now InvoiceFilterTest only tests
Line 426: the InvoiceFilter class. It does not test the IssuedInvoices class. IssuedInvoices
Line 427: deserves to be tested, but in another place, using an integration test (which we’ll dis-
Line 428: cuss in chapter 9).
Line 429:  A cohesive test also has fewer chances of failing for another reason. In the old ver-
Line 430: sion, the filterInvoices test could fail because of a bug in the InvoiceFilter class
Line 431: or a bug in the IssuedInvoices class (imagine a bug in the SQL query that retrieves
Line 432: the invoices from the database). The new tests can only fail because of a bug in
Line 433: InvoiceFilter, never because of IssuedInvoices. This is handy, as a developer will
Line 434: spend less time debugging if this test fails. Our new approach for testing Invoice-
Line 435: Filter is faster, easier to write, and more cohesive.
Line 436: NOTE
Line 437: This part of the book does not focus on systematic testing. But that is
Line 438: what you should do, regardless of whether you are using mocks. Look at the
Line 439: filterInvoices test method. Its goal is to filter invoices that are below 100.
Line 440: In our (currently only) test case, we ensure that this works, and we even
Line 441: exercise the 100 boundary. You may want to exercise other cases, such as
Line 442: empty lists, or lists with a single element, or other test cases that emerge
Line 443: during specification-based and structural testing. I don’t do that in this
Line 444: chapter, but you should remember all the techniques discussed in the previ-
Line 445: ous chapters.
Line 446: In a real software system, the business rule implemented by InvoiceFilter would
Line 447: probably be best executed in the database. A simple SQL query would do the job
Line 448: with a much better performance. Try to abstract away from this simple example:
Line 449: whenever you have a dependency that is expensive to use during testing, stubs may
Line 450: come in handy. 
Line 451: 
Line 452: --- 페이지 178 ---
Line 453: 150
Line 454: CHAPTER 6
Line 455: Test doubles and mocks
Line 456: 6.2.2
Line 457: Mocks and expectations
Line 458: Next, let’s discuss mocks. Suppose our current system has a new requirement:
Line 459: All low-valued invoices should be sent to our SAP system (a software that man-
Line 460: ages business operations). SAP offers a sendInvoice web service that receives
Line 461: invoices.
Line 462: You know you probably want to test the new class without depending on a real full-
Line 463: blown SAP web service. So, the SAPInvoiceSender class (which contains the main
Line 464: logic of the feature) receives, via its constructor, a class that communicates with SAP.
Line 465: For simplicity, suppose there is a SAP interface. The SAPInvoiceSender’s main method,
Line 466: sendLowValuedInvoices, gets all the low-valued invoices using the InvoiceFilter
Line 467: class discussed in the previous section and then passes the resulting invoices to SAP.
Line 468: public interface SAP {   
Line 469:   void send(Invoice invoice);
Line 470: }
Line 471: public class SAPInvoiceSender {
Line 472:   private final InvoiceFilter filter;  
Line 473:   private final SAP sap;               
Line 474:   public SAPInvoiceSender(InvoiceFilter filter, SAP sap) {  
Line 475:     this.filter = filter;
Line 476:     this.sap = sap;
Line 477:   }
Line 478:   public void sendLowValuedInvoices() {  
Line 479:     List<Invoice> lowValuedInvoices = filter.lowValueInvoices();
Line 480:     for(Invoice invoice : lowValuedInvoices) {
Line 481:       sap.send(invoice);
Line 482:     }
Line 483:   }
Line 484: }
Line 485: Let’s test the SAPInvoiceSender class (see listing 6.6 for the implementation of the
Line 486: test suite). For this test, we stub the InvoiceFilter class. For SAPInvoiceSender,
Line 487: InvoiceFilter is a class that returns a list of invoices. It is not the goal of the current
Line 488: test to test InvoiceFilter, so we should stub this class to facilitate testing the method
Line 489: we do want to test. The stub returns a list of low-valued invoices.
Line 490:  The main purpose of this test is to ensure that every low-valued invoice is sent to
Line 491: SAP. How can we assert that this is happening without having the real SAP? It is sim-
Line 492: ple: we ensure that the call to SAP’s send() method happened. How do we do that?
Line 493:  Mockito, behind the scenes, records all the interactions with its mocks. This means
Line 494: if we mock the SAP interface and pass it to the class under test, at the end of the test,
Line 495: Listing 6.5
Line 496: SAPInvoiceSender class
Line 497: This interface encapsulates the communication 
Line 498: with SAP. Note that it does not matter how the 
Line 499: concrete implementation will work.
Line 500: We have fields for both the 
Line 501: required dependencies.
Line 502: The two
Line 503: dependencies
Line 504: are required
Line 505: by the
Line 506: constructor
Line 507: of the class.
Line 508: The logic of the method is straightforward. 
Line 509: We first get the low-value invoices from 
Line 510: the InvoiceFilter. Then we pass each of 
Line 511: them to SAP.
Line 512: 
Line 513: --- 페이지 179 ---
Line 514: 151
Line 515: An introduction to mocking frameworks
Line 516: all we need to do is ask the mock whether the method is called. For that, we use
Line 517: Mockito’s verify assertion (listing 6.6). Note the syntax: we repeat the method we
Line 518: expect to be called. We can even pass the specific parameters we expect. In the case of
Line 519: this test method, we expect the send method to be called for both the mauricio and
Line 520: frank invoices.
Line 521: public class SAPInvoiceSenderTest {
Line 522:   private InvoiceFilter filter = mock(InvoiceFilter.class);   
Line 523:   private SAP sap = mock(SAP.class);                          
Line 524:   private SAPInvoiceSender sender =
Line 525:     new SAPInvoiceSender(filter, sap);  
Line 526:   @Test
Line 527:   void sendToSap() {
Line 528:     Invoice mauricio = new Invoice("Mauricio", 20);
Line 529:     Invoice frank = new Invoice("Frank", 99);
Line 530:     List<Invoice> invoices = Arrays.asList(mauricio, frank);
Line 531:     when(filter.lowValueInvoices()).thenReturn(invoices);   
Line 532:     sender.sendLowValuedInvoices();   
Line 533:     verify(sap).send(mauricio);   
Line 534:     verify(sap).send(frank);      
Line 535:   }
Line 536: }
Line 537: Again, note how we define the expectations of the mock object. We know exactly how
Line 538: the InvoiceFilter class should interact with the mock. When the test is executed,
Line 539: Mockito checks whether these expectations were met and fails the test if they were not.
Line 540:  If you want to see Mockito in action, comment out the call to sap.send() in the
Line 541: sendLowValuedInvoices method to see the test fail. Mockito will say something like
Line 542: what you see in listing 6.7. Mockito expected the send method to be called to the
Line 543: “mauricio” invoice, but it was not. Mockito even complements the message and says
Line 544: that it did not see any interactions with this mock. This is an extra tip to help you
Line 545: debug the failing test.
Line 546: Wanted but not invoked:
Line 547: sap.send(        
Line 548:     Invoice{customer='Mauricio', value=20}
Line 549: );
Line 550: Actually, there were zero interactions with this mock.
Line 551: Listing 6.6
Line 552: Tests for the SAPInvoiceSender class
Line 553: Listing 6.7
Line 554: Mockito’s verify-failing message
Line 555: Instantiates all the mocks as fields. Nothing
Line 556: changes in terms of behavior. JUnit instantiates
Line 557: a new class before running each of the test
Line 558: methods. This is a matter of taste, but I usually
Line 559: like to have my mocks as fields, so I do not need
Line 560: to instantiate them in every test method.
Line 561: Passes the
Line 562: mock and the
Line 563: stub to the
Line 564: class under
Line 565: test
Line 566: Sets up the 
Line 567: InvoiceFilter stub. 
Line 568: It will return two 
Line 569: invoices whenever 
Line 570: lowValueInvoices() 
Line 571: is called.
Line 572: Calls the
Line 573: method
Line 574: under test,
Line 575: knowing
Line 576: that these
Line 577: two invoices
Line 578: will be sent
Line 579: to SAP
Line 580: Ensures that the send method 
Line 581: was called for both invoices
Line 582: send() was not invoked 
Line 583: for this invoice!
Line 584: 
Line 585: --- 페이지 180 ---
Line 586: 152
Line 587: CHAPTER 6
Line 588: Test doubles and mocks
Line 589: This example illustrates the main difference between stubbing and mocking. Stub-
Line 590: bing means returning hard-coded values for a given method call. Mocking means
Line 591: not only defining what methods do but also explicitly defining the interactions with
Line 592: the mock.
Line 593:  Mockito enables us to define even more specific expectations. For example, look
Line 594: at the following expectations.
Line 595: verify(sap, times(2)).send(any(Invoice.class));   
Line 596: verify(sap, times(1)).send(mauricio);    
Line 597: verify(sap, times(1)).send(frank);   
Line 598: These expectations are more restrictive than the earlier ones. We now expect the SAP
Line 599: mock to have its send method invoked precisely two times (for any given Invoice).
Line 600: We then expect the send method to be called once for the mauricio invoice and once
Line 601: for the frank invoice.
Line 602:  Let’s write one more test so you become more familiar with Mockito. Let’s exercise
Line 603: the case where there are no low-valued invoices. The code is basically the same as in
Line 604: the previous test, but we make our stub return an empty list when the lowValue-
Line 605: Invoices() method of InvoiceFilter is called. We then expect no interactions with
Line 606: the SAP mock. That can be accomplished through the Mockito.never() and
Line 607: Mockito.any() methods in combination with verify().
Line 608: @Test
Line 609: void noLowValueInvoices() {
Line 610:   List<Invoice> invoices = emptyList();
Line 611:   when(filter.lowValueInvoices()).thenReturn(invoices);   
Line 612:   sender.sendLowValuedInvoices();
Line 613:   verify(sap, never()).send(any(Invoice.class));   
Line 614: }
Line 615: You may wonder why I did not put this new SAP sending functionality in the existing
Line 616: InvoiceFilter class. The lowValueInvoices method would then be both a command
Line 617: and a query. Mixing both concepts in a single method is not a good idea, as it may
Line 618: confuse developers who call this method. An advantage of separating commands from
Line 619: queries is that, from a mocking perspective, you know what to do. You should stub the
Line 620: queries, as you now know that queries return values and do not change the object’s
Line 621: Listing 6.8
Line 622: More Mockito expectations
Line 623: Listing 6.9
Line 624: Test for when there are no low-value invoices
Line 625: Verifies that the send method was
Line 626: called precisely twice for any invoice
Line 627: Verifies that the send method 
Line 628: was called precisely once for 
Line 629: the “mauricio” invoice
Line 630: Verifies that the send method was called
Line 631: precisely once for the “frank” invoice
Line 632: This time, the 
Line 633: stub will return 
Line 634: an empty list.
Line 635: The important part of this 
Line 636: test is the assertion. We 
Line 637: ensure that the send() 
Line 638: method was not invoked 
Line 639: for any invoice.
Line 640: 
Line 641: --- 페이지 181 ---
Line 642: 153
Line 643: An introduction to mocking frameworks
Line 644: state; and you should mock commands, as you know they change the world outside
Line 645: the object under test.
Line 646: NOTE
Line 647: If you want to learn more, search for “command-query separation”
Line 648: (CQS) or read Fowler’s wiki entry on CQS (2005). As you get used to testing
Line 649: and writing tests, you will see that the better the code, the easier it is to test it.
Line 650: In chapter 7, we will discuss code decisions you can make in your production
Line 651: code to facilitate testing.
Line 652: To learn more about the differences between mocks and stubs, see the article “Mocks
Line 653: Aren’t Stubs,” by Martin Fowler (2007). 
Line 654: 6.2.3
Line 655: Capturing arguments
Line 656: Imagine a tiny change in the requirements of sending the invoice to the SAP feature:
Line 657: Instead of receiving the Invoice entity directly, SAP now requires the data to
Line 658: be sent in a different format. SAP requires the customer’s name, the value of
Line 659: the invoice, and a generated ID.
Line 660: The ID should have the following format: <date><customer code>.
Line 661: The date should always be in the “MMddyyyy” format: <month><day><year
Line 662: with 4 digits>.
Line 663: The customer code should be the first two characters of the customer’s
Line 664: first name. If the customer’s name has fewer than two characters, it should
Line 665: be “X”.
Line 666: Implementation-wise, we change the SAP interface to receive a new SapInvoice entity.
Line 667: This entity has three fields: customer, value, and id. We then modify the SAPInvoice-
Line 668: Sender so for each low-value invoice, it creates a new SapInvoice entity with the cor-
Line 669: rect id and sends it to SAP. The next listing contains the new implementation.
Line 670: public class SapInvoice {      
Line 671:   private final String customer;
Line 672:   private final int value;
Line 673:   private final String id;
Line 674:   public SapInvoice(String customer, int value, String id) {
Line 675:     // constructor
Line 676:   }
Line 677:   // getters
Line 678: }
Line 679: public interface SAP {   
Line 680:   void send(SapInvoice invoice);
Line 681: }
Line 682: Listing 6.10
Line 683: Changing the SAP-related classes to support the new required format
Line 684: A new entity to 
Line 685: represent the 
Line 686: new format
Line 687: SAP receives this 
Line 688: new SapInvoice 
Line 689: entity.
Line 690: 
Line 691: --- 페이지 182 ---
Line 692: 154
Line 693: CHAPTER 6
Line 694: Test doubles and mocks
Line 695: public class SAPInvoiceSender {
Line 696:   private final InvoiceFilter filter;
Line 697:   private final SAP sap;
Line 698:   public SAPInvoiceSender(InvoiceFilter filter, SAP sap) {   
Line 699:     this.filter = filter;
Line 700:     this.sap = sap;
Line 701:   }
Line 702:   public void sendLowValuedInvoices() {
Line 703:     List<Invoice> lowValuedInvoices = filter.lowValueInvoices();
Line 704:     for(Invoice invoice : lowValuedInvoices) {
Line 705:       String customer = invoice.getCustomer();
Line 706:       int value = invoice.getValue();
Line 707:       String sapId = generateId(invoice);
Line 708:       SapInvoice sapInvoice =
Line 709:         new SapInvoice(customer, value, sapId);   
Line 710:       sap.send(sapInvoice);   
Line 711:     }
Line 712:   }
Line 713:   private String generateId(Invoice invoice) {   
Line 714:     String date = LocalDate.now().format(
Line 715:       ➥ DateTimeFormatter.ofPattern("MMddyyyy"));
Line 716:     String customer = invoice.getCustomer();
Line 717:     return date +
Line 718:       (customer.length()>=2 ? customer.substring(0,2) : "X");   
Line 719:   }
Line 720: }
Line 721: When it comes to testing, we know that we should stub the InvoiceFilter class. We
Line 722: can also mock the SAP class and ensure that the send() method was called, as shown
Line 723: next.
Line 724: @Test
Line 725: void sendSapInvoiceToSap() {
Line 726:   Invoice mauricio = new Invoice("Mauricio", 20);
Line 727:   List<Invoice> invoices = Arrays.asList(mauricio);
Line 728:   when(filter.lowValueInvoices()).thenReturn(invoices);  
Line 729:   sender.sendLowValuedInvoices();
Line 730:   verify(sap).send(any(SapInvoice.class));   
Line 731: }
Line 732: Listing 6.11
Line 733: Test for the new implementation of SAPInvoiceSender
Line 734: The constructor 
Line 735: is the same as 
Line 736: before.
Line 737: Instantiates the 
Line 738: new SAPInvoice 
Line 739: object
Line 740: Sends the new 
Line 741: entity to SAP
Line 742: Generates the 
Line 743: required ID as in 
Line 744: the requirements
Line 745: Returns the 
Line 746: date plus the 
Line 747: customer’s 
Line 748: code
Line 749: Again, we stub 
Line 750: InvoiceFilter.
Line 751: Asserts that SAP received a SapInvoice. 
Line 752: But which SapInvoice? Any. That is not 
Line 753: good. We want to be more specific.
Line 754: 
Line 755: --- 페이지 183 ---
Line 756: 155
Line 757: An introduction to mocking frameworks
Line 758: This test ensures that the send method of the SAP is called. But how do we assert that
Line 759: the generated SapInvoice is the correct one? For example, how do we ensure that the
Line 760: generated ID is correct?
Line 761:  One idea could be to extract the logic of converting an Invoice to a SapInvoice,
Line 762: as shown in listing 6.12. The convert() method receives an invoice, generates the
Line 763: new id, and returns a SapInvoice. A simple class like this could be tested via unit tests
Line 764: without any stubs or mocks. We can instantiate different Invoices, call the convert
Line 765: method, and assert that the returned SapInvoice is correct. I leave that as an exercise
Line 766: for you.
Line 767: public class InvoiceToSapInvoiceConverter {
Line 768:   public SapInvoice convert(Invoice invoice) {   
Line 769:     String customer = invoice.getCustomer();
Line 770:     int value = invoice.getValue();
Line 771:     String sapId = generateId(invoice);
Line 772:     SapInvoice sapInvoice = new SapInvoice(customer, value, sapId);
Line 773:     return sapInvoice;
Line 774:   }
Line 775:   private String generateId(Invoice invoice) {   
Line 776:     String date = LocalDate.now()
Line 777:       .format(DateTimeFormatter.ofPattern("MMddyyyy"));
Line 778:     String customer = invoice.getCustomer();
Line 779:     return date +
Line 780:       (customer.length()>=2 ? customer.substring(0,2) : "X");
Line 781:   }
Line 782: }
Line 783: In chapter 10, we further discuss refactorings you can apply to your code to facilitate
Line 784: testing. I strongly recommend doing so. But for the sake of argument, let’s suppose
Line 785: this is not a possibility. How can we get the SapInvoice object generated in the cur-
Line 786: rent implementation of SAPInvoiceSender and assert it? This is our chance to use
Line 787: another of Mockito’s features: the argument captor.
Line 788:  Mockito allows us to get the specific objects passed to its mocks. We then ask the
Line 789: SAP mock to give us the SapInvoice passed to it during the execution of the method,
Line 790: to make assertions on it (see listing 6.13). Instead of using any(SAPInvoice.class),
Line 791: we pass an instance of an ArgumentCaptor. We then capture its value, which in this
Line 792: case is an instance of SapInvoice. We make traditional assertions on the contents of
Line 793: this object.
Line 794:  
Line 795:  
Line 796:  
Line 797: Listing 6.12
Line 798: Class that converts from Invoice to SapInvoice
Line 799: This method is straightforward. 
Line 800: It does not depend on any 
Line 801: complex classes, so we can 
Line 802: write unit tests for it as we 
Line 803: have done previously.
Line 804: The same generateId 
Line 805: method we saw 
Line 806: before
Line 807: 
Line 808: --- 페이지 184 ---
Line 809: 156
Line 810: CHAPTER 6
Line 811: Test doubles and mocks
Line 812: @ParameterizedTest
Line 813: @CsvSource({   
Line 814:     "Mauricio,Ma",
Line 815:     "M,X"}
Line 816: )
Line 817: void sendToSapWithTheGeneratedId(String customer, String customerCode) {
Line 818:   Invoice mauricio = new Invoice(customer, 20);
Line 819:   List<Invoice> invoices = Arrays.asList(mauricio);
Line 820:   when(filter.lowValueInvoices()).thenReturn(invoices);
Line 821:   sender.sendLowValuedInvoices();
Line 822:   ArgumentCaptor<SapInvoice> captor =
Line 823:     ArgumentCaptor.forClass(SapInvoice.class);   
Line 824:   verify(sap).send(captor.capture());    
Line 825:   SapInvoice generatedSapInvoice = captor.getValue();  
Line 826:   String date = LocalDate.now().format(DateTimeFormatter.
Line 827:     ofPattern("MMddyyyy"));
Line 828:   assertThat(generatedSapInvoice)
Line 829:     .isEqualTo(new SapInvoice(customer, 20, date + customerCode));   
Line 830: }
Line 831: Note that we have at least two different test cases to ensure that the generated ID is
Line 832: correct: one where the customer’s name is longer than two characters and another
Line 833: where it is shorter than two characters. Given that the structure of the test method
Line 834: would be the same for both methods, I decided to use a parameterized test. I also used
Line 835: the CsvSource to pass the different test cases to the test method. The CSV source
Line 836: enables us to pass the inputs via comma-separated values. I usually go for CSV sources
Line 837: whenever the inputs are simple and easily written, as in this case.
Line 838:  Interestingly, although my first option is always to try to refactor the code so I can
Line 839: write simple unit tests, I use argument captors often. In practice, it is common to have
Line 840: such classes, where most of what you do is coordinate the data flow between different
Line 841: components, and objects that need to be asserted may be created on the fly by the
Line 842: method but not returned to the caller.
Line 843: NOTE
Line 844: There is another test I find fundamental in the sendToSapWithThe-
Line 845: GeneratedId method: we are missing proper boundary testing. The length of
Line 846: the customer’s name (two) is a boundary, so I would test with a customer name
Line 847: that is precisely of length two. Again, we are discussing mocks, but when it
Line 848: comes to designing test cases, all the techniques we have discussed apply. 
Line 849: Listing 6.13
Line 850: Test using the ArgumentCaptor feature of Mockito
Line 851: Passes the two test cases. The test 
Line 852: method is executed twice: once for 
Line 853: “Mauricio” and once for “M”.
Line 854: Instantiates an ArgumentCaptor 
Line 855: with the type of the object we 
Line 856: are expecting to capture
Line 857: Calls the verify method 
Line 858: and passes the argument 
Line 859: captor as the parameter 
Line 860: of the method
Line 861: The argument
Line 862: was already
Line 863: captured.
Line 864: Now we
Line 865: extract it.
Line 866: Uses a traditional assertion, ensuring
Line 867: that the ID matches what is expected
Line 868: 
Line 869: --- 페이지 185 ---
Line 870: 157
Line 871: An introduction to mocking frameworks
Line 872: 6.2.4
Line 873: Simulating exceptions
Line 874: The developer realizes that SAP’s send method may throw a SapException if a prob-
Line 875: lem occurs. This leads to a new requirement:
Line 876: The system should return the list of invoices that failed to be sent to SAP. A
Line 877: failure should not make the program stop. Instead, the program should try to
Line 878: send all the invoices, even though some of them may fail.
Line 879: One easy way to implement this is to try to catch any possible exceptions. If an excep-
Line 880: tion happens, we store the failed invoice as shown in the following listing.
Line 881: public List<Invoice> sendLowValuedInvoices() {
Line 882:   List<Invoice> failedInvoices = new ArrayList<>();
Line 883:   List<Invoice> lowValuedInvoices = filter.lowValueInvoices();
Line 884:   for(Invoice invoice : lowValuedInvoices) {
Line 885:     String customer = invoice.getCustomer();
Line 886:     int value = invoice.getValue();
Line 887:     String sapId = generateId(invoice);
Line 888:     SapInvoice sapInvoice = new SapInvoice(customer, value, sapId);
Line 889:     try {       
Line 890:       sap.send(sapInvoice);
Line 891:     } catch(SAPException e) {
Line 892:       failedInvoices.add(invoice);
Line 893:     }
Line 894:   }
Line 895:   return failedInvoices;   
Line 896: }
Line 897: How do we test this? By now, you probably see that all we need to do is to force our sap
Line 898: mock to throw an exception for one of the invoices. We should use Mockito’s doThrow()
Line 899: .when() chain of calls. This is similar to the when() API you already know, but now we
Line 900: want it to throw an exception (see listing 6.15). Note that we configure the mock to
Line 901: throw an exception for the frank invoice. Then we assert that the list of failed invoices
Line 902: returned by the new sendLowValuedInvoices contains that invoice and that SAP
Line 903: was called for both the mauricio and the frank invoices. Also, because the SAP inter-
Line 904: face receives a SapInvoice and not an Invoice, we must instantiate three invoices
Line 905: (Maurício’s, Frank’s, and Steve’s) before asserting that the send method was called.
Line 906: @Test
Line 907: void returnFailedInvoices() {
Line 908:   Invoice mauricio = new Invoice("Mauricio", 20);
Line 909:   Invoice frank = new Invoice("Frank", 25);
Line 910:   Invoice steve = new Invoice("Steve", 48);
Line 911: Listing 6.14
Line 912: Catching a possible SAPException
Line 913: Listing 6.15
Line 914: Mocks that throw exceptions
Line 915: Catches the possible SAPException. 
Line 916: If that happens, we store the failed 
Line 917: invoice in a list.
Line 918: Returns the 
Line 919: list of failed 
Line 920: invoices
Line 921: 
Line 922: --- 페이지 186 ---
Line 923: 158
Line 924: CHAPTER 6
Line 925: Test doubles and mocks
Line 926:   List<Invoice> invoices = Arrays.asList(mauricio, frank, steve);
Line 927:   when(filter.lowValueInvoices()).thenReturn(invoices);
Line 928:   String date = LocalDate.now()
Line 929:     .format(DateTimeFormatter.ofPattern("MMddyyyy"));
Line 930:   SapInvoice franksInvoice = new SapInvoice("Frank", 25, date + "Fr");
Line 931:   doThrow(new SAPException())
Line 932:     .when(sap).send(franksInvoice);  
Line 933:   List<Invoice> failedInvoices = sender.sendLowValuedInvoices();   
Line 934:   assertThat(failedInvoices).containsExactly(frank);               
Line 935:   SapInvoice mauriciosInvoice =
Line 936:     new SapInvoice("Mauricio", 20, date + "Ma");
Line 937:   verify(sap).send(mauriciosInvoice);           
Line 938:   SapInvoice stevesInvoice =
Line 939:     new SapInvoice("Steve", 48, date + "St");
Line 940:   verify(sap).send(stevesInvoice);              
Line 941: }
Line 942: NOTE
Line 943: Creating SapInvoices is becoming a pain, given that we always need
Line 944: to get the current date, put it in the MMddyyyy format, and concatenate it
Line 945: with the first two letters of the customer’s name. You may want to extract all
Line 946: this logic to a helper method or a helper class. Helper methods are wide-
Line 947: spread in test code. Remember, test code is as important as production
Line 948: code. All the best practices you follow when implementing your production
Line 949: code should be applied to your test code, too. We will discuss test code qual-
Line 950: ity in chapter 10.
Line 951: Configuring mocks to throw exceptions enables us to test how our systems would
Line 952: behave in unexpected scenarios. This is perfect for many software systems that inter-
Line 953: act with external systems, which may not behave as expected. Think of a web service
Line 954: that is not available for a second: would your application behave correctly if this hap-
Line 955: pened? How would you test the program behavior without using mocks or stubs? How
Line 956: would you force the web service API to throw you an exception? Doing so would be
Line 957: harder than telling the mock to throw an exception.
Line 958:  The requirement says one more thing: “A failure should not make the program
Line 959: stop; rather, the program should try to send all the invoices, even though some of
Line 960: them may fail.” We also tested that in our test method. We ensured that steve’s
Line 961: invoice—the one after frank’s invoice, which throws the exception—is sent to SAP. 
Line 962: 6.3
Line 963: Mocks in the real world
Line 964: Now that you know how to write mocks and stubs and how you can write powerful tests
Line 965: with them, it is time to discuss best practices. As you can imagine, some developers are
Line 966: big fans of mocking. Others believe mocks should not be used. It is a fact that mocks
Line 967: make your tests less real.
Line 968: Configures the mock to throw an exception 
Line 969: when it receives Frank’s invoice. Note the call to 
Line 970: doThrow().when(): this is the first time we use it.
Line 971: Gets the returned list of failed
Line 972: invoices and ensures that it
Line 973: only has Frank’s invoice
Line 974: Asserts that we tried to 
Line 975: send both Maurício’s 
Line 976: and Steve’s invoices
Line 977: 
Line 978: --- 페이지 187 ---
Line 979: 159
Line 980: Mocks in the real world
Line 981:  When should we mock? When is it best not to mock? What other best practices
Line 982: should I follow? I tackle those questions next.
Line 983: 6.3.1
Line 984: The disadvantages of mocking
Line 985: I have been talking a lot about the advantages of mocks. However, as I hinted before, a
Line 986: common (and heated) discussion among practitioners is whether to use mocks. Let’s
Line 987: look at possible disadvantages.
Line 988:  Some developers strongly believe that using mocks may lead to test suites that test the
Line 989: mock, not the code. That can happen. When you use mocks, you are naturally making your
Line 990: test less realistic. In production, your code will use the concrete implementation of the
Line 991: class you mocked during the test. Something may go wrong in the way the classes com-
Line 992: municate in production, for example, and you may miss it because you mocked them.
Line 993:  Consider a class A that depends on class B. Suppose class B offers a method sum()
Line 994: that always returns positive numbers (that is, the post-condition of sum()). When test-
Line 995: ing class A, the developer decides to mock B. Everything seems to work. Months later, a
Line 996: developer changes the post-conditions of B’s sum(): now it also returns negative num-
Line 997: bers. In a common development workflow, a developer would apply these changes in
Line 998: B and update B’s tests to reflect the change. It is easy to forget to check whether A han-
Line 999: dles this new post-condition well. Even worse, A’s test suite will still pass! A mocks B,
Line 1000: and the mock does not know that B changed. In large-scale software, it can be easy to
Line 1001: lose control of your mocks in the sense that mocks may not represent the real contract
Line 1002: of the class.
Line 1003:  For mock objects to work well on a large scale, developers must design careful
Line 1004: (and hopefully stable) contracts. If contracts are well designed and stable, you do not
Line 1005: need to be afraid of mocks. And although we use the example of a contract break as a
Line 1006: disadvantage of mocks, it is part of the coder’s job to find the dependencies of the
Line 1007: contract change and check that the new contract is covered, mocks or not.
Line 1008:  Another disadvantage is that tests that use mocks are naturally more coupled with
Line 1009: the code they test than tests that do not use mocks. Think of all the tests we have writ-
Line 1010: ten without mocks. They call a method, and they assert the output. They do not know
Line 1011: anything about the actual implementation of the method. Now, think of all the tests
Line 1012: we wrote in this chapter. The test methods know some things about the production
Line 1013: code. The tests we wrote for SAPInvoiceSender know that the class uses Invoice-
Line 1014: Filter’s lowValueInvoices method and that SAP’s send method must be called for all
Line 1015: the invoices. This is a lot of information about the class under test.
Line 1016:  What is the problem with the test knowing so much? It may be harder to change. If
Line 1017: the developer changes how the SAPInvoiceSender class does its job and, say, stops
Line 1018: using the InvoiceFilter class or uses the same filter differently, the developer may
Line 1019: also have to change the tests. The mocks and their expectations may be completely
Line 1020: different.
Line 1021:  Therefore, although mocks simplify our tests, they increase the coupling between
Line 1022: the test and the production code, which may force us to change the test whenever we
Line 1023: 
Line 1024: --- 페이지 188 ---
Line 1025: 160
Line 1026: CHAPTER 6
Line 1027: Test doubles and mocks
Line 1028: change the production code. Spadini and colleagues, including me, observed this
Line 1029: through empirical studies in open source systems (2019). Can you avoid such coupling?
Line 1030: Not really, but at least now you are aware of it.
Line 1031:  Interestingly, developers consider this coupling a major drawback of mocks. But I
Line 1032: appreciate that my tests break when I change how a class interacts with other classes.
Line 1033: The broken tests make me reflect on the changes I am making. Of course, my tests do
Line 1034: not break as a result of every minor change I make in my production code. I also do
Line 1035: not use mocks in every situation. I believe that when mocks are properly used, the
Line 1036: coupling with the production code is not a big deal.
Line 1037: 6.3.2
Line 1038: What to mock and what not to mock
Line 1039: Mocks and stubs are useful tools for simplifying the process of writing unit tests.
Line 1040: However, mocking too much might also be a problem. A test that uses the real depen-
Line 1041: dencies is more real than a test that uses doubles and, consequently, is more prone
Line 1042: to find real bugs. Therefore, we do not want to mock a dependency that should not
Line 1043: be mocked. Imagine you are testing class A, which depends on class B. How do we
Line 1044: know whether we should mock or stub B or whether it is better to use the real, con-
Line 1045: crete implementation?
Line 1046:  Pragmatically, developers often mock or stub the following types of dependencies:
Line 1047: Dependencies that are too slow—If the dependency is too slow for any reason, it
Line 1048: might be a good idea to simulate it. We do not want slow test suites. Therefore,
Line 1049: I mock classes that deal with databases or web services. Note that I still do inte-
Line 1050: gration tests to ensure that these classes work properly, but I use mocks for all
Line 1051: the other classes that depend on these slow classes.
Line 1052: Dependencies that communicate with external infrastructure—If the dependency talks
Line 1053: to (external) infrastructure, it may be too slow or too complex to set up the
Line 1054: required infrastructure. So, I apply the same principle: whenever testing a class
Line 1055: that depends on a class that handles external infrastructure, I mock the depen-
Line 1056: dency (as we mocked the IssuedInvoices class when testing the Invoice-
Line 1057: Filter class). I then write integration tests for these classes.
Line 1058: Mocking as a design technique
Line 1059: Whenever I say that mocks increase coupling with production code, I am talking about
Line 1060: using mocks from a testing perspective: not using mocks as a way to design the code,
Line 1061: but in the sense of “This is the code we have: let’s test it.” In this case, mocks are
Line 1062: naturally coupled with the code under test, and changes in the code will impact
Line 1063: the mocks.
Line 1064: If you are using mocks as a design technique (as explained in Freeman and Pryce’s
Line 1065: 2009 book), you should look at it from a different angle. You want your mocks to be
Line 1066: coupled with the code under test because you care about how the code does its job.
Line 1067: If the code changes, you want your mocks to change. 
Line 1068: 
Line 1069: --- 페이지 189 ---
Line 1070: 161
Line 1071: Mocks in the real world
Line 1072: Cases that are hard to simulate—If we want to force the dependency to behave in a
Line 1073: hard-to-simulate way, mocks or stubs can help. A common example is when we
Line 1074: would like the dependency to throw an exception. Forcing an exception might
Line 1075: be tricky when using the real dependency but is easy to do with a stub.
Line 1076: On the other hand, developers tend not to mock or stub the following dependencies:
Line 1077: Entities—Entities are classes that represent business concepts. They consist pri-
Line 1078: marily of data and methods that manipulate this data. Think of the Invoice
Line 1079: class in this chapter or the ShoppingCart class from previous chapters. In busi-
Line 1080: ness systems, entities commonly depend on other entities. This means, when-
Line 1081: ever testing an entity, we need to instantiate other entities.
Line 1082: For example, to test a ShoppingCart, we may need to instantiate Products
Line 1083: and Items. One possibility would be to mock the Product class when the focus is
Line 1084: to test the ShoppingCart. However, this is not something I recommend. Entities
Line 1085: are classes that are simple to manipulate. Mocking them may require more
Line 1086: work. Therefore, I prefer to never mock them. If my test needs three entities, I
Line 1087: instantiate them.
Line 1088: I make exceptions for heavy entities. Some entities require dozens of other
Line 1089: entities. Think of a complex Invoice class that depends on 10 other entities: Cus-
Line 1090: tomer, Product, and so on. Mocking this complex Invoice class may be easier.
Line 1091: Native libraries and utility methods—It is also not common to mock or stub librar-
Line 1092: ies that come with our programming language and utility methods. For exam-
Line 1093: ple, why would we mock ArrayList or a call to String.format? Unless you have
Line 1094: a very good reason, avoid mocking them.
Line 1095: Things that are simple enough—Simple classes may not be worth mocking. If you
Line 1096: feel a class is too simple to be mocked, it probably is.
Line 1097: Interestingly, I always followed those rules, because they made sense to me. In 2018–
Line 1098: 2019, Spadini, myself, and colleagues performed a study to see how developers mock
Line 1099: in the wild. Our findings were surprisingly similar to this list.
Line 1100:  Let me illustrate with a code example. Consider a BookStore class with the follow-
Line 1101: ing requirement:
Line 1102: Given a list of books and their respective quantities, the program should
Line 1103: return the total price of the cart.
Line 1104: If the bookstore does not have all the requested copies of the book, it
Line 1105: includes all the copies it has in stock in the final cart and lets the user know
Line 1106: about the missing ones.
Line 1107: The implementation (listing 6.16) uses a BookRepository class to check whether the
Line 1108: book is available in the store. If not enough copies are available, it keeps track of the
Line 1109: unavailable ones in the Overview class. For the available books, the store notifies Buy-
Line 1110: BookProcess. In the end, it returns the Overview class containing the total amount to
Line 1111: be paid and the list of unavailable copies.
Line 1112: 
Line 1113: --- 페이지 190 ---
Line 1114: 162
Line 1115: CHAPTER 6
Line 1116: Test doubles and mocks
Line 1117: class BookStore {
Line 1118:   private BookRepository bookRepository;
Line 1119:   private BuyBookProcess process;
Line 1120:   public BookStore(BookRepository bookRepository, BuyBookProcess process)  
Line 1121:   {
Line 1122:     this.bookRepository = bookRepository;
Line 1123:     this.process = process;
Line 1124:   }
Line 1125:   private void retrieveBook(String ISBN, int amount, Overview overview) {
Line 1126:     Book book = bookRepository.findByISBN(ISBN);   
Line 1127:     if (book.getAmount() < amount) {   
Line 1128:       overview.addUnavailable(book, amount - book.getAmount());
Line 1129:       amount = book.getAmount();
Line 1130:     }
Line 1131:     overview.addToTotalPrice(amount * book.getPrice());   
Line 1132:     process.buyBook(book, amount);     
Line 1133:   }
Line 1134:   public Overview getPriceForCart(Map<String, Integer> order) {
Line 1135:     if(order==null)
Line 1136:       return null;
Line 1137:     Overview overview = new Overview();
Line 1138:     for (String ISBN : order.keySet()) {     
Line 1139:       retrieveBook(ISBN, order.get(ISBN), overview);
Line 1140:     }
Line 1141:     return overview;
Line 1142:   }
Line 1143: }
Line 1144: Let’s discuss the main dependencies of the BookStore class:
Line 1145: The BookRepository class is responsible for, among other things, searching for
Line 1146: books in the database. This means the concrete implementation of this class
Line 1147: sends SQL queries to a database, parses the result, and transforms it into Book
Line 1148: classes. Using the concrete BookRepository implementation in the test might
Line 1149: be too painful: we would need to set up the database, ensure that it had the
Line 1150: books we wanted persisted, clean the database afterward, and so on. This is a
Line 1151: good dependency to mock.
Line 1152: The BuyBookProcess class is responsible for the process of someone buying a
Line 1153: book. We do not know exactly what it does, but it sounds complex. BuyBook-
Line 1154: Process deserves its own test suite, and we do not want to mix that with the
Line 1155: BookStore tests. This is another good dependency to mock.
Line 1156: Listing 6.16
Line 1157: Implementation of BookStore
Line 1158: We know we must mock
Line 1159: and stub things, so we
Line 1160: inject the dependencies.
Line 1161: Searches
Line 1162: for the
Line 1163: book using
Line 1164: its ISBN
Line 1165: If the number 
Line 1166: of copies in 
Line 1167: stock is less 
Line 1168: than the 
Line 1169: number of 
Line 1170: copies the user 
Line 1171: wants, we keep 
Line 1172: track of the 
Line 1173: missing ones.
Line 1174: Adds the
Line 1175: available
Line 1176: copies to
Line 1177: the final
Line 1178: price
Line 1179: Notifies the
Line 1180: buy book
Line 1181: process
Line 1182: Processes each 
Line 1183: book in the order
Line 1184: 
Line 1185: --- 페이지 191 ---
Line 1186: 163
Line 1187: Mocks in the real world
Line 1188: The Book class represents a book. The implementation of BookStore gets the
Line 1189: books that are returned by BookRepository and uses that information to
Line 1190: know the book’s price and how many copies the bookstore has in stock. This
Line 1191: is a simple class, and there is no need to mock it since it is easy to instantiate a
Line 1192: concrete Book.
Line 1193: The Overview class is also a simple, plain old Java object that stores the total
Line 1194: price of the cart and the list of unavailable books. Again, there is no need to
Line 1195: mock it.
Line 1196: The Map<String, Integer> that the getPriceForCart receives as an input is a
Line 1197: Map object. Map and its concrete implementation HashMap are part of the Java
Line 1198: language. They are simple data structures that also do not need to be mocked.
Line 1199: Now that we have decided what should be mocked and what should not be mocked,
Line 1200: we write the tests. The following test exercises the behavior of the program with a
Line 1201: more complex order.
Line 1202: @Test
Line 1203: void moreComplexOrder() {
Line 1204:   BookRepository bookRepo = mock(BookRepository.class);   
Line 1205:   BuyBookProcess process = mock(BuyBookProcess.class);    
Line 1206:   Map<String, Integer> orderMap = new HashMap<>();  
Line 1207:   orderMap.put("PRODUCT-ENOUGH-QTY", 5);    
Line 1208:   orderMap.put("PRODUCT-PRECISE-QTY", 10);
Line 1209:   orderMap.put("PRODUCT-NOT-ENOUGH", 22);
Line 1210:   Book book1 = new Book("PRODUCT-ENOUGH-QTY", 20, 11); // 11 > 5
Line 1211:   when(bookRepo.findByISBN("PRODUCT-ENOUGH-QTY"))
Line 1212:     .thenReturn(book1);                
Line 1213:   Book book2 = new Book("PRODUCT-PRECISE-QTY", 25, 10); // 10 == 10
Line 1214:   when(bookRepo.findByISBN("PRODUCT-PRECISE-QTY"))
Line 1215:     .thenReturn(book2);                
Line 1216:   Book book3 = new Book("PRODUCT-NOT-ENOUGH", 37, 21); // 21 < 22
Line 1217:   when(bookRepo.findByISBN("PRODUCT-NOT-ENOUGH"))
Line 1218:     .thenReturn(book3);                
Line 1219:   BookStore bookStore = new BookStore(bookRepo, process);   
Line 1220:   Overview overview = bookStore.getPriceForCart(orderMap);
Line 1221:   int expectedPrice =        
Line 1222:       5*20 + // from the first product
Line 1223:           10*25 + // from the second product
Line 1224:           21*37; // from the third product
Line 1225:   assertThat(overview.getTotalPrice()).isEqualTo(expectedPrice);
Line 1226: Listing 6.17
Line 1227: Test for BookStore, only mocking what needs to be mocked
Line 1228: As agreed, 
Line 1229: BookRepository 
Line 1230: and BuyBookProcess 
Line 1231: should be mocked.
Line 1232: No need
Line 1233: to mock
Line 1234: HashMap
Line 1235: The order has three books: one 
Line 1236: where there is enough quantity, 
Line 1237: one where the available quantity 
Line 1238: is precisely what is requested in 
Line 1239: the order, and one where there is 
Line 1240: not enough quantity.
Line 1241: Stubs the
Line 1242: BookRepository
Line 1243: to return the
Line 1244: three books
Line 1245: Injects the 
Line 1246: mocks and 
Line 1247: stubs into 
Line 1248: BookStore
Line 1249: Ensures that 
Line 1250: the total price 
Line 1251: is correct
Line 1252: 
Line 1253: --- 페이지 192 ---
Line 1254: 164
Line 1255: CHAPTER 6
Line 1256: Test doubles and mocks
Line 1257:   verify(process).buyBook(book1, 5);    
Line 1258:   verify(process).buyBook(book2, 10);   
Line 1259:   verify(process).buyBook(book3, 21);   
Line 1260:   assertThat(overview.getUnavailable())
Line 1261:       .containsExactly(entry(book3, 1));  
Line 1262: }
Line 1263: Could we mock everything? Yes, we could—but doing so would not make sense. You
Line 1264: should only stub and mock what is needed. But whenever you mock, you reduce the
Line 1265: reality of the test. It is up to you to understand this trade-off. 
Line 1266: 6.3.3
Line 1267: Date and time wrappers
Line 1268: Software systems often use date and time information. For example, you might need
Line 1269: the current date to add a special discount to the customer’s shopping cart, or you
Line 1270: might need the current time to start a batch processing job. To fully exercise some
Line 1271: pieces of code, our tests need to provide different dates and times as input.
Line 1272:  Given that date and time operations are common, a best practice is to wrap them
Line 1273: into a dedicated class (often called Clock). Let’s show that using an example:
Line 1274: The program should give a 15% discount on the total amount of an order if
Line 1275: the current date is Christmas. There is no discount on other dates.
Line 1276: A possible implementation for this requirement is shown next.
Line 1277: public class ChristmasDiscount {
Line 1278:   public double applyDiscount(double amount) {
Line 1279:     LocalDate today = LocalDate.now();  
Line 1280:     double discountPercentage = 0;
Line 1281:     boolean isChristmas = today.getMonth() == Month.DECEMBER
Line 1282:       && today.getDayOfMonth() == 25;
Line 1283:     if(isChristmas)   
Line 1284:       discountPercentage = 0.15;
Line 1285:     return amount - (amount * discountPercentage);
Line 1286:   }
Line 1287: }
Line 1288: The implementation is straightforward; given the characteristics of the class, unit testing
Line 1289: seems to be a perfect fit. The question is, how can we write unit tests for it? To test both
Line 1290: cases (Christmas/not Christmas), we need to be able to control/stub the LocalDate
Line 1291: class, so it returns the dates we want. Right now, this is not easy to do, given that the
Line 1292: Listing 6.18
Line 1293: ChristmasDiscount implementation
Line 1294: Ensures that BuyBookProcess 
Line 1295: was called for three books 
Line 1296: with the right amounts
Line 1297: Ensures that the list of 
Line 1298: unavailable books contains 
Line 1299: the one missing book
Line 1300: Gets the current 
Line 1301: date. Note the 
Line 1302: static call.
Line 1303: If it is Christmas, we 
Line 1304: apply the discount.
Line 1305: 
Line 1306: --- 페이지 193 ---
Line 1307: 165
Line 1308: Mocks in the real world
Line 1309: method makes explicit, direct calls to LocalDate.now(). The problem is analogous when
Line 1310: InvoiceFilter instantiated the IssuedInvoices class directly: we could not stub it.
Line 1311:  We can then ask a more specific question: how can we stub Java’s Time API? In par-
Line 1312: ticular, how can we do so for the static method call to LocalDate.now()? Mockito
Line 1313: allows developers to mock static methods (http://mng.bz/g48n), so we could use this
Line 1314: Mockito feature.
Line 1315:  Another solution (which is still popular in code bases) is to encapsulate all the date
Line 1316: and time logic into a class. In other words, we create a class called Clock, and this class
Line 1317: handles these operations. The rest of our system only uses this class when it needs
Line 1318: dates and times. This new Clock class is passed as a dependency to all classes that need
Line 1319: it and can therefore be stubbed. The new version of ChristmasDiscount is in the fol-
Line 1320: lowing listing.
Line 1321: public class Clock {
Line 1322:   public LocalDate now() {   
Line 1323:     return LocalDate.now();
Line 1324:   }
Line 1325:   // any other date and time operation here...
Line 1326: }
Line 1327: public class ChristmasDiscount {
Line 1328:   private final Clock clock;               
Line 1329:   public ChristmasDiscount(Clock clock) {  
Line 1330:     this.clock = clock;
Line 1331:   }
Line 1332:   public double applyDiscount(double rawAmount) {
Line 1333:     LocalDate today = clock.now();   
Line 1334:     double discountPercentage = 0;
Line 1335:     boolean isChristmas = today.getMonth() == Month.DECEMBER
Line 1336:         && today.getDayOfMonth() == 25;
Line 1337:     if(isChristmas)
Line 1338:       discountPercentage = 0.15;
Line 1339:     return rawAmount - (rawAmount * discountPercentage);
Line 1340:   }
Line 1341: }
Line 1342: Testing it should be easy, given that we can stub the Clock class (see listing 6.20). We
Line 1343: have two tests: one for when it is Christmas (where we set the clock to December 25 of
Line 1344: any year) and another for when it is not Christmas (where we set the clock to any
Line 1345: other date).
Line 1346: Listing 6.19
Line 1347: The Clock abstraction
Line 1348: Encapsulates the static call. This 
Line 1349: seems too simple, but think of other, 
Line 1350: more complex operations you will 
Line 1351: encapsulate in this class.
Line 1352: Clock is a plain old dependency 
Line 1353: that we store in a field and 
Line 1354: receive via the constructor.
Line 1355: Calls the clock whenever we need, 
Line 1356: for example, the current date
Line 1357: 
Line 1358: --- 페이지 194 ---
Line 1359: 166
Line 1360: CHAPTER 6
Line 1361: Test doubles and mocks
Line 1362: public class ChristmasDiscountTest {
Line 1363:   private final Clock clock = mock(Clock.class);    
Line 1364:   private final ChristmasDiscount cd = new ChristmasDiscount(clock);
Line 1365:   @Test
Line 1366:   public void christmas() {
Line 1367:     LocalDate christmas = LocalDate.of(2015, Month.DECEMBER, 25);
Line 1368:     when(clock.now()).thenReturn(christmas);   
Line 1369:     double finalValue = cd.applyDiscount(100.0);
Line 1370:     assertThat(finalValue).isCloseTo(85.0, offset(0.001));
Line 1371:   }
Line 1372:   @Test
Line 1373:   public void notChristmas() {
Line 1374:     LocalDate notChristmas = LocalDate.of(2015, Month.DECEMBER, 26);
Line 1375:     when(clock.now()).thenReturn(notChristmas);     
Line 1376:     double finalValue = cd.applyDiscount(100.0);
Line 1377:     assertThat(finalValue).isCloseTo(100.0, offset(0.001));
Line 1378:   }
Line 1379: }
Line 1380: As I said, creating an abstraction on top of date and time operations is common. The
Line 1381: idea is that having a class that encapsulates these operations will facilitate the testing
Line 1382: of the other classes in the system, because they are no longer handling date and time
Line 1383: operations. And because these classes now receive this clock abstraction as a depen-
Line 1384: dency, it can be easily stubbed. Martin Fowler’s wiki even has an entry called Clock-
Line 1385: Wrapper, which explains the same thing.
Line 1386:  Is it a problem to use Mockito’s ability to mock static methods? As always, there are
Line 1387: no right and wrong answers. If your system does not have complex date and time
Line 1388: operations, stubbing them using Mockito’s mockStatic() API should be fine. Pragma-
Line 1389: tism always makes sense. 
Line 1390: 6.3.4
Line 1391: Mocking types you do not own
Line 1392: Mocking frameworks are powerful. They even allow you to mock classes you do not
Line 1393: own. For example, we could stub the LocalDate class if we wanted to. We can mock
Line 1394: any classes from any library our software system uses. The question is, do we want to?
Line 1395:  When mocking, it is a best practice to avoid mocking types you do not own. Imag-
Line 1396: ine that your software system uses a library. This library is costly, so you decide to mock
Line 1397: it 100% of the time. In the long run, you may face the following complications:
Line 1398: If this library ever changes (for example, a method stops doing what it was sup-
Line 1399: posed to do), you will not have a breaking test. The entire behavior of that
Line 1400: library was mocked. You will only notice it in production. Remember that you
Line 1401: want your tests to break whenever something goes wrong.
Line 1402: Listing 6.20
Line 1403: Testing the new ChristmasDiscount
Line 1404: Clock is a stub.
Line 1405: Stubs the now() 
Line 1406: method to return 
Line 1407: the Christmas date
Line 1408: Stubs the now() 
Line 1409: method. It now 
Line 1410: returns a date that 
Line 1411: is not Christmas.
Line 1412: 
Line 1413: --- 페이지 195 ---
Line 1414: 167
Line 1415: Mocks in the real world
Line 1416: It may be difficult to mock external libraries. Think about the library you use to
Line 1417: access a database such as Hibernate. Mocking all the API calls to Hibernate is
Line 1418: too complex. Your tests will quickly become difficult to maintain.
Line 1419: What is the solution? When you need to mock a type you do not own, you create an
Line 1420: abstraction on top of it that encapsulates all the interactions with that type of library.
Line 1421: In a way, the Clock class we discussed is an example. We do not own the Time API, so
Line 1422: we created an abstraction that encapsulates it. These abstractions will let you hide all
Line 1423: the complexity of that type, offering a much simpler API to the rest of your software
Line 1424: system (which is good for the production code). At the same time, we can easily stub
Line 1425: these abstractions.
Line 1426:  If the behavior of your class changes, you do not have any failing tests anyway, as
Line 1427: your classes depend on the abstraction, not on the real thing. This is not a problem if
Line 1428: you apply the right test levels. In all the classes of the system that depend on this
Line 1429: abstraction, you can mock or stub the dependency. At this point, a change in the type
Line 1430: you do not own will not be caught by the test suite. The abstraction depends on the
Line 1431: contracts of the type before it changed. However, the abstraction itself needs to be
Line 1432: tested using integration tests. These integration tests will break if the type changes.
Line 1433:  Suppose you encapsulate all the behavior of a specific XML parser in an Xml-
Line 1434: Writer class. The abstraction offers a single method: write(Invoice). All the classes
Line 1435: of the system that depend on XmlWriter have write mocked in their unit tests. The
Line 1436: XmlWriter class, which calls the XML parser, will not mock the library. Rather, it will
Line 1437: make calls to the real library and see how it reacts. It will make sure the XML is written
Line 1438: as expected. If the library changes, this one test will break. It will then be up to the
Line 1439: developer to understand what to do, given the new behavior of the type. See figure 6.2
Line 1440: for an illustration.
Line 1441: In practice, unit tests are fast and easy to write and do not depend on external librar-
Line 1442: ies. Integration tests ensure that the interaction with the library happens as expected,
Line 1443: and they capture any changes in the behavior.
Line 1444: Mocks XmlWriter
Line 1445: XmlWriter
Line 1446: (External)
Line 1447: library
Line 1448: A
Line 1449: B
Line 1450: C
Line 1451: ATest
Line 1452: (unit test)
Line 1453: BTest
Line 1454: (unit test)
Line 1455: CTest
Line 1456: (unit test)
Line 1457: XmlWriter
Line 1458: (mock)
Line 1459: XmlWriterTest
Line 1460: (integration test)
Line 1461: Figure 6.2
Line 1462: XmlWriter is 
Line 1463: mocked when the developer 
Line 1464: is testing classes that use it 
Line 1465: (A, B, and C, in the example). 
Line 1466: XmlWriter is then tested 
Line 1467: via integration tests, 
Line 1468: exercising the library.
Line 1469: 
Line 1470: --- 페이지 196 ---
Line 1471: 168
Line 1472: CHAPTER 6
Line 1473: Test doubles and mocks
Line 1474:  Creating abstractions on top of dependencies that you do not own, as a way to gain
Line 1475: more control, is a common technique among developers. (The idea of only mocking
Line 1476: types you own was suggested by Freeman et al. in the paper that introduced the con-
Line 1477: cept of mock objects [2004] and by Mockito.) Doing so increases the overall complex-
Line 1478: ity of the system and requires maintaining another abstraction. But does the ease in
Line 1479: testing the system that we get from adding the abstraction compensate for the cost of
Line 1480: the increased complexity? Often, the answer is yes: it does pay off. 
Line 1481: 6.3.5
Line 1482: What do others say about mocking?
Line 1483: As I said, some developers favor mocking, and others do not. Software Engineering at Goo-
Line 1484: gle, edited by Winters, Manshreck, and Wright (2020), has an entire chapter dedicated
Line 1485: to test doubles. Here’s what I understood from it, along with my own point of view:
Line 1486: Using test doubles requires the system to be designed for testability. Indeed, as we saw, if
Line 1487: you use mocks, you need to make sure the class under test can receive the mock.
Line 1488: Building test doubles faithful to the real implementation is challenging. Test doubles must
Line 1489: be as faithful as possible. If your mocks do not offer the same contracts and expec-
Line 1490: tations of the production class, your tests may all pass, but the software system
Line 1491: will fail in production. Whenever you are mocking, make sure your mocks faith-
Line 1492: fully represent the class you are mocking.
Line 1493: Prefer realism over isolation. When possible, opt for the real implementation instead of
Line 1494: fakes, stubs, or mocks. I fully agree with this. Although I did my best to convince
Line 1495: you about the usefulness of mocking (that was the point of this chapter), real-
Line 1496: ism always wins over isolation. I am pragmatic about it, though. If it is getting
Line 1497: too hard to test with the real dependency, I mock it.
Line 1498: The following are trade-offs to consider when deciding whether to use a test
Line 1499: double:
Line 1500: – The execution time of the real implementation—I also take the execution time of
Line 1501: the dependency into account when deciding to mock or not. I usually mock
Line 1502: slow dependencies.
Line 1503: – How much non-determinism we would get from using the real implementation—
Line 1504: While I did not discuss non-deterministic behavior, dependencies that pres-
Line 1505: ent such behavior may be good candidates for mocking.
Line 1506: When using the real implementation is not possible or too costly, prefer fakes over mocks. I
Line 1507: do not fully agree with this recommendation. In my opinion, you either use the
Line 1508: real implementation or mock it. A fake implementation may end up having the
Line 1509: same problems as a mock. How do you ensure that the fake implementation has
Line 1510: the same behavior as the real implementation? I rarely use fakes.
Line 1511: Excessive mocking can be dangerous, as tests become unclear (hard to comprehend), brittle
Line 1512: (may break too often), and less effective (reduced ability to detect faults). I agree. If you
Line 1513: are mocking too much or the class under test forces you to mock too much,
Line 1514: that may be a sign that the production class is poorly designed.
Line 1515: 
Line 1516: --- 페이지 197 ---
Line 1517: 169
Line 1518: Exercises
Line 1519: When mocking, prefer state testing rather than interaction testing. Google says you
Line 1520: should make sure you are asserting a change of state and/or the consequence
Line 1521: of the action under test, rather than the precise interaction that the action has
Line 1522: with the mocked object. Google’s point is similar to what we discussed about
Line 1523: mocks and coupling. Interaction testing tends to be too coupled with the imple-
Line 1524: mentation of the system under test.
Line 1525: While I agree with this point, properly written interaction tests are useful.
Line 1526: They tell you when the interaction changed. This is my rule of thumb: if what
Line 1527: matters in the class I am testing is the interaction between classes, I do interac-
Line 1528: tion testing (my assertions check that the interactions are as expected). When
Line 1529: what matters is the result of processing, I do state testing (my assertions check
Line 1530: the return value or whether the state of the class is as expected).
Line 1531: Avoid over-specified interaction tests. Focus on the relevant arguments and functions.
Line 1532: This is a good suggestion and best practice. Make sure you only mock and stub
Line 1533: what needs to be mocked and stubbed. Only verify the interactions that make
Line 1534: sense for that test. Do not verify every single interaction that happens.
Line 1535: Good interaction testing requires strict guidelines when designing the system under test.
Line 1536: Google engineers tend not to do this. Using mocks properly is challenging even for
Line 1537: senior developers. Focus on training and team education, and help your devel-
Line 1538: oper peers do better interaction testing. 
Line 1539: Exercises
Line 1540: 6.1
Line 1541: Mocks, stubs, and fakes. What are they, and how do they differ from each other?
Line 1542: 6.2
Line 1543: The following InvoiceFilter class is responsible for returning the invoices for
Line 1544: an amount smaller than 100.0. It uses the IssuedInvoices type, which is
Line 1545: responsible for communication with the database.
Line 1546: public class InvoiceFilter {
Line 1547:   private IssuedInvoices invoices;
Line 1548:   public InvoiceFilter(IssuedInvoices invoices) {
Line 1549:     this.invoices = invoices;
Line 1550:   }
Line 1551:   public List<Invoice> filter() {
Line 1552:     return invoices.all().stream()
Line 1553:         .filter(invoice -> invoice.getValue() < 100.0)
Line 1554:         .collect(toList());
Line 1555:   }
Line 1556: }
Line 1557: Which of the following statements about this class is false?
Line 1558: A Integration testing is the only way to achieve 100% branch coverage.
Line 1559: B Its implementation allows for dependency injection, which enables mocking.
Line 1560: 
Line 1561: --- 페이지 198 ---
Line 1562: 170
Line 1563: CHAPTER 6
Line 1564: Test doubles and mocks
Line 1565: C It is possible to write completely isolated unit tests by, for example, using
Line 1566: mocks.
Line 1567: D The IssuedInvoices type (a direct dependency of InvoiceFilter)
Line 1568: should be tested using integration tests.
Line 1569: 6.3
Line 1570: You are testing a system that triggers advanced events based on complex combi-
Line 1571: nations of external, boolean conditions relating to the weather (outside tem-
Line 1572: perature, amount of rain, wind, and so on). The system has been designed
Line 1573: cleanly and consists of a set of cooperating classes, each of which has a single
Line 1574: responsibility. You use specification-based testing for this logic and test it using
Line 1575: mocks.
Line 1576: Which of the following is a valid test strategy?
Line 1577: A You use mocks to support observing the external conditions.
Line 1578: B You create mock objects to represent each variant you need to test.
Line 1579: C You use mocks to control the external conditions and to observe the event
Line 1580: being triggered.
Line 1581: D You use mocks to control the triggered events.
Line 1582: 6.4
Line 1583: Class A depends on a static method in class B. If you want to test class A, which of
Line 1584: the following two actions should you apply to do so properly?
Line 1585: Approach 1: Mock class B to control the behavior of the methods in class B.
Line 1586: Approach 2: Refactor class A, so the outcome of the method of class B is now
Line 1587: used as a parameter.
Line 1588: A Only approach 1
Line 1589: B Neither
Line 1590: C Only approach 2
Line 1591: D Both
Line 1592: 6.5
Line 1593: According to the guidelines provided in the book, what types of classes should
Line 1594: you mock, and which should you not mock?
Line 1595: 6.6
Line 1596: Now that you know the advantages and disadvantages of test doubles, what are
Line 1597: your thoughts about them? Do you plan to use mocks and stubs, or do you pre-
Line 1598: fer to focus on integration tests?
Line 1599: Summary
Line 1600: Test doubles help us test classes that depend on slow, complex, or external com-
Line 1601: ponents that are hard to control and observe.
Line 1602: There are different types of test doubles. Stubs are doubles that return hard-
Line 1603: coded values whenever methods are called. Mocks are like stubs, but we can
Line 1604: define how we expect a mock to interact with other classes.
Line 1605: Mocking can help us in testing, but it also has disadvantages. The mock may dif-
Line 1606: fer from the real implementation, and that would cause our tests to pass while
Line 1607: the system would fail.
Line 1608: 
Line 1609: --- 페이지 199 ---
Line 1610: 171
Line 1611: Summary
Line 1612: Tests that use mocks are more coupled with the production code than tests
Line 1613: that do not use mocks. When not carefully planned, such coupling can be
Line 1614: problematic.
Line 1615: Production classes should allow for the mock to be injected. One common
Line 1616: approach is to require all dependencies via the constructor.
Line 1617: You do not have to (and should not) mock everything, even when you decide to
Line 1618: go for mocks. Only mock what is necessary.
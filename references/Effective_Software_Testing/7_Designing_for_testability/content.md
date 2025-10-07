Line 1: 
Line 2: --- 페이지 200 ---
Line 3: 172
Line 4: Designing for testability
Line 5: I usually say that every software system can be tested. However, some systems are more
Line 6: testable than others. Imagine that for a single test case, we need to set up three differ-
Line 7: ent web services, create five different files in different folders, and put the database
Line 8: in a specific state. After all that, we exercise the feature under test and, to assert the
Line 9: correct behavior, again need to see if the three web services were invoked, the five
Line 10: files were consumed correctly, and the database is now in a different state. All those
Line 11: steps are doable. But couldn’t this process be simpler?
Line 12:  Software systems are sometimes not ready for or designed to be tested. In this
Line 13: chapter, we discuss some of the main ideas behind systems that have high testability.
Line 14: Testability is how easy it is to write automated tests for the system, class, or method
Line 15: under test. In chapter 6, we saw that by allowing dependencies to be injected, we
Line 16: This chapter covers
Line 17: Designing testable code at the architectural, 
Line 18: design, and implementation levels
Line 19: Understanding the Hexagonal Architecture, 
Line 20: dependency injection, observability, and 
Line 21: controllability
Line 22: Avoiding testability pitfalls
Line 23: 
Line 24: --- 페이지 201 ---
Line 25: 173
Line 26: Separating infrastructure code from domain code
Line 27: could stub the dependency. This chapter is about other strategies you can use to make
Line 28: testing easier.
Line 29:  The topic of design for testability deserves an entire book. In this chapter, I cover
Line 30: several design principles that solve most of the problems I face. When presenting
Line 31: these principles, I will discuss the underlying ideas so you can apply them even if the
Line 32: code changes you must make differ from my examples.
Line 33:  Design for testability is fundamental if our goal is to achieve systematic testing—if
Line 34: your code is hard to test, you probably won’t test it. When do I design for testability?
Line 35: What is the right moment to think about testability? All the time. Much of it happens
Line 36: while I am implementing a feature.
Line 37:  You should design for testability from the very beginning, which is why I put it in the
Line 38: “testing to guide development” part of the flow back in chapter 1, figure 1.4. Sometimes
Line 39: I cannot see the untestable part during the implementation phase, and it haunts me
Line 40: during the test phase. When that happens, I go back to my code and refactor it.
Line 41:  Some developers argue that designing for testability is harder and costs too many
Line 42: extra lines of code. This may be true. Writing spaghetti code is easier than develop-
Line 43: ing cohesive classes that collaborate and are easily tested. One of the goals of this
Line 44: chapter is to convince you that the extra effort of designing for testability will pay
Line 45: off. Good, testable code costs more than bad code, but it is the only way to ensure
Line 46: quality.
Line 47: 7.1
Line 48: Separating infrastructure code from domain code
Line 49: I could spend pages discussing architectural patterns that enable testability. Instead,
Line 50: I will focus on what I consider the most important advice: separate infrastructure code
Line 51: from domain code.
Line 52:  The domain is where the core of the system lies: that is, where all the business rules,
Line 53: logic, entities, services, and similar elements reside. Entities like Invoice and services
Line 54: such as ChristmasDiscount are examples of domain classes. Infrastructure relates to all
Line 55: code that handles an external dependency: for example, pieces of code that handle
Line 56: database queries (in this case, the database is an external dependency) or web service
Line 57: calls or file reads and writes. In our previous examples, all of our data access objects
Line 58: (DAOs) are part of the infrastructure code.
Line 59:  In practice, when domain code and infrastructure code are mixed, the system
Line 60: becomes harder to test. You should separate them as much as possible so the infra-
Line 61: structure does not get in the way of testing. Let’s start with InvoiceFilter example,
Line 62: now containing the SQL logic instead of depending on a DAO.
Line 63: public class InvoiceFilter {
Line 64:   private List<Invoice> all() { 
Line 65:     try {
Line 66:       Connection connection =
Line 67: Listing 7.1
Line 68: InvoiceFilter that mixes domain and infrastructure
Line 69: This method gets all the invoices 
Line 70: directly from the database. Note that it 
Line 71: resides in the InvoiceFilter class, unlike 
Line 72: in previous examples.
Line 73: 
Line 74: --- 페이지 202 ---
Line 75: 174
Line 76: CHAPTER 7
Line 77: Designing for testability
Line 78:         DriverManager.getConnection("db", "root", ""); 
Line 79:       PreparedStatement ps =
Line 80:         connection.prepareStatement("select * from invoice"));
Line 81:       Result rs = ps.executeQuery();
Line 82:       List<Invoice> allInvoices = new ArrayList<>();
Line 83:       while (rs.next()) {
Line 84:         allInvoices.add(new Invoice(
Line 85:           rs.getString("name"), rs.getInt("value")));
Line 86:       }
Line 87:       ps.close();
Line 88:       connection.close();
Line 89:       return allInvoices;
Line 90:     } catch(Exception e) { 
Line 91:       // handle the exception
Line 92:     }
Line 93:   }
Line 94: }
Line 95: public List<Invoice> lowValueInvoices() { 
Line 96:   List<Invoice> issuedInvoices = all();
Line 97:   return issuedInvoices.all().stream()
Line 98:     .filter(invoice -> invoice.value < 100)
Line 99:     .collect(toList());
Line 100:  }
Line 101: }
Line 102: We can make the following observations about this class:
Line 103: Domain code and infrastructure code are mixed. This means we will not be able to
Line 104: avoid database access when testing the low-value invoices rule. How would you
Line 105: stub the private method while exercising the public method? Because we can-
Line 106: not easily stub the database part, we must consider it when writing the tests. As
Line 107: we have seen many times already, this is more complex.
Line 108: The more responsibilities, the more complexity, and the more chances for bugs. Classes
Line 109: that are less cohesive contain more code. More code means more opportunities
Line 110: for bugs. This example class may have bugs related to SQL and the business
Line 111: logic, for example. Empirical research shows that longer methods and classes
Line 112: are more prone to defects (see the 2006 paper by Shatnawi and Li).
Line 113: Infrastructure is not the only external influence our code may suffer from. User inter-
Line 114: faces are often mixed with domain code, which is usually a bad idea for testability. You
Line 115: should not need the user interface to exercise your system’s business rules.
Line 116:  Besides the hassle of handling infrastructure when writing tests, extra cognitive
Line 117: effort is often required to engineer the test cases. Speaking from experience, it is
Line 118: much easier to test a class that has a single responsibility and no infrastructure than it
Line 119: is to test a non-cohesive class that handles business rules and, for example, database
Line 120: JDBC code to execute a
Line 121: simple SELECT query. If
Line 122: you are not a Java
Line 123: developer, there is no
Line 124: need to know what
Line 125: PreparedStatement
Line 126: and Result are.
Line 127: Database APIs often 
Line 128: throw exceptions that 
Line 129: we need to handle.
Line 130: The same lowValueInvoices method 
Line 131: we’ve seen before, but now it calls 
Line 132: a method in the same class to get 
Line 133: the invoices from the database.
Line 134: 
Line 135: --- 페이지 203 ---
Line 136: 175
Line 137: Separating infrastructure code from domain code
Line 138: access. Simpler code also has fewer possibilities and corner cases to see and explore.
Line 139: On the other hand, the more complex the code is, or the more responsibilities it has,
Line 140: the more we must think about test cases and possible interactions between features
Line 141: that are implemented in one place. In the example, the interaction between the infra-
Line 142: structure code and the business rule is simple: the method returns invoices from the
Line 143: database. But classes that do more complex things and handle more complex infra-
Line 144: structure can quickly become a nightmare during testing and maintenance.
Line 145:  The architecture of the software system under development needs to enforce a
Line 146: clear separation of responsibilities. The simplest way to describe it is by explaining the
Line 147: Ports and Adapters (or Hexagonal Architecture) pattern. As Alistair Cockburn proposed
Line 148: (2005), the domain (business logic) depends on ports rather than directly on the infra-
Line 149: structure. These ports are interfaces that define what the infrastructure can do and
Line 150: enable the application to get information from or send information to something
Line 151: else. They are completely separated from the implementation of the infrastructure.
Line 152: On the other hand, the adapters are very close to the infrastructure. They are the
Line 153: implementations of the ports that talk to the database, web service, and so on. They
Line 154: know how the infrastructure works and how to communicate with it.
Line 155:  Figure 7.1 illustrates a hexagonal architecture. The inside of the hexagon represents
Line 156: the application and all its business logic. The code is related to the application’s business
Line 157: logic and functional requirements. It knows nothing about external systems or required
Line 158: infrastructure. However, the application will require information or interaction with the
Line 159: external world at some point. For that, the application does not interact directly with the
Line 160: external system: instead, it communicates with a port. The port should be agnostic of the
Line 161: technology and, from the application’s perspective, abstract away details of how commu-
Line 162: nication happens. Finally, the adapter is coupled to the external infrastructure. The
Line 163: Database
Line 164: adapter
Line 165: Feature 2
Line 166: Feature N
Line 167: Feature 1
Line 168: Some system
Line 169: adapter
Line 170: UI adapter
Line 171: Some other
Line 172: system adapter
Line 173: Port
Line 174: Port
Line 175: Port
Line 176: Port
Line 177: Figure 7.1
Line 178: An illustration of the Hexagonal Architecture (or Ports and Adapters) pattern
Line 179: 
Line 180: --- 페이지 204 ---
Line 181: 176
Line 182: CHAPTER 7
Line 183: Designing for testability
Line 184: adapter knows how to send or retrieve messages from the external infrastructure and
Line 185: sends them back to the application in the format defined by the port.
Line 186:  Let’s cook up a simple example that illustrates these concepts in practice. Suppose
Line 187: an online web shop has the following requirements:
Line 188: For all the shopping carts that were paid today, the system should
Line 189: Set the status of the shopping cart as ready for delivery, and persist its new
Line 190: state in the database.
Line 191: Notify the delivery center, and let them know they should send the goods
Line 192: to the customer.
Line 193: Notify the SAP system.
Line 194: Send an e-mail to the customer confirming that the payment was success-
Line 195: ful. The e-mail should contain an estimate of when delivery will happen.
Line 196: The information is available via the delivery center API.
Line 197: The first step is identifying what belongs to the application (the hexagon) and what
Line 198: does not. It is clear that any business rule related to ShoppingCart, such as changing
Line 199: its state, as well as the entire workflow the shopping cart goes through once it’s paid,
Line 200: belongs inside the hexagon. However, a service that provides e-mail capabilities, a ser-
Line 201: vice that communicates with the SAP, a service that communicates with the delivery
Line 202: center API (which is probably offered as a web service), and a service that can commu-
Line 203: nicate with the database are all handled by external systems. For those, we need to
Line 204: devise a clear interface for the application to communicate with (the ports) together
Line 205: with a concrete implementation that can handle communication with the external sys-
Line 206: tem (the adapters). Figure 7.2 illustrates the concrete application of the Ports and
Line 207: Adapters pattern to this example.
Line 208:  A natural implementation for the PaidShoppingCartsBatch class would be the
Line 209: code in listing 7.2. It does not contain a single detail regarding infrastructure. This
Line 210: entire class could easily be unit-tested if we stubbed its dependencies. Does it need a
Line 211: list of paid shopping carts, normally returned by cartsPaidToday()? We stub it. Does
Line 212: it notify the SAP via the cartReadyForDelivery() method? We mock SAP and later
Line 213: assert the interaction with this method.
Line 214:  When we put everything together in production, the method will communicate
Line 215: with databases and web services. But at unit testing time, we do not care about that.
Line 216: The same testing philosophy we discussed in chapter 6 applies here: when (unit) test-
Line 217: ing the PaidShoppingCartsBatch class, we should focus on PaidShoppingCartsBatch
Line 218: and not its dependencies. This is possible here because (1) we receive its dependen-
Line 219: cies via the constructor (which enables us to pass mocks and stubs to the class), and
Line 220: (2) this class is only about business and has no lines of infrastructure code.
Line 221:  
Line 222:  
Line 223:  
Line 224: 
Line 225: --- 페이지 205 ---
Line 226: 177
Line 227: Separating infrastructure code from domain code
Line 228: public class PaidShoppingCartsBatch {
Line 229:   private ShoppingCartRepository db;
Line 230:   private DeliveryCenter deliveryCenter;
Line 231:   private CustomerNotifier notifier;
Line 232:   private SAP sap;
Line 233:   public PaidShoppingCartsBatch(ShoppingCartRepository db,
Line 234:     ➥ DeliveryCenter deliveryCenter,
Line 235:                  CustomerNotifier notifier, SAP sap) { 
Line 236:     this.db = db;
Line 237:     this.deliveryCenter = deliveryCenter;
Line 238:     this.notifier = notifier;
Line 239:     this.sap = sap;
Line 240:   }
Line 241:   public void processAll() {
Line 242:     List<ShoppingCart> paidShoppingCarts = db.cartsPaidToday();
Line 243: Listing 7.2
Line 244: PaidShoppingCartsBatch implementation
Line 245: SMTPEmailSender
Line 246: EmailService
Line 247: DeliveryCenter
Line 248: CartRepository
Line 249: SAP
Line 250: SAPSoapWebService
Line 251: DeliveryCenter
Line 252: RestApi
Line 253: CartHibernateDao
Line 254: ShoppingCart
Line 255: DeliveryCenter
Line 256: web service
Line 257: SAP web
Line 258: service
Line 259: SMTP
Line 260: server
Line 261: MySQL
Line 262: database
Line 263: These are domain objects. They only know about
Line 264: business. They use the ports whenever they
Line 265: need something outside their boundaries.
Line 266: Ports abstract away the
Line 267: infrastructure details. They
Line 268: speak “business language.”
Line 269: Adapters implement the port
Line 270: interface and handle the
Line 271: external infrastructure.
Line 272: PaidShoppingCarts
Line 273: Batch
Line 274: Figure 7.2
Line 275: A concrete implementation of the Hexagonal Architecture (or Ports and Adapters) pattern for the 
Line 276: shopping carts example
Line 277: All dependencies are 
Line 278: injected, which means we 
Line 279: can pass stubs and mocks 
Line 280: during testing.
Line 281: 
Line 282: --- 페이지 206 ---
Line 283: 178
Line 284: CHAPTER 7
Line 285: Designing for testability
Line 286:     for (ShoppingCart cart : paidShoppingCarts) { 
Line 287:       LocalDate estimatedDayOfDelivery = deliveryCenter.deliver(cart); 
Line 288:       cart.markAsReadyForDelivery(estimatedDayOfDelivery); 
Line 289:       db.persist(cart);                                    
Line 290:       notifier.sendEstimatedDeliveryNotification(cart); 
Line 291:       sap.cartReadyForDelivery(cart);   
Line 292:     }
Line 293:   }
Line 294: }
Line 295: Look at the class’s four dependencies: ShoppingCartRepository, DeliveryCenter,
Line 296: CustomerNotifier, and SAP. These are interfaces and, in the Hexagonal Architec-
Line 297: ture, ports. They establish a protocol for communication between the application
Line 298: and the external world. These interfaces are completely agnostic of technology and
Line 299: infrastructure details. In other words, they abstract all the complexity of the infra-
Line 300: structure away from the domain code. As a result, the interfaces do not depend on
Line 301: anything strange, such as database or web service classes. They do depend on other
Line 302: domain classes, such as ShoppingCart, and that is fine. The following listing con-
Line 303: tains the interface declarations of all the ports.
Line 304: public interface DeliveryCenter { 
Line 305:   LocalDate deliver(ShoppingCart cart);
Line 306: }
Line 307: public interface CustomerNotifier { 
Line 308:   void sendEstimatedDeliveryNotification(ShoppingCart cart);
Line 309: }
Line 310: public interface SAP {
Line 311:   void cartReadyForDelivery(ShoppingCart cart);
Line 312: }
Line 313: public interface ShoppingCartRepository { 
Line 314:   List<ShoppingCart> cartsPaidToday();
Line 315:   void persist(ShoppingCart cart);
Line 316: }
Line 317: We are now only missing the implementation of the adapters. This code is out of the
Line 318: scope of this book, but in terms of implementation, these adapters are classes that
Line 319: implement the ports’ interfaces. The next listing provides some skeleton code to give
Line 320: you an idea what the adapters will look like.
Line 321: Listing 7.3
Line 322: Interface declarations of all the ports
Line 323: For each 
Line 324: paid cart …
Line 325: … notify
Line 326: the delivery
Line 327: system about
Line 328: the delivery
Line 329: … mark it 
Line 330: as ready for 
Line 331: delivery and 
Line 332: persist that to 
Line 333: the database
Line 334: … send a notification
Line 335: to the customer
Line 336: … and notify
Line 337: the SAP.
Line 338: The DeliveryCenter interface’s concrete 
Line 339: implementation will probably consume a very 
Line 340: complex web service, but the port abstracts 
Line 341: this away. Ports speak business language and 
Line 342: do not let infrastructure details leak.
Line 343: The same thing happens for CustomerNotifier 
Line 344: and all other interfaces/ports.
Line 345: This one does not even 
Line 346: have “database” in the 
Line 347: name. “Repository” is a 
Line 348: more business-like term.
Line 349: 
Line 350: --- 페이지 207 ---
Line 351: 179
Line 352: Separating infrastructure code from domain code
Line 353: public class DeliveryCenterRestApi implements DeliveryCenter {
Line 354:   @Override
Line 355:   public LocalDate deliver(ShoppingCart cart) {
Line 356:     // all the code required to communicate
Line 357:     // with the delivery API
Line 358:     // and returns a LocalDate
Line 359:   }
Line 360: }
Line 361: public class SMTPCustomerNotifier implements CustomerNotifier {
Line 362:   @Override
Line 363:   public void sendEstimatedDeliveryNotification(ShoppingCart cart) {
Line 364:     // all the required code to
Line 365:     // send an email via SMTP
Line 366:   }
Line 367: }
Line 368: public class SAPSoapWebService implements SAP {
Line 369:   @Override
Line 370:   public void cartReadyForDelivery(ShoppingCart cart) {
Line 371:     // all the code required to send the
Line 372:     // cart to SAP's SOAP web service
Line 373:   }
Line 374: }
Line 375: public class ShoppingCartHibernateDao
Line 376:  implements ShoppingCartRepository {
Line 377:   @Override
Line 378:   public List<ShoppingCart> cartsPaidToday() {
Line 379:     // a Hibernate query to get the list of all
Line 380:     // invoices that were paid today
Line 381:   }
Line 382:   @Override
Line 383:   public void persist(ShoppingCart cart) {
Line 384:     // a hibernate code to persist the cart
Line 385:     // in the database
Line 386:   }
Line 387: }
Line 388: Why does this pattern improve testability? If our domain classes depend only on
Line 389: ports, we can easily exercise all the behavior of the domain logic by stubbing and
Line 390: mocking the ports. In the PaidShoppingCartsBatch example, we can stub and mock
Line 391: the ShoppingCartRepository, DeliveryCenter, CustomerNotifier, and SAP ports
Line 392: and focus on testing the main behavior of the PaidShoppingCartsBatch class.
Line 393: Again, we do not care if the DeliveryCenter adapter does its job properly. That one
Line 394: will be exercised in its own test suite.
Line 395:  Listing 7.5 shows an example test of PaidShoppingCartsBatch. This is a single
Line 396: test. As a developer, you should apply all the testing techniques and devise several
Line 397: Listing 7.4
Line 398: Simplified implementation of the adapters
Line 399: 
Line 400: --- 페이지 208 ---
Line 401: 180
Line 402: CHAPTER 7
Line 403: Designing for testability
Line 404: test cases for any behavior and corner cases you see. Even exceptional behaviors can
Line 405: be easily exercised.
Line 406: import static org.mockito.Mockito.*;
Line 407: @ExtendWith(MockitoExtension.class) 
Line 408: public class PaidShoppingCartsBatchTest {
Line 409:   @Mock ShoppingCartRepository db;
Line 410:   @Mock private DeliveryCenter deliveryCenter;
Line 411:   @Mock private CustomerNotifier notifier;
Line 412:   @Mock private SAP sap;
Line 413:   @Test
Line 414:   void theWholeProcessHappens() {
Line 415:     PaidShoppingCartsBatch batch = new PaidShoppingCartsBatch(db,
Line 416:       ➥ deliveryCenter, notifier, sap);         
Line 417:     ShoppingCart someCart = spy(new ShoppingCart());   
Line 418:     LocalDate someDate = LocalDate.now();
Line 419:     when(db.cartsPaidToday()).thenReturn(Arrays.asList(someCart));
Line 420:     when(deliveryCenter.deliver(someCart)).thenReturn(someDate);
Line 421:     batch.processAll();
Line 422:     verify(deliveryCenter).deliver(someCart); 
Line 423:     verify(notifier).sendEstimatedDeliveryNotification(someCart);
Line 424:     verify(db).persist(someCart);
Line 425:     verify(sap).cartReadyForDelivery(someCart);
Line 426:     verify(someCart).markAsReadyForDelivery(someDate);
Line 427:   }
Line 428: }
Line 429: Although we only tested the application code, the code from the adapters should also
Line 430: be tested. The real implementation of the ShoppingCartRepository—let’s call it
Line 431: ShoppingCartHibernateDao (because it uses the Hibernate framework)—will contain
Line 432: SQL queries that are complex and prone to bugs, so it deserves a dedicated test suite.
Line 433: The real SAPSoapWebService class will have complex code to call the SOAP-like web
Line 434: service and should also be exercised. Those classes require integration testing, follow-
Line 435: ing our discussion of the testing pyramid in chapter 1. Later in this book, I show how
Line 436: to write some of those integration tests.
Line 437: NOTE
Line 438: Although I could also have mocked the ShoppingCart class, I followed
Line 439: the advice I gave in chapter 6: do not mock entities unless they are complex. I
Line 440: preferred to spy on them rather than mock them.
Line 441: Listing 7.5
Line 442: Test for PaidShoppingCartsBatchTest, mocking the ports
Line 443: The @ExtendWith and @Mock 
Line 444: annotations are extensions provided 
Line 445: by Mockito. We do not even need to 
Line 446: write Mockito.mock(…). The framework 
Line 447: instantiates a mock for us in these fields.
Line 448: Instantiates the class 
Line 449: under test and passes the 
Line 450: mocks as dependencies
Line 451: The ShoppingCart is a simple entity, so we do not 
Line 452: need to mock it. Nevertheless, let’s spy on it to 
Line 453: assert its interactions later.
Line 454: Verifies that interactions 
Line 455: with the dependencies 
Line 456: happened as expected
Line 457: 
Line 458: --- 페이지 209 ---
Line 459: 181
Line 460: Dependency injection and controllability
Line 461: This idea of separating infrastructure from domain code appears not only in Cock-
Line 462: burn’s Hexagonal Architecture but also in many other interesting works on software
Line 463: design, such as the well-known Domain-Driven Design by Evans (2004) and Martin’s
Line 464: Clean Architecture (2018). This principle is pervasive among those who talk about soft-
Line 465: ware design and testability. I agree with all these authors.
Line 466:  A common question for those new to the Hexagonal Architecture (or domain-
Line 467: driven design, or clean architecture) is, “Do I need to create interfaces for every
Line 468: port?” I hope to convince you that there are no rights and wrongs, that everything
Line 469: depends, and that being pragmatic is key. Of course you do not have to create inter-
Line 470: faces for everything in your software system. I create interfaces for ports where I see
Line 471: more than one implementation. Even if I do not create an interface to represent an
Line 472: abstract behavior, I make sure the concrete implementation does not leak any of its
Line 473: implementation details. Context and pragmatism are kings.
Line 474:  To sum up, the main “design for testability” principle I follow at the architectural
Line 475: level is to separate infrastructure from business code. Do not be tempted to think,
Line 476: for instance, “This is a simple call to the database. Look how easy it is to implement
Line 477: here!” It is always easier to write untestable code, but doing so will bite you in the
Line 478: future. 
Line 479: 7.2
Line 480: Dependency injection and controllability
Line 481: At the architectural level, we saw that an important concern is to ensure that application
Line 482: (or domain) code is fully separated from the infrastructure code. At the class level, the
Line 483: most important recommendation I can give you is to ensure that classes are fully control-
Line 484: lable (that is, you can easily control what the class under test does) and observable (you
Line 485: can see what is going on with the class under test and inspect its outcome).
Line 486:  For controllability, the most common implementation strategy I apply is the one
Line 487: we used in chapter 6: if a class depends on another class, make it so the dependency can
Line 488: easily be replaced by a mock, fake, or stub. Look back at the PaidShoppingCartsBatch
Line 489: class (listing 7.2). It depends on four other classes. The PaidShoppingCartsBatch class
Line 490: receives all its dependencies via constructor, so we can easily inject mocks. The version
Line 491: of PaidShoppingCartsBatch in listing 7.6 does not receive its dependencies but
Line 492: instead instantiates them directly. How can we test this class without depending on
Line 493: databases, web services, and so on? It is almost the same implementation but much
Line 494: harder to test. It is that easy to write untestable code.
Line 495: public class VeryBadPaidShoppingCartsBatch {
Line 496:   public void processAll() {
Line 497:     ShoppingCartHibernateDao db = new ShoppingCartHibernateDao(); 
Line 498:     List<ShoppingCart> paidShoppingCarts = db.cartsPaidToday();
Line 499:     for (ShoppingCart cart : paidShoppingCarts) {
Line 500: Listing 7.6
Line 501: A badly implemented PaidShoppingCartsBatch
Line 502: Instantiates the database
Line 503: adapter. Bad for testability!
Line 504: 
Line 505: --- 페이지 210 ---
Line 506: 182
Line 507: CHAPTER 7
Line 508: Designing for testability
Line 509:       DeliveryCenterRestApi deliveryCenter =
Line 510:         new DeliveryCenterRestApi();   
Line 511:       LocalDate estimatedDayOfDelivery = deliveryCenter.deliver(cart);
Line 512:       cart.markAsReadyForDelivery(estimatedDayOfDelivery); 
Line 513:       db.persist(cart);                                    
Line 514:       SMTPCustomerNotifier notifier = new SMTPCustomerNotifier(); 
Line 515:       notifier.sendEstimatedDeliveryNotification(cart);
Line 516:       SAPSoapWebService sap = new SAPSoapWebService();   
Line 517:       sap.cartReadyForDelivery(cart);
Line 518:     }
Line 519:   }
Line 520: }
Line 521: Traditional code tends to be responsible for instantiating its dependencies. But this
Line 522: hinders our ability to control the internals of the class and use mocks to write unit
Line 523: tests. For our classes to be testable, we must allow their dependencies (especially the
Line 524: ones we plan to stub during testing) to be injected.
Line 525:  In the implementation, this can be as simple as receiving the dependencies via
Line 526: constructor or, in more complex cases, via setters. Making sure dependencies can be
Line 527: injected (the term dependency injection is commonly used to refer to this idea; I also
Line 528: describe it in chapter 6) improves our code in many ways:
Line 529: It enables us to mock or stub the dependencies during testing, increasing our
Line 530: productivity during the testing phase.
Line 531: It makes all the dependencies more explicit. They all need to be injected (via
Line 532: constructor, for example).
Line 533: It offers better separation of concerns: classes do not need to worry about how
Line 534: to build their dependencies, as the dependencies are injected into them.
Line 535: The class becomes more extensible. This point is not related to testing, but as a
Line 536: client of the class, you can pass any dependency via the constructor.
Line 537: NOTE
Line 538: A Java developer may recognize several frameworks and libraries con-
Line 539: nected to dependency injection, such as the well-known Spring framework
Line 540: and Google Guice. If your classes allow dependencies to be injected, Spring
Line 541: and Guice will automatically help you instantiate those classes and their tree
Line 542: of dependencies. While such frameworks are not needed at testing time (we
Line 543: usually pass the mocked dependencies manually to the classes under test),
Line 544: this approach is particularly useful to instantiate classes and their dependen-
Line 545: cies at production time. I suggest learning more about such frameworks!
Line 546: By devising interfaces that represent the abstract interactions that domains and infra-
Line 547: structure classes will have with each other (the ports), we better separate the con-
Line 548: cerns, reduce the coupling between layers, and devise simpler flows of interactions
Line 549: between layers. In our example, the PaidShoppingCartsBatch domain class does not
Line 550: depend on the adapters directly. Rather, it depends on an interface that defines what
Line 551: Notifies the
Line 552: delivery system
Line 553: about the delivery.
Line 554: But first, we need
Line 555: to instantiate its
Line 556: adapter. Bad for
Line 557: testability!
Line 558: Marks as ready 
Line 559: for delivery and 
Line 560: persist
Line 561: Sends a notification
Line 562: using the adapter
Line 563: directly. Bad for
Line 564: testability!
Line 565: Notifies SAP
Line 566: using the
Line 567: adapter
Line 568: directly. Bad
Line 569: for testability!
Line 570: 
Line 571: --- 페이지 211 ---
Line 572: 183
Line 573: Dependency injection and controllability
Line 574: the adapters should do abstractly. The SAP port interface knows nothing about how
Line 575: the real SAP works. It provides a cartReadyForDelivery method to the domain
Line 576: classes. This completely decouples the domain code from details of how the external
Line 577: infrastructure works.
Line 578:  The dependency inversion principle (note the word inversion, not injection) helps us
Line 579: formalize these concepts:
Line 580: High-level modules (such as our business classes) should not depend on low-
Line 581: level modules. Both should depend on abstractions (such as interfaces).
Line 582: Abstractions should not depend on details. Details (concrete implementations)
Line 583: should depend on abstractions.
Line 584: Figure 7.3 illustrates the principle. The domain objects, which are considered high-
Line 585: level classes, do not depend on low-level details such as a database or web service com-
Line 586: munication. Instead, they depend on abstractions of those low-level details. In the fig-
Line 587: ure, the abstractions are represented by the interfaces.
Line 588: Note the pattern: our code should always depend as much as possible on abstractions
Line 589: and as little as possible on details. The advantage of always depending on abstractions
Line 590: and not on low-level details is that abstractions are less fragile and less prone to
Line 591: change than low-level details. You probably do not want to change your code when-
Line 592: ever a low-level detail changes.
Line 593:  Again, coming up with interfaces for everything is too much work. I prefer to make
Line 594: sure all of my classes offer a clear interface to their consumers—one that does not
Line 595: leak internal details. For those more familiar with object-oriented programming con-
Line 596: cepts, I am talking about proper encapsulation.
Line 597:  How does depending on an abstraction help with testing? When you unit-test a
Line 598: class, you probably mock and stub its dependencies. When you mock, you naturally
Line 599: High-level class
Line 600: (e.g., domain object)
Line 601: High-level class
Line 602: Interface
Line 603: Interface
Line 604: Low-level class
Line 605: (e.g., database
Line 606: adapter)
Line 607: Low-level class
Line 608: Low-level class
Line 609: High-level modules
Line 610: Low-level modules
Line 611: High-level modules and low-level
Line 612: modules do not know each other;
Line 613: they all depend on interfaces.
Line 614: Figure 7.3
Line 615: An illustration of the dependency inversion principle
Line 616: 
Line 617: --- 페이지 212 ---
Line 618: 184
Line 619: CHAPTER 7
Line 620: Designing for testability
Line 621: depend on what the mocked class offers as a contract. The more complex the class
Line 622: you are mocking, the harder it is to write the test. When you have ports, adapters, and
Line 623: the dependency inversion principle in mind, the interface of a port is naturally sim-
Line 624: ple. The methods that ports offer are usually cohesive and straight to the point.
Line 625:  In the example, the ShoppingCartRepository class has a List<ShoppingCart>
Line 626: cartsPaidToday() method. It is clear what this method does: it returns a list of shop-
Line 627: ping carts that were paid today. Mocking this method is trivial. Its concrete adapter
Line 628: implementation is probably complicated, full of database-related code and SQL que-
Line 629: ries. The interface removes all this complexity from testing the PaidShoppingCarts-
Line 630: Batch class. Therefore, designing the ports in a simple way also makes your code
Line 631: easier to test. Complex ports and interfaces require more work.
Line 632:  When things become more complicated, making sure dependencies are always
Line 633: injected may not be as straightforward as I have made it seem. It is much easier not to do
Line 634: this. But you must convince yourself that the extra effort will pay off later during testing.
Line 635: NOTE
Line 636: This chapter is a quick introduction to the Hexagonal Architecture
Line 637: and to the Dependency Inversion Priniciple. I suggest you dive into the
Line 638: related literature, including the books by Martin (2014) and Freeman and
Line 639: Pryce (2009), for more details. I also recommend Schuchert’s guest post on
Line 640: dependency inversion in the wild in Fowler’s wiki (2013); he explains the dif-
Line 641: ference between dependency inversion and dependency injection and gives
Line 642: lots of examples of how he applied the principle in real-world situations. 
Line 643: 7.3
Line 644: Making your classes and methods observable
Line 645: Observability, at the class level, is about how easy it is to assert that the behavior of the
Line 646: functionality went as expected. My main advice is to ensure that your classes provide
Line 647: developers with simple and easy ways to assert their state. Does a class produce a list of
Line 648: objects you need to assert one by one? Create a getListOfSomething in that class,
Line 649: which the test can use to get the generated list of objects. Does a class make calls to
Line 650: other classes? Make sure these dependencies can be mocked and your test can assert
Line 651: their interaction. Does a class make internal changes in its attributes, but the class can-
Line 652: not or does not offer getters to each of them? Make the class offer a simple isValid
Line 653: method that returns whether the class is in a valid state.
Line 654:  It has to be easy for the test code to inspect the class behavior. Whenever it is difficult
Line 655: to observe whether the program behaves as expected, reflect on how observable the
Line 656: classes are. Do not be afraid to introduce simple getters or simple solutions to facilitate
Line 657: your testing. Behavior that is easy to observe will make the test code much easier! Let’s
Line 658: look at two pragmatic changes I make in my code so it is more observable.
Line 659: 7.3.1
Line 660: Example 1: Introducing methods to facilitate assertions
Line 661: Take another look at the processAll() method and its test, in listings 7.2 and 7.5. Most
Line 662: of what its test asserts is the interaction with the ports. Such assertions are easily done,
Line 663: and we did not need much more than basic Mockito. Now, let’s look closer at one specific
Line 664: assertion: verify(someCart).markAsReadyForDelivery(someDate);. The someCart
Line 665: 
Line 666: --- 페이지 213 ---
Line 667: 185
Line 668: Making your classes and methods observable
Line 669: instance of ShoppingCart is not a mock but a spy. To ensure that the cart was marked as
Line 670: ready for delivery, we had to spy on the object. Mockito’s API enables us to spy objects
Line 671: with a single line of code. However, whenever we need a spy to assert the behavior, we
Line 672: must ask ourselves why we need a spy. Isn’t there an easier way?
Line 673:  In this particular case, we need to check whether ShoppingCart is marked as ready
Line 674: for delivery after processing (listing 7.7). We can increase the observability of the
Line 675: ShoppingCart class (in other words, we can make it simpler to observe the expected
Line 676: behavior of the shopping cart) by making it provide a method that indicates whether
Line 677: it is ready for delivery: isReadyForDelivery.
Line 678: public class ShoppingCart {
Line 679:     private boolean readyForDelivery = false;
Line 680:     // more info about the shopping cart...
Line 681:     public void markAsReadyForDelivery(Calendar estimatedDayOfDelivery) {
Line 682:         this.readyForDelivery = true;
Line 683:         // ...
Line 684:     }
Line 685:     public boolean isReadyForDelivery() { 
Line 686:         return readyForDelivery;
Line 687:     }
Line 688: }
Line 689: Because we can now easily ask ShoppingCart whether it is ready for delivery, our test
Line 690: no longer requires a spy. A vanilla assertion should do. Here is the new test.
Line 691: @Test
Line 692: void theWholeProcessHappens() {
Line 693:   PaidShoppingCartsBatch batch = new PaidShoppingCartsBatch(db,
Line 694:     ➥ deliveryCenter, notifier, sap);
Line 695:   ShoppingCart someCart = new ShoppingCart(); 
Line 696:   assertThat(someCart.isReadyForDelivery()).isFalse();
Line 697:   Calendar someDate = Calendar.getInstance();
Line 698:   when(db.cartsPaidToday()).thenReturn(Arrays.asList(someCart));
Line 699:   when(deliveryCenter.deliver(someCart)).thenReturn(someDate);
Line 700:   batch.processAll();
Line 701:   verify(deliveryCenter).deliver(someCart);
Line 702:   verify(notifier).sendEstimatedDeliveryNotification(someCart);
Line 703:   verify(db).persist(someCart);
Line 704:   verify(sap).cartReadyForDelivery(someCart);
Line 705:   assertThat(someCart.isReadyForDelivery()).isTrue(); 
Line 706: }
Line 707: Listing 7.7
Line 708: Improving the observability of the ShoppingCart class
Line 709: Listing 7.8
Line 710: Avoiding the spy when testing PaidShoppingCartsBatch
Line 711: The new isReadyForDelivery 
Line 712: method is here to improve 
Line 713: the observability of the class.
Line 714: No need for a spy 
Line 715: anymore, as it is now easy 
Line 716: to observe the behavior.
Line 717: Uses a simple vanilla 
Line 718: assertion instead of a 
Line 719: Mockito assertion
Line 720: 
Line 721: --- 페이지 214 ---
Line 722: 186
Line 723: CHAPTER 7
Line 724: Designing for testability
Line 725: I urge you not to take this particular code change (the addition of a getter) as the
Line 726: solution for all observability issues. Rather, abstract away what we did here: we noticed
Line 727: that asserting that the shopping cart was marked as ready for delivery was not straight-
Line 728: forward, as it required a spy. We then re-evaluated our code and looked for a simple
Line 729: way to let the test know that the shopping cart was marked as ready for delivery. In this
Line 730: case, a getter was the easy implementation. 
Line 731: 7.3.2
Line 732: Example 2: Observing the behavior of void methods
Line 733: When a method returns an object, it is natural to think that assertions will check
Line 734: whether the returned object is as expected. However, this does not happen naturally
Line 735: in void methods. If your method does not return anything, what will you assert? It is
Line 736: even more complicated if what you need to assert stays within the method. As an
Line 737: example, the following method creates a set of Installments based on a Shopping-
Line 738: Cart.
Line 739: public class InstallmentGenerator {
Line 740:   private InstallmentRepository repository;
Line 741:   public InstallmentGenerator(InstallmentRepository repository) { 
Line 742:     this.repository = repository;
Line 743:   }
Line 744:   public void generateInstallments(ShoppingCart cart,
Line 745:     ➥ int numberOfInstallments) {
Line 746:     LocalDate nextInstallmentDueDate = LocalDate.now(); 
Line 747:     double amountPerInstallment = cart.getValue() / numberOfInstallments; 
Line 748:     for(int i = 1; i <= numberOfInstallments; i++) { 
Line 749:       nextInstallmentDueDate =
Line 750:         nextInstallmentDueDate.plusMonths(1);   
Line 751:       Installment newInstallment =
Line 752:         new Installment(nextInstallmentDueDate, amountPerInstallment);
Line 753:       repository.persist(newInstallment); 
Line 754:     }
Line 755:   }
Line 756: }
Line 757: To test this method, we need to check whether the newly created Installments are set
Line 758: with the right value and date. The question is, how can we get the Installments eas-
Line 759: ily? The Installment classes are instantiated within the method and sent to the repos-
Line 760: itory for persistence, and that is it. If you know Mockito well, you know there is a way
Line 761: to get all the instances passed to a mock: an ArgumentCaptor. The overall idea is that
Line 762: we ask the mock, “Can you give me all the instances passed to you during the test?” We
Line 763: Listing 7.9
Line 764: InstallmentGenerator 
Line 765: We can inject a stub of
Line 766: InstallmentRepository.
Line 767: Creates a variable to store the
Line 768: last installment date
Line 769: Calculates the
Line 770: amount per
Line 771: installment
Line 772: Creates a sequence 
Line 773: of installments, one 
Line 774: month apart
Line 775: Adds 1 to
Line 776: the month
Line 777: Creates and persists 
Line 778: the installment
Line 779: 
Line 780: --- 페이지 215 ---
Line 781: 187
Line 782: Making your classes and methods observable
Line 783: then make assertions about them. In this case, we can ask the repository mock
Line 784: whether all the Installments were passed to the persist method.
Line 785:  The test in listing 7.10 creates a shopping cart with value 100 and asks the genera-
Line 786: tor for 10 installments. Therefore, it should create 10 installments of 10.0 each. That is
Line 787: what we want to assert. After the method under test is executed, we collect all the install-
Line 788: ments using an ArgumentCaptor. See the calls for capture() and getAllValues(). With
Line 789: the list available, we use traditional AssertJ assertions.
Line 790: public class InstallmentGeneratorTest {
Line 791:     @Mock private InstallmentRepository repository; 
Line 792:     @Test
Line 793:     void checkInstallments() {
Line 794:       InstallmentGenerator generator =
Line 795:         new InstallmentGenerator(repository); 
Line 796:       ShoppingCart cart = new ShoppingCart(100.0);
Line 797:       generator.generateInstallments(cart, 10); 
Line 798:       ArgumentCaptor<Installment> captor =
Line 799:         ArgumentCaptor.forClass(Installment.class); 
Line 800:       verify(repository,times(10)).persist(captor.capture());     
Line 801:       List<Installment> allInstallments = captor.getAllValues();  
Line 802:       assertThat(allInstallments)
Line 803:           .hasSize(10)
Line 804:           .allMatch(i -> i.getValue() == 10); 
Line 805:       for(int month = 1; month <= 10; month++) { 
Line 806:         final LocalDate dueDate = LocalDate.now().plusMonths(month);
Line 807:         assertThat(allInstallments)
Line 808:             .anyMatch(i -> i.getDate().equals(dueDate));
Line 809:       }
Line 810:     }
Line 811: }
Line 812: The ArgumentCaptor makes writing the test possible. ArgumentCaptors are handy
Line 813: whenever we test methods that return void.
Line 814:  If we apply the idea of simplicity, you may wonder if there is a way to avoid the
Line 815: ArgumentCaptor. It would be much simpler if there were a “get all generated install-
Line 816: ments” method. If we make the generateInstallments method return the list of all
Line 817: newly generated Installments, the test becomes even simpler. The change required
Line 818: in InstallmentGenerator is small: as all we need to do is keep track of the install-
Line 819: ments in a list. The following listing shows the new implementation.
Line 820: Listing 7.10
Line 821: Tests for InstallmentGenerator using ArgumentCaptor
Line 822: Creates a mock of 
Line 823: the repository
Line 824: Instantiates the class
Line 825: under test, passing the
Line 826: mock as a dependency
Line 827: Calls the method 
Line 828: under test. Note that 
Line 829: the method returns 
Line 830: void, so we need 
Line 831: something smarter to 
Line 832: assert its behavior.
Line 833: Creates an
Line 834: ArgumentCaptor
Line 835: Using the captor, we
Line 836: get all the installments
Line 837: passed to the repository.
Line 838: Asserts that the installments 
Line 839: are correct. All of them should 
Line 840: have a value of 10.0.
Line 841: Also asserts that
Line 842: the installments
Line 843: should be one
Line 844: month apart
Line 845: 
Line 846: --- 페이지 216 ---
Line 847: 188
Line 848: CHAPTER 7
Line 849: Designing for testability
Line 850: public List<Installment> generateInstallments(ShoppingCart cart,
Line 851:   ➥ int numberOfInstallments) {
Line 852:   List<Installment> generatedInstallments = new ArrayList<Installment>(); 
Line 853:   LocalDate nextInstallmentDueDate = LocalDate.now();
Line 854:   double amountPerInstallment = cart.getValue() / numberOfInstallments;
Line 855:   for(int i = 1; i <= numberOfInstallments; i++) {
Line 856:     nextInstallmentDueDate = nextInstallmentDueDate.plusMonths(1);
Line 857:     Installment newInstallment =
Line 858:       new Installment(nextInstallmentDueDate, amountPerInstallment);
Line 859:     repository.persist(newInstallment);
Line 860:     generatedInstallments.add(newInstallment); 
Line 861:   }
Line 862:   return generatedInstallments; 
Line 863: }
Line 864: Now we can avoid the ArgumentCaptor completely in the test code.
Line 865: public class InstallmentGeneratorTest {
Line 866:     @Mock
Line 867:     private InstallmentRepository repository;
Line 868:     @Test
Line 869:     void checkInstallments() {
Line 870:       ShoppingCart cart = new ShoppingCart(100.0);
Line 871:       InstallmentGenerator generator =
Line 872:         new InstallmentGenerator(repository);
Line 873:       List<Installment> allInstallments =
Line 874:         generator.generateInstallments(cart, 10); 
Line 875:       assertThat(allInstallments)
Line 876:           .hasSize(10)
Line 877:           .allMatch(i -> i.getValue() == 10); 
Line 878:       for(int month = 1; month <= 10; month++) {
Line 879:         final LocalDate dueDate = LocalDate.now().plusMonths(month);
Line 880:         assertThat(allInstallments)
Line 881:             .anyMatch(i -> i.getDate().equals(dueDate));
Line 882:       }
Line 883:     }
Line 884: }
Line 885: Listing 7.11
Line 886: InstallmentGenerator returning the list of installments
Line 887: Listing 7.12
Line 888: InstallmentGeneratorTest without the ArgumentCaptor
Line 889: Creates a
Line 890: list that will
Line 891: keep track
Line 892: of all the
Line 893: generated
Line 894: installments
Line 895: Stores each of 
Line 896: the generated 
Line 897: installments
Line 898: Returns the list 
Line 899: of installments
Line 900: The method under 
Line 901: test returns the list of 
Line 902: installments. No need 
Line 903: for ArgumentCaptor.
Line 904: Same assertions 
Line 905: as before
Line 906: 
Line 907: --- 페이지 217 ---
Line 908: 189
Line 909: Dependency via class constructor or value via method parameter?
Line 910: Again, do not take this example literally. Just remember that small design changes
Line 911: that improve your testability are fine. Sometimes it can be hard to tell whether a
Line 912: change will make the code design bad. Try it, and if you don’t like it, discard it. Prag-
Line 913: matism is key. 
Line 914: 7.4
Line 915: Dependency via class constructor or value via 
Line 916: method parameter?
Line 917: A very common design decision is whether to pass a dependency to the class via con-
Line 918: structor (so the class uses the dependency to get a required value) or pass that value
Line 919: directly to the method. As always, there is no right or wrong way. However, there is a
Line 920: trade-off you must understand to make the best decision.
Line 921:  Let’s use the ChristmasDiscount example, as it fits this discussion perfectly. The
Line 922: following listing shows the code again.
Line 923: public class ChristmasDiscount {
Line 924:   private final Clock clock;
Line 925:   public ChristmasDiscount(Clock clock) { 
Line 926:     this.clock = clock;
Line 927:   }
Line 928:   public double applyDiscount(double rawAmount) {
Line 929:     LocalDate today = clock.now(); 
Line 930:     double discountPercentage = 0;
Line 931:     boolean isChristmas = today.getMonth()== Month.DECEMBER
Line 932:                 && today.getDayOfMonth()==25;
Line 933:     if(isChristmas)
Line 934:       discountPercentage = 0.15;
Line 935:     return rawAmount - (rawAmount * discountPercentage);
Line 936:   }
Line 937: }
Line 938: The ChristmasDiscount class needs the current date so it knows whether it is
Line 939: Christmas and whether to apply the Christmas discount. To get the date, the class
Line 940: uses another dependency, which knows how to get the current date: the Clock
Line 941: class. Testing ChristmasDiscount is easy because we can stub Clock and simulate
Line 942: any date we want.
Line 943:  But having to stub one class is more complex than not having to stub one class.
Line 944: Another way to model this class and its expected behavior is to avoid the dependency
Line 945: on Clock and receive the data as a parameter of the method. This other implementa-
Line 946: tion is shown in listing 7.14. Now the applyDiscount() method receives two parame-
Line 947: ters: rawAmount and today, which is today’s date.
Line 948: Listing 7.13
Line 949: ChristmasDiscount class, one more time
Line 950: We can inject a stubbed 
Line 951: version of Clock here.
Line 952: Calls the now() method 
Line 953: to get the current date
Line 954: 
Line 955: --- 페이지 218 ---
Line 956: 190
Line 957: CHAPTER 7
Line 958: Designing for testability
Line 959: public class ChristmasDiscount {
Line 960:   public double applyDiscount(double rawAmount, LocalDate today) { 
Line 961:     double discountPercentage = 0;
Line 962:     boolean isChristmas = today.getMonth()== Month.DECEMBER
Line 963:                 && today.getDayOfMonth()==25;
Line 964:     if(isChristmas)
Line 965:       discountPercentage = 0.15;
Line 966:     return rawAmount - (rawAmount * discountPercentage);
Line 967:   }
Line 968: }
Line 969: This method is also easily testable. We do not even need mocks to test it, as we can pass
Line 970: any LocalDate object to this method. So, if it is easier to pass the value via method
Line 971: parameter rather than a dependency via its constructor, why do we do it?
Line 972:  First, let’s explore the pros and cons of passing the value we want directly via a
Line 973: method parameter, avoiding all the dependencies. This is often the simplest solution in
Line 974: terms of both implementation (no need for dependencies via constructor) and testing
Line 975: (passing different values via method calls). But the downside is that all the callers of this
Line 976: class will need to provide this parameter. In this example, ChristmasDiscount expects
Line 977: today to be passed as a parameter. This means the clients of the applyDiscount()
Line 978: method must pass the current date. How do we get the current date in this code base?
Line 979: Using the Clock class. So, while ChristmasDiscount no longer depends on Clock, its
Line 980: callers will depend on it. In a way, we pushed the Clock dependency up one level. The
Line 981: question is, is this dependency better in the class we are modeling now or in its callers?
Line 982:  Now, let’s explore the idea of passing a dependency that knows how to get the
Line 983: required parameter. We did this in the first implementation of the ChristmasDiscount
Line 984: class, which depends on Clock; the applyDiscount() method invokes clock.now()
Line 985: whenever it needs the current date. While this solution is more complicated than the
Line 986: previous one, it enables us to easily stub the dependency as we did in chapter 6.
Line 987:  It is also simple to write tests for the classes that depend on ChristmasDiscount.
Line 988: These classes will mock ChristmasDiscount’s applyDiscount(double rawAmount)
Line 989: method without requiring the Clock. The next listing shows a generic consumer
Line 990: that receives the ChristmasDiscount class via the constructor, so you can stub it
Line 991: during testing.
Line 992: public class SomeBusinessService {
Line 993:   private final ChristmasDiscount discount;
Line 994:   public SomeBusinessService(ChristmasDiscount discount) { 
Line 995:     this.discount = discount;
Line 996:   }
Line 997: Listing 7.14
Line 998: ChristmasDiscount without depending on Clock
Line 999: Listing 7.15
Line 1000: Generic consumer of the ChristmasDiscount class
Line 1001: The method
Line 1002: receives one
Line 1003: more parameter:
Line 1004: a LocalDate.
Line 1005: We inject a
Line 1006: ChristmasDiscount stub here.
Line 1007: 
Line 1008: --- 페이지 219 ---
Line 1009: 191
Line 1010: Designing for testability in the real world
Line 1011:   public void doSomething() {
Line 1012:     // ... some business logic here ...
Line 1013:     discount.applyDiscount(100.0);
Line 1014:     // continue the logic here...
Line 1015:   }
Line 1016: }
Line 1017: Listing 7.16 shows the tests for this SomeBusinessService class. We stub the Christmas-
Line 1018: Discount class. Note that this test does not need to handle Clock. Although Clock is a
Line 1019: dependency of the concrete implementation of ChristmasDiscount, we do not care
Line 1020: about that when stubbing. So, in a way, the ChristmasDiscount class gets more com-
Line 1021: plicated, but we simplify testing its consumers.
Line 1022: @Test
Line 1023: void test() {
Line 1024:   ChristmasDiscount discount = Mockito.mock(ChristmasDiscount.class); 
Line 1025:   SomeBusinessService service = new SomeBusinessService(discount);
Line 1026:   service.doSomething();
Line 1027:   // ... test continues ...
Line 1028: }
Line 1029: Receiving a dependency via constructor adds a little complexity to the overall class
Line 1030: and its tests but simplifies its client classes. Receiving the data via method parameter
Line 1031: simplifies the class and its tests but adds a little complexity to the clients. Software
Line 1032: engineering is all about trade-offs.
Line 1033:  As a rule of thumb, I try to simplify the work of the callers of my class. If I must
Line 1034: choose between simplifying the class I am testing now (such as making Christmas-
Line 1035: Discount receive the date via parameter) but complicating the life of all its callers
Line 1036: (they all must get the date of today themselves) or the other way around (Christmas-
Line 1037: Discount gets more complicated and depends on Clock, but the callers do not need
Line 1038: anything else), I always pick the latter. 
Line 1039: 7.5
Line 1040: Designing for testability in the real world
Line 1041: Writing tests offers a significant advantage during development: if you pay attention to
Line 1042: them (or listen to them, as many developers say), they may give you hints about the
Line 1043: design of the code you are testing. Achieving good class design is a challenge in com-
Line 1044: plex object-oriented systems. The more help we get, the better.
Line 1045:  The buzz about tests giving feedback about the design of the code comes from the
Line 1046: fact that all your test code does is exercise the production class:
Line 1047: 1
Line 1048: It instantiates the class under test. It can be as simple as a new A() or as compli-
Line 1049: cated as A(dependency1, dependency2, …). If a class needs dependencies, the
Line 1050: test should also instantiate them.
Line 1051: Listing 7.16
Line 1052: Example of the test for the generic consumer class
Line 1053: Mocks ChristmasDiscount. Note
Line 1054: that we do not need to mock
Line 1055: or do anything with Clock.
Line 1056: 
Line 1057: --- 페이지 220 ---
Line 1058: 192
Line 1059: CHAPTER 7
Line 1060: Designing for testability
Line 1061: 2
Line 1062: It invokes the method under test. It can be as simple as a.method() or as com-
Line 1063: plicated as a.precall1(); a.precall2(); a.method(param1, param2, …);. If a
Line 1064: method has pre-conditions before being invoked and/or receiving parameters,
Line 1065: the test should also be responsible for those.
Line 1066: 3
Line 1067: It asserts that the method behaves as expected. It can be as simple as assert-
Line 1068: That(return).isEqualTo(42); or as complicated as dozens of lines to
Line 1069: observe what has happened in the system. Again, your test code is responsible
Line 1070: for all the assertions.
Line 1071: You should constantly monitor how hard it is to perform each of these steps. Is it dif-
Line 1072: ficult to instantiate the class under test? Maybe there is a way to design it with fewer
Line 1073: dependencies. Is it hard to invoke the method under test? Maybe there is a way to
Line 1074: design it so its pre-conditions are easier to handle. Is it difficult to assert the out-
Line 1075: come of the method? Maybe there is a way to design it so it is easier to observe what
Line 1076: the method does.
Line 1077:  Next, I will describe some things I pay attention to when writing tests. They give me
Line 1078: feedback about the design and testability of the class I am testing.
Line 1079: 7.5.1
Line 1080: The cohesion of the class under test
Line 1081: Cohesion is about a module, a class, a method, or any element in your architecture
Line 1082: having only a single responsibility. Classes with multiple responsibilities are naturally
Line 1083: more complex and harder to comprehend than classes with fewer responsibilities. So,
Line 1084: strive for classes and methods that do one thing. Defining what a single responsibility
Line 1085: means is tricky and highly context-dependent. Nevertheless, sometimes it can be easy
Line 1086: to detect multiple responsibilities in a single element, such as a method that calculates
Line 1087: a specific tax and updates the values of all its invoices.
Line 1088:  Let’s give you some ideas about what you can observe in a test. Note that these tips
Line 1089: are symptoms or indications that something may be wrong with the production code.
Line 1090: It is up to you to make the final decision. Also, note that these tips are solely based on
Line 1091: my experience as a developer and are not scientifically validated:
Line 1092: Non-cohesive classes have very large test suites. They contain a lot of behavior that
Line 1093: needs to be tested. Pay attention to the number of tests you write for a single
Line 1094: class and/or method. If the number of tests grows beyond what you consider
Line 1095: reasonable, maybe it is time to re-evaluate the responsibilities of that class or
Line 1096: method. A common refactoring strategy is to break the class in two.
Line 1097: Non-cohesive classes have test suites that never stop growing. You expect the class to
Line 1098: reach a more stable status at some point. However, if you notice that you are
Line 1099: always going back to the same test class and adding new tests, this may be a bad
Line 1100: design. It is usually related to the lack of a decent abstraction.
Line 1101: – A class that never stops growing breaks both the Single Responsibility (SRP)
Line 1102: and the Open Closed (OCP) principles from the SOLID guidelines. A com-
Line 1103: mon refactoring strategy is to create an abstraction to represent the different
Line 1104: 
Line 1105: --- 페이지 221 ---
Line 1106: 193
Line 1107: Designing for testability in the real world
Line 1108: roles and move each calculation rule to its own class. Google the Strategy
Line 1109: design pattern to see code examples. 
Line 1110: 7.5.2
Line 1111: The coupling of the class under test
Line 1112: In a world of cohesive classes, we combine different classes to build large behaviors.
Line 1113: But doing so may lead to a highly coupled design. Excessive coupling may harm evolu-
Line 1114: tion, as changes in one class may propagate to other classes in ways that are not clear.
Line 1115: Therefore, we should strive for classes that are coupled as little as possible.
Line 1116:  Your test code can help you detect highly coupled classes:
Line 1117: If the production class requires you to instantiate many dependencies in your
Line 1118: test code, this may be a sign. Consider redesigning the class. There are different
Line 1119: refactoring strategies you can employ. Maybe the large behavior that the class
Line 1120: implements can be broken into two steps.
Line 1121: – Sometimes coupling is unavoidable, and the best we can do is manage it bet-
Line 1122: ter. Breaking a class enables developers to test it more easily. I will give more
Line 1123: concrete examples of such cases in the following chapters.
Line 1124: Another sign is if you observe a test failing in class ATest (supposedly testing the
Line 1125: behavior of class A), but when you debug it, you find the problem in class B. This
Line 1126: is a clear issue with dependencies: a problem in class B somehow leaked to class A.
Line 1127: It is time to re-evaluate how these classes are coupled and how they interact and
Line 1128: see if such leakages can be prevented in future versions of the system. 
Line 1129: 7.5.3
Line 1130: Complex conditions and testability
Line 1131: We have seen in previous chapters that very complex conditions (such as an if state-
Line 1132: ment composed of multiple boolean operations) require considerable effort from tes-
Line 1133: ters. For example, we may devise too many tests after applying boundary testing or
Line 1134: condition + branch coverage criteria. Reducing the complexity of such conditions by,
Line 1135: for example, breaking them into multiple smaller conditions will not reduce the over-
Line 1136: all complexity of the problem but will at least spread it out. 
Line 1137: 7.5.4
Line 1138: Private methods and testability
Line 1139: A common question among developers is whether to test private methods. In princi-
Line 1140: ple, testers should test private methods only through their public methods. However,
Line 1141: testers often feel the urge to test a particular private method in isolation.
Line 1142:  A common reason for this feeling is the lack of cohesion or the complexity of the
Line 1143: private method. In other words, this method does something so different from the
Line 1144: public method, and/or its task is so complicated, that it must be tested separately. This
Line 1145: is a good example of the test speaking to us. In terms of design, this may mean the pri-
Line 1146: vate method does not belong in its current place. A common refactoring is to extract
Line 1147: the method, perhaps to a brand new class. There, the former private method, now a
Line 1148: public method, can be tested normally. The original class, where the private method
Line 1149: used to be, should now depend on this new class. 
Line 1150: 
Line 1151: --- 페이지 222 ---
Line 1152: 194
Line 1153: CHAPTER 7
Line 1154: Designing for testability
Line 1155: 7.5.5
Line 1156: Static methods, singletons, and testability
Line 1157: As we have seen, static methods adversely affect testability. Therefore, a good rule of
Line 1158: thumb is to avoid creating static methods whenever possible. Exceptions to this rule are
Line 1159: utility methods, which are often not mocked. If your system has to depend on a specific
Line 1160: static method, perhaps because it comes with the framework your software depends on,
Line 1161: adding an abstraction on top of it—similar to what we did with the LocalDate class in
Line 1162: the previous chapter—may be a good decision to facilitate testability.
Line 1163:  The same recommendation applies when your system needs code from others or
Line 1164: external dependencies. Again, creating layers and classes that abstract away the
Line 1165: dependency may help you increase testability. Don’t be afraid to create these extra lay-
Line 1166: ers: although it may seem that they will increase the overall complexity of the design,
Line 1167: the increased testability pays off.
Line 1168:  Using the Singleton design pattern also harms testability. This approach ensures
Line 1169: that there is only one instance of a class throughout the entire system. Whenever you
Line 1170: need an instance of that class, you ask the singleton, and the singleton returns the
Line 1171: same one. A singleton makes testing difficult because it is like having a global variable
Line 1172: that is persistent throughout the program’s life cycle. When testing software systems
Line 1173: that use singletons, we often have to write extra code in the test suite to reset or
Line 1174: replace the singleton in the different test cases. Singletons also bring other disadvan-
Line 1175: tages to maintainability in general. If you are not familiar with this pattern, I suggest
Line 1176: reading about it. 
Line 1177: 7.5.6
Line 1178: The Hexagonal Architecture and mocks as a design technique
Line 1179: Now that you know about the Hexagonal Architecture and the idea of ports and
Line 1180: adapters, we can talk about mocks as a design technique. In a nutshell, whenever
Line 1181: mockists develop a feature (or a domain object) and notice that they need something
Line 1182: from another place, they let a port emerge. As we saw, the port is an interface that
Line 1183: allows the mockist to develop the remainder of the feature without being bothered by
Line 1184: the concrete implementation of the adapter. The mockist takes this as a design activ-
Line 1185: ity: they reflect on the contract that the port should offer to the core of the applica-
Line 1186: tion and model the best interface possible.
Line 1187:  Whenever I am coding a class (or set of classes) and notice that I need something
Line 1188: else, I let an interface emerge that represents this “something else.” I reflect on what the
Line 1189: class under development needs from it, model the best interface, and continue develop-
Line 1190: ing the class. Only later do I implement the concrete adapter. I enjoy this approach as it
Line 1191: lets me focus on the class I am implementing by giving me a way to abstract things that I
Line 1192: do not care about right now, like the implementation of adapters. 
Line 1193:  
Line 1194:  
Line 1195: 
Line 1196: --- 페이지 223 ---
Line 1197: 195
Line 1198: Exercises
Line 1199: 7.5.7
Line 1200: Further reading about designing for testability
Line 1201: Entire books can be written about this topic. In fact, entire books have been written
Line 1202: about it:
Line 1203: Michael Feathers’s Working Effectively with Legacy Code (2004) is about working
Line 1204: with legacy systems, but a huge part of it is about untestable code (common in
Line 1205: legacy) and how to make it testable. Feathers also has a nice talk on YouTube
Line 1206: about the “deep synergy between well-designed production code and testabil-
Line 1207: ity,” as he calls it (2013).
Line 1208: Steve Freeman and Nat Pryce’s book Growing-Object Oriented Systems Guided by
Line 1209: Tests (2009) is also a primer for writing classes that are easy to test.
Line 1210: Robert Martin’s Clean Architecture ideas (2018) align with the ideas discussed here. 
Line 1211: Exercises
Line 1212: 7.1
Line 1213: Observability and controllability are two important concepts of software testing.
Line 1214: Three developers could benefit from improving either the observability or the
Line 1215: controllability of the system/class they are testing, but each developer encoun-
Line 1216: ters a problem.
Line 1217: State whether each of the problems relates to observability or controllability.
Line 1218: A Developer 1: “I can’t assert whether the method under test worked well.”
Line 1219: B Developer 2: “I need to make sure this class starts with a boolean set to
Line 1220: false, but I can’t do it.”
Line 1221: C Developer 3: “I instantiated the mock object, but there’s no way to inject it
Line 1222: into the class.”
Line 1223: 7.2
Line 1224: Sarah has joined a mobile app team that has been trying to write automated
Line 1225: tests for a while. The team wants to write unit tests for part of their code, but
Line 1226: they tell Sarah, “It’s hard.” After some code review, the developers list the fol-
Line 1227: lowing problems in their code base:
Line 1228: A Many classes mix infrastructure and business rules.
Line 1229: B The database has large tables and no indexes.
Line 1230: C There are lots of calls to libraries and external APIs.
Line 1231: D Some classes have too many attributes/fields.
Line 1232: To increase testability, the team has a budget to work on two of these four
Line 1233: issues. Which items should Sarah recommend that they tackle first?
Line 1234: Note: All four issues should be fixed, but try to prioritize the two most
Line 1235: important ones. Which influences testability the most?
Line 1236: 7.3
Line 1237: How can you improve the testability of the following OrderDeliveryBatch class?
Line 1238: public class OrderDeliveryBatch {
Line 1239:   public void runBatch() {
Line 1240: 
Line 1241: --- 페이지 224 ---
Line 1242: 196
Line 1243: CHAPTER 7
Line 1244: Designing for testability
Line 1245:     OrderDao dao = new OrderDao();
Line 1246:     DeliveryStartProcess delivery = new DeliveryStartProcess();
Line 1247:     List<Order> orders = dao.paidButNotDelivered();
Line 1248:     for (Order order : orders) {
Line 1249:       delivery.start(order);
Line 1250:       if (order.isInternational()) {
Line 1251:         order.setDeliveryDate("5 days from now");
Line 1252:       } else {
Line 1253:         order.setDeliveryDate("2 days from now");
Line 1254:       }
Line 1255:     }
Line 1256:   }
Line 1257: }
Line 1258: class OrderDao {
Line 1259:   // accesses a database
Line 1260: }
Line 1261: class DeliveryStartProcess {
Line 1262:   // communicates with a third-party web service
Line 1263: }
Line 1264: 7.4
Line 1265: Consider the KingsDayDiscount class below:
Line 1266: public class KingsDayDiscount {
Line 1267:   public double discount(double value) {
Line 1268:     Calendar today = Calendar.getInstance();
Line 1269:     boolean isKingsDay = today.get(MONTH) == Calendar.APRIL
Line 1270:         && today.get(DAY_OF_MONTH) == 27;
Line 1271:     return isKingsDay ? value * 0.15 : 0;
Line 1272:   }
Line 1273: }
Line 1274: What would you do to make this class more testable?
Line 1275: 7.5
Line 1276: Think about your current project. Are parts of it hard to test? Can you explain
Line 1277: why? What can you do to make it more testable?
Line 1278: Summary
Line 1279: Writing tests can be easy or hard. Untestable code makes our lives harder. Strive
Line 1280: for code that is easy (or at least easier) to test.
Line 1281: Separate infrastructure from domain code. Infrastructure makes it harder to
Line 1282: write tests. Separating domain from infrastructure enables us to write unit tests
Line 1283: for the domain logic much more cheaply.
Line 1284: 
Line 1285: --- 페이지 225 ---
Line 1286: 197
Line 1287: Summary
Line 1288: Ensure that classes are easily controllable and observable. Controllability is usu-
Line 1289: ally achieved by ensuring that we can control the dependencies of the class
Line 1290: under test. Observability is achieved by ensuring that the class provides easy
Line 1291: ways for the test to assert expected behavior.
Line 1292: While you should not change your code in ways you do not believe in, you
Line 1293: should also be pragmatic. I am all in favor of changing the production code to
Line 1294: facilitate testing.
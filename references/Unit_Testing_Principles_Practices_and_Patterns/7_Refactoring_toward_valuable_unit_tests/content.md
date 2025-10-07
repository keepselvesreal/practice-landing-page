Line 1: 
Line 2: --- 페이지 173 ---
Line 3: 151
Line 4: Refactoring toward
Line 5: valuable unit tests
Line 6: In chapter 1, I defined the properties of a good unit test suite:
Line 7: It is integrated into the development cycle.
Line 8: It targets only the most important parts of your code base.
Line 9: It provides maximum value with minimum maintenance costs. To achieve
Line 10: this last attribute, you need to be able to:
Line 11: – Recognize a valuable test (and, by extension, a test of low value).
Line 12: – Write a valuable test.
Line 13: Chapter 4 covered the topic of recognizing a valuable test using the four attributes:
Line 14: protection against regressions, resistance to refactoring, fast feedback, and main-
Line 15: tainability. And chapter 5 expanded on the most important one of the four: resis-
Line 16: tance to refactoring.
Line 17:  As I mentioned earlier, it’s not enough to recognize valuable tests, you should also
Line 18: be able to write such tests. The latter skill requires the former, but it also requires
Line 19: This chapter covers
Line 20: Recognizing the four types of code
Line 21: Understanding the Humble Object pattern
Line 22: Writing valuable tests
Line 23: 
Line 24: --- 페이지 174 ---
Line 25: 152
Line 26: CHAPTER 7
Line 27: Refactoring toward valuable unit tests
Line 28: that you know code design techniques. Unit tests and the underlying code are highly
Line 29: intertwined, and it’s impossible to create valuable tests without putting effort into the
Line 30: code base they cover.
Line 31:  You saw an example of a code base transformation in chapter 6, where we refac-
Line 32: tored an audit system toward a functional architecture and, as a result, were able to
Line 33: apply output-based testing. This chapter generalizes this approach onto a wider spec-
Line 34: trum of applications, including those that can’t use a functional architecture. You’ll
Line 35: see practical guidelines on how to write valuable tests in almost any software project.
Line 36: 7.1
Line 37: Identifying the code to refactor
Line 38: It’s rarely possible to significantly improve a test suite without refactoring the underly-
Line 39: ing code. There’s no way around it—test and production code are intrinsically con-
Line 40: nected. In this section, you’ll see how to categorize your code into the four types in
Line 41: order to outline the direction of the refactoring. The subsequent sections show a com-
Line 42: prehensive example.
Line 43: 7.1.1
Line 44: The four types of code
Line 45: In this section, I describe the four types of code that serve as a foundation for the rest
Line 46: of this chapter. 
Line 47:  All production code can be categorized along two dimensions:
Line 48: Complexity or domain significance
Line 49: The number of collaborators
Line 50: Code complexity is defined by the number of decision-making (branching) points in the
Line 51: code. The greater that number, the higher the complexity.
Line 52: How to calculate cyclomatic complexity
Line 53: In computer science, there’s a special term that describes code complexity: cyclo-
Line 54: matic complexity. Cyclomatic complexity indicates the number of branches in a given
Line 55: program or method. This metric is calculated as
Line 56: 1 + <number of branching points>
Line 57: Thus, a method with no control flow statements (such as if statements or condi-
Line 58: tional loops) has a cyclomatic complexity of 1 + 0 = 1.
Line 59: There’s another meaning to this metric. You can think of it in terms of the number of
Line 60: independent paths through the method from an entry to an exit, or the number of tests
Line 61: needed to get a 100% branch coverage.
Line 62: Note that the number of branching points is counted as the number of simplest pred-
Line 63: icates involved. For instance, a statement like IF condition1 AND condition2
Line 64: THEN ... is equivalent to IF condition1 THEN IF condition2 THEN ... Therefore,
Line 65: its complexity would be 1 + 2 = 3.
Line 66: 
Line 67: --- 페이지 175 ---
Line 68: 153
Line 69: Identifying the code to refactor
Line 70: Domain significance shows how significant the code is for the problem domain of your
Line 71: project. Normally, all code in the domain layer has a direct connection to the end
Line 72: users’ goals and thus exhibits a high domain significance. On the other hand, utility
Line 73: code doesn’t have such a connection.
Line 74:  Complex code and code that has domain significance benefit from unit testing the
Line 75: most because the corresponding tests have great protection against regressions. Note
Line 76: that the domain code doesn’t have to be complex, and complex code doesn’t have to
Line 77: exhibit domain significance to be test-worthy. The two components are independent
Line 78: of each other. For example, a method calculating an order price can contain no con-
Line 79: ditional statements and thus have the cyclomatic complexity of 1. Still, it’s important
Line 80: to test such a method because it represents business-critical functionality.
Line 81:  The second dimension is the number of collaborators a class or a method has. As
Line 82: you may remember from chapter 2, a collaborator is a dependency that is either
Line 83: mutable or out-of-process (or both). Code with a large number of collaborators is
Line 84: expensive to test. That’s due to the maintainability metric, which depends on the size
Line 85: of the test. It takes space to bring collaborators to an expected condition and then
Line 86: check their state or interactions with them afterward. And the more collaborators
Line 87: there are, the larger the test becomes.
Line 88:  The type of the collaborators also matters. Out-of-process collaborators are a no-go
Line 89: when it comes to the domain model. They add additional maintenance costs due to
Line 90: the necessity to maintain complicated mock machinery in tests. You also have to be
Line 91: extra prudent and only use mocks to verify interactions that cross the application
Line 92: boundary in order to maintain proper resistance to refactoring (refer to chapter 5 for
Line 93: more details). It’s better to delegate all communications with out-of-process depen-
Line 94: dencies to classes outside the domain layer. The domain classes then will only work
Line 95: with in-process dependencies.
Line 96:  Notice that both implicit and explicit collaborators count toward this number. It
Line 97: doesn’t matter if the system under test (SUT) accepts a collaborator as an argument
Line 98: or refers to it implicitly via a static method, you still have to set up this collaborator in
Line 99: tests. Conversely, immutable dependencies (values or value objects) don’t count. Such
Line 100: dependencies are much easier to set up and assert against.
Line 101:  The combination of code complexity, its domain significance, and the number of
Line 102: collaborators give us the four types of code shown in figure 7.1:
Line 103: Domain model and algorithms (figure 7.1, top left)—Complex code is often part of
Line 104: the domain model but not in 100% of all cases. You might have a complex algo-
Line 105: rithm that’s not directly related to the problem domain.
Line 106: Trivial code (figure 7.1, bottom left)—Examples of such code in C# are parameter-
Line 107: less constructors and one-line properties: they have few (if any) collaborators
Line 108: and exhibit little complexity or domain significance.
Line 109: Controllers (figure 7.1, bottom right)—This code doesn’t do complex or business-
Line 110: critical work by itself but coordinates the work of other components like domain
Line 111: classes and external applications.
Line 112: 
Line 113: --- 페이지 176 ---
Line 114: 154
Line 115: CHAPTER 7
Line 116: Refactoring toward valuable unit tests
Line 117: Overcomplicated code (figure 7.1, top right)—Such code scores highly on both
Line 118: metrics: it has a lot of collaborators, and it’s also complex or important. An
Line 119: example here are fat controllers (controllers that don’t delegate complex work
Line 120: anywhere and do everything themselves).
Line 121: Unit testing the top-left quadrant (domain model and algorithms) gives you the best
Line 122: return for your efforts. The resulting unit tests are highly valuable and cheap. They’re
Line 123: valuable because the underlying code carries out complex or important logic, thus
Line 124: increasing tests’ protection against regressions. And they’re cheap because the code
Line 125: has few collaborators (ideally, none), thus decreasing tests’ maintenance costs.
Line 126:  Trivial code shouldn’t be tested at all; such tests have a close-to-zero value. As for
Line 127: controllers, you should test them briefly as part of a much smaller set of the overarch-
Line 128: ing integration tests (I cover this topic in part 3).
Line 129:  The most problematic type of code is the overcomplicated quadrant. It’s hard to
Line 130: unit test but too risky to leave without test coverage. Such code is one of the main rea-
Line 131: sons many people struggle with unit testing. This whole chapter is primarily devoted
Line 132: to how you can bypass this dilemma. The general idea is to split overcomplicated code
Line 133: into two parts: algorithms and controllers (figure 7.2), although the actual implemen-
Line 134: tation can be tricky at times.
Line 135: TIP
Line 136: The more important or complex the code, the fewer collaborators it
Line 137: should have.
Line 138: Getting rid of the overcomplicated code and unit testing only the domain model and
Line 139: algorithms is the path to a highly valuable, easily maintainable test suite. With this
Line 140: approach, you won’t have 100% test coverage, but you don’t need to—100% coverage
Line 141: shouldn’t ever be your goal. Your goal is a test suite where each test adds significant
Line 142: value to the project. Refactor or get rid of all other tests. Don’t allow them to inflate
Line 143: the size of your test suite.
Line 144: Complexity,
Line 145: domain
Line 146: signiﬁcance
Line 147: Domain model,
Line 148: algorithms
Line 149: Overcomplicated
Line 150: code
Line 151: Trivial code
Line 152: Number of
Line 153: collaborators
Line 154: Controllers
Line 155: Figure 7.1
Line 156: The four types of code, 
Line 157: categorized by code complexity and 
Line 158: domain significance (the vertical 
Line 159: axis) and the number of collaborators 
Line 160: (the horizontal axis).
Line 161: 
Line 162: --- 페이지 177 ---
Line 163: 155
Line 164: Identifying the code to refactor
Line 165: NOTE
Line 166: Remember that it’s better to not write a test at all than to write a
Line 167: bad test.
Line 168: Of course, getting rid of overcomplicated code is easier said than done. Still, there are
Line 169: techniques that can help you do that. I’ll first explain the theory behind those tech-
Line 170: niques and then demonstrate them using a close-to-real-world example. 
Line 171: 7.1.2
Line 172: Using the Humble Object pattern to split overcomplicated code
Line 173: To split overcomplicated code, you need to use the Humble Object design pattern.
Line 174: This pattern was introduced by Gerard Meszaros in his book xUnit Test Patterns: Refac-
Line 175: toring Test Code (Addison-Wesley, 2007) as one of the ways to battle code coupling, but
Line 176: it has a much broader application. You’ll see why shortly.
Line 177:  We often find that code is hard to test because it’s coupled to a framework depen-
Line 178: dency (see figure 7.3). Examples include asynchronous or multi-threaded execution,
Line 179: user interfaces, communication with out-of-process dependencies, and so on.
Line 180: To bring the logic of this code under test, you need to extract a testable part out of it.
Line 181: As a result, the code becomes a thin, humble wrapper around that testable part: it glues
Line 182: Complexity,
Line 183: domain
Line 184: signiﬁcance
Line 185: Domain model,
Line 186: algorithms
Line 187: Overcomplicated
Line 188: code
Line 189: Trivial code
Line 190: Number of
Line 191: collaborators
Line 192: Controllers
Line 193: Figure 7.2
Line 194: Refactor overcomplicated 
Line 195: code by splitting it into algorithms and 
Line 196: controllers. Ideally, you should have no 
Line 197: code in the top-right quadrant.
Line 198: Overcomplicated code
Line 199: Hard-to-test
Line 200: dependency
Line 201: Logic
Line 202: Test
Line 203: Figure 7.3
Line 204: It’s hard to test 
Line 205: code that couples to a difficult 
Line 206: dependency. Tests have to deal 
Line 207: with that dependency, too, which 
Line 208: increases their maintenance cost.
Line 209: 
Line 210: --- 페이지 178 ---
Line 211: 156
Line 212: CHAPTER 7
Line 213: Refactoring toward valuable unit tests
Line 214: the hard-to-test dependency and the newly extracted component together, but itself
Line 215: contains little or no logic and thus doesn’t need to be tested (figure 7.4).
Line 216:  If this approach looks familiar, it’s because you already saw it in this book. In fact,
Line 217: both hexagonal and functional architectures implement this exact pattern. As you
Line 218: may remember from previous chapters, hexagonal architecture advocates for the sep-
Line 219: aration of business logic and communications with out-of-process dependencies. This
Line 220: is what the domain and application services layers are responsible for, respectively.
Line 221:  Functional architecture goes even further and separates business logic from com-
Line 222: munications with all collaborators, not just out-of-process ones. This is what makes
Line 223: functional architecture so testable: its functional core has no collaborators. All depen-
Line 224: dencies in a functional core are immutable, which brings it very close to the vertical
Line 225: axis on the types-of-code diagram (figure 7.5).
Line 226: Humble object
Line 227: Hard-to-test
Line 228: dependency
Line 229: Test
Line 230: Logic
Line 231: Figure 7.4
Line 232: The Humble Object 
Line 233: pattern extracts the logic out of the 
Line 234: overcomplicated code, making that 
Line 235: code so humble that it doesn’t need to 
Line 236: be tested. The extracted logic is 
Line 237: moved into another class, decoupled 
Line 238: from the hard-to-test dependency.
Line 239: Complexity,
Line 240: domain
Line 241: signiﬁcance
Line 242: Number of
Line 243: collaborators
Line 244: Domain model,
Line 245: algorithms
Line 246: Overcomplicated
Line 247: code
Line 248: Trivial code
Line 249: Controllers
Line 250: Domain layer
Line 251: Mutable shell and
Line 252: application services layer
Line 253: Functional core
Line 254: Figure 7.5
Line 255: The functional core in a functional architecture and the domain layer in 
Line 256: a hexagonal architecture reside in the top-left quadrant: they have few collaborators 
Line 257: and exhibit high complexity and domain significance. The functional core is closer 
Line 258: to the vertical axis because it has no collaborators. The mutable shell (functional 
Line 259: architecture) and the application services layer (hexagonal architecture) belong 
Line 260: to the controllers’ quadrant.
Line 261: 
Line 262: --- 페이지 179 ---
Line 263: 157
Line 264: Identifying the code to refactor
Line 265: Another way to view the Humble Object pattern is as a means to adhere to the Single
Line 266: Responsibility principle, which states that each class should have only a single respon-
Line 267: sibility.1 One such responsibility is always business logic; the pattern can be applied to
Line 268: segregate that logic from pretty much anything.
Line 269:  In our particular situation, we are interested in the separation of business logic
Line 270: and orchestration. You can think of these two responsibilities in terms of code depth
Line 271: versus code width. Your code can be either deep (complex or important) or wide (work
Line 272: with many collaborators), but never both (figure 7.6).
Line 273: I can’t stress enough how important this separation is. In fact, many well-known princi-
Line 274: ples and patterns can be described as a form of the Humble Object pattern: they are
Line 275: designed specifically to segregate complex code from the code that does orchestration.
Line 276:  You already saw the relationship between this pattern and hexagonal and func-
Line 277: tional architectures. Other examples include the Model-View-Presenter (MVP) and
Line 278: the Model-View-Controller (MVC) patterns. These two patterns help you decouple
Line 279: business logic (the Model part), UI concerns (the View), and the coordination between
Line 280: them (Presenter or Controller). The Presenter and Controller components are humble
Line 281: objects: they glue the view and the model together.
Line 282:  Another example is the Aggregate pattern from Domain-Driven Design.2 One of its
Line 283: goals is to reduce connectivity between classes by grouping them into clusters—
Line 284: aggregates. The classes are highly connected inside those clusters, but the clusters them-
Line 285: selves are loosely coupled. Such a structure decreases the total number of communica-
Line 286: tions in the code base. The reduced connectivity, in turn, improves testability.
Line 287: 1 See Agile Principles, Patterns, and Practices in C# by Robert C. Martin and Micah Martin (Prentice Hall, 2006).
Line 288: 2 See Domain-Driven Design: Tackling Complexity in the Heart of Software by Eric Evans (Addison-Wesley, 2003).
Line 289: Controllers
Line 290: Domain layer,
Line 291: algorithms
Line 292: Figure 7.6
Line 293: Code depth versus code width is 
Line 294: a useful metaphor to apply when you think of 
Line 295: the separation between the business logic 
Line 296: and orchestration responsibilities. Controllers 
Line 297: orchestrate many dependencies (represented as 
Line 298: arrows in the figure) but aren’t complex on their 
Line 299: own (complexity is represented as block height). 
Line 300: Domain classes are the opposite of that.
Line 301: 
Line 302: --- 페이지 180 ---
Line 303: 158
Line 304: CHAPTER 7
Line 305: Refactoring toward valuable unit tests
Line 306:  Note that improved testability is not the only reason to maintain the separation
Line 307: between business logic and orchestration. Such a separation also helps tackle code
Line 308: complexity, which is crucial for project growth, too, especially in the long run. I per-
Line 309: sonally always find it fascinating how a testable design is not only testable but also easy
Line 310: to maintain. 
Line 311: 7.2
Line 312: Refactoring toward valuable unit tests
Line 313: In this section, I’ll show a comprehensive example of splitting overcomplicated code
Line 314: into algorithms and controllers. You saw a similar example in the previous chapter,
Line 315: where we talked about output-based testing and functional architecture. This time, I’ll
Line 316: generalize this approach to all enterprise-level applications, with the help of the Hum-
Line 317: ble Object pattern. I’ll use this project not only in this chapter but also in the subse-
Line 318: quent chapters of part 3.
Line 319: 7.2.1
Line 320: Introducing a customer management system
Line 321: The sample project is a customer management system (CRM) that handles user
Line 322: registrations. All users are stored in a database. The system currently supports only
Line 323: one use case: changing a user’s email. There are three business rules involved in this
Line 324: operation:
Line 325: If the user’s email belongs to the company’s domain, that user is marked as an
Line 326: employee. Otherwise, they are treated as a customer.
Line 327: The system must track the number of employees in the company. If the user’s
Line 328: type changes from employee to customer, or vice versa, this number must
Line 329: change, too.
Line 330: When the email changes, the system must notify external systems by sending a
Line 331: message to a message bus.
Line 332: The following listing shows the initial implementation of the CRM system.
Line 333: public class User
Line 334: {
Line 335: public int UserId { get; private set; }
Line 336: public string Email { get; private set; }
Line 337: public UserType Type { get; private set; }
Line 338: public void ChangeEmail(int userId, string newEmail)
Line 339: {
Line 340: object[] data = Database.GetUserById(userId);    
Line 341: UserId = userId;
Line 342: Email = (string)data[1];
Line 343: Type = (UserType)data[2];
Line 344: if (Email == newEmail)
Line 345: return;
Line 346: Listing 7.1
Line 347: Initial implementation of the CRM system
Line 348: Retrieves the user’s 
Line 349: current email and 
Line 350: type from the 
Line 351: database
Line 352: 
Line 353: --- 페이지 181 ---
Line 354: 159
Line 355: Refactoring toward valuable unit tests
Line 356: object[] companyData = Database.GetCompany();       
Line 357: string companyDomainName = (string)companyData[0];
Line 358: int numberOfEmployees = (int)companyData[1];
Line 359: string emailDomain = newEmail.Split('@')[1];
Line 360: bool isEmailCorporate = emailDomain == companyDomainName;
Line 361: UserType newType = isEmailCorporate                       
Line 362: ? UserType.Employee
Line 363:                        
Line 364: : UserType.Customer;
Line 365:                        
Line 366: if (Type != newType)
Line 367: {
Line 368: int delta = newType == UserType.Employee ? 1 : -1;
Line 369: int newNumber = numberOfEmployees + delta;
Line 370: Database.SaveCompany(newNumber);        
Line 371: }
Line 372: Email = newEmail;
Line 373: Type = newType;
Line 374: Database.SaveUser(this);              
Line 375: MessageBus.SendEmailChangedMessage(UserId, newEmail);       
Line 376: }
Line 377: }
Line 378: public enum UserType
Line 379: {
Line 380: Customer = 1,
Line 381: Employee = 2
Line 382: }
Line 383: The User class changes a user email. Note that, for brevity, I omitted simple valida-
Line 384: tions such as checks for email correctness and user existence in the database. Let’s
Line 385: analyze this implementation from the perspective of the types-of-code diagram.
Line 386:  The code’s complexity is not too high. The ChangeEmail method contains only a
Line 387: couple of explicit decision-making points: whether to identify the user as an employee
Line 388: or a customer, and how to update the company’s number of employees. Despite being
Line 389: simple, these decisions are important: they are the application’s core business logic.
Line 390: Hence, the class scores highly on the complexity and domain significance dimension.
Line 391:  On the other hand, the User class has four dependencies, two of which are explicit
Line 392: and the other two of which are implicit. The explicit dependencies are the userId
Line 393: and newEmail arguments. These are values, though, and thus don’t count toward the
Line 394: class’s number of collaborators. The implicit ones are Database and MessageBus.
Line 395: These two are out-of-process collaborators. As I mentioned earlier, out-of-process col-
Line 396: laborators are a no-go for code with high domain significance. Hence, the User class
Line 397: scores highly on the collaborators dimension, which puts this class into the overcom-
Line 398: plicated category (figure 7.7).
Line 399:  This approach—when a domain class retrieves and persists itself to the database—
Line 400: is called the Active Record pattern. It works fine in simple or short-lived projects but
Line 401: Retrieves the organization’s 
Line 402: domain name and the 
Line 403: number of employees 
Line 404: from the database
Line 405: Sets the user type 
Line 406: depending on the new 
Line 407: email’s domain name
Line 408: Updates the number 
Line 409: of employees in the 
Line 410: organization, if needed
Line 411: Persists the user 
Line 412: in the database
Line 413: Sends a notification
Line 414: to the message bus
Line 415: 
Line 416: --- 페이지 182 ---
Line 417: 160
Line 418: CHAPTER 7
Line 419: Refactoring toward valuable unit tests
Line 420: often fails to scale as the code base grows. The reason is precisely this lack of separa-
Line 421: tion between these two responsibilities: business logic and communication with out-of-
Line 422: process dependencies. 
Line 423: 7.2.2
Line 424: Take 1: Making implicit dependencies explicit
Line 425: The usual approach to improve testability is to make implicit dependencies explicit:
Line 426: that is, introduce interfaces for Database and MessageBus, inject those interfaces into
Line 427: User, and then mock them in tests. This approach does help, and that’s exactly what
Line 428: we did in the previous chapter when we introduced the implementation with mocks
Line 429: for the audit system. However, it’s not enough.
Line 430:  From the perspective of the types-of-code diagram, it doesn’t matter if the domain
Line 431: model refers to out-of-process dependencies directly or via an interface. Such depen-
Line 432: dencies are still out-of-process; they are proxies to data that is not yet in memory. You
Line 433: still need to maintain complicated mock machinery in order to test such classes,
Line 434: which increases the tests’ maintenance costs. Moreover, using mocks for the database
Line 435: dependency would lead to test fragility (we’ll discuss this in the next chapter).
Line 436:  Overall, it’s much cleaner for the domain model not to depend on out-of-process
Line 437: collaborators at all, directly or indirectly (via an interface). That’s what the hexagonal
Line 438: architecture advocates as well—the domain model shouldn’t be responsible for com-
Line 439: munications with external systems. 
Line 440: 7.2.3
Line 441: Take 2: Introducing an application services layer
Line 442: To overcome the problem of the domain model directly communicating with external
Line 443: systems, we need to shift this responsibility to another class, a humble controller (an
Line 444: application service, in the hexagonal architecture taxonomy). As a general rule, domain
Line 445: classes should only depend on in-process dependencies, such as other domain classes,
Line 446: or plain values. Here’s what the first version of that application service looks like.
Line 447: Domain model,
Line 448: algorithms
Line 449: Overcomplicated
Line 450: code
Line 451: Trivial code
Line 452: Controllers
Line 453: Complexity,
Line 454: domain
Line 455: signiﬁcance
Line 456: Number of
Line 457: collaborators
Line 458: User class
Line 459: Figure 7.7
Line 460: The initial 
Line 461: implementation of the User 
Line 462: class scores highly on both 
Line 463: dimensions and thus falls 
Line 464: into the category of 
Line 465: overcomplicated code.
Line 466: 
Line 467: --- 페이지 183 ---
Line 468: 161
Line 469: Refactoring toward valuable unit tests
Line 470: public class UserController
Line 471: {
Line 472: private readonly Database _database = new Database();
Line 473: private readonly MessageBus _messageBus = new MessageBus();
Line 474: public void ChangeEmail(int userId, string newEmail)
Line 475: {
Line 476: object[] data = _database.GetUserById(userId);
Line 477: string email = (string)data[1];
Line 478: UserType type = (UserType)data[2];
Line 479: var user = new User(userId, email, type);
Line 480: object[] companyData = _database.GetCompany();
Line 481: string companyDomainName = (string)companyData[0];
Line 482: int numberOfEmployees = (int)companyData[1];
Line 483: int newNumberOfEmployees = user.ChangeEmail(
Line 484: newEmail, companyDomainName, numberOfEmployees);
Line 485: _database.SaveCompany(newNumberOfEmployees);
Line 486: _database.SaveUser(user);
Line 487: _messageBus.SendEmailChangedMessage(userId, newEmail);
Line 488: }
Line 489: }
Line 490: This is a good first try; the application service helped offload the work with out-of-
Line 491: process dependencies from the User class. But there are some issues with this imple-
Line 492: mentation:
Line 493: The out-of-process dependencies (Database and MessageBus) are instantiated
Line 494: directly, not injected. That’s going to be a problem for the integration tests we’ll
Line 495: be writing for this class.
Line 496: The controller reconstructs a User instance from the raw data it receives from
Line 497: the database. This is complex logic and thus shouldn’t belong to the applica-
Line 498: tion service, whose sole role is orchestration, not logic of any complexity or
Line 499: domain significance.
Line 500: The same is true for the company’s data. The other problem with that data is
Line 501: that User now returns an updated number of employees, which doesn’t look
Line 502: right. The number of company employees has nothing to do with a specific
Line 503: user. This responsibility should belong elsewhere.
Line 504: The controller persists modified data and sends notifications to the message
Line 505: bus unconditionally, regardless of whether the new email is different than the
Line 506: previous one.
Line 507: The User class has become quite easy to test because it no longer has to communicate
Line 508: with out-of-process dependencies. In fact, it has no collaborators whatsoever—out-of-
Line 509: process or not. Here’s the new version of User’s ChangeEmail method:
Line 510: Listing 7.2
Line 511: Application service, version 1
Line 512: 
Line 513: --- 페이지 184 ---
Line 514: 162
Line 515: CHAPTER 7
Line 516: Refactoring toward valuable unit tests
Line 517: public int ChangeEmail(string newEmail,
Line 518: string companyDomainName, int numberOfEmployees)
Line 519: {
Line 520: if (Email == newEmail)
Line 521: return numberOfEmployees;
Line 522: string emailDomain = newEmail.Split('@')[1];
Line 523: bool isEmailCorporate = emailDomain == companyDomainName;
Line 524: UserType newType = isEmailCorporate
Line 525: ? UserType.Employee
Line 526: : UserType.Customer;
Line 527: if (Type != newType)
Line 528: {
Line 529: int delta = newType == UserType.Employee ? 1 : -1;
Line 530: int newNumber = numberOfEmployees + delta;
Line 531: numberOfEmployees = newNumber;
Line 532: }
Line 533: Email = newEmail;
Line 534: Type = newType;
Line 535: return numberOfEmployees;
Line 536: }
Line 537: Figure 7.8 shows where User and UserController currently stand in our diagram.
Line 538: User has moved to the domain model quadrant, close to the vertical axis, because it
Line 539: no longer has to deal with collaborators. UserController is more problematic.
Line 540: Although I’ve put it into the controllers quadrant, it almost crosses the boundary into
Line 541: overcomplicated code because it contains logic that is quite complex. 
Line 542: Domain model,
Line 543: algorithms
Line 544: Overcomplicated
Line 545: code
Line 546: Trivial code
Line 547: Controllers
Line 548: Complexity,
Line 549: domain
Line 550: signiﬁcance
Line 551: Number of
Line 552: collaborators
Line 553: UserController
Line 554: User
Line 555: Figure 7.8
Line 556: Take 2 puts User in the domain model quadrant, close to the vertical 
Line 557: axis. UserController almost crosses the boundary with the overcomplicated 
Line 558: quadrant because it contains complex logic.
Line 559: 
Line 560: --- 페이지 185 ---
Line 561: 163
Line 562: Refactoring toward valuable unit tests
Line 563: 7.2.4
Line 564: Take 3: Removing complexity from the application service
Line 565: To put UserController firmly into the controllers quadrant, we need to extract the
Line 566: reconstruction logic from it. If you use an object-relational mapping (ORM) library
Line 567: to map the database into the domain model, that would be a good place to which to
Line 568: attribute the reconstruction logic. Each ORM library has a dedicated place where you
Line 569: can specify how your database tables should be mapped to domain classes, such as
Line 570: attributes on top of those domain classes, XML files, or files with fluent mappings.
Line 571:  If you don’t want to or can’t use an ORM, create a factory in the domain model
Line 572: that will instantiate the domain classes using raw database data. This factory can be a
Line 573: separate class or, for simpler cases, a static method in the existing domain classes. The
Line 574: reconstruction logic in our sample application is not too complicated, but it’s good to
Line 575: keep such things separated, so I’m putting it in a separate UserFactory class as shown
Line 576: in the following listing.
Line 577: public class UserFactory
Line 578: {
Line 579: public static User Create(object[] data)
Line 580: {
Line 581: Precondition.Requires(data.Length >= 3);
Line 582: int id = (int)data[0];
Line 583: string email = (string)data[1];
Line 584: UserType type = (UserType)data[2];
Line 585: return new User(id, email, type);
Line 586: }
Line 587: }
Line 588: This code is now fully isolated from all collaborators and therefore easily testable.
Line 589: Notice that I’ve put a safeguard in this method: a requirement to have at least three
Line 590: elements in the data array. Precondition is a simple custom class that throws an
Line 591: exception if the Boolean argument is false. The reason for this class is the more
Line 592: succinct code and the condition inversion: affirmative statements are more read-
Line 593: able than negative ones. In our example, the data.Length >= 3 requirement reads
Line 594: better than
Line 595: if (data.Length < 3)
Line 596: throw new Exception();
Line 597: Note that while this reconstruction logic is somewhat complex, it doesn’t have domain
Line 598: significance: it isn’t directly related to the client’s goal of changing the user email. It’s
Line 599: an example of the utility code I refer to in previous chapters.
Line 600:  
Line 601: Listing 7.3
Line 602: User factory
Line 603: 
Line 604: --- 페이지 186 ---
Line 605: 164
Line 606: CHAPTER 7
Line 607: Refactoring toward valuable unit tests
Line 608: 7.2.5
Line 609: Take 4: Introducing a new Company class
Line 610: Look at this code in the controller once again:
Line 611: object[] companyData = _database.GetCompany();
Line 612: string companyDomainName = (string)companyData[0];
Line 613: int numberOfEmployees = (int)companyData[1];
Line 614: int newNumberOfEmployees = user.ChangeEmail(
Line 615: newEmail, companyDomainName, numberOfEmployees);
Line 616: The awkwardness of returning an updated number of employees from User is a sign
Line 617: of a misplaced responsibility, which itself is a sign of a missing abstraction. To fix this,
Line 618: we need to introduce another domain class, Company, that bundles the company-
Line 619: related logic and data together, as shown in the following listing.
Line 620: public class Company
Line 621: {
Line 622: public string DomainName { get; private set; }
Line 623: public int NumberOfEmployees { get; private set; }
Line 624: public void ChangeNumberOfEmployees(int delta)
Line 625: {
Line 626: Precondition.Requires(NumberOfEmployees + delta >= 0);
Line 627: NumberOfEmployees += delta;
Line 628: }
Line 629: public bool IsEmailCorporate(string email)
Line 630: {
Line 631: string emailDomain = email.Split('@')[1];
Line 632: return emailDomain == DomainName;
Line 633: }
Line 634: }
Line 635: How is the reconstruction logic complex?
Line 636: How is the reconstruction logic complex, given that there’s only a single branching
Line 637: point in the UserFactory.Create() method? As I mentioned in chapter 1, there
Line 638: could be a lot of hidden branching points in the underlying libraries used by the code
Line 639: and thus a lot of potential for something to go wrong. This is exactly the case for the
Line 640: UserFactory.Create() method.
Line 641: Referring to an array element by index (data[0]) entails an internal decision made
Line 642: by the .NET Framework as to what data element to access. The same is true for the
Line 643: conversion from object to int or string. Internally, the .NET Framework decides
Line 644: whether to throw a cast exception or allow the conversion to proceed. All these hid-
Line 645: den branches make the reconstruction logic test-worthy, despite the lack of decision
Line 646: points in it. 
Line 647: Listing 7.4
Line 648: The new class in the domain layer
Line 649: 
Line 650: --- 페이지 187 ---
Line 651: 165
Line 652: Refactoring toward valuable unit tests
Line 653: There are two methods in this class: ChangeNumberOfEmployees() and IsEmail-
Line 654: Corporate(). These methods help adhere to the tell-don’t-ask principle I mentioned
Line 655: in chapter 5. This principle advocates for bundling together data and operations on
Line 656: that data. A User instance will tell the company to change its number of employees or
Line 657: figure out whether a particular email is corporate; it won’t ask for the raw data and do
Line 658: everything on its own.
Line 659:  There’s also a new CompanyFactory class, which is responsible for the reconstruc-
Line 660: tion of Company objects, similar to UserFactory. This is how the controller now looks.
Line 661: public class UserController
Line 662: {
Line 663: private readonly Database _database = new Database();
Line 664: private readonly MessageBus _messageBus = new MessageBus();
Line 665: public void ChangeEmail(int userId, string newEmail)
Line 666: {
Line 667: object[] userData = _database.GetUserById(userId);
Line 668: User user = UserFactory.Create(userData);
Line 669: object[] companyData = _database.GetCompany();
Line 670: Company company = CompanyFactory.Create(companyData);
Line 671: user.ChangeEmail(newEmail, company);
Line 672: _database.SaveCompany(company);
Line 673: _database.SaveUser(user);
Line 674: _messageBus.SendEmailChangedMessage(userId, newEmail);
Line 675: }
Line 676: }
Line 677: And here’s the User class.
Line 678: public class User
Line 679: {
Line 680: public int UserId { get; private set; }
Line 681: public string Email { get; private set; }
Line 682: public UserType Type { get; private set; }
Line 683: public void ChangeEmail(string newEmail, Company company)
Line 684: {
Line 685: if (Email == newEmail)
Line 686: return;
Line 687: UserType newType = company.IsEmailCorporate(newEmail)
Line 688: ? UserType.Employee
Line 689: : UserType.Customer;
Line 690: Listing 7.5
Line 691: Controller after refactoring 
Line 692: Listing 7.6
Line 693: User after refactoring 
Line 694: 
Line 695: --- 페이지 188 ---
Line 696: 166
Line 697: CHAPTER 7
Line 698: Refactoring toward valuable unit tests
Line 699: if (Type != newType)
Line 700: {
Line 701: int delta = newType == UserType.Employee ? 1 : -1;
Line 702: company.ChangeNumberOfEmployees(delta);
Line 703: }
Line 704: Email = newEmail;
Line 705: Type = newType;
Line 706: }
Line 707: }
Line 708: Notice how the removal of the misplaced responsibility made User much cleaner.
Line 709: Instead of operating on company data, it accepts a Company instance and delegates
Line 710: two important pieces of work to that instance: determining whether an email is corpo-
Line 711: rate and changing the number of employees in the company.
Line 712:  Figure 7.9 shows where each class stands in the diagram. The factories and both
Line 713: domain classes reside in the domain model and algorithms quadrant. User has moved
Line 714: to the right because it now has one collaborator, Company, whereas previously it had
Line 715: none. That has made User less testable, but not much.
Line 716: UserController now firmly stands in the controllers quadrant because all of its com-
Line 717: plexity has moved to the factories. The only thing this class is responsible for is gluing
Line 718: together all the collaborating parties.
Line 719: Domain model,
Line 720: algorithms
Line 721: Overcomplicated
Line 722: code
Line 723: Trivial code
Line 724: Controllers
Line 725: Complexity,
Line 726: domain
Line 727: signiﬁcance
Line 728: Number of
Line 729: collaborators
Line 730: UserController
Line 731: User
Line 732: Company,
Line 733: UserFactory,
Line 734: CompanyFactory
Line 735: Figure 7.9
Line 736: User has shifted to the right because it now has the Company 
Line 737: collaborator. UserController firmly stands in the controllers quadrant; all 
Line 738: its complexity has moved to the factories.
Line 739: 
Line 740: --- 페이지 189 ---
Line 741: 167
Line 742: Analysis of optimal unit test coverage
Line 743:  Note the similarities between this implementation and the functional architecture
Line 744: from the previous chapter. Neither the functional core in the audit system nor the
Line 745: domain layer in this CRM (the User and Company classes) communicates with out-of-
Line 746: process dependencies. In both implementations, the application services layer is
Line 747: responsible for such communication: it gets the raw data from the filesystem or from
Line 748: the database, passes that data to stateless algorithms or the domain model, and then
Line 749: persists the results back to the data storage.
Line 750:  The difference between the two implementations is in their treatment of side
Line 751: effects. The functional core doesn’t incur any side effects whatsoever. The CRM’s
Line 752: domain model does, but all those side effects remain inside the domain model in the
Line 753: form of the changed user email and the number of employees. The side effects only
Line 754: cross the domain model’s boundary when the controller persists the User and Company
Line 755: objects in the database.
Line 756:  The fact that all side effects are contained in memory until the very last moment
Line 757: improves testability a lot. Your tests don’t need to examine out-of-process dependen-
Line 758: cies, nor do they need to resort to communication-based testing. All the verification
Line 759: can be done using output-based and state-based testing of objects in memory. 
Line 760: 7.3
Line 761: Analysis of optimal unit test coverage
Line 762: Now that we’ve completed the refactoring with the help of the Humble Object pat-
Line 763: tern, let’s analyze which parts of the project fall into which code category and how
Line 764: those parts should be tested. Table 7.1 shows all the code from the sample project
Line 765: grouped by position in the types-of-code diagram.
Line 766: With the full separation of business logic and orchestration at hand, it’s easy to decide
Line 767: which parts of the code base to unit test.
Line 768: 7.3.1
Line 769: Testing the domain layer and utility code
Line 770: Testing methods in the top-left quadrant in table 7.1 provides the best results in cost-
Line 771: benefit terms. The code’s high complexity or domain significance guarantees great
Line 772: protection against regressions, while having few collaborators ensures the lowest mainte-
Line 773: nance costs. This is an example of how User could be tested:
Line 774: Table 7.1
Line 775: Types of code in the sample project after refactoring using the Humble Object pattern
Line 776: Few collaborators
Line 777: Many collaborators
Line 778: High complexity or 
Line 779: domain significance
Line 780: ChangeEmail(newEmail, company) in User;
Line 781: ChangeNumberOfEmployees(delta) and 
Line 782: IsEmailCorporate(email) in Company; 
Line 783: and Create(data) in UserFactory and 
Line 784: CompanyFactory
Line 785: Low complexity and 
Line 786: domain significance
Line 787: Constructors in User and Company
Line 788: ChangeEmail(userId, 
Line 789: newEmail) in 
Line 790: UserController
Line 791: 
Line 792: --- 페이지 190 ---
Line 793: 168
Line 794: CHAPTER 7
Line 795: Refactoring toward valuable unit tests
Line 796: [Fact]
Line 797: public void Changing_email_from_non_corporate_to_corporate()
Line 798: {
Line 799: var company = new Company("mycorp.com", 1);
Line 800: var sut = new User(1, "user@gmail.com", UserType.Customer);
Line 801: sut.ChangeEmail("new@mycorp.com", company);
Line 802: Assert.Equal(2, company.NumberOfEmployees);
Line 803: Assert.Equal("new@mycorp.com", sut.Email);
Line 804: Assert.Equal(UserType.Employee, sut.Type);
Line 805: }
Line 806: To achieve full coverage, you’d need another three such tests:
Line 807: public void Changing_email_from_corporate_to_non_corporate()
Line 808: public void Changing_email_without_changing_user_type()
Line 809: public void Changing_email_to_the_same_one()
Line 810: Tests for the other three classes would be even shorter, and you could use parameter-
Line 811: ized tests to group several test cases together:
Line 812: [InlineData("mycorp.com", "email@mycorp.com", true)]
Line 813: [InlineData("mycorp.com", "email@gmail.com", false)]
Line 814: [Theory]
Line 815: public void Differentiates_a_corporate_email_from_non_corporate(
Line 816: string domain, string email, bool expectedResult)
Line 817: {
Line 818: var sut = new Company(domain, 0);
Line 819: bool isEmailCorporate = sut.IsEmailCorporate(email);
Line 820: Assert.Equal(expectedResult, isEmailCorporate);
Line 821: }
Line 822: 7.3.2
Line 823: Testing the code from the other three quadrants
Line 824: Code with low complexity and few collaborators (bottom-left quadrant in table 7.1) is
Line 825: represented by the constructors in User and Company, such as
Line 826: public User(int userId, string email, UserType type)
Line 827: {
Line 828: UserId = userId;
Line 829: Email = email;
Line 830: Type = type;
Line 831: }
Line 832: These constructors are trivial and aren’t worth the effort. The resulting tests wouldn’t
Line 833: provide great enough protection against regressions.
Line 834:  The refactoring has eliminated all code with high complexity and a large number
Line 835: of collaborators (top-right quadrant in table 7.1), so we have nothing to test there,
Line 836: either. As for the controllers quadrant (bottom-right in table 7.1), we’ll discuss testing
Line 837: it in the next chapter. 
Line 838: 
Line 839: --- 페이지 191 ---
Line 840: 169
Line 841: Handling conditional logic in controllers
Line 842: 7.3.3
Line 843: Should you test preconditions?
Line 844: Let’s take a look at a special kind of branching points—preconditions—and see whether
Line 845: you should test them. For example, look at this method from Company once again:
Line 846: public void ChangeNumberOfEmployees(int delta)
Line 847: {
Line 848: Precondition.Requires(NumberOfEmployees + delta >= 0);
Line 849: NumberOfEmployees += delta;
Line 850: }
Line 851: It has a precondition stating that the number of employees in the company should
Line 852: never become negative. This precondition is a safeguard that’s activated only in
Line 853: exceptional cases. Such exceptional cases are usually the result of bugs. The only pos-
Line 854: sible reason for the number of employees to go below zero is if there’s an error in
Line 855: code. The safeguard provides a mechanism for your software to fail fast and to prevent
Line 856: the error from spreading and being persisted in the database, where it would be much
Line 857: harder to deal with. Should you test such preconditions? In other words, would such
Line 858: tests be valuable enough to have in the test suite?
Line 859:  There’s no hard rule here, but the general guideline I recommend is to test all pre-
Line 860: conditions that have domain significance. The requirement for the non-negative
Line 861: number of employees is such a precondition. It’s part of the Company class’s invariants:
Line 862: conditions that should be held true at all times. But don’t spend time testing precon-
Line 863: ditions that don’t have domain significance. For example, UserFactory has the follow-
Line 864: ing safeguard in its Create method:
Line 865: public static User Create(object[] data)
Line 866: {
Line 867: Precondition.Requires(data.Length >= 3);
Line 868: /* Extract id, email, and type out of data */
Line 869: }
Line 870: There’s no domain meaning to this precondition and therefore not much value in
Line 871: testing it. 
Line 872: 7.4
Line 873: Handling conditional logic in controllers
Line 874: Handling conditional logic and simultaneously maintaining the domain layer free of
Line 875: out-of-process collaborators is often tricky and involves trade-offs. In this section, I’ll
Line 876: show what those trade-offs are and how to decide which of them to choose in your
Line 877: own project.
Line 878:  The separation between business logic and orchestration works best when a busi-
Line 879: ness operation has three distinct stages:
Line 880: Retrieving data from storage
Line 881: Executing business logic
Line 882: Persisting data back to the storage (figure 7.10)
Line 883: 
Line 884: --- 페이지 192 ---
Line 885: 170
Line 886: CHAPTER 7
Line 887: Refactoring toward valuable unit tests
Line 888: There are a lot of situations where these stages aren’t as clearcut, though. As we discussed
Line 889: in chapter 6, you might need to query additional data from an out-of-process depen-
Line 890: dency based on an intermediate result of the decision-making process (figure 7.11). Writ-
Line 891: ing to the out-of-process dependency often depends on that result, too.
Line 892: As also discussed in the previous chapter, you have three options in such a situation:
Line 893: Push all external reads and writes to the edges anyway. This approach preserves the
Line 894: read-decide-act structure but concedes performance: the controller will call
Line 895: out-of-process dependencies even when there’s no need for that.
Line 896: Inject the out-of-process dependencies into the domain model and allow the business
Line 897: logic to directly decide when to call those dependencies.
Line 898: Split the decision-making process into more granular steps and have the controller act
Line 899: on each of those steps separately.
Line 900: Read
Line 901: Invoke
Line 902: Write
Line 903: Out-of-process
Line 904: dependencies:
Line 905: ﬁlesystem,
Line 906: database, etc.
Line 907: Application
Line 908: service
Line 909: (controller)
Line 910: Business logic
Line 911: (domain
Line 912: model)
Line 913: Figure 7.10
Line 914: Hexagonal and functional architectures work best when all 
Line 915: references to out-of-process dependencies can be pushed to the edges of 
Line 916: business operations.
Line 917: Read
Line 918: Read
Line 919: Invoke 1
Line 920: Write
Line 921: Out-of-process
Line 922: dependencies:
Line 923: ﬁlesystem,
Line 924: database, etc.
Line 925: Application
Line 926: service
Line 927: (controller)
Line 928: Business logic
Line 929: (domain
Line 930: model)
Line 931: Invoke 2
Line 932: Figure 7.11
Line 933: A hexagonal architecture doesn’t work as well when you need to refer to 
Line 934: out-of-process dependencies in the middle of the business operation.
Line 935: 
Line 936: --- 페이지 193 ---
Line 937: 171
Line 938: Handling conditional logic in controllers
Line 939: The challenge is to balance the following three attributes:
Line 940: Domain model testability, which is a function of the number and type of collabora-
Line 941: tors in domain classes
Line 942: Controller simplicity, which depends on the presence of decision-making (branch-
Line 943: ing) points in the controller
Line 944: Performance, as defined by the number of calls to out-of-process dependencies
Line 945: Each option only gives you two out of the three attributes (figure 7.12):
Line 946: Pushing all external reads and writes to the edges of a business operation—Preserves
Line 947: controller simplicity and keeps the domain model isolated from out-of-process
Line 948: dependencies (thus allowing it to remain testable) but concedes performance.
Line 949: Injecting out-of-process dependencies into the domain model—Keeps performance and
Line 950: the controller’s simplicity intact but damages domain model testability.
Line 951: Splitting the decision-making process into more granular steps—Helps with both per-
Line 952: formance and domain model testability but concedes controller simplicity.
Line 953: You’ll need to introduce decision-making points in the controller in order to
Line 954: manage these granular steps.
Line 955: In most software projects, performance is important, so the first approach (pushing
Line 956: external reads and writes to the edges of a business operation) is out of the question.
Line 957: The second option (injecting out-of-process dependencies into the domain model)
Line 958: brings most of your code into the overcomplicated quadrant on the types-of-code dia-
Line 959: gram. This is exactly what we refactored the initial CRM implementation away from. I
Line 960: recommend that you avoid this approach: such code no longer preserves the separation
Line 961: Domain model
Line 962: testability
Line 963: Performance
Line 964: Pushing all external reads
Line 965: and writes to the edges of
Line 966: the business operation
Line 967: Injecting out-of-process
Line 968: dependencies into the
Line 969: domain model
Line 970: Splitting the decision-making
Line 971: process into more granular steps
Line 972: Controller simplicity
Line 973: Figure 7.12
Line 974: There’s no single solution that satisfies all three attributes: controller simplicity, 
Line 975: domain model testability, and performance. You have to choose two out of the three.
Line 976: 
Line 977: --- 페이지 194 ---
Line 978: 172
Line 979: CHAPTER 7
Line 980: Refactoring toward valuable unit tests
Line 981: between business logic and communication with out-of-process dependencies and
Line 982: thus becomes much harder to test and maintain.
Line 983:  That leaves you with the third option: splitting the decision-making process into
Line 984: smaller steps. With this approach, you will have to make your controllers more com-
Line 985: plex, which will also push them closer to the overcomplicated quadrant. But there are
Line 986: ways to mitigate this problem. Although you will rarely be able to factor all the com-
Line 987: plexity out of controllers as we did previously in the sample project, you can keep that
Line 988: complexity manageable.
Line 989: 7.4.1
Line 990: Using the CanExecute/Execute pattern
Line 991: The first way to mitigate the growth of the controllers’ complexity is to use the Can-
Line 992: Execute/Execute pattern, which helps avoid leaking of business logic from the
Line 993: domain model to controllers. This pattern is best explained with an example, so let’s
Line 994: expand on our sample project.
Line 995:  Let’s say that a user can change their email only until they confirm it. If a user tries
Line 996: to change the email after the confirmation, they should be shown an error message.
Line 997: To accommodate this new requirement, we’ll add a new property to the User class.
Line 998: public class User
Line 999: {
Line 1000: public int UserId { get; private set; }
Line 1001: public string Email { get; private set; }
Line 1002: public UserType Type { get; private set; }
Line 1003: public bool IsEmailConfirmed               
Line 1004: { get; private set; }
Line 1005:                
Line 1006: /* ChangeEmail(newEmail, company) method */
Line 1007: }
Line 1008: There are two options for where to put this check. First, you could put it in User’s
Line 1009: ChangeEmail method:
Line 1010: public string ChangeEmail(string newEmail, Company company)
Line 1011: {
Line 1012: if (IsEmailConfirmed)
Line 1013: return "Can't change a confirmed email";
Line 1014: /* the rest of the method */
Line 1015: }
Line 1016: Then you could make the controller either return an error or incur all necessary side
Line 1017: effects, depending on this method’s output.
Line 1018: public string ChangeEmail(int userId, string newEmail)
Line 1019: {
Line 1020: Listing 7.7
Line 1021: User with a new property
Line 1022: Listing 7.8
Line 1023: The controller, still stripped of all decision-making
Line 1024: New property
Line 1025: 
Line 1026: --- 페이지 195 ---
Line 1027: 173
Line 1028: Handling conditional logic in controllers
Line 1029: object[] userData = _database.GetUserById(userId);
Line 1030:   
Line 1031: User user = UserFactory.Create(userData);
Line 1032:   
Line 1033: object[] companyData = _database.GetCompany();
Line 1034:   
Line 1035: Company company = CompanyFactory.Create(companyData);   
Line 1036: string error = user.ChangeEmail(newEmail, company);
Line 1037:      
Line 1038: if (error != null)
Line 1039:     
Line 1040: return error;
Line 1041:      
Line 1042: _database.SaveCompany(company);
Line 1043:       
Line 1044: _database.SaveUser(user);
Line 1045:  
Line 1046: _messageBus.SendEmailChangedMessage(userId, newEmail); 
Line 1047: return "OK";
Line 1048:  
Line 1049: }
Line 1050: This implementation keeps the controller free of decision-making, but it does so at
Line 1051: the expense of a performance drawback. The Company instance is retrieved from the
Line 1052: database unconditionally, even when the email is confirmed and thus can’t be changed.
Line 1053: This is an example of pushing all external reads and writes to the edges of a business
Line 1054: operation.
Line 1055: NOTE
Line 1056: I don’t consider the new if statement analyzing the error string an
Line 1057: increase in complexity because it belongs to the acting phase; it’s not part of
Line 1058: the decision-making process. All the decisions are made by the User class, and
Line 1059: the controller merely acts on those decisions.
Line 1060: The second option is to move the check for IsEmailConfirmed from User to the
Line 1061: controller.
Line 1062: public string ChangeEmail(int userId, string newEmail)
Line 1063: {
Line 1064: object[] userData = _database.GetUserById(userId);
Line 1065: User user = UserFactory.Create(userData);
Line 1066: if (user.IsEmailConfirmed)
Line 1067:    
Line 1068: return "Can't change a confirmed email";  
Line 1069: object[] companyData = _database.GetCompany();
Line 1070: Company company = CompanyFactory.Create(companyData);
Line 1071: user.ChangeEmail(newEmail, company);
Line 1072: _database.SaveCompany(company);
Line 1073: _database.SaveUser(user);
Line 1074: _messageBus.SendEmailChangedMessage(userId, newEmail);
Line 1075: return "OK";
Line 1076: }
Line 1077: Listing 7.9
Line 1078: Controller deciding whether to change the user’s email
Line 1079: Prepares 
Line 1080: the data
Line 1081: Makes a
Line 1082: decision
Line 1083: Acts on the 
Line 1084: decision
Line 1085: Decision-making 
Line 1086: moved here from User.
Line 1087: 
Line 1088: --- 페이지 196 ---
Line 1089: 174
Line 1090: CHAPTER 7
Line 1091: Refactoring toward valuable unit tests
Line 1092: With this implementation, the performance stays intact: the Company instance is
Line 1093: retrieved from the database only after it is certain that the email can be changed. But
Line 1094: now the decision-making process is split into two parts:
Line 1095: Whether to proceed with the change of email (performed by the controller)
Line 1096: What to do during that change (performed by User)
Line 1097: Now it’s also possible to change the email without verifying the IsEmailConfirmed
Line 1098: flag first, which diminishes the domain model’s encapsulation. Such fragmentation
Line 1099: hinders the separation between business logic and orchestration and moves the con-
Line 1100: troller closer to the overcomplicated danger zone.
Line 1101:  To prevent this fragmentation, you can introduce a new method in User, CanChange-
Line 1102: Email(), and make its successful execution a precondition for changing an email. The
Line 1103: modified version in the following listing follows the CanExecute/Execute pattern.
Line 1104: public string CanChangeEmail()
Line 1105: {
Line 1106: if (IsEmailConfirmed)
Line 1107: return "Can't change a confirmed email";
Line 1108: return null;
Line 1109: }
Line 1110: public void ChangeEmail(string newEmail, Company company)
Line 1111: {
Line 1112: Precondition.Requires(CanChangeEmail() == null);
Line 1113: /* the rest of the method */
Line 1114: }
Line 1115: This approach provides two important benefits:
Line 1116: The controller no longer needs to know anything about the process of chang-
Line 1117: ing emails. All it needs to do is call the CanChangeEmail() method to see if the
Line 1118: operation can be done. Notice that this method can contain multiple valida-
Line 1119: tions, all encapsulated away from the controller.
Line 1120: The additional precondition in ChangeEmail() guarantees that the email won’t
Line 1121: ever be changed without checking for the confirmation first.
Line 1122: This pattern helps you to consolidate all decisions in the domain layer. The controller
Line 1123: no longer has an option not to check for the email confirmation, which essentially
Line 1124: eliminates the new decision-making point from that controller. Thus, although the
Line 1125: controller still contains the if statement calling CanChangeEmail(), you don’t need to
Line 1126: test that if statement. Unit testing the precondition in the User class itself is enough.
Line 1127: NOTE
Line 1128: For simplicity’s sake, I’m using a string to denote an error. In a real-
Line 1129: world project, you may want to introduce a custom Result class to indicate
Line 1130: the success or failure of an operation. 
Line 1131: Listing 7.10
Line 1132: Changing an email using the CanExecute/Execute pattern
Line 1133: 
Line 1134: --- 페이지 197 ---
Line 1135: 175
Line 1136: Handling conditional logic in controllers
Line 1137: 7.4.2
Line 1138: Using domain events to track changes in the domain model
Line 1139: It’s sometimes hard to deduct what steps led the domain model to the current state.
Line 1140: Still, it might be important to know these steps because you need to inform external
Line 1141: systems about what exactly has happened in your application. Putting this responsibil-
Line 1142: ity on the controllers would make them more complicated. To avoid that, you can
Line 1143: track important changes in the domain model and then convert those changes into
Line 1144: calls to out-of-process dependencies after the business operation is complete. Domain
Line 1145: events help you implement such tracking.
Line 1146: DEFINITION
Line 1147: A domain event describes an event in the application that is mean-
Line 1148: ingful to domain experts. The meaningfulness for domain experts is what
Line 1149: differentiates domain events from regular events (such as button clicks).
Line 1150: Domain events are often used to inform external applications about import-
Line 1151: ant changes that have happened in your system.
Line 1152: Our CRM has a tracking requirement, too: it has to notify external systems about
Line 1153: changed user emails by sending messages to the message bus. The current implemen-
Line 1154: tation has a flaw in the notification functionality: it sends messages even when the
Line 1155: email is not changed, as shown in the following listing.
Line 1156: // User
Line 1157: public void ChangeEmail(string newEmail, Company company)
Line 1158: {
Line 1159: Precondition.Requires(CanChangeEmail() == null);
Line 1160: if (Email == newEmail)   
Line 1161: return;
Line 1162: /* the rest of the method */
Line 1163: }
Line 1164: // Controller
Line 1165: public string ChangeEmail(int userId, string newEmail)
Line 1166: {
Line 1167: /* preparations */
Line 1168: user.ChangeEmail(newEmail, company);
Line 1169: _database.SaveCompany(company);
Line 1170: _database.SaveUser(user);
Line 1171: _messageBus.SendEmailChangedMessage(  
Line 1172: userId, newEmail);
Line 1173:   
Line 1174: return "OK";
Line 1175: }
Line 1176: You could resolve this bug by moving the check for email sameness to the controller,
Line 1177: but then again, there are issues with the business logic fragmentation. And you can’t
Line 1178: Listing 7.11
Line 1179: Sends a notification even when the email has not changed
Line 1180: User email may 
Line 1181: not change.
Line 1182: The controller sends 
Line 1183: a message anyway.
Line 1184: 
Line 1185: --- 페이지 198 ---
Line 1186: 176
Line 1187: CHAPTER 7
Line 1188: Refactoring toward valuable unit tests
Line 1189: put this check to CanChangeEmail() because the application shouldn’t return an
Line 1190: error if the new email is the same as the old one.
Line 1191:  Note that this particular check probably doesn’t introduce too much business logic
Line 1192: fragmentation, so I personally wouldn’t consider the controller overcomplicated if it
Line 1193: contained that check. But you may find yourself in a more difficult situation in which
Line 1194: it’s hard to prevent your application from making unnecessary calls to out-of-process
Line 1195: dependencies without passing those dependencies to the domain model, thus over-
Line 1196: complicating that domain model. The only way to prevent such overcomplication is
Line 1197: the use of domain events.
Line 1198:  From an implementation standpoint, a domain event is a class that contains data
Line 1199: needed to notify external systems. In our specific example, it is the user’s ID and
Line 1200: email:
Line 1201: public class EmailChangedEvent
Line 1202: {
Line 1203: public int UserId { get; }
Line 1204: public string NewEmail { get; }
Line 1205: }
Line 1206: NOTE
Line 1207: Domain events should always be named in the past tense because they
Line 1208: represent things that already happened. Domain events are values—they are
Line 1209: immutable and interchangeable.
Line 1210: User will have a collection of such events to which it will add a new element when the
Line 1211: email changes. This is how its ChangeEmail() method looks after the refactoring.
Line 1212: public void ChangeEmail(string newEmail, Company company)
Line 1213: {
Line 1214: Precondition.Requires(CanChangeEmail() == null);
Line 1215: if (Email == newEmail)
Line 1216: return;
Line 1217: UserType newType = company.IsEmailCorporate(newEmail)
Line 1218: ? UserType.Employee
Line 1219: : UserType.Customer;
Line 1220: if (Type != newType)
Line 1221: {
Line 1222: int delta = newType == UserType.Employee ? 1 : -1;
Line 1223: company.ChangeNumberOfEmployees(delta);
Line 1224: }
Line 1225: Email = newEmail;
Line 1226: Type = newType;
Line 1227: EmailChangedEvents.Add(
Line 1228:   
Line 1229: new EmailChangedEvent(UserId, newEmail));  
Line 1230: }
Line 1231: Listing 7.12
Line 1232: User adding an event when the email changes
Line 1233: A new event indicates 
Line 1234: the change of email.
Line 1235: 
Line 1236: --- 페이지 199 ---
Line 1237: 177
Line 1238: Handling conditional logic in controllers
Line 1239: The controller then will convert the events into messages on the bus.
Line 1240: public string ChangeEmail(int userId, string newEmail)
Line 1241: {
Line 1242: object[] userData = _database.GetUserById(userId);
Line 1243: User user = UserFactory.Create(userData);
Line 1244: string error = user.CanChangeEmail();
Line 1245: if (error != null)
Line 1246: return error;
Line 1247: object[] companyData = _database.GetCompany();
Line 1248: Company company = CompanyFactory.Create(companyData);
Line 1249: user.ChangeEmail(newEmail, company);
Line 1250: _database.SaveCompany(company);
Line 1251: _database.SaveUser(user);
Line 1252: foreach (var ev in user.EmailChangedEvents)  
Line 1253: {
Line 1254:   
Line 1255: _messageBus.SendEmailChangedMessage(
Line 1256:   
Line 1257: ev.UserId, ev.NewEmail);
Line 1258:   
Line 1259: }
Line 1260:   
Line 1261: return "OK";
Line 1262: }
Line 1263: Notice that the Company and User instances are still persisted in the database uncondi-
Line 1264: tionally: the persistence logic doesn’t depend on domain events. This is due to the dif-
Line 1265: ference between changes in the database and messages in the bus.
Line 1266:  Assuming that no application has access to the database other than the CRM, com-
Line 1267: munications with that database are not part of the CRM’s observable behavior—they
Line 1268: are implementation details. As long as the final state of the database is correct, it
Line 1269: doesn’t matter how many calls your application makes to that database. On the other
Line 1270: hand, communications with the message bus are part of the application’s observable
Line 1271: behavior. In order to maintain the contract with external systems, the CRM should put
Line 1272: messages on the bus only when the email changes.
Line 1273:  There are performance implications to persisting data in the database uncondi-
Line 1274: tionally, but they are relatively insignificant. The chances that after all the validations
Line 1275: the new email is the same as the old one are quite small. The use of an ORM can also
Line 1276: help. Most ORMs won’t make a round trip to the database if there are no changes to
Line 1277: the object state.
Line 1278:  You can generalize the solution with domain events: extract a DomainEvent base
Line 1279: class and introduce a base class for all domain classes, which would contain a collec-
Line 1280: tion of such events: List<DomainEvent> events. You can also write a separate event
Line 1281: dispatcher instead of dispatching domain events manually in controllers. Finally, in
Line 1282: larger projects, you might need a mechanism for merging domain events before
Line 1283: Listing 7.13
Line 1284: The controller processing domain events
Line 1285: Domain event 
Line 1286: processing
Line 1287: 
Line 1288: --- 페이지 200 ---
Line 1289: 178
Line 1290: CHAPTER 7
Line 1291: Refactoring toward valuable unit tests
Line 1292: dispatching them. That topic is outside the scope of this book, though. You can read
Line 1293: about it in my article “Merging domain events before dispatching” at http://mng
Line 1294: .bz/YeVe.
Line 1295:  Domain events remove the decision-making responsibility from the controller and
Line 1296: put that responsibility into the domain model, thus simplifying unit testing communi-
Line 1297: cations with external systems. Instead of verifying the controller itself and using mocks
Line 1298: to substitute out-of-process dependencies, you can test the domain event creation
Line 1299: directly in unit tests, as shown next.
Line 1300: [Fact]
Line 1301: public void Changing_email_from_corporate_to_non_corporate()
Line 1302: {
Line 1303: var company = new Company("mycorp.com", 1);
Line 1304: var sut = new User(1, "user@mycorp.com", UserType.Employee, false);
Line 1305: sut.ChangeEmail("new@gmail.com", company);
Line 1306: company.NumberOfEmployees.Should().Be(0);
Line 1307: sut.Email.Should().Be("new@gmail.com");
Line 1308: sut.Type.Should().Be(UserType.Customer);
Line 1309: sut.EmailChangedEvents.Should().Equal(
Line 1310:    
Line 1311: new EmailChangedEvent(1, "new@gmail.com"));  
Line 1312: }
Line 1313: Of course, you’ll still need to test the controller to make sure it does the orchestration
Line 1314: correctly, but doing so requires a much smaller set of tests. That’s the topic of the next
Line 1315: chapter. 
Line 1316: 7.5
Line 1317: Conclusion
Line 1318: Notice a theme that has been present throughout this chapter: abstracting away the
Line 1319: application of side effects to external systems. You achieve such abstraction by keeping
Line 1320: those side effects in memory until the very end of the business operation, so that they
Line 1321: can be tested with plain unit tests without involving out-of-process dependencies.
Line 1322: Domain events are abstractions on top of upcoming messages in the bus. Changes in
Line 1323: domain classes are abstractions on top of upcoming modifications in the database.
Line 1324: NOTE
Line 1325: It’s easier to test abstractions than the things they abstract.
Line 1326: Although we were able to successfully contain all the decision-making in the domain
Line 1327: model with the help of domain events and the CanExecute/Execute pattern, you
Line 1328: won’t be able to always do that. There are situations where business logic fragmenta-
Line 1329: tion is inevitable.
Line 1330:  For example, there’s no way to verify email uniqueness outside the controller with-
Line 1331: out introducing out-of-process dependencies in the domain model. Another example
Line 1332: is failures in out-of-process dependencies that should alter the course of the business
Line 1333: Listing 7.14
Line 1334: Testing the creation of a domain event
Line 1335: Simultaneously asserts 
Line 1336: the collection size and the 
Line 1337: element in the collection
Line 1338: 
Line 1339: --- 페이지 201 ---
Line 1340: 179
Line 1341: Conclusion
Line 1342: operation. The decision about which way to go can’t reside in the domain layer
Line 1343: because it’s not the domain layer that calls those out-of-process dependencies. You will
Line 1344: have to put this logic into controllers and then cover it with integration tests. Still,
Line 1345: even with the potential fragmentation, there’s a lot of value in separating business
Line 1346: logic from orchestration because this separation drastically simplifies the unit test-
Line 1347: ing process.
Line 1348:  Just as you can’t avoid having some business logic in controllers, you will rarely be
Line 1349: able to remove all collaborators from domain classes. And that’s fine. One, two, or
Line 1350: even three collaborators won’t turn a domain class into overcomplicated code, as long
Line 1351: as these collaborators don’t refer to out-of-process dependencies.
Line 1352:  Don’t use mocks to verify interactions with such collaborators, though. These
Line 1353: interactions have nothing to do with the domain model’s observable behavior. Only
Line 1354: the very first call, which goes from a controller to a domain class, has an immediate
Line 1355: connection to that controller’s goal. All the subsequent calls the domain class
Line 1356: makes to its neighbor domain classes within the same operation are implementa-
Line 1357: tion details.
Line 1358:  Figure 7.13 illustrates this idea. It shows the communications between components
Line 1359: in the CRM and their relationship to observable behavior. As you may remember from
Line 1360: chapter 5, whether a method is part of the class’s observable behavior depends on
Line 1361: whom the client is and what the goals of that client are. To be part of the observable
Line 1362: behavior, the method must meet one of the following two criteria:
Line 1363: Have an immediate connection to one of the client’s goals
Line 1364: Incur a side effect in an out-of-process dependency that is visible to external
Line 1365: applications
Line 1366: The controller’s ChangeEmail() method is part of its observable behavior, and so is
Line 1367: the call it makes to the message bus. The first method is the entry point for the exter-
Line 1368: nal client, thereby meeting the first criterion. The call to the bus sends messages to
Line 1369: external applications, thereby meeting the second criterion. You should verify both of
Line 1370: External client
Line 1371: Application
Line 1372: service
Line 1373: (controller)
Line 1374: Message bus
Line 1375: User
Line 1376: Company
Line 1377: Observable behavior
Line 1378: for external client
Line 1379: Observable behavior
Line 1380: for controller
Line 1381: Observable
Line 1382: behavior for user
Line 1383: Figure 7.13
Line 1384: A map that shows communications among components in the CRM and the 
Line 1385: relationship between these communications and observable behavior
Line 1386: 
Line 1387: --- 페이지 202 ---
Line 1388: 180
Line 1389: CHAPTER 7
Line 1390: Refactoring toward valuable unit tests
Line 1391: these method calls (which is the topic of the next chapter). However, the subsequent
Line 1392: call from the controller to User doesn’t have an immediate connection to the goals of
Line 1393: the external client. That client doesn’t care how the controller decides to implement
Line 1394: the change of email as long as the final state of the system is correct and the call to the
Line 1395: message bus is in place. Therefore, you shouldn’t verify calls the controller makes to
Line 1396: User when testing that controller’s behavior.
Line 1397:  When you step one level down the call stack, you get a similar situation. Now it’s
Line 1398: the controller who is the client, and the ChangeEmail method in User has an immedi-
Line 1399: ate connection to that client’s goal of changing the user email and thus should be
Line 1400: tested. But the subsequent calls from User to Company are implementation details
Line 1401: from the controller’s point of view. Therefore, the test that covers the ChangeEmail
Line 1402: method in User shouldn’t verify what methods User calls on Company. The same line
Line 1403: of reasoning applies when you step one more level down and test the two methods in
Line 1404: Company from User’s point of view.
Line 1405:  Think of the observable behavior and implementation details as onion layers. Test
Line 1406: each layer from the outer layer’s point of view, and disregard how that layer talks to
Line 1407: the underlying layers. As you peel these layers one by one, you switch perspective:
Line 1408: what previously was an implementation detail now becomes an observable behavior,
Line 1409: which you then cover with another set of tests. 
Line 1410: Summary
Line 1411: Code complexity is defined by the number of decision-making points in the
Line 1412: code, both explicit (made by the code itself) and implicit (made by the libraries
Line 1413: the code uses).
Line 1414: Domain significance shows how significant the code is for the problem domain
Line 1415: of your project. Complex code often has high domain significance and vice
Line 1416: versa, but not in 100% of all cases.
Line 1417: Complex code and code that has domain significance benefit from unit test-
Line 1418: ing the most because the corresponding tests have greater protection against
Line 1419: regressions.
Line 1420: Unit tests that cover code with a large number of collaborators have high
Line 1421: maintenance costs. Such tests require a lot of space to bring collaborators to
Line 1422: an expected condition and then check their state or interactions with them
Line 1423: afterward.
Line 1424: All production code can be categorized into four types of code by its complexity
Line 1425: or domain significance and the number of collaborators:
Line 1426: – Domain model and algorithms (high complexity or domain significance, few
Line 1427: collaborators) provide the best return on unit testing efforts.
Line 1428: – Trivial code (low complexity and domain significance, few collaborators)
Line 1429: isn’t worth testing at all.
Line 1430: 
Line 1431: --- 페이지 203 ---
Line 1432: 181
Line 1433: Summary
Line 1434: – Controllers (low complexity and domain significance, large number of col-
Line 1435: laborators) should be tested briefly by integration tests.
Line 1436: – Overcomplicated code (high complexity or domain significance, large num-
Line 1437: ber of collaborators) should be split into controllers and complex code.
Line 1438: The more important or complex the code is, the fewer collaborators it should
Line 1439: have.
Line 1440: The Humble Object pattern helps make overcomplicated code testable by
Line 1441: extracting business logic out of that code into a separate class. As a result, the
Line 1442: remaining code becomes a controller—a thin, humble wrapper around the busi-
Line 1443: ness logic.
Line 1444: The hexagonal and functional architectures implement the Humble Object
Line 1445: pattern. Hexagonal architecture advocates for the separation of business logic and
Line 1446: communications with out-of-process dependencies. Functional architecture sepa-
Line 1447: rates business logic from communications with all collaborators, not just out-of-
Line 1448: process ones.
Line 1449: Think of the business logic and orchestration responsibilities in terms of code
Line 1450: depth versus code width. Your code can be either deep (complex or important)
Line 1451: or wide (work with many collaborators), but never both.
Line 1452: Test preconditions if they have a domain significance; don’t test them otherwise.
Line 1453: There are three important attributes when it comes to separating business logic
Line 1454: from orchestration:
Line 1455: – Domain model testability—A function of the number and the type of collabora-
Line 1456: tors in domain classes
Line 1457: – Controller simplicity—Depends on the presence of decision-making points in
Line 1458: the controller
Line 1459: – Performance—Defined by the number of calls to out-of-process dependencies
Line 1460: You can have a maximum of two of these three attributes at any given moment:
Line 1461: – Pushing all external reads and writes to the edges of a business operation—Preserves
Line 1462: controller simplicity and keeps the domain model testability, but concedes
Line 1463: performance
Line 1464: – Injecting out-of-process dependencies into the domain model—Keeps performance
Line 1465: and the controller’s simplicity, but damages domain model testability
Line 1466: – Splitting the decision-making process into more granular steps—Preserves perfor-
Line 1467: mance and domain model testability, but gives up controller simplicity
Line 1468: Splitting the decision-making process into more granular steps—Is a trade-off with the
Line 1469: best set of pros and cons. You can mitigate the growth of controller complexity
Line 1470: using the following two patterns:
Line 1471: – The CanExecute/Execute pattern introduces a CanDo() for each Do() method
Line 1472: and makes its successful execution a precondition for Do(). This pattern
Line 1473: essentially eliminates the controller’s decision-making because there’s no
Line 1474: option not to call CanDo() before Do().
Line 1475: 
Line 1476: --- 페이지 204 ---
Line 1477: 182
Line 1478: CHAPTER 7
Line 1479: Refactoring toward valuable unit tests
Line 1480: – Domain events help track important changes in the domain model, and then
Line 1481: convert those changes to calls to out-of-process dependencies. This pattern
Line 1482: removes the tracking responsibility from the controller.
Line 1483: It’s easier to test abstractions than the things they abstract. Domain events are
Line 1484: abstractions on top of upcoming calls to out-of-process dependencies. Changes
Line 1485: in domain classes are abstractions on top of upcoming modifications in the
Line 1486: data storage.
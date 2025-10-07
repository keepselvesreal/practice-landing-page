Line 1: 
Line 2: --- 페이지 207 ---
Line 3: 185
Line 4: Why integration testing?
Line 5: You can never be sure your system works as a whole if you rely on unit tests exclu-
Line 6: sively. Unit tests are great at verifying business logic, but it’s not enough to check
Line 7: that logic in a vacuum. You have to validate how different parts of it integrate with
Line 8: each other and external systems: the database, the message bus, and so on.
Line 9:  In this chapter, you’ll learn the role of integration tests: when you should apply
Line 10: them and when it’s better to rely on plain old unit tests or even other techniques
Line 11: such as the Fail Fast principle. You will see which out-of-process dependencies to
Line 12: use as-is in integration tests and which to replace with mocks. You will also see inte-
Line 13: gration testing best practices that will help improve the health of your code base in
Line 14: general: making domain model boundaries explicit, reducing the number of layers
Line 15: in the application, and eliminating circular dependencies. Finally, you’ll learn why
Line 16: interfaces with a single implementation should be used sporadically, and how and
Line 17: when to test logging functionality.
Line 18: This chapter covers
Line 19: Understanding the role of integration testing
Line 20: Diving deeper into the Test Pyramid concept
Line 21: Writing valuable integration tests
Line 22: 
Line 23: --- 페이지 208 ---
Line 24: 186
Line 25: CHAPTER 8
Line 26: Why integration testing?
Line 27: 8.1
Line 28: What is an integration test?
Line 29: Integration tests play an important role in your test suite. It’s also crucial to balance
Line 30: the number of unit and integration tests. You will see shortly what that role is and how
Line 31: to maintain the balance, but first, let me give you a refresher on what differentiates an
Line 32: integration test from a unit test.
Line 33: 8.1.1
Line 34: The role of integration tests
Line 35: As you may remember from chapter 2, a unit test is a test that meets the following three
Line 36: requirements:
Line 37: Verifies a single unit of behavior,
Line 38: Does it quickly,
Line 39: And does it in isolation from other tests.
Line 40: A test that doesn’t meet at least one of these three requirements falls into the category
Line 41: of integration tests. An integration test then is any test that is not a unit test.
Line 42:  In practice, integration tests almost always verify how your system works in integra-
Line 43: tion with out-of-process dependencies. In other words, these tests cover the code from
Line 44: the controllers quadrant (see chapter 7 for more details about code quadrants). The
Line 45: diagram in figure 8.1 shows the typical responsibilities of unit and integration tests.
Line 46: Unit tests cover the domain model, while integration tests check the code that glues
Line 47: that domain model with out-of-process dependencies.
Line 48: Domain model,
Line 49: algorithms
Line 50: Overcomplicated
Line 51: code
Line 52: Trivial code
Line 53: Controllers
Line 54: Complexity,
Line 55: domain
Line 56: signiﬁcance
Line 57: Number of
Line 58: collaborators
Line 59: Integration
Line 60: tests
Line 61: Unit tests
Line 62: Figure 8.1
Line 63: Integration tests cover controllers, while unit tests cover the domain 
Line 64: model and algorithms. Trivial and overcomplicated code shouldn’t be tested at all.
Line 65: 
Line 66: --- 페이지 209 ---
Line 67: 187
Line 68: What is an integration test?
Line 69: Note that tests covering the controllers quadrant can sometimes be unit tests too. If all
Line 70: out-of-process dependencies are replaced with mocks, there will be no dependencies
Line 71: shared between tests, which will allow those tests to remain fast and maintain their iso-
Line 72: lation from each other. Most applications do have an out-of-process dependency that
Line 73: can’t be replaced with a mock, though. It’s usually a database—a dependency that is
Line 74: not visible to other applications.
Line 75:  As you may also remember from chapter 7, the other two quadrants from figure 8.1
Line 76: (trivial code and overcomplicated code) shouldn’t be tested at all. Trivial code isn’t
Line 77: worth the effort, while overcomplicated code should be refactored into algorithms
Line 78: and controllers. Thus, all your tests must focus on the domain model and the control-
Line 79: lers quadrants exclusively. 
Line 80: 8.1.2
Line 81: The Test Pyramid revisited
Line 82: It’s important to maintain a balance between unit and integration tests. Working
Line 83: directly with out-of-process dependencies makes integration tests slow. Such tests are
Line 84: also more expensive to maintain. The increase in maintainability costs is due to
Line 85: The necessity to keep the out-of-process dependencies operational
Line 86: The greater number of collaborators involved, which inflates the test’s size
Line 87: On the other hand, integration tests go through a larger amount of code (both your
Line 88: code and the code of the libraries used by the application), which makes them better
Line 89: than unit tests at protecting against regressions. They are also more detached from
Line 90: the production code and therefore have better resistance to refactoring.
Line 91:  The ratio between unit and integration tests can differ depending on the project’s
Line 92: specifics, but the general rule of thumb is the following: check as many of the business
Line 93: scenario’s edge cases as possible with unit tests; use integration tests to cover one
Line 94: happy path, as well as any edge cases that can’t be covered by unit tests.
Line 95: DEFINITION
Line 96: A happy path is a successful execution of a business scenario. An
Line 97: edge case is when the business scenario execution results in an error.
Line 98: Shifting the majority of the workload to unit tests helps keep maintenance costs low.
Line 99: At the same time, having one or two overarching integration tests per business sce-
Line 100: nario ensures the correctness of your system as a whole. This guideline forms the pyr-
Line 101: amid-like ratio between unit and integration tests, as shown in figure 8.2 (as discussed
Line 102: in chapter 2, end-to-end tests are a subset of integration tests).
Line 103:  The Test Pyramid can take different shapes depending on the project’s complexity.
Line 104: Simple applications have little (if any) code in the domain model and algorithms
Line 105: quadrant. As a result, tests form a rectangle instead of a pyramid, with an equal num-
Line 106: ber of unit and integration tests (figure 8.3). In the most trivial cases, you might have
Line 107: no unit tests whatsoever.
Line 108:  Note that integration tests retain their value even in simple applications. Regard-
Line 109: less of how simple your code is, it’s still important to verify how it works in integration
Line 110: with other subsystems. 
Line 111: 
Line 112: --- 페이지 210 ---
Line 113: 188
Line 114: CHAPTER 8
Line 115: Why integration testing?
Line 116: 8.1.3
Line 117: Integration testing vs. failing fast
Line 118: This section elaborates on the guideline of using integration tests to cover one happy
Line 119: path per business scenario and any edge cases that can’t be covered by unit tests. 
Line 120:  For an integration test, select the longest happy path in order to verify interactions
Line 121: with all out-of-process dependencies. If there’s no one path that goes through all such
Line 122: interactions, write additional integration tests—as many as needed to capture commu-
Line 123: nications with every external system.
Line 124:  As with the edge cases that can’t be covered by unit tests, there are exceptions to
Line 125: this part of the guideline, too. There’s no need to test an edge case if an incorrect
Line 126: execution of that edge case immediately fails the entire application. For example, you
Line 127: saw in chapter 7 how User from the sample CRM system implemented a CanChange-
Line 128: Email method and made its successful execution a precondition for ChangeEmail():
Line 129: End-
Line 130: to-end
Line 131: Integration
Line 132: tests
Line 133: Unit tests
Line 134: Test count
Line 135: Protection against
Line 136: regressions,
Line 137: resistance to
Line 138: refactoring
Line 139: Fast feedback,
Line 140: maintainability
Line 141: Figure 8.2
Line 142: The Test Pyramid represents a trade-off that works best for most 
Line 143: applications. Fast, cheap unit tests cover the majority of edge cases, while a 
Line 144: smaller number of slow, more expensive integration tests ensure the correctness 
Line 145: of the system as a whole.
Line 146: Figure 8.3
Line 147: The Test Pyramid of a simple project. 
Line 148: Little complexity requires a smaller number of unit 
Line 149: tests compared to a normal pyramid.
Line 150: Unit tests
Line 151: Integration tests
Line 152: 
Line 153: --- 페이지 211 ---
Line 154: 189
Line 155: What is an integration test?
Line 156: public void ChangeEmail(string newEmail, Company company)
Line 157: {
Line 158: Precondition.Requires(CanChangeEmail() == null);
Line 159: /* the rest of the method */
Line 160: }
Line 161: The controller invokes CanChangeEmail() and interrupts the operation if that
Line 162: method returns an error:
Line 163: // UserController
Line 164: public string ChangeEmail(int userId, string newEmail)
Line 165: {
Line 166: object[] userData = _database.GetUserById(userId);
Line 167: User user = UserFactory.Create(userData);
Line 168: string error = user.CanChangeEmail();
Line 169: if (error != null)                    
Line 170: return error;                     
Line 171: /* the rest of the method */
Line 172: }
Line 173: This example shows the edge case you could theoretically cover with an integration
Line 174: test. Such a test doesn’t provide a significant enough value, though. If the controller
Line 175: tries to change the email without consulting with CanChangeEmail() first, the applica-
Line 176: tion crashes. This bug reveals itself with the first execution and thus is easy to notice
Line 177: and fix. It also doesn’t lead to data corruption.
Line 178: TIP
Line 179: It’s better to not write a test at all than to write a bad test. A test that
Line 180: doesn’t provide significant value is a bad test.
Line 181: Unlike the call from the controller to CanChangeEmail(), the presence of the precon-
Line 182: dition in User should be tested. But that is better done with a unit test; there’s no need
Line 183: for an integration test.
Line 184:  Making bugs manifest themselves quickly is called the Fail Fast principle, and it’s a
Line 185: viable alternative to integration testing.
Line 186: The Fail Fast principle 
Line 187: The Fail Fast principle stands for stopping the current operation as soon as any unex-
Line 188: pected error occurs. This principle makes your application more stable by
Line 189: Shortening the feedback loop—The sooner you detect a bug, the easier it is
Line 190: to fix. A bug that is already in production is orders of magnitude more expen-
Line 191: sive to fix compared to a bug found during development.
Line 192: Protecting the persistence state—Bugs lead to corruption of the application’s
Line 193: state. Once that state penetrates into the database, it becomes much harder
Line 194: to fix. Failing fast helps you prevent the corruption from spreading.
Line 195: Edge case
Line 196: 
Line 197: --- 페이지 212 ---
Line 198: 190
Line 199: CHAPTER 8
Line 200: Why integration testing?
Line 201: 8.2
Line 202: Which out-of-process dependencies to test directly
Line 203: As I mentioned earlier, integration tests verify how your system integrates with out-of-
Line 204: process dependencies. There are two ways to implement such verification: use the real
Line 205: out-of-process dependency, or replace that dependency with a mock. This section
Line 206: shows when to apply each of the two approaches.
Line 207: 8.2.1
Line 208: The two types of out-of-process dependencies
Line 209: All out-of-process dependencies fall into two categories:
Line 210: Managed dependencies (out-of-process dependencies you have full control over)—These
Line 211: dependencies are only accessible through your application; interactions with
Line 212: them aren’t visible to the external world. A typical example is a database. Exter-
Line 213: nal systems normally don’t access your database directly; they do that through
Line 214: the API your application provides.
Line 215: Unmanaged dependencies (out-of-process dependencies you don’t have full control over)—
Line 216: Interactions with such dependencies are observable externally. Examples include
Line 217: an SMTP server and a message bus: both produce side effects visible to other
Line 218: applications.
Line 219: I mentioned in chapter 5 that communications with managed dependencies are
Line 220: implementation details. Conversely, communications with unmanaged dependencies
Line 221: are part of your system’s observable behavior (figure 8.4). This distinction leads to the
Line 222: difference in treatment of out-of-process dependencies in integration tests.
Line 223: IMPORTANT
Line 224: Use real instances of managed dependencies; replace unman-
Line 225: aged dependencies with mocks.
Line 226: As discussed in chapter 5, the requirement to preserve the communication pattern
Line 227: with unmanaged dependencies stems from the necessity to maintain backward com-
Line 228: patibility with those dependencies. Mocks are perfect for this task. With mocks, you
Line 229: can ensure communication pattern permanence in light of any possible refactorings.
Line 230: (continued)
Line 231: Stopping the current operation is normally done by throwing exceptions, because
Line 232: exceptions have semantics that are perfectly suited for the Fail Fast principle: they
Line 233: interrupt the program flow and pop up to the highest level of the execution stack,
Line 234: where you can log them and shut down or restart the operation.
Line 235: Preconditions are one example of the Fail Fast principle in action. A failing precondi-
Line 236: tion signifies an incorrect assumption made about the application state, which is
Line 237: always a bug. Another example is reading data from a configuration file. You can
Line 238: arrange the reading logic such that it will throw an exception if the data in the config-
Line 239: uration file is incomplete or incorrect. You can also put this logic close to the appli-
Line 240: cation startup, so that the application doesn’t launch if there’s a problem with its
Line 241: configuration. 
Line 242: 
Line 243: --- 페이지 213 ---
Line 244: 191
Line 245: Which out-of-process dependencies to test directly
Line 246: However, there’s no need to maintain backward compatibility in communications with
Line 247: managed dependencies, because your application is the only one that talks to them.
Line 248: External clients don’t care how you organize your database; the only thing that mat-
Line 249: ters is the final state of your system. Using real instances of managed dependencies in
Line 250: integration tests helps you verify that final state from the external client’s point of
Line 251: view. It also helps during database refactorings, such as renaming a column or even
Line 252: migrating from one database to another. 
Line 253: 8.2.2
Line 254: Working with both managed and unmanaged dependencies
Line 255: Sometimes you’ll encounter an out-of-process dependency that exhibits attributes of
Line 256: both managed and unmanaged dependencies. A good example is a database that
Line 257: other applications have access to.
Line 258:  The story usually goes like this. A system begins with its own dedicated database. After
Line 259: a while, another system begins to require data from the same database. And so the team
Line 260: decides to share access to a limited number of tables just for ease of integration with that
Line 261: other system. As a result, the database becomes a dependency that is both managed and
Line 262: unmanaged. It still contains parts that are visible to your application only; but, in addi-
Line 263: tion to those parts, it also has a number of tables accessible by other applications.
Line 264:  The use of a database is a poor way to implement integration between systems
Line 265: because it couples these systems to each other and complicates their further develop-
Line 266: ment. Only resort to this approach when all other options are exhausted. A better way
Line 267: to do the integration is via an API (for synchronous communications) or a message
Line 268: bus (for asynchronous communications).
Line 269:  But what do you do when you already have a shared database and can’t do any-
Line 270: thing about it in the foreseeable future? In this case, treat tables that are visible to
Line 271: SMTP service
Line 272: (unmanaged
Line 273: dependency)
Line 274: Observable behavior (contract)
Line 275: Implementation details
Line 276: Application
Line 277: database
Line 278: (managed
Line 279: dependency)
Line 280: Third-party
Line 281: system
Line 282: (external
Line 283: client)
Line 284: Figure 8.4
Line 285: Communications with managed dependencies are implementation 
Line 286: details; use such dependencies as-is in integration tests. Communications 
Line 287: with unmanaged dependencies are part of your system’s observable behavior. 
Line 288: Such dependencies should be mocked out.
Line 289: 
Line 290: --- 페이지 214 ---
Line 291: 192
Line 292: CHAPTER 8
Line 293: Why integration testing?
Line 294: other applications as an unmanaged dependency. Such tables in effect act as a mes-
Line 295: sage bus, with their rows playing the role of messages. Use mocks to make sure the
Line 296: communication pattern with these tables remains unchanged. At the same time, treat
Line 297: the rest of your database as a managed dependency and verify its final state, not the
Line 298: interactions with it (figure 8.5).
Line 299: It’s important to differentiate these two parts of your database because, again, the
Line 300: shared tables are observable externally, and you need to be careful about how your
Line 301: application communicates with them. Don’t change the way your system interacts with
Line 302: those tables unless absolutely necessary! You never know how other applications will
Line 303: react to such a change. 
Line 304: 8.2.3
Line 305: What if you can’t use a real database in integration tests?
Line 306: Sometimes, for reasons outside of your control, you just can’t use a real version of a
Line 307: managed dependency in integration tests. An example would be a legacy database
Line 308: that you can’t deploy to a test automation environment, not to mention a developer
Line 309: machine, because of some IT security policy, or because the cost of setting up and
Line 310: maintaining a test database instance is prohibitive.
Line 311:  What should you do in such a situation? Should you mock out the database anyway,
Line 312: despite it being a managed dependency? No, because mocking out a managed depen-
Line 313: dency compromises the integration tests’ resistance to refactoring. Furthermore, such
Line 314: External applications
Line 315: Table
Line 316: Table
Line 317: Table
Line 318: Table
Line 319: Managed part
Line 320: Table
Line 321: Table
Line 322: Unmanaged part
Line 323: Test directly
Line 324: Replace with mocks
Line 325: Database
Line 326: Your application
Line 327: Figure 8.5
Line 328: Treat the part of the database that is visible to external 
Line 329: applications as an unmanaged dependency. Replace it with mocks in 
Line 330: integration tests. Treat the rest of the database as a managed dependency. 
Line 331: Verify its final state, not interactions with it.
Line 332: 
Line 333: --- 페이지 215 ---
Line 334: 193
Line 335: Integration testing: An example
Line 336: tests no longer provide as good protection against regressions. And if the database is
Line 337: the only out-of-process dependency in your project, the resulting integration tests
Line 338: would deliver no additional protection compared to the existing set of unit tests (assum-
Line 339: ing these unit tests follow the guidelines from chapter 7).
Line 340:  The only thing such integration tests would do, in addition to unit tests, is check
Line 341: what repository methods the controller calls. In other words, you wouldn’t really gain
Line 342: confidence about anything other than those three lines of code in your controller
Line 343: being correct, while still having to do a lot of plumbing.
Line 344:  If you can’t test the database as-is, don’t write integration tests at all, and instead,
Line 345: focus exclusively on unit testing of the domain model. Remember to always put all
Line 346: your tests under close scrutiny. Tests that don’t provide a high enough value should
Line 347: have no place in your test suite. 
Line 348: 8.3
Line 349: Integration testing: An example
Line 350: Let’s get back to the sample CRM system from chapter 7 and see how it can be cov-
Line 351: ered with integration tests. As you may recall, this system implements one feature:
Line 352: changing the user’s email. It retrieves the user and the company from the database,
Line 353: delegates the decision-making to the domain model, and then saves the results back
Line 354: to the database and puts a message on the bus if needed (figure 8.6).
Line 355: The following listing shows how the controller currently looks.
Line 356: public class UserController
Line 357: {
Line 358: private readonly Database _database = new Database();
Line 359: private readonly MessageBus _messageBus = new MessageBus();
Line 360: public string ChangeEmail(int userId, string newEmail)
Line 361: {
Line 362: Listing 8.1
Line 363: The user controller 
Line 364: Application
Line 365: service
Line 366: (controller)
Line 367: Business logic
Line 368: (domain model)
Line 369: Database
Line 370: Message bus
Line 371: GetUserById
Line 372: CanChangeEmail
Line 373: SaveCompany
Line 374: GetCompany
Line 375: ChangeEmail
Line 376: SaveUser
Line 377: SendMessage
Line 378: Figure 8.6
Line 379: The use case of changing the user’s email. The controller orchestrates the work between 
Line 380: the database, the message bus, and the domain model.
Line 381: 
Line 382: --- 페이지 216 ---
Line 383: 194
Line 384: CHAPTER 8
Line 385: Why integration testing?
Line 386: object[] userData = _database.GetUserById(userId);
Line 387: User user = UserFactory.Create(userData);
Line 388: string error = user.CanChangeEmail();
Line 389: if (error != null)
Line 390: return error;
Line 391: object[] companyData = _database.GetCompany();
Line 392: Company company = CompanyFactory.Create(companyData);
Line 393: user.ChangeEmail(newEmail, company);
Line 394: _database.SaveCompany(company);
Line 395: _database.SaveUser(user);
Line 396: foreach (EmailChangedEvent ev in user.EmailChangedEvents)
Line 397: {
Line 398: _messageBus.SendEmailChangedMessage(ev.UserId, ev.NewEmail);
Line 399: }
Line 400: return "OK";
Line 401: }
Line 402: }
Line 403: In the following section, I’ll first outline scenarios to verify using integration tests.
Line 404: Then I’ll show you how to work with the database and the message bus in tests.
Line 405: 8.3.1
Line 406: What scenarios to test?
Line 407: As I mentioned earlier, the general guideline for integration testing is to cover the
Line 408: longest happy path and any edge cases that can’t be exercised by unit tests. The longest
Line 409: happy path is the one that goes through all out-of-process dependencies.
Line 410:  In the CRM project, the longest happy path is a change from a corporate to a non-
Line 411: corporate email. Such a change leads to the maximum number of side effects:
Line 412: In the database, both the user and the company are updated: the user changes
Line 413: its type (from corporate to non-corporate) and email, and the company changes
Line 414: its number of employees.
Line 415: A message is sent to the message bus.
Line 416: As for the edge cases that aren’t tested by unit tests, there’s only one such edge case:
Line 417: the scenario where the email can’t be changed. There’s no need to test this scenario,
Line 418: though, because the application will fail fast if this check isn’t present in the control-
Line 419: ler. That leaves us with a single integration test:
Line 420: public void Changing_email_from_corporate_to_non_corporate()
Line 421: 
Line 422: --- 페이지 217 ---
Line 423: 195
Line 424: Integration testing: An example
Line 425: 8.3.2
Line 426: Categorizing the database and the message bus
Line 427: Before writing the integration test, you need to categorize the two out-of-process
Line 428: dependencies and decide which of them to test directly and which to replace with a
Line 429: mock. The application database is a managed dependency because no other system
Line 430: can access it. Therefore, you should use a real instance of it. The integration test will
Line 431: Insert a user and a company into the database.
Line 432: Run the change of email scenario on that database.
Line 433: Verify the database state.
Line 434: On the other hand, the message bus is an unmanaged dependency—its sole pur-
Line 435: pose is to enable communication with other systems. The integration test will mock
Line 436: out the message bus and verify the interactions between the controller and the
Line 437: mock afterward. 
Line 438: 8.3.3
Line 439: What about end-to-end testing?
Line 440: There will be no end-to-end tests in our sample project. An end-to-end test in a sce-
Line 441: nario with an API would be a test running against a deployed, fully functioning ver-
Line 442: sion of that API, which means no mocks for any of the out-of-process dependencies
Line 443: (figure 8.7). On the other hand, integration tests host the application within the same
Line 444: process and substitute unmanaged dependencies with mocks (figure 8.8).
Line 445:  As I mentioned in chapter 2, whether to use end-to-end tests is a judgment call. For
Line 446: the most part, when you include managed dependencies in the integration testing
Line 447: scope and mock out only unmanaged dependencies, integration tests provide a level
Line 448: End-to-end test
Line 449: Application
Line 450: Message bus
Line 451: Database
Line 452: Out-of-process
Line 453: In-process
Line 454: Figure 8.7
Line 455: End-to-end tests emulate the external client and therefore test a 
Line 456: deployed version of the application with all out-of-process dependencies included 
Line 457: in the testing scope. End-to-end tests shouldn’t check managed dependencies 
Line 458: (such as the database) directly, only indirectly through the application.
Line 459: 
Line 460: --- 페이지 218 ---
Line 461: 196
Line 462: CHAPTER 8
Line 463: Why integration testing?
Line 464: of protection that is close enough to that of end-to-end tests, so you can skip end-to-
Line 465: end testing. However, you could still create one or two overarching end-to-end tests
Line 466: that would provide a sanity check for the project after deployment. Make such tests go
Line 467: through the longest happy path, too, to ensure that your application communicates
Line 468: with all out-of-process dependencies properly. To emulate the external client’s behav-
Line 469: ior, check the message bus directly, but verify the database’s state through the applica-
Line 470: tion itself. 
Line 471: 8.3.4
Line 472: Integration testing: The first try
Line 473: Here’s the first version of the integration test.
Line 474: [Fact]
Line 475: public void Changing_email_from_corporate_to_non_corporate()
Line 476: {
Line 477: // Arrange
Line 478: var db = new Database(ConnectionString);
Line 479:     
Line 480: User user = CreateUser(
Line 481:    
Line 482: "user@mycorp.com", UserType.Employee, db);   
Line 483: CreateCompany("mycorp.com", 1, db);
Line 484:    
Line 485: var messageBusMock = new Mock<IMessageBus>();         
Line 486: var sut = new UserController(db, messageBusMock.Object);
Line 487: // Act
Line 488: string result = sut.ChangeEmail(user.UserId, "new@gmail.com");
Line 489: Listing 8.2
Line 490: The integration test
Line 491: Integration test
Line 492: Application
Line 493: Message bus
Line 494: mock
Line 495: Database
Line 496: Out-of-process
Line 497: In-process
Line 498: Figure 8.8
Line 499: Integration tests host the application within the same process. Unlike 
Line 500: end-to-end tests, integration tests substitute unmanaged dependencies with 
Line 501: mocks. The only out-of-process components for integration tests are managed 
Line 502: dependencies.
Line 503: Database 
Line 504: repository
Line 505: Creates the user 
Line 506: and company in 
Line 507: the database
Line 508: Sets up a 
Line 509: mock for the 
Line 510: message bus
Line 511: 
Line 512: --- 페이지 219 ---
Line 513: 197
Line 514: Using interfaces to abstract dependencies
Line 515: // Assert
Line 516: Assert.Equal("OK", result);
Line 517: object[] userData = db.GetUserById(user.UserId);   
Line 518: User userFromDb = UserFactory.Create(userData);    
Line 519: Assert.Equal("new@gmail.com", userFromDb.Email);   
Line 520: Assert.Equal(UserType.Customer, userFromDb.Type);  
Line 521: object[] companyData = db.GetCompany();
Line 522:    
Line 523: Company companyFromDb = CompanyFactory
Line 524:    
Line 525: .Create(companyData);
Line 526:    
Line 527: Assert.Equal(0, companyFromDb.NumberOfEmployees);  
Line 528: messageBusMock.Verify(
Line 529:     
Line 530: x => x.SendEmailChangedMessage(
Line 531:     
Line 532: user.UserId, "new@gmail.com"),    
Line 533: Times.Once);
Line 534:      
Line 535: }
Line 536: TIP
Line 537: Notice that in the arrange section, the test doesn’t insert the user and
Line 538: the company into the database on its own but instead calls the CreateUser
Line 539: and CreateCompany helper methods. These methods can be reused across
Line 540: multiple integration tests.
Line 541: It’s important to check the state of the database independently of the data used as
Line 542: input parameters. To do that, the integration test queries the user and company data
Line 543: separately in the assert section, creates new userFromDb and companyFromDb instances,
Line 544: and only then asserts their state. This approach ensures that the test exercises both
Line 545: writes to and reads from the database and thus provides the maximum protection
Line 546: against regressions. The reading itself must be implemented using the same code the
Line 547: controller uses internally: in this example, using the Database, UserFactory, and
Line 548: CompanyFactory classes.
Line 549:  This integration test, while it gets the job done, can still benefit from some
Line 550: improvement. For instance, you could use helper methods in the assertion section, too,
Line 551: in order to reduce this section’s size. Also, messageBusMock doesn’t provide as good
Line 552: protection against regressions as it potentially could. We’ll talk about these improve-
Line 553: ments in the subsequent two chapters where we discuss mocking and database testing
Line 554: best practices. 
Line 555: 8.4
Line 556: Using interfaces to abstract dependencies
Line 557: One of the most misunderstood subjects in the sphere of unit testing is the use of
Line 558: interfaces. Developers often ascribe invalid reasons to why they introduce interfaces
Line 559: and, as a result, tend to overuse them. In this section, I’ll expand on those invalid
Line 560: reasons and show in what circumstances the use of interfaces is and isn’t preferable.
Line 561:  
Line 562: Asserts the 
Line 563: user’s state
Line 564: Asserts the 
Line 565: company’s 
Line 566: state
Line 567: Checks the 
Line 568: interactions 
Line 569: with the mock
Line 570: 
Line 571: --- 페이지 220 ---
Line 572: 198
Line 573: CHAPTER 8
Line 574: Why integration testing?
Line 575: 8.4.1
Line 576: Interfaces and loose coupling
Line 577: Many developers introduce interfaces for out-of-process dependencies, such as the
Line 578: database or the message bus, even when these interfaces have only one implementation.
Line 579: This practice has become so widespread nowadays that hardly anyone questions it.
Line 580: You’ll often see class-interface pairs similar to the following:
Line 581: public interface IMessageBus
Line 582: public class MessageBus : IMessageBus
Line 583: public interface IUserRepository
Line 584: public class UserRepository : IUserRepository
Line 585: The common reasoning behind the use of such interfaces is that they help to
Line 586: Abstract out-of-process dependencies, thus achieving loose coupling
Line 587: Add new functionality without changing the existing code, thus adhering to the
Line 588: Open-Closed principle (OCP)
Line 589: Both of these reasons are misconceptions. Interfaces with a single implementation are
Line 590: not abstractions and don’t provide loose coupling any more than concrete classes that
Line 591: implement those interfaces. Genuine abstractions are discovered, not invented. The dis-
Line 592: covery, by definition, takes place post factum, when the abstraction already exists but
Line 593: is not yet clearly defined in the code. Thus, for an interface to be a genuine abstrac-
Line 594: tion, it must have at least two implementations.
Line 595:  The second reason (the ability to add new functionality without changing the exist-
Line 596: ing code) is a misconception because it violates a more foundational principle:
Line 597: YAGNI. YAGNI stands for “You aren’t gonna need it” and advocates against investing
Line 598: time in functionality that’s not needed right now. You shouldn’t develop this function-
Line 599: ality, nor should you modify your existing code to account for the appearance of such
Line 600: functionality in the future. The two major reasons are as follows:
Line 601: Opportunity cost—If you spend time on a feature that business people don’t need
Line 602: at the moment, you steer that time away from features they do need right now.
Line 603: Moreover, when the business people finally come to require the developed func-
Line 604: tionality, their view on it will most likely have evolved, and you will still need to
Line 605: adjust the already-written code. Such activity is wasteful. It’s more beneficial to
Line 606: implement the functionality from scratch when the actual need for it emerges.
Line 607: The less code in the project, the better. Introducing code just in case without an imme-
Line 608: diate need unnecessarily increases your code base’s cost of ownership. It’s bet-
Line 609: ter to postpone introducing new functionality until as late a stage of your
Line 610: project as possible.
Line 611: TIP
Line 612: Writing code is an expensive way to solve problems. The less code the
Line 613: solution requires and the simpler that code is, the better.
Line 614: There are exceptional cases where YAGNI doesn’t apply, but these are few and far
Line 615: between. For those cases, see my article “OCP vs YAGNI,” at https://enterprise-
Line 616: craftsmanship.com/posts/ocp-vs-yagni. 
Line 617: 
Line 618: --- 페이지 221 ---
Line 619: 199
Line 620: Using interfaces to abstract dependencies
Line 621: 8.4.2
Line 622: Why use interfaces for out-of-process dependencies?
Line 623: So, why use interfaces for out-of-process dependencies at all, assuming that each of
Line 624: those interfaces has only one implementation? The real reason is much more practi-
Line 625: cal and down-to-earth. It’s to enable mocking—as simple as that. Without an interface,
Line 626: you can’t create a test double and thus can’t verify interactions between the system
Line 627: under test and the out-of-process dependency.
Line 628:  Therefore, don’t introduce interfaces for out-of-process dependencies unless you need to mock
Line 629: out those dependencies. You only mock out unmanaged dependencies, so the guideline
Line 630: can be boiled down to this: use interfaces for unmanaged dependencies only. Still inject
Line 631: managed dependencies into the controller explicitly, but use concrete classes for that.
Line 632:  Note that genuine abstractions (abstractions that have more than one implementa-
Line 633: tion) can be represented with interfaces regardless of whether you mock them out.
Line 634: Introducing an interface with a single implementation for reasons other than mock-
Line 635: ing is a violation of YAGNI, however.
Line 636:  And you might have noticed in listing 8.2 that UserController now accepts both
Line 637: the message bus and the database explicitly via the constructor, but only the message
Line 638: bus has a corresponding interface. The database is a managed dependency and thus
Line 639: doesn’t require such an interface. Here’s the controller:
Line 640: public class UserController
Line 641: {
Line 642: private readonly Database _database;   
Line 643: private readonly IMessageBus _messageBus;    
Line 644: public UserController(Database database, IMessageBus messageBus)
Line 645: {
Line 646: _database = database;
Line 647: _messageBus = messageBus;
Line 648: }
Line 649: public string ChangeEmail(int userId, string newEmail)
Line 650: {
Line 651: /* the method uses _database and _messageBus */
Line 652: }
Line 653: }
Line 654: NOTE
Line 655: You can mock out a dependency without resorting to an interface by
Line 656: making methods in that dependency virtual and using the class itself as a base
Line 657: for the mock. This approach is inferior to the one with interfaces, though. I
Line 658: explain more on this topic of interfaces versus base classes in chapter 11. 
Line 659: 8.4.3
Line 660: Using interfaces for in-process dependencies
Line 661: You sometimes see code bases where interfaces back not only out-of-process depen-
Line 662: dencies but in-process dependencies as well. For example:
Line 663: public interface IUser
Line 664: {
Line 665: int UserId { get; set; }
Line 666: A concrete 
Line 667: class
Line 668: The interface
Line 669: 
Line 670: --- 페이지 222 ---
Line 671: 200
Line 672: CHAPTER 8
Line 673: Why integration testing?
Line 674: string Email { get; }
Line 675: string CanChangeEmail();
Line 676: void ChangeEmail(string newEmail, Company company);
Line 677: }
Line 678: public class User : IUser
Line 679: {
Line 680: /* ... */
Line 681: }
Line 682: Assuming that IUser has only one implementation (and such specific interfaces always
Line 683: have only one implementation), this is a huge red flag. Just like with out-of-process
Line 684: dependencies, the only reason to introduce an interface with a single implementation
Line 685: for a domain class is to enable mocking. But unlike out-of-process dependencies, you
Line 686: should never check interactions between domain classes, because doing so results in
Line 687: brittle tests: tests that couple to implementation details and thus fail on the metric of
Line 688: resisting to refactoring (see chapter 5 for more details about mocks and test fragility). 
Line 689: 8.5
Line 690: Integration testing best practices
Line 691: There are some general guidelines that can help you get the most out of your integra-
Line 692: tion tests:
Line 693: Making domain model boundaries explicit
Line 694: Reducing the number of layers in the application
Line 695: Eliminating circular dependencies
Line 696: As usual, best practices that are beneficial for tests also tend to improve the health of
Line 697: your code base in general.
Line 698: 8.5.1
Line 699: Making domain model boundaries explicit
Line 700: Try to always have an explicit, well-known place for the domain model in your code
Line 701: base. The domain model is the collection of domain knowledge about the problem your
Line 702: project is meant to solve. Assigning the domain model an explicit boundary helps you
Line 703: better visualize and reason about that part of your code.
Line 704:  This practice also helps with testing. As I mentioned earlier in this chapter, unit
Line 705: tests target the domain model and algorithms, while integration tests target control-
Line 706: lers. The explicit boundary between domain classes and controllers makes it easier to
Line 707: tell the difference between unit and integration tests.
Line 708:  The boundary itself can take the form of a separate assembly or a namespace. The
Line 709: particulars aren’t that important as long as all of the domain logic is put under a sin-
Line 710: gle, distinct umbrella and not scattered across the code base. 
Line 711: 8.5.2
Line 712: Reducing the number of layers
Line 713: Most programmers naturally gravitate toward abstracting and generalizing the code
Line 714: by introducing additional layers of indirection. In a typical enterprise-level applica-
Line 715: tion, you can easily observe several such layers (figure 8.9).
Line 716: 
Line 717: --- 페이지 223 ---
Line 718: 201
Line 719: Integration testing best practices
Line 720: In extreme cases, an application gets so many abstraction layers that it becomes too
Line 721: hard to navigate the code base and understand the logic behind even the simplest
Line 722: operations. At some point, you just want to get to the specific solution of the problem
Line 723: at hand, not some generalization of that solution in a vacuum.
Line 724: All problems in computer science can be solved by another layer of indirection, except for
Line 725: the problem of too many layers of indirection.
Line 726:                                                                    
Line 727: —David J. Wheeler
Line 728: Layers of indirection negatively affect your ability to reason about the code. When
Line 729: every feature has a representation in each of those layers, you have to expend signifi-
Line 730: cant effort assembling all the pieces into a cohesive picture. This creates an additional
Line 731: mental burden that handicaps the entire development process.
Line 732:  An excessive number of abstractions doesn’t help unit or integration testing,
Line 733: either. Code bases with many layers of indirections tend not to have a clear boundary
Line 734: between controllers and the domain model (which, as you might remember from
Line 735: chapter 7, is a precondition for effective tests). There’s also a much stronger tendency
Line 736: to verify each layer separately. This tendency results in a lot of low-value integration
Line 737: tests, each of which exercises only the code from a specific layer and mocks out layers
Line 738: Application
Line 739: services layer
Line 740: Business logic
Line 741: implementation layer
Line 742: Abstractions layer
Line 743: Persistence layer
Line 744: Order checkout
Line 745: Changing user email
Line 746: Resetting password
Line 747: Figure 8.9
Line 748: Various application concerns are often addressed by 
Line 749: separate layers of indirection. A typical feature takes up a small 
Line 750: portion of each layer.
Line 751: 
Line 752: --- 페이지 224 ---
Line 753: 202
Line 754: CHAPTER 8
Line 755: Why integration testing?
Line 756: underneath. The end result is always the same: insufficient protection against regres-
Line 757: sions combined with low resistance to refactoring.
Line 758:  Try to have as few layers of indirection as possible. In most backend systems, you
Line 759: can get away with just three: the domain model, application services layer (control-
Line 760: lers), and infrastructure layer. The infrastructure layer typically consists of algorithms
Line 761: that don’t belong to the domain model, as well as code that enables access to out-of-
Line 762: process dependencies (figure 8.10). 
Line 763: 8.5.3
Line 764: Eliminating circular dependencies
Line 765: Another practice that can drastically improve the maintainability of your code base
Line 766: and make testing easier is eliminating circular dependencies.
Line 767: DEFINITION
Line 768: A circular dependency (also known as cyclic dependency) is two or
Line 769: more classes that directly or indirectly depend on each other to function
Line 770: properly.
Line 771: A typical example of a circular dependency is a callback:
Line 772: public class CheckOutService
Line 773: {
Line 774: public void CheckOut(int orderId)
Line 775: {
Line 776: var service = new ReportGenerationService();
Line 777: service.GenerateReport(orderId, this);
Line 778: Application
Line 779: services layer
Line 780: Domain layer
Line 781: Infrastructure layer
Line 782: Order checkout
Line 783: Changing user email
Line 784: Resetting password
Line 785: Figure 8.10
Line 786: You can get away with just three layers: the domain layer (contains 
Line 787: domain logic), application services layers (provides an entry point for the external 
Line 788: client, and coordinates the work between domain classes and out-of-process 
Line 789: dependencies), and infrastructure layer (works with out-of-process dependencies; 
Line 790: database repositories, ORM mappings, and SMTP gateways reside in this layer).
Line 791: 
Line 792: --- 페이지 225 ---
Line 793: 203
Line 794: Integration testing best practices
Line 795: /* other code */
Line 796: }
Line 797: }
Line 798: public class ReportGenerationService
Line 799: {
Line 800: public void GenerateReport(
Line 801: int orderId,
Line 802: CheckOutService checkOutService)
Line 803: {
Line 804: /* calls checkOutService when generation is completed */
Line 805: }
Line 806: }
Line 807: Here, CheckOutService creates an instance of ReportGenerationService and passes
Line 808: itself to that instance as an argument. ReportGenerationService calls CheckOut-
Line 809: Service back to notify it about the result of the report generation.
Line 810:  Just like an excessive number of abstraction layers, circular dependencies add tre-
Line 811: mendous cognitive load when you try to read and understand the code. The reason is
Line 812: that circular dependencies don’t give you a clear starting point from which you can
Line 813: begin exploring the solution. To understand just one class, you have to read and
Line 814: understand the whole graph of its siblings all at once. Even a small set of interdepen-
Line 815: dent classes can quickly become too hard to grasp.
Line 816:  Circular dependencies also interfere with testing. You often have to resort to inter-
Line 817: faces and mocking in order to split the class graph and isolate a single unit of behav-
Line 818: ior, which, again, is a no-go when it comes to testing the domain model (more on that
Line 819: in chapter 5).
Line 820:  Note that the use of interfaces only masks the problem of circular dependencies. If
Line 821: you introduce an interface for CheckOutService and make ReportGenerationService
Line 822: depend on that interface instead of the concrete class, you remove the circular depen-
Line 823: dency at compile time (figure 8.11), but the cycle still persists at runtime. Even
Line 824: though the compiler no longer regards this class composition as a circular reference,
Line 825: the cognitive load required to understand the code doesn’t become any smaller. If
Line 826: anything, it increases due to the additional interface.
Line 827: CheckOutService
Line 828: ICheckOutService
Line 829: ReportGenerationService
Line 830: Figure 8.11
Line 831: With an interface, you remove the circular dependency 
Line 832: at compile time, but not at runtime. The cognitive load required to 
Line 833: understand the code doesn’t become any smaller.
Line 834: 
Line 835: --- 페이지 226 ---
Line 836: 204
Line 837: CHAPTER 8
Line 838: Why integration testing?
Line 839: A better approach to handle circular dependencies is to get rid of them. Refactor
Line 840: ReportGenerationService such that it depends on neither CheckOutService nor the
Line 841: ICheckOutService interface, and make ReportGenerationService return the result
Line 842: of its work as a plain value instead of calling CheckOutService:
Line 843: public class CheckOutService
Line 844: {
Line 845: public void CheckOut(int orderId)
Line 846: {
Line 847: var service = new ReportGenerationService();
Line 848: Report report = service.GenerateReport(orderId);
Line 849: /* other work */
Line 850: }
Line 851: }
Line 852: public class ReportGenerationService
Line 853: {
Line 854: public Report GenerateReport(int orderId)
Line 855: {
Line 856: /* ... */
Line 857: }
Line 858: }
Line 859: It’s rarely possible to eliminate all circular dependencies in your code base. But even
Line 860: then, you can minimize the damage by making the remaining graphs of interdepen-
Line 861: dent classes as small as possible. 
Line 862: 8.5.4
Line 863: Using multiple act sections in a test
Line 864: As you might remember from chapter 3, having more than one arrange, act, or assert
Line 865: section in a test is a code smell. It’s a sign that this test checks multiple units of behav-
Line 866: ior, which, in turn, hinders the test’s maintainability. For example, if you have two
Line 867: related use cases—say, user registration and user deletion—it might be tempting to
Line 868: check both of these use cases in a single integration test. Such a test could have the
Line 869: following structure:
Line 870: Arrange—Prepare data with which to register a user.
Line 871: Act—Call UserController.RegisterUser().
Line 872: Assert—Query the database to see if the registration is completed successfully.
Line 873: Act—Call UserController.DeleteUser().
Line 874: Assert—Query the database to make sure the user is deleted.
Line 875: This approach is compelling because the user states naturally flow from one another,
Line 876: and the first act (registering a user) can simultaneously serve as an arrange phase for
Line 877: the subsequent act (user deletion). The problem is that such tests lose focus and can
Line 878: quickly become too bloated.
Line 879:  It’s best to split the test by extracting each act into a test of its own. It may seem like
Line 880: unnecessary work (after all, why create two tests where one would suffice?), but this
Line 881: 
Line 882: --- 페이지 227 ---
Line 883: 205
Line 884: How to test logging functionality
Line 885: work pays off in the long run. Having each test focus on a single unit of behavior
Line 886: makes those tests easier to understand and modify when necessary.
Line 887:  The exception to this guideline is tests working with out-of-process dependencies
Line 888: that are hard to bring to a desirable state. Let’s say for example that registering a user
Line 889: results in creating a bank account in an external banking system. The bank has provi-
Line 890: sioned a sandbox for your organization, and you want to use that sandbox in an end-
Line 891: to-end test. The problem is that the sandbox is too slow, or maybe the bank limits the
Line 892: number of calls you can make to that sandbox. In such a scenario, it becomes benefi-
Line 893: cial to combine multiple acts into a single test and thus reduce the number of interac-
Line 894: tions with the problematic out-of-process dependency.
Line 895:  Hard-to-manage out-of-process dependencies are the only legitimate reason to
Line 896: write a test with more than one act section. This is why you should never have multiple
Line 897: acts in a unit test—unit tests don’t work with out-of-process dependencies. Even inte-
Line 898: gration tests should rarely have several acts. In practice, multistep tests almost always
Line 899: belong to the category of end-to-end tests. 
Line 900: 8.6
Line 901: How to test logging functionality
Line 902: Logging is a gray area, and it isn’t obvious what to do with it when it comes to testing.
Line 903: This is a complex topic that I’ll split into the following questions:
Line 904: Should you test logging at all?
Line 905: If so, how should you test it?
Line 906: How much logging is enough?
Line 907: How do you pass around logger instances?
Line 908: We’ll use our sample CRM project as an example.
Line 909: 8.6.1
Line 910: Should you test logging?
Line 911: Logging is a cross-cutting functionality, which you can require in any part of your code
Line 912: base. Here’s an example of logging in the User class.
Line 913: public class User
Line 914: {
Line 915: public void ChangeEmail(string newEmail, Company company)
Line 916: {
Line 917: _logger.Info(    
Line 918: $"Changing email for user {UserId} to {newEmail}");
Line 919: Precondition.Requires(CanChangeEmail() == null);
Line 920: if (Email == newEmail)
Line 921: return;
Line 922: UserType newType = company.IsEmailCorporate(newEmail)
Line 923: ? UserType.Employee
Line 924: : UserType.Customer;
Line 925: Listing 8.3
Line 926: An example of logging in User
Line 927: Start of the
Line 928: method
Line 929: 
Line 930: --- 페이지 228 ---
Line 931: 206
Line 932: CHAPTER 8
Line 933: Why integration testing?
Line 934: if (Type != newType)
Line 935: {
Line 936: int delta = newType == UserType.Employee ? 1 : -1;
Line 937: company.ChangeNumberOfEmployees(delta);
Line 938: _logger.Info(
Line 939:    
Line 940: $"User {UserId} changed type " +
Line 941:    
Line 942: $"from {Type} to {newType}");
Line 943:    
Line 944: }
Line 945: Email = newEmail;
Line 946: Type = newType;
Line 947: EmailChangedEvents.Add(new EmailChangedEvent(UserId, newEmail));
Line 948: _logger.Info(
Line 949:     
Line 950: $"Email is changed for user {UserId}");
Line 951: }
Line 952: }
Line 953: The User class records in a log file each beginning and ending of the ChangeEmail
Line 954: method, as well as the change of the user type. Should you test this functionality?
Line 955:  On the one hand, logging generates important information about the applica-
Line 956: tion’s behavior. But on the other hand, logging can be so ubiquitous that it’s not obvi-
Line 957: ous whether this functionality is worth the additional, quite significant, testing effort.
Line 958: The answer to the question of whether you should test logging comes down to this: Is
Line 959: logging part of the application’s observable behavior, or is it an implementation detail?
Line 960:  In that sense, it isn’t different from any other functionality. Logging ultimately
Line 961: results in side effects in an out-of-process dependency such as a text file or a database.
Line 962: If these side effects are meant to be observed by your customer, the application’s cli-
Line 963: ents, or anyone else other than the developers themselves, then logging is an observ-
Line 964: able behavior and thus must be tested. If the only audience is the developers, then it’s
Line 965: an implementation detail that can be freely modified without anyone noticing, in
Line 966: which case it shouldn’t be tested.
Line 967:  For example, if you write a logging library, then the logs this library produces are
Line 968: the most important (and the only) part of its observable behavior. Another example is
Line 969: when business people insist on logging key application workflows. In this case, logs
Line 970: also become a business requirement and thus have to be covered by tests. However, in
Line 971: the latter example, you might also have separate logging just for developers.
Line 972:  Steve Freeman and Nat Pryce, in their book Growing Object-Oriented Software, Guided
Line 973: by Tests (Addison-Wesley Professional, 2009), call these two types of logging support
Line 974: logging and diagnostic logging:
Line 975: Support logging produces messages that are intended to be tracked by support
Line 976: staff or system administrators.
Line 977: Diagnostic logging helps developers understand what’s going on inside the
Line 978: application. 
Line 979: Changes the 
Line 980: user type
Line 981: End of the
Line 982: method
Line 983: 
Line 984: --- 페이지 229 ---
Line 985: 207
Line 986: How to test logging functionality
Line 987: 8.6.2
Line 988: How should you test logging?
Line 989: Because logging involves out-of-process dependencies, when it comes to testing it, the
Line 990: same rules apply as with any other functionality that touches out-of-process dependen-
Line 991: cies. You need to use mocks to verify interactions between your application and the
Line 992: log storage.
Line 993: INTRODUCING A WRAPPER ON TOP OF ILOGGER
Line 994: But don’t just mock out the ILogger interface. Because support logging is a business
Line 995: requirement, reflect that requirement explicitly in your code base. Create a special
Line 996: DomainLogger class where you explicitly list all the support logging needed for the
Line 997: business; verify interactions with that class instead of the raw ILogger.
Line 998:  For example, let’s say that business people require you to log all changes of the
Line 999: users’ types, but the logging at the beginning and the end of the method is there just
Line 1000: for debugging purposes. The next listing shows the User class after introducing a
Line 1001: DomainLogger class.
Line 1002: public void ChangeEmail(string newEmail, Company company)
Line 1003: {
Line 1004: _logger.Info(
Line 1005:      
Line 1006: $"Changing email for user {UserId} to {newEmail}");
Line 1007: Precondition.Requires(CanChangeEmail() == null);
Line 1008: if (Email == newEmail)
Line 1009: return;
Line 1010: UserType newType = company.IsEmailCorporate(newEmail)
Line 1011: ? UserType.Employee
Line 1012: : UserType.Customer;
Line 1013: if (Type != newType)
Line 1014: {
Line 1015: int delta = newType == UserType.Employee ? 1 : -1;
Line 1016: company.ChangeNumberOfEmployees(delta);
Line 1017: _domainLogger.UserTypeHasChanged(         
Line 1018: UserId, Type, newType);
Line 1019:          
Line 1020: }
Line 1021: Email = newEmail;
Line 1022: Type = newType;
Line 1023: EmailChangedEvents.Add(new EmailChangedEvent(UserId, newEmail));
Line 1024: _logger.Info(
Line 1025:    
Line 1026: $"Email is changed for user {UserId}");
Line 1027: }
Line 1028: The diagnostic logging still uses the old logger (which is of type ILogger), but the
Line 1029: support logging now uses the new domainLogger instance of type IDomainLogger. The
Line 1030: following listing shows the implementation of IDomainLogger.
Line 1031: Listing 8.4
Line 1032: Extracting support logging into the DomainLogger class
Line 1033: Diagnostic
Line 1034: logging
Line 1035: Support 
Line 1036: logging
Line 1037: Diagnostic
Line 1038: logging
Line 1039: 
Line 1040: --- 페이지 230 ---
Line 1041: 208
Line 1042: CHAPTER 8
Line 1043: Why integration testing?
Line 1044: public class DomainLogger : IDomainLogger
Line 1045: {
Line 1046: private readonly ILogger _logger;
Line 1047: public DomainLogger(ILogger logger)
Line 1048: {
Line 1049: _logger = logger;
Line 1050: }
Line 1051: public void UserTypeHasChanged(
Line 1052: int userId, UserType oldType, UserType newType)
Line 1053: {
Line 1054: _logger.Info(
Line 1055: $"User {userId} changed type " +
Line 1056: $"from {oldType} to {newType}");
Line 1057: }
Line 1058: }
Line 1059: DomainLogger works on top of ILogger: it uses the domain language to declare spe-
Line 1060: cific log entries required by the business, thus making support logging easier to
Line 1061: understand and maintain. In fact, this implementation is very similar to the concept
Line 1062: of structured logging, which enables great flexibility when it comes to log file post-
Line 1063: processing and analysis. 
Line 1064: UNDERSTANDING STRUCTURED LOGGING
Line 1065: Structured logging is a logging technique where capturing log data is decoupled from
Line 1066: the rendering of that data. Traditional logging works with simple text. A call like
Line 1067: logger.Info("User Id is " + 12);
Line 1068: first forms a string and then writes that string to a log storage. The problem with this
Line 1069: approach is that the resulting log files are hard to analyze due to the lack of structure.
Line 1070: For example, it’s not easy to see how many messages of a particular type there are and
Line 1071: how many of those relate to a specific user ID. You’d need to use (or even write your
Line 1072: own) special tooling for that.
Line 1073:  On the other hand, structured logging introduces structure to your log storage.
Line 1074: The use of a structured logging library looks similar on the surface:
Line 1075: logger.Info("User Id is {UserId}", 12);
Line 1076: But its underlying behavior differs significantly. Behind the scenes, this method com-
Line 1077: putes a hash of the message template (the message itself is stored in a lookup storage
Line 1078: for space efficiency) and combines that hash with the input parameters to form a set
Line 1079: of captured data. The next step is the rendering of that data. You can still have a flat log
Line 1080: file, as with traditional logging, but that’s just one possible rendering. You could also
Line 1081: configure the logging library to render the captured data as a JSON or a CSV file,
Line 1082: where it would be easier to analyze (figure 8.12).
Line 1083: Listing 8.5
Line 1084: DomainLogger as a wrapper on top of ILogger
Line 1085: 
Line 1086: --- 페이지 231 ---
Line 1087: 209
Line 1088: How to test logging functionality
Line 1089: DomainLogger in listing 8.5 isn’t a structured logger per se, but it operates in the same
Line 1090: spirit. Look at this method once again:
Line 1091: public void UserTypeHasChanged(
Line 1092: int userId, UserType oldType, UserType newType)
Line 1093: {
Line 1094: _logger.Info(
Line 1095: $"User {userId} changed type " +
Line 1096: $"from {oldType} to {newType}");
Line 1097: }
Line 1098: You can view UserTypeHasChanged() as the message template’s hash. Together with
Line 1099: the userId, oldType, and newType parameters, that hash forms the log data. The
Line 1100: method’s implementation renders the log data into a flat log file. And you can easily
Line 1101: create additional renderings by also writing the log data into a JSON or a CSV file. 
Line 1102: WRITING TESTS FOR SUPPORT AND DIAGNOSTIC LOGGING
Line 1103: As I mentioned earlier, DomainLogger represents an out-of-process dependency—the
Line 1104: log storage. This poses a problem: User now interacts with that dependency and thus
Line 1105: violates the separation between business logic and communication with out-of-process
Line 1106: dependencies. The use of DomainLogger has transitioned User to the category of
Line 1107: Log data
Line 1108: logger.Info("User Id is {UserId}", 12)
Line 1109: MessageTemplate
Line 1110: UserId
Line 1111: User Id is {UserId}
Line 1112: 12
Line 1113: User Id is 12
Line 1114: Flat log ﬁle
Line 1115: { “MessageTemplate”: “…”,
Line 1116: “UserId” : 12 }
Line 1117: MessageTemplate,UserId
Line 1118: User Id is {UserId},12
Line 1119: JSON ﬁle
Line 1120: CSV ﬁle
Line 1121: Rendering
Line 1122: Figure 8.12
Line 1123: Structured logging decouples log data from renderings of that data. You can set up 
Line 1124: multiple renderings, such as a flat log file, JSON, or CSV file.
Line 1125: 
Line 1126: --- 페이지 232 ---
Line 1127: 210
Line 1128: CHAPTER 8
Line 1129: Why integration testing?
Line 1130: overcomplicated code, making it harder to test and maintain (refer to chapter 7 for
Line 1131: more details about code categories).
Line 1132:  This problem can be solved the same way we implemented the notification of
Line 1133: external systems about changed user emails: with the help of domain events (again,
Line 1134: see chapter 7 for details). You can introduce a separate domain event to track changes
Line 1135: in the user type. The controller will then convert those changes into calls to Domain-
Line 1136: Logger, as shown in the following listing.
Line 1137: public void ChangeEmail(string newEmail, Company company)
Line 1138: {
Line 1139: _logger.Info(
Line 1140: $"Changing email for user {UserId} to {newEmail}");
Line 1141: Precondition.Requires(CanChangeEmail() == null);
Line 1142: if (Email == newEmail)
Line 1143: return;
Line 1144: UserType newType = company.IsEmailCorporate(newEmail)
Line 1145: ? UserType.Employee
Line 1146: : UserType.Customer;
Line 1147: if (Type != newType)
Line 1148: {
Line 1149: int delta = newType == UserType.Employee ? 1 : -1;
Line 1150: company.ChangeNumberOfEmployees(delta);
Line 1151: AddDomainEvent(
Line 1152:         
Line 1153: new UserTypeChangedEvent(
Line 1154:         
Line 1155: UserId, Type, newType));        
Line 1156: }
Line 1157: Email = newEmail;
Line 1158: Type = newType;
Line 1159: AddDomainEvent(new EmailChangedEvent(UserId, newEmail));
Line 1160: _logger.Info($"Email is changed for user {UserId}");
Line 1161: }
Line 1162: Notice that there are now two domain events: UserTypeChangedEvent and Email-
Line 1163: ChangedEvent. Both of them implement the same interface (IDomainEvent) and thus
Line 1164: can be stored in the same collection.
Line 1165:  And here is how the controller looks.
Line 1166: public string ChangeEmail(int userId, string newEmail)
Line 1167: {
Line 1168: object[] userData = _database.GetUserById(userId);
Line 1169: User user = UserFactory.Create(userData);
Line 1170: Listing 8.6
Line 1171: Replacing DomainLogger in User with a domain event
Line 1172: Listing 8.7
Line 1173: Latest version of UserController
Line 1174: Uses a domain 
Line 1175: event instead of 
Line 1176: DomainLogger
Line 1177: 
Line 1178: --- 페이지 233 ---
Line 1179: 211
Line 1180: How to test logging functionality
Line 1181: string error = user.CanChangeEmail();
Line 1182: if (error != null)
Line 1183: return error;
Line 1184: object[] companyData = _database.GetCompany();
Line 1185: Company company = CompanyFactory.Create(companyData);
Line 1186: user.ChangeEmail(newEmail, company);
Line 1187: _database.SaveCompany(company);
Line 1188: _database.SaveUser(user);
Line 1189: _eventDispatcher.Dispatch(user.DomainEvents);   
Line 1190: return "OK";
Line 1191: }
Line 1192: EventDispatcher is a new class that converts domain events into calls to out-of-process
Line 1193: dependencies:
Line 1194: 
Line 1195: EmailChangedEvent translates into _messageBus.SendEmailChangedMessage().
Line 1196: 
Line 1197: UserTypeChangedEvent translates into _domainLogger.UserTypeHasChanged().
Line 1198: The use of UserTypeChangedEvent has restored the separation between the two
Line 1199: responsibilities: domain logic and communication with out-of-process dependencies.
Line 1200: Testing support logging now isn’t any different from testing the other unmanaged
Line 1201: dependency, the message bus:
Line 1202: Unit tests should check an instance of UserTypeChangedEvent in the User
Line 1203: under test.
Line 1204: The single integration test should use a mock to ensure the interaction with
Line 1205: DomainLogger is in place.
Line 1206: Note that if you need to do support logging in the controller and not one of the
Line 1207: domain classes, there’s no need to use domain events. As you may remember from
Line 1208: chapter 7, controllers orchestrate the collaboration between the domain model and
Line 1209: out-of-process dependencies. DomainLogger is one of such dependencies, and thus
Line 1210: UserController can use that logger directly.
Line 1211:  Also notice that I didn’t change the way the User class does diagnostic logging.
Line 1212: User still uses the logger instance directly in the beginning and at the end of its Chan-
Line 1213: geEmail method. This is by design. Diagnostic logging is for developers only; you
Line 1214: don’t need to unit test this functionality and thus don’t have to keep it out of the
Line 1215: domain model.
Line 1216:  Still, refrain from the use of diagnostic logging in User or other domain classes
Line 1217: when possible. I explain why in the next section. 
Line 1218: Dispatches user 
Line 1219: domain events
Line 1220: 
Line 1221: --- 페이지 234 ---
Line 1222: 212
Line 1223: CHAPTER 8
Line 1224: Why integration testing?
Line 1225: 8.6.3
Line 1226: How much logging is enough?
Line 1227: Another important question is about the optimum amount of logging. How much log-
Line 1228: ging is enough? Support logging is out of the question here because it’s a business
Line 1229: requirement. You do have control over diagnostic logging, though.
Line 1230:  It’s important not to overuse diagnostic logging, for the following two reasons:
Line 1231: Excessive logging clutters the code. This is especially true for the domain model.
Line 1232: That’s why I don’t recommend using diagnostic logging in User even though
Line 1233: such a use is fine from a unit testing perspective: it obscures the code.
Line 1234: Logs’ signal-to-noise ratio is key. The more you log, the harder it is to find relevant
Line 1235: information. Maximize the signal; minimize the noise.
Line 1236: Try not to use diagnostic logging in the domain model at all. In most cases, you can
Line 1237: safely move that logging from domain classes to controllers. And even then, resort to
Line 1238: diagnostic logging only temporarily when you need to debug something. Remove it
Line 1239: once you finish debugging. Ideally, you should use diagnostic logging for unhandled
Line 1240: exceptions only. 
Line 1241: 8.6.4
Line 1242: How do you pass around logger instances?
Line 1243: Finally, the last question is how to pass logger instances in the code. One way to
Line 1244: resolve these instances is using static methods, as shown in the following listing.
Line 1245: public class User
Line 1246: {
Line 1247: private static readonly ILogger _logger =   
Line 1248: LogManager.GetLogger(typeof(User));     
Line 1249: public void ChangeEmail(string newEmail, Company company)
Line 1250: {
Line 1251: _logger.Info(
Line 1252: $"Changing email for user {UserId} to {newEmail}");
Line 1253: /* ... */
Line 1254: _logger.Info($"Email is changed for user {UserId}");
Line 1255: }
Line 1256: }
Line 1257: Steven van Deursen and Mark Seeman, in their book Dependency Injection Principles,
Line 1258: Practices, Patterns (Manning Publications, 2018), call this type of dependency acquisi-
Line 1259: tion ambient context. This is an anti-pattern. Two of their arguments are that
Line 1260: The dependency is hidden and hard to change.
Line 1261: Testing becomes more difficult.
Line 1262: I fully agree with this analysis. To me, though, the main drawback of ambient con-
Line 1263: text is that it masks potential problems in code. If injecting a logger explicitly into a
Line 1264: Listing 8.8
Line 1265: Storing ILogger in a static field
Line 1266: Resolves ILogger through a 
Line 1267: static method, and stores it 
Line 1268: in a private static field
Line 1269: 
Line 1270: --- 페이지 235 ---
Line 1271: 213
Line 1272: Summary
Line 1273: domain class becomes so inconvenient that you have to resort to ambient context,
Line 1274: that’s a certain sign of trouble. You either log too much or use too many layers of indi-
Line 1275: rection. In any case, ambient context is not a solution. Instead, tackle the root cause
Line 1276: of the problem.
Line 1277:  The following listing shows one way to explicitly inject the logger: as a method
Line 1278: argument. Another way is through the class constructor.
Line 1279: public void ChangeEmail(
Line 1280: string newEmail,      
Line 1281: Company company,      
Line 1282: ILogger logger)       
Line 1283: {
Line 1284: logger.Info(
Line 1285: $"Changing email for user {UserId} to {newEmail}");
Line 1286: /* ... */
Line 1287: logger.Info($"Email is changed for user {UserId}");
Line 1288: }
Line 1289: 8.7
Line 1290: Conclusion
Line 1291: View communications with all out-of-process dependencies through the lens of whether
Line 1292: this communication is part of the application’s observable behavior or an imple-
Line 1293: mentation detail. The log storage isn’t any different in that regard. Mock logging
Line 1294: functionality if the logs are observable by non-programmers; don’t test it otherwise.
Line 1295: In the next chapter, we’ll dive deeper into the topic of mocking and best practices
Line 1296: related to it. 
Line 1297: Summary
Line 1298: An integration test is any test that is not a unit test. Integration tests verify how
Line 1299: your system works in integration with out-of-process dependencies:
Line 1300: – Integration tests cover controllers; unit tests cover algorithms and the domain
Line 1301: model.
Line 1302: – Integration tests provide better protection against regressions and resistance
Line 1303: to refactoring; unit tests have better maintainability and feedback speed.
Line 1304: The bar for integration tests is higher than for unit tests: the score they have in
Line 1305: the metrics of protection against regressions and resistance to refactoring must
Line 1306: be higher than that of a unit test to offset the worse maintainability and feed-
Line 1307: back speed. The Test Pyramid represents this trade-off: the majority of tests
Line 1308: should be fast and cheap unit tests, with a smaller number of slow and more
Line 1309: expensive integration tests that check correctness of the system as a whole:
Line 1310: – Check as many of the business scenario’s edge cases as possible with unit
Line 1311: tests. Use integration tests to cover one happy path, as well as any edge cases
Line 1312: that can’t be covered by unit tests.
Line 1313: Listing 8.9
Line 1314: Injecting the logger explicitly
Line 1315: Method 
Line 1316: injection 
Line 1317: 
Line 1318: --- 페이지 236 ---
Line 1319: 214
Line 1320: CHAPTER 8
Line 1321: Why integration testing?
Line 1322: – The shape of the Test Pyramid depends on the project’s complexity. Simple
Line 1323: projects have little code in the domain model and thus can have an equal
Line 1324: number of unit and integration tests. In the most trivial cases, there might be
Line 1325: no unit tests.
Line 1326: The Fail Fast principle advocates for making bugs manifest themselves quickly
Line 1327: and is a viable alternative to integration testing.
Line 1328: Managed dependencies are out-of-process dependencies that are only accessible
Line 1329: through your application. Interactions with managed dependencies aren’t
Line 1330: observable externally. A typical example is the application database.
Line 1331: Unmanaged dependencies are out-of-process dependencies that other applications
Line 1332: have access to. Interactions with unmanaged dependencies are observable exter-
Line 1333: nally. Typical examples include an SMTP server and a message bus.
Line 1334: Communications with managed dependencies are implementation details; com-
Line 1335: munications with unmanaged dependencies are part of your system’s observ-
Line 1336: able behavior.
Line 1337: Use real instances of managed dependencies in integration tests; replace unman-
Line 1338: aged dependencies with mocks.
Line 1339: Sometimes an out-of-process dependency exhibits attributes of both managed and
Line 1340: unmanaged dependencies. A typical example is a database that other applications
Line 1341: have access to. Treat the observable part of the dependency as an unmanaged
Line 1342: dependency: replace that part with mocks in tests. Treat the rest of the depen-
Line 1343: dency as a managed dependency: verify its final state, not interactions with it.
Line 1344: An integration test must go through all layers that work with a managed depen-
Line 1345: dency. In an example with a database, this means checking the state of that
Line 1346: database independently of the data used as input parameters.
Line 1347: Interfaces with a single implementation are not abstractions and don’t provide
Line 1348: loose coupling any more than the concrete classes that implement those inter-
Line 1349: faces. Trying to anticipate future implementations for such interfaces violates
Line 1350: the YAGNI (you aren’t gonna need it) principle.
Line 1351: The only legitimate reason to use interfaces with a single implementation is to
Line 1352: enable mocking. Use such interfaces only for unmanaged dependencies. Use
Line 1353: concrete classes for managed dependencies.
Line 1354: Interfaces with a single implementation used for in-process dependencies are
Line 1355: a red flag. Such interfaces hint at using mocks to check interactions between
Line 1356: domain classes, which leads to coupling tests to the code’s implementation
Line 1357: details.
Line 1358: Have an explicit and well-known place for the domain model in your code base.
Line 1359: The explicit boundary between domain classes and controllers makes it easier
Line 1360: to tell unit and integration tests apart.
Line 1361: An excessive number of layers of indirection negatively affects your ability to
Line 1362: reason about the code. Have as few layers of indirections as possible. In most
Line 1363: 
Line 1364: --- 페이지 237 ---
Line 1365: 215
Line 1366: Summary
Line 1367: backend systems, you can get away with just three of them: the domain model,
Line 1368: an application services layer (controllers), and an infrastructure layer.
Line 1369: Circular dependencies add cognitive load when you try to understand the code.
Line 1370: A typical example is a callback (when a callee notifies the caller about the result
Line 1371: of its work). Break the cycle by introducing a value object; use that value object
Line 1372: to return the result from the callee to the caller.
Line 1373: Multiple act sections in a test are only justified when that test works with out-of-
Line 1374: process dependencies that are hard to bring into a desirable state. You should
Line 1375: never have multiple acts in a unit test, because unit tests don’t work with out-of-
Line 1376: process dependencies. Multistep tests almost always belong to the category of
Line 1377: end-to-end tests.
Line 1378: Support logging is intended for support staff and system administrators; it’s
Line 1379: part of the application’s observable behavior. Diagnostic logging helps devel-
Line 1380: opers understand what’s going on inside the application: it’s an implementa-
Line 1381: tion detail.
Line 1382: Because support logging is a business requirement, reflect that requirement
Line 1383: explicitly in your code base. Introduce a special DomainLogger class where you
Line 1384: list all the support logging needed for the business.
Line 1385: Treat support logging like any other functionality that works with an out-of-pro-
Line 1386: cess dependency. Use domain events to track changes in the domain model;
Line 1387: convert those domain events into calls to DomainLogger in controllers.
Line 1388: Don’t test diagnostic logging. Unlike support logging, you can do diagnostic
Line 1389: logging directly in the domain model.
Line 1390: Use diagnostic logging sporadically. Excessive diagnostic logging clutters the
Line 1391: code and damages the logs’ signal-to-noise ratio. Ideally, you should only use
Line 1392: diagnostic logging for unhandled exceptions.
Line 1393: Always inject all dependencies explicitly (including loggers), either via the con-
Line 1394: structor or as a method argument.
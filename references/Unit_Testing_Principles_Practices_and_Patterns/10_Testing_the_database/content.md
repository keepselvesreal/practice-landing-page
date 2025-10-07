Line 1: 
Line 2: --- 페이지 251 ---
Line 3: 229
Line 4: Testing the database
Line 5: The last piece of the puzzle in integration testing is managed out-of-process depen-
Line 6: dencies. The most common example of a managed dependency is an application
Line 7: database—a database no other application has access to.
Line 8:  Running tests against a real database provides bulletproof protection against
Line 9: regressions, but those tests aren’t easy to set up. This chapter shows the preliminary
Line 10: steps you need to take before you can start testing your database: it covers keeping
Line 11: track of the database schema, explains the difference between the state-based and
Line 12: migration-based database delivery approaches, and demonstrates why you should
Line 13: choose the latter over the former.
Line 14:  After learning the basics, you’ll see how to manage transactions during the test,
Line 15: clean up leftover data, and keep tests small by eliminating insignificant parts and
Line 16: amplifying the essentials. This chapter focuses on relational databases, but many of
Line 17: This chapter covers
Line 18: Prerequisites for testing the database
Line 19: Database testing best practices
Line 20: Test data life cycle
Line 21: Managing database transactions in tests
Line 22: 
Line 23: --- 페이지 252 ---
Line 24: 230
Line 25: CHAPTER 10
Line 26: Testing the database
Line 27: the same principles are applicable to other types of data stores such as document-ori-
Line 28: ented databases or even plain text file storages.
Line 29: 10.1
Line 30: Prerequisites for testing the database
Line 31: As you might recall from chapter 8, managed dependencies should be included as-is
Line 32: in integration tests. That makes working with those dependencies more laborious
Line 33: than unmanaged ones because using a mock is out of the question. But even before
Line 34: you start writing tests, you must take preparatory steps to enable integration testing. In
Line 35: this section, you’ll see these prerequisites:
Line 36: Keeping the database in the source control system
Line 37: Using a separate database instance for every developer
Line 38: Applying the migration-based approach to database delivery
Line 39: Like almost everything in testing, though, practices that facilitate testing also improve
Line 40: the health of your database in general. You’ll get value out of those practices even if
Line 41: you don’t write integration tests.
Line 42: 10.1.1 Keeping the database in the source control system
Line 43: The first step on the way to testing the database is treating the database schema as reg-
Line 44: ular code. Just as with regular code, a database schema is best stored in a source con-
Line 45: trol system such as Git.
Line 46:  I’ve worked on projects where programmers maintained a dedicated database
Line 47: instance, which served as a reference point (a model database). During development,
Line 48: all schema changes accumulated in that instance. Upon production deployments, the
Line 49: team compared the production and model databases, used a special tool to generate
Line 50: upgrade scripts, and ran those scripts in production (figure 10.1).
Line 51: Model
Line 52: database
Line 53: Production
Line 54: database
Line 55: Compare
Line 56: Modiﬁcations by
Line 57: programmers
Line 58: Upgrade
Line 59: scripts
Line 60: Generate
Line 61: Apply
Line 62: Comparison
Line 63: tool
Line 64: Figure 10.1
Line 65: Having a dedicated instance as a model database is an anti-pattern. The database 
Line 66: schema is best stored in a source control system.
Line 67: 
Line 68: --- 페이지 253 ---
Line 69: 231
Line 70: Prerequisites for testing the database
Line 71: Using a model database is a horrible way to maintain database schema. That’s because
Line 72: there’s
Line 73: No change history—You can’t trace the database schema back to some point in
Line 74: the past, which might be important when reproducing bugs in production.
Line 75: No single source of truth—The model database becomes a competing source of
Line 76: truth about the state of development. Maintaining two such sources (Git and
Line 77: the model database) creates an additional burden.
Line 78: On the other hand, keeping all the database schema updates in the source control sys-
Line 79: tem helps you to maintain a single source of truth and also to track database changes
Line 80: along with the changes of regular code. No modifications to the database structure
Line 81: should be made outside of the source control. 
Line 82: 10.1.2 Reference data is part of the database schema
Line 83: When it comes to the database schema, the usual suspects are tables, views, indexes,
Line 84: stored procedures, and anything else that forms a blueprint of how the database is
Line 85: constructed. The schema itself is represented in the form of SQL scripts. You
Line 86: should be able to use those scripts to create a fully functional, up-to-date database
Line 87: instance of your own at any time during development. However, there’s another
Line 88: part of the database that belongs to the database schema but is rarely viewed as
Line 89: such: reference data.
Line 90: DEFINITION
Line 91: Reference data is data that must be prepopulated in order for the
Line 92: application to operate properly.
Line 93: Take the CRM system from the earlier chapters, for example. Its users can be either of
Line 94: type Customer or type Employee. Let’s say that you want to create a table with all user
Line 95: types and introduce a foreign key constraint from User to that table. Such a constraint
Line 96: would provide an additional guarantee that the application won’t ever assign a user a
Line 97: nonexistent type. In this scenario, the content of the UserType table would be refer-
Line 98: ence data because the application relies on its existence in order to persist users in the
Line 99: database.
Line 100: TIP
Line 101: There’s a simple way to differentiate reference data from regular data.
Line 102: If your application can modify the data, it’s regular data; if not, it’s refer-
Line 103: ence data.
Line 104: Because reference data is essential for your application, you should keep it in the
Line 105: source control system along with tables, views, and other parts of the database schema,
Line 106: in the form of SQL INSERT statements.
Line 107:  Note that although reference data is normally stored separately from regular data,
Line 108: the two can sometimes coexist in the same table. To make this work, you need to intro-
Line 109: duce a flag differentiating data that can be modified (regular data) from data that can’t
Line 110: be modified (reference data) and forbid your application from changing the latter. 
Line 111: 
Line 112: --- 페이지 254 ---
Line 113: 232
Line 114: CHAPTER 10
Line 115: Testing the database
Line 116: 10.1.3 Separate instance for every developer
Line 117: It’s difficult enough to run tests against a real database. It becomes even more difficult
Line 118: if you have to share that database with other developers. The use of a shared database
Line 119: hinders the development process because
Line 120: Tests run by different developers interfere with each other.
Line 121: Non-backward-compatible changes can block the work of other developers.
Line 122: Keep a separate database instance for every developer, preferably on that developer’s
Line 123: own machine in order to maximize test execution speed. 
Line 124: 10.1.4 State-based vs. migration-based database delivery
Line 125: There are two major approaches to database delivery: state-based and migration-based.
Line 126: The migration-based approach is more difficult to implement and maintain initially,
Line 127: but it works much better than the state-based approach in the long run.
Line 128: THE STATE-BASED APPROACH
Line 129: The state-based approach to database delivery is similar to what I described in figure
Line 130: 10.1. You also have a model database that you maintain throughout development.
Line 131: During deployments, a comparison tool generates scripts for the production database
Line 132: to bring it up to date with the model database. The difference is that with the state-
Line 133: based approach, you don’t actually have a physical model database as a source of
Line 134: truth. Instead, you have SQL scripts that you can use to create that database. The
Line 135: scripts are stored in the source control.
Line 136:  In the state-based approach, the comparison tool does all the hard lifting. What-
Line 137: ever the state of the production database, the tool does everything needed to get it in
Line 138: sync with the model database: delete unnecessary tables, create new ones, rename col-
Line 139: umns, and so on. 
Line 140: THE MIGRATION-BASED APPROACH
Line 141: On the other hand, the migration-based approach emphasizes the use of explicit
Line 142: migrations that transition the database from one version to another (figure 10.2).
Line 143: With this approach, you don’t use tools to automatically synchronize the production
Line 144: and development databases; you come up with upgrade scripts yourself. However, a
Line 145: database comparison tool can still be useful when detecting undocumented changes
Line 146: in the production database schema.
Line 147: CREATE TABLE
Line 148: dbo.Customer (…)
Line 149: ALTER TABLE
Line 150: dbo.Customer (…)
Line 151: CREATE TABLE
Line 152: dbo.User (…)
Line 153: Migration 1
Line 154: Migration 2
Line 155: Migration 3
Line 156: Figure 10.2
Line 157: The migration-based approach to database delivery emphasizes the use of explicit 
Line 158: migrations that transition the database from one version to another.
Line 159: 
Line 160: --- 페이지 255 ---
Line 161: 233
Line 162: Prerequisites for testing the database
Line 163: In the migration-based approach, migrations and not the database state become the
Line 164: artifacts you store in the source control. Migrations are usually represented with
Line 165: plain SQL scripts (popular tools include Flyway [https://flywaydb.org] and Liquibase
Line 166: [https://liquibase.org]), but they can also be written using a DSL-like language that
Line 167: gets translated into SQL. The following example shows a C# class that represents a
Line 168: database migration with the help of the FluentMigrator library (https://github.com/
Line 169: fluentmigrator/fluentmigrator):
Line 170: [Migration(1)]
Line 171:           
Line 172: public class CreateUserTable : Migration
Line 173: {
Line 174: public override void Up()       
Line 175: {
Line 176: Create.Table("Users");
Line 177: }
Line 178: public override void Down()    
Line 179: {
Line 180: Delete.Table("Users");
Line 181: }
Line 182: }
Line 183: PREFER THE MIGRATION-BASED APPROACH OVER THE STATE-BASED ONE
Line 184: The difference between the state-based and migration-based approaches to database
Line 185: delivery comes down to (as their names imply) state versus migrations (see figure 10.3):
Line 186: The state-based approach makes the state explicit (by virtue of storing that
Line 187: state in the source control) and lets the comparison tool implicitly control the
Line 188: migrations.
Line 189: The migration-based approach makes the migrations explicit but leaves the state
Line 190: implicit. It’s impossible to view the database state directly; you have to assemble
Line 191: it from the migrations.
Line 192: Migration 
Line 193: number
Line 194: Forward 
Line 195: migration
Line 196: Backward migration (helpful 
Line 197: when downgrading to an 
Line 198: earlier database version to 
Line 199: reproduce a bug)
Line 200: State-based
Line 201: approach
Line 202: State of the database
Line 203: Migration mechanism
Line 204: Migration-based
Line 205: approach
Line 206: Implicit
Line 207: Implicit
Line 208: Explicit
Line 209: Explicit
Line 210: Figure 10.3
Line 211: The state-based approach makes the state explicit and 
Line 212: migrations implicit; the migration-based approach makes the opposite choice.
Line 213: 
Line 214: --- 페이지 256 ---
Line 215: 234
Line 216: CHAPTER 10
Line 217: Testing the database
Line 218: Such a distinction leads to different sets of trade-offs. The explicitness of the database
Line 219: state makes it easier to handle merge conflicts, while explicit migrations help to tackle
Line 220: data motion.
Line 221: DEFINITION
Line 222: Data motion is the process of changing the shape of existing data
Line 223: so that it conforms to the new database schema.
Line 224: Although the alleviation of merge conflicts and the ease of data motion might look
Line 225: like equally important benefits, in the vast majority of projects, data motion is much more
Line 226: important than merge conflicts. Unless you haven’t yet released your application to pro-
Line 227: duction, you always have data that you can’t simply discard.
Line 228:  For example, when splitting a Name column into FirstName and LastName, you not
Line 229: only have to drop the Name column and create the new FirstName and LastName col-
Line 230: umns, but you also have to write a script to split all existing names into two pieces.
Line 231: There is no easy way to implement this change using the state-driven approach; com-
Line 232: parison tools are awful when it comes to managing data. The reason is that while the
Line 233: database schema itself is objective, meaning there is only one way to interpret it, data
Line 234: is context-dependent. No tool can make reliable assumptions about data when gener-
Line 235: ating upgrade scripts. You have to apply domain-specific rules in order to implement
Line 236: proper transformations.
Line 237:  As a result, the state-based approach is impractical in the vast majority of projects.
Line 238: You can use it temporarily, though, while the project still has not been released to pro-
Line 239: duction. After all, test data isn’t that important, and you can re-create it every time you
Line 240: change the database. But once you release the first version, you will have to switch to
Line 241: the migration-based approach in order to handle data motion properly.
Line 242: TIP
Line 243: Apply every modification to the database schema (including reference
Line 244: data) through migrations. Don’t modify migrations once they are committed
Line 245: to the source control. If a migration is incorrect, create a new migration
Line 246: instead of fixing the old one. Make exceptions to this rule only when the
Line 247: incorrect migration can lead to data loss. 
Line 248: 10.2
Line 249: Database transaction management
Line 250: Database transaction management is a topic that’s important for both production and
Line 251: test code. Proper transaction management in production code helps you avoid data
Line 252: inconsistencies. In tests, it helps you verify integration with the database in a close-to-
Line 253: production setting.
Line 254:  In this section, I’ll first show how to handle transactions in the production code
Line 255: (the controller) and then demonstrate how to use them in integration tests. I’ll con-
Line 256: tinue using the same CRM project you saw in the earlier chapters as an example.
Line 257: 
Line 258: --- 페이지 257 ---
Line 259: 235
Line 260: Database transaction management
Line 261: 10.2.1 Managing database transactions in production code
Line 262: Our sample CRM project uses the Database class to work with User and Company.
Line 263: Database creates a separate SQL connection on each method call. Every such connec-
Line 264: tion implicitly opens an independent transaction behind the scenes, as the following
Line 265: listing shows.
Line 266: public class Database
Line 267: {
Line 268: private readonly string _connectionString;
Line 269: public Database(string connectionString)
Line 270: {
Line 271: _connectionString = connectionString;
Line 272: }
Line 273: public void SaveUser(User user)
Line 274: {
Line 275: bool isNewUser = user.UserId == 0;
Line 276: using (var connection =
Line 277: new SqlConnection(_connectionString))      
Line 278: {
Line 279: /* Insert or update the user depending on isNewUser */
Line 280: }
Line 281: }
Line 282: public void SaveCompany(Company company)
Line 283: {
Line 284: using (var connection =
Line 285: new SqlConnection(_connectionString))      
Line 286: {
Line 287: /* Update only; there's only one company */
Line 288: }
Line 289: }
Line 290: }
Line 291: As a result, the user controller creates a total of four database transactions during a
Line 292: single business operation, as shown in the following listing.
Line 293: public string ChangeEmail(int userId, string newEmail)
Line 294: {
Line 295: object[] userData = _database.GetUserById(userId);    
Line 296: User user = UserFactory.Create(userData);
Line 297: string error = user.CanChangeEmail();
Line 298: if (error != null)
Line 299: return error;
Line 300: Listing 10.1
Line 301: Class that enables access to the database
Line 302: Listing 10.2
Line 303: User controller
Line 304: Opens a
Line 305: database
Line 306: transaction
Line 307: Opens a new 
Line 308: database 
Line 309: transaction
Line 310: 
Line 311: --- 페이지 258 ---
Line 312: 236
Line 313: CHAPTER 10
Line 314: Testing the database
Line 315: object[] companyData = _database.GetCompany();        
Line 316: Company company = CompanyFactory.Create(companyData);
Line 317: user.ChangeEmail(newEmail, company);
Line 318: _database.SaveCompany(company);                       
Line 319: _database.SaveUser(user);                             
Line 320: _eventDispatcher.Dispatch(user.DomainEvents);
Line 321: return "OK";
Line 322: }
Line 323: It’s fine to open multiple transactions during read-only operations: for example, when
Line 324: returning user information to the external client. But if the business operation
Line 325: involves data mutation, all updates taking place during that operation should be
Line 326: atomic in order to avoid inconsistencies. For example, the controller can successfully
Line 327: persist the company but then fail when saving the user due to a database connectivity
Line 328: issue. As a result, the company’s NumberOfEmployees can become inconsistent with
Line 329: the total number of Employee users in the database.
Line 330: DEFINITION
Line 331: Atomic updates are executed in an all-or-nothing manner. Each
Line 332: update in the set of atomic updates must either be complete in its entirety or
Line 333: have no effect whatsoever.
Line 334: SEPARATING DATABASE CONNECTIONS FROM DATABASE TRANSACTIONS
Line 335: To avoid potential inconsistencies, you need to introduce a separation between two
Line 336: types of decisions:
Line 337: What data to update
Line 338: Whether to keep the updates or roll them back
Line 339: Such a separation is important because the controller can’t make these decisions
Line 340: simultaneously. It only knows whether the updates can be kept when all the steps in
Line 341: the business operation have succeeded. And it can only take those steps by accessing
Line 342: the database and trying to make the updates. You can implement the separation
Line 343: between these responsibilities by splitting the Database class into repositories and a
Line 344: transaction:
Line 345: Repositories are classes that enable access to and modification of the data in the
Line 346: database. There will be two repositories in our sample project: one for User and
Line 347: the other for Company.
Line 348: A transaction is a class that either commits or rolls back data updates in full. This
Line 349: will be a custom class relying on the underlying database’s transactions to pro-
Line 350: vide atomicity of data modification.
Line 351: Not only do repositories and transactions have different responsibilities, but they also
Line 352: have different lifespans. A transaction lives during the whole business operation and is
Line 353: disposed of at the very end of it. A repository, on the other hand, is short-lived. You
Line 354: Opens a new 
Line 355: database 
Line 356: transaction
Line 357: 
Line 358: --- 페이지 259 ---
Line 359: 237
Line 360: Database transaction management
Line 361: can dispose of a repository as soon as the call to the database is completed. As a result,
Line 362: repositories always work on top of the current transaction. When connecting to the
Line 363: database, a repository enlists itself into the transaction so that any data modifications
Line 364: made during that connection can later be rolled back by the transaction.
Line 365:  Figure 10.4 shows how the communication between the controller and the data-
Line 366: base looks in listing 10.2. Each database call is wrapped into its own transaction;
Line 367: updates are not atomic.
Line 368: Figure 10.5 shows the application after the introduction of explicit transactions. The
Line 369: transaction mediates interactions between the controller and the database. All four
Line 370: database calls are still there, but now data modifications are either committed or
Line 371: rolled back in full.
Line 372: The following listing shows the controller after introducing a transaction and repositories.
Line 373: public class UserController
Line 374: {
Line 375: private readonly Transaction _transaction;
Line 376: private readonly UserRepository _userRepository;
Line 377: Listing 10.3
Line 378: User controller, repositories, and a transaction
Line 379: Database
Line 380: GetUserById
Line 381: Controller
Line 382: SaveCompany
Line 383: GetCompany
Line 384: SaveUser
Line 385: Figure 10.4
Line 386: Wrapping each 
Line 387: database call into a separate 
Line 388: transaction introduces a risk of 
Line 389: inconsistencies due to hardware or 
Line 390: software failures. For example, the 
Line 391: application can update the number of 
Line 392: employees in the company but not 
Line 393: the employees themselves.
Line 394: Transaction
Line 395: Database
Line 396: Controller
Line 397: Commit tran
Line 398: Commit tran
Line 399: SaveUser
Line 400: SaveUser
Line 401: SaveCompany
Line 402: SaveCompany
Line 403: GetCompany
Line 404: GetCompany
Line 405: GetUserById
Line 406: GetUserById
Line 407: Open tran
Line 408: Open tran
Line 409: Figure 10.5
Line 410: The transaction mediates interactions between the controller and the database and 
Line 411: thus enables atomic data modification.
Line 412: 
Line 413: --- 페이지 260 ---
Line 414: 238
Line 415: CHAPTER 10
Line 416: Testing the database
Line 417: private readonly CompanyRepository _companyRepository;
Line 418: private readonly EventDispatcher _eventDispatcher;
Line 419: public UserController(
Line 420: Transaction transaction,     
Line 421: MessageBus messageBus,
Line 422: IDomainLogger domainLogger)
Line 423: {
Line 424: _transaction = transaction;
Line 425: _userRepository = new UserRepository(transaction);
Line 426: _companyRepository = new CompanyRepository(transaction);
Line 427: _eventDispatcher = new EventDispatcher(
Line 428: messageBus, domainLogger);
Line 429: }
Line 430: public string ChangeEmail(int userId, string newEmail)
Line 431: {
Line 432: object[] userData = _userRepository           
Line 433: .GetUserById(userId);
Line 434:            
Line 435: User user = UserFactory.Create(userData);
Line 436: string error = user.CanChangeEmail();
Line 437: if (error != null)
Line 438: return error;
Line 439: object[] companyData = _companyRepository     
Line 440: .GetCompany();
Line 441:       
Line 442: Company company = CompanyFactory.Create(companyData);
Line 443: user.ChangeEmail(newEmail, company);
Line 444: _companyRepository.SaveCompany(company);      
Line 445: _userRepository.SaveUser(user);
Line 446:       
Line 447: _eventDispatcher.Dispatch(user.DomainEvents);
Line 448: _transaction.Commit();     
Line 449: return "OK";
Line 450: }
Line 451: }
Line 452: public class UserRepository
Line 453: {
Line 454: private readonly Transaction _transaction;
Line 455: public UserRepository(Transaction transaction)    
Line 456: {
Line 457: _transaction = transaction;
Line 458: }
Line 459: /* ... */
Line 460: }
Line 461: public class Transaction : IDisposable
Line 462: {
Line 463: Accepts a 
Line 464: transaction
Line 465: Uses the
Line 466: repositories
Line 467: instead
Line 468: of the
Line 469: Database
Line 470: class
Line 471: Commits the 
Line 472: transaction 
Line 473: on success
Line 474: Injects a 
Line 475: transaction into 
Line 476: a repository
Line 477: 
Line 478: --- 페이지 261 ---
Line 479: 239
Line 480: Database transaction management
Line 481: public void Commit() { /* ... */ }
Line 482: public void Dispose() { /* ... */ }
Line 483: }
Line 484: The internals of the Transaction class aren’t important, but if you’re curious, I’m
Line 485: using .NET’s standard TransactionScope behind the scenes. The important part
Line 486: about Transaction is that it contains two methods:
Line 487: 
Line 488: Commit()marks the transaction as successful. This is only called when the busi-
Line 489: ness operation itself has succeeded and all data modifications are ready to be
Line 490: persisted.
Line 491: 
Line 492: Dispose()ends the transaction. This is called indiscriminately at the end of the
Line 493: business operation. If Commit() was previously invoked, Dispose() persists all
Line 494: data updates; otherwise, it rolls them back.
Line 495: Such a combination of Commit() and Dispose() guarantees that the database is
Line 496: altered only during happy paths (the successful execution of the business scenario).
Line 497: That’s why Commit() resides at the very end of the ChangeEmail() method. In the
Line 498: event of any error, be it a validation error or an unhandled exception, the execution
Line 499: flow returns early and thereby prevents the transaction from being committed.
Line 500:  Commit() is invoked by the controller because this method call requires decision-
Line 501: making. There’s no decision-making involved in calling Dispose(), though, so you
Line 502: can delegate that method call to a class from the infrastructure layer. The same class
Line 503: that instantiates the controller and provides it with the necessary dependencies
Line 504: should also dispose of the transaction once the controller is done working.
Line 505:  Notice how UserRepository requires Transaction as a constructor parameter.
Line 506: This explicitly shows that repositories always work on top of transactions; a repository
Line 507: can’t call the database on its own. 
Line 508: UPGRADING THE TRANSACTION TO A UNIT OF WORK
Line 509: The introduction of repositories and a transaction is a good way to avoid potential
Line 510: data inconsistencies, but there’s an even better approach. You can upgrade the
Line 511: Transaction class to a unit of work.
Line 512: DEFINITION
Line 513: A unit of work maintains a list of objects affected by a business
Line 514: operation. Once the operation is completed, the unit of work figures out all
Line 515: updates that need to be done to alter the database and executes those
Line 516: updates as a single unit (hence the pattern name).
Line 517: The main advantage of a unit of work over a plain transaction is the deferral of
Line 518: updates. Unlike a transaction, a unit of work executes all updates at the end of the
Line 519: business operation, thus minimizing the duration of the underlying database transac-
Line 520: tion and reducing data congestion (see figure 10.6). Often, this pattern also helps to
Line 521: reduce the number of database calls.
Line 522: NOTE
Line 523: Database transactions also implement the unit-of-work pattern.
Line 524: 
Line 525: --- 페이지 262 ---
Line 526: 240
Line 527: CHAPTER 10
Line 528: Testing the database
Line 529: Maintaining a list of modified objects and then figuring out what SQL script to gener-
Line 530: ate can look like a lot of work. In reality, though, you don’t need to do that work your-
Line 531: self. Most object-relational mapping (ORM) libraries implement the unit-of-work
Line 532: pattern for you. In .NET, for example, you can use NHibernate or Entity Framework,
Line 533: both of which provide classes that do all the hard lifting (those classes are ISession
Line 534: and DbContext, respectively). The following listing shows how UserController looks
Line 535: in combination with Entity Framework.
Line 536: public class UserController
Line 537: {
Line 538: private readonly CrmContext _context;
Line 539: private readonly UserRepository _userRepository;
Line 540: private readonly CompanyRepository _companyRepository;
Line 541: private readonly EventDispatcher _eventDispatcher;
Line 542: public UserController(
Line 543: CrmContext context,                     
Line 544: MessageBus messageBus,
Line 545: IDomainLogger domainLogger)
Line 546: {
Line 547: _context = context;
Line 548: _userRepository = new UserRepository(
Line 549: context);                           
Line 550: _companyRepository = new CompanyRepository(
Line 551: context);                           
Line 552: _eventDispatcher = new EventDispatcher(
Line 553: messageBus, domainLogger);
Line 554: }
Line 555: public string ChangeEmail(int userId, string newEmail)
Line 556: {
Line 557: User user = _userRepository.GetUserById(userId);
Line 558: Listing 10.4
Line 559: User controller with Entity Framework
Line 560: Unit of work
Line 561: GetUserById
Line 562: Database
Line 563: SaveCompany
Line 564: GetCompany
Line 565: Controller
Line 566: SaveUser
Line 567: Create
Line 568: SaveChanges
Line 569: GetUserById
Line 570: GetCompany
Line 571: Save all
Line 572: Figure 10.6
Line 573: A unit of work executes all updates at the end of the business operation. The updates 
Line 574: are still wrapped in a database transaction, but that transaction lives for a shorter period of time, 
Line 575: thus reducing data congestion.
Line 576: CrmContext
Line 577: replaces
Line 578: Transaction.
Line 579: 
Line 580: --- 페이지 263 ---
Line 581: 241
Line 582: Database transaction management
Line 583: string error = user.CanChangeEmail();
Line 584: if (error != null)
Line 585: return error;
Line 586: Company company = _companyRepository.GetCompany();
Line 587: user.ChangeEmail(newEmail, company);
Line 588: _companyRepository.SaveCompany(company);
Line 589: _userRepository.SaveUser(user);
Line 590: _eventDispatcher.Dispatch(user.DomainEvents);
Line 591: _context.SaveChanges();  
Line 592: return "OK";
Line 593: }
Line 594: }
Line 595: CrmContext is a custom class that contains mapping between the domain model and
Line 596: the database (it inherits from Entity Framework’s DbContext). The controller in list-
Line 597: ing 10.4 uses CrmContext instead of Transaction. As a result,
Line 598: Both repositories now work on top of CrmContext, just as they worked on top of
Line 599: Transaction in the previous version.
Line 600: The controller commits changes to the database via context.SaveChanges()
Line 601: instead of transaction.Commit().
Line 602: Notice that there’s no need for UserFactory and CompanyFactory anymore because
Line 603: Entity Framework now serves as a mapper between the raw database data and
Line 604: domain objects.
Line 605: Data inconsistencies in non-relational databases
Line 606: It’s easy to avoid data inconsistencies when using a relational database: all major
Line 607: relational databases provide atomic updates that can span as many rows as needed.
Line 608: But how do you achieve the same level of protection with a non-relational database
Line 609: such as MongoDB?
Line 610: The problem with most non-relational databases is the lack of transactions in the
Line 611: classical sense; atomic updates are guaranteed only within a single document. If a
Line 612: business operation affects multiple documents, it becomes prone to inconsisten-
Line 613: cies. (In non-relational databases, a document is the equivalent of a row.)
Line 614: Non-relational databases approach inconsistencies from a different angle: they
Line 615: require you to design your documents such that no business operation modifies more
Line 616: than one of those documents at a time. This is possible because documents are
Line 617: more flexible than rows in relational databases. A single document can store data of
Line 618: any shape and complexity and thus capture side effects of even the most sophisti-
Line 619: cated business operations.
Line 620: CrmContext 
Line 621: replaces 
Line 622: Transaction.
Line 623: 
Line 624: --- 페이지 264 ---
Line 625: 242
Line 626: CHAPTER 10
Line 627: Testing the database
Line 628: 10.2.2 Managing database transactions in integration tests
Line 629: When it comes to managing database transactions in integration tests, adhere to the
Line 630: following guideline: don’t reuse database transactions or units of work between sections of the
Line 631: test. The following listing shows an example of reusing CrmContext in the integration
Line 632: test after switching that test to Entity Framework.
Line 633: [Fact]
Line 634: public void Changing_email_from_corporate_to_non_corporate()
Line 635: {
Line 636: using (var context =
Line 637:    
Line 638: new CrmContext(ConnectionString))   
Line 639: {
Line 640: // Arrange
Line 641: var userRepository =
Line 642:          
Line 643: new UserRepository(context);
Line 644:          
Line 645: var companyRepository =
Line 646:          
Line 647: new CompanyRepository(context);         
Line 648: var user = new User(0, "user@mycorp.com",
Line 649: UserType.Employee, false);
Line 650: userRepository.SaveUser(user);
Line 651: var company = new Company("mycorp.com", 1);
Line 652: companyRepository.SaveCompany(company);
Line 653: context.SaveChanges();                      
Line 654: var busSpy = new BusSpy();
Line 655: var messageBus = new MessageBus(busSpy);
Line 656: var loggerMock = new Mock<IDomainLogger>();
Line 657: var sut = new UserController(
Line 658: context,                     
Line 659: messageBus,
Line 660: loggerMock.Object);
Line 661: // Act
Line 662: string result = sut.ChangeEmail(user.UserId, "new@gmail.com");
Line 663: // Assert
Line 664: Assert.Equal("OK", result);
Line 665: User userFromDb = userRepository     
Line 666: .GetUserById(user.UserId);       
Line 667: (continued)
Line 668: In domain-driven design, there’s a guideline saying that you shouldn’t modify more
Line 669: than one aggregate per business operation. This guideline serves the same goal: pro-
Line 670: tecting you from data inconsistencies. The guideline is only applicable to systems
Line 671: that work with document databases, though, where each document corresponds to
Line 672: one aggregate. 
Line 673: Listing 10.5
Line 674: Integration test reusing CrmContext
Line 675: Creates a 
Line 676: context
Line 677: Uses the context 
Line 678: in the arrange 
Line 679: section . . .
Line 680: . . . in act . . .
Line 681: . . . and in assert
Line 682: 
Line 683: --- 페이지 265 ---
Line 684: 243
Line 685: Test data life cycle
Line 686: Assert.Equal("new@gmail.com", userFromDb.Email);
Line 687: Assert.Equal(UserType.Customer, userFromDb.Type);
Line 688: Company companyFromDb = companyRepository     
Line 689: .GetCompany();
Line 690:      
Line 691: Assert.Equal(0, companyFromDb.NumberOfEmployees);
Line 692: busSpy.ShouldSendNumberOfMessages(1)
Line 693: .WithEmailChangedMessage(user.UserId, "new@gmail.com");
Line 694: loggerMock.Verify(
Line 695: x => x.UserTypeHasChanged(
Line 696: user.UserId, UserType.Employee, UserType.Customer),
Line 697: Times.Once);
Line 698: }
Line 699: }
Line 700: This test uses the same instance of CrmContext in all three sections: arrange, act, and
Line 701: assert. This is a problem because such reuse of the unit of work creates an environment
Line 702: that doesn’t match what the controller experiences in production. In production, each
Line 703: business operation has an exclusive instance of CrmContext. That instance is created
Line 704: right before the controller method invocation and is disposed of immediately after.
Line 705:  To avoid the risk of inconsistent behavior, integration tests should replicate the
Line 706: production environment as closely as possible, which means the act section must not
Line 707: share CrmContext with anyone else. The arrange and assert sections must get their
Line 708: own instances of CrmContext too, because, as you might remember from chapter 8,
Line 709: it’s important to check the state of the database independently of the data used as
Line 710: input parameters. And although the assert section does query the user and the com-
Line 711: pany independently of the arrange section, these sections still share the same database
Line 712: context. That context can (and many ORMs do) cache the requested data for perfor-
Line 713: mance improvements.
Line 714: TIP
Line 715: Use at least three transactions or units of work in an integration test: one
Line 716: per each arrange, act, and assert section. 
Line 717: 10.3
Line 718: Test data life cycle
Line 719: The shared database raises the problem of isolating integration tests from each other.
Line 720: To solve this problem, you need to
Line 721: Execute integration tests sequentially.
Line 722: Remove leftover data between test runs.
Line 723: Overall, your tests shouldn’t depend on the state of the database. Your tests should
Line 724: bring that state to the required condition on their own.
Line 725: 10.3.1 Parallel vs. sequential test execution
Line 726: Parallel execution of integration tests involves significant effort. You have to ensure
Line 727: that all test data is unique so no database constraints are violated and tests don’t acci-
Line 728: dentally pick up input data after each other. Cleaning up leftover data also becomes
Line 729: . . . and in assert
Line 730: 
Line 731: --- 페이지 266 ---
Line 732: 244
Line 733: CHAPTER 10
Line 734: Testing the database
Line 735: trickier. It’s more practical to run integration tests sequentially rather than spend time
Line 736: trying to squeeze additional performance out of them.
Line 737:  Most unit testing frameworks allow you to define separate test collections and
Line 738: selectively disable parallelization in them. Create two such collections (for unit and
Line 739: integration tests), and then disable test parallelization in the collection with the inte-
Line 740: gration tests.
Line 741:  As an alternative, you could parallelize tests using containers. For example, you
Line 742: could put the model database on a Docker image and instantiate a new container
Line 743: from that image for each integration test. In practice, though, this approach creates
Line 744: too much of an additional maintenance burden. With Docker, you not only have to
Line 745: keep track of the database itself, but you also need to
Line 746: Maintain Docker images
Line 747: Make sure each test gets its own container instance
Line 748: Batch integration tests (because you most likely won’t be able to create all con-
Line 749: tainer instances at once)
Line 750: Dispose of used-up containers
Line 751: I don’t recommend using containers unless you absolutely need to minimize your
Line 752: integration tests’ execution time. Again, it’s more practical to have just one database
Line 753: instance per developer. You can run that single instance in Docker, though. I advocate
Line 754: against premature parallelization, not the use of Docker per se. 
Line 755: 10.3.2 Clearing data between test runs
Line 756: There are four options to clean up leftover data between test runs:
Line 757: Restoring a database backup before each test—This approach addresses the problem
Line 758: of data cleanup but is much slower than the other three options. Even with con-
Line 759: tainers, the removal of a container instance and creation of a new one usually
Line 760: takes several seconds, which quickly adds to the total test suite execution time.
Line 761: Cleaning up data at the end of a test—This method is fast but susceptible to skip-
Line 762: ping the cleanup phase. If the build server crashes in the middle of the test, or
Line 763: you shut down the test in the debugger, the input data remains in the database
Line 764: and affects further test runs.
Line 765: Wrapping each test in a database transaction and never committing it—In this case, all
Line 766: changes made by the test and the SUT are rolled back automatically. This
Line 767: approach solves the problem of skipping the cleanup phase but poses another
Line 768: issue: the introduction of an overarching transaction can lead to inconsistent
Line 769: behavior between the production and test environments. It’s the same problem
Line 770: as with reusing a unit of work: the additional transaction creates a setup that’s
Line 771: different than that in production.
Line 772: Cleaning up data at the beginning of a test—This is the best option. It works fast,
Line 773: doesn’t result in inconsistent behavior, and isn’t prone to accidentally skipping
Line 774: the cleanup phase.
Line 775: 
Line 776: --- 페이지 267 ---
Line 777: 245
Line 778: Test data life cycle
Line 779: TIP
Line 780: There’s no need for a separate teardown phase; implement that phase as
Line 781: part of the arrange section.
Line 782: The data removal itself must be done in a particular order, to honor the database’s
Line 783: foreign key constraints. I sometimes see people use sophisticated algorithms to figure
Line 784: out relationships between tables and automatically generate the deletion script or
Line 785: even disable all integrity constraints and re-enable them afterward. This is unneces-
Line 786: sary. Write the SQL script manually: it’s simpler and gives you more granular control
Line 787: over the deletion process.
Line 788:  Introduce a base class for all integration tests, and put the deletion script there. With
Line 789: such a base class, you will have the script run automatically at the start of each test, as
Line 790: shown in the following listing.
Line 791: public abstract class IntegrationTests
Line 792: {
Line 793: private const string ConnectionString = "...";
Line 794: protected IntegrationTests()
Line 795: {
Line 796: ClearDatabase();
Line 797: }
Line 798: private void ClearDatabase()
Line 799: {
Line 800: string query =
Line 801: "DELETE FROM dbo.[User];" +    
Line 802: "DELETE FROM dbo.Company;";    
Line 803: using (var connection = new SqlConnection(ConnectionString))
Line 804: {
Line 805: var command = new SqlCommand(query, connection)
Line 806: {
Line 807: CommandType = CommandType.Text
Line 808: };
Line 809: connection.Open();
Line 810: command.ExecuteNonQuery();
Line 811: }
Line 812: }
Line 813: }
Line 814: TIP
Line 815: The deletion script must remove all regular data but none of the refer-
Line 816: ence data. Reference data, along with the rest of the database schema, should
Line 817: be controlled solely by migrations. 
Line 818: Listing 10.6
Line 819: Base class for integration tests
Line 820: Deletion 
Line 821: script
Line 822: 
Line 823: --- 페이지 268 ---
Line 824: 246
Line 825: CHAPTER 10
Line 826: Testing the database
Line 827: 10.3.3 Avoid in-memory databases
Line 828: Another way to isolate integration tests from each other is by replacing the database
Line 829: with an in-memory analog, such as SQLite. In-memory databases can seem beneficial
Line 830: because they
Line 831: Don’t require removal of test data
Line 832: Work faster
Line 833: Can be instantiated for each test run
Line 834: Because in-memory databases aren’t shared dependencies, integration tests in effect
Line 835: become unit tests (assuming the database is the only managed dependency in the
Line 836: project), similar to the approach with containers described in section 10.3.1.
Line 837:  In spite of all these benefits, I don’t recommend using in-memory databases
Line 838: because they aren’t consistent functionality-wise with regular databases. This is, once
Line 839: again, the problem of a mismatch between production and test environments. Your
Line 840: tests can easily run into false positives or (worse!) false negatives due to the differ-
Line 841: ences between the regular and in-memory databases. You’ll never gain good protec-
Line 842: tion with such tests and will have to do a lot of regression testing manually anyway.
Line 843: TIP
Line 844: Use the same database management system (DBMS) in tests as in pro-
Line 845: duction. It’s usually fine for the version or edition to differ, but the vendor
Line 846: must remain the same. 
Line 847: 10.4
Line 848: Reusing code in test sections
Line 849: Integration tests can quickly grow too large and thus lose ground on the maintainabil-
Line 850: ity metric. It’s important to keep integration tests as short as possible but without cou-
Line 851: pling them to each other or affecting readability. Even the shortest tests shouldn’t
Line 852: depend on one another. They also should preserve the full context of the test scenario
Line 853: and shouldn’t require you to examine different parts of the test class to understand
Line 854: what’s going on.
Line 855:  The best way to shorten integration is by extracting technical, non-business-related
Line 856: bits into private methods or helper classes. As a side bonus, you’ll get to reuse those
Line 857: bits. In this section, I’ll show how to shorten all three sections of the test: arrange, act,
Line 858: and assert.
Line 859: 10.4.1 Reusing code in arrange sections
Line 860: The following listing shows how our integration test looks after providing a separate
Line 861: database context (unit of work) for each of its sections.
Line 862: [Fact]
Line 863: public void Changing_email_from_corporate_to_non_corporate()
Line 864: {
Line 865: // Arrange
Line 866: User user;
Line 867: Listing 10.7
Line 868: Integration test with three database contexts
Line 869: 
Line 870: --- 페이지 269 ---
Line 871: 247
Line 872: Reusing code in test sections
Line 873: using (var context = new CrmContext(ConnectionString))
Line 874: {
Line 875: var userRepository = new UserRepository(context);
Line 876: var companyRepository = new CompanyRepository(context);
Line 877: user = new User(0, "user@mycorp.com",
Line 878: UserType.Employee, false);
Line 879: userRepository.SaveUser(user);
Line 880: var company = new Company("mycorp.com", 1);
Line 881: companyRepository.SaveCompany(company);
Line 882: context.SaveChanges();
Line 883: }
Line 884: var busSpy = new BusSpy();
Line 885: var messageBus = new MessageBus(busSpy);
Line 886: var loggerMock = new Mock<IDomainLogger>();
Line 887: string result;
Line 888: using (var context = new CrmContext(ConnectionString))
Line 889: {
Line 890: var sut = new UserController(
Line 891: context, messageBus, loggerMock.Object);
Line 892: // Act
Line 893: result = sut.ChangeEmail(user.UserId, "new@gmail.com");
Line 894: }
Line 895: // Assert
Line 896: Assert.Equal("OK", result);
Line 897: using (var context = new CrmContext(ConnectionString))
Line 898: {
Line 899: var userRepository = new UserRepository(context);
Line 900: var companyRepository = new CompanyRepository(context);
Line 901: User userFromDb = userRepository.GetUserById(user.UserId);
Line 902: Assert.Equal("new@gmail.com", userFromDb.Email);
Line 903: Assert.Equal(UserType.Customer, userFromDb.Type);
Line 904: Company companyFromDb = companyRepository.GetCompany();
Line 905: Assert.Equal(0, companyFromDb.NumberOfEmployees);
Line 906: busSpy.ShouldSendNumberOfMessages(1)
Line 907: .WithEmailChangedMessage(user.UserId, "new@gmail.com");
Line 908: loggerMock.Verify(
Line 909: x => x.UserTypeHasChanged(
Line 910: user.UserId, UserType.Employee, UserType.Customer),
Line 911: Times.Once);
Line 912: }
Line 913: }
Line 914: As you might remember from chapter 3, the best way to reuse code between the tests’
Line 915: arrange sections is to introduce private factory methods. For example, the following
Line 916: listing creates a user.
Line 917: 
Line 918: --- 페이지 270 ---
Line 919: 248
Line 920: CHAPTER 10
Line 921: Testing the database
Line 922: private User CreateUser(
Line 923: string email, UserType type, bool isEmailConfirmed)
Line 924: {
Line 925: using (var context = new CrmContext(ConnectionString))
Line 926: {
Line 927: var user = new User(0, email, type, isEmailConfirmed);
Line 928: var repository = new UserRepository(context);
Line 929: repository.SaveUser(user);
Line 930: context.SaveChanges();
Line 931: return user;
Line 932: }
Line 933: }
Line 934: You can also define default values for the method’s arguments, as shown next.
Line 935: private User CreateUser(
Line 936: string email = "user@mycorp.com",
Line 937: UserType type = UserType.Employee,
Line 938: bool isEmailConfirmed = false)
Line 939: {
Line 940: /* ... */
Line 941: }
Line 942: With default values, you can specify arguments selectively and thus shorten the test
Line 943: even further. The selective use of arguments also emphasizes which of those argu-
Line 944: ments are relevant to the test scenario.
Line 945: User user = CreateUser(
Line 946: email: "user@mycorp.com",
Line 947: type: UserType.Employee);
Line 948: Listing 10.8
Line 949: A separate method that creates a user
Line 950: Listing 10.9
Line 951: Adding default values to the factory
Line 952: Listing 10.10
Line 953: Using the factory method
Line 954: Object Mother vs. Test Data Builder
Line 955: The pattern shown in listings 10.9 and 10.10 is called the Object Mother. The Object
Line 956: Mother is a class or method that helps create test fixtures (objects the test runs
Line 957: against).
Line 958: There’s another pattern that helps achieve the same goal of reusing code in arrange
Line 959: sections: Test Data Builder. It works similarly to Object Mother but exposes a fluent
Line 960: interface instead of plain methods. Here’s a Test Data Builder usage example:
Line 961: 
Line 962: --- 페이지 271 ---
Line 963: 249
Line 964: Reusing code in test sections
Line 965: WHERE TO PUT FACTORY METHODS
Line 966: When you start distilling the tests’ essentials and move the technicalities out to fac-
Line 967: tory methods, you face the question of where to put those methods. Should they
Line 968: reside in the same class as the tests? The base IntegrationTests class? Or in a sepa-
Line 969: rate helper class?
Line 970:  Start simple. Place the factory methods in the same class by default. Move them
Line 971: into separate helper classes only when code duplication becomes a significant issue.
Line 972: Don’t put the factory methods in the base class; reserve that class for code that has to
Line 973: run in every test, such as data cleanup. 
Line 974: 10.4.2 Reusing code in act sections
Line 975: Every act section in integration tests involves the creation of a database transaction or
Line 976: a unit of work. This is how the act section currently looks in listing 10.7:
Line 977: string result;
Line 978: using (var context = new CrmContext(ConnectionString))
Line 979: {
Line 980: var sut = new UserController(
Line 981: context, messageBus, loggerMock.Object);
Line 982: // Act
Line 983: result = sut.ChangeEmail(user.UserId, "new@gmail.com");
Line 984: }
Line 985: This section can also be reduced. You can introduce a method accepting a delegate
Line 986: with the information of what controller function needs to be invoked. The method
Line 987: will then decorate the controller invocation with the creation of a database context, as
Line 988: shown in the following listing.
Line 989: private string Execute(
Line 990: Func<UserController, string> func,   
Line 991: MessageBus messageBus,
Line 992: IDomainLogger logger)
Line 993: {
Line 994: using (var context = new CrmContext(ConnectionString))
Line 995: {
Line 996: var controller = new UserController(
Line 997: User user = new UserBuilder()
Line 998: .WithEmail("user@mycorp.com")
Line 999: .WithType(UserType.Employee)
Line 1000: .Build();
Line 1001: Test Data Builder slightly improves test readability but requires too much boilerplate.
Line 1002: For that reason, I recommend sticking to the Object Mother (at least in C#, where you
Line 1003: have optional arguments as a language feature).
Line 1004: Listing 10.11
Line 1005: Decorator method
Line 1006: Delegate defines 
Line 1007: a controller 
Line 1008: function.
Line 1009: 
Line 1010: --- 페이지 272 ---
Line 1011: 250
Line 1012: CHAPTER 10
Line 1013: Testing the database
Line 1014: context, messageBus, logger);
Line 1015: return func(controller);
Line 1016: }
Line 1017: }
Line 1018: With this decorator method, you can boil down the test’s act section to just a couple
Line 1019: of lines:
Line 1020: string result = Execute(
Line 1021: x => x.ChangeEmail(user.UserId, "new@gmail.com"),
Line 1022: messageBus, loggerMock.Object);
Line 1023: 10.4.3 Reusing code in assert sections
Line 1024: Finally, the assert section can be shortened, too. The easiest way to do that is to intro-
Line 1025: duce helper methods similar to CreateUser and CreateCompany, as shown in the fol-
Line 1026: lowing listing.
Line 1027: User userFromDb = QueryUser(user.UserId);         
Line 1028: Assert.Equal("new@gmail.com", userFromDb.Email);
Line 1029: Assert.Equal(UserType.Customer, userFromDb.Type);
Line 1030: Company companyFromDb = QueryCompany();           
Line 1031: Assert.Equal(0, companyFromDb.NumberOfEmployees);
Line 1032: You can take a step further and create a fluent interface for these data assertions, sim-
Line 1033: ilar to what you saw in chapter 9 with BusSpy. In C#, a fluent interface on top of exist-
Line 1034: ing domain classes can be implemented using extension methods, as shown in the
Line 1035: following listing.
Line 1036: public static class UserExternsions
Line 1037: {
Line 1038: public static User ShouldExist(this User user)
Line 1039: {
Line 1040: Assert.NotNull(user);
Line 1041: return user;
Line 1042: }
Line 1043: public static User WithEmail(this User user, string email)
Line 1044: {
Line 1045: Assert.Equal(email, user.Email);
Line 1046: return user;
Line 1047: }
Line 1048: }
Line 1049: With this fluent interface, the assertions become much easier to read:
Line 1050: User userFromDb = QueryUser(user.UserId);
Line 1051: userFromDb
Line 1052: .ShouldExist()
Line 1053: Listing 10.12
Line 1054: Data assertions after extracting the querying logic
Line 1055: Listing 10.13
Line 1056: Fluent interface for data assertions
Line 1057: New helper 
Line 1058: methods
Line 1059: 
Line 1060: --- 페이지 273 ---
Line 1061: 251
Line 1062: Reusing code in test sections
Line 1063: .WithEmail("new@gmail.com")
Line 1064: .WithType(UserType.Customer);
Line 1065: Company companyFromDb = QueryCompany();
Line 1066: companyFromDb
Line 1067: .ShouldExist()
Line 1068: .WithNumberOfEmployees(0);
Line 1069: 10.4.4 Does the test create too many database transactions?
Line 1070: After all the simplifications made earlier, the integration test has become more read-
Line 1071: able and, therefore, more maintainable. There’s one drawback, though: the test now
Line 1072: uses a total of five database transactions (units of work), where before it used only
Line 1073: three, as shown in the following listing.
Line 1074: public class UserControllerTests : IntegrationTests
Line 1075: {
Line 1076: [Fact]
Line 1077: public void Changing_email_from_corporate_to_non_corporate()
Line 1078: {
Line 1079: // Arrange
Line 1080: User user = CreateUser(
Line 1081:                  
Line 1082: email: "user@mycorp.com",
Line 1083: type: UserType.Employee);
Line 1084: CreateCompany("mycorp.com", 1);                 
Line 1085: var busSpy = new BusSpy();
Line 1086: var messageBus = new MessageBus(busSpy);
Line 1087: var loggerMock = new Mock<IDomainLogger>();
Line 1088: // Act
Line 1089: string result = Execute(                        
Line 1090: x => x.ChangeEmail(user.UserId, "new@gmail.com"),
Line 1091: messageBus, loggerMock.Object);
Line 1092: // Assert
Line 1093: Assert.Equal("OK", result);
Line 1094: User userFromDb = QueryUser(user.UserId);       
Line 1095: userFromDb
Line 1096: .ShouldExist()
Line 1097: .WithEmail("new@gmail.com")
Line 1098: .WithType(UserType.Customer);
Line 1099: Company companyFromDb = QueryCompany();         
Line 1100: companyFromDb
Line 1101: .ShouldExist()
Line 1102: .WithNumberOfEmployees(0);
Line 1103: busSpy.ShouldSendNumberOfMessages(1)
Line 1104: .WithEmailChangedMessage(user.UserId, "new@gmail.com");
Line 1105: loggerMock.Verify(
Line 1106: Listing 10.14
Line 1107: Integration test after moving all technicalities out of it
Line 1108: Instantiates a
Line 1109: new database
Line 1110: context
Line 1111: behind the
Line 1112: scenes
Line 1113: 
Line 1114: --- 페이지 274 ---
Line 1115: 252
Line 1116: CHAPTER 10
Line 1117: Testing the database
Line 1118: x => x.UserTypeHasChanged(
Line 1119: user.UserId, UserType.Employee, UserType.Customer),
Line 1120: Times.Once);
Line 1121: }
Line 1122: }
Line 1123: Is the increased number of database transactions a problem? And, if so, what can
Line 1124: you do about it? The additional database contexts are a problem to some degree
Line 1125: because they make the test slower, but there’s not much that can be done about it.
Line 1126: It’s another example of a trade-off between different aspects of a valuable test: this
Line 1127: time between fast feedback and maintainability. It’s worth it to make that trade-off
Line 1128: and exchange performance for maintainability in this particular case. The perfor-
Line 1129: mance degradation shouldn’t be that significant, especially when the database is
Line 1130: located on the developer’s machine. At the same time, the gains in maintainability
Line 1131: are quite substantial. 
Line 1132: 10.5
Line 1133: Common database testing questions
Line 1134: In this last section of the chapter, I’d like to answer common questions related to
Line 1135: database testing, as well as briefly reiterate some important points made in chapters 8
Line 1136: and 9.
Line 1137: 10.5.1 Should you test reads?
Line 1138: Throughout the last several chapters, we’ve worked with a sample scenario of chang-
Line 1139: ing a user email. This scenario is an example of a write operation (an operation that
Line 1140: leaves a side effect in the database and other out-of-process dependencies). Most
Line 1141: applications contain both write and read operations. An example of a read operation
Line 1142: would be returning the user information to the external client. Should you test both
Line 1143: writes and reads?
Line 1144:  It’s crucial to thoroughly test writes, because the stakes are high. Mistakes in write
Line 1145: operations often lead to data corruption, which can affect not only your database but
Line 1146: also external applications. Tests that cover writes are highly valuable due to the protec-
Line 1147: tion they provide against such mistakes.
Line 1148:  This is not the case for reads: a bug in a read operation usually doesn’t have conse-
Line 1149: quences that are as detrimental. Therefore, the threshold for testing reads should be
Line 1150: higher than that for writes. Test only the most complex or important read operations;
Line 1151: disregard the rest.
Line 1152:  Note that there’s also no need for a domain model in reads. One of the main goals
Line 1153: of domain modeling is encapsulation. And, as you might remember from chapters 5
Line 1154: and 6, encapsulation is about preserving data consistency in light of any changes. The
Line 1155: lack of data changes makes encapsulation of reads pointless. In fact, you don’t need a
Line 1156: fully fledged ORM such as NHibernate or Entity Framework in reads, either. You are
Line 1157: better off using plain SQL, which is superior to an ORM performance-wise, thanks to
Line 1158: bypassing unnecessary layers of abstraction (figure 10.7).
Line 1159: 
Line 1160: --- 페이지 275 ---
Line 1161: 253
Line 1162: Common database testing questions
Line 1163: Because there are hardly any abstraction layers in reads (the domain model is one
Line 1164: such layer), unit tests aren’t of any use there. If you decide to test your reads, do so
Line 1165: using integration tests on a real database. 
Line 1166: 10.5.2 Should you test repositories?
Line 1167: Repositories provide a useful abstraction on top of the database. Here’s a usage exam-
Line 1168: ple from our sample CRM project:
Line 1169: User user = _userRepository.GetUserById(userId);
Line 1170: _userRepository.SaveUser(user);
Line 1171: Should you test repositories independently of other integration tests? It might seem
Line 1172: beneficial to test how repositories map domain objects to the database. After all,
Line 1173: there’s significant room for a mistake in this functionality. Still, such tests are a net loss
Line 1174: to your test suite due to high maintenance costs and inferior protection against
Line 1175: regressions. Let’s discuss these two drawbacks in more detail.
Line 1176: HIGH MAINTENANCE COSTS
Line 1177: Repositories fall into the controllers quadrant on the types-of-code diagram from
Line 1178: chapter 7 (figure 10.8). They exhibit little complexity and communicate with an out-
Line 1179: of-process dependency: the database. The presence of that out-of-process dependency
Line 1180: is what inflates the tests’ maintenance costs.
Line 1181:  When it comes to maintenance costs, testing repositories carries the same burden
Line 1182: as regular integration tests. But does such testing provide an equal amount of benefits
Line 1183: in return? Unfortunately, it doesn’t.
Line 1184: Writes
Line 1185: Database
Line 1186: Client
Line 1187: Reads
Line 1188: Application
Line 1189: . . . not here
Line 1190: Domain model goes here . . .
Line 1191: Figure 10.7
Line 1192: There’s no need for a domain model in reads. And because the cost of a 
Line 1193: mistake in reads is lower than it is in writes, there’s also not as much need for integration 
Line 1194: testing.
Line 1195: 
Line 1196: --- 페이지 276 ---
Line 1197: 254
Line 1198: CHAPTER 10
Line 1199: Testing the database
Line 1200: INFERIOR PROTECTION AGAINST REGRESSIONS
Line 1201: Repositories don’t carry that much complexity, and a lot of the gains in protection
Line 1202: against regressions overlap with the gains provided by regular integration tests. Thus,
Line 1203: tests on repositories don’t add significant enough value.
Line 1204:  The best course of action in testing a repository is to extract the little complexity it
Line 1205: has into a self-contained algorithm and test that algorithm exclusively. That’s what
Line 1206: UserFactory and CompanyFactory were for in earlier chapters. These two classes per-
Line 1207: formed all the mappings without taking on any collaborators, out-of-process or other-
Line 1208: wise. The repositories (the Database class) only contained simple SQL queries.
Line 1209:  Unfortunately, such a separation between data mapping (formerly performed by
Line 1210: the factories) and interactions with the database (formerly performed by Database) is
Line 1211: impossible when using an ORM. You can’t test your ORM mappings without calling
Line 1212: the database, at least not without compromising resistance to refactoring. Therefore,
Line 1213: adhere to the following guideline: don’t test repositories directly, only as part of the overarch-
Line 1214: ing integration test suite.
Line 1215:  Don’t test EventDispatcher separately, either (this class converts domain events
Line 1216: into calls to unmanaged dependencies). There are too few gains in protection against
Line 1217: regressions in exchange for the too-high costs required to maintain the complicated
Line 1218: mock machinery. 
Line 1219: 10.6
Line 1220: Conclusion
Line 1221: Well-crafted tests against the database provide bulletproof protection from bugs. In
Line 1222: my experience, they are one of the most effective tools, without which it’s impossible
Line 1223: Domain model,
Line 1224: algorithms
Line 1225: Overcomplicated
Line 1226: code
Line 1227: Trivial code
Line 1228: Controllers
Line 1229: Complexity,
Line 1230: domain
Line 1231: signiﬁcance
Line 1232: Number of
Line 1233: collaborators
Line 1234: Repositories
Line 1235: Figure 10.8
Line 1236: Repositories exhibit little complexity and communicate with the 
Line 1237: out-of-process dependency, thus falling into the controllers quadrant on the 
Line 1238: types-of-code diagram.
Line 1239: 
Line 1240: --- 페이지 277 ---
Line 1241: 255
Line 1242: Summary
Line 1243: to gain full confidence in your software. Such tests help enormously when you refac-
Line 1244: tor the database, switch the ORM, or change the database vendor.
Line 1245:  In fact, our sample project transitioned to the Entity Framework ORM earlier in
Line 1246: this chapter, and I only needed to modify a couple of lines of code in the integration
Line 1247: test to make sure the transition was successful. Integration tests working directly with
Line 1248: managed dependencies are the most efficient way to protect against bugs resulting
Line 1249: from large-scale refactorings. 
Line 1250: Summary
Line 1251: Store database schema in a source control system, along with your source code.
Line 1252: Database schema consists of tables, views, indexes, stored procedures, and any-
Line 1253: thing else that forms a blueprint of how the database is constructed.
Line 1254: Reference data is also part of the database schema. It is data that must be pre-
Line 1255: populated in order for the application to operate properly. To differentiate
Line 1256: between reference and regular data, look at whether your application can mod-
Line 1257: ify that data. If so, it’s regular data; otherwise, it’s reference data.
Line 1258: Have a separate database instance for every developer. Better yet, host that
Line 1259: instance on the developer’s own machine for maximum test execution speed.
Line 1260: The state-based approach to database delivery makes the state explicit and lets a
Line 1261: comparison tool implicitly control migrations. The migration-based approach
Line 1262: emphasizes the use of explicit migrations that transition the database from one
Line 1263: state to another. The explicitness of the database state makes it easier to handle
Line 1264: merge conflicts, while explicit migrations help tackle data motion.
Line 1265: Prefer the migration-based approach over state-based, because handling data
Line 1266: motion is much more important than merge conflicts. Apply every modification
Line 1267: to the database schema (including reference data) through migrations.
Line 1268: Business operations must update data atomically. To achieve atomicity, rely on
Line 1269: the underlying database’s transaction mechanism.
Line 1270: Use the unit of work pattern when possible. A unit of work relies on the under-
Line 1271: lying database’s transactions; it also defers all updates to the end of the business
Line 1272: operation, thus improving performance.
Line 1273: Don’t reuse database transactions or units of work between sections of the
Line 1274: test. Each arrange, act, and assert section should have its own transaction or
Line 1275: unit of work.
Line 1276: Execute integration tests sequentially. Parallel execution involves significant
Line 1277: effort and usually is not worth it.
Line 1278: Clean up leftover data at the start of a test. This approach works fast, doesn’t
Line 1279: result in inconsistent behavior, and isn’t prone to accidentally skipping the
Line 1280: cleanup phase. With this approach, you don’t have to introduce a separate tear-
Line 1281: down phase, either.
Line 1282: 
Line 1283: --- 페이지 278 ---
Line 1284: 256
Line 1285: CHAPTER 10
Line 1286: Testing the database
Line 1287: Avoid in-memory databases such as SQLite. You’ll never gain good protection if
Line 1288: your tests run against a database from a different vendor. Use the same database
Line 1289: management system in tests as in production.
Line 1290: Shorten tests by extracting non-essential parts into private methods or helper
Line 1291: classes:
Line 1292: – For the arrange section, choose Object Mother over Test Data Builder.
Line 1293: – For act, create decorator methods.
Line 1294: – For assert, introduce a fluent interface.
Line 1295: The threshold for testing reads should be higher than that for writes. Test only
Line 1296: the most complex or important read operations; disregard the rest.
Line 1297: Don’t test repositories directly, but only as part of the overarching integration
Line 1298: test suite. Tests on repositories introduce too high maintenance costs for too
Line 1299: few additional gains in protection against regressions.
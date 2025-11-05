# 10.2.1 Managing database transactions in production code (pp.235-242)

---
**Page 235**

235
Database transaction management
10.2.1 Managing database transactions in production code
Our sample CRM project uses the Database class to work with User and Company.
Database creates a separate SQL connection on each method call. Every such connec-
tion implicitly opens an independent transaction behind the scenes, as the following
listing shows.
public class Database
{
private readonly string _connectionString;
public Database(string connectionString)
{
_connectionString = connectionString;
}
public void SaveUser(User user)
{
bool isNewUser = user.UserId == 0;
using (var connection =
new SqlConnection(_connectionString))      
{
/* Insert or update the user depending on isNewUser */
}
}
public void SaveCompany(Company company)
{
using (var connection =
new SqlConnection(_connectionString))      
{
/* Update only; there's only one company */
}
}
}
As a result, the user controller creates a total of four database transactions during a
single business operation, as shown in the following listing.
public string ChangeEmail(int userId, string newEmail)
{
object[] userData = _database.GetUserById(userId);    
User user = UserFactory.Create(userData);
string error = user.CanChangeEmail();
if (error != null)
return error;
Listing 10.1
Class that enables access to the database
Listing 10.2
User controller
Opens a
database
transaction
Opens a new 
database 
transaction


---
**Page 236**

236
CHAPTER 10
Testing the database
object[] companyData = _database.GetCompany();        
Company company = CompanyFactory.Create(companyData);
user.ChangeEmail(newEmail, company);
_database.SaveCompany(company);                       
_database.SaveUser(user);                             
_eventDispatcher.Dispatch(user.DomainEvents);
return "OK";
}
It’s fine to open multiple transactions during read-only operations: for example, when
returning user information to the external client. But if the business operation
involves data mutation, all updates taking place during that operation should be
atomic in order to avoid inconsistencies. For example, the controller can successfully
persist the company but then fail when saving the user due to a database connectivity
issue. As a result, the company’s NumberOfEmployees can become inconsistent with
the total number of Employee users in the database.
DEFINITION
Atomic updates are executed in an all-or-nothing manner. Each
update in the set of atomic updates must either be complete in its entirety or
have no effect whatsoever.
SEPARATING DATABASE CONNECTIONS FROM DATABASE TRANSACTIONS
To avoid potential inconsistencies, you need to introduce a separation between two
types of decisions:
What data to update
Whether to keep the updates or roll them back
Such a separation is important because the controller can’t make these decisions
simultaneously. It only knows whether the updates can be kept when all the steps in
the business operation have succeeded. And it can only take those steps by accessing
the database and trying to make the updates. You can implement the separation
between these responsibilities by splitting the Database class into repositories and a
transaction:
Repositories are classes that enable access to and modification of the data in the
database. There will be two repositories in our sample project: one for User and
the other for Company.
A transaction is a class that either commits or rolls back data updates in full. This
will be a custom class relying on the underlying database’s transactions to pro-
vide atomicity of data modification.
Not only do repositories and transactions have different responsibilities, but they also
have different lifespans. A transaction lives during the whole business operation and is
disposed of at the very end of it. A repository, on the other hand, is short-lived. You
Opens a new 
database 
transaction


---
**Page 237**

237
Database transaction management
can dispose of a repository as soon as the call to the database is completed. As a result,
repositories always work on top of the current transaction. When connecting to the
database, a repository enlists itself into the transaction so that any data modifications
made during that connection can later be rolled back by the transaction.
 Figure 10.4 shows how the communication between the controller and the data-
base looks in listing 10.2. Each database call is wrapped into its own transaction;
updates are not atomic.
Figure 10.5 shows the application after the introduction of explicit transactions. The
transaction mediates interactions between the controller and the database. All four
database calls are still there, but now data modifications are either committed or
rolled back in full.
The following listing shows the controller after introducing a transaction and repositories.
public class UserController
{
private readonly Transaction _transaction;
private readonly UserRepository _userRepository;
Listing 10.3
User controller, repositories, and a transaction
Database
GetUserById
Controller
SaveCompany
GetCompany
SaveUser
Figure 10.4
Wrapping each 
database call into a separate 
transaction introduces a risk of 
inconsistencies due to hardware or 
software failures. For example, the 
application can update the number of 
employees in the company but not 
the employees themselves.
Transaction
Database
Controller
Commit tran
Commit tran
SaveUser
SaveUser
SaveCompany
SaveCompany
GetCompany
GetCompany
GetUserById
GetUserById
Open tran
Open tran
Figure 10.5
The transaction mediates interactions between the controller and the database and 
thus enables atomic data modification.


---
**Page 238**

238
CHAPTER 10
Testing the database
private readonly CompanyRepository _companyRepository;
private readonly EventDispatcher _eventDispatcher;
public UserController(
Transaction transaction,     
MessageBus messageBus,
IDomainLogger domainLogger)
{
_transaction = transaction;
_userRepository = new UserRepository(transaction);
_companyRepository = new CompanyRepository(transaction);
_eventDispatcher = new EventDispatcher(
messageBus, domainLogger);
}
public string ChangeEmail(int userId, string newEmail)
{
object[] userData = _userRepository           
.GetUserById(userId);
           
User user = UserFactory.Create(userData);
string error = user.CanChangeEmail();
if (error != null)
return error;
object[] companyData = _companyRepository     
.GetCompany();
      
Company company = CompanyFactory.Create(companyData);
user.ChangeEmail(newEmail, company);
_companyRepository.SaveCompany(company);      
_userRepository.SaveUser(user);
      
_eventDispatcher.Dispatch(user.DomainEvents);
_transaction.Commit();     
return "OK";
}
}
public class UserRepository
{
private readonly Transaction _transaction;
public UserRepository(Transaction transaction)    
{
_transaction = transaction;
}
/* ... */
}
public class Transaction : IDisposable
{
Accepts a 
transaction
Uses the
repositories
instead
of the
Database
class
Commits the 
transaction 
on success
Injects a 
transaction into 
a repository


---
**Page 239**

239
Database transaction management
public void Commit() { /* ... */ }
public void Dispose() { /* ... */ }
}
The internals of the Transaction class aren’t important, but if you’re curious, I’m
using .NET’s standard TransactionScope behind the scenes. The important part
about Transaction is that it contains two methods:

Commit()marks the transaction as successful. This is only called when the busi-
ness operation itself has succeeded and all data modifications are ready to be
persisted.

Dispose()ends the transaction. This is called indiscriminately at the end of the
business operation. If Commit() was previously invoked, Dispose() persists all
data updates; otherwise, it rolls them back.
Such a combination of Commit() and Dispose() guarantees that the database is
altered only during happy paths (the successful execution of the business scenario).
That’s why Commit() resides at the very end of the ChangeEmail() method. In the
event of any error, be it a validation error or an unhandled exception, the execution
flow returns early and thereby prevents the transaction from being committed.
 Commit() is invoked by the controller because this method call requires decision-
making. There’s no decision-making involved in calling Dispose(), though, so you
can delegate that method call to a class from the infrastructure layer. The same class
that instantiates the controller and provides it with the necessary dependencies
should also dispose of the transaction once the controller is done working.
 Notice how UserRepository requires Transaction as a constructor parameter.
This explicitly shows that repositories always work on top of transactions; a repository
can’t call the database on its own. 
UPGRADING THE TRANSACTION TO A UNIT OF WORK
The introduction of repositories and a transaction is a good way to avoid potential
data inconsistencies, but there’s an even better approach. You can upgrade the
Transaction class to a unit of work.
DEFINITION
A unit of work maintains a list of objects affected by a business
operation. Once the operation is completed, the unit of work figures out all
updates that need to be done to alter the database and executes those
updates as a single unit (hence the pattern name).
The main advantage of a unit of work over a plain transaction is the deferral of
updates. Unlike a transaction, a unit of work executes all updates at the end of the
business operation, thus minimizing the duration of the underlying database transac-
tion and reducing data congestion (see figure 10.6). Often, this pattern also helps to
reduce the number of database calls.
NOTE
Database transactions also implement the unit-of-work pattern.


---
**Page 240**

240
CHAPTER 10
Testing the database
Maintaining a list of modified objects and then figuring out what SQL script to gener-
ate can look like a lot of work. In reality, though, you don’t need to do that work your-
self. Most object-relational mapping (ORM) libraries implement the unit-of-work
pattern for you. In .NET, for example, you can use NHibernate or Entity Framework,
both of which provide classes that do all the hard lifting (those classes are ISession
and DbContext, respectively). The following listing shows how UserController looks
in combination with Entity Framework.
public class UserController
{
private readonly CrmContext _context;
private readonly UserRepository _userRepository;
private readonly CompanyRepository _companyRepository;
private readonly EventDispatcher _eventDispatcher;
public UserController(
CrmContext context,                     
MessageBus messageBus,
IDomainLogger domainLogger)
{
_context = context;
_userRepository = new UserRepository(
context);                           
_companyRepository = new CompanyRepository(
context);                           
_eventDispatcher = new EventDispatcher(
messageBus, domainLogger);
}
public string ChangeEmail(int userId, string newEmail)
{
User user = _userRepository.GetUserById(userId);
Listing 10.4
User controller with Entity Framework
Unit of work
GetUserById
Database
SaveCompany
GetCompany
Controller
SaveUser
Create
SaveChanges
GetUserById
GetCompany
Save all
Figure 10.6
A unit of work executes all updates at the end of the business operation. The updates 
are still wrapped in a database transaction, but that transaction lives for a shorter period of time, 
thus reducing data congestion.
CrmContext
replaces
Transaction.


---
**Page 241**

241
Database transaction management
string error = user.CanChangeEmail();
if (error != null)
return error;
Company company = _companyRepository.GetCompany();
user.ChangeEmail(newEmail, company);
_companyRepository.SaveCompany(company);
_userRepository.SaveUser(user);
_eventDispatcher.Dispatch(user.DomainEvents);
_context.SaveChanges();  
return "OK";
}
}
CrmContext is a custom class that contains mapping between the domain model and
the database (it inherits from Entity Framework’s DbContext). The controller in list-
ing 10.4 uses CrmContext instead of Transaction. As a result,
Both repositories now work on top of CrmContext, just as they worked on top of
Transaction in the previous version.
The controller commits changes to the database via context.SaveChanges()
instead of transaction.Commit().
Notice that there’s no need for UserFactory and CompanyFactory anymore because
Entity Framework now serves as a mapper between the raw database data and
domain objects.
Data inconsistencies in non-relational databases
It’s easy to avoid data inconsistencies when using a relational database: all major
relational databases provide atomic updates that can span as many rows as needed.
But how do you achieve the same level of protection with a non-relational database
such as MongoDB?
The problem with most non-relational databases is the lack of transactions in the
classical sense; atomic updates are guaranteed only within a single document. If a
business operation affects multiple documents, it becomes prone to inconsisten-
cies. (In non-relational databases, a document is the equivalent of a row.)
Non-relational databases approach inconsistencies from a different angle: they
require you to design your documents such that no business operation modifies more
than one of those documents at a time. This is possible because documents are
more flexible than rows in relational databases. A single document can store data of
any shape and complexity and thus capture side effects of even the most sophisti-
cated business operations.
CrmContext 
replaces 
Transaction.


---
**Page 242**

242
CHAPTER 10
Testing the database
10.2.2 Managing database transactions in integration tests
When it comes to managing database transactions in integration tests, adhere to the
following guideline: don’t reuse database transactions or units of work between sections of the
test. The following listing shows an example of reusing CrmContext in the integration
test after switching that test to Entity Framework.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
using (var context =
   
new CrmContext(ConnectionString))   
{
// Arrange
var userRepository =
         
new UserRepository(context);
         
var companyRepository =
         
new CompanyRepository(context);         
var user = new User(0, "user@mycorp.com",
UserType.Employee, false);
userRepository.SaveUser(user);
var company = new Company("mycorp.com", 1);
companyRepository.SaveCompany(company);
context.SaveChanges();                      
var busSpy = new BusSpy();
var messageBus = new MessageBus(busSpy);
var loggerMock = new Mock<IDomainLogger>();
var sut = new UserController(
context,                     
messageBus,
loggerMock.Object);
// Act
string result = sut.ChangeEmail(user.UserId, "new@gmail.com");
// Assert
Assert.Equal("OK", result);
User userFromDb = userRepository     
.GetUserById(user.UserId);       
(continued)
In domain-driven design, there’s a guideline saying that you shouldn’t modify more
than one aggregate per business operation. This guideline serves the same goal: pro-
tecting you from data inconsistencies. The guideline is only applicable to systems
that work with document databases, though, where each document corresponds to
one aggregate. 
Listing 10.5
Integration test reusing CrmContext
Creates a 
context
Uses the context 
in the arrange 
section . . .
. . . in act . . .
. . . and in assert



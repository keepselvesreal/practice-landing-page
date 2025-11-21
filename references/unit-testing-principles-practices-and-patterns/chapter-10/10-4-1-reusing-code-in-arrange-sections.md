# 10.4.1 Reusing code in arrange sections (pp.246-249)

---
**Page 246**

246
CHAPTER 10
Testing the database
10.3.3 Avoid in-memory databases
Another way to isolate integration tests from each other is by replacing the database
with an in-memory analog, such as SQLite. In-memory databases can seem beneficial
because they
Don’t require removal of test data
Work faster
Can be instantiated for each test run
Because in-memory databases aren’t shared dependencies, integration tests in effect
become unit tests (assuming the database is the only managed dependency in the
project), similar to the approach with containers described in section 10.3.1.
 In spite of all these benefits, I don’t recommend using in-memory databases
because they aren’t consistent functionality-wise with regular databases. This is, once
again, the problem of a mismatch between production and test environments. Your
tests can easily run into false positives or (worse!) false negatives due to the differ-
ences between the regular and in-memory databases. You’ll never gain good protec-
tion with such tests and will have to do a lot of regression testing manually anyway.
TIP
Use the same database management system (DBMS) in tests as in pro-
duction. It’s usually fine for the version or edition to differ, but the vendor
must remain the same. 
10.4
Reusing code in test sections
Integration tests can quickly grow too large and thus lose ground on the maintainabil-
ity metric. It’s important to keep integration tests as short as possible but without cou-
pling them to each other or affecting readability. Even the shortest tests shouldn’t
depend on one another. They also should preserve the full context of the test scenario
and shouldn’t require you to examine different parts of the test class to understand
what’s going on.
 The best way to shorten integration is by extracting technical, non-business-related
bits into private methods or helper classes. As a side bonus, you’ll get to reuse those
bits. In this section, I’ll show how to shorten all three sections of the test: arrange, act,
and assert.
10.4.1 Reusing code in arrange sections
The following listing shows how our integration test looks after providing a separate
database context (unit of work) for each of its sections.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
// Arrange
User user;
Listing 10.7
Integration test with three database contexts


---
**Page 247**

247
Reusing code in test sections
using (var context = new CrmContext(ConnectionString))
{
var userRepository = new UserRepository(context);
var companyRepository = new CompanyRepository(context);
user = new User(0, "user@mycorp.com",
UserType.Employee, false);
userRepository.SaveUser(user);
var company = new Company("mycorp.com", 1);
companyRepository.SaveCompany(company);
context.SaveChanges();
}
var busSpy = new BusSpy();
var messageBus = new MessageBus(busSpy);
var loggerMock = new Mock<IDomainLogger>();
string result;
using (var context = new CrmContext(ConnectionString))
{
var sut = new UserController(
context, messageBus, loggerMock.Object);
// Act
result = sut.ChangeEmail(user.UserId, "new@gmail.com");
}
// Assert
Assert.Equal("OK", result);
using (var context = new CrmContext(ConnectionString))
{
var userRepository = new UserRepository(context);
var companyRepository = new CompanyRepository(context);
User userFromDb = userRepository.GetUserById(user.UserId);
Assert.Equal("new@gmail.com", userFromDb.Email);
Assert.Equal(UserType.Customer, userFromDb.Type);
Company companyFromDb = companyRepository.GetCompany();
Assert.Equal(0, companyFromDb.NumberOfEmployees);
busSpy.ShouldSendNumberOfMessages(1)
.WithEmailChangedMessage(user.UserId, "new@gmail.com");
loggerMock.Verify(
x => x.UserTypeHasChanged(
user.UserId, UserType.Employee, UserType.Customer),
Times.Once);
}
}
As you might remember from chapter 3, the best way to reuse code between the tests’
arrange sections is to introduce private factory methods. For example, the following
listing creates a user.


---
**Page 248**

248
CHAPTER 10
Testing the database
private User CreateUser(
string email, UserType type, bool isEmailConfirmed)
{
using (var context = new CrmContext(ConnectionString))
{
var user = new User(0, email, type, isEmailConfirmed);
var repository = new UserRepository(context);
repository.SaveUser(user);
context.SaveChanges();
return user;
}
}
You can also define default values for the method’s arguments, as shown next.
private User CreateUser(
string email = "user@mycorp.com",
UserType type = UserType.Employee,
bool isEmailConfirmed = false)
{
/* ... */
}
With default values, you can specify arguments selectively and thus shorten the test
even further. The selective use of arguments also emphasizes which of those argu-
ments are relevant to the test scenario.
User user = CreateUser(
email: "user@mycorp.com",
type: UserType.Employee);
Listing 10.8
A separate method that creates a user
Listing 10.9
Adding default values to the factory
Listing 10.10
Using the factory method
Object Mother vs. Test Data Builder
The pattern shown in listings 10.9 and 10.10 is called the Object Mother. The Object
Mother is a class or method that helps create test fixtures (objects the test runs
against).
There’s another pattern that helps achieve the same goal of reusing code in arrange
sections: Test Data Builder. It works similarly to Object Mother but exposes a fluent
interface instead of plain methods. Here’s a Test Data Builder usage example:


---
**Page 249**

249
Reusing code in test sections
WHERE TO PUT FACTORY METHODS
When you start distilling the tests’ essentials and move the technicalities out to fac-
tory methods, you face the question of where to put those methods. Should they
reside in the same class as the tests? The base IntegrationTests class? Or in a sepa-
rate helper class?
 Start simple. Place the factory methods in the same class by default. Move them
into separate helper classes only when code duplication becomes a significant issue.
Don’t put the factory methods in the base class; reserve that class for code that has to
run in every test, such as data cleanup. 
10.4.2 Reusing code in act sections
Every act section in integration tests involves the creation of a database transaction or
a unit of work. This is how the act section currently looks in listing 10.7:
string result;
using (var context = new CrmContext(ConnectionString))
{
var sut = new UserController(
context, messageBus, loggerMock.Object);
// Act
result = sut.ChangeEmail(user.UserId, "new@gmail.com");
}
This section can also be reduced. You can introduce a method accepting a delegate
with the information of what controller function needs to be invoked. The method
will then decorate the controller invocation with the creation of a database context, as
shown in the following listing.
private string Execute(
Func<UserController, string> func,   
MessageBus messageBus,
IDomainLogger logger)
{
using (var context = new CrmContext(ConnectionString))
{
var controller = new UserController(
User user = new UserBuilder()
.WithEmail("user@mycorp.com")
.WithType(UserType.Employee)
.Build();
Test Data Builder slightly improves test readability but requires too much boilerplate.
For that reason, I recommend sticking to the Object Mother (at least in C#, where you
have optional arguments as a language feature).
Listing 10.11
Decorator method
Delegate defines 
a controller 
function.



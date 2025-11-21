# 10.2.2 Managing database transactions in integration tests (pp.242-243)

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


---
**Page 243**

243
Test data life cycle
Assert.Equal("new@gmail.com", userFromDb.Email);
Assert.Equal(UserType.Customer, userFromDb.Type);
Company companyFromDb = companyRepository     
.GetCompany();
     
Assert.Equal(0, companyFromDb.NumberOfEmployees);
busSpy.ShouldSendNumberOfMessages(1)
.WithEmailChangedMessage(user.UserId, "new@gmail.com");
loggerMock.Verify(
x => x.UserTypeHasChanged(
user.UserId, UserType.Employee, UserType.Customer),
Times.Once);
}
}
This test uses the same instance of CrmContext in all three sections: arrange, act, and
assert. This is a problem because such reuse of the unit of work creates an environment
that doesn’t match what the controller experiences in production. In production, each
business operation has an exclusive instance of CrmContext. That instance is created
right before the controller method invocation and is disposed of immediately after.
 To avoid the risk of inconsistent behavior, integration tests should replicate the
production environment as closely as possible, which means the act section must not
share CrmContext with anyone else. The arrange and assert sections must get their
own instances of CrmContext too, because, as you might remember from chapter 8,
it’s important to check the state of the database independently of the data used as
input parameters. And although the assert section does query the user and the com-
pany independently of the arrange section, these sections still share the same database
context. That context can (and many ORMs do) cache the requested data for perfor-
mance improvements.
TIP
Use at least three transactions or units of work in an integration test: one
per each arrange, act, and assert section. 
10.3
Test data life cycle
The shared database raises the problem of isolating integration tests from each other.
To solve this problem, you need to
Execute integration tests sequentially.
Remove leftover data between test runs.
Overall, your tests shouldn’t depend on the state of the database. Your tests should
bring that state to the required condition on their own.
10.3.1 Parallel vs. sequential test execution
Parallel execution of integration tests involves significant effort. You have to ensure
that all test data is unique so no database constraints are violated and tests don’t acci-
dentally pick up input data after each other. Cleaning up leftover data also becomes
. . . and in assert



# 10.4.3 Reusing code in assert sections (pp.250-251)

---
**Page 250**

250
CHAPTER 10
Testing the database
context, messageBus, logger);
return func(controller);
}
}
With this decorator method, you can boil down the test’s act section to just a couple
of lines:
string result = Execute(
x => x.ChangeEmail(user.UserId, "new@gmail.com"),
messageBus, loggerMock.Object);
10.4.3 Reusing code in assert sections
Finally, the assert section can be shortened, too. The easiest way to do that is to intro-
duce helper methods similar to CreateUser and CreateCompany, as shown in the fol-
lowing listing.
User userFromDb = QueryUser(user.UserId);         
Assert.Equal("new@gmail.com", userFromDb.Email);
Assert.Equal(UserType.Customer, userFromDb.Type);
Company companyFromDb = QueryCompany();           
Assert.Equal(0, companyFromDb.NumberOfEmployees);
You can take a step further and create a fluent interface for these data assertions, sim-
ilar to what you saw in chapter 9 with BusSpy. In C#, a fluent interface on top of exist-
ing domain classes can be implemented using extension methods, as shown in the
following listing.
public static class UserExternsions
{
public static User ShouldExist(this User user)
{
Assert.NotNull(user);
return user;
}
public static User WithEmail(this User user, string email)
{
Assert.Equal(email, user.Email);
return user;
}
}
With this fluent interface, the assertions become much easier to read:
User userFromDb = QueryUser(user.UserId);
userFromDb
.ShouldExist()
Listing 10.12
Data assertions after extracting the querying logic
Listing 10.13
Fluent interface for data assertions
New helper 
methods


---
**Page 251**

251
Reusing code in test sections
.WithEmail("new@gmail.com")
.WithType(UserType.Customer);
Company companyFromDb = QueryCompany();
companyFromDb
.ShouldExist()
.WithNumberOfEmployees(0);
10.4.4 Does the test create too many database transactions?
After all the simplifications made earlier, the integration test has become more read-
able and, therefore, more maintainable. There’s one drawback, though: the test now
uses a total of five database transactions (units of work), where before it used only
three, as shown in the following listing.
public class UserControllerTests : IntegrationTests
{
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
// Arrange
User user = CreateUser(
                 
email: "user@mycorp.com",
type: UserType.Employee);
CreateCompany("mycorp.com", 1);                 
var busSpy = new BusSpy();
var messageBus = new MessageBus(busSpy);
var loggerMock = new Mock<IDomainLogger>();
// Act
string result = Execute(                        
x => x.ChangeEmail(user.UserId, "new@gmail.com"),
messageBus, loggerMock.Object);
// Assert
Assert.Equal("OK", result);
User userFromDb = QueryUser(user.UserId);       
userFromDb
.ShouldExist()
.WithEmail("new@gmail.com")
.WithType(UserType.Customer);
Company companyFromDb = QueryCompany();         
companyFromDb
.ShouldExist()
.WithNumberOfEmployees(0);
busSpy.ShouldSendNumberOfMessages(1)
.WithEmailChangedMessage(user.UserId, "new@gmail.com");
loggerMock.Verify(
Listing 10.14
Integration test after moving all technicalities out of it
Instantiates a
new database
context
behind the
scenes



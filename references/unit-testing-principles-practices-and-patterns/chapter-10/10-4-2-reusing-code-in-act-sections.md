# 10.4.2 Reusing code in act sections (pp.249-250)

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



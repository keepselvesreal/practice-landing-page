# 8.3.4 Integration testing: The first try (pp.196-197)

---
**Page 196**

196
CHAPTER 8
Why integration testing?
of protection that is close enough to that of end-to-end tests, so you can skip end-to-
end testing. However, you could still create one or two overarching end-to-end tests
that would provide a sanity check for the project after deployment. Make such tests go
through the longest happy path, too, to ensure that your application communicates
with all out-of-process dependencies properly. To emulate the external client’s behav-
ior, check the message bus directly, but verify the database’s state through the applica-
tion itself. 
8.3.4
Integration testing: The first try
Here’s the first version of the integration test.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
// Arrange
var db = new Database(ConnectionString);
    
User user = CreateUser(
   
"user@mycorp.com", UserType.Employee, db);   
CreateCompany("mycorp.com", 1, db);
   
var messageBusMock = new Mock<IMessageBus>();         
var sut = new UserController(db, messageBusMock.Object);
// Act
string result = sut.ChangeEmail(user.UserId, "new@gmail.com");
Listing 8.2
The integration test
Integration test
Application
Message bus
mock
Database
Out-of-process
In-process
Figure 8.8
Integration tests host the application within the same process. Unlike 
end-to-end tests, integration tests substitute unmanaged dependencies with 
mocks. The only out-of-process components for integration tests are managed 
dependencies.
Database 
repository
Creates the user 
and company in 
the database
Sets up a 
mock for the 
message bus


---
**Page 197**

197
Using interfaces to abstract dependencies
// Assert
Assert.Equal("OK", result);
object[] userData = db.GetUserById(user.UserId);   
User userFromDb = UserFactory.Create(userData);    
Assert.Equal("new@gmail.com", userFromDb.Email);   
Assert.Equal(UserType.Customer, userFromDb.Type);  
object[] companyData = db.GetCompany();
   
Company companyFromDb = CompanyFactory
   
.Create(companyData);
   
Assert.Equal(0, companyFromDb.NumberOfEmployees);  
messageBusMock.Verify(
    
x => x.SendEmailChangedMessage(
    
user.UserId, "new@gmail.com"),    
Times.Once);
     
}
TIP
Notice that in the arrange section, the test doesn’t insert the user and
the company into the database on its own but instead calls the CreateUser
and CreateCompany helper methods. These methods can be reused across
multiple integration tests.
It’s important to check the state of the database independently of the data used as
input parameters. To do that, the integration test queries the user and company data
separately in the assert section, creates new userFromDb and companyFromDb instances,
and only then asserts their state. This approach ensures that the test exercises both
writes to and reads from the database and thus provides the maximum protection
against regressions. The reading itself must be implemented using the same code the
controller uses internally: in this example, using the Database, UserFactory, and
CompanyFactory classes.
 This integration test, while it gets the job done, can still benefit from some
improvement. For instance, you could use helper methods in the assertion section, too,
in order to reduce this section’s size. Also, messageBusMock doesn’t provide as good
protection against regressions as it potentially could. We’ll talk about these improve-
ments in the subsequent two chapters where we discuss mocking and database testing
best practices. 
8.4
Using interfaces to abstract dependencies
One of the most misunderstood subjects in the sphere of unit testing is the use of
interfaces. Developers often ascribe invalid reasons to why they introduce interfaces
and, as a result, tend to overuse them. In this section, I’ll expand on those invalid
reasons and show in what circumstances the use of interfaces is and isn’t preferable.
 
Asserts the 
user’s state
Asserts the 
company’s 
state
Checks the 
interactions 
with the mock



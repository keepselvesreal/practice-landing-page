# 10.4.4 Does the test create too many database transactions? (pp.251-252)

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


---
**Page 252**

252
CHAPTER 10
Testing the database
x => x.UserTypeHasChanged(
user.UserId, UserType.Employee, UserType.Customer),
Times.Once);
}
}
Is the increased number of database transactions a problem? And, if so, what can
you do about it? The additional database contexts are a problem to some degree
because they make the test slower, but there’s not much that can be done about it.
It’s another example of a trade-off between different aspects of a valuable test: this
time between fast feedback and maintainability. It’s worth it to make that trade-off
and exchange performance for maintainability in this particular case. The perfor-
mance degradation shouldn’t be that significant, especially when the database is
located on the developer’s machine. At the same time, the gains in maintainability
are quite substantial. 
10.5
Common database testing questions
In this last section of the chapter, I’d like to answer common questions related to
database testing, as well as briefly reiterate some important points made in chapters 8
and 9.
10.5.1 Should you test reads?
Throughout the last several chapters, we’ve worked with a sample scenario of chang-
ing a user email. This scenario is an example of a write operation (an operation that
leaves a side effect in the database and other out-of-process dependencies). Most
applications contain both write and read operations. An example of a read operation
would be returning the user information to the external client. Should you test both
writes and reads?
 It’s crucial to thoroughly test writes, because the stakes are high. Mistakes in write
operations often lead to data corruption, which can affect not only your database but
also external applications. Tests that cover writes are highly valuable due to the protec-
tion they provide against such mistakes.
 This is not the case for reads: a bug in a read operation usually doesn’t have conse-
quences that are as detrimental. Therefore, the threshold for testing reads should be
higher than that for writes. Test only the most complex or important read operations;
disregard the rest.
 Note that there’s also no need for a domain model in reads. One of the main goals
of domain modeling is encapsulation. And, as you might remember from chapters 5
and 6, encapsulation is about preserving data consistency in light of any changes. The
lack of data changes makes encapsulation of reads pointless. In fact, you don’t need a
fully fledged ORM such as NHibernate or Entity Framework in reads, either. You are
better off using plain SQL, which is superior to an ORM performance-wise, thanks to
bypassing unnecessary layers of abstraction (figure 10.7).



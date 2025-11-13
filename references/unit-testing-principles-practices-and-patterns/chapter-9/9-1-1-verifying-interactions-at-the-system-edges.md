# 9.1.1 Verifying interactions at the system edges (pp.219-222)

---
**Page 219**

219
Maximizing mocks’ value
// Arrange
var db = new Database(ConnectionString);
User user = CreateUser("user@mycorp.com", UserType.Employee, db);
CreateCompany("mycorp.com", 1, db);
var messageBusMock = new Mock<IMessageBus>();   
var loggerMock = new Mock<IDomainLogger>();     
var sut = new UserController(
db, messageBusMock.Object, loggerMock.Object);
// Act
string result = sut.ChangeEmail(user.UserId, "new@gmail.com");
// Assert
Assert.Equal("OK", result);
object[] userData = db.GetUserById(user.UserId);
User userFromDb = UserFactory.Create(userData);
Assert.Equal("new@gmail.com", userFromDb.Email);
Assert.Equal(UserType.Customer, userFromDb.Type);
object[] companyData = db.GetCompany();
Company companyFromDb = CompanyFactory.Create(companyData);
Assert.Equal(0, companyFromDb.NumberOfEmployees);
messageBusMock.Verify(
  
x => x.SendEmailChangedMessage(
  
user.UserId, "new@gmail.com"),  
Times.Once);
  
loggerMock.Verify(
  
x => x.UserTypeHasChanged(
  
user.UserId,
  
UserType.Employee,
  
UserType.Customer),
  
Times.Once);
  
}
This test mocks out two unmanaged dependencies: IMessageBus and IDomainLogger.
I’ll focus on IMessageBus first. We’ll discuss IDomainLogger later in this chapter.
9.1.1
Verifying interactions at the system edges
Let’s discuss why the mocks used by the integration test in listing 9.3 aren’t ideal in
terms of their protection against regressions and resistance to refactoring and how we
can fix that.
TIP
When mocking, always adhere to the following guideline: verify interac-
tions with unmanaged dependencies at the very edges of your system.
The problem with messageBusMock in listing 9.3 is that the IMessageBus interface
doesn’t reside at the system’s edge. Look at that interface’s implementation.
 
Sets up the 
mocks
Verifies the 
interactions 
with the mocks


---
**Page 220**

220
CHAPTER 9
Mocking best practices
public interface IMessageBus
{
void SendEmailChangedMessage(int userId, string newEmail);
}
public class MessageBus : IMessageBus
{
private readonly IBus _bus;
public void SendEmailChangedMessage(
int userId, string newEmail)
{
_bus.Send("Type: USER EMAIL CHANGED; " +
$"Id: {userId}; " +
$"NewEmail: {newEmail}");
}
}
public interface IBus
{
void Send(string message);
}
Both the IMessageBus and IBus interfaces (and the classes implementing them) belong
to our project’s code base. IBus is a wrapper on top of the message bus SDK library (pro-
vided by the company that develops that message bus). This wrapper encapsulates non-
essential technical details, such as connection credentials, and exposes a nice, clean
interface for sending arbitrary text messages to the bus. IMessageBus is a wrapper on
top of IBus; it defines messages specific to your domain. IMessageBus helps you keep all
such messages in one place and reuse them across the application.
 It’s possible to merge the IBus and IMessageBus interfaces together, but that
would be a suboptimal solution. These two responsibilities—hiding the external
library’s complexity and holding all application messages in one place—are best kept
separated. This is the same situation as with ILogger and IDomainLogger, which you
saw in chapter 8. IDomainLogger implements specific logging functionality required
by the business, and it does that by using the generic ILogger behind the scenes.
 Figure 9.1 shows where IBus and IMessageBus stand from a hexagonal architec-
ture perspective: IBus is the last link in the chain of types between the controller and
the message bus, while IMessageBus is only an intermediate step on the way.
 Mocking IBus instead of IMessageBus maximizes the mock’s protection against
regressions. As you might remember from chapter 4, protection against regressions is
a function of the amount of code that is executed during the test. Mocking the very
last type that communicates with the unmanaged dependency increases the number
of classes the integration test goes through and thus improves the protection. This
guideline is also the reason you don’t want to mock EventDispatcher. It resides even
further away from the edge of the system, compared to IMessageBus.
Listing 9.4
Message bus 


---
**Page 221**

221
Maximizing mocks’ value
Here’s the integration test after retargeting it from IMessageBus to IBus. I’m omitting
the parts that didn’t change from listing 9.3.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
var busMock = new Mock<IBus>();
var messageBus = new MessageBus(busMock.Object);     
var loggerMock = new Mock<IDomainLogger>();
var sut = new UserController(db, messageBus, loggerMock.Object);
/* ... */
busMock.Verify(
x => x.Send(
"Type: USER EMAIL CHANGED; " +  
$"Id: {user.UserId}; " +
  
"NewEmail: new@gmail.com"),
  
Times.Once);
}
Listing 9.5
Integration test targeting IBus
External client
Message bus
IMessageBus
Controller
Domain model
IBus
Figure 9.1
IBus resides at the system’s edge; IMessageBus is only an intermediate 
link in the chain of types between the controller and the message bus. Mocking IBus 
instead of IMessageBus achieves the best protection against regressions.
Uses a concrete 
class instead of 
the interface
Verifies the actual 
message sent to 
the bus


---
**Page 222**

222
CHAPTER 9
Mocking best practices
Notice how the test now uses the concrete MessageBus class and not the correspond-
ing IMessageBus interface. IMessageBus is an interface with a single implementation,
and, as you’ll remember from chapter 8, mocking is the only legitimate reason to have
such interfaces. Because we no longer mock IMessageBus, this interface can be
deleted and its usages replaced with MessageBus.
 Also notice how the test in listing 9.5 checks the text message sent to the bus. Com-
pare it to the previous version:
messageBusMock.Verify(
x => x.SendEmailChangedMessage(user.UserId, "new@gmail.com"),
Times.Once);
There’s a huge difference between verifying a call to a custom class that you wrote and
the actual text sent to external systems. External systems expect text messages from your
application, not calls to classes like MessageBus. In fact, text messages are the only side
effect observable externally; classes that participate in producing those messages are
mere implementation details. Thus, in addition to the increased protection against
regressions, verifying interactions at the very edges of your system also improves resis-
tance to refactoring. The resulting tests are less exposed to potential false positives; no
matter what refactorings take place, such tests won’t turn red as long as the message’s
structure is preserved.
 The same mechanism is at play here as the one that gives integration and end-to-end
tests additional resistance to refactoring compared to unit tests. They are more detached
from the code base and, therefore, aren’t affected as much during low-level refactorings.
TIP
A call to an unmanaged dependency goes through several stages before
it leaves your application. Pick the last such stage. It is the best way to ensure
backward compatibility with external systems, which is the goal that mocks
help you achieve. 
9.1.2
Replacing mocks with spies
As you may remember from chapter 5, a spy is a variation of a test double that serves
the same purpose as a mock. The only difference is that spies are written manually,
whereas mocks are created with the help of a mocking framework. Indeed, spies are
often called handwritten mocks.
 It turns out that, when it comes to classes residing at the system edges, spies are supe-
rior to mocks. Spies help you reuse code in the assertion phase, thereby reducing the
test’s size and improving readability. The next listing shows an example of a spy that
works on top of IBus.
public interface IBus
{
void Send(string message);
}
Listing 9.6
A spy (also known as a handwritten mock)



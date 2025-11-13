# 9.1.2 Replacing mocks with spies (pp.222-224)

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


---
**Page 223**

223
Maximizing mocks’ value
public class BusSpy : IBus
{
private List<string> _sentMessages =    
new List<string>();
    
public void Send(string message)
{
_sentMessages.Add(message);
    
}
public BusSpy ShouldSendNumberOfMessages(int number)
{
Assert.Equal(number, _sentMessages.Count);
return this;
}
public BusSpy WithEmailChangedMessage(int userId, string newEmail)
{
string message = "Type: USER EMAIL CHANGED; " +
$"Id: {userId}; " +
$"NewEmail: {newEmail}";
Assert.Contains(
   
_sentMessages, x => x == message);   
return this;
}
}
The following listing is a new version of the integration test. Again, I’m showing only
the relevant parts.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
var busSpy = new BusSpy();
var messageBus = new MessageBus(busSpy);
var loggerMock = new Mock<IDomainLogger>();
var sut = new UserController(db, messageBus, loggerMock.Object);
/* ... */
busSpy.ShouldSendNumberOfMessages(1)
.WithEmailChangedMessage(user.UserId, "new@gmail.com");
}
Verifying the interactions with the message bus is now succinct and expressive, thanks
to the fluent interface that BusSpy provides. With that fluent interface, you can chain
together several assertions, thus forming cohesive, almost plain-English sentences.
TIP
You can rename BusSpy into BusMock. As I mentioned earlier, the differ-
ence between a mock and a spy is an implementation detail. Most programmers
Listing 9.7
Using the spy from listing 6.43
Stores all sent 
messages 
locally
Asserts that the 
message has been sent


---
**Page 224**

224
CHAPTER 9
Mocking best practices
aren’t familiar with the term spy, though, so renaming the spy as BusMock can
save your colleagues unnecessary confusion.
There’s a reasonable question to be asked here: didn’t we just make a full circle and
come back to where we started? The version of the test in listing 9.7 looks a lot like the
earlier version that mocked IMessageBus:
messageBusMock.Verify(
x => x.SendEmailChangedMessage(
  
user.UserId, "new@gmail.com"),  
Times.Once);      
These assertions are similar because both BusSpy and MessageBus are wrappers on
top of IBus. But there’s a crucial difference between the two: BusSpy is part of the test
code, whereas MessageBus belongs to the production code. This difference is import-
ant because you shouldn’t rely on the production code when making assertions in tests.
 Think of your tests as auditors. A good auditor wouldn’t just take the auditee’s
words at face value; they would double-check everything. The same is true with the
spy: it provides an independent checkpoint that raises an alarm when the message
structure is changed. On the other hand, a mock on IMessageBus puts too much trust
in the production code. 
9.1.3
What about IDomainLogger?
The mock that previously verified interactions with IMessageBus is now targeted at
IBus, which resides at the system’s edge. Here are the current mock assertions in the
integration test.
busSpy.ShouldSendNumberOfMessages(1)
  
.WithEmailChangedMessage(
  
user.UserId, "new@gmail.com");  
loggerMock.Verify(
    
x => x.UserTypeHasChanged(
  
user.UserId,
  
UserType.Employee,
  
UserType.Customer),
  
Times.Once);
  
Note that just as MessageBus is a wrapper on top of IBus, DomainLogger is a wrapper
on top of ILogger (see chapter 8 for more details). Shouldn’t the test be retargeted at
ILogger, too, because this interface also resides at the application boundary?
 In most projects, such retargeting isn’t necessary. While the logger and the mes-
sage bus are unmanaged dependencies and, therefore, both require maintaining
backward compatibility, the accuracy of that compatibility doesn’t have to be the
same. With the message bus, it’s important not to allow any changes to the structure of
Listing 9.8
Mock assertions
Same as WithEmailChanged-
Message(user.UserId, 
"new@gmail.com")
Same as 
ShouldSendNumberOfMessages(1)
Checks 
interactions 
with IBus
Checks 
interactions with 
IDomainLogger



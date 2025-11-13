# 9.1.3 What about IDomainLogger? (pp.224-225)

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


---
**Page 225**

225
Mocking best practices
the messages, because you never know how external systems will react to such
changes. But the exact structure of text logs is not that important for the intended
audience (support staff and system administrators). What’s important is the existence
of those logs and the information they carry. Thus, mocking IDomainLogger alone
provides the necessary level of protection. 
9.2
Mocking best practices
You’ve learned two major mocking best practices so far:
Applying mocks to unmanaged dependencies only
Verifying the interactions with those dependencies at the very edges of your
system
In this section, I explain the remaining best practices:
Using mocks in integration tests only, not in unit tests
Always verifying the number of calls made to the mock
Mocking only types that you own
9.2.1
Mocks are for integration tests only
The guideline saying that mocks are for integration tests only, and that you shouldn’t
use mocks in unit tests, stems from the foundational principle described in chapter 7:
the separation of business logic and orchestration. Your code should either communi-
cate with out-of-process dependencies or be complex, but never both. This principle
naturally leads to the formation of two distinct layers: the domain model (that handles
complexity) and controllers (that handle the communication).
 Tests on the domain model fall into the category of unit tests; tests covering con-
trollers are integration tests. Because mocks are for unmanaged dependencies only,
and because controllers are the only code working with such dependencies, you
should only apply mocking when testing controllers—in integration tests. 
9.2.2
Not just one mock per test
You might sometimes hear the guideline of having only one mock per test. According
to this guideline, if you have more than one mock, you are likely testing several things
at a time.
 This is a misconception that follows from a more foundational misunderstanding
covered in chapter 2: that a unit in a unit test refers to a unit of code, and all such units
must be tested in isolation from each other. On the contrary: the term unit means
a unit of behavior, not a unit of code. The amount of code it takes to implement such a
unit of behavior is irrelevant. It could span across multiple classes, a single class, or
take up just a tiny method.
 With mocks, the same principle is at play: it’s irrelevant how many mocks it takes to ver-
ify a unit of behavior. Earlier in this chapter, it took us two mocks to check the scenario
of changing the user email from corporate to non-corporate: one for the logger and



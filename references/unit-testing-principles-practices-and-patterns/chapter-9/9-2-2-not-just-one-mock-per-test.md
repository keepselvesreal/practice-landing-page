# 9.2.2 Not just one mock per test (pp.225-226)

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


---
**Page 226**

226
CHAPTER 9
Mocking best practices
the other for the message bus. That number could have been larger. In fact, you don’t
have control over how many mocks to use in an integration test. The number of
mocks depends solely on the number of unmanaged dependencies participating in
the operation. 
9.2.3
Verifying the number of calls
When it comes to communications with unmanaged dependencies, it’s important to
ensure both of the following:
The existence of expected calls
The absence of unexpected calls
This requirement, once again, stems from the need to maintain backward compatibil-
ity with unmanaged dependencies. The compatibility must go both ways: your appli-
cation shouldn’t omit messages that external systems expect, and it also shouldn’t
produce unexpected messages. It’s not enough to check that the system under test
sends a message like this:
messageBusMock.Verify(
x => x.SendEmailChangedMessage(user.UserId, "new@gmail.com"));
You also need to ensure that this message is sent exactly once:
messageBusMock.Verify(
x => x.SendEmailChangedMessage(user.UserId, "new@gmail.com"),
Times.Once);      
With most mocking libraries, you can also explicitly verify that no other calls are
made on the mock. In Moq (the mocking library of my choice), this verification
looks as follows:
messageBusMock.Verify(
x => x.SendEmailChangedMessage(user.UserId, "new@gmail.com"),
Times.Once);
messageBusMock.VerifyNoOtherCalls();     
BusSpy implements this functionality, too:
busSpy
.ShouldSendNumberOfMessages(1)
.WithEmailChangedMessage(user.UserId, "new@gmail.com");
The spy’s check ShouldSendNumberOfMessages(1) encompasses both Times.Once and
VerifyNoOtherCalls() verifications from the mock. 
Ensures that the method 
is called only once
The additional 
check



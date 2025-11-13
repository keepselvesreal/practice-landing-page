# 5.1.2 Mock (the tool) vs. mock (the test double) (pp.94-96)

---
**Page 94**

94
CHAPTER 5
Mocks and test fragility
The difference between these two types boils down to the following:
Mocks help to emulate and examine outcoming interactions. These interactions
are calls the SUT makes to its dependencies to change their state.
Stubs help to emulate incoming interactions. These interactions are calls the
SUT makes to its dependencies to get input data (figure 5.2).
All other differences between the five variations are insignificant implementation
details. For example, spies serve the same role as mocks. The distinction is that spies
are written manually, whereas mocks are created with the help of a mocking frame-
work. Sometimes people refer to spies as handwritten mocks.
 On the other hand, the difference between a stub, a dummy, and a fake is in how
intelligent they are. A dummy is a simple, hardcoded value such as a null value or a
made-up string. It’s used to satisfy the SUT’s method signature and doesn’t partici-
pate in producing the final outcome. A stub is more sophisticated. It’s a fully fledged
dependency that you configure to return different values for different scenarios.
Finally, a fake is the same as a stub for most purposes. The difference is in the ratio-
nale for its creation: a fake is usually implemented to replace a dependency that
doesn’t yet exist.
 Notice the difference between mocks and stubs (aside from outcoming versus
incoming interactions). Mocks help to emulate and examine interactions between the
SUT and its dependencies, while stubs only help to emulate those interactions. This is
an important distinction. You will see why shortly. 
5.1.2
Mock (the tool) vs. mock (the test double)
The term mock is overloaded and can mean different things in different circum-
stances. I mentioned in chapter 2 that people often use this term to mean any test
double, whereas mocks are only a subset of test doubles. But there’s another meaning
System under test
SMTP server
Send an email
Retrieve data
Database
Stub
Mock
Figure 5.2
Sending an email is 
an outcoming interaction: an inter-
action that results in a side effect 
in the SMTP server. A test double 
emulating such an interaction is 
a mock. Retrieving data from the 
database is an incoming inter-
action; it doesn’t result in a 
side effect. The corresponding 
test double is a stub.


---
**Page 95**

95
Differentiating mocks from stubs
for the term mock. You can refer to the classes from mocking libraries as mocks, too.
These classes help you create actual mocks, but they themselves are not mocks per se.
The following listing shows an example.
[Fact]
public void Sending_a_greetings_email()
{
var mock = new Mock<IEmailGateway>();      
var sut = new Controller(mock.Object);
sut.GreetUser("user@email.com");
mock.Verify(
   
x => x.SendGreetingsEmail(   
"user@email.com"),
   
Times.Once);
   
}
The test in listing 5.1 uses the Mock class from the mocking library of my choice
(Moq). This class is a tool that enables you to create a test double—a mock. In other
words, the class Mock (or Mock<IEmailGateway>) is a mock (the tool), while the instance
of that class, mock, is a mock (the test double). It’s important not to conflate a mock (the
tool) with a mock (the test double) because you can use a mock (the tool) to create
both types of test doubles: mocks and stubs.
 The test in the following listing also uses the Mock class, but the instance of that
class is not a mock, it’s a stub.
[Fact]
public void Creating_a_report()
{
var stub = new Mock<IDatabase>();       
stub.Setup(x => x.GetNumberOfUsers())     
.Returns(10);
     
var sut = new Controller(stub.Object);
Report report = sut.CreateReport();
Assert.Equal(10, report.NumberOfUsers);
}
This test double emulates an incoming interaction—a call that provides the SUT with
input data. On the other hand, in the previous example (listing 5.1), the call to Send-
GreetingsEmail() is an outcoming interaction. Its sole purpose is to incur a side
effect—send an email. 
Listing 5.1
Using the Mock class from a mocking library to create a mock
Listing 5.2
Using the Mock class to create a stub
Uses a mock (the 
tool) to create a mock 
(the test double)
Examines the call 
from the SUT to 
the test double
Uses a mock 
(the tool) to 
create a stub
Sets up a 
canned answer


---
**Page 96**

96
CHAPTER 5
Mocks and test fragility
5.1.3
Don’t assert interactions with stubs
As I mentioned in section 5.1.1, mocks help to emulate and examine outcoming interac-
tions between the SUT and its dependencies, while stubs only help to emulate incom-
ing interactions, not examine them. The difference between the two stems from the
guideline of never asserting interactions with stubs. A call from the SUT to a stub is not
part of the end result the SUT produces. Such a call is only a means to produce the
end result: a stub provides input from which the SUT then generates the output.
NOTE
Asserting interactions with stubs is a common anti-pattern that leads to
fragile tests.
As you might remember from chapter 4, the only way to avoid false positives and thus
improve resistance to refactoring in tests is to make those tests verify the end result
(which, ideally, should be meaningful to a non-programmer), not implementation
details. In listing 5.1, the check
mock.Verify(x => x.SendGreetingsEmail("user@email.com"))
corresponds to an actual outcome, and that outcome is meaningful to a domain
expert: sending a greetings email is something business people would want the system
to do. At the same time, the call to GetNumberOfUsers() in listing 5.2 is not an out-
come at all. It’s an internal implementation detail regarding how the SUT gathers
data necessary for the report creation. Therefore, asserting this call would lead to test
fragility: it shouldn’t matter how the SUT generates the end result, as long as that
result is correct. The following listing shows an example of such a brittle test.
[Fact]
public void Creating_a_report()
{
var stub = new Mock<IDatabase>();
stub.Setup(x => x.GetNumberOfUsers()).Returns(10);
var sut = new Controller(stub.Object);
Report report = sut.CreateReport();
Assert.Equal(10, report.NumberOfUsers);
stub.Verify(
   
x => x.GetNumberOfUsers(),   
Times.Once);
   
}
This practice of verifying things that aren’t part of the end result is also called over-
specification. Most commonly, overspecification takes place when examining interac-
tions. Checking for interactions with stubs is a flaw that’s quite easy to spot because
tests shouldn’t check for any interactions with stubs. Mocks are a more complicated sub-
Listing 5.3
Asserting an interaction with a stub
Asserts the 
interaction 
with the stub



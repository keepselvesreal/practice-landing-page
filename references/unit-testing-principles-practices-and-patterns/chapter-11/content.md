# Unit testing anti-patterns (pp.259-Back cover)

---
**Page 259**

259
Unit testing anti-patterns
This chapter is an aggregation of lesser related topics (mostly anti-patterns) that
didn’t fit in earlier in the book and are better served on their own. An anti-pattern is
a common solution to a recurring problem that looks appropriate on the surface
but leads to problems further down the road.
 You will learn how to work with time in tests, how to identify and avoid such anti-
patterns as unit testing of private methods, code pollution, mocking concrete
classes, and more. Most of these topics follow from the first principles described in
part 2. Still, they are well worth spelling out explicitly. You’ve probably heard of at
least some of these anti-patterns in the past, but this chapter will help you connect
the dots, so to speak, and see the foundations they are based on.
This chapter covers
Unit testing private methods
Exposing private state to enable unit testing
Leaking domain knowledge to tests
Mocking concrete classes


---
**Page 260**

260
CHAPTER 11
Unit testing anti-patterns
11.1
Unit testing private methods
When it comes to unit testing, one of the most commonly asked questions is how to
test a private method. The short answer is that you shouldn’t do so at all, but there’s
quite a bit of nuance to this topic.
11.1.1 Private methods and test fragility
Exposing methods that you would otherwise keep private just to enable unit testing
violates one of the foundational principles we discussed in chapter 5: testing observ-
able behavior only. Exposing private methods leads to coupling tests to implementa-
tion details and, ultimately, damaging your tests’ resistance to refactoring—the most
important metric of the four. (All four metrics, once again, are protection against
regressions, resistance to refactoring, fast feedback, and maintainability.) Instead of
testing private methods directly, test them indirectly, as part of the overarching observ-
able behavior. 
11.1.2 Private methods and insufficient coverage
Sometimes, the private method is too complex, and testing it as part of the observable
behavior doesn’t provide sufficient coverage. Assuming the observable behavior
already has reasonable test coverage, there can be two issues at play:
This is dead code. If the uncovered code isn’t being used, this is likely some extra-
neous code left after a refactoring. It’s best to delete this code.
There’s a missing abstraction. If the private method is too complex (and thus is
hard to test via the class’s public API), it’s an indication of a missing abstraction
that should be extracted into a separate class.
Let’s illustrate the second issue with an example.
public class Order
{
private Customer _customer;
private List<Product> _products;
public string GenerateDescription()
{
return $"Customer name: {_customer.Name}, " +
$"total number of products: {_products.Count}, " +
$"total price: {GetPrice()}";             
}
private decimal GetPrice()     
{
decimal basePrice = /* Calculate based on _products */;
decimal discounts = /* Calculate based on _customer */;
decimal taxes = /* Calculate based on _products */;
Listing 11.1
A class with a complex private method
The complex private
method is used by a
much simpler public
method.
Complex private 
method


---
**Page 261**

261
Unit testing private methods
return basePrice - discounts + taxes;
}
}
The GenerateDescription() method is quite simple: it returns a generic description
of the order. But it uses the private GetPrice() method, which is much more com-
plex: it contains important business logic and needs to be thoroughly tested. That
logic is a missing abstraction. Instead of exposing the GetPrice method, make this
abstraction explicit by extracting it into a separate class, as shown in the next listing.
public class Order
{
private Customer _customer;
private List<Product> _products;
public string GenerateDescription()
{
var calc = new PriceCalculator();
return $"Customer name: {_customer.Name}, " +
$"total number of products: {_products.Count}, " +
$"total price: {calc.Calculate(_customer, _products)}";
}
}
public class PriceCalculator
{
public decimal Calculate(Customer customer, List<Product> products)
{
decimal basePrice = /* Calculate based on products */;
decimal discounts = /* Calculate based on customer */;
decimal taxes = /* Calculate based on products */;
return basePrice - discounts + taxes;
}
}
Now you can test PriceCalculator independently of Order. You can also use the
output-based (functional) style of unit testing, because PriceCalculator doesn’t
have any hidden inputs or outputs. See chapter 6 for more information about styles
of unit testing. 
11.1.3 When testing private methods is acceptable
There are exceptions to the rule of never testing private methods. To understand
those exceptions, we need to revisit the relationship between the code’s publicity and
purpose from chapter 5. Table 11.1 sums up that relationship (you already saw this
table in chapter 5; I’m copying it here for convenience).
Listing 11.2
Extracting the complex private method


---
**Page 262**

262
CHAPTER 11
Unit testing anti-patterns
As you might remember from chapter 5, making the observable behavior public and
implementation details private results in a well-designed API. On the other hand,
leaking implementation details damages the code’s encapsulation. The intersection of
observable behavior and private methods is marked N/A in the table because for a
method to become part of observable behavior, it has to be used by the client code,
which is impossible if that method is private.
 Note that testing private methods isn’t bad in and of itself. It’s only bad because
those private methods are a proxy for implementation details. Testing implementa-
tion details is what ultimately leads to test brittleness. Having that said, there are rare
cases where a method is both private and part of observable behavior (and thus the
N/A marking in table 11.1 isn’t entirely correct).
 Let’s take a system that manages credit inquiries as an example. New inquiries are
bulk-loaded directly into the database once a day. Administrators then review those
inquiries one by one and decide whether to approve them. Here’s how the Inquiry
class might look in that system.
public class Inquiry
{
public bool IsApproved { get; private set; }
public DateTime? TimeApproved { get; private set; }
private Inquiry(
  
bool isApproved, DateTime? timeApproved)  
{
if (isApproved && !timeApproved.HasValue)
throw new Exception();
IsApproved = isApproved;
TimeApproved = timeApproved;
}
public void Approve(DateTime now)
{
if (IsApproved)
return;
IsApproved = true;
TimeApproved = now;
}
}
Table 11.1
The relationship between the code’s publicity and purpose
Observable behavior
Implementation detail
Public
Good
Bad
Private
N/A
Good
Listing 11.3
A class with a private constructor
Private 
constructor


---
**Page 263**

263
Exposing private state
The private constructor is private because the class is restored from the database by an
object-relational mapping (ORM) library. That ORM doesn’t need a public construc-
tor; it may well work with a private one. At the same time, our system doesn’t need a
constructor, either, because it’s not responsible for the creation of those inquiries.
 How do you test the Inquiry class given that you can’t instantiate its objects? On
the one hand, the approval logic is clearly important and thus should be unit tested.
But on the other, making the constructor public would violate the rule of not expos-
ing private methods.
 Inquiry’s constructor is an example of a method that is both private and part of
the observable behavior. This constructor fulfills the contract with the ORM, and the
fact that it’s private doesn’t make that contract less important: the ORM wouldn’t be
able to restore inquiries from the database without it.
 And so, making Inquiry’s constructor public won’t lead to test brittleness in this par-
ticular case. In fact, it will arguably bring the class’s API closer to being well-designed.
Just make sure the constructor contains all the preconditions required to maintain its
encapsulation. In listing 11.3, such a precondition is the requirement to have the
approval time in all approved inquiries.
 Alternatively, if you prefer to keep the class’s public API surface as small as possi-
ble, you can instantiate Inquiry via reflection in tests. Although this looks like a hack,
you are just following the ORM, which also uses reflection behind the scenes. 
11.2
Exposing private state
Another common anti-pattern is exposing private state for the sole purpose of unit
testing. The guideline here is the same as with private methods: don’t expose state
that you would otherwise keep private—test observable behavior only. Let’s take a
look at the following listing.
public class Customer
{
private CustomerStatus _status =   
CustomerStatus.Regular;
   
public void Promote()
{
_status = CustomerStatus.Preferred;
}
public decimal GetDiscount()
{
return _status == CustomerStatus.Preferred ? 0.05m : 0m;
}
}
public enum CustomerStatus
{
Listing 11.4
A class with private state
Private 
state


---
**Page 264**

264
CHAPTER 11
Unit testing anti-patterns
Regular,
Preferred
}
This example shows a Customer class. Each customer is created in the Regular status
and then can be promoted to Preferred, at which point they get a 5% discount on
everything.
 How would you test the Promote() method? This method’s side effect is a change
of the _status field, but the field itself is private and thus not available in tests. A
tempting solution would be to make this field public. After all, isn’t the change of sta-
tus the ultimate goal of calling Promote()?
 That would be an anti-pattern, however. Remember, your tests should interact with the
system under test (SUT) exactly the same way as the production code and shouldn’t have any spe-
cial privileges. In listing 11.4, the _status field is hidden from the production code and
thus is not part of the SUT’s observable behavior. Exposing that field would result in
coupling tests to implementation details. How to test Promote(), then?
 What you should do, instead, is look at how the production code uses this class. In
this particular example, the production code doesn’t care about the customer’s status;
otherwise, that field would be public. The only information the production code does
care about is the discount the customer gets after the promotion. And so that’s what
you need to verify in tests. You need to check that
A newly created customer has no discount.
Once the customer is promoted, the discount becomes 5%.
Later, if the production code starts using the customer status field, you’d be able to
couple to that field in tests too, because it would officially become part of the SUT’s
observable behavior.
NOTE
Widening the public API surface for the sake of testability is a bad practice. 
11.3
Leaking domain knowledge to tests
Leaking domain knowledge to tests is another quite common anti-pattern. It usually
takes place in tests that cover complex algorithms. Let’s take the following (admit-
tedly, not that complex) calculation algorithm as an example:
public static class Calculator
{
public static int Add(int value1, int value2)
{
return value1 + value2;
}
}
This listing shows an incorrect way to test it.


---
**Page 265**

265
Leaking domain knowledge to tests
public class CalculatorTests
{
[Fact]
public void Adding_two_numbers()
{
int value1 = 1;
int value2 = 3;
int expected = value1 + value2;      
int actual = Calculator.Add(value1, value2);
Assert.Equal(expected, actual);
}
}
You could also parameterize the test to throw in a couple more test cases at almost no
additional cost.
public class CalculatorTests
{
[Theory]
[InlineData(1, 3)]
[InlineData(11, 33)]
[InlineData(100, 500)]
public void Adding_two_numbers(int value1, int value2)
{
int expected = value1 + value2;    
int actual = Calculator.Add(value1, value2);
Assert.Equal(expected, actual);
}
}
Listings 11.5 and 11.6 look fine at first, but they are, in fact, examples of the anti-pattern:
these tests duplicate the algorithm implementation from the production code. Of
course, it might not seem like a big deal. After all, it’s just one line. But that’s only
because the example is rather simplified. I’ve seen tests that covered complex algo-
rithms and did nothing but reimplement those algorithms in the arrange part. They
were basically a copy-paste from the production code.
 These tests are another example of coupling to implementation details. They score
almost zero on the metric of resistance to refactoring and are worthless as a result.
Such tests don’t have a chance of differentiating legitimate failures from false posi-
tives. Should a change in the algorithm make those tests fail, the team would most
likely just copy the new version of that algorithm to the test without even trying to
Listing 11.5
Leaking algorithm implementation
Listing 11.6
A parameterized version of the same test
The leakage
The leakage


---
**Page 266**

266
CHAPTER 11
Unit testing anti-patterns
identify the root cause (which is understandable, because the tests were a mere dupli-
cation of the algorithm in the first place).
 How to test the algorithm properly, then? Don’t imply any specific implementation when
writing tests. Instead of duplicating the algorithm, hard-code its results into the test, as
shown in the following listing.
public class CalculatorTests
{
[Theory]
[InlineData(1, 3, 4)]
[InlineData(11, 33, 44)]
[InlineData(100, 500, 600)]
public void Adding_two_numbers(int value1, int value2, int expected)
{
int actual = Calculator.Add(value1, value2);
Assert.Equal(expected, actual);
}
}
It can seem counterintuitive at first, but hardcoding the expected result is a good
practice when it comes to unit testing. The important part with the hardcoded values
is to precalculate them using something other than the SUT, ideally with the help of a
domain expert. Of course, that’s only if the algorithm is complex enough (we are all
experts at summing up two numbers). Alternatively, if you refactor a legacy applica-
tion, you can have the legacy code produce those results and then use them as expected
values in tests. 
11.4
Code pollution
The next anti-pattern is code pollution.
DEFINITION
Code pollution is adding production code that’s only needed for
testing.
Code pollution often takes the form of various types of switches. Let’s take a logger as
an example.
public class Logger
{
private readonly bool _isTestEnvironment;
public Logger(bool isTestEnvironment)    
{
_isTestEnvironment = isTestEnvironment;
}
Listing 11.7
Test with no domain knowledge
Listing 11.8
Logger with a Boolean switch 
The switch


---
**Page 267**

267
Code pollution
public void Log(string text)
{
if (_isTestEnvironment)     
return;
/* Log the text */
}
}
public class Controller
{
public void SomeMethod(Logger logger)
{
logger.Log("SomeMethod is called");
}
}
In this example, Logger has a constructor parameter that indicates whether the class
runs in production. If so, the logger records the message into the file; otherwise, it
does nothing. With such a Boolean switch, you can disable the logger during test runs,
as shown in the following listing.
[Fact]
public void Some_test()
{
var logger = new Logger(true);    
var sut = new Controller();
sut.SomeMethod(logger);
/* assert */
}
The problem with code pollution is that it mixes up test and production code and
thereby increases the maintenance costs of the latter. To avoid this anti-pattern, keep
the test code out of the production code base.
 In the example with Logger, introduce an ILogger interface and create two imple-
mentations of it: a real one for production and a fake one for testing purposes. After
that, re-target Controller to accept the interface instead of the concrete class, as
shown in the following listing.
public interface ILogger
{
void Log(string text);
}
Listing 11.9
A test using the Boolean switch
Listing 11.10
A version without the switch
The switch
Sets the parameter to 
true to indicate the 
test environment


---
**Page 268**

268
CHAPTER 11
Unit testing anti-patterns
public class Logger : ILogger
  
{
  
public void Log(string text)  
{
  
/* Log the text */
  
}
  
}
  
public class FakeLogger : ILogger   
{
   
public void Log(string text)    
{
   
/* Do nothing */
   
}
   
}
   
public class Controller
{
public void SomeMethod(ILogger logger)
{
logger.Log("SomeMethod is called");
}
}
Such a separation helps keep the production logger simple because it no longer has
to account for different environments. Note that ILogger itself is arguably a form of
code pollution: it resides in the production code base but is only needed for testing.
So how is the new implementation better?
 The kind of pollution ILogger introduces is less damaging and easier to deal
with. Unlike the initial Logger implementation, with the new version, you can’t acci-
dentally invoke a code path that isn’t intended for production use. You can’t have
bugs in interfaces, either, because they are just contracts with no code in them. In
contrast to Boolean switches, interfaces don’t introduce additional surface area for
potential bugs. 
11.5
Mocking concrete classes
So far, this book has shown mocking examples using interfaces, but there’s an alterna-
tive approach: you can mock concrete classes instead and thus preserve part of the
original classes’ functionality, which can be useful at times. This alternative has a sig-
nificant drawback, though: it violates the Single Responsibility principle. The next list-
ing illustrates this idea.
public class StatisticsCalculator
{
public (double totalWeight, double totalCost) Calculate(
int customerId)
{
List<DeliveryRecord> records = GetDeliveries(customerId);
Listing 11.11
A class that calculates statistics
Belongs in the 
production code
Belongs in 
the test code


---
**Page 269**

269
Mocking concrete classes
double totalWeight = records.Sum(x => x.Weight);
double totalCost = records.Sum(x => x.Cost);
return (totalWeight, totalCost);
}
public List<DeliveryRecord> GetDeliveries(int customerId)
{
/* Call an out-of-process dependency
to get the list of deliveries */
}
}
StatisticsCalculator gathers and calculates customer statistics: the weight and cost
of all deliveries sent to a particular customer. The class does the calculation based on
the list of deliveries retrieved from an external service (the GetDeliveries method).
Let’s also say there’s a controller that uses StatisticsCalculator, as shown in the fol-
lowing listing.
public class CustomerController
{
private readonly StatisticsCalculator _calculator;
public CustomerController(StatisticsCalculator calculator)
{
_calculator = calculator;
}
public string GetStatistics(int customerId)
{
(double totalWeight, double totalCost) = _calculator
.Calculate(customerId);
return
$"Total weight delivered: {totalWeight}. " +
$"Total cost: {totalCost}";
}
}
How would you test this controller? You can’t supply it with a real Statistics-
Calculator instance, because that instance refers to an unmanaged out-of-process
dependency. The unmanaged dependency has to be substituted with a stub. At the
same time, you don’t want to replace StatisticsCalculator entirely, either. This
class contains important calculation functionality, which needs to be left intact.
 One way to overcome this dilemma is to mock the StatisticsCalculator class
and override only the GetDeliveries() method, which can be done by making that
method virtual, as shown in the following listing.
 
Listing 11.12
A controller using StatisticsCalculator


---
**Page 270**

270
CHAPTER 11
Unit testing anti-patterns
[Fact]
public void Customer_with_no_deliveries()
{
// Arrange
var stub = new Mock<StatisticsCalculator> { CallBase = true };
stub.Setup(x => x.GetDeliveries(1))         
.Returns(new List<DeliveryRecord>());
var sut = new CustomerController(stub.Object);
// Act
string result = sut.GetStatistics(1);
// Assert
Assert.Equal("Total weight delivered: 0. Total cost: 0", result);
}
The CallBase = true setting tells the mock to preserve the base class’s behavior unless
it’s explicitly overridden. With this approach, you can substitute only a part of the class
while keeping the rest as-is. As I mentioned earlier, this is an anti-pattern.
NOTE
The necessity to mock a concrete class in order to preserve part of its
functionality is a result of violating the Single Responsibility principle.
StatisticsCalculator combines two unrelated responsibilities: communicating with
the unmanaged dependency and calculating statistics. Look at listing 11.11 again. The
Calculate() method is where the domain logic lies. GetDeliveries() just gathers
the inputs for that logic. Instead of mocking StatisticsCalculator, split this class in
two, as the following listing shows.
public class DeliveryGateway : IDeliveryGateway
{
public List<DeliveryRecord> GetDeliveries(int customerId)
{
/* Call an out-of-process dependency
to get the list of deliveries */
}
}
public class StatisticsCalculator
{
public (double totalWeight, double totalCost) Calculate(
List<DeliveryRecord> records)
{
double totalWeight = records.Sum(x => x.Weight);
double totalCost = records.Sum(x => x.Cost);
return (totalWeight, totalCost);
}
}
Listing 11.13
Test that mocks the concrete class
Listing 11.14
Splitting StatisticsCalculator into two classes
GetDeliveries() must 
be made virtual.


---
**Page 271**

271
Working with time
The next listing shows the controller after the refactoring.
public class CustomerController
{
private readonly StatisticsCalculator _calculator;
private readonly IDeliveryGateway _gateway;
public CustomerController(
StatisticsCalculator calculator,   
IDeliveryGateway gateway)
   
{
_calculator = calculator;
_gateway = gateway;
}
public string GetStatistics(int customerId)
{
var records = _gateway.GetDeliveries(customerId);
(double totalWeight, double totalCost) = _calculator
.Calculate(records);
return
$"Total weight delivered: {totalWeight}. " +
$"Total cost: {totalCost}";
}
}
The responsibility of communicating with the unmanaged dependency has transi-
tioned to DeliveryGateway. Notice how this gateway is backed by an interface, which
you can now use for mocking instead of the concrete class. The code in listing 11.15 is
an example of the Humble Object design pattern in action. Refer to chapter 7 to
learn more about this pattern. 
11.6
Working with time
Many application features require access to the current date and time. Testing func-
tionality that depends on time can result in false positives, though: the time during
the act phase might not be the same as in the assert. There are three options for stabi-
lizing this dependency. One of these options is an anti-pattern; and of the other two,
one is preferable to the other.
11.6.1 Time as an ambient context
The first option is to use the ambient context pattern. You already saw this pattern in
chapter 8 in the section about testing loggers. In the context of time, the ambient con-
text would be a custom class that you’d use in code instead of the framework’s built-in
DateTime.Now, as shown in the next listing.
 
Listing 11.15
Controller after the refactoring
Two separate 
dependencies


---
**Page 272**

272
CHAPTER 11
Unit testing anti-patterns
public static class DateTimeServer
{
private static Func<DateTime> _func;
public static DateTime Now => _func();
public static void Init(Func<DateTime> func)
{
_func = func;
}
}
DateTimeServer.Init(() => DateTime.Now);     
DateTimeServer.Init(() => new DateTime(2020, 1, 1));      
Just as with the logger functionality, using an ambient context for time is also an anti-
pattern. The ambient context pollutes the production code and makes testing more
difficult. Also, the static field introduces a dependency shared between tests, thus tran-
sitioning those tests into the sphere of integration testing. 
11.6.2 Time as an explicit dependency
A better approach is to inject the time dependency explicitly (instead of referring to it
via a static method in an ambient context), either as a service or as a plain value, as
shown in the following listing.
public interface IDateTimeServer
{
DateTime Now { get; }
}
public class DateTimeServer : IDateTimeServer
{
public DateTime Now => DateTime.Now;
}
public class InquiryController
{
private readonly DateTimeServer _dateTimeServer;
public InquiryController(
DateTimeServer dateTimeServer)    
{
_dateTimeServer = dateTimeServer;
}
public void ApproveInquiry(int id)
{
Inquiry inquiry = GetById(id);
Listing 11.16
Current date and time as an ambient context
Listing 11.17
Current date and time as an explicit dependency
Initialization code 
for production
Initialization code 
for unit tests
Injects time as 
a service


---
**Page 273**

273
Summary
inquiry.Approve(_dateTimeServer.Now);      
SaveInquiry(inquiry);
}
}
Of these two options, prefer injecting the time as a value rather than as a service. It’s
easier to work with plain values in production code, and it’s also easier to stub those
values in tests.
 Most likely, you won’t be able to always inject the time as a plain value, because
dependency injection frameworks don’t play well with value objects. A good compro-
mise is to inject the time as a service at the start of a business operation and then
pass it as a value in the remainder of that operation. You can see this approach in
listing 11.17: the controller accepts DateTimeServer (the service) but then passes a
DateTime value to the Inquiry domain class. 
11.7
Conclusion
In this chapter, we looked at some of the most prominent real-world unit testing use
cases and analyzed them using the four attributes of a good test. I understand that it
may be overwhelming to start applying all the ideas and guidelines from this book at
once. Also, your situation might not be as clear-cut. I publish reviews of other people’s
code and answer questions (related to unit testing and code design in general) on my
blog at https://enterprisecraftsmanship.com. You can also submit your own question
at https://enterprisecraftsmanship.com/about. You might also be interested in taking
my online course, where I show how to build an application from the ground up,
applying all the principles described in this book in practice, at https://unittesting-
course.com.
 You can always catch me on twitter at @vkhorikov, or contact me directly through
https://enterprisecraftsmanship.com/about. I look forward to hearing from you!
Summary
Exposing private methods to enable unit testing leads to coupling tests to
implementation and, ultimately, damaging the tests’ resistance to refactoring.
Instead of testing private methods directly, test them indirectly as part of the
overarching observable behavior.
If the private method is too complex to be tested as part of the public API that
uses it, that’s an indication of a missing abstraction. Extract this abstraction into
a separate class instead of making the private method public.
In rare cases, private methods do belong to the class’s observable behavior.
Such methods usually implement a non-public contract between the class and
an ORM or a factory.
Don’t expose state that you would otherwise keep private for the sole purpose
of unit testing. Your tests should interact with the system under test exactly the
same way as the production code; they shouldn’t have any special privileges.
Injects time as 
a plain value


---
**Page 274**

274
CHAPTER 11
Unit testing anti-patterns
Don’t imply any specific implementation when writing tests. Verify the produc-
tion code from a black-box perspective; avoid leaking domain knowledge to
tests (see chapter 4 for more details about black-box and white-box testing).
Code pollution is adding production code that’s only needed for testing. It’s an
anti-pattern because it mixes up test and production code and increases the
maintenance costs of the latter.
The necessity to mock a concrete class in order to preserve part of its function-
ality is a result of violating the Single Responsibility principle. Separate that
class into two classes: one with the domain logic, and the other one communi-
cating with the out-of-process dependency.
Representing the current time as an ambient context pollutes the production
code and makes testing more difficult. Inject time as an explicit dependency—
either as a service or as a plain value. Prefer the plain value whenever possible.


---
**Page 275**

275
index
A
AAA (arrange, act, and assert) pattern 42–49
avoiding if statements 44–45
avoiding multiple AAA sections 43–44
differentiating system under test 47–48
dropping AAA comments 48–49
overview 42–43
reusing code in test sections 246–252
in act sections 249–250
in arrange sections 246–249
in assert sections 250
section size 45–47
arrange section 45
number of assertions in assert 
section 47
sections larger than a single line 45–47
teardown phase 47
abstractions 198, 260
Active Record pattern 159
adapters 227
aggregates 157
ambient context 212
anti-patterns 212
code pollution 266–268
exposing private state 263–264
leaking domain knowledge to tests
264–266
mocking concrete classes 268–271
private methods 260–263
acceptability of testing 261–263
insufficient coverage 260–261
test fragility 260
time 271–273
as ambient context 271–272
as explicit dependency 272–273
API (application programming interface) 104, 
111, 133, 191, 195, 227, 264
missing abstractions 260
public vs. private 99
well-designed 100–101, 105, 108, 262
application behavior 57
application services layer 133–134
arrange, act, and assert pattern. See AAA 
pattern
assertion libraries, using to improve test 
readability 62–63
assertion-free testing 12–13
asynchronous communications 191
atomic updates 236
automation concepts 87–90
black-box vs. white-box testing 89–90
Test Pyramid 87–89
B
backward migration 233
bad tests 189
black-box testing 68, 89–90
Boolean switches 266–268
branch coverage metric 10–11
brittle tests 83–84, 116, 216
brittleness 86, 125
bugs 68, 79, 104, 175, 189
business logic 106–107, 156, 169, 
179
C
CanExecute/Execute pattern 172, 174
CAP theorem 86–87
captured data 208


---
**Page 276**

INDEX
276
circular dependencies 203
defined 202
eliminating 202–204
classical school of unit testing 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 27–30
mocks 114–116
mocking out out-of-process dependencies
115–116
using mocks to verify behavior 116
precise bug location 36
testing large graph of interconnected classes 35
testing one class at a time 34–35
cleanup phase 244
clusters, grouping into aggregates 157
code complexity 104, 152
code coverage metric 9–10
code coverage tools 90
code depth 157
code pollution 127, 266–268, 272
code width 157
collaborators 32, 148, 153
command query separation. See CQS principle
commands 97
communication-based testing 122–123, 128
feedback speed 124
maintainability 127
overuse of 124
protection against regressions and feedback 
speed 124
resistance to refactoring 124–125
vulnerability to false alarms 124
communications
between applications 107, 110
between classes in application 110, 116
conditional logic 169–180
CanExecute/Execute pattern 172–174
domain events for tracking changes in the 
domain model 175–178
constructors, reusing test fixtures between 
tests 52
containers 244
controllers 153, 225
simplicity 171
coverage metrics, measuring test suite quality 
with 8–15
aiming for particular coverage number 15
branch coverage metric 10–11
code coverage metric 9–10
problems with 12–15
code paths in external libraries 14–15
impossible to verify all possible outcomes
12–13
CQS (command query separation) principle
97–98
CRUD (create, read, update, and delete) 
operations 89
CSV files 208–209
cyclic dependency 202
cyclomatic complexity 152
D
data inconsistencies 241
data mapping 254
data motion 234
data, bundling 104
database backup, restoring 244
database management system (DBMS) 246
database testing
common questions 252–255
testing reads 252–253
testing repositories 253–254
database transaction management 234–243
in integration tests 242–243
in production code 235–242
prerequisites for 230–234
keeping database in source control 
system 230–231
reference data as part of database 
schema 231
separate instances for every developer
232
state-based vs. migration-based database 
delivery 232–234
reusing code in test sections 246–252
creating too many database 
transactions 251–252
in act sections 249–250
in arrange sections 246–249
in assert sections 250
test data life cycle 243–246
avoiding in-memory databases 246
clearing data between test runs 244–245
parallel vs. sequential test execution
243–244
database transaction management 234–243
in integration tests 242–243
in production code 235–242
separating connections from transactions
236–239
upgrading transaction to unit of work
239–242
database transactions 244
daysFromNow parameter 60
DBMS (database management system) 246
dead code 260
deliveryDate parameter 62


---
**Page 277**

INDEX
277
dependencies 28–29, 35
classical school of unit testing 30–34
London school of unit testing 30–34
out-of-process 161, 190
shared 29, 31
types of 115
Detroit approach, unit testing 21
diagnostic logging 206, 212
discovered abstractions 198
Docker container 28
domain events, tracking changes in domain 
model 175–178
domain layers 106–107, 109, 133–134
domain model 16, 153, 225
connecting with external applications 111
testability 171
domain significance 153
dummy test double 93–94
E
EasyMock 25
edge cases 187, 189, 194
encapsulation 46, 252
end-to-end tests 88–89, 195–196, 205, 222
classical school of unit testing 38–39
London school of unit testing 38–39
possibility of creating ideal tests 81
enterprise applications 5
Entity Framework 240–242, 255
entropy 6
error handling 146
exceptions 130
expected parameter 62
explicit inputs and outputs 130
external libraries 81
external reads 170–171, 173
external state 130
external writes 170–171, 173
F
Fail Fast principle 185, 189
failing preconditions 190
fake dependencies 93
fake test double 93–94
false negatives 76–77
false positives 69–70, 77, 82, 86, 96, 99, 124
causes of 71–74
importance of 78–79
fast feedback 81–86, 88, 99, 123, 252, 260
fat controllers 154
feedback loop, shortening 189
feedback speed 79–80, 124
fixed state 50
Fluent Assertions 62
fragile tests 96, 113
frameworks 81
functional architecture 128–134
defined 132–133
drawbacks of 146–149
applicability of 147–148
code base size increases 149
performance drawbacks 148
functional programming 128–131
hexagonal architecture 133–134
transitioning to output-based testing 135–146
audit system 135–137
refactoring toward functional 
architecture 140–145
using mocks to decouple tests from 
filesystem 137–140
functional core 132–133, 143–144, 156
functional programming 121
functional testing 38, 121, 128
G
Git 230–231
Given-When-Then pattern 43
GUI (graphical user interface) tests 38
H
handwritten mocks 94, 222
happy paths 187, 194, 239
helper methods 126–127
hexagonal architecture 106–107, 128, 156
defining 106–110
functional architecture 133–134
purpose of 107
hexagons 106, 108, 134
hidden outputs 131
high coupling, reusing test fixtures between 
tests 52
HTML tags 72
humble controller 160
Humble Object pattern 155, 157–158, 167, 271
humble objects 157
humble wrappers 155
I
ideal tests 80–87
brittle tests 83–84
end-to-end tests 81
possibility of creating 81
trivial tests 82–83
if statements 10–11, 44–45, 143, 152, 173–174
immutability 133


---
**Page 278**

INDEX
278
immutable classes 133
immutable core 132, 134
immutable events 176
immutable objects 30, 132
implementation details 99–105
incoming interactions 94–95
infrastructure code 16
infrastructure layer 202
in-memory databases 246
in-process dependencies 199–200
INSERT statements 231
integer type 14
integration testing
best practices 200–205
eliminating circular dependencies
202–204
making domain model boundaries 
explicit 200
multiple act sections 204–205
reducing number of layers 200–202
classical school of unit testing 37–39
database transaction management in
242–243
defined 186–190
example of 193–197
categorizing database and message bus 195
end-to-end testing 195–196
first version 196–197
scenarios 194
failing fast 188–190
interfaces for abstracting dependencies
197–200
in-process dependencies 199–200
loose coupling and 198
out-of-process dependencies 199
logging functionality 205–213
amount of logging 212
introducing wrapper on top of ILogger
207–208
passing around logger instances 212–213
structured logging 208–209
whether to test or not 205–206
writing tests for support and diagnostic 
logging 209–211
London school of unit testing 37–39
out-of-process dependencies 190–193
types of 190–191
when real databases are unavailable
192–193
working with both 191–192
role of 186–187
Test Pyramid 187
interconnected classes 34
internal keyword 99
invariant violations 46, 103
invariants 100, 103
isolation issue
classical school of unit testing 27–30
London school of unit testing 21–27
isSuccess flag 113
J
JMock 25
JSON files 208–209
L
logging functionality testing 205–213
amount of logging 212
introducing wrapper on top of ILogger
207–208
passing around logger instances 212–213
structured logging 208–209
whether to test or not 205–206
writing tests for support and diagnostic 
logging 209–211
London school of unit testing 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 21–27
mocks 114–116
mocking out out-of-process dependencies
115–116
using mocks to verify behavior 116
precise bug location 36
testing large graph of interconnected classes 35
testing one class at a time 34–35
loose coupling, interfaces for abstracting depen-
dencies and 198
M
maintainability 79–80, 85, 88, 99, 137, 148, 
252, 260
comparing testing styles 125–127
communication-based tests 127
output-based tests 125
state-based tests 125–127
managed dependencies 190, 192, 246
mathematical functions 128–131
merging domain events 177
message bus 190–192, 199, 220, 224
method signatures 128
method under test (MUT) 25
Microsoft MSTest 49
migration-based database delivery 232–234
missing abstractions 260
mock chains 127


---
**Page 279**

INDEX
279
mocking frameworks 25
mockist style, unit testing 21
Mockito 25
mocks 25, 254
best practices 225–227
for integration tests only 225
not just one mock per test 225–226
only mock types that you own 227
verifying number of calls 226
decoupling tests from filesystem 137–140
defined 25
London school vs. classical school 114–116
mocking out out-of-process 
dependencies 115–116
using mocks to verify behavior 116
maximizing value of 217–225
IDomainLogger 224–225
replacing mocks with spies 222–224
verifying interactions at system edges
219–222
mocking concrete classes 268–271
observable behavior vs. implementation 
details 99–105
leaking implementation details 100–105
observable behavior vs. public API 99–100
well-designed API and encapsulation
103–104
stubs 93–98
asserting interactions with stubs 96–97
commands and queries 97–98
mock (tool) vs. mock (test double) 94–95
types of test doubles 93–94
using mocks and stubs together 97
test doubles 25
test fragility 106–114
defining hexagonal architecture 106–110
intra-system vs. inter-system 
communications 110–114
model database 230
Model-View-Controller (MVC) pattern 157
Moq 25, 95, 226
MSTest 49
MUT (method under test) 25
mutable objects 132
mutable shell 132–133, 143–144
MVC (Model-View-Controller) pattern 157
N
naming tests 54–58
guidelines for 56
renaming tests to meet guidelines 56–58
NHibernate 240
noise, reducing 78
NSubstitute 25
NuGet package 49
NUnit 49, 51
O
object graphs 22–23
Object Mother 248
object-oriented programming (OOP) 63, 133
object-relational mapping (ORM) 163, 177, 
227, 240, 243, 254–255, 263
observable behavior 99, 105, 108, 115, 263
leaking implementation details 100–105
public API 99–100
well-designed API and encapsulation 103–104
OCP (Open-Closed principle) 198
OOP (object-oriented programming) 63, 133
Open-Closed principle (OCP) 198
operations 99, 104
orchestration, separating business logic from
169, 179
ORM (object-relational mapping) 163, 177, 
227, 240, 243, 254–255, 263
outcoming interactions 94–95
out-of-process collaborators 159–160
out-of-process dependencies 28, 33, 38–39, 
115, 125, 148, 160–161, 167, 170, 176, 
186, 200, 229
integration testing 190–193
interfaces for abstracting dependencies 199
types of 190–191
when real databases are unavailable
192–193
working with both 191–192
output value 121
output-based testing 120–121, 124, 128
feedback speed 124
maintainability 125
protection against regressions and feedback 
speed 124
resistance to refactoring 124–125
transitioning to functional architecture 
and 135–146
audit system 135–137
refactoring toward functional 
architecture 140–145
using mocks to decouple tests from 
filesystem 137–140
overcomplicated code 154
overspecification 96
P
parallel test execution 243–244
parameterized tests 59, 61
partition tolerance 86


---
**Page 280**

INDEX
280
performance 171
persistence state 189
preconditions 190
private APIs 99
private constructors 263
private dependencies 28–29, 31, 115
private keyword 99
private methods 260–263
acceptability of testing 261–263
insufficient coverage and 260–261
reusing test fixtures between tests 52–54
test fragility and 260
Product array 129
production code 8
protection against regressions 68–69, 81, 84–86, 
88, 99, 260
comparing testing styles 124
importance of false positives and false 
negatives 78–79
maximizing test accuracy 76–78
Public API 99, 109
pure functions 128
Q
queries 97
R
random number generators 29
read operations 252
readability 53
read-decide-act approach 148
refactoring 165
analysis of optimal test coverage 167–169
testing domain layer and utility code 167–168
testing from other three quadrants 168
testing preconditions 169
conditional logic in controllers 169–180
CanExecute/Execute pattern 172–174
domain events for tracking changes in the 
domain model 175–178
identifying code to refactor 152–158
four types of code 152–155
Humble Object pattern for splitting overcom-
plicated code 155–158
resistance to 69–71
comparing testing styles 124–125
importance of false positives and false 
negatives 78–79
maximizing test accuracy 76–78
to parameterized tests
general discussion 58–62
generating data for parameterized tests
60–62
toward valuable unit tests 158–167
application services layer 160–162
Company class 164–167
customer management system 158–160
making implicit dependencies explicit 160
removing complexity from application 
service 163–164
reference data 231, 234, 245
referential transparency 130
regression errors 8, 69, 82
regressions 7, 229
repositories 236–237, 241, 253
resistance to refactoring 69–71, 79–81, 83–85, 
88–90, 92–93, 99, 123, 260, 265
comparing testing styles 124–125
importance of false positives and false 
negatives 78–79
maximizing test accuracy 76–78
return statement 10
return true statement 10
reusability 53
S
scalability 7
sequential test execution 243–244
shallowness 124–125
shared dependencies 28–29, 31, 33, 115, 148, 246
side effects 130–134, 190
signal-to-noise ratio 212
Single Responsibility principle 157, 268, 270
single-line act section 45
SMTP service 110, 112–115, 134, 190
software bugs 7, 68
software entropy 6
source of truth 231
spies 94, 222–224
spy test double 93
SQL scripts 231–232, 240, 245
SQLite 246
state 99, 101
state verification 125
state-based database delivery 232
state-based testing 120–122, 124, 128, 135
feedback speed 124
maintainability 125–127
protection against regressions and feedback 
speed 124
resistance to refactoring 124–125
stubs, mocks 93–98
asserting interactions with stubs 96–97
commands and queries 97–98
mock (tool) vs. mock (test double) 94–95
types of test doubles 93–94
using mocks and stubs together 97


---
**Page 281**

INDEX
281
sub-renderers collection 105
support logging 206, 212
sustainability 7
sustainable growth 6
SUT (system under test) 24–25, 29, 36–37, 43, 
45, 47–48, 57, 71, 73–75, 84, 93–94, 96–97, 
120–121, 123, 153, 244, 264, 266
switch statement 10
synchronous communications 191
system leaks 100
T
tables 191
tautology tests 82
TDD (test-driven development) 36, 43
tell-don’t-ask principle 104
test code 8
test coverage 9
Test Data Builder 248
test data life cycle 243–246
avoiding in-memory databases 246
clearing data between test runs 244–245
parallel vs. sequential test execution
243–244
test doubles 22–23, 25, 28, 93–94, 98, 199
test fixtures 248
defined 50
reusing between tests
constructors 52
high coupling 52
private factory methods 52–54
reusing between tests 50–54
test fragility, mocks and 106–114
defining hexagonal architecture 106–110
intra-system vs. inter-system 
communications 110–114
test isolation 115
Test Pyramid
general discussion 87–89
integration testing 187
test suites
characteristics of successful suites 15–17
integration into development cycle 16
maximum value with minimum maintenance 
costs 17
targeting most important parts of code 
base 16–17
coverage metrics, measuring test suite quality 
with 8–15
aiming for particular coverage number 15
branch coverage metric 10–11
code coverage metric 9–10
problems with 12–15
third-party applications 81, 112
tight coupling 5
time 271–273
as ambient context 271–272
as explicit dependency 272–273
trivial code 153–154
trivial tests 82–83
true negative 76
true positive 76
two-line act section 46
U
UI (user interface) tests 38
unit of behavior 56, 225
unit of work 239, 242
unit testing
anatomy of 41–63
AAA pattern 42–49
assertion libraries, using to improve test 
readability 62–63
naming tests 54–58
refactoring to parameterized tests 58–62
reusing test fixtures between tests 50–54
xUnit testing framework 49–50
automation concepts 87–90
black-box vs. white-box testing 89–90
Test Pyramid 87–89
characteristics of successful test suites 15–17
integration into development cycle 16
maximum value with minimum maintenance 
costs 17
targeting most important parts of code 
base 16–17
classical school of 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 27–30
precise bug location 36
testing large graph of interconnected 
classes 35
testing one class at a time 34–35
coverage metrics, measuring test suite quality 
with 8–15
aiming for particular coverage number 15
branch coverage metric 10–11
code coverage metric 9–10
problems with 12–15
current state of 4–5
defined 21–30
four pillars of 68–80
feedback speed 79–80
maintainability 79–80
protection against regressions 68–69
resistance to refactoring 69–71


---
**Page 282**

INDEX
282
unit testing (continued)
functional architecture 128–134
defined 132–133
drawbacks of 146–149
functional programming 128–131
hexagonal architecture 133–134
transitioning to output-based testing
135–146
goal of 5–8
good vs. bad tests 7–8
ideal tests 80–87
brittle tests 83–84
end-to-end tests 81
possibility of creating 81
trivial tests 82–83
London school of 30–37
dependencies 30–34
end-to-end tests 38–39
integration tests 37–39
isolation issue 21–27
precise bug location 36
testing large graph of interconnected 
classes 35
testing one class at a time 34–35
styles of 120–123
communication-based testing
122–123
comparing 123–128
output-based testing 120–121
state-based testing 121–122
units of behavior 34
units of code 21, 27–29, 34, 47, 225
unmanaged dependencies 190, 199, 211, 216, 
218, 220, 222, 226, 254
user controller 193
user interface (UI) tests 38
V
value objects 31, 126–127
void type 97
volatile dependencies 29
W
white-box testing 89–90
write operation 252
X
xUnit testing framework 49–50
Y
YAGNI (You aren’t gonna need it) principle
198–199


---
**Page Back cover**

Vladimir Khorikov
G
reat testing practices will help maximize your project 
quality and delivery speed. Wrong tests will break your 
code, multiply bugs, and increase time and costs. You 
owe it to yourself—and your projects—to learn how to do 
excellent unit testing to increase your productivity and the 
end-to-end quality of your software.
Unit Testing: Principles, Practices, and Patterns teaches you to 
design and write tests that target the domain model and 
other key areas of your code base. In this clearly written 
guide, you learn to develop professional-quality test suites, 
safely automate your testing process, and integrate testing 
throughout the application life cycle. As you adopt a testing 
mindset, you’ll be amazed at how better tests cause you to 
write better code. 
What’s Inside
● Universal guidelines to assess any unit test
● Testing to identify and avoid anti-patterns
● Refactoring tests along with the production code
● Using integration tests to verify the whole system
For readers who know the basics of unit testing. The C# 
examples apply to any language.
Vladimir Khorikov is an author, blogger, and Microsoft MVP. 
He has mentored numerous teams on the ins and outs of 
unit testing.
To download their free eBook in PDF, ePub, and Kindle formats, owners 
of this book should visit www.manning.com/books/unit-testing
$49.99 / Can $65.99  [INCLUDING eBOOK]
Unit Testing Principles, Practices, and Patterns
TESTING/SOFTWARE DEVELOPMENT
M A N N I N G
“
This book is an
 indispensable resource.”
 
—Greg Wright
Kainos Software Ltd.
“
Serves as a valuable and 
humbling encouragement 
to double down and test 
well, something we need 
no matter how experienced 
  we may be.”
 
—Mark Nenadov, BorderConnect
“
I wish I had this book 
twenty years ago when I was 
starting my career in 
  software development.”
—Conor Redmond
Incomm Product Control 
“
This is the kind of book 
on unit testing I have been 
 waiting on for a long time.”
 
—Jeremy Lange, G2
See first page
ISBN-13: 978-1-61729-627-7
ISBN-10: 1-61729-627-9



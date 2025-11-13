# 11.5 Mocking concrete classes (pp.268-271)

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



# 11.6.1 Time as an ambient context (pp.271-272)

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



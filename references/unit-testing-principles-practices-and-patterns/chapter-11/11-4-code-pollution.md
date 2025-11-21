# 11.4 Code pollution (pp.266-268)

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



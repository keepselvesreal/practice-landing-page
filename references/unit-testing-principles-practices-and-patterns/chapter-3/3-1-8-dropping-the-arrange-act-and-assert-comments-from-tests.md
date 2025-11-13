# 3.1.8 Dropping the arrange, act, and assert comments from tests (pp.48-49)

---
**Page 48**

48
CHAPTER 3
The anatomy of a unit test
public class CalculatorTests
{
[Fact]
public void Sum_of_two_numbers()
{
// Arrange
double first = 10;
double second = 20;
var sut = new Calculator();    
// Act
double result = sut.Sum(first, second);
// Assert
Assert.Equal(30, result);
}
}
3.1.8
Dropping the arrange, act, and assert comments from tests
Just as it’s important to set the SUT apart from its dependencies, it’s also important to
differentiate the three sections from each other, so that you don’t spend too much
time figuring out what section a particular line in the test belongs to. One way to do
that is to put // Arrange, // Act, and // Assert comments before the beginning of
each section. Another way is to separate the sections with empty lines, as shown next.
public class CalculatorTests
{
[Fact]
public void Sum_of_two_numbers()
{
double first = 10;
   
double second = 20;
  
var sut = new Calculator();  
double result = sut.Sum(first, second);   
Assert.Equal(30, result);   
}
}
Separating sections with empty lines works great in most unit tests. It allows you to
keep a balance between brevity and readability. It doesn’t work as well in large tests,
though, where you may want to put additional empty lines inside the arrange section
to differentiate between configuration stages. This is often the case in integration
tests—they frequently contain complicated setup logic. Therefore,
Listing 3.4
Differentiating the SUT from its dependencies
Listing 3.5
Calculator with sections separated by empty lines
The calculator is 
now called sut. 
Arrange
Act
Assert


---
**Page 49**

49
Exploring the xUnit testing framework
Drop the section comments in tests that follow the AAA pattern and where you
can avoid additional empty lines inside the arrange and assert sections.
Keep the section comments otherwise. 
3.2
Exploring the xUnit testing framework
In this section, I give a brief overview of unit testing tools available in .NET, and
their features. I’m using xUnit (https://github.com/xunit/xunit) as the unit testing
framework (note that you need to install the xunit.runner.visualstudio NuGet
package in order to run xUnit tests from Visual Studio). Although this framework
works in .NET only, every object-oriented language (Java, C++, JavaScript, and so
on) has unit testing frameworks, and all those frameworks look quite similar to each
other. If you’ve worked with one of them, you won’t have any issues working with
another.
 In .NET alone, there are several alternatives to choose from, such as NUnit
(https://github.com/nunit/nunit) and the built-in Microsoft MSTest. I personally
prefer xUnit for the reasons I’ll describe shortly, but you can also use NUnit; these two
frameworks are pretty much on par in terms of functionality. I don’t recommend
MSTest, though; it doesn’t provide the same level of flexibility as xUnit and NUnit.
And don’t take my word for it—even people inside Microsoft refrain from using
MSTest. For example, the ASP.NET Core team uses xUnit.
 I prefer xUnit because it’s a cleaner, more concise version of NUnit. For example,
you may have noticed that in the tests I’ve brought up so far, there are no framework-
related attributes other than [Fact], which marks the method as a unit test so the unit
testing framework knows to run it. There are no [TestFixture] attributes; any public
class can contain a unit test. There’s also no [SetUp] or [TearDown]. If you need to
share configuration logic between tests, you can put it inside the constructor. And if
you need to clean something up, you can implement the IDisposable interface, as
shown in this listing.
public class CalculatorTests : IDisposable
{
private readonly Calculator _sut;
public CalculatorTests()
   
{
   
_sut = new Calculator();   
}
   
[Fact]
public void Sum_of_two_numbers()
{
/* ... */
}
Listing 3.6
Arrangement and teardown logic, shared by all tests
Called before 
each test in 
the class



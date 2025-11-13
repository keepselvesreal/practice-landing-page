# 3.2 Exploring the xUnit testing framework (pp.49-50)

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


---
**Page 50**

50
CHAPTER 3
The anatomy of a unit test
public void Dispose()   
{
   
_sut.CleanUp();
   
}
   
}
As you can see, the xUnit authors took significant steps toward simplifying the
framework. A lot of notions that previously required additional configuration (like
[TestFixture] or [SetUp] attributes) now rely on conventions or built-in language
constructs.
 I particularly like the [Fact] attribute, specifically because it’s called Fact and not
Test. It emphasizes the rule of thumb I mentioned in the previous chapter: each test
should tell a story. This story is an individual, atomic scenario or fact about the problem
domain, and the passing test is a proof that this scenario or fact holds true. If the test
fails, it means either the story is no longer valid and you need to rewrite it, or the sys-
tem itself has to be fixed.
 I encourage you to adopt this way of thinking when you write unit tests. Your tests
shouldn’t be a dull enumeration of what the production code does. Rather, they should
provide a higher-level description of the application’s behavior. Ideally, this description
should be meaningful not just to programmers but also to business people. 
3.3
Reusing test fixtures between tests
It’s important to know how and when to reuse code between tests. Reusing code
between arrange sections is a good way to shorten and simplify your tests, and this sec-
tion shows how to do that properly.
 I mentioned earlier that often, fixture arrangements take up too much space. It
makes sense to extract these arrangements into separate methods or classes that you
then reuse between tests. There are two ways you can perform such reuse, but only
one of them is beneficial; the other leads to increased maintenance costs.
Test fixture
The term test fixture has two common meanings:
1
A test fixture is an object the test runs against. This object can be a regular
dependency—an argument that is passed to the SUT. It can also be data in
the database or a file on the hard disk. Such an object needs to remain in a
known, fixed state before each test run, so it produces the same result.
Hence the word fixture.
2
The other definition comes from the NUnit testing framework. In NUnit, Test-
Fixture is an attribute that marks a class containing tests.
I use the first definition throughout this book.
Called after 
each test in 
the class



# 3.1.7 Differentiating the system under test (pp.47-48)

---
**Page 47**

47
How to structure a unit test
Purchase method and not rely on the client code to do so. When it comes to main-
taining invariants, you should eliminate any potential course of action that could lead
to an invariant violation.
 This guideline of keeping the act section down to a single line holds true for the
vast majority of code that contains business logic, but less so for utility or infrastruc-
ture code. Thus, I won’t say “never do it.” Be sure to examine each such case for a
potential breach in encapsulation, though. 
3.1.5
How many assertions should the assert section hold?
Finally, there’s the assert section. You may have heard about the guideline of having
one assertion per test. It takes root in the premise discussed in the previous chapter:
the premise of targeting the smallest piece of code possible.
 As you already know, this premise is incorrect. A unit in unit testing is a unit of
behavior, not a unit of code. A single unit of behavior can exhibit multiple outcomes,
and it’s fine to evaluate them all in one test.
 Having that said, you need to watch out for assertion sections that grow too large:
it could be a sign of a missing abstraction in the production code. For example,
instead of asserting all properties inside an object returned by the SUT, it may be bet-
ter to define proper equality members in the object’s class. You can then compare the
object to an expected value using a single assertion. 
3.1.6
What about the teardown phase?
Some people also distinguish a fourth section, teardown, which comes after arrange, act,
and assert. For example, you can use this section to remove any files created by the
test, close a database connection, and so on. The teardown is usually represented by a
separate method, which is reused across all tests in the class. Thus, I don’t include this
phase in the AAA pattern.
 Note that most unit tests don’t need teardown. Unit tests don’t talk to out-of-process
dependencies and thus don’t leave side effects that need to be disposed of. That’s a
realm of integration testing. We’ll talk more about how to properly clean up after inte-
gration tests in part 3. 
3.1.7
Differentiating the system under test
The SUT plays a significant role in tests. It provides an entry point for the behavior
you want to invoke in the application. As we discussed in the previous chapter, this
behavior can span across as many as several classes or as little as a single method. But
there can be only one entry point: one class that triggers that behavior.
 Thus it’s important to differentiate the SUT from its dependencies, especially
when there are quite a few of them, so that you don’t need to spend too much time
figuring out who is who in the test. To do that, always name the SUT in tests sut. The
following listing shows how CalculatorTests would look after renaming the Calcu-
lator instance.


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



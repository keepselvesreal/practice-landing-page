# 3.1.1 Using the AAA pattern (pp.42-43)

---
**Page 42**

42
CHAPTER 3
The anatomy of a unit test
and .NET; most unit testing frameworks exhibit similar functionality, regardless of
the programming language. If you learn one of them, you won’t have problems work-
ing with another.
3.1
How to structure a unit test
This section shows how to structure unit tests using the arrange, act, and assert pat-
tern, what pitfalls to avoid, and how to make your tests as readable as possible.
3.1.1
Using the AAA pattern
The AAA pattern advocates for splitting each test into three parts: arrange, act, and
assert. (This pattern is sometimes also called the 3A pattern.) Let’s take a Calculator
class with a single method that calculates a sum of two numbers:
public class Calculator
{
public double Sum(double first, double second)
{
return first + second;
}
}
The following listing shows a test that verifies the class’s behavior. This test follows the
AAA pattern.
public class CalculatorTests         
{
[Fact]    
public void Sum_of_two_numbers()   
{
// Arrange
double first = 10;
   
double second = 20;
   
var calculator = new Calculator();  
// Act
double result = calculator.Sum(first, second);    
// Assert
Assert.Equal(30, result);   
}
}
The AAA pattern provides a simple, uniform structure for all tests in the suite. This
uniformity is one of the biggest advantages of this pattern: once you get used to it, you
can easily read and understand any test. That, in turn, reduces maintenance costs for
your entire test suite. The structure is as follows:
Listing 3.1
A test covering the Sum method in calculator
Class-container for a 
cohesive set of tests
xUnit’s attribute 
indicating a test
Name of the
unit test
Arrange 
section
Act section
Assert section


---
**Page 43**

43
How to structure a unit test
In the arrange section, you bring the system under test (SUT) and its dependen-
cies to a desired state.
In the act section, you call methods on the SUT, pass the prepared dependen-
cies, and capture the output value (if any).
In the assert section, you verify the outcome. The outcome may be represented
by the return value, the final state of the SUT and its collaborators, or the meth-
ods the SUT called on those collaborators.
The natural inclination is to start writing a test with the arrange section. After all, it
comes before the other two. This approach works well in the vast majority of cases, but
starting with the assert section is a viable option too. When you practice Test-Driven
Development (TDD)—that is, when you create a failing test before developing a
feature—you don’t know enough about the feature’s behavior yet. So, it becomes
advantageous to first outline what you expect from the behavior and then figure out
how to develop the system to meet this expectation.
 Such a technique may look counterintuitive, but it’s how we approach problem
solving. We start by thinking about the objective: what a particular behavior should to
do for us. The actual solving of the problem comes after that. Writing down the asser-
tions before everything else is merely a formalization of this thinking process. But
again, this guideline is only applicable when you follow TDD—when you write a test
before the production code. If you write the production code before the test, by the
time you move on to the test, you already know what to expect from the behavior, so
starting with the arrange section is a better option. 
3.1.2
Avoid multiple arrange, act, and assert sections
Occasionally, you may encounter a test with multiple arrange, act, or assert sections. It
usually works as shown in figure 3.1.
 When you see multiple act sections separated by assert and, possibly, arrange sec-
tions, it means the test verifies multiple units of behavior. And, as we discussed in
chapter 2, such a test is no longer a unit test but rather is an integration test. It’s best
Given-When-Then pattern
You might have heard of the Given-When-Then pattern, which is similar to AAA. This
pattern also advocates for breaking the test down into three parts:
Given—Corresponds to the arrange section
When—Corresponds to the act section
Then—Corresponds to the assert section
There’s no difference between the two patterns in terms of the test composition. The
only distinction is that the Given-When-Then structure is more readable to non-
programmers. Thus, Given-When-Then is more suitable for tests that are shared with
non-technical people.



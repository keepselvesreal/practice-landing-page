# 3.0 Introduction [auto-generated] (pp.41-42)

---
**Page 41**

41
The anatomy of
a unit test
In this remaining chapter of part 1, I’ll give you a refresher on some basic topics.
I’ll go over the structure of a typical unit test, which is usually represented by the
arrange, act, and assert (AAA) pattern. I’ll also show the unit testing framework of
my choice—xUnit—and explain why I’m using it and not one of its competitors.
 Along the way, we’ll talk about naming unit tests. There are quite a few compet-
ing pieces of advice on this topic, and unfortunately, most of them don’t do a good
enough job improving your unit tests. In this chapter, I describe those less-useful
naming practices and show why they usually aren’t the best choice. Instead of those
practices, I give you an alternative—a simple, easy-to-follow guideline for naming
tests in a way that makes them readable not only to the programmer who wrote
them, but also to any other person familiar with the problem domain.
 Finally, I’ll talk about some features of the framework that help streamline the
process of unit testing. Don’t worry about this information being too specific to C#
This chapter covers
The structure of a unit test
Unit test naming best practices
Working with parameterized tests
Working with fluent assertions


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



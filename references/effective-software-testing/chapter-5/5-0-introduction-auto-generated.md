# 5.0 Introduction [auto-generated] (pp.117-118)

---
**Page 117**

117
Property-based testing
So far, we have been doing example-based testing. We judiciously divide the input
space of a program (into partitions), pick one concrete example from all the possi-
ble ones, and write the test case. What if we did not have to pick one concrete
example out of many? What if we could express the property we are trying to exercise
and let the test framework choose several concrete examples for us? Our tests
would be less dependent on a concrete example, and the test framework would be
able to call the method under test multiple times with different input parameters—
usually with zero effort from us.
 This is what property-based testing is about. We do not pick a concrete example;
rather, we define a property (or a set of properties) that the program should
adhere to, and the test framework tries to find a counterexample that causes the
program to break with these properties.
 I have learned that the best way to teach how to write property-based tests is with
multiple examples. So, this chapter presents five different examples with varying
levels of complexity. I want you to focus on my way of thinking and notice how
much creativity is required to write such tests.
This chapter covers
Writing property-based tests
Understanding when to write property-based tests 
or example-based tests


---
**Page 118**

118
CHAPTER 5
Property-based testing
5.1
Example 1: The passing grade program
Consider the following requirement, inspired by a similar problem in Kaner et al.’s
book (2013):
A student passes an exam if they get a grade >= 5.0. Grades below that are a
fail. Grades fall in the range [1.0, 10.0].
A simple implementation for this program is shown in the following listing.
public class PassingGrade {
  public boolean passed(float grade) {
    if (grade < 1.0 || grade > 10.0) 
      throw new IllegalArgumentException();
    return grade >= 5.0;
  }
}
If we were to apply specification-based testing to this program, we would probably
devise partitions such as “passing grade,” “failing grade,” and “grades outside the
range.” We would then devise a single test case per partition. With property-based test-
ing, we want to formulate properties that the program should have. I see the following
properties for this requirement:

fail—For all numbers ranging from 1.0 (inclusive) to 5.0 (exclusive), the pro-
gram should return false.

pass—For all numbers ranging from 5.0 (inclusive) to 10.0 (inclusive), the pro-
gram should return true.

invalid—For all invalid grades (which we define as any number below 1.0 or
greater than 10.0), the program must throw an exception.
Can you see the difference between what we do in specification-based testing and
what we aim to do in property-based testing? Let’s write a suite test by test, starting
with the fail property. For that, we will use jqwik (https://jqwik.net), a popular prop-
erty-based testing framework for Java.
NOTE
Property-based testing frameworks are available in many different lan-
guages, although their APIs vary significantly (unlike unit testing frameworks
like JUnit, which all look similar). If you are applying this knowledge to
another language, your task is to study the framework that is available in your
programming language. The way to think and reason is the same across dif-
ferent languages.
Before I show the concrete implementation, let me break down property-based testing
step by step, using jqwik’s lingo:
Listing 5.1
Implementation of the PassingGrade program
Note the pre-condition 
check here.



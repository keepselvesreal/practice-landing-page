# 1.4 Exit point types (pp.11-12)

---
**Page 11**

11
1.4
Exit point types
1.4
Exit point types
We’ve seen that we have three different types of end results:
The invoked function returns a useful value (not undefined). If this was in a stati-
cally typed language such as Java or C#, we’d say it is a public, non-void function.
There’s a noticeable change to the state or behavior of the system before and
after invocation that can be determined without interrogating private state.
There’s a callout to a third-party system over which the test has no control. That
third-party system doesn’t return any value, or that value is ignored. (Example:
the code calls a third-party logging system that was not written by you, and you
don’t control its source code.)
Let’s see how the idea of entry and exit points affects the definition of a unit test: A
unit test is a piece of code that invokes a unit of work and checks one specific exit point
as an end result of that unit of work. If the assumptions about the end result turn out
to be wrong, the unit test has failed. A unit test’s scope can span as little as a function
or as much as multiple modules or components, depending on how many functions
and modules are used between the entry point and the exit point. 
XUnit Test Patterns’ definition of entry and exit points
Gerard Meszaros’ book XUnit Test Patterns (Addison-Wesley Professional, 2007) dis-
cusses the notion of direct inputs and outputs, and indirect inputs and outputs. Direct
inputs are what I like to call entry points. Meszaros refers to it as “using the front
door” of a component. Indirect outputs in that book are the other two types of exit
points I mentioned (state change and calling a third party). 
Both versions of these ideas have evolved in parallel, but the idea of a “unit of work”
only appears in this book. A unit of work, coupled with entry and exit points, makes
much more sense to me than direct and indirect inputs and outputs, but you can con-
sider this a stylistic choice about how to teach the concept of test scopes. You can
find more about XUnit Test Patterns at xunitpatterns.com. 
sum(numbers)
Return value
Unit
of
work
Call third-party
logger
State change
totalSoFar()
Figure 1.5
Showing three exit 
points from a function


---
**Page 12**

12
CHAPTER 1
The basics of unit testing
1.5
Different exit points, different techniques
Why am I spending so much time talking about types of exit points? Because not only
is it a great idea to separate the tests for each exit point, but different types of exit
points might require different techniques to test successfully:
Return-value-based exit points (direct outputs in Meszaros’ XUnit Test Patterns)
should be the easiest exit points to test. You trigger an entry point, you get
something back, and you check the value you got back.
State-based tests (indirect outputs) usually require a little more gymnastics. You
call something, and then you do another call to check something else (or you
call the previous thing again) to see if everything went according to plan. 
In a third-party situation (indirect outputs), we have the most hoops to jump through.
We haven’t discussed this yet, but that’s where we’re forced to use things like mock
objects to replace the external system with something we can control and interrogate in
our tests. I’ll cover this idea deeply later in the book. 
1.6
A test from scratch
Let’s go back to the first, simplest version of the
code (listing 1.1) and try to test it, shall we? If we
were to try to write a test for this, what would it
look like? 
 Let’s take the visual approach first with figure 1.6.
Our entry point is sum with an input of a string called
numbers. sum is also our exit point, since we will get a
return value back from it and check its value.
 It’s possible to write an automated unit test
without using a test framework. In fact, because
developers have gotten more into the habit of
automating their testing, I’ve seen plenty of them
doing this before discovering test frameworks. In
this section, we’ll write such a test without a frame-
work, so that you can contrast this approach with
using a framework in chapter 2.
Which exit points make the most problems?
As a rule of thumb, I try to mostly use either return-value-based or state-based tests. I
try to avoid mock-object-based tests if I can, and usually I can. As a result, I usually
have no more than 5% of my tests using mock objects for verification. Those types of
tests complicate things and make maintainability more difficult. Sometimes there’s no
escape, though, and we’ll discuss them as we proceed in the next chapters.
sum(numbers)
Return value
Unit
of
work
Test
Figure 1.6
A visual view of our test



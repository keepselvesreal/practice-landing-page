# 1.5 Different exit points, different techniques (pp.12-12)

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



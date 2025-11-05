# 2.0 Introduction [auto-generated] (pp.20-21)

---
**Page 20**

20
What is a unit test?
As mentioned in chapter 1, there are a surprising number of nuances in the defini-
tion of a unit test. Those nuances are more important than you might think—so
much so that the differences in interpreting them have led to two distinct views on
how to approach unit testing.
 These views are known as the classical and the London schools of unit testing.
The classical school is called “classical” because it’s how everyone originally
approached unit testing and test-driven development. The London school takes
root in the programming community in London. The discussion in this chapter
about the differences between the classical and London styles lays the foundation
for chapter 5, where I cover the topic of mocks and test fragility in detail.
This chapter covers
What a unit test is
The differences between shared, private, 
and volatile dependencies
The two schools of unit testing: classical 
and London
The differences between unit, integration, 
and end-to-end tests


---
**Page 21**

21
The definition of “unit test”
 Let’s start by defining a unit test, with all due caveats and subtleties. This definition
is the key to the difference between the classical and London schools.
2.1
The definition of “unit test”
There are a lot of definitions of a unit test. Stripped of their non-essential bits, the
definitions all have the following three most important attributes. A unit test is an
automated test that
Verifies a small piece of code (also known as a unit),
Does it quickly,
And does it in an isolated manner.
The first two attributes here are pretty non-controversial. There might be some dis-
pute as to what exactly constitutes a fast unit test because it’s a highly subjective mea-
sure. But overall, it’s not that important. If your test suite’s execution time is good
enough for you, it means your tests are quick enough.
 What people have vastly different opinions about is the third attribute. The isola-
tion issue is the root of the differences between the classical and London schools of
unit testing. As you will see in the next section, all other differences between the two
schools flow naturally from this single disagreement on what exactly isolation means. I
prefer the classical style for the reasons I describe in section 2.3.
2.1.1
The isolation issue: The London take
What does it mean to verify a piece of code—a unit—in an isolated manner? The Lon-
don school describes it as isolating the system under test from its collaborators. It
means if a class has a dependency on another class, or several classes, you need to
replace all such dependencies with test doubles. This way, you can focus on the class
under test exclusively by separating its behavior from any external influence.
 
The classical and London schools of unit testing
The classical approach is also referred to as the Detroit and, sometimes, the classi-
cist approach to unit testing. Probably the most canonical book on the classical
school is the one by Kent Beck: Test-Driven Development: By Example (Addison-Wesley
Professional, 2002).
The London style is sometimes referred to as mockist. Although the term mockist is
widespread, people who adhere to this style of unit testing generally don’t like it, so
I call it the London style throughout this book. The most prominent proponents of this
approach are Steve Freeman and Nat Pryce. I recommend their book, Growing Object-
Oriented Software, Guided by Tests (Addison-Wesley Professional, 2009), as a good
source on this subject.



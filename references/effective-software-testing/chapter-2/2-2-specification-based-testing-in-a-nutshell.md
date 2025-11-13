# 2.2 Specification-based testing in a nutshell (pp.45-46)

---
**Page 45**

45
Specification-based testing in a nutshell
2.2
Specification-based testing in a nutshell
I propose a seven-step approach to derive systematic tests based on a specification.
This approach is a mix of the category-partition method proposed by Ostrand and Balcer
in their seminal 1988 work, and Kaner et al.’s Domain Testing Workbook (2013), with my
own twist: see figure 2.4.
The steps are as follows:
1
Understand the requirement, inputs, and outputs. We need an overall idea of what
we are about to test. Read the requirements carefully. What should the program
do? What should it not do? Does it handle specific corner cases? Identify the
input and output variables in play, their types (integers, strings, and so on),
and their input domain (for example, is the variable a number that must be
between 5 and 10?). Some of these characteristics can be found in the pro-
gram’s specification; others may not be stated explicitly. Try to understand the
nitty-gritty details of the requirements.
2
Explore the program. If you did not write the program yourself, a very good way to
determine what it does (besides reading the documentation) is to play with it.
Call the program under test with different inputs and see what it produces as
output. Continue until you are sure your mental model matches what the pro-
gram does. This exploration does not have to be (and should not be) system-
atic. Rather, focus on increasing your understanding. Remember that you are
still not testing the program.
3
Judiciously explore the possible inputs and outputs, and identify the partitions. Identify-
ing the correct partitions is the hardest part of testing. If you miss one, you may
let a bug slip through. I propose three steps to identify the partitions:
a
Look at each input variable individually. Explore its type (is it an integer? is it
a string?) and the range of values it can receive (can it be null? is it a number
ranging from 0 to 100? does it allow negative numbers?).
b
Look at how each variable may interact with another. Variables often have
dependencies or put constraints on each other, and those should be tested.
Understand the
requirement.
Explore the
program.
Identify the
partitions.
Analyze the
boundaries.
Devise test
cases.
Automate test
cases.
Augment
(creativity and
experience).
Figure 2.4
The seven steps I propose to derive test cases based on specifications. The solid 
arrows indicate the standard path to follow. The dashed arrows indicate that, as always, the 
process should be iterative, so in practice you’ll go back and forth until you are confident about the 
test suite you’ve created.


---
**Page 46**

46
CHAPTER 2
Specification-based testing
c
Explore the possible types of outputs, and make sure you are testing them
all. While exploring the inputs and outputs, pay attention to any implicit
(business) rules, logic, or expected behavior.
4
Identify the boundaries. Bugs love boundaries, so be extra thorough here. Analyze
the boundaries of all the partitions you devised in the previous step. Identify
the relevant ones, and add them to the list.
5
Devise test cases based on the partitions and boundaries. The basic idea is to combine
all the partitions in the different categories to test all possible combinations of
inputs. However, combining them all may be too expensive, so part of the task is
to reduce the number of combinations. The common strategy is to test excep-
tional behavior only once and not combine it with the other partitions.
6
Automate the test cases. A test is only a test when it is automated. Therefore, the
goal is to write (JUnit) automated tests for all the test cases you just devised.
This means identifying concrete input values for them and having a clear
expectation of what the program should do (the output). Remember that test
code is code, so reduce duplication and ensure that the code is easy to read and
that the different test cases are easily identifiable in case one fails.
7
Augment the test suite with creativity and experience. Perform some final checks.
Revisit all the tests you created, using your experience and creativity. Did you
miss something? Does your gut feeling tell you that the program may fail in a
specific case? If so, add a new test case. 
2.3
Finding bugs with specification testing
The developers of the Apache Commons Lang framework (the framework where I
extracted the implementation of the substringsBetween method) are just too good.
We did not find any bugs there. Let’s look at another example: one implemented by
me, an average developer who makes mistakes from time to time. This example will
show you the value of specification testing. Try to spot the bug before I reveal it!
 Some friends and I have participated in many coding challenges, primarily for fun.
A couple of years ago we worked on the following problem inspired by LeetCode
(https://leetcode.com/problems/add-two-numbers):
The method receives two numbers, left and right (each represented as a list
of digits), adds them, and returns the result as a list of digits.
Each element in the left and right lists of digits should be a number from
[0–9]. An IllegalArgumentException is thrown if this pre-condition does
not hold.

left—A list containing the left number. Null returns null; empty means 0.

right—A list containing the right number. Null returns null; empty
means 0.
The program returns the sum of left and right as a list of digits.



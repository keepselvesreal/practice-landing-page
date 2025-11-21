# 2.6 Summary (pp.61-63)

---
**Page 61**

61
Summary
D
[A, B]: invalid
E
[C, M]: valid
F
[N, Z]: invalid
Based on what you as a tester assume about the program, what other corner or
boundary cases can you come up with? Describe these invalid cases and how
they may exercise the program based on your assumptions.
2.4
A program called FizzBuzz does the following: given an integer n, return the
string formed from the number followed by “!”. If the number is divisible by 3,
use “Fizz” instead of the number; and if the number is divisible by 5, use “Buzz”
instead of the number, and if the number is divisible by both 3 and 5, use “Fizz-
Buzz” instead of the number.
Examples:
A The integer 3 yields “Fizz!”
B The integer 4 yields “4!”
C The integer 5 yields “Buzz!”
D The integer 15 yields “FizzBuzz!”
A novice tester is trying to devise as many tests as possible for the FizzBuzz
method and comes up with the following:
A T1 = 15
B T2 = 30
C T3 = 8
D T4 = 6
E T5 = 25
Which of these tests can be removed while maintaining a good test suite? Which
concept can we use to determine the test(s) that can be removed?
2.5
A game has the following condition: numberOfPoints <= 570. Perform bound-
ary analysis on the condition. What are the on and off points?
A On point = 570, off point = 571
B On point = 571, off point = 570
C On point = 570, off point = 569
D On point = 569, off point = 570
2.6
Perform boundary analysis on the following equality: x == 10. What are the on
and off points?
Summary
Requirements are the most important artifact we can use to generate tests.
Specification-based testing techniques help us explore the requirements in a
systematic way. For example, they help us examine the domain space of the dif-
ferent input variables and how they interact with each other.


---
**Page 62**

62
CHAPTER 2
Specification-based testing
I propose a seven-step approach for specification testing: (1) understand the
requirements, (2) explore the program if you do not know much about it, (3)
judiciously analyze the properties of the inputs and outputs and identify the
partitions, (4) analyze the boundaries, (5) devise concrete test cases, (6) imple-
ment the concrete test cases as automated (JUnit) tests, and (7) use creativity
and experience to augment the test suite.
Bugs love boundaries. However, identifying the boundaries may be the most
challenging part of specification testing.
The number of test cases may be too large, even in simpler programs. This
means you must decide what should be tested and what should not be tested.


---
**Page 63**

63
Structural testing
and code coverage
In the previous chapter, we discussed using software requirements as the main
element to guide the testing. Once specification-based testing is done, the next
step is to augment the test suite with the help of the source code. There are several rea-
sons to do so.
 First, you may have forgotten a partition or two when analyzing the require-
ments, and you may notice that while looking at the source code. Second, when
implementing code, you take advantage of language constructs, algorithms, and
data structures that are not explicit in the documentation. Implementation-specific
details should also be exercised to increase the likelihood of ensuring the pro-
gram’s full correctness.
This chapter covers
Creating test cases based on the code structure
Combining structural testing and specification-
based testing
Using code coverage properly
Why some developers (wrongly) dislike code 
coverage



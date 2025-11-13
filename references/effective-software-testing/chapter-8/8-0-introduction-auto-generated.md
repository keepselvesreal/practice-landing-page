# 8.0 Introduction [auto-generated] (pp.198-199)

---
**Page 198**

198
Test-driven development
Software developers are pretty used to the traditional development process. First,
they implement. Then, and only then, they test. But why not do it the other way
around? In other words, why not write a test first and then implement the produc-
tion code?
 In this chapter, we discuss this well-known approach: test-driven development (TDD).
In a nutshell, TDD challenges our traditional way of coding, which has always been
“write some code and then test it.” With TDD, we start by writing a test representing
the next small feature we want to implement. This test naturally fails, as the feature
has not yet been implemented! We then make the test pass by writing some code.
With the test now green, and knowing that the feature has been implemented, we
go back to the code we wrote and refactor it.
 TDD is a popular practice, especially among Agile practitioners. Before I dive
into the advantages of TDD and pragmatic questions about working this way, let’s
look at a small example.
This chapter covers
Understanding test-driven development
Being productive with TDD
When not to use TDD


---
**Page 199**

199
Our first TDD session
8.1
Our first TDD session
For this example, we will create a program that converts Roman numerals to integers.
Roman numerals represent numbers with seven symbols:
I, unus, 1, (one)
V, quinque, 5 (five)
X, decem, 10 (ten)
L, quinquaginta, 50 (fifty)
C, centum, 100 (one hundred)
D, quingenti, 500 (five hundred)
M, mille, 1,000 (one thousand)
To represent all possible numbers, the Romans combined the symbols, following
these two rules:
Digits of lower or equal value on the right are added to the higher-value digit.
Digits of lower value on the left are subtracted from the higher-value digit.
For instance, the number XV represents 15 (10 + 5), and the number XXIV rep-
resents 24 (10 + 10 – 1 + 5).
 The goal of our TDD session is to implement the following requirement:
Implement a program that receives a Roman numeral (as a string) and
returns its representation in the Arabic numeral system (as an integer).
Coming up with examples is part of TDD. So, think about different inputs you can
give the program, and their expected outputs. For example, if we input "I" to the
program, we expect it to return 1. If we input "XII" to the program, we expect it to
return 12. Here are the cases I can think of:
Simple cases, such as numbers with single characters:
– If we input "I", the program must return 1.
– If we input "V", the program must return 5.
– If we input "X", the program must return 10.
Numbers composed of more than one character (without using the subtrac-
tive notation):
– If we input "II", the program must return 2.
– If we input "III", the program must return 3.
– If we input "VI", the program must return 6.
– If we input "XVII", the program must return 17.
Numbers that use simple subtractive notation:
– If we input "IV", the program must return 4.
– If we input "IX", the program must return 9.



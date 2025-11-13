# 3.4.1 An abstract example (pp.72-73)

---
**Page 72**

72
CHAPTER 3
Structural testing and code coverage
3.4
Complex conditions and the MC/DC coverage criterion
Devising test suites that maximize the number of bugs they can identify while minimiz-
ing the effort/cost of building the test suite is part of any tester’s job. The question is,
what can we do about complex, lengthy if statements? Modified condition/decision
coverage (MC/DC) is a good answer.
 The MC/DC criterion looks at combinations of conditions, as path coverage does.
However, instead of testing all possible combinations, we identify the important combi-
nations that need to be tested. MC/DC exercises each of these conditions so that it
can, independently of the other conditions, affect the outcome of the entire decision.
Every possible condition of each parameter must influence the outcome at least once.
(For details, read Kelly Hayhurst’s 2001 paper.)
3.4.1
An abstract example
Let’s take a simple abstract example: if(A && (B || C)), where A, B, and C all evaluate
to booleans. MC/DC dictates the following:
For condition A:
– There must be one test case where A = true (say, T1).
– There must be one test case where A = false (say, T2).
– T1 and T2 (which we call independence pairs) must have different outcomes
(for example, T1 makes the entire decision evaluate to true, and T2 makes
the entire decision evaluate to false).
– Variables B and C in T1 must be equivalent (either both evaluate to true or
both evaluate to false) to B and C in T2. In other words, B and C must have
the same truth values in T1 and T2.
For condition B:
– There must be one test case where B = true (say, T3).
– There must be one test case where B = false (say, T4).
– T3 and T4 must have different outcomes.
– Variables A and C in T3 must be equivalent to A and C in T4.
For condition C:
– There must be one test case where C = true (say, T5).
– There must be one test case where C = false (say, T6).
– T5 and T6 have different outcomes.
– Variables A and B in T5 must be equivalent to A and B in T6.
If conditions have only binary outcomes (that is, true or false), the number of tests
required to achieve 100% MC/DC coverage is N + 1, where N is the number of condi-
tions in the decision (as shown by Chilenski [2001]). Note that N + 1 is smaller than
the total number of possible combinations (2N). So, to devise a test suite that achieves
100% MC/DC, we must create N + 1 test cases that, when combined, exercise all the
combinations independently from the others. 


---
**Page 73**

73
Complex conditions and the MC/DC coverage criterion
3.4.2
Creating a test suite that achieves MC/DC
The question is how to (mechanically) select such test cases. Let’s continue using the
same if statement from the CountWords program (from listing 3.4). The statement
takes three booleans as input: (1) whether the current character is a letter and
whether this letter is (2) “s” or (3) “r”. Generically, this is the same as the A && (B || C)
example we just discussed.
 To test this program, we first use a truth table to see all the combinations and their
outcomes. In this case, we have three decisions, and 23 = 8. Therefore, we have tests T1
to T8, as listed in table 3.1.
Our goal is to apply the MC/DC criterion to these test cases and select N + 1 tests,
which in this case means 3 + 1 = 4. To determine which four tests satisfy MC/DC, we
need to go condition by condition, beginning by selecting the pairs of combinations
(or tests) for the isLetter part of the condition:
For T1, isLetter, last == s, and last == r are all true, and decision (that is,
the outcome of the entire boolean expression) is also true. We now look for
another test in the table where the value of isLetter is the opposite of the
value in T1 but the other values (last == s and last == r) are the same. This
means look for a test where isLetter is false, last == s is true, last == r is
true, and decision is false. This combination appears in T5.
Thus, we have found a pair of tests, T1 and T5 (an independence pair), where
isLetter is the only parameter that is different and the outcome (decision)
changes. In other words, for this pair of tests, isLetter independently influences
the outcome (decision). Let’s keep the pair {T1, T5} in our list of test cases.
We could stop here and move to the next variable. But finding all indepen-
dence pairs for isLetter may help us reduce the final number of test cases, as
you will see. So let’s continue and look at the next test. In T2, isLetter is true,
Table 3.1
Truth table for the if expression from the CountWords program
Test case
isLetter
last == s
last == r
decision
T1
true
true
true
true
T2
true
true
false
true
T3
true
false
true
true
T4
true
false
false
false
T5
false
true
true
false
T6
false
true
false
false
T7
false
false
true
false
T8
false
false
false
false



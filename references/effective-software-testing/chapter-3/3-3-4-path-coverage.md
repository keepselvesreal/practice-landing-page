# 3.3.4 Path coverage (pp.71-72)

---
**Page 71**

71
Code coverage criteria
 In the extended CFG in figure 3.6, branch nodes contain only a single condition.
The complicated if is broken into three nodes. 
3.3.4
Path coverage
A developer aiming for path coverage covers all the possible paths of execution of the
program. While ideally this is the strongest criterion, it is often impossible or too
expensive to achieve. In a single program with three conditions, where each condition
could be independently evaluated to true or false, we would have 23 = 8 paths to
cover. In a program with 10 conditions, the total number of combinations would be
210 = 1024. In other words, we would need to devise more than a thousand tests!
 Path coverage also gets more complicated for programs with loops. In a program
with an unbounded loop, the loop might iterate hundreds of times. A rigorous tester
aiming for path coverage would have to try the program with the loop executing one
time, two times, three times, and so on. 
int         0
words    ;
=
char       ''
last =
;
for int     0
(    i =  ;
i++
words++;
last
t(i);
= str.charA
words++;
return words;
true
true
false
false
i<str.length()
last == 'r'
last       )
== 's'
!isLetter
(str.charAt(i))
last == 's'
last == 'r'
Decision blocks now contain
just a single condition.
true
true
false
false
false
false
true
true
Figure 3.6
The extended control-flow graph of the CountWords program. Each condition 
is in its own node. Covering all the edges in the graph means achieving 100% condition + 
branch coverage.


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



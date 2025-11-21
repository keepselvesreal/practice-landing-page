# 3.3.3 Condition + branch coverage (pp.70-71)

---
**Page 70**

70
CHAPTER 3
Structural testing and code coverage
3.3.3
Condition + branch coverage
Condition + branch coverage considers not only possible branches but also each con-
dition of each branch statement. For example, the first if statement in the Count-
Words program contains three conditions: !Character.isLetter(str.charAt(i)),
last == 's', and last == 'r'. Therefore, a developer aiming for condition + branch
coverage should create a test suite that exercises each of those individual conditions
being evaluated to true and false at least once and the entire branch statement
being true and false at least once.
 Note that blindly looking only at the conditions (and ignoring how they are com-
bined) may result in test suites that do not cover everything. Imagine a simple if(A || B).
A test suite composed of two tests (T1 that makes A true and B false and T2 that
makes A false and B true) covers the two conditions, as each condition is exercised
as true and false. However, the test suite does not fully cover the branch, as in both
tests, the evaluation of the entire if statement is always true. This is why we use condi-
tion + branch coverage, and not only (basic) condition coverage.
 
int         0
words    ;
=
char        ''
last =
;
for int     0
(    i =  ;
i++)
words++;
last
t(i);
= str.charA
words++;
return words;
true
false
false
false
true
true
(last == 'r'
||
==
last
's')
(!isLetter
(str.charAt(i))
&& (l
==
ast
's'
||            ))
last == 'r'
i<str.length()
Rectangles
represent
code blocks
Diamonds represent
decision blocks
Arrows
represent
the flow
Figure 3.5
A control-flow graph of the CountWords program


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



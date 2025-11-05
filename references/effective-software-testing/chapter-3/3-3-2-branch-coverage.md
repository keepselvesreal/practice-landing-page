# 3.3.2 Branch coverage (pp.69-70)

---
**Page 69**

69
Code coverage criteria
 Before I show another running example of structural testing and discuss how to
pragmatically use it in our daily lives, the next section introduces the coverage criteria
we use with this approach. 
3.3
Code coverage criteria
Whenever we identify a line of code that is not covered, we have to decide how thor-
ough (or rigorous) we want to be when covering that line. Let’s revisit an if statement
from the CountWords program.
if (!Character.isLetter(str.charAt(i)) &&
 (last == 's' || last == 'r'))
A developer may decide to only cover the line—in other words, if a test passes through
that if line, the developer will consider it covered. A single test case can do this. A
slightly more thorough developer may cover the if being evaluated to true and
false; doing so requires two test cases. A third developer may explore each condition
in the if statement. This particular if has three conditions requiring at least two tests
each, for a total of six tests. Finally, a very thorough tester may decide to cover every
possible execution path of this statement. Given that it has three different conditions,
doing so requires 2 × 2 × 2 = 8 test cases.
 Let’s formalize this discussion. Note that you’ve already seen some of these terms.
3.3.1
Line coverage
A developer who aims to achieve line coverage wants at least one test case that cov-
ers the line under test. It does not matter if that line contains a complex if statement
full of conditions. If a test touches that line in any way, the developer can count the
line as covered. 
3.3.2
Branch coverage
Branch coverage takes into consideration the fact that branching instructions (ifs,
fors, whiles, and so on) make the program behave in different ways, depending how
the instruction is evaluated. For a simple if(a && b) statement, having a test case T1
that makes the if statement true and another test case T2 that makes the statement
false is enough to consider the branch covered.
 Figure 3.5 illustrates a control-flow graph (CFG) of the CountWords program. You
can see that for each if instruction, two edges come out of the node: one represent-
ing where the flow goes if the statement is evaluated to true and another representing
where the program goes if the statement is evaluated to false. Covering all the edges
in the graph means achieving 100% branch coverage. 
Listing 3.4
An if expression from the CountWords program


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



# 3.2 Structural testing in a nutshell (pp.68-69)

---
**Page 68**

68
CHAPTER 3
Structural testing and code coverage
3.2
Structural testing in a nutshell
Based on what we just did, let me define a simple approach that any developer can fol-
low (see figure 3.4):
1
Perform specification-based testing, as discussed in the previous chapter.
2
Read the implementation, and understand the main coding decisions made by the
developer.
3
Run the devised test suite with a code coverage tool.
4
For each piece of code that is not covered:
a
Understand why that piece of code was not tested. Why didn’t you see this test
case during specification-based testing? Consult with the requirements engi-
neer if you need more clarity.
b
Decide whether the piece of code deserves a test. Testing or not testing that
piece of code is now a conscious decision on your part.
c
If a test is needed, implement an automated test case that covers the missing
piece.
5
Go back to the source code and look for other interesting tests you can devise based on
the code. For each identified piece of the code, perform the substeps of step 4.
The most important thing about this approach is that structural testing complements the
test suite previously devised via specification-based testing. The code coverage tool is an auto-
mated way to identify parts that are not covered.
 Just like the approach I proposed in chapter 2, this one is meant to be iterative and
not to restrain you to a single way of working. It is not uncommon to go back to the
specification and devise additional interesting test cases.
Speciﬁcation-
based testing
(c apter
h
2)
Read the
implementation
Identify the non-
covered parts
Understand why
it is not tested
Should it
be tested?
Write a test
Look for other
interesting cases
7
For all
on-cove
n
red code
Yes
1
2
3-4
4c
4b
4a
5
Figure 3.4
Applying structural testing in a nutshell. Arrows indicate the 
iterative nature of the process. The diamond represents the moment where the 
developer decides whether to write the test case.


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



# 3.10.2 What does it mean to achieve 100% coverage? (pp.86-88)

---
**Page 86**

86
CHAPTER 3
Structural testing and code coverage
 The empirical results also show that coverage alone is not always a strong indica-
tor of how good a test suite is. We also noticed that in the test cases we derived for
the CountWords problem at the beginning of this chapter. We purposefully did bad
specification-based testing and then augmented the test suite with structural testing.
We ended up with three test cases that achieve 100% condition + branch coverage.
But is the test suite strong enough? I don’t think so. I can think of many extra test
cases that would touch the same lines and branches again but would nonetheless
make the test suite much more effective against possible bugs.
 On the other hand, although 100% coverage does not necessarily mean the system
is properly tested, having very low coverage does mean your system is not properly
tested. Having a system with, say, 10% coverage means there is much to be done as far
as testing.
 I suggest reading Google’s code coverage best practices (Arguelles, Ivankovic, and
Bender, 2020). Their perceptions are in line with everything we have discussed here. 
3.10.2 What does it mean to achieve 100% coverage?
I have purposefully skipped talking much about achieving 100% line coverage or
branch coverage or other coverage. I do not believe that achieving a number should
be the goal. Nevertheless, given how prevalent those numbers are in practice, it is
important to understand them. First, let’s talk about the metrics themselves.
NOTE
Formulas vary among the tools on the market. Check your tool’s man-
ual to better understand the precise numbers you get.
If the entire test suite covers all the lines in the program (or in the class or method
under test), that suite achieves 100% line coverage. A simple formula to calculate the
line coverage of a given program or method is to divide the number of lines covered
by the total number of lines:
You can calculate this number at the method level, class level, package level, system
level, or whatever level you are interested in.
 Similar to line coverage, a formula to calculate the achieved branch coverage of a
program or method is the number of branches covered divided by the total number
of branches:
In a simple program such as if(x) { do A } else { do B }, the total number of branches
is two (the single if statement branches the program in two ways). Therefore, if one


---
**Page 87**

87
Structural testing in the real world
test in your test suite covers, say x = true, your test suite achieves 1/2 × 100% = 50%
branch coverage. Note that due to criteria subsumption, which we discussed earlier, if
you cover all the branches of the program, you also cover all the lines.
 Finally, a formula to calculate the condition + branch coverage of a given program or
method is the sum of all branches and conditions covered, divided by the total num-
ber of branches and conditions:
In a simple program such as if(x || y) { do A } else { do B }, the total number of
branches is two (the single if statement branches the program in two ways) and the
total number of conditions is four (two conditions for x and two conditions for y).
Therefore, if you have two tests in your test suite—T1: (true, true) and T2: (false,
true)—the test suite achieves (1 + 3)/(2 + 4) × 100% = 66.6% condition + branch cov-
erage. The test suite covers only one branch of the program (the true branch, as both
T1 and T2 make the if expression evaluate to true), and three of the four conditions
(x is exercised as true and false, but y is only exercised as true).
 Figure 3.10 shows a simple illustration of line coverage, branch coverage, and
condition + branch coverage. When someone says, “My test suite achieves 80% con-
dition + branch coverage,” you now understand that 80% of the branches and con-
ditions are covered by at least one test case. And when someone says, “My test suite
achieves 100% line coverage,” you know that 100% of the lines are covered by at
least one test case. 
if(x)
Do A
Do B
true
false
Suppose a t
T1 mak
ue.
est
es the
tr
if
• Line cover
= 66.6%
age: 2/3
• Branch coverage: 1/2 = 50%
if(x || y)
Do A
Do B
true
false
Imagine a test T1 where
.
x = true
• Line cover
= 66.6%
age: 2/3
• Branch cover
e:
ag
1/2 = 50%
• Branch + c
c
erage: (1 + 2)/(2 + 4) = 50%
ondition ov
Figure 3.10
Two control-flow graphs of simple programs and how the different coverage 
criteria are calculated


---
**Page 88**

88
CHAPTER 3
Structural testing and code coverage
3.10.3 What coverage criterion to use
This is a popular question among practitioners and researchers. If we settle for a
less-rigorous criterion, such as line coverage instead of branch coverage, we might
miss something. Plus this question brings the focus back to the metric, which we do
not want.
 Which criterion to use depends on the context: what you are testing at that
moment and how rigorous you want the testing to be. Structural testing is meant to
complement specification-based testing. When you dive into the source code and look
for uncovered parts, you may decide to use branch coverage for a specific if expres-
sion but MC/DC for another if expression. This makes the approach less systematic
(and, therefore, more prone to errors and different developers using different crite-
ria), but it is the most pragmatic approach I know. You may want to perform some risk
assessment to determine how important it is to be thorough.
 My rule of thumb is branch coverage: I always try to at least reach all the branches
of the program. Whenever I see a more complicated expression, I evaluate the need
for condition + branch coverage. If I see an even more complex expression, I consider
MC/DC. 
3.10.4 MC/DC when expressions are too complex and 
cannot be simplified
MC/DC is increasingly valuable as expressions become more complicated. Listing 3.11
shows an example of a complex expression that I extracted from Chilenski’s 2001
paper. It is an anonymized version of a condition found in a level A flight simulation
program and contains an impressive 76 conditions. Achieving path coverage in such a
complex expression is impossible (276 = 7.5 × 1022 test cases), so smart approaches
such as MC/DC come in handy.
Bv or (Ev != El) or Bv2 or Bv3 or Bv4 or Bv5 or Bv6 or Bv7 or Bv8 or Bv9 or
Bv10 or Bv11 or Bv12 or Bv13 or Bv14 or Bv15 or Bv16 or Bv17 or Bv18 or
Bv19 or Bv20 or Bv21 or Bv22 or Bv23 or Bv24 or Bv25 or Bv26 or Bv27 or
Bv28 or Bv29 or Bv30 or Bv31 or Bv32 or Bv33 or Bv34 or Bv35 or Bv36 or
Bv37 or Bv38 or Bv39 or Bv40 or Bv41 or Bv42 or Bv43 or Bv44 or Bv45 or
Bv46 or Bv47 or Bv48 or Bv49 or Bv50 or Bv51 or (Ev2 = El2) or
((Ev3 = El2) and (Sav != Sac)) or Bv52 or Bv53 or Bv54 or Bv55 or Bv56
or Bv57 or Bv58 or Bv59 or Bv60 or Bv61 or Bv62 or Bv63 or Bv64 or Bv65
or Ev4 != El3 or Ev5 = El4 or Ev6 = El4 or Ev7 = El4 or Ev8 = El4 or
Ev9 = El4 or Ev10 = El4
Pragmatically speaking, testing such a complex expression, with or without MC/DC, is
a challenge, and you should avoid doing so when possible. Sometimes you can break
an expression into smaller bits that you can then test. But in cases where breaking
complex expressions is not possible, MC/DC shines.
Listing 3.11
Complex expression from flight simulation software



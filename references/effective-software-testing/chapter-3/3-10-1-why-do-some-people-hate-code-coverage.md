# 3.10.1 Why do some people hate code coverage? (pp.84-86)

---
**Page 84**

84
CHAPTER 3
Structural testing and code coverage
      .isEqualTo(expectedNoOfClumps);
}
static Stream<Arguments> generator() {   
  return Stream.of(
    of(new int[]{}, 0), // empty
    of(null, 0), // null
    of(new int[]{1,2,2,2,1}, 1), // one clump
    of(new int[]{1}, 0) // one element
  );
}
This test suite is reasonable and exercises the main behavior of the program, but note
how weak it is. It achieves 100% branch coverage, but it misses many interesting test
cases. Even without performing systematic specification testing, in a program that
counts clumps, it is natural to try the program with multiple clumps instead of just
one. We could try it with the last clump happening at the last item of the array or with
an array that has a clump starting in the first position. Such specific cases cannot be
captured by pure structural testing guided mainly by coverage. This is yet another rea-
son not to rely blindly on coverage. Structural testing shows its value when combined
with knowledge of the specification. 
3.10
Structural testing in the real world
Now that you have a clear picture of structural testing, the coverage criteria you can
use for guidance, and how to use structural testing in combination with specification-
based testing, let me discuss a few interesting points.
3.10.1 Why do some people hate code coverage?
I find it interesting that some people rage against code coverage. A prevalent opinion
is, “If I write a test case with no assertions, I achieve 100% coverage, but I am not test-
ing anything!” This is true. If your tests have no assertions, they do not test anything,
but the production code is exercised. However, I consider that a flawed argument. It
assumes the very worst (unrealistic) scenario possible. If you are writing test suites with
no assertions, you have bigger problems to take care of before you can enjoy the ben-
efits of structural testing.
 Between the lines, people use such an argument to explain that you should not
look at the coverage number blindly, because it can mislead you. That I fully agree
with. Here, the misconception is how people see code coverage. If code coverage is
only a number you should achieve, you may end up writing less useful test cases and
gaming the metric (something that Bouwers, Visser, and Van Deursen have argued
in 2012).
 I hope this chapter has clarified how structural testing and code coverage should
be used: to augment specification-based testing, quickly identify parts of the code that
are not currently exercised by the test suite, and identify partitions you missed when
The four test 
cases we defined


---
**Page 85**

85
Structural testing in the real world
doing specification-based testing. Achieving a high coverage number may be a conse-
quence of you doing that, but the purpose is different. If you leave a line uncovered, it
is because you thought about it and decided not to cover it.
EMPIRICAL EVIDENCE IN FAVOR OF CODE COVERAGE
Understanding whether structural coverage helps and whether high coverage num-
bers lead to better-tested software has been the goal of many empirical software engi-
neering researchers. Interestingly, while researchers have not yet found a magical
coverage number that we should aim for, some evidence points toward the benefits of
structural testing. I quote four of these studies:
Hutchins et al. (1994)—“Within the limited domain of our experiments, test sets
achieving coverage levels over 90% usually showed significantly better fault
detection than randomly chosen test sets of the same size. In addition, signifi-
cant improvements in the effectiveness of coverage-based tests usually occurred
as coverage increased from 90% to 100%. However, the results also indicate
that 100% code coverage alone is not a reliable indicator of the effectiveness of
a test set.”
Namin and Andrews (2009)—“Our experiments indicate that coverage is some-
times correlated with effectiveness when test suite size is controlled for, and that
using both size and coverage yields a more accurate prediction of effectiveness
than test suite size alone. This, in turn, suggests that both size and coverage are
important to test suite effectiveness.”
Inozemtseva and Holmes (2014)—“We found that there is a low to moderate cor-
relation between coverage and effectiveness when the number of test cases in
the suite is controlled for. In addition, we found that stronger forms of coverage
do not provide greater insight into the effectiveness of the suite. Our results
suggest that coverage, while useful for identifying under-tested parts of a pro-
gram, should not be used as a quality target because it is not a good indicator of
test suite effectiveness.”
Gopinath et al. (2020)—“This paper finds a correlation between lightweight,
widely available coverage criteria (statement, block, branch, and path coverage)
and mutation kills for hundreds of Java programs (…). For both original and
generated suites, statement coverage is the best predictor for mutation kills,
and in fact does a relatively good job of predicting suite quality.”
Although developing sound experiments to show whether coverage helps is difficult,
and we are not quite there yet (see Chen et al.’s 2020 paper for a good statistical expla-
nation of why it is hard), the current results make sense to me. Even with the small
code examples we have been exploring, we can see a relationship between covering all
the partitions via specification-based testing and covering the entire source code. The
opposite is also true: if you cover a significant part of the source code, you also cover
most of the partitions. Therefore, high coverage implies more partitions being tested.


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



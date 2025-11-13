# 4.1 Improving Unit Testing Skills Using Code Coverage (pp.71-79)

---
**Page 71**

CHAPTER 4
Expanding Your Testing Horizons
At this point, you’ve worked through the core topics in unit testing, including
JUnit and unit testing fundamentals, how to test various scenarios, and how
to use test doubles to deal with dependencies.
In this chapter, you’ll review a few topics that begin to move outside the sphere
of “doing unit testing”:
• Code coverage and how it can help (or hurt)
• Challenges with writing tests for multithreaded code
• Writing integration tests
Improving Unit Testing Skills Using Code Coverage
Code coverage metrics measure the percentage of code that your unit tests
execute (exercise) when run. Ostensibly, code that is covered is working, and
code that is not covered represents the risk of breakage.
From a high level, tests that exhaust all relevant pieces of code provide 100
percent coverage. Code with no tests whatsoever has 0 percent coverage. Most
code lies somewhere in between.
Many tools exist that will calculate coverage metrics for Java code, including
JaCoCo, OpenClover, SonarQube, and Cobertura. IntelliJ IDEA ships with a
coverage tool built into the IDE.
Numerous coverage metrics exist to measure various code aspects. Function
coverage, for example, measures the percentage of functions (methods) exer-
cised by tests. Some of the other metrics include line, statement, branch,
condition, and path coverage.
report erratum  •  discuss


---
**Page 72**

Line and statement coverage metrics are similar. Line coverage measures
source lines exercised. Since a line can consist of multiple statements, some
tools measure statement coverage.
Branch, condition, and path coverage metrics are similarly related. Branch
coverage measures whether all branches of a conditional statement (for
example, both true and false branches of an if statement) are executed. Condition
coverage measures whether all conditionals (including each in a complex
conditional) have evaluated to both true and false. Path coverage measures
whether every possible route through the code has been executed.
Most of the popular Java coverage tools support calculating line and branch
coverage. You’ll learn about these in this section.
Understanding Statement Coverage
Consider a Batter class that tracks a baseball batter’s strike count. A batter is
out after three strikes. A swing-and-a-miss with the bat—a strike—increments
the strike count. A foul ball (a ball hit out of play) also increments the strike
count unless the batter already has two strikes.
utj3-coverage/01/src/main/java/util/Batter.java
public class Batter {
private int strikeCount = 0;
public void foul() {
if (strikeCount < 2)
strikeCount++;
}
public void strike() {
strikeCount++;
}
public int strikeCount() {
return strikeCount;
}
}
Note the strike method. If none of your tests trigger its execution, its coverage
is 0 percent. If your tests do result in a call to strike, its whopping one line of
code gets exercised, and thus the recorded coverage is 100 percent.
The foul method contains a conditional. It increments strikeCount only if there
are fewer than two strikes. A conditional, implemented in Java with an if
statement, demands at least two tests—one that forces the conditional block
to execute (because the conditional expression resolved to true) and one that
bypasses the if block code.
Chapter 4. Expanding Your Testing Horizons • 72
report erratum  •  discuss


---
**Page 73**

The following test covers the special case—when two strikes already exist.
utj3-coverage/01/src/test/java/util/ABatter.java
@Test
void doesNotIncrementStrikesWhenAtTwo() {
batter.strike();
batter.strike();
batter.foul();
assertEquals(2, batter.strikeCount());
}
If you run this test “with coverage” (that’s the actual text on an IDEA menu
item), the if statement conditional evaluates to false because strikeCount is not
less than two. As a result, the if-statement body doesn’t execute, and strikeCount
is not incremented.
Here’s a tool window showing the summary coverage metrics:
Method coverage shows that three of three possible methods defined on the
Batter class were exercised. That’s not terribly interesting or useful.
Line coverage shows that three of four lines were exercised across those three
methods—one of the lines didn’t get covered when the test ran. In this case,
it’s because you only ran one test in ABatter. Run them all to attain 100 percent
line coverage.
The real value of a coverage tool is that it shows exactly what lines are exer-
cised and what lines are not. IDEA’s coverage tool window shows colored
markers in the gutter (the gray strip left of the source code) to the immediate
right of the line numbers. It marks executed lines as green, lines not executed
as red, and lines partially covered (read on) as yellow as shown in the figure
on page 74.
The increment operation (strikeCount++) is marked red because it is never
executed.
Uncovered code is one of two things: dead or risky.
It can be near-impossible to determine whether code is ever needed or used.
“All dead” code (as opposed to mostly dead code, which might have some
report erratum  •  discuss
Improving Unit Testing Skills Using Code Coverage • 73


---
**Page 74**

future resurrected purpose) can waste time in many ways. Like a vampire,
dead code sucks time: when you read it, when it shows up in search results,
and when you mistakenly start making changes (true stories here) to it.
When you encounter uncovered, mostly dead code, bring it into the sunlight
of your whole team. If it doesn’t shrivel away under their scrutiny, cover the
code with tests. Otherwise, delete it.
Unit tests declare intent. If you test every intent, you can safely
delete untested code.
Add a second test involving only a single strike to get 100 percent coverage
in foul:
utj3-coverage/01/src/test/java/util/ABatter.java
@Test
void incrementsStrikesWhenLessThan2() {
batter.strike();
batter.foul();
assertEquals(2, batter.strikeCount());
}
Conditionals and Code Coverage
Line coverage is an unsophisticated metric that tells you only whether a line
of code was executed or not. It doesn’t tell you if you’ve explored different
Chapter 4. Expanding Your Testing Horizons • 74
report erratum  •  discuss


---
**Page 75**

data cases. For example, if a method accepts an int, did you test it with 0?
With negative numbers and very large numbers? A coverage tool doesn’t even
tell you if the tests contain any assertions. (Yes, some clever developers do
that to make their coverage numbers look better.)
Complex conditionals often represent insufficiently covered paths through
your code. You create complex conditionals when you produce Boolean
expressions involving the logical operators OR (||) and AND (&&).
Suppose you write one test that exercises a complex conditional using only
the OR operator. The line coverage metric will credit your tests for the entire
line containing the complex conditional as long as any one of its Boolean
expressions resolves to true. But you won’t have ensured that all the other
Boolean expressions behave as expected.
Conditional coverage tools can help you pinpoint deficiencies in your coverage
of conditionals.
Take a look at the next intended increment of the Batter code, which supports
tracking balls and walks. It introduces the notion of whether or not a batter’s
turn at home plate is “done,” meaning that they either struck out or walked
(hits and fielding outs would come later). The method isDone implements that
complex conditional.
utj3-coverage/02/src/main/java/util/Batter.java
public class Batter {
private int strikeCount = 0;
private int ballCount = 0;
public void foul() {
if (strikeCount < 2)
strikeCount++;
}
public void ball() {
ballCount++;
}
public void strike() {
strikeCount++;
}
public int strikeCount() {
return strikeCount;
}
public boolean isDone() {
➤
return struckOut() || walked();
➤
}
➤
report erratum  •  discuss
Improving Unit Testing Skills Using Code Coverage • 75


---
**Page 76**

private boolean walked() {
return ballCount == 4;
}
private boolean struckOut() {
return strikeCount == 3;
}
}
A new test is added to the test class to cover a strikeout case:
utj3-coverage/02/src/test/java/util/ABatter.java
@Test
void whenStruckOut() {
batter.strike();
batter.strike();
batter.strike();
assertTrue(batter.isDone());
}
IDEA supports the branch coverage metric, but it is turned off by default.
Turn it on and run all the tests in ABatter. Your code coverage summary now
includes a column for Branch Coverage %:
The summary pane shows that you have a branch coverage deficiency; cur-
rently, it measures only 50 percent. Again, the more revealing aspect is how
the coverage tool marks code within the editor for Batter. The isDone method is
marked with yellow to indicate that not all branches of the complex conditional
are covered. A call to struckOut occurs, but not to walked.
Chapter 4. Expanding Your Testing Horizons • 76
report erratum  •  discuss


---
**Page 77**

The struckOut method is also marked as partially covered. If you click on the
yellow marker, IDEA reveals the coverage data:
Hits: 1
Covered 1/2 branches
In other words, the method was invoked (“hit”) one time. Full branch coverage
of a simple Boolean conditional would require getting hit twice—once where
it evaluates to true and once where it gets evaluated to false.
To garner full coverage for ABatter, you’ll need to add a couple of tests to not
only exercise the walked method but to also ensure that you have a test in
which the entire expression in isDone returns false.
utj3-coverage/03/src/test/java/util/ABatter.java
@Test
void isDoneWithWalk() {
for (var i = 0; i < 4; i++)
batter.ball();
assertTrue(batter.isDone());
}
@Test
void isNotDoneWhenNeitherWalkNorStrikeout() {
assertFalse(batter.isDone());
}
How Much Coverage Is Enough?
Any one of your unit tests will exercise only a very small percentage of code—a
unit’s worth. If you want 100 percent coverage, write unit tests for every unit
you add to your system. Emphasize testing the behaviors, not the methods.
Use tools like ZOM to help you think through the different cases and their
outcomes.
On the surface, it would seem that higher code coverage is good and lower
coverage is not so good. But your manager craves a single number that says,
“Yup, we’re doing well on our unit testing practice,” or “No, we’re not writing
enough unit tests.”
To satisfy your manager, you’d unfortunately need to first determine what
enough means. Obviously, 0 percent is not enough. And 100 percent would
be great, but is it realistic? The use of certain frameworks can make it nearly
impossible to hit 100 percent without some trickery.
Most folks out there (the purveyors of Emma included) suggest that coverage
under 70 percent is insufficient. I agree.
report erratum  •  discuss
Improving Unit Testing Skills Using Code Coverage • 77


---
**Page 78**

Many developers also claim that attempts to increase coverage represent
diminishing returns on value. I disagree. Teams that habitually write unit tests
after they write code achieve coverage levels of 70 percent with relative ease.
Unfortunately, that means the remaining 30 percent of their code remains
untested, often because it’s difficult, hard-to-test code. Difficult code hides more
defects, so at least a third of your defects will probably lie in this untested code.
Jeff’s Theory of Code Coverage: the amount of costly code
increases in the areas of least coverage.
The better your design, the easier it is to write tests. Revisit Chapter 8, Refactor-
ing to Cleaner Code, on page 147 and Chapter 9, Refactoring Your Code’s
Structure, on page 169 to understand how to better structure your code. A
good design coupled with the will to increase coverage will move you in the
direction of 100 percent, which should lead to fewer defects. You might not
reach 100 percent, and that’s okay.
Developers practicing TDD (see Chapter 11, Advancing with Test-Driven Devel-
opment (TDD), on page 211) achieve percentages well over 90 percent, largely by
definition. They write a test for each new behavior they’re about to code. Those
who do TDD, myself included, rarely look at the coverage numbers. TDD makes
coverage a self-fulfilling prophecy.
Coverage percentages can mislead. You can easily write a few tests that blast
through a large percentage of code yet assert little of use. Most tools don’t
even care if your tests have no assertions (which means they’re not really
tests). The tools certainly don’t care if your tests are cryptic or prolix or if they
assert nothing useful. Too many teams spend a fortune writing unit tests
with decent coverage numbers but little value.
Unfortunately, managers always want a single number they can use to mea-
sure success. The code-coverage number is but a surface-level metric that
means little if the tests stink. And if someone tells the team that the metric
goal matters most, the tests will stink.
A downward code coverage trend is probably useful information, however.
Your coverage percentage should either increase or become stable over time
as you add behavior.
The Value in Code Coverage
If you write your tests after you write the corresponding code, you’ll miss
numerous test cases until you improve your skills and habits. Even if you
Chapter 4. Expanding Your Testing Horizons • 78
report erratum  •  discuss


---
**Page 79**

try TDD and write tests first for all unit behaviors, you’ll still find yourself
sneaking in untested logic over time.
As you’re learning, lean on the visual red-yellow-and-green annotations that
the tools produce.
Use code-coverage tools to help you understand where your code
lacks coverage or where your team is trending downward.
Do your best to avoid the code coverage metric debate and convince your
leadership that the metric is not for them. It will ultimately create problems
when used for anything but educational purposes.
Testing Multithreaded Code
It’s hard enough to write code that works as expected. That’s one reason to
write unit tests. It’s dramatically harder to write concurrent code that works
and even harder to verify that it’s safe enough to ship.
In one sense, testing application code that requires concurrent processing is
technically out of the realm of unit testing. It’s better classified as integration
testing. You’re verifying that you can integrate the notion of your application-
specific logic with the ability to execute portions of it concurrently.
Tests for threaded code tend to be slower because you must expand the scope
of execution time to ensure that you have no concurrency issues. Threading
defects sometimes sneakily lie in wait, surfacing long after you thought you’d
stomped them all out.
There are piles of ways to approach multithreading in Java and, similarly,
piles of ways for your implementation to go wrong: deadlock, race conditions,
livelock, starvation, and thread interference, to name a few. One could fill a
book (or at least several chapters) covering how to test for and correct all of
these policies. I’m not allowed to fill that much paper, so you’ll see only a
short example that highlights a couple of key thoughts.
Tips for Testing Multithreaded Code
Here’s a short list of techniques for designing and analyzing multithreaded
code that minimizes concurrency issues:
• Minimize the overlap between threading controls and application code.
Rework your design so that you can unit test the bulk of application
report erratum  •  discuss
Testing Multithreaded Code • 79



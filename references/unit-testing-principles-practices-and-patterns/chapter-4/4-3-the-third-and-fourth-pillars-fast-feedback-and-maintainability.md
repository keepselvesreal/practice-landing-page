# 4.3 The third and fourth pillars: Fast feedback and maintainability (pp.79-80)

---
**Page 79**

79
The third and fourth pillars: Fast feedback and maintainability
Why are false positives not as important initially? Because the importance of refactor-
ing is also not immediate; it increases gradually over time. You don’t need to conduct
many code clean-ups in the beginning of the project. Newly written code is often shiny
and flawless. It’s also still fresh in your memory, so you can easily refactor it even if
tests raise false alarms.
 But as time goes on, the code base deteriorates. It becomes increasingly complex
and disorganized. Thus you have to start conducting regular refactorings in order to
mitigate this tendency. Otherwise, the cost of introducing new features eventually
becomes prohibitive.
 As the need for refactoring increases, the importance of resistance to refactoring in
tests increases with it. As I explained earlier, you can’t refactor when the tests keep cry-
ing “wolf” and you keep getting warnings about bugs that don’t exist. You quickly lose
trust in such tests and stop viewing them as a reliable source of feedback.
 Despite the importance of protecting your code against false positives, especially in
the later project stages, few developers perceive false positives this way. Most people
tend to focus solely on improving the first attribute of a good unit test—protection
against regressions, which is not enough to build a valuable, highly accurate test suite
that helps sustain project growth.
 The reason, of course, is that far fewer projects get to those later stages, mostly
because they are small and the development finishes before the project becomes too
big. Thus developers face the problem of unnoticed bugs more often than false
alarms that swarm the project and hinder all refactoring undertakings. And so, people
optimize accordingly. Nevertheless, if you work on a medium to large project, you
have to pay equal attention to both false negatives (unnoticed bugs) and false posi-
tives (false alarms). 
4.3
The third and fourth pillars: Fast feedback 
and maintainability
In this section, I talk about the two remaining pillars of a good unit test:
Fast feedback
Maintainability
As you may remember from chapter 2, fast feedback is an essential property of a unit
test. The faster the tests, the more of them you can have in the suite and the more
often you can run them.
 With tests that run quickly, you can drastically shorten the feedback loop, to the
point where the tests begin to warn you about bugs as soon as you break the code, thus
reducing the cost of fixing those bugs almost to zero. On the other hand, slow tests
delay the feedback and potentially prolong the period during which the bugs remain
unnoticed, thus increasing the cost of fixing them. That’s because slow tests discour-
age you from running them often, and therefore lead to wasting more time moving in
a wrong direction.


---
**Page 80**

80
CHAPTER 4
The four pillars of a good unit test
 Finally, the fourth pillar of good units tests, the maintainability metric, evaluates
maintenance costs. This metric consists of two major components:
How hard it is to understand the test—This component is related to the size of the
test. The fewer lines of code in the test, the more readable the test is. It’s also
easier to change a small test when needed. Of course, that’s assuming you don’t
try to compress the test code artificially just to reduce the line count. The qual-
ity of the test code matters as much as the production code. Don’t cut corners
when writing tests; treat the test code as a first-class citizen.
How hard it is to run the test—If the test works with out-of-process dependencies,
you have to spend time keeping those dependencies operational: reboot the
database server, resolve network connectivity issues, and so on. 
4.4
In search of an ideal test
Here are the four attributes of a good unit test once again:
Protection against regressions
Resistance to refactoring
Fast feedback
Maintainability
These four attributes, when multiplied together, determine the value of a test. And by
multiplied, I mean in a mathematical sense; that is, if a test gets zero in one of the attri-
butes, its value turns to zero as well:
Value estimate = [0..1] * [0..1] * [0..1] * [0..1]
TIP
In order to be valuable, the test needs to score at least something in all
four categories.
Of course, it’s impossible to measure these attributes precisely. There’s no code analy-
sis tool you can plug a test into and get the exact numbers. But you can still evaluate
the test pretty accurately to see where a test stands with regard to the four attributes.
This evaluation, in turn, gives you the test’s value estimate, which you can use to
decide whether to keep the test in the suite.
 Remember, all code, including test code, is a liability. Set a fairly high threshold
for the minimum required value, and only allow tests in the suite if they meet this
threshold. A small number of highly valuable tests will do a much better job sustain-
ing project growth than a large number of mediocre tests.
 I’ll show some examples shortly. For now, let’s examine whether it’s possible to cre-
ate an ideal test.



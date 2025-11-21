# 4.2.2 The importance of false positives and false negatives: The dynamics (pp.78-79)

---
**Page 78**

78
CHAPTER 4
The four pillars of a good unit test
accuracy. The first is to increase the numerator, signal: that is, make the test better at
finding regressions. The second is to reduce the denominator, noise: make the test bet-
ter at not raising false alarms.
 Both are critically important. There’s no use for a test that isn’t capable of finding
any bugs, even if it doesn’t raise false alarms. Similarly, the test’s accuracy goes to zero
when it generates a lot of noise, even if it’s capable of finding all the bugs in code.
These findings are simply lost in the sea of irrelevant information. 
4.2.2
The importance of false positives and false negatives: 
The dynamics
In the short term, false positives are not as bad as false negatives. In the beginning of a
project, receiving a wrong warning is not that big a deal as opposed to not being
warned at all and running the risk of a bug slipping into production. But as the proj-
ect grows, false positives start to have an increasingly large effect on the test suite
(figure 4.5).
Test accuracy =
Noise (number of false alarms raised)
Signal (number of bugs found)
Figure 4.4
A test is accurate insofar as it generates a 
strong signal (is capable of finding bugs) with as little 
noise (false alarms) as possible.
Eﬀect on the
test suite
Project duration
False negatives
False positives
Figure 4.5
False positives (false alarms) don’t have as much of a 
negative effect in the beginning. But they become increasingly 
important as the project grows—as important as false negatives 
(unnoticed bugs).


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



# 1.2.1 What makes a good or bad test? (pp.7-8)

---
**Page 7**

7
The goal of unit testing
domino effect. Eventually, the code base becomes unreliable. And worst of all, it’s
hard to bring it back to stability.
 Tests help overturn this tendency. They act as a safety net—a tool that provides
insurance against a vast majority of regressions. Tests help make sure the existing
functionality works, even after you introduce new features or refactor the code to bet-
ter fit new requirements.
DEFINITION
A regression is when a feature stops working as intended after a cer-
tain event (usually, a code modification). The terms regression and software bug
are synonyms and can be used interchangeably.
The downside here is that tests require initial—sometimes significant—effort. But they
pay for themselves in the long run by helping the project to grow in the later stages.
Software development without the help of tests that constantly verify the code base
simply doesn’t scale.
 Sustainability and scalability are the keys. They allow you to maintain development
speed in the long run.
1.2.1
What makes a good or bad test?
Although unit testing helps maintain project growth, it’s not enough to just write tests.
Badly written tests still result in the same picture.
 As shown in figure 1.2, bad tests do help to slow down code deterioration at the
beginning: the decline in development speed is less prominent compared to the situa-
tion with no tests at all. But nothing really changes in the grand scheme of things. It
might take longer for such a project to enter the stagnation phase, but stagnation is
still inevitable.
Without tests
With good tests
With bad tests
Progress
Work
hours
spent
Figure 1.2
The difference in 
growth dynamics between 
projects with good and bad 
tests. A project with badly 
written tests exhibits the 
properties of a project with 
good tests at the beginning, 
but it eventually falls into 
the stagnation phase.


---
**Page 8**

8
CHAPTER 1
The goal of unit testing
Remember, not all tests are created equal. Some of them are valuable and contribute a lot
to overall software quality. Others don’t. They raise false alarms, don’t help you catch
regression errors, and are slow and difficult to maintain. It’s easy to fall into the trap
of writing unit tests for the sake of unit testing without a clear picture of whether it
helps the project.
 You can’t achieve the goal of unit testing by just throwing more tests at the project.
You need to consider both the test’s value and its upkeep cost. The cost component is
determined by the amount of time spent on various activities:
Refactoring the test when you refactor the underlying code
Running the test on each code change
Dealing with false alarms raised by the test
Spending time reading the test when you’re trying to understand how the
underlying code behaves
It’s easy to create tests whose net value is close to zero or even is negative due to high
maintenance costs. To enable sustainable project growth, you have to exclusively
focus on high-quality tests—those are the only type of tests that are worth keeping in
the test suite.
It’s crucial to learn how to differentiate between good and bad unit tests. I cover this
topic in chapter 4. 
1.3
Using coverage metrics to measure test suite quality
In this section, I talk about the two most popular coverage metrics—code coverage
and branch coverage—how to calculate them, how they’re used, and problems with
them. I’ll show why it’s detrimental for programmers to aim at a particular coverage
number and why you can’t just rely on coverage metrics to determine the quality of
your test suite.
DEFINITION
A coverage metric shows how much source code a test suite exe-
cutes, from none to 100%.
Production code vs. test code 
People often think production code and test code are different. Tests are assumed
to be an addition to production code and have no cost of ownership. By extension,
people often believe that the more tests, the better. This isn’t the case. Code is a
liability, not an asset. The more code you introduce, the more you extend the surface
area for potential bugs in your software, and the higher the project’s upkeep cost. It’s
always better to solve problems with as little code as possible.
Tests are code, too. You should view them as the part of your code base that aims at
solving a particular problem: ensuring the application’s correctness. Unit tests, just
like any other code, are also vulnerable to bugs and require maintenance.



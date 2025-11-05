# 3.1.2 Avoid multiple arrange, act, and assert sections (pp.43-44)

---
**Page 43**

43
How to structure a unit test
In the arrange section, you bring the system under test (SUT) and its dependen-
cies to a desired state.
In the act section, you call methods on the SUT, pass the prepared dependen-
cies, and capture the output value (if any).
In the assert section, you verify the outcome. The outcome may be represented
by the return value, the final state of the SUT and its collaborators, or the meth-
ods the SUT called on those collaborators.
The natural inclination is to start writing a test with the arrange section. After all, it
comes before the other two. This approach works well in the vast majority of cases, but
starting with the assert section is a viable option too. When you practice Test-Driven
Development (TDD)—that is, when you create a failing test before developing a
feature—you don’t know enough about the feature’s behavior yet. So, it becomes
advantageous to first outline what you expect from the behavior and then figure out
how to develop the system to meet this expectation.
 Such a technique may look counterintuitive, but it’s how we approach problem
solving. We start by thinking about the objective: what a particular behavior should to
do for us. The actual solving of the problem comes after that. Writing down the asser-
tions before everything else is merely a formalization of this thinking process. But
again, this guideline is only applicable when you follow TDD—when you write a test
before the production code. If you write the production code before the test, by the
time you move on to the test, you already know what to expect from the behavior, so
starting with the arrange section is a better option. 
3.1.2
Avoid multiple arrange, act, and assert sections
Occasionally, you may encounter a test with multiple arrange, act, or assert sections. It
usually works as shown in figure 3.1.
 When you see multiple act sections separated by assert and, possibly, arrange sec-
tions, it means the test verifies multiple units of behavior. And, as we discussed in
chapter 2, such a test is no longer a unit test but rather is an integration test. It’s best
Given-When-Then pattern
You might have heard of the Given-When-Then pattern, which is similar to AAA. This
pattern also advocates for breaking the test down into three parts:
Given—Corresponds to the arrange section
When—Corresponds to the act section
Then—Corresponds to the assert section
There’s no difference between the two patterns in terms of the test composition. The
only distinction is that the Given-When-Then structure is more readable to non-
programmers. Thus, Given-When-Then is more suitable for tests that are shared with
non-technical people.


---
**Page 44**

44
CHAPTER 3
The anatomy of a unit test
to avoid such a test structure. A single action ensures that your tests remain within the
realm of unit testing, which means they are simple, fast, and easy to understand. If you
see a test containing a sequence of actions and assertions, refactor it. Extract each act
into a test of its own.
 It’s sometimes fine to have multiple act sections in integration tests. As you may
remember from the previous chapter, integration tests can be slow. One way to speed
them up is to group several integration tests together into a single test with multiple
acts and assertions. It’s especially helpful when system states naturally flow from one
another: that is, when an act simultaneously serves as an arrange for the subsequent act.
 But again, this optimization technique is only applicable to integration tests—and
not all of them, but rather those that are already slow and that you don’t want to
become even slower. There’s no need for such an optimization in unit tests or integra-
tion tests that are fast enough. It’s always better to split a multistep unit test into sev-
eral tests. 
3.1.3
Avoid if statements in tests
Similar to multiple occurrences of the arrange, act, and assert sections, you may some-
times encounter a unit test with an if statement. This is also an anti-pattern. A test—
whether a unit test or an integration test—should be a simple sequence of steps with
no branching.
 An if statement indicates that the test verifies too many things at once. Such a test,
therefore, should be split into several tests. But unlike the situation with multiple AAA
Arrange the test
Act
Assert
Act some more
Assert again
Figure 3.1
Multiple arrange, act, and assert sections are a hint that the test verifies 
too many things at once. Such a test needs to be split into several tests to fix the 
problem.



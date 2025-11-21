# 1.0 Introduction [auto-generated] (pp.3-4)

---
**Page 3**

3
The goal of unit testing
Learning unit testing doesn’t stop at mastering the technical bits of it, such as
your favorite test framework, mocking library, and so on. There’s much more to
unit testing than the act of writing tests. You always have to strive to achieve the
best return on the time you invest in unit testing, minimizing the effort you put
into tests and maximizing the benefits they provide. Achieving both things isn’t
an easy task.
 It’s fascinating to watch projects that have achieved this balance: they grow
effortlessly, don’t require much maintenance, and can quickly adapt to their cus-
tomers’ ever-changing needs. It’s equally frustrating to see projects that failed to do
so. Despite all the effort and an impressive number of unit tests, such projects drag
on slowly, with lots of bugs and upkeep costs.
This chapter covers
The state of unit testing
The goal of unit testing
Consequences of having a bad test suite
Using coverage metrics to measure test 
suite quality
Attributes of a successful test suite


---
**Page 4**

4
CHAPTER 1
The goal of unit testing
 That’s the difference between various unit testing techniques. Some yield great
outcomes and help maintain software quality. Others don’t: they result in tests that
don’t contribute much, break often, and require a lot of maintenance in general.
 What you learn in this book will help you differentiate between good and bad unit
testing techniques. You’ll learn how to do a cost-benefit analysis of your tests and apply
proper testing techniques in your particular situation. You’ll also learn how to avoid
common anti-patterns—patterns that may make sense at first but lead to trouble down
the road.
 But let’s start with the basics. This chapter gives a quick overview of the state of
unit testing in the software industry, describes the goal behind writing and maintain-
ing tests, and provides you with the idea of what makes a test suite successful.
1.1
The current state of unit testing
For the past two decades, there’s been a push toward adopting unit testing. The push
has been so successful that unit testing is now considered mandatory in most compa-
nies. Most programmers practice unit testing and understand its importance. There’s
no longer any dispute as to whether you should do it. Unless you’re working on a
throwaway project, the answer is, yes, you do.
 When it comes to enterprise application development, almost every project
includes at least some unit tests. A significant percentage of such projects go far
beyond that: they achieve good code coverage with lots and lots of unit and integra-
tion tests. The ratio between the production code and the test code could be any-
where between 1:1 and 1:3 (for each line of production code, there are one to
three lines of test code). Sometimes, this ratio goes much higher than that, to a
whopping 1:10.
 But as with all new technologies, unit testing continues to evolve. The discussion
has shifted from “Should we write unit tests?” to “What does it mean to write good unit
tests?” This is where the main confusion still lies.
 You can see the results of this confusion in software projects. Many projects have
automated tests; they may even have a lot of them. But the existence of those tests
often doesn’t provide the results the developers hope for. It can still take program-
mers a lot of effort to make progress in such projects. New features take forever to
implement, new bugs constantly appear in the already implemented and accepted
functionality, and the unit tests that are supposed to help don’t seem to mitigate this
situation at all. They can even make it worse.
 It’s a horrible situation for anyone to be in—and it’s the result of having unit tests
that don’t do their job properly. The difference between good and bad tests is not
merely a matter of taste or personal preference, it’s a matter of succeeding or failing
at this critical project you’re working on.
 It’s hard to overestimate the importance of the discussion of what makes a good
unit test. Still, this discussion isn’t occurring much in the software development industry



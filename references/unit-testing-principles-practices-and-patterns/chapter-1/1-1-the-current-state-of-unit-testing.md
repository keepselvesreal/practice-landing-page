# 1.1 The current state of unit testing (pp.4-5)

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


---
**Page 5**

5
The goal of unit testing
today. You’ll find a few articles and conference talks online, but I’ve yet to see any
comprehensive material on this topic.
 The situation in books isn’t any better; most of them focus on the basics of unit
testing but don’t go much beyond that. Don’t get me wrong. There’s a lot of value in
such books, especially when you are just starting out with unit testing. However, the
learning doesn’t end with the basics. There’s a next level: not just writing tests, but
doing unit testing in a way that provides you with the best return on your efforts.
When you reach this point, most books pretty much leave you to your own devices to
figure out how to get to that next level.
 This book takes you there. It teaches a precise, scientific definition of the ideal
unit test. You’ll see how this definition can be applied to practical, real-world exam-
ples. My hope is that this book will help you understand why your particular project
may have gone sideways despite having a good number of tests, and how to correct its
course for the better.
 You’ll get the most value out of this book if you work in enterprise application
development, but the core ideas are applicable to any software project.
1.2
The goal of unit testing
Before taking a deep dive into the topic of unit testing, let’s step back and consider
the goal that unit testing helps you to achieve. It’s often said that unit testing practices
lead to a better design. And it’s true: the necessity to write unit tests for a code base
normally leads to a better design. But that’s not the main goal of unit testing; it’s
merely a pleasant side effect.
What is an enterprise application?
An enterprise application is an application that aims at automating or assisting an
organization’s inner processes. It can take many forms, but usually the characteris-
tics of an enterprise software are
High business logic complexity
Long project lifespan
Moderate amounts of data
Low or moderate performance requirements 
The relationship between unit testing and code design
The ability to unit test a piece of code is a nice litmus test, but it only works in one
direction. It’s a good negative indicator—it points out poor-quality code with relatively
high accuracy. If you find that code is hard to unit test, it’s a strong sign that the code
needs improvement. The poor quality usually manifests itself in tight coupling, which
means different pieces of production code are not decoupled from each other
enough, and it’s hard to test them separately.



# 2.2 The library, the assert, the runner, and the reporter (pp.33-34)

---
**Page 33**

33
2.2
The library, the assert, the runner, and the reporter
Imagine trying to write all this reporting functionality yourself. It’s possible, but who’s
got the time and the inclination? Plus, you’d have to take care of any bugs in the
reporting mechanism. 
 If we change goodbye to hello in the test, we can see what happens when the test
passes (figure 2.3). Nice and green, as all things should be (again, in the digital ver-
sion—otherwise it’s nice and grey).
You might note that it takes 1.5 seconds to run this single Hello World test. If we used
the command jest --watch instead, we could have Jest monitor filesystem activity in
our folder and automatically run tests for files that have changed without re-initializ-
ing itself every time. This can save a considerable amount of time, and it really helps
with the whole notion of continuous testing. Set a terminal in the other window of your
workstation with jest --watch on it, and you can keep coding and getting fast feed-
back on issues you might be creating. That’s a good way to get into the flow of things.
 Jest also supports async-style testing and callbacks. I’ll touch on these when we get
to those topics later in the book, but if you’d like to learn more about this style now,
head over to the Jest documentation on the subject: https://jestjs.io/docs/en/asyn-
chronous.
2.2
The library, the assert, the runner, and the reporter
Jest has acted in several capacities for us:
It acted as a test library to use when writing the test.
It acted as an assertion library for asserting inside the test (expect).
It acted as the test runner.
It acted as the test reporter for the test run.
Jest also provides isolation facilities to create mocks, stubs, and spies, though we
haven’t seen that yet. We’ll touch on these ideas in later chapters. 
 Other than isolation facilities, it’s very common in other languages for a test frame-
work to fill all the roles I just mentioned—library, assertions, test runner, and test
reporter—but the JavaScript world seems a bit more fragmented. Many other test
frameworks provide only some of these facilities. Perhaps this is because the mantra of
Figure 2.3
Jest terminal 
output for a passing test 


---
**Page 34**

34
CHAPTER 2
A first unit test
“do one thing, and do it well” has been taken to heart, or perhaps it’s for other rea-
sons. In any case, Jest stands out as one of a handful of all-in-one frameworks. It is a
testament to the strength of the open source culture in JavaScript that for each one of
these categories, there are multiple tools that you can mix and match to create your
own super toolset. 
 One of the reasons I chose Jest for this book is so we don’t have to bother too
much with the tooling or deal with missing features—we can just focus on the pat-
terns. That way we won’t have to use multiple frameworks in a book that is mostly con-
cerned with patterns and antipatterns.
2.3
What unit testing frameworks offer
Let’s zoom out for a second and see where we are. What do frameworks like Jest offer
us over creating our own framework, like we started to do in the previous chapter, or
over manually testing things? 
Structure—Instead of reinventing the wheel every time you want to test a fea-
ture, when you use a test framework you always start out the same way—by writ-
ing a test with a well-defined structure that everyone can easily recognize, read,
and understand.
Repeatability—When using a test framework, it’s easy to repeat the act of writing
a new test. It’s also easy to repeat the execution of the test, using a test runner,
and it’s easy to do this quickly and many times a day. It’s also easy to understand
failures and their causes. Someone has already done all the hard work for us,
instead of us having to code all that stuff into our hand-rolled framework. 
Confidence and time savings—When we roll our own test framework, the frame-
work is more likely to have bugs in it, since it is less battle-tested than an existing
mature and widely used framework. On the other hand, manually testing things
is usually very time consuming. When we’re short on time, we’ll likely focus on
testing the things that feel the most critical and skip over things that might feel
less important. We could be skipping small but significant bugs. By making it
easy to write new tests, it’s more likely that we’ll also write tests for the stuff that
feels less significant because we won’t be spending too much time writing tests
for the big stuff.
Shared understanding—The framework’s reporting can be helpful for managing
tasks at the team level (when a test is passing, it means the task is done). Some
people find this useful.
In short, frameworks for writing, running, and reviewing unit tests and their results
can make a huge difference in the daily lives of developers who are willing to invest
the time in learning how to use them properly. Figure 2.4 shows the areas in software
development in which a unit testing framework and its helper tools have influence,
and table 2.1 lists the types of actions we usually execute with a test framework.



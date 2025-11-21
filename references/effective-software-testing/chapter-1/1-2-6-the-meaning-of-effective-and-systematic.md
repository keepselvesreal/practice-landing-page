# 1.2.6 The meaning of effective and systematic (pp.15-16)

---
**Page 15**

15
Effective software testing for developers
1.2.4
The myth of “correctness by design”
Now that you have a clearer picture of what I mean by effective and systematic soft-
ware testing, let me debunk a myth. There is a perception among software developers
that if you design code in a simple way, it will not have bugs, as if the secret of bug-free
code is simplicity.
 Empirical research in software engineering has repeatedly shown that simple,
non-smelly code is less prone to defects than complex code (see, for example, the
2006 paper by Shatnawi and Li). However, simplicity is far from enough. It is naive
to believe that testing can be fully replaced by simplicity. The same is true for
“correctness by design”: designing your code well does not mean you avoid all pos-
sible bugs.
1.2.5
The cost of testing
You may be thinking that forcing developers to apply rigorous testing may be too
costly. Figure 1.4 shows the many techniques developers have to apply if they follow
the flow I am proposing. It is true: testing software properly is more work than not
doing so. Let me convince you why it is worth it:
The cost of bugs that happen in production often outweighs the cost of preven-
tion (as shown by Boehm and Papaccio, 1988). Think of a popular web shop
and how much it would cost the shop if the payment application goes down for
30 minutes due to a bug that could have been easily prevented via testing.
Teams that produce many bugs tend to waste time in an eternal loop where
developers write bugs, customers (or dedicated QAs) find the bugs, developers
fix the bugs, customers find a different set of bugs, and so on.
Practice is key. Once developers are used to engineering test cases, they can do
it much faster. 
1.2.6
The meaning of effective and systematic
I have been using two words to describe how I expect a developer to test: effectively and
systematically. Being effective means we focus on writing the right tests. Software testing
is all about trade-offs. Testers want to maximize the number of bugs they find while
minimizing the effort required to find the bugs. How do we achieve this? By knowing
what to test.
 All the techniques I present in this book have a clear beginning (what to test) and
a clear end (when to stop). Of course, I do not mean your systems will be bug-free if you
follow these techniques. As a community, we still do not know how to build bug-free
systems. But I can confidently say that the number of bugs will be reduced, hopefully
to tolerable levels.
 Being systematic means that for a given piece of code, any developer should come
up with the same test suite. Testing often happens in an ad hoc manner. Developers
engineer the test cases that come to mind. It is common to see two developers devel-


---
**Page 16**

16
CHAPTER 1
Effective and systematic software testing
oping different test suites for the same program. We should be able to systematize our
processes to reduce the dependency on the developer who is doing the job.
 I understand and agree with the argument that software development is a creative
process that cannot be executed by robots. I believe that humans will always be in the
loop when it comes to building software; but why not let developers focus on what
requires creativity? A lot of software testing can be systematized, and that is what you
will see throughout this book. 
1.2.7
The role of test automation
Automation is key for an effective testing process. Every test case we devise here is
later automated via a testing framework such as JUnit. Let me clearly distinguish
between test case design and test case execution. Once a test case is written, a framework
runs it and shows reports, failures, and so on. This is all that these frameworks do.
Their role is very important, but the real challenge in software testing is not writing
JUnit code but designing decent test cases that may reveal bugs. Designing test cases is
mostly a human activity and is what this book primarily focuses on.
NOTE
If you are not familiar with JUnit, it should not be a problem, because
the examples in the book are easy to read. But as I mention throughout the
book, the more familiar you are with the testing framework, the better.
In the chapters where I discuss testing techniques, we first engineer the test cases and
only later automate them with JUnit code. In real life, you may mingle both activities;
but in this book, I decided to keep them separate so you can see the difference. This
also means the book does not talk much about tooling. JUnit and other testing frame-
works are powerful tools, and I recommend reading the manuals and books that focus
on them. 
1.3
Principles of software testing 
(or, why testing is so difficult)
A simplistic view of software testing is that if we want our systems to be well tested, we
must keep adding tests until we have enough. I wish it were that simple. Ensuring that
programs have no bugs is virtually impossible, and developers should understand why
that is the case.
 In this section, I discuss some principles that make our lives as software testers
more difficult and what we can do to mitigate them. These principles were inspired by
those presented in the International Software Testing Qualifications Board (ISTQB)
book by Black, Veenendaal, and Graham (2012).
1.3.1
Exhaustive testing is impossible
We do not have the resources to completely test our programs. Testing all possible sit-
uations in a software system might be impossible even if we had unlimited resources.
Imagine a software system with “only” 300 different flags or configuration settings



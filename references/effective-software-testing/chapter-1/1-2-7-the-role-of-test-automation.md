# 1.2.7 The role of test automation (pp.16-16)

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



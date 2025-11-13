# 1.3.1 Exhaustive testing is impossible (pp.16-17)

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


---
**Page 17**

17
Principles of software testing (or, why testing is so difficult)
(such as the Linux operating system). Each flag can be set to true or false (Boolean)
and can be set independently from the others. The software system behaves differ-
ently according to the configured combination of flags. Having two possible values for
each of the 300 flags gives 2300 combinations that need to be tested. For comparison,
the number of atoms in the universe is estimated to be 1080. In other words, this soft-
ware system has more possible combinations to be tested than the universe has atoms.
 Knowing that testing everything is not possible, we have to choose (or prioritize)
what to test. This is why I emphasize the need for effective tests. The book discusses tech-
niques that will help you identify the relevant test cases. 
1.3.2
Knowing when to stop testing
Prioritizing which tests to engineer is difficult. Creating too few tests may leave us with
a software system that does not behave as intended (that is, it’s full of bugs). On the
other hand, creating test after test without proper consideration can lead to ineffec-
tive tests (and cost time and money). As I said before, our goal should always be to
maximize the number of bugs found while minimizing the resources we spend on
finding those bugs. To that aim, I will discuss different adequacy criteria that will help
you decide when to stop testing. 
1.3.3
Variability is important (the pesticide paradox)
There is no silver bullet in software testing. In other words, there is no single testing
technique that you can always apply to find all possible bugs. Different testing tech-
niques help reveal different bugs. If you use only a single technique, you may find all
the bugs you can with that technique and no more.
 A more concrete example is a team that relies solely on unit testing techniques.
The team may find all the bugs that can be captured at the unit test level, but they may
miss bugs that only occur at the integration level.
 This is known as the pesticide paradox: every method you use to prevent or find bugs
leaves a residue of subtler bugs against which those methods are ineffectual. Testers
must use different testing strategies to minimize the number of bugs left in the soft-
ware. When studying the various testing strategies presented in this book, keep in
mind that combining them all is probably a wise decision. 
1.3.4
Bugs happen in some places more than others
As I said earlier, given that exhaustive testing is impossible, software testers have to pri-
oritize the tests they perform. When prioritizing test cases, note that bugs are not uni-
formly distributed. Empirically, our community has observed that some components
present more bugs than others. For example, a Payment module may require more
rigorous testing than a Marketing module.
 As a real-world example, take Schröter and colleagues (2006), who studied bugs in
the Eclipse projects. They observed that 71% of files that imported compiler packages
had to be fixed later. In other words, such files were more prone to defects than the



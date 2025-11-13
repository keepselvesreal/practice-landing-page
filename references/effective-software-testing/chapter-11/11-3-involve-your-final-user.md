# 11.3 Involve your final user (pp.278-278)

---
**Page 278**

278
CHAPTER 11
Wrapping up the book
 I am betting all my chips on intelligent testing. I do not talk much about it in this
book, although it appears in figure 11.1. Intelligent testing is all about having comput-
ers explore software systems for us. In this book, we automated the process of test exe-
cution. Test case engineering—that is, thinking of good tests—was a human activity.
Intelligent testing systems propose test cases for us.
 The idea is no longer novel among academics. There are many interesting intelli-
gent testing techniques, some of which are mature enough to be deployed into pro-
duction. Facebook, for example, has deployed Sapienz, a tool that uses search-based
algorithms that automatically explore mobile apps, looking for crashes. And Google
deploys fuzz testing (generating unexpected inputs to programs to see if they crash)
on a large scale to identify bugs in open source systems. And the beauty of the
research is that these tools are not randomly generating input data: they are getting
smarter and smarter.
 If you want to play with automated test case generation, try EvoSuite for Java
(www.evosuite.org). EvoSuite receives a class as input and produces a set of JUnit tests
that often achieve 100% branch coverage. It is awe-inspiring. I am hoping the big soft-
ware development companies of this world will catch up with this idea and build more
production-ready tools. 
11.3
Involve your final user
This book focuses on verification. Verification ensures that the code works as we
expect. Another angle to consider is validation: whether the software does what the
user wants or needs. Delivering software that brings the most value is as essential as
delivering software that works. Be sure you have mechanisms to ensure that you are
building the right software in your pipeline. 
11.4
Unit testing is hard in practice
I have a clear position regarding unit testing versus integration testing: you should do
as much unit testing as possible and leave integration testing for the parts of the sys-
tem that need it. For that to happen, you need code that is easily tested and designed
with testability in mind. However, most readers of this book are not in such a situation.
Software systems are rarely designed this way.
 When you write new pieces of code that you have more control over, be sure you
code in a unit-testable way. This means integrating the new code with hard-to-test
legacy code. I have a very simple suggestion that works in most cases. Imagine that
you need to add new behavior to a legacy class. Instead of coding the behavior in
this class, create a new class, put the new behavior in it, and unit-test it. Then, in the
legacy class, instantiate the new class and call the method. This way, you avoid the
hassle of writing a test for a class that is impossible to test. The following listing
shows an example.
 
 



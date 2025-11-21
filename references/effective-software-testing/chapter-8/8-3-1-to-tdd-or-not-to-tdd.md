# 8.3.1 To TDD or not to TDD? (pp.208-209)

---
**Page 208**

208
CHAPTER 8
Test-driven development
Feedback about design—The test code is often the first client of the class or com-
ponent we are developing. A test method instantiates the class under test,
invokes a method passing all its required parameters, and asserts that the
method produces the expected results. If this is hard to do, perhaps there is a
better way to design the class. When doing TDD, these problems arise earlier in
the development of the feature. And the earlier we observe such issues, the
cheaper it is to fix them.
NOTE
TDD shows its advantages best in more complicated problems. I sug-
gest watching James Shore’s YouTube playlist on TDD (2014), where he TDDs
an entire software system. I also recommend Freeman and Pryce’s book Grow-
ing Object-Oriented Systems Guided by Tests (2009). They also TDD an entire system,
and they discuss in depth how they use tests to guide their design decisions.
8.3
TDD in the real world
This section discusses the most common questions and discussions around TDD.
Some developers love TDD and defend its use fiercely; others recommend not
using it.
 As always, software engineering practices are not silver bullets. The reflections I
share in this section are personal and not based on scientific evidence. The best way to
see if TDD is beneficial for you is to try it!
8.3.1
To TDD or not to TDD?
Skeptical readers may be thinking, “I can get the same benefits without doing TDD. I
can think more about my requirements, force myself to only implement what is
needed, and consider the testability of my class from the beginning. I do not need to
write tests for that!” That is true. But I appreciate TDD because it gives me a rhythm to
follow. Finding the next-simplest feature, writing a test for it, implementing nothing
more than what is needed, and reflecting on what I did gives me a pace that I can fully
control. TDD helps me avoid infinite loops of confusion and frustration.
 The more defined development cycle also reminds me to review my code often.
The TDD cycle offers a natural moment to reflect: as soon as the test passes. When
all my tests are green, I consider whether there is anything to improve in the cur-
rent code.
 Designing classes is one of the most challenging tasks of a software engineer. I
appreciate the TDD cycle because it forces me to use the code I am developing from
the very beginning. The perception I have about the class I am designing is often dif-
ferent from my perception when I try to use the class. I can combine both of these
perceptions and make the best decision about how to model the class.
 If you write the tests after the code, and not before, as in TDD, the challenge is
making sure the time between writing code and testing is small enough to provide
developers with timely feedback. Don’t write code for an entire day and then start test-
ing—that may be too late.


---
**Page 209**

209
TDD in the real world
8.3.2
TDD 100% of the time?
Should we always use TDD? My answer is a pragmatic “no.” I do a lot of TDD, but I do
not use TDD 100% of the time. It depends on how much I need to learn about the
feature I am implementing:
I use TDD when I don’t have a clear idea of how to design, architect, or imple-
ment a specific requirement. In such cases, I like to go slowly and use my tests
to experiment with different possibilities. If I am working on a problem I
know well, and I already know the best way to solve the problem, I do not
mind skipping a few cycles.
I use TDD when dealing with a complex problem or a problem I lack the
expertise to solve. Whenever I face a challenging implementation, TDD helps
me take a step back and learn about the requirements as I go by writing very
small tests.
I do not use TDD when there is nothing to be learned in the process. If I already
know the problem and how to best solve it, I am comfortable coding the solu-
tion directly. (Even if I do not use TDD, I always write tests promptly. I never
leave it until the end of the day or the end of the sprint. I code the production
code, and then I code the test code. And if I have trouble, I take a step back and
slow down.)
TDD creates opportunities for me to learn more about the code I am writing from an
implementation point of view (does it do what it needs to do?) as well as from a design
point of view (is it structured in a way that I want?). But for some complex features, it’s
difficult even to determine what the first test should look like; in those cases, I do not
use TDD.
 We need ways to stop and think about what we are doing. TDD is a perfect
approach for that purpose, but not the only one. Deciding when to use TDD comes
with experience. You will quickly learn what works best for you. 
8.3.3
Does TDD work for all types of applications and domains?
TDD works for most types of applications and domains. There are even books about
using it for embedded systems, where things are naturally more challenging, such as
Grenning’s book Test Driven Development for Embedded C (2011). If you can write auto-
mated tests for your application, you can do TDD. 
8.3.4
What does the research say about TDD?
TDD is such a significant part of software development that it is no wonder research-
ers try to assess its effectiveness using scientific methods. Because so many people
treat it as a silver bullet, I strongly believe that you should know what practitioners
think, what I think, and what research currently knows about the subject.
 Research has shown several situations in which TDD can improve class design:



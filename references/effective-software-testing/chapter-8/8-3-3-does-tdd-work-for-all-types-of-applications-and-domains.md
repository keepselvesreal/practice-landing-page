# 8.3.3 Does TDD work for all types of applications and domains? (pp.209-209)

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



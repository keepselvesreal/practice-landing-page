# 8.3.4 What does the research say about TDD? (pp.209-211)

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


---
**Page 210**

210
CHAPTER 8
Test-driven development
Janzen (2005) showed that TDD practitioners, compared to non-TDDers, pro-
duced less-complex algorithms and test suites that covered more.
Janzen and Saiedian (2006) showed that the code produced using TDD made
better use of object-oriented concepts, and responsibilities were better distrib-
uted into different classes. In contrast, other teams produced more proce-
dural code.
George and Williams (2003) showed that although TDD can initially reduce the
productivity of inexperienced developers, 92% of the developers in a qualitative
analysis thought that TDD helped improve code quality.
Dogša and Baticˇ (2011) also found an improvement in class design when using
TDD. According to the authors, the improvement resulted from the simplicity
TDD adds to the process.
Erdogmus et al. (2005) used an experiment with 24 undergraduate students to
show that TDD increased their productivity but did not change the quality of
the produced code.
Nagappan and colleagues (2008) performed three case studies at Microsoft and
showed that the pre-release defect density of projects that were TDD’d
decreased 40 to 90% in comparison to projects that did not do TDD.
Fucci et al. (2016) argue that the important aspect is writing tests (before or after).
Gerosa and I (2015) have made similar observations after interviewing many TDD
practitioners. This is also the perception of practitioners. To quote Michael Feathers
(2008), “That’s the magic, and it’s why unit testing works also. When you write unit
tests, TDD-style or after your development, you scrutinize, you think, and often you
prevent problems without even encountering a test failure.”
 However, other academic studies show inconclusive results for TDD:
Müeller and Hagner (2002), after an experiment with 19 students taking a one-
semester graduate course on extreme programming, observed that test-first did
not accelerate implementation compared to traditional approaches. The code
written with TDD was also not more reliable.
Siniaalto and Abrahamsson (2007) compared five small-scale software proj-
ects using different code metrics and showed that the benefits of TDD were
not clear.
Shull and colleagues (2010), after summarizing the findings of 14 papers on
TDD, concluded that TDD shows no consistent effect on internal code quality.
This paper is easy to read, and I recommend that you look at it.
As an academic who has read most of the work on this topic, I find that many of these
studies—both those that show positive effects and those that do not—are not perfect.
Some use students, who are not experts in software development or TDD. Others use
toy projects without specific room for TDD to demonstrate its benefits. And some use
code metrics such as coupling and cohesion that only partially measure code quality.
Of course, designing experiments to measure the benefits of a software engineering


---
**Page 211**

211
TDD in the real world
practice is challenging, and the academic community is still trying to find the best way
to do it.
 More recent papers explore the idea that TDD’s effects may be due not to the
“write the tests first” aspect but rather to taking baby steps toward the final goal. Fucci
et al. (2016) argue that “the claimed benefits of TDD may not be due to its distinctive
test-first dynamic, but rather due to the fact that TDD-like processes encourage fine-
grained, steady steps that improve focus and flow.”
 I suggest that you give TDD a chance. See if it fits your way of working and your
programming style. You may decide to adopt it full-time (like many of my colleagues)
or only in a few situations (like me), or you may choose never to do it (also like many
of my colleagues). It is up to you. 
8.3.5
Other schools of TDD
TDD does not tell you how to start or what tests to write. This flexibility gave rise to
various different schools of TDD. If you are familiar with TDD, you may have heard
of the London school of TDD, mockist vs. classicist TDD, and outside-in TDD. This
section summarizes their differences and points you to other material if you want to
learn more.
 In the classicist school of TDD (or the Detroit school of TDD, or inside-out TDD), devel-
opers start their TDD cycles with the different units that will compose the overall fea-
ture. More often than not, classicist TDDers begin with the entities that hold the main
business rules; they slowly work toward the outside of the feature and connect these
entities to, say, controllers, UIs, and web services. In other words, classicists go from
the inside (entities and business rules) to the outside (interface with the user).
 Classicists also avoid mocks as much as possible. For example, when implementing a
business rule that would require the interaction of two or more other classes, classicists
would focus on testing the entire behavior at once (all the classes working together)
without mocking dependencies or making sure to test the units in a fully isolated man-
ner. Classicists argue that mocks reduce the effectiveness of the test suite and make test
suites more fragile. This is the same negative argument we discussed in chapter 6.
 The London school of TDD (or outside-in TDD, or mockist TDD), on the other hand,
prefers to start from the outside (such as the UI or the controller that handles the web
service) and then slowly work toward the units that will handle the functionality. To do
so, they focus on how the different objects will collaborate. And for that to happen in
an outside-in manner, these developers use mocks to explore how the collaboration
will work. They favor testing isolated units.
 Both schools of thought use the test code to learn more about the design of the
code being developed. I like the way Test Double (2018) puts it: “In [the] Detroit
school, if an object is hard to test, then it’s hard to use; in [the] London school, if a
dependency is hard to mock, then it’s hard to use for the object that’ll be using it.”
 My style is a mixture of both schools. I start from the inside, coding entities and
business rules, and then slowly work to the outside, making the external layers call



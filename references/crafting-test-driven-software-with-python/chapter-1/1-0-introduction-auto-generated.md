# 1.0 Introduction [auto-generated] (pp.6-7)

---
**Page 6**

1
Getting Started with Software
Testing
Many think that the big step from "coding" to "software engineering" is made by having
elegant architectures, well-defined execution plans, and software that moves big
companies' processes. This mostly comes from our vision of the classic industrial product
development world, where planning mostly mattered more than execution, because the
execution was moved forward by an assembly line and software was an expensive internal
utility that only big companies could afford
As software development science moved forward and matured, it became clear that classic
industrial best practices weren't always a great fit for it. The reason being that every
software product was very different, due to the technologies involved, the speed at which
those technologies evolve, and in the end the fact that different software had to do totally
different things. Thus the idea developed that software development was more similar to
craftsmanship than to industry.
If you embrace that it's very hard, and not very effective, to try to eliminate uncertainty and
issues with tons of preparation work due to the very nature of software itself, it becomes
evident that the most important part of software development is detecting defects and
ensuring it achieves the expected goals. Those two things are usually mostly done by
having tests and a fitness function that can verify the software does what we really mean it
to – founding pieces of the whole Software Quality Control discipline, which is what this
chapter will introduce and, in practice, what this book is all about.
In this chapter, we will go through testing software products and the best practices in
quality control. We will also introduce automatic tests and how they are superseding
manual testing. We will take a look at what Test-Driven Development (TDD) is and how
to apply it in Python, giving some guidance on how to distinguish between the various
categories of tests, how to implement them, and how to get the right balance between test
efficacy and test cost.


---
**Page 7**

Getting Started with Software Testing
Chapter 1
[ 7 ]
In this chapter, we will cover the following:
Introducing software testing and quality control
Introducing automatic tests and test suites
Introducing test-driven development and unit tests
Understanding integration and functional tests
Understanding the testing pyramid and trophy
Technical requirements
A working Python interpreter is all that's needed.
The examples have been written in Python 3.7 but should work in most modern Python
versions.
You can find the code files present in this chapter on GitHub at https:/​/​github.​com/
PacktPublishing/​Crafting-​Test-​Driven-​Software-​with-​Python/​tree/​main/​Chapter01.
Introducing software testing and quality
control
From the early days, it was clear that like any other machine, software needed a way to 
verify it was working properly and was built with no defects.
Software development processes have been heavily inspired by manufacturing industry
standards, and early on, testing and quality control were introduced into the product
development life cycle. So software companies frequently have a quality assurance team
that focuses on setting up processes to guarantee robust software and track results.
Those processes usually include a quality control process where the quality of the built
artifact is assessed before it can be considered ready for users.
The quality control process usually achieves such confidence through the execution of a test
plan. This is usually a checklist that a dedicated team goes through during the various
phases of production to ensure the software behaves as expected.



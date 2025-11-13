# 1.6.0 Introduction [auto-generated] (pp.26-27)

---
**Page 26**

Getting Started with Software Testing
Chapter 1
[ 26 ]
How you do that can easily involve the same exact technologies and it's just a matter of
different goals. Properly covering the behavior of your software with the right kind of tests
can be the difference between buggy software and reliable software. That's why there has
been a long debate about how to structure test suites, leading to the testing pyramid and
the testing trophy as the most widespread models of test distribution.
Understanding the testing pyramid and
trophy
Given the need to provide different kinds of tests – unit, integration, and E2E as each one of
them has different benefits and costs, the next immediate question is how do we get the
right balance?
Each kind of test comes with a benefit and a cost, so it's a matter of finding where we get
the best return on investment:
E2E tests verify the real experience of what the user faces. They are, in theory, the
most realistic kind of tests and can detect problems such as incompatibilities with
specific platforms (for example, browsers) and exercise our system as a whole.
But when something goes wrong, it is hard to spot where the problem lies. They
are very slow and tend to be flaky (failing for reasons unrelated to our software,
such as network conditions).
Integration tests usually provide a reasonable guarantee that the software is
doing what it is expected to do and are fairly robust to internal implementation
changes, requiring less frequent refactoring when the internals of the software
change. But they can still get very slow if your system involves writes to database
services, the rendering of page templates, routing HTTP requests, and generally
slow parts. And when something goes wrong, we might have to go through tens
of layers before being able to spot where the problem is.
Unit tests can be very fast (especially when talking of solitary units) and provide
very pinpointed information about where problems are. But they can't always 
guarantee that the software as a whole does what it's expected to do and can
make changing implementation details expensive because a change to internals
that don't impact the software behavior might require changing tens of unit tests.
Each of them has its own pros and cons, and the development community has long argued
how to get the right balance.
The two primary models that have emerged are the testing pyramid and the testing trophy,
named after their shapes.


---
**Page 27**

Getting Started with Software Testing
Chapter 1
[ 27 ]
The testing pyramid
The testing pyramid originates from Mike Cohn's Succeeding with Agile book, where the two
rules of thumb are "Write test with different granularities" (so you should have unit,
integration, E2E, and so on...) and "the more you get high level, the less you should test" (so you
should have tons of unit tests, and a few E2E tests).
While different people will argue about which different layers are contained within it, the
testing pyramid can be simplified to look like this:
Figure 1.1 – Testing pyramid
The tip of the pyramid is narrow, thus meaning we have fewer of those tests, while the base
is wider, meaning we should mostly cover code with those kinds of tests. So, as we move
down through the layers, the lower we get, the more tests we should have.
The idea is that as unit tests are fast to run and expose pinpointed issues early on, you
should have a lot of them and shrink the number of tests as they move to higher layers and
thus get slower and vaguer about what's broken.
The testing pyramid is probably the most widespread practice for organizing tests and
usually pairs well with test-driven development as unit tests are the founding tool for the
TDD process.



# 1.6.1 The testing pyramid (pp.27-28)

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


---
**Page 28**

Getting Started with Software Testing
Chapter 1
[ 28 ]
The other most widespread model is the testing trophy, which instead emphasizes
integration tests.
The testing trophy
The testing trophy originates from a phrase by Guillermo Rauch, the author of Socket.io
and many other famous JavaScript-based technologies. Guillermo stated that developers
should "Write tests. Not too many. Mostly integration."
Like Mike Cohn, he clearly states that tests are the foundation of any effective software
development practice, but he argues that they have a diminishing return and thus it's
important to find the sweet spot where you get the best return on the time spent writing
tests.
That sweet spot is expected to live in integration tests because you usually need fewer of
them to spot real problems, they are not too bound to implementation details, and they are
still fast enough that you can afford to write a few of them.
So the testing trophy will look like this:
Figure 1.2 – Testing trophy



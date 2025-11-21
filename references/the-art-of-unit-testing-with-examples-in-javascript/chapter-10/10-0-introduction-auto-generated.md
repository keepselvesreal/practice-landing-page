# 10.0 Introduction [auto-generated] (pp.194-195)

---
**Page 194**

194
Developing
a testing strategy
Unit tests represent just one of the types of tests you could and should write. In this
chapter, we’ll discuss how unit testing fits into an organizational testing strategy. As
soon as we start to look at other types of tests, we start asking some really important
questions:
At what level do we want to test various features? (UI, backend, API, unit,
etc.)
How do we decide at which level to test a feature? Do we test it multiple times
on many levels?
Should we have more functional end-to-end tests or more unit tests?
This chapter covers
Testing level pros and cons
Common antipatterns in test levels
The test recipe strategy
Delivery-blocking and non-blocking tests
Delivery vs. discovery pipelines
Test parallelization


---
**Page 195**

195
10.1
Common test types and levels
How can we optimize the speed of tests without sacrificing trust in them?
Who should write each type of test? 
The answers to these questions, and many more, are what I’d call a testing strategy. 
 The first step in our journey is to frame the scope of the testing strategy in terms of
test types. 
10.1
Common test types and levels
Different industries might have different test types and levels. Figure 10.1, which we
first discussed in chapter 7, is a rather generic set of test types that I feel fits 90% of the
organizations I consult with, if not more. The higher the level of the tests, the more
real dependencies they use, which gives us confidence in the overall system’s correct-
ness. The downside is that such tests are slower and flakier.
Most speed
• Easier to maintain
• Easier to write
• Faster feedback loop
Most conﬁdence
• Harder to maintain
• Harder to write
• Slower feedback loop
Conﬁdence
E2E/UI system tests
E2E/UI isolated tests
API tests (out of process)
Integration tests (in memory)
Component tests (in memory)
Unit tests (in memory)
Figure 10.1
Common software test levels 



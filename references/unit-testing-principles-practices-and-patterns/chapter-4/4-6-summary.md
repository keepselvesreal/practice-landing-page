# 4.6 Summary (pp.90-92)

---
**Page 90**

90
CHAPTER 4
The four pillars of a good unit test
back to a behavior that is meaningful to a business person, which is a strong sign that
these tests are fragile and don’t add much value. Black-box testing provides the oppo-
site set of pros and cons (table 4.1).
As you may remember from section 4.4.5, you can’t compromise on resistance to refac-
toring: a test either possesses resistance to refactoring or it doesn’t. Therefore, choose black-
box testing over white-box testing by default. Make all tests—be they unit, integration, or
end-to-end—view the system as a black box and verify behavior meaningful to the
problem domain. If you can’t trace a test back to a business requirement, it’s an indi-
cation of the test’s brittleness. Either restructure or delete this test; don’t let it into the
suite as-is. The only exception is when the test covers utility code with high algorith-
mic complexity (more on this in chapter 7).
 Note that even though black-box testing is preferable when writing tests, you can
still use the white-box method when analyzing the tests. Use code coverage tools to see which
code branches are not exercised, but then turn around and test them as if you know nothing about
the code’s internal structure. Such a combination of the white-box and black-box meth-
ods works best. 
Summary
A good unit test has four foundational attributes that you can use to analyze any
automated test, whether unit, integration, or end-to-end:
– Protection against regressions
– Resistance to refactoring
– Fast feedback
– Maintainability
Protection against regressions is a measure of how good the test is at indicating the
presence of bugs (regressions). The more code the test executes (both your
code and the code of libraries and frameworks used in the project), the higher
the chance this test will reveal a bug.
Resistance to refactoring is the degree to which a test can sustain application code
refactoring without producing a false positive.
A false positive is a false alarm—a result indicating that the test fails, whereas
the functionality it covers works as intended. False positives can have a devastat-
ing effect on the test suite:
– They dilute your ability and willingness to react to problems in code, because
you get accustomed to false alarms and stop paying attention to them.
Table 4.1
The pros and cons of white-box and black-box testing
Protection against regressions
Resistance to refactoring
White-box testing
Good
Bad
Black-box testing
Bad
Good


---
**Page 91**

91
Summary
– They diminish your perception of tests as a reliable safety net and lead to los-
ing trust in the test suite.
False positives are a result of tight coupling between tests and the internal imple-
mentation details of the system under test. To avoid such coupling, the test
must verify the end result the SUT produces, not the steps it took to do that.
Protection against regressions and resistance to refactoring contribute to test accuracy.
A test is accurate insofar as it generates a strong signal (is capable of finding
bugs, the sphere of protection against regressions) with as little noise (false posi-
tives) as possible (the sphere of resistance to refactoring).
False positives don’t have as much of a negative effect in the beginning of the
project, but they become increasingly important as the project grows: as import-
ant as false negatives (unnoticed bugs).
Fast feedback is a measure of how quickly the test executes.
Maintainability consists of two components:
– How hard it is to understand the test. The smaller the test, the more read-
able it is.
– How hard it is to run the test. The fewer out-of-process dependencies the test
reaches out to, the easier it is to keep them operational.
A test’s value estimate is the product of scores the test gets in each of the four attri-
butes. If the test gets zero in one of the attributes, its value turns to zero as well.
It’s impossible to create a test that gets the maximum score in all four attri-
butes, because the first three—protection against regressions, resistance to refactor-
ing, and fast feedback—are mutually exclusive. The test can only maximize two
out of the three.
Resistance to refactoring is non-negotiable because whether a test possess this attri-
bute is mostly a binary choice: the test either has resistance to refactoring or it
doesn’t. The trade-off between the attributes comes down to the choice
between protection against regressions and fast feedback.
The Test Pyramid advocates for a certain ratio of unit, integration, and end-to-
end tests: end-to-end tests should be in the minority, unit tests in the majority,
and integration tests somewhere in the middle.
Different types of tests in the pyramid make different choices between fast feed-
back and protection against regressions. End-to-end tests favor protection against
regressions, while unit tests favor fast feedback.
Use the black-box testing method when writing tests. Use the white-box method
when analyzing the tests.


---
**Page 92**

92
Mocks and test fragility
Chapter 4 introduced a frame of reference that you can use to analyze specific tests
and unit testing approaches. In this chapter, you’ll see that frame of reference in
action; we’ll use it to dissect the topic of mocks.
 The use of mocks in tests is a controversial subject. Some people argue that
mocks are a great tool and apply them in most of their tests. Others claim that mocks
lead to test fragility and try not to use them at all. As the saying goes, the truth lies
somewhere in between. In this chapter, I’ll show that, indeed, mocks often result in
fragile tests—tests that lack the metric of resistance to refactoring. But there are still
cases where mocking is applicable and even preferable.
This chapter covers
Differentiating mocks from stubs
Defining observable behavior and implementation 
details
Understanding the relationship between mocks 
and test fragility
Using mocks without compromising resistance 
to refactoring



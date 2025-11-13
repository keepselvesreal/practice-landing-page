# 3.5 Handling loops and similar constructs (pp.75-75)

---
**Page 75**

75
Criteria subsumption, and choosing a criterion
 If we were to pick T1 or T5, we would have to include the other as well, as they are
opposites. Therefore, they are unnecessarily increasing the number of tests. To ensure
that our test suite contains at most four test cases, we can add either T6 or T7, as their
opposites (T2 and T3) are already included in our test cases. I picked T6 randomly.
(You can have more than one set of tests that achieves 100% MC/DC, and all solutions
are equally acceptable.)
 Therefore, the tests we need for 100% MC/DC coverage are {T2, T3, T4, T6}.
These are the only four tests we need—certainly cheaper than the eight tests we would
need for path coverage. Now that we know which tests we need to implement, we can
automate them.
NOTE
I have a video on YouTube that explains MC/DC visually: www.youtube
.com/watch?v=HzmnCVaICQ4. 
3.5
Handling loops and similar constructs
You may wonder what to do in the case of loops, such as for and while. The code
block inside the loop may be executed different numbers of times, making testing
more complicated.
 Think of a while(true) loop, which can be non-terminating. To be rigorous, we
would have to test the program with the loop block executed one time, two times,
three times, and so on. Or imagine a for(i = 0; i < 10; i++) loop with a break inside
the body. We would have to test what happened if the loop body executed up to 10
times. How can we handle a long-lasting loop (that runs for many iterations) or an
unbounded loop (that is executed an unknown number of times)?
 Given that exhaustive testing is impossible, testers often rely on the loop
boundary adequacy criterion to decide when to stop testing a loop. A test suite satisfies
this criterion if and only if for every loop
There is a test case that exercises the loop zero times.
There is a test case that exercises the loop once.
There is a test case that exercises the loop multiple times.
Pragmatically speaking, my experience shows that the main challenge comes when
devising the test case for the loop being executed multiple times. Should the test case
force the loop to iterate 2, 5, or 10 times? This decision requires a good understand-
ing of the program and its requirement. With optimal understanding of the specs, you
should be able to devise good tests for the loop. Do not be afraid to create two or
more tests for the “multiple times” case. Do whatever you need to do to ensure that
the loop works as expected. 
3.6
Criteria subsumption, and choosing a criterion
You may have noticed that some of the criteria we have discussed are more rigorous
than others. For example, a single test is enough to achieve 100% line coverage, but two
tests are needed for 100% branch coverage. Some strategies subsume other strategies.



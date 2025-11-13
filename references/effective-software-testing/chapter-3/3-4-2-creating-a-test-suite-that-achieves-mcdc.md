# 3.4.2 Creating a test suite that achieves MC/DC (pp.73-75)

---
**Page 73**

73
Complex conditions and the MC/DC coverage criterion
3.4.2
Creating a test suite that achieves MC/DC
The question is how to (mechanically) select such test cases. Let’s continue using the
same if statement from the CountWords program (from listing 3.4). The statement
takes three booleans as input: (1) whether the current character is a letter and
whether this letter is (2) “s” or (3) “r”. Generically, this is the same as the A && (B || C)
example we just discussed.
 To test this program, we first use a truth table to see all the combinations and their
outcomes. In this case, we have three decisions, and 23 = 8. Therefore, we have tests T1
to T8, as listed in table 3.1.
Our goal is to apply the MC/DC criterion to these test cases and select N + 1 tests,
which in this case means 3 + 1 = 4. To determine which four tests satisfy MC/DC, we
need to go condition by condition, beginning by selecting the pairs of combinations
(or tests) for the isLetter part of the condition:
For T1, isLetter, last == s, and last == r are all true, and decision (that is,
the outcome of the entire boolean expression) is also true. We now look for
another test in the table where the value of isLetter is the opposite of the
value in T1 but the other values (last == s and last == r) are the same. This
means look for a test where isLetter is false, last == s is true, last == r is
true, and decision is false. This combination appears in T5.
Thus, we have found a pair of tests, T1 and T5 (an independence pair), where
isLetter is the only parameter that is different and the outcome (decision)
changes. In other words, for this pair of tests, isLetter independently influences
the outcome (decision). Let’s keep the pair {T1, T5} in our list of test cases.
We could stop here and move to the next variable. But finding all indepen-
dence pairs for isLetter may help us reduce the final number of test cases, as
you will see. So let’s continue and look at the next test. In T2, isLetter is true,
Table 3.1
Truth table for the if expression from the CountWords program
Test case
isLetter
last == s
last == r
decision
T1
true
true
true
true
T2
true
true
false
true
T3
true
false
true
true
T4
true
false
false
false
T5
false
true
true
false
T6
false
true
false
false
T7
false
false
true
false
T8
false
false
false
false


---
**Page 74**

74
CHAPTER 3
Structural testing and code coverage
last == s is true, last == r is false, and decision is true. We repeat the pro-
cess and search for a test where isLetter is the opposite of the value in T2 but
last == s and last == r remain the same. We find this combination in T6.
We have found another pair of tests, T2 and T6, where isLetter is the only
parameter that is different and the outcome (decision) also changes, which we
also add to our list of test cases.
We repeat the process for T3 (isLetter is true, last == s is false, last == r is
true) and find that the isLetter parameter in T7 (isLetter is false, last ==
s is false, last == r is true) is the opposite of the value in T3 and changes the
outcome (decision).
The pair for T4 (isLetter is true, last == s is false, last == r is false) is T8
(isLetter is false, last == s is false, last == r is false). The outcome of
both tests is the same (decision is false), which means the pair {T4, T8} does
not show how isLetter can independently affect the overall outcome.
We do not find another new or suitable pair when repeating the process for T5, T6,
T7, and T8, so we move on from the isLetter parameter to the last == s parameter.
We repeat the same process, but now we search for the opposite value of parameter
last == s, while isLetter and last == r stay the same:
For T1 (isLetter is true, last == s is true, last == r is true), we search for a
test where isLetter is true, last == s is false, last == r is true). This appears
to be the case in T3. However, the outcome is the same for both test cases.
Therefore, {T1, T3} does not show how the last == s parameter independently
affects the outcome.
After repeating all the steps for the other tests, we find that only {T2, T4} have
different values for the last == s parameter where the outcome also changes.
Finally, we move to the last == r parameter. As with the last == s parameter, one pair
of combinations works: {T3, T4}. I highly recommend carrying out the entire process
yourself to get a feel for how it works.
 We now have all the pairs for each parameter:

isLetter: {1, 5}, {2, 6}, {3, 7}

last == s: {2, 4}

last == r: {3, 4}
Having a single independence pair per variable (isLetter, last == s, and last == r)
is enough. We want to minimize the total number of tests, and we know we can
achieve this with N + 1 tests. We do not have any choices with conditions last == s and
last == r, as we found only one pair of tests for each parameter. This means we need
tests T2, T3, and T4. Finally, we need to find the appropriate pair of tests for isLetter.
Note that any of the test pairs (T1-T5, T2-T6, or T3-T7) would work. However, we want
to reduce the total number of tests in the test suite (and again, we know we only need
four in this case).


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



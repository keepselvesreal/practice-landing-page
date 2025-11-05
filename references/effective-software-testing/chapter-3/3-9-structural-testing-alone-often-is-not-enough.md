# 3.9 Structural testing alone often is not enough (pp.82-84)

---
**Page 82**

82
CHAPTER 3
Structural testing and code coverage
@Test
void sameInstance() {
  String str = "sometext";
  assertThat(leftPad(str, 5, "-")).isSameAs(str);
}
We are now much more confident that our test suite covers all the critical behavior of
the program. Structural testing and code coverage helped us identify parts of the code
that we did not test (or partitions we missed) during our specification-based testing—
and that is what structural testing is all about. 
3.8
Boundary testing and structural testing
The most challenging part of specification-based testing is identifying boundaries.
They are tricky to find, given the way we write specifications. Luckily, they are much
easier to find in source code, given how precise code has to be. All the boundary test-
ing ideas we discussed in the previous chapter apply here.
 The idea of identifying and testing on and off points fits nicely in structural testing.
For example, we can analyze the if statements in the leftPad program:

if (pads <= 0)—The on point is 0 and evaluates the expression to true. The off
point is the nearest point to the on point that makes the expression evaluate to
false. In this case, given that pads is an integer, the nearest point is 1.

if (pads == padLen)—The on point is padLen. Given the equality and that padLen
is an integer, we have two off points: one that happens when pads == padLen - 1
and another that happens when pads = padLen + 1.

if (pads < padLen)—The on point is again padLen. The on point evaluates the
expression to false. The off point is, therefore, pads == padLen - 1.
As a tester, you may want to use this information to see whether you can augment your
test suite.
 We discussed the loop boundary criterion earlier, which helps us try different pos-
sible boundaries. If a loop has a less conventional, more complicated expression, con-
sider applying on and off analysis there as well. 
3.9
Structural testing alone often is not enough
If code is the source of all truth, why can’t we just do structural testing? This is a very
interesting question. Test suites derived only with structural testing can be reasonably
effective, but they may not be strong enough. Let’s look at an example (see the
“counting clumps” problem, inspired by a CodingBat assignment: https://codingbat
.com/prob/p193817):
 
Listing 3.8
Another extra test for leftPad


---
**Page 83**

83
Structural testing alone often is not enough
The program should count the number of clumps in an array. A clump is a
sequence of the same element with a length of at least 2.

nums—The array for which to count the clumps. The array must be non-
null and length > 0; the program returns 0 if any pre-condition is violated.
The program returns the number of clumps in the array.
The following listing shows an implementation.
public static int countClumps(int[] nums) {
  if (nums == null || nums.length == 0) {   
    return 0;
  }
  int count = 0;
  int prev = nums[0];
  boolean inClump = false;
  for (int i = 1; i < nums.length; i++) {
    if (nums[i] == prev && !inClump) {   
      inClump = true;
      count += 1;
    }
    if (nums[i] != prev) {   
      prev = nums[i];
      inClump = false;
    }
  }
  return count;
}
Suppose we decide not to look at the requirements. We want to achieve, say, 100%
branch coverage. Three tests are enough to do that (T1–T3). Maybe we also want to
do some extra boundary testing and decide to exercise the loop, iterating a single
time (T4):
T1: an empty array
T2: a null array
T3: an array with a single clump of three elements in the middle (for example,
[1,2,2,2,1])
T4: an array with a single element
To check that for yourself, write down these three tests as (JUnit) automated test cases
and run your favorite code coverage tool as in the following.
@ParameterizedTest
@MethodSource("generator")
void testClumps(int[] nums, int expectedNoOfClumps) {
  assertThat(Clumps.countClumps(nums))
Listing 3.9
Implementing the code clumps requirement
Listing 3.10
100% branch coverage for the clump-counting problem
If null or empty 
(pre-condition), 
return 0 right away.
If the current number is the 
same as the previous number, 
we have identified a clump.
If the current number 
differs from the previous 
one, we are not in a clump.


---
**Page 84**

84
CHAPTER 3
Structural testing and code coverage
      .isEqualTo(expectedNoOfClumps);
}
static Stream<Arguments> generator() {   
  return Stream.of(
    of(new int[]{}, 0), // empty
    of(null, 0), // null
    of(new int[]{1,2,2,2,1}, 1), // one clump
    of(new int[]{1}, 0) // one element
  );
}
This test suite is reasonable and exercises the main behavior of the program, but note
how weak it is. It achieves 100% branch coverage, but it misses many interesting test
cases. Even without performing systematic specification testing, in a program that
counts clumps, it is natural to try the program with multiple clumps instead of just
one. We could try it with the last clump happening at the last item of the array or with
an array that has a clump starting in the first position. Such specific cases cannot be
captured by pure structural testing guided mainly by coverage. This is yet another rea-
son not to rely blindly on coverage. Structural testing shows its value when combined
with knowledge of the specification. 
3.10
Structural testing in the real world
Now that you have a clear picture of structural testing, the coverage criteria you can
use for guidance, and how to use structural testing in combination with specification-
based testing, let me discuss a few interesting points.
3.10.1 Why do some people hate code coverage?
I find it interesting that some people rage against code coverage. A prevalent opinion
is, “If I write a test case with no assertions, I achieve 100% coverage, but I am not test-
ing anything!” This is true. If your tests have no assertions, they do not test anything,
but the production code is exercised. However, I consider that a flawed argument. It
assumes the very worst (unrealistic) scenario possible. If you are writing test suites with
no assertions, you have bigger problems to take care of before you can enjoy the ben-
efits of structural testing.
 Between the lines, people use such an argument to explain that you should not
look at the coverage number blindly, because it can mislead you. That I fully agree
with. Here, the misconception is how people see code coverage. If code coverage is
only a number you should achieve, you may end up writing less useful test cases and
gaming the metric (something that Bouwers, Visser, and Van Deursen have argued
in 2012).
 I hope this chapter has clarified how structural testing and code coverage should
be used: to augment specification-based testing, quickly identify parts of the code that
are not currently exercised by the test suite, and identify partitions you missed when
The four test 
cases we defined



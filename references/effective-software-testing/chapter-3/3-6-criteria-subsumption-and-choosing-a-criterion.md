# 3.6 Criteria subsumption, and choosing a criterion (pp.75-77)

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


---
**Page 76**

76
CHAPTER 3
Structural testing and code coverage
Formally, a strategy X subsumes strategy Y if all elements that Y exercises are also exer-
cised by X. Figure 3.7 illustrates the relationships among the coverage criteria.
Branch coverage subsumes line coverage, which means 100% branch coverage always
implies 100% line coverage. However, 100% line coverage does not imply 100%
branch coverage. Moreover, 100% condition + branch coverage always implies 100%
branch coverage and 100% line coverage. Following this train of thought, we see that
path coverage subsumes all other criteria. This is logical as path coverage covers all
possible paths of the program. Next, we see that MC/DC is stronger than condition +
branch coverage, as MC/DC ensures the independence of each condition. And condi-
tion + branch coverage subsumes both branch and condition coverage independently.
Finally, all other criteria, except basic condition coverage, subsume line coverage,
which is the weakest criterion in the figure.
 You now understand the trade-offs of choosing one criterion over another. A
weaker criterion may be cheaper and faster to achieve but leave many parts of the
code uncovered. On the other hand, a stronger criterion may cover the code more
rigorously at a higher cost. It is up to you, the developer, to decide which criterion
to use.
NOTE
Basic condition coverage does not necessarily subsume line coverage,
for the same reason we always use condition + branch coverage together. We
can achieve 100% basic condition coverage in a simple if(A || B) by having
two tests, T1={true, false} and T2={false, true}. But both tests make the deci-
sion block true, so the false branch and its lines are not exercised. 
MC/DC
Branch + condition
coverage
Statement/line
coverage
Path coverage
Branch
coverage
Condition
coverage
Arrows indicate the
subsumption relations. This
means if you achieve one,
you achieve the other, too.
Line coverage is our
weakest criterion.
Path coverage is our
strongest criterion
and subsumes all
others.
Figure 3.7
The different coverage criteria and their subsumption relations


---
**Page 77**

77
Specification-based and structural testing: A running example
3.7
Specification-based and structural testing: 
A running example
Let’s try specification-based testing and structural testing together on a real-world exam-
ple: the leftPad() function from Apache Commons Lang (http://mng.bz/zQ2g):
Left-pad a string with a specified string. Pad to a size of size.

str—The string to pad out; may be null.

size—The size to pad to.

padStr—The string to pad with. Null or empty is treated as a single space.
The method returns a left-padded string, the original string if no padding is
necessary, or null if a null string is input.
For example, if we give "abc" as the string input, a dash "-" as the pad string, and 5 as
the size, the program will output "--abc".
 A developer on your team comes up with the implementation in listing 3.5. For
now, suppose you are testing code written by others, so you need to build an under-
standing of the code before you can test it properly. Specification-based testing and
structural testing are applied the same way, regardless of whether you wrote the code.
In later chapters, we discuss test-driven development and how you can use tests to
guide you through implementation.
public static String leftPad(final String str, final int size,
  String padStr) {
  if (str == null) {   
    return null;
  }
  if (padStr==null || padStr.isEmpty()) {   
    padStr = SPACE;
  }
  final int padLen = padStr.length();
  final int strLen = str.length();
  final int pads = size - strLen;
  if (pads <= 0) {          
    // returns original String when possible
    return str;
  }
  if (pads == padLen) {            
    return padStr.concat(str);
  } else if (pads < padLen) {    
    return padStr.substring(0, pads).concat(str);
Listing 3.5
leftPad implementation from the Apache Commons
If the string to pad is 
null, we return null 
right away.
If the pad string is 
null or empty, we 
make it a space.
There is no 
need to pad 
this string.
If the number of characters to 
pad matches the size of the 
pad string, we concatenate it.
If we cannot fit the entire 
pad string, we add only 
the part that fits.



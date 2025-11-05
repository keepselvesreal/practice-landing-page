# 3.10.5 Other coverage criteria (pp.89-90)

---
**Page 89**

89
Structural testing in the real world
For completeness, here are some final remarks about MC/DC. First, in the example in
section 3.1, we apply unique-cause MC/DC criteria: we identify an independence pair
(T1, T2) where only a single condition and the final outcome change between T1 and
T2. That may not be possible in all cases. For example, consider (A && B) || (A && C).
Ideally, we would demonstrate the independence of the first A, B, the second A, and C.
But it is impossible to change the first A and not change the second A. Thus, we can-
not demonstrate the independence of each A in the expression. In such cases, we
allow A to vary, but we fix all other variables (this is called masked MC/DC).
 Second, note that it may not be possible to achieve MC/DC in some expressions,
such as (A and B) or (A and not B). While the independence pairs (TT, FT) would
show the independence of A, there are no pairs that show the independence of B. In
such cases, revisit the expression, as it may have been poorly designed. In this exam-
ple, the expression could be reformulated to simply A.
 Finally, mathematically speaking, N + 1 is the theoretical lower bound for the num-
ber of tests you may need when applying MC/DC. In other words, you may need more
than N + 1 test cases to achieve MC/DC in some expressions. However, the empirical
study by Chilenski (2001) shows that the majority of expressions in practice require
N + 1 tests. This has been my observation, too: N + 1 is most of the times the number
of required test cases. 
3.10.5 Other coverage criteria
Throughout this chapter, we have used the program’s control flow as a way to derive
different tests. Another way of approaching structural testing is to look at the data flow:
examining how the data flows to different parts of the program.
 For example, imagine that a variable is defined, then modified one, two, or three
times in other parts of the program, and then used again later. You may want to
ensure that you exercise all the possible ways this variable is touched. Trying to sum-
marize data-flow coverage in one sentence is unfair, and a lot of energy has been spent
coming up with criteria, but this should give you some intuition about it.
MC/DC in SQLite
A nice story of the benefits of MC/DC was told by Richard Hipp, the creator and pri-
mary developer of SQLite, the most popular embedded database. In the Corecursive
#066 podcast, Richard says, “I had this idea, I’m going to write tests to bring SQLite
up to the quality of 100% MC/DC, and that took a year of 60-hour weeks. That was
hard, hard work. I was putting in 12-hour days every single day. I was getting so tired
of this because with this sort of thing, it’s the old joke of, you get 95% of the func-
tionality with the first 95% of your budget, and the last 5% on the second 95% of your
budget. It’s kind of the same thing. It’s pretty easy to get up to 90 or 95% test cov-
erage. Getting that last 5% is really, really hard, and it took about a year for me to get
there, but once we got to that point, we stopped getting bug reports from Android.”
What a powerful success story of MC/DC.


---
**Page 90**

90
CHAPTER 3
Structural testing and code coverage
 I do not discuss data-flow coverage in this book, but I suggest you read more about
it. Pezzè and Young (2008) give a nice explanation. 
3.10.6 What should not be covered?
We have talked a lot about what to test and cover. Let’s quickly discuss what not to
cover. Achieving 100% coverage may be impossible or not even desirable. For exam-
ple, the code snippet in listing 3.12 returns the full path of a specific directory. The
code may throw a URISyntaxException, which we catch and wrap around a Runtime-
Exception. (For the Java experts, we are converting a checked exception to an
unchecked exception.)
public static String resourceFolder(String path) {
  try {
    return Paths.get(ResourceUtils.class
      .getResource("/").toURI()).toString() + path;
  } catch (URISyntaxException e) {
    throw new RuntimeException(e);
  }
}
To achieve 100% line coverage, we would need to exercise the catch block. For that to
happen, we would have to somehow force the toURI method to throw the exception.
We could use mocks (discussed later in this book), but I cannot see any advantage in
doing that. It is more important to test what would happen to the rest of the system if
resourceFolder threw a RuntimeException. That is much easier to do, as we have
more control over the resourceFolder method than the Java toURI() method.
Therefore, this piece of code it is not worth covering and shows why blindly aiming for
100% coverage makes no sense.
 In Java, in particular, I tend not to write dedicated tests for equals and hashCode
methods or straightforward getters and setters. These are tested implicitly by the tests
that exercise the other methods that use them.
 To close this discussion, I want to reinforce that, for me, all code should be covered
until proven otherwise. I start from the idea that I should have 100% coverage. Then, if I
see that a piece of code does not need to be covered, I make an exception. But be
careful—experience shows that bugs tend to appear in areas you do not cover well. 
3.11
Mutation testing
All the coverage criteria discussed in this chapter consider how much of the produc-
tion code is exercised by a test. What they all miss is whether the assertions that these
tests make are good and strong enough to capture bugs. If we introduce a bug in the
code, even in a line covered by a test, will the test break?
 As mentioned earlier, coverage alone is not enough to determine whether a test
suite is good. We have been thinking about how far our test suite goes to evaluate the
Listing 3.12
A method that does not deserve full coverage



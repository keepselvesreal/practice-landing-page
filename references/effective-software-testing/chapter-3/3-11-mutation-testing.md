# 3.11 Mutation testing (pp.90-93)

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


---
**Page 91**

91
Mutation testing
strength of our test suite. Now let’s think of the test suite’s fault detection capability. How
many bugs can it reveal?
 This is the idea behind mutation testing. In a nutshell, we purposefully insert a bug
in the existing code and check whether the test suite breaks. If it does, that’s a point
for the test suite. If it does not (all tests are green even with the bug in the code), we
have found something to improve in our test suite. We then repeat the process: we
create another buggy version of the problem by changing something else in the code,
and we check whether the test suite captures that bug.
 These buggy versions are mutants of the original, supposedly correct, version of the
program. If the test suite breaks when executed against a mutant, we say that the test
suite kills that mutant. If it does not break, we say that the mutant survives. A test suite
achieves 100% mutation coverage if it kills all possible mutants.
 Mutation testing makes two interesting assumptions. First, the competent programmer
hypothesis assumes that the program is written by a competent programmer and that
the implemented version is either correct or differs from the correct program by a
combination of simple errors. Second, the coupling effect says that a complex bug is
caused by a combination of many small bugs. Therefore, if your test suite can catch
simple bugs, it will also catch the more complex ones.
 Pitest is the most popular open source tool for mutation testing in Java (https://
pitest.org/quickstart/mutators). Here are a few examples of mutators from its manual:
Conditionals boundary—Relational operators such as < and <= are replaced by
other relational operators.
Increment—It replaces i++ with i-- and vice versa.
Invert negatives—It negates variables: for example, i becomes -i.
Math operators—It replaces mathematical operators: for example, a plus
becomes a minus.
True returns—It replaces entire boolean variables with true.
Remove conditionals—It replaces entire if statements with a simple if(true) {…}.
Running Pitest is simple, as it comes with plugins for Maven and Gradle. For example,
I ran it against the LeftPad implementation and tests we wrote earlier; figure 3.11
shows the resulting report. As in a code coverage report, a line’s background color
indicates whether all the mutants were killed by the test suite.
 The next step is to evaluate the surviving mutants. It is very important to analyze
each surviving mutant, as some may not be useful.
 Remember that mutation testing tools do not know your code—they simply mutate
it. This sometimes means they create mutants that are not useful. For example, in the
line that contains int pads = size - strLen, Pitest mutated the size variable to size++.
Our test suite does not catch this bug, but this is not a useful mutant: the size variable is
not used after this line, so incrementing it has no effect on the program.
 You should view mutation testing in the same way as coverage tools: it can augment
the test suite engineered based on the program’s requirements.


---
**Page 92**

92
CHAPTER 3
Structural testing and code coverage
Mutation testing faces various challenges in practice, including the cost. To use muta-
tion testing, we must generate many mutants and execute the whole test suite with
each one. This makes mutation testing quite expensive. Considerable research is ded-
icated to lowering the cost of mutation testing, such as reducing the number of
mutants to try, detecting equivalent mutants (mutants that are identical to the original
program in terms of behavior), and reducing the number of test cases or test case exe-
cutions (see the work of Ferrari, Pizzoleto, and Offutt, 2018). As a community, we are
taking steps toward a solution, but we are not there yet.
 Despite the cost, mutation testing is highly beneficial. In a very recent paper by
Parsai and Demeyer (2020), the authors demonstrate that mutation coverage reveals
additional weaknesses in the test suite compared to branch coverage and that it can
do so with an acceptable performance overhead during project build. Even large com-
panies like Google are investing in mutation testing in their systems, as reported by
Petrovic´ and Ivankovic´ (2018).
 Researchers are also exploring mutation testing in areas other than Java backend
code. Yandrapally and Mesbah (2021) propose mutations for the Document Object
Model (DOM) in HTML pages to assess whether web tests (which we discuss in
Figure 3.11
Part of a report generated by Pitest. Lines 26, 31, 32, 36, 38, 39, 43, and 44 have surviving mutants.


---
**Page 93**

93
Exercises
chapter 9) are strong enough. In addition, Tuya and colleagues (2006) proposed the
use of mutation in SQL queries.
 I suggest that you try to apply mutation testing, especially in more sensitive parts of
your system. While running mutation testing for the entire system can be expensive,
running it for a smaller set of classes is feasible and may give you valuable insights
about what else to test. 
Exercises
3.1
Consider the following piece of code, which plays a game of Blackjack:
01. public int play(int left, int right) {
02.    int ln = left;
03.    int rn = right;
04.    if (ln > 21)
05.        ln = 0;
06.    if (rn > 21)
07.        rn = 0;
08.    if (ln > rn)
09.        return ln;
10.    else
11.       return rn;
12. }
What is the line coverage of a test where left=22 and right=21? In the calcula-
tion, disregard the lines with the function signature and the last curly bracket
(lines 1 and 12).
A 60%
B 80%
C 70%
D 100%
3.2
Consider the following remove method:
public boolean remove(Object o) {
  if (o == null) {
    for (Node<E> x = first; x != null; x = x.next) {
      if (x.item == null) {
        unlink(x);
        return true;
      }
    }
  } else {
    for (Node<E> x = first; x != null; x = x.next) {
      if (o.equals(x.item)) {
        unlink(x);
        return true;
      }
    }
  }
  return false;
}



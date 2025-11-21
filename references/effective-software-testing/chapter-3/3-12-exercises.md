# 3.12 Exercises (pp.93-96)

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


---
**Page 94**

94
CHAPTER 3
Structural testing and code coverage
This is the implementation of the Java Platform, Standard Edition 8 Develop-
ment Kit (JDK 8) LinkedList remove method.
Create a test suite (a set of tests) that achieves 100% line coverage. Use as few
tests as possible. Feel free to write them as JUnit tests or as a set of inputs and
expected outputs.
3.3
Following is Java’s implementation of the LinkedList’s computeIfPresent()
method:
public V computeIfPresent(K key,
➥ BiFunction<? super K, ? super V, ? extends V> rf) {
  if (rf == null) {
    throw new NullPointerException();
  }
  Node<K,V> e;
  V oldValue;
  int hash = hash(key);
  e = getNode(hash, key);
  oldValue = e.value;
  if (e != null && oldValue != null) {
    V v = rf.apply(key, oldValue);
    if (v != null) {
      e.value = v;
      afterNodeAccess(e);
      return v;
    } else {
      removeNode(hash, key, null, false, true);
    }
  }
  return null;
}
What is the minimum number of tests required to achieve 100% branch cover-
age?
A 2
B 3
C 4
D 6
3.4
Consider the expression (A & B) | C with the following truth table:
Test case
A
B
C
(A & B) | C
1
T
T
T
T
2
T
T
F
T
3
T
F
T
T


---
**Page 95**

95
Exercises
What test suite(s) achieve 100% MC/DC? The numbers correspond to the test
case column in the truth table. Select all that apply.
A {2, 3, 4, 6}
B {2, 4, 5, 6}
C {1, 3, 4, 6}
D {3, 4, 5, 8}
3.5
Draw the truth table for the expression A && (A || B).
Is it possible to achieve MC/DC coverage for this expression? Why or why not?
What would you tell the developer who wrote this expression?
3.6
Consider the following method:
public String sameEnds(String string) {
  int length = string.length();
  int half = length / 2;
  String left = "";
  String right = "";
  int size = 0;
  for (int i = 0; i < half; i++) {
    left = left + string.charAt(i);
    right = string.charAt(length - 1 - i) + right;
    if (left.equals(right)) {
      size = left.length();
    }
  }
  return string.substring(0, size);
}
Which of the following statements is not correct?
A It is possible to devise a single test case that achieves 100% line coverage
and 100% decision coverage.
B It is possible to devise a single test case that achieves 100% line coverage
and 100% (basic) condition coverage.
4
T
F
F
F
5
F
T
T
T
6
F
T
F
F
7
F
F
T
T
8
F
F
F
F
Test case
A
B
C
(A & B) | C


---
**Page 96**

96
CHAPTER 3
Structural testing and code coverage
C It is possible to devise a single test case that achieves 100% line coverage
and 100% decision + condition coverage.
D It is possible to devise a single test case that achieves 100% line coverage
and 100% path coverage.
3.7
Which of the following statements concerning the subsumption relations between
test adequacy criteria is true?
A MC/DC subsumes statement coverage.
B Statement coverage subsumes branch coverage.
C Branch coverage subsumes path coverage.
D Basic condition coverage subsumes branch coverage.
3.8
A test suite satisfies the loop boundary adequacy criterion if for every loop L:
A Test cases iterate L zero times, once, and more than once.
B Test cases iterate L once and more than once.
C Test cases iterate L zero times and one time.
D Test cases iterate L zero times, once, more than once, and N, where N is
the maximum number of iterations.
3.9
Which of the following statements is correct about the relationship between
specification-based testing and structural testing?
A A testing process should prioritize structural testing because it’s cheaper yet
highly effective (maybe even more effective than specification-based testing).
B Specification-based testing can only be effectively performed when we have
proper models of the program under test. A simple user story is not enough.
C Boundary analysis can only be done if testers have access to the source
code, and thus it should be considered a structural testing technique.
D None of the other answers is true.
Summary
Structural testing uses the source code to augment the test suite engineered via
specification-based testing.
The overall idea of structural testing is to analyze which parts of the code are
not yet covered and reflect on whether they should be covered or not.
Some coverage criteria are less rigorous and therefore less expensive (for exam-
ple, line coverage). Others are more rigorous but also more expensive (such as
MC/DC coverage). As a developer, you have to decide which criteria to use.
Code coverage should not be used as a number to be achieved. Rather, cover-
age tools should be used to support developers in performing structural testing
(that is, understanding what parts are not covered and why).
Mutation testing ensures that our test suite is strong enough: in other words,
that it can catch as many bugs as possible.



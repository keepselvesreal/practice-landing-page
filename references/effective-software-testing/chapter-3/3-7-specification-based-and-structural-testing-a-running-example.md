# 3.7 Specification-based and structural testing: A running example (pp.77-82)

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


---
**Page 78**

78
CHAPTER 3
Structural testing and code coverage
  } else {                
    final char[] padding = new char[pads];
    final char[] padChars = padStr.toCharArray();
    for (int i = 0; i < pads; i++) {
      padding[i] = padChars[i % padLen];
    }
    return new String(padding).concat(str);
  }
}
Now it is time for some systematic testing. As we know, the first step is to apply
specification-based testing. Let’s follow the process discussed in chapter 2 (I suggest
you try to do it yourself and compare your solution to mine):
1
We read the requirements. We understand that the program adds a given char-
acter/string to the beginning (left) of the string, up to a specific size. The pro-
gram has three input parameters: str, representing the original string to be
padded; size, representing the desired size of the returned string; and padStr,
representing the string used to pad. The program returns a String. The pro-
gram has specific behavior if any of the inputs is null. (If we had implemented
the feature ourselves, we would probably skip this step, as we would already
have a complete understanding of the requirements.)
2
Based on all the observations in step 1, we derive the following list of partitions:
– str parameter
Null
Empty string
Non-empty string
– size parameter
Negative number
Positive number
– padStr parameter
Null
Empty
Non-empty
– str, size parameters

size < len(str)

size > len(str)
3
There are several boundaries:
– size being precisely 0
– str having length 1
– padStr having length 1
– size being precisely the length of str
We have to add the pad 
string more than once. We 
go character by character 
until the string is fully 
padded.


---
**Page 79**

79
Specification-based and structural testing: A running example
4
We can devise single tests for exceptional cases such as null, empty, and nega-
tive size. We also have a boundary related to padStr: we can exercise padStr
with a single character only once and have all other tests use a pad with a single
character (otherwise, the number of combinations would be too large). We
obtain the following tests:
– T1: str is null.
– T2: str is empty.
– T3: negative size.
– T4: padStr is null.
– T5: padStr is empty.
– T6: padStr has a single character.
– T7: size is equal to the length of str.
– T8: size is equal to 0.
– T9: size is smaller than the length of str.
Now we automate the tests. I used a parameterized test, but it is fine if you prefer nine
traditional JUnit tests.
public class LeftPadTest {
  @ParameterizedTest
  @MethodSource("generator")
  void test(String originalStr, int size, String padString,
   String expectedStr) {               
    assertThat(leftPad(originalStr, size, padString))
        .isEqualTo(expectedStr);
  }
  static Stream<Arguments> generator() {     
    return Stream.of(
      of(null, 10, "-", null),  
      of("", 5, "-", "-----"),  
      of("abc", -1, "-", "abc"),      
      of("abc", 5, null, "  abc"),      
      of("abc", 5, "", " abc"),         
      of("abc", 5, "-", "--abc"),    
      of("abc", 3, "-", "abc"),      
      of("abc", 0, "-", "abc"),     
      of("abc", 2, "-", "abc")     
    );
  }
}
It is time to augment the test suite through structural testing. Let’s use a code cover-
age tool to tell us what we have already covered (see figure 3.8). The report shows that
we are missing some branches: the if (pads == padLen) and else if (pads < padLen)
expressions.
Listing 3.6
Tests for LeftPad after specification-based testing
The parameterized 
test, similar to the 
ones we have written 
before
The nine tests we created 
are provided by the 
method source.
T1
T2
T3
T4
T5
T6
T7
T8
T9


---
**Page 80**

80
CHAPTER 3
Structural testing and code coverage
This is useful information. Why didn’t we cover these lines? What did we miss? As a
developer, you should triangulate what you see in the source with the specification
and your mental model of the program. In this case, we conclude that we did not
exercise padStr being smaller, greater, or equal to the remaining space in str. What a
tricky boundary! This is why structural testing is essential: it helps identify partitions
and boundaries we may have missed.
 With that information in mind, we derive three more test cases:
T10: the length of padStr is equal to the remaining spaces in str.
T11: the length of padStr is greater than the remaining spaces in str.
T12: the length of padStr is smaller than the remaining spaces in str (this test
may be similar to T6).
We add these three extra test cases to our parameterized test, as shown in listing 3.7.
When we run the coverage tool again, we get a report similar to the one in figure 3.9.
We now cover all the branches.
static Stream<Arguments> generator() {
  return Stream.of(
    // ... others here
Listing 3.7
Three new test cases for leftPad
The red lines indicate parts of the
code that are still not covered!
Figure 3.8
Code coverage achieved by the specification-based tests for the leftPad method. The 
two return lines near the arrow are not covered; the if and else if, also near the arrow, are 
only partially covered. The remaining lines are fully covered.


---
**Page 81**

81
Specification-based and structural testing: A running example
    of("abc", 5, "--", "--abc"), // T10
    of("abc", 5, "---", "--abc"), // T11
    of("abc", 5, "-", "--abc") // T12
  );
}
NOTE
Interestingly, if you look at the entire class, JaCoCo does not give
100% coverage, but only 96%. The report highlights the first line of the file:
the declaration of the class, public class LeftPadUtils {. The leftPad
method is static, so none of our tests instantiate this class. Given that we know
the context, we can ignore the fact that this line is not covered. This is a good
example of why only looking at the numbers makes no sense. We discuss this
further, later in the chapter.
With all the branches covered, we now look for other interesting cases to test. The
implementation contains interesting decisions that we may decide to test. In particu-
lar, we observe an if (pads <= 0) block with the code comment “returns original
String when possible”. As a tester, you may decide to test this specific behavior: “If the
string is not padded, the program should return the same String instance.” That can
be written as a JUnit test as follows.
 
 
All lines are green.
Everything is
covered!
Figure 3.9
Code coverage of the leftPad method after specification-based and structural tests. We 
now achieve 100% branch coverage.


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



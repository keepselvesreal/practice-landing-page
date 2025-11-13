# 2.3 Finding bugs with specification testing (pp.46-54)

---
**Page 46**

46
CHAPTER 2
Specification-based testing
c
Explore the possible types of outputs, and make sure you are testing them
all. While exploring the inputs and outputs, pay attention to any implicit
(business) rules, logic, or expected behavior.
4
Identify the boundaries. Bugs love boundaries, so be extra thorough here. Analyze
the boundaries of all the partitions you devised in the previous step. Identify
the relevant ones, and add them to the list.
5
Devise test cases based on the partitions and boundaries. The basic idea is to combine
all the partitions in the different categories to test all possible combinations of
inputs. However, combining them all may be too expensive, so part of the task is
to reduce the number of combinations. The common strategy is to test excep-
tional behavior only once and not combine it with the other partitions.
6
Automate the test cases. A test is only a test when it is automated. Therefore, the
goal is to write (JUnit) automated tests for all the test cases you just devised.
This means identifying concrete input values for them and having a clear
expectation of what the program should do (the output). Remember that test
code is code, so reduce duplication and ensure that the code is easy to read and
that the different test cases are easily identifiable in case one fails.
7
Augment the test suite with creativity and experience. Perform some final checks.
Revisit all the tests you created, using your experience and creativity. Did you
miss something? Does your gut feeling tell you that the program may fail in a
specific case? If so, add a new test case. 
2.3
Finding bugs with specification testing
The developers of the Apache Commons Lang framework (the framework where I
extracted the implementation of the substringsBetween method) are just too good.
We did not find any bugs there. Let’s look at another example: one implemented by
me, an average developer who makes mistakes from time to time. This example will
show you the value of specification testing. Try to spot the bug before I reveal it!
 Some friends and I have participated in many coding challenges, primarily for fun.
A couple of years ago we worked on the following problem inspired by LeetCode
(https://leetcode.com/problems/add-two-numbers):
The method receives two numbers, left and right (each represented as a list
of digits), adds them, and returns the result as a list of digits.
Each element in the left and right lists of digits should be a number from
[0–9]. An IllegalArgumentException is thrown if this pre-condition does
not hold.

left—A list containing the left number. Null returns null; empty means 0.

right—A list containing the right number. Null returns null; empty
means 0.
The program returns the sum of left and right as a list of digits.


---
**Page 47**

47
Finding bugs with specification testing
For example, adding the numbers 23 and 42 means a (left) list with two elements
[2,3], a (right) list with two elements [4,2] and, as an output, a list with two elements
[6,5] (since 23 + 42 = 65).
 My initial implementation was as follows.
public List<Integer> add(List<Integer> left, List<Integer> right) {
  if (left == null || right == null)   
    return null;
  Collections.reverse(left);   
  Collections.reverse(right);
  LinkedList<Integer> result = new LinkedList<>();
  int carry = 0;
  for (int i = 0; i < max(left.size(), right.size()); i++) {  
    int leftDigit = left.size() > i ? left.get(i) : 0;
    int rightDigit = right.size() > i ? right.get(i) : 0;
    if (leftDigit < 0 || leftDigit > 9 ||
     rightDigit < 0 || rightDigit > 9)    
      throw new IllegalArgumentException();
    int sum = leftDigit + rightDigit + carry;   
    result.addFirst(sum % 10);   
    carry = sum / 10;   
  }
  return result;
}
The algorithm works as follows. First it reverses both lists of digits, so the least signifi-
cant digit is on the left. This makes it easier for us to loop through the list. Then, for
each digit in both the left and right numbers, the algorithm gets the next relevant
digits and sums them. If the resulting sum is greater than 10, +1 needs to be carried to
the next most significant digit. In the end, the algorithm returns the list.
 I was just having fun with coding, so I did not write systematic tests. I tried a couple
of inputs and observed that the output was correct. If you already understand the con-
cept of code coverage, these four tests achieve 100% branch coverage if we discard the
ifs related to checking null and pre-conditions (if you are not familiar with code cov-
erage, don’t worry; we discuss it in the next chapter):
T1 = [1] + [1] = [2]
T2 = [1,5] + [1,0] = [2,5]
Listing 2.9
Initial implementation of the add() method
Returns null if left 
or right is null
Reverses the numbers so the least 
significant digit is on the left
While there 
is a digit, keeps 
summing, taking 
carries into 
consideration
Throws an exception 
if the pre-condition 
does not hold
Sums the left digit with 
the right digit with the 
possible carry
The digit should be a number between 0 and 
9. We calculate it by taking the rest of the 
division (the % operator) of the sum by 10.
If the sum is greater than 10, carries the 
rest of the division to the next digit


---
**Page 48**

48
CHAPTER 2
Specification-based testing
T3 = [1,5] + [1,5] = [3,0]
T4 = [5,0,0] + [2,5,0] = [7,5,0]
The program worked fine for these inputs. I submitted it to the coding challenge plat-
form, and, to my surprise, the implementation was rejected! There was a bug in my code.
Before I show you where it is, here is how specification testing would have caught it.
 First we analyze each parameter in isolation:

left parameter—It is a list, so we should first exercise basic inputs such as null,
empty, a single digit, and multiple digits. Given that this list represents a num-
ber, we should also try a number with many zeroes on the left. Such zeroes are
useless, but it is good to see whether the implementation can handle them.
Thus we have the following partitions:
– Empty
– Null
– Single digit
– Multiple digits
– Zeroes on the left

right parameter—We have the same list of partitions as for the left parameter:
– Empty
– Null
– Single digit
– Multiple digits
– Zeroes on the left
left and right have a relationship. Let’s explore that:
(left, right) parameters—They can be different sizes, and the program should
be able to handle it:
– length(left list) > length(right list)
– length(left list) < length(right list)
– length(left list) = length(right list)
While not explicit in the documentation, we know that the sum of two numbers
should be the same regardless of whether the highest number is on the left or right
side of the equation. We also know that some sums require carrying. For example,
suppose we’re summing 18 + 15: 8 + 5 = 13, which means we have a 3, and we carry +1
to the next digit. We then add 1 + 1 + 1: the first 1 from the left number, the second
1 from the right number, and the third 1 carried from the previous sum. The final
result is 33. Figure 2.5 illustrates this process.
+1
1
1
+
+ carry = 3
8 + 5 = 3
1
3
3 3
1 8
1 5
+
Figure 2.5
Illustrating the carry 
when summing 18 + 15


---
**Page 49**

49
Finding bugs with specification testing
The carry is such an important concept in this program that it deserves testing. This is
what I meant in listing 2.9 when I said to pay extra attention to specific (business)
rules and logic:
Carry—Let’s try sums that require carrying in many different ways. These are
good places to start:
– Sum without a carry
– Sum with a carry: one carry at the beginning
– Sum with a carry: one carry in the middle
– Sum with a carry: many carries
– Sum with a carry: many carries, not in a row
– Sum with a carry: carry propagated to a new (most significant) digit
The only boundary worth testing is the following: ensuring that cases such as 99 + 1
(where the final number is carried to a new, most significant digit) are covered. This
comes from the last partition derived when analyzing the carry: “Sum with a carry:
carry propagated to a new (most significant) digit.”
 With all the inputs and outputs analyzed, it is time to derive concrete test cases.
Let’s apply the following strategy:
1
Test nulls and empties just once.
2
Test numbers with single digits just once.
3
Test numbers with multiple digits, with left and right having the same and
different lengths. We will be thorough and have the same set of tests for both
equal and different lengths, and we will duplicate the test suite to ensure that
everything works if left is longer than right or vice versa.
4
We will exercise the zeroes on the left, but a few test cases are enough.
5
Test the boundary.
Domain knowledge is still fundamental to engineer good test cases
Up to this point, this chapter may have given you the impression that if you analyze
every parameter of the method, you can derive all the test cases you need. Life would
be much easier if that were true!
Analyzing parameters, even without much domain knowledge, will help you uncover
many bugs. However, having a deep understanding of the requirements is still key in
devising good test cases. In the current example, the requirements do not discuss
the carry. We devised many tests around the carry because we have a deep knowl-
edge of the problem. We build up knowledge over time; so although the systematic
approaches I discuss will help you uncover many common bugs, it is your job to learn
about the domain of the software system you’re working on. (And if you wrote the
code, you have an advantage: you know it deeply!)


---
**Page 50**

50
CHAPTER 2
Specification-based testing
Let’s look at the specific test cases:
Nulls and empties
– T1: left null
– T2: left empty
– T3: right null
– T4: right empty
Single digits
– T5: single digit, no carry
– T6: single digit, carry
Multiple digits
– T7: no carry
– T8: carry in the least significant digit
– T9: carry in the middle
– T10: many carries
– T11: many carries, not in a row
– T12: carry propagated to a new (now most significant) digit
Multiple digits with different lengths (one for left longer than right, and one
for right longer than left)
– T13: no carry
– T14: carry in the least significant digit
– T15: carry in the middle
– T16: many carries
– T17: many carries, not in a row
– T18: carry propagated to a new (now most significant) digit
Zeroes on the left
– T19: no carry
– T20: carry
Boundaries
– T21: carry to a new most significant digit, by one (such as 99 +1 ).
Now we transform them into automated test cases, as shown in listing 2.10. A few
remarks about this listing:
This test uses the ParameterizedTest feature from JUnit. The idea is that we
write a single generic test method that works like a skeleton. Instead of having
hard-coded values, it uses variables. The concrete values are passed to the test
method later. The testCases() method provides inputs to the shouldReturn-
CorrectResult test method. The link between the test method and the method
source is done through the @MethodSource annotation. JUnit offers other ways
to provide inputs to methods, such as inline comma-separated values (see the
@CsvSource annotation in the documentation).


---
**Page 51**

51
Finding bugs with specification testing
The numbers() helper method receives a list of integers and converts it to a
List<Integer>, which the method under test receives. This helper method
increases the legibility of the test methods. (For the Java experts, the Arrays
.asList() native method would have yielded the same result.)
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.Arguments;
import org.junit.jupiter.params.provider.MethodSource;
import java.util.ArrayList;
import java.util.List;
import java.util.stream.Stream;
import static org.assertj.core.api.Assertions.assertThat;
import static org.assertj.core.api.Assertions.assertThatThrownBy;
import static org.junit.jupiter.params.provider.Arguments.of;
public class NumberUtilsTest {
 @ParameterizedTest          
 @MethodSource("testCases")                          
 void shouldReturnCorrectResult(List<Integer> left,
  List<Integer> right, List<Integer> expected) {
   assertThat(new NumberUtils().add(left, right))   
       .isEqualTo(expected);
 }
 static Stream<Arguments> testCases() {     
   return Stream.of(
     of(null, numbers(7,2), null), // T1                
     of(numbers(), numbers(7,2), numbers(7,2)), // T2   
     of(numbers(9,8), null, null), // T3                
     of(numbers(9,8), numbers(), numbers(9,8 )), // T4  
     of(numbers(1), numbers(2), numbers(3)), // T5     
     of(numbers(9), numbers(2), numbers(1,1)), // T6   
     of(numbers(2,2), numbers(3,3), numbers(5,5)), // T7          
     of(numbers(2,9), numbers(2,3), numbers(5,2)), // T8          
     of(numbers(2,9,3), numbers(1,8,3), numbers(4,7,6)), // T9    
     of(numbers(1,7,9), numbers(2,6,8), numbers(4,4,7)), // T10   
     of(numbers(1,9,1,7,1), numbers(1,8,1,6,1),
       numbers(3,7,3,3,2)), // T11                                
     of(numbers(9,9,8), numbers(1,7,2), numbers(1,1,7,0)), // T12 
     of(numbers(2,2), numbers(3), numbers(2,5)), // T13.1          
     of(numbers(3), numbers(2,2), numbers(2,5)), // T13.2          
     of(numbers(2,2), numbers(9), numbers(3,1)), // T14.1          
     of(numbers(9), numbers(2,2), numbers(3,1)), // T14.2          
     of(numbers(1,7,3), numbers(9,2), numbers(2,6,5)), // T15.1    
     of(numbers(9,2), numbers(1,7,3), numbers(2,6,5)), // T15.2    
Listing 2.10
Tests for the add method
A parameterized test is 
a perfect fit for these 
kinds of tests!
Indicates the name of 
the method that will 
provide the inputs
Calls the
method under
test, using the
parameterized
values
One argument 
per test case
Tests with nulls 
and empties
Tests with 
single digits
Tests with 
multiple 
digits
Tests with multiple
digits, different
length, with and
without carry
(from both sides)


---
**Page 52**

52
CHAPTER 2
Specification-based testing
     of(numbers(3,1,7,9), numbers(2,6,8), numbers(3,4,4,7)), // T16.1    
     of(numbers(2,6,8), numbers(3,1,7,9), numbers(3,4,4,7)), // T16.2    
     of(numbers(1,9,1,7,1), numbers(2,1,8,1,6,1),
       numbers(2,3,7,3,3,2)), // T17.1                                   
     of(numbers(2,1,8,1,6,1), numbers(1,9,1,7,1),
       numbers(2,3,7,3,3,2)), // T17.2                                   
     of(numbers(9,9,8), numbers(9,1,7,2), numbers(1,0,1,7,0)), // T18.1  
     of(numbers(9,1,7,2), numbers(9,9,8), numbers(1,0,1,7,0)), // T18.2  
     of(numbers(0,0,0,1,2), numbers(0,2,3), numbers(3,5)), // T19   
     of(numbers(0,0,0,1,2), numbers(0,2,9), numbers(4,1)), // T20   
     of(numbers(9,9), numbers(1), numbers(1,0,0)) // T21   
   );
 }
 private static List<Integer> numbers(int... nums) {   
   List<Integer> list = new ArrayList<>();
   for(int n : nums)
     list.add(n);
   return list;
 }
}
Interestingly, a lot of these test cases break! See the JUnit report in figure 2.6. For
example, take the first failing test, T6 (single digit with a carry). Given left = [9] and
right = [2], we expect the output to be [1,1]. But the program outputs [1]! T12
(“carry propagated to a new (now most significant) digit”) also fails: given left =
[9,9,8] and right = [1,7,2], we expect the output to be [1,1,7,0], but it is
[1,7,0]. The program cannot handle the carry when the carry needs to become a
new leftmost digit.
 What a tricky bug! Did you see it when we wrote the method implementation?
 There is a simple fix: all we need to do is add the carry at the end, if necessary.
Here’s the implementation.
// ... all the code here ...
if (carry > 0)
    result.addFirst(carry);
return result;
With these tests passing, we see that the program does not handle zeroes to the left.
When left = [0,0,0,1,2] and right = [0,2,3], we expect the output to be [3,5],
but the program returns [0,0,0,3,5]. The fix is also straightforward: remove the
zeroes on the left before returning the result (listing 2.12).
 
Listing 2.11
First bug fix in the add program
Tests with multiple
digits, different
length, with and
without carry
(from both sides)
Tests with zeroes
on the left
The boundary 
test
Auxiliary method
that produces a list of
integers. Auxiliary methods
are common in test suites to
help developers write more
maintainable test code.


---
**Page 53**

53
Finding bugs with specification testing
 
// ... previous code here...
if (carry > 0)
    result.addFirst(carry);
while (result.size() > 1 && result.get(0) == 0)   
  result.remove(0);
return result;
Listing 2.12
Second bug fix in the add program
Left
Right
Expected
output
These tests are all
failing! This means
our implementation
has a bug.
Figure 2.6
The results of the test cases we just created. A lot of them fail, indicating 
that the program has a bug!
Removes leading 
zeroes from the 
result


---
**Page 54**

54
CHAPTER 2
Specification-based testing
We’re only missing test cases to ensure that the pre-condition holds that each digit is a
number between 0 and 9. All we need to do is pass various invalid digits. Let’s do it
directly in the JUnit test as follows.
@ParameterizedTest       
@MethodSource("digitsOutOfRange")
void shouldThrowExceptionWhenDigitsAreOutOfRange(List<Integer> left,
  ➥ List<Integer> right) {
  assertThatThrownBy(() -> new NumberUtils().add(left, right))
      .isInstanceOf(IllegalArgumentException.class);   
}
static Stream<Arguments> digitsOutOfRange() {  
  return Stream.of(
      of(numbers(1,-1,1), numbers(1)),
      of(numbers(1), numbers(1,-1,1)),
      of(numbers(1,10,1), numbers(1)),
      of(numbers(1), numbers(1,11,1))
  );
}
All tests are now passing. Given the thoroughness of our test suite, I feel confident
enough to move on.
NOTE
Interestingly, the bugs we found in this example were caused not by
buggy code but by a lack of code. This is a common type of bug, and it can be
caught by specification testing. When in doubt, write a test! Writing auto-
mated (unit) test cases is so quick that they let you easily see what happens.
Having too many useless tests is a problem, but a couple will not hurt. 
2.4
Specification-based testing in the real world
Now that you have a clear understanding of how to systematically devise test cases
based on specifications, here are a few pragmatic tips I have learned over the years.
2.4.1
The process should be iterative, not sequential
Describing iterative processes in writing is challenging. My explanation may have
given you the impression that this process is fully sequential and that you move to the
next step only when you have completed the previous one. However, the entire pro-
cess is meant to be iterative. In practice, I go back and forth between the different
steps. Often, when I’m writing test cases, I notice that I missed a partition or bound-
ary, and I go back and improve my test suite. 
Listing 2.13
Tests for a pre-condition of the add program
A parameterized test 
also fits well here.
Asserts that 
an exception 
happens
Passes invalid 
arguments



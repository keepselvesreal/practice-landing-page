# 5.3 Example 3: Testing the indexOf method (pp.124-129)

---
**Page 124**

124
CHAPTER 5
Property-based testing
5.3
Example 3: Testing the indexOf method
The Apache Commons Lang has an interesting method called indexOf() (http://mng
.bz/M24m) with the following documentation, adapted from its Javadoc:
Finds the index of the given value in the array starting at the given index. This
method returns –1 for a null input array. A negative startIndex is treated as
zero. A startIndex larger than the array length will return –1.
Input parameters:

array: Array to search for the object. May be null.

valueToFind: Value to find.

startIndex: Index at which to start searching.
The method returns the index of the value within the array, or –1 if not found
or null.
Following is the implementation of this method.
class ArrayUtils {
  public static int indexOf(final int[] array, final int valueToFind,
    ➥ int startIndex) {
    if (array == null) { 
      return -1;
    }
    if (startIndex < 0) { 
      startIndex = 0;
    }
    for (int i = startIndex; i < array.length; i++) {
      if (valueToFind == array[i]) {
        return i; 
      }
    }
    return -1; 
  }
}
In this example, let’s first apply the techniques we already know. Start by exploring the
input variables and how they interact with each other:

array of integers:
– Null
– Single element
– Multiple elements

valueToFind:
– Any integer
Listing 5.8
Implementation of the indexOf method
The method accepts a null array and returns -1 in such a 
case. Another option could be to throw an exception, but 
the developer decided to use a weaker pre-condition.
The same goes for startIndex: 
if the index is negative, the 
method assumes it is 0.
If the value is found, 
return the index.
If the value is not in 
the array, return -1.


---
**Page 125**

125
Example 3: Testing the indexOf method

startIndex:
– Negative number
– 0 [boundary]
– Positive number

(array, startIndex):
– startIndex in array
– startIndex outside the boundaries of array

(array, valueToFind):
– valueToFind not in array
– valueToFind in array
– valueToFind many times in array

(array, valueToFind, startIndex):
– valueToFind in array, but before startIndex
– valueToFind in array, but after startIndex
– valueToFind in array, precisely in startIndex [boundary]
– valueToFind in array multiple times after startIndex
– valueToFind in array multiple times, one before and another after startIndex
We now create the test cases by combining the different partitions:
1
array is null
2
array with a single element, valueToFind in array
3
array with a single element, valueToFind not in array
4
startIndex negative, value in array
5
startIndex outside the boundaries of array
6
array with multiple elements, valueToFind in array, startIndex after value-
ToFind
7
array with multiple elements, valueToFind in array, startIndex before
valueToFind
8
array with multiple elements, valueToFind in array, startIndex precisely at
valueToFind
9
array with multiple elements, valueToFind in array multiple times, start-
Index before valueToFind
10
array with multiple elements, valueToFind in array multiple times, one before
startIndex
11
array with multiple elements, valueToFind not in array
In JUnit, the test suite looks like the following listing.
import static org.junit.jupiter.params.provider.Arguments.of;
public class ArrayUtilsTest {
Listing 5.9
First tests for the indexOf() method


---
**Page 126**

126
CHAPTER 5
Property-based testing
  @ParameterizedTest
  @MethodSource("testCases")
  void testIndexOf(int[] array, int valueToFind, int startIndex,
    ➥ int expectedResult) {
    int result = ArrayUtils.indexOf(array, valueToFind, startIndex);
    assertThat(result).isEqualTo(expectedResult);
  }
  static Stream<Arguments> testCases() { 
    int[] array = new int[] { 1, 2, 3, 4, 5, 4, 6, 7 };
    return Stream.of(
      of(null, 1, 1, -1), 
      of(new int[] { 1 }, 1, 0, 0), 
      of(new int[] { 1 }, 2, 0, -1), 
      of(array, 1, 10, -1), 
      of(array, 2, -1, 1), 
      of(array, 4, 6, -1), 
      of(array, 4, 1, 3), 
      of(array, 4, 3, 3), 
      of(array, 4, 1, 3), 
      of(array, 4, 4, 5), 
      of(array, 8, 0, -1) 
    );
  }
}
Listing 5.10 shows the test suite developed for the library method itself (http://mng
.bz/aDAY). I added some comments, so you can see how their tests related to our
tests. This test suite contains our test cases T1, T4, T5, T6, T7, T8, T10, and T11. Inter-
estingly, it is not testing the behavior of the array with a single element or the case in
which the element appears again after the first time it is found.
@Test
public void testIndexOfIntWithStartIndex() {
  int[] array = null;
  assertEquals(-1, ArrayUtils.indexOf(array, 0, 2)); 
  array = new int[]{0, 1, 2, 3, 0};
  assertEquals(4, ArrayUtils.indexOf(array, 0, 2)); 
  assertEquals(-1, ArrayUtils.indexOf(array, 1, 2)); 
  assertEquals(2, ArrayUtils.indexOf(array, 2, 2)); 
  assertEquals(3, ArrayUtils.indexOf(array, 3, 2)); 
  assertEquals(3, ArrayUtils.indexOf(array, 3, -1)); 
  assertEquals(-1, ArrayUtils.indexOf(array, 99, 0)); 
Listing 5.10
Original test suite of the indexOf() method
All the test cases we engineered 
are implemented here.
T1
T2
T3
T4
T5
T6
T7
T8
T9
T10
T11
Similar to test case T1
Similar to test case T10
Similar to test case T6
Similar to test case T8
Similar to test case T7
Similar to test case T4
Similar to test case T11


---
**Page 127**

127
Example 3: Testing the indexOf method
  assertEquals(-1, ArrayUtils.indexOf(array, 0, 6)); 
}
NOTE
Parameterized tests seem to be less popular in open source systems.
For methods with simple signatures, inputs, and outputs, like indexOf, we
could argue that parameterized tests are overkill. When creating this exam-
ple, I considered writing two different traditional JUnit test cases: one con-
taining only the exceptional behavior and another containing the remaining
test cases. In the end, organizing test cases is a matter of personal taste—talk
to your team and see what approach they prefer. We talk more about test
code quality and readability in chapter 10.
Both test suites look good and are quite strong. But now, let’s express the main behav-
ior of the method via property-based testing.
 The overall idea of the test is to insert a random value in a random position of a
random array. The indexOf() method will look for this random value. Finally, the test
will assert that the method returns an index that matches the random position where
we inserted the element.
 The tricky part of writing such a test is ensuring that the random value we add in the
array does not already exist in the random array. If the value is already there, this may
break our test. Consider a randomly generated array containing [1, 2, 3, 4]: if we
insert a random element 4 (which already exists in the array) on index 1 of the array,
we will get a different response depending on whether startIndex is 0 or 3. To avoid
such confusion, we generate random values that do not exist in the randomly gener-
ated array. This is easily achievable in jqwik. The property-based test needs at least four
parameters:

numbers—A list of random integers (we generate a list, as it is much easier to
add an element at a random position in a list than in an array). This list will
have a size of 100 and will contain values between –1000 and 1000.

value—A random integer that is the value to be inserted into the list. We gener-
ate values ranging from 1001 to 2000, ensuring that whatever value is generated
will not exist in the list.

indexToAddElement—A random integer that represents a random index for
where to add this element. The index ranges from 0 to 99 (the list has size 100).

startIndex—A random integer that represents the index where we ask the
method to start the search. This is also a random number ranging from 0 to 99.
With all the random values ready, the method adds the random value at the random
position and calls indexOf with the random array, the random value to search, and the
random index at which to start the search. We then assert that the method returns
indexToAddElement if indexToAddElement >= startIndex (that is, the element was
inserted after the start index) or –1 if the element was inserted before the start index.
Figure 5.1 illustrates this process.
 The concrete implementation of the jqwik test can be found in listing 5.11.
Similar to test case T5


---
**Page 128**

128
CHAPTER 5
Property-based testing
@Property
void indexOf(
  @ForAll
  @Size(value = 100) List<@IntRange(min = -1000, max = 1000)
  ➥ Integer> numbers, 
  @ForAll
  @IntRange(min = 1001, max = 2000) int value, 
  @ForAll
  @IntRange(max = 99) int indexToAddElement, 
  @ForAll
  @IntRange(max = 99) int startIndex) { 
 numbers.add(indexToAddElement, value); 
 int[] array = convertListToArray(numbers); 
 int expectedIndex = indexToAddElement >= startIndex ?
   indexToAddElement : -1;  
 assertThat(ArrayUtils.indexOf(array, value, startIndex))
   .isEqualTo(expectedIndex); 
}
private int[] convertListToArray(List<Integer> numbers) { 
  int[] array = numbers.stream().mapToInt(x -> x).toArray();
  return array;
}
Listing 5.11
Property-based test for the indexOf() method
5
6
…
31
–1
…
89
87
numbers =
0
1
2
56
57
100
1500
value =
Lots of random unique
integers. This list has a
size of 00 (after the
1
element is inserted,
size = 0 ).
1 1
This value is not
in the original list.
58
indexToAdd
Element =
1
startIndex =
1500
58
Where to start looking. It may
be before or after the position
at which we inserted the element.
The index at which to insert
the element we will search for
Figure 5.1
The data generation of the property-based test for the indexOf method
Generates a list with 100 numbers 
ranging from -1000 to 1000
Generates a random number that we
insert into the array. This number is
outside the range of the list so we
can find it easily.
Randomly picks a 
place to put the 
element in the list
Randomly picks a 
number to start the 
search in the array
Adds the number to 
the list at the randomly 
chosen position
Converts the list to an array, since 
this is what the method expects
If we added the element after the start index, 
we expect the method to return the position 
where we inserted the element. Otherwise we 
expect the method to return -1.
Asserts that the 
search for the value 
returns the index 
we expect
Utility method that
converts a list of
integers to an array


---
**Page 129**

129
Example 4: Testing the Basket class
Jqwik will generate a large number of random inputs for this method, ensuring that
regardless of where the value to find is, and regardless of the chosen start index, the
method will always return the expected index. Notice how this property-based test bet-
ter exercises the properties of the method than the testing method we used earlier.
 I hope this example shows you that writing property-based tests requires creativity.
Here, we had to come up with the idea of generating a random value that is never in
the list so that the indexOf method could find it without ambiguity. We also had to be
creative when doing the assertion, given that the randomly generated indexToAdd-
Element could be larger or smaller than the startIndex (which would drastically
change the output). Pay attention to these two points:
1
Ask yourself, “Am I exercising the property as closely as possible to the real
world?” If you come up with input data that will be wildly different from what
you expect in the real world, it may not be a good test.
2
Do all the partitions have the same likelihood of being exercised by your test?
In the example, the element to be found is sometimes before and sometimes
after the start index. If you write a test in which, say, 95% of the inputs have the
element before the start index, you may be biasing your test too much. You
want all the partitions to have the same likelihood of being exercised.
In the example code, given that both indexToAddElement and startIndex
are random numbers between 0 and 99, we expect about a 50-50 split between
the partitions. When you are unsure about the distribution, add some debug-
ging instructions and see what inputs or partitions your test generates or
exercises. 
5.4
Example 4: Testing the Basket class
Let’s explore one last example that revisits the Basket class from chapter 4. The class
offers two methods: an add() method that receives a product and adds it a quantity
of times to the basket, and a remove() method that removes a product completely
from the cart. Let’s start with the add method.
import static java.math.BigDecimal.valueOf;
public class Basket {
  private BigDecimal totalValue = BigDecimal.ZERO;
  private Map<Product, Integer> basket = new HashMap<>();
  public void add(Product product, int qtyToAdd) {
    assert product != null : "Product is required";               
    assert qtyToAdd > 0 : "Quantity has to be greater than zero"; 
    BigDecimal oldTotalValue = totalValue; 
Listing 5.12
Implementation of Baskets add method
Checks all the
pre-conditions
Stores the old value so we can check 
the post-condition later



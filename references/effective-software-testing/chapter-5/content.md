# Property-based testing (pp.117-141)

---
**Page 117**

117
Property-based testing
So far, we have been doing example-based testing. We judiciously divide the input
space of a program (into partitions), pick one concrete example from all the possi-
ble ones, and write the test case. What if we did not have to pick one concrete
example out of many? What if we could express the property we are trying to exercise
and let the test framework choose several concrete examples for us? Our tests
would be less dependent on a concrete example, and the test framework would be
able to call the method under test multiple times with different input parameters—
usually with zero effort from us.
 This is what property-based testing is about. We do not pick a concrete example;
rather, we define a property (or a set of properties) that the program should
adhere to, and the test framework tries to find a counterexample that causes the
program to break with these properties.
 I have learned that the best way to teach how to write property-based tests is with
multiple examples. So, this chapter presents five different examples with varying
levels of complexity. I want you to focus on my way of thinking and notice how
much creativity is required to write such tests.
This chapter covers
Writing property-based tests
Understanding when to write property-based tests 
or example-based tests


---
**Page 118**

118
CHAPTER 5
Property-based testing
5.1
Example 1: The passing grade program
Consider the following requirement, inspired by a similar problem in Kaner et al.’s
book (2013):
A student passes an exam if they get a grade >= 5.0. Grades below that are a
fail. Grades fall in the range [1.0, 10.0].
A simple implementation for this program is shown in the following listing.
public class PassingGrade {
  public boolean passed(float grade) {
    if (grade < 1.0 || grade > 10.0) 
      throw new IllegalArgumentException();
    return grade >= 5.0;
  }
}
If we were to apply specification-based testing to this program, we would probably
devise partitions such as “passing grade,” “failing grade,” and “grades outside the
range.” We would then devise a single test case per partition. With property-based test-
ing, we want to formulate properties that the program should have. I see the following
properties for this requirement:

fail—For all numbers ranging from 1.0 (inclusive) to 5.0 (exclusive), the pro-
gram should return false.

pass—For all numbers ranging from 5.0 (inclusive) to 10.0 (inclusive), the pro-
gram should return true.

invalid—For all invalid grades (which we define as any number below 1.0 or
greater than 10.0), the program must throw an exception.
Can you see the difference between what we do in specification-based testing and
what we aim to do in property-based testing? Let’s write a suite test by test, starting
with the fail property. For that, we will use jqwik (https://jqwik.net), a popular prop-
erty-based testing framework for Java.
NOTE
Property-based testing frameworks are available in many different lan-
guages, although their APIs vary significantly (unlike unit testing frameworks
like JUnit, which all look similar). If you are applying this knowledge to
another language, your task is to study the framework that is available in your
programming language. The way to think and reason is the same across dif-
ferent languages.
Before I show the concrete implementation, let me break down property-based testing
step by step, using jqwik’s lingo:
Listing 5.1
Implementation of the PassingGrade program
Note the pre-condition 
check here.


---
**Page 119**

119
Example 1: The passing grade program
1
For each property we want to express, we create a method and annotate it with
@Property. These methods look like JUnit tests, but instead of containing a sin-
gle example, they contain an overall property.
2
Properties use randomly generated data. Jqwik includes several generators for
various types (including Strings, Integers, Lists, Dates, and so on.). Jqwik
allows you to define different sets of constraints and restrictions to these param-
eters: for example, to generate only positive Integers or only Strings with a
length between 5 and 10 characters. The property method receives all the
required data for that test as parameters.
3
The property method calls the method under test and asserts that the method’s
behavior is correct.
4
When the test runs, jqwik generates a large amount of random data (following
the characteristics you defined) and calls the test for it, looking for an input
that would break the property. If jqwik finds an input that makes your test fail,
the tool reports this input back to the developer. The developer then has an
example of an input that breaks their program.
The following listing shows the code for the fail property.
public class PassingGradesPBTest {
  private final PassingGrade pg = new PassingGrade();
  @Property
  void fail( 
   @ForAll 
   @FloatRange(min = 1f, max = 5f, maxIncluded = false) 
   float grade) { 
    assertThat(pg.passed(grade)).isFalse();
  }
}
We annotate the test method with @Property instead of @Test. The test method
receives a grade parameter that jqwik will set, following the rules we give it. We then
annotate the grade parameter with two properties. First, we say that this property
should hold for all (@ForAll) grades. This is jqwik’s terminology. If we left only the
@ForAll annotation, jqwik would try any possible float as input. However, for this fail
property, we want numbers varying from 1.0 to 5.0, which we specify using the @Float-
Range annotation. The test then asserts that the program returns false for all the pro-
vided grades.
Listing 5.2
A property-based test for the fail property
Defines the characteristics of the values 
we want to generate via annotations
Any parameter to be 
generated by jqwik 
must be annotated 
with ForAll.
We want random floats 
in a [1.0, 5.0] interval 
(max value excluded), 
which we define in the 
FloatRange annotation.
The grade parameter will be
generated according to the rules
specified in the annotations.


---
**Page 120**

120
CHAPTER 5
Property-based testing
 When we run the test, jqwik randomly provides values for the grade parameter, fol-
lowing the ranges we specified. With its default configuration, jqwik randomly gener-
ates 1,000 different inputs for this method. If this is your first time with property-based
testing, I suggest that you write some print statements in the body of the test method
to see the values generated by the framework. Note how random they are and how
much they vary.
 Correspondingly, we can test the pass property using a similar strategy, as shown next.
@Property
void pass(
  @ForAll
  @FloatRange(min = 5f, max = 10f, maxIncluded = true) 
  float grade) {
  assertThat(pg.passed(grade)).isTrue();
}
Finally, to make jqwik generate numbers that are outside of the valid range of grades,
we need to use a smarter generator (as FloatRange does not allow us to express things
like “grade < 1.0 or grade > 10.0”). See the invalidGrades() provider method in the
following listing: methods annotated with @Provide are used to express more com-
plex inputs that need to be generated.
@Property
void invalid(
 @ForAll("invalidGrades") 
 float grade) {
  assertThatThrownBy(() -> {
    pg.passed(grade);
  }).isInstanceOf(IllegalArgumentException.class); 
}
@Provide 
private Arbitrary<Float> invalidGrades() {
  return Arbitraries.oneOf( 
      Arbitraries.floats().lessThan(1f), 
      Arbitraries.floats().greaterThan(10f) 
  );
}
The @Property test method is straightforward: for all grades generated, we assert that
an exception is thrown. The challenge is generating random grades. We express this
in the invalidGrades provider method, which should return either a grade smaller
than 1 or a grade greater than 10. Also, note that the method returns an Arbitrary.
Listing 5.3
A property-based test for the pass property
Listing 5.4
A property-based test for the invalidGrades property
We want random 
floats in the range 
of [5.0, 10.0], max 
value included.
The @ForAll annotation receives 
the name of a Provider method 
that will generate the data.
Asserts that an 
exception is thrown 
for any value outside 
the boundary
A provider method needs to be 
annotated with @Provide.
Makes the method 
randomly return …
… a float that is 
less than 1.0 …
… or greater than 10.0.


---
**Page 121**

121
Example 1: The passing grade program
An Arbitrary is how jqwik handles arbitrary values that need to be generated. If you
need, say, arbitrary floats, your provider method should return an Arbitrary<Float>.
 To give the two options to jqwik, we use the Arbitraries.oneOf() method. The
Arbitraries class contains dozens of methods that help build arbitrary data. The
oneOf() method receives a list of arbitrary values it may return. Behind the scenes,
this method ensures that the distribution of data points generated is fairly distributed:
for example, it generates as many “smaller than 1” inputs as “greater than 10” inputs.
Then, we use another helper, the Arbitraries.floats() method, to generate ran-
dom floats. Finally, we use the lessThan() and greaterThan() methods to generate
numbers less than 1 and greater than 10, respectively.
NOTE
I suggest exploring the methods that the Arbitraries class provides!
Jqwik is a very extensive framework and contains lots of methods to help you
build any property you need. I will not discuss every feature of the framework, as
that would be an entire book by itself. Instead, I recommend that you dive into
jqwik’s excellent user guide: https://jqwik.net/docs/current/user-guide.html.
When we run the tests, all of them pass, since our implementation is correct. Now,
let’s introduce a bug in the code to see the jqwik output. For example, let’s change
return grade >= 5.0 to return grade > 5.0, a simple off-by-one mistake. When we run
our test suite again, the pass property test fails as expected! Jqwik also produces nice
output to help us debug the problem.
|-------------------jqwik-------------------
tries = 11                    | \# of calls to property
checks = 11                   | \# of not rejected calls
generation = RANDOMIZED       | parameters are randomly generated
after-failure = PREVIOUS_SEED | use the previous seed
when-fixed-seed = ALLOW       | fixing the random seed is allowed
edge-cases\#mode = MIXIN      | edge cases are mixed in
edge-cases\#total = 2         | \# of all combined edge cases
edge-cases\#tried = 1         | \# of edge cases tried in current run
seed = 7015333710778187630    | random seed to reproduce generated values
Sample
------
  arg0: 5.0
The output shows that jqwik found a counterexample in attempt number 11. Only 11
trials were enough to find the bug! Jqwik then shows a set of configuration parameters
that may be useful when reproducing and debugging more complex cases. In particu-
lar, note the seed information: you can reuse that seed later to force jqwik to come up
with the same sequence of inputs. Below the configuration, we see the sample that
caused the bug: the value 5.0, as expected.
Listing 5.5
An example of a jqwik test failure


---
**Page 122**

122
CHAPTER 5
Property-based testing
NOTE
If you are connecting the dots with previous chapters, you may be won-
dering about boundary testing. Jqwik is smart enough to also generate
boundary values! If we ask jqwik to generate, say, floats smaller than 1.0,
jqwik will generate 1.0 as a test. If we ask jqwik to generate any integer, jqwik
will try the maximum and minimum possible integers as well as 0 and nega-
tive numbers. 
5.2
Example 2: Testing the unique method
The Apache Commons Lang offers the unique method (http://mng.bz/XWGM). Fol-
lowing is its adapted Javadoc:
Returns an array consisting of the unique values in data. The return array is
sorted in descending order. Empty arrays are allowed, but null arrays result in
a NullPointerException. Infinities are allowed.
Parameters:

data: Array to scan
The method returns a descending list of values included in the input array. It
throws a NullPointerException if data is null.
You can see its implementation next.
public static int[] unique(int[] data) {
  TreeSet<Integer> values = new TreeSet<Integer>(); 
  for (int i = 0; i < data.length; i++) {
     values.add(data[i]);
  }
  final int count = values.size();
  final int[] out = new int[count]; 
  Iterator<Integer> iterator = values.iterator();
  int i = 0;
  while (iterator.hasNext()) { 
     out[count - ++i] = iterator.next();
  }
  return out;
}
Let’s go straight to property-based testing. Here, we focus on the main property of the
method: given an array of integers, the method returns a new array containing only
the unique values of the original array, sorted in descending order. This is the prop-
erty we will embed in a jqwik test.
 Our test works as follows. First we create a random list of integers. To ensure that
the list has repeated numbers, we create a list of size 100 and limit the range of integers
Listing 5.6
Implementation of the unique method
Uses a treeset to 
filter out repeated 
elements
Creates the new array 
using the size of the tree
Visits the treeset and 
adds the elements to 
the new array


---
**Page 123**

123
Example 2: Testing the unique method
to [0,20]. We then call the unique method and assert that the array contains all the
elements of the original array, does not have duplicates, and is sorted in descending
order. Let’s write that down in jqwik.
public class MathArraysPBTest {
  @Property
  void unique(
   @ForAll
   @Size(value = 100) 
   List<@IntRange(min = 1, max = 20) Integer> 
   numbers) {
    int[] doubles = convertListToArray(numbers);
    int[] result = MathArrays.unique(doubles);
    assertThat(result)
        .contains(doubles) 
        .doesNotHaveDuplicates() 
        .isSortedAccordingTo(reverseOrder()); 
  }
  private int[] convertListToArray(List<Integer> numbers) { 
    int[] array = numbers
      .stream()
      .mapToInt(x -> x)
      .toArray();
    return array;
  }
}
TIP
Note how AssertJ simplifies our lives with its many ready-to-use asser-
tions. Without it, the developer would have to write lots of extra code. When
writing complex assertions, check the documentation to see whether some-
thing is available out of the box!
NOTE
One of my students noticed that even if we do not restrict the integer
list to numbers in [0, 20], jqwik will produce lists with duplicated elements. In
his exploration, he noticed that 11% of the produced arrays had a duplicated
element. As a tester, you may want to consider whether 11% is a good rate. To
measure this, my student used jqwik’s statistics feature (http://mng.bz/y4gE),
which enables you to measure the distribution of the input values.
Jqwik did not find any inputs that would break the program. So, our implementation
seems to work. Let’s move to the next example. 
Listing 5.7
Property-based test for the unique method
An array of 
size 100
With values in [0, 20]. Given 
the size of the array (100), 
we know it will contain 
repeated elements.
Contains all the elements
No duplicates
In descending order
Utility method
that converts a list of
integers to an array


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


---
**Page 130**

130
CHAPTER 5
Property-based testing
    int existingQuantity = basket.getOrDefault(product, 0); 
    int newQuantity = existingQuantity + qtyToAdd;
    basket.put(product, newQuantity);
    BigDecimal valueAlreadyInTheCart = product.getPrice()
      .multiply(valueOf(existingQuantity)); 
    BigDecimal newFinalValueForTheProduct = product.getPrice()
      .multiply(valueOf(newQuantity));      
    totalValue = totalValue
      .subtract(valueAlreadyInTheCart)
      .add(newFinalValueForTheProduct); 
    assert basket.containsKey(product) : "Product was not inserted in     
    ➥ the basket";                                                       
    assert totalValue.compareTo(oldTotalValue) == 1 : "Total value should 
    ➥ be greater than previous total value";                             
    assert invariant() : "Invariant does not hold";                       
  }
}
The implementation is straightforward. First it does the pre-condition checks we dis-
cussed in chapter 4. The product cannot be null, and the quantity of the product to
be added to the cart has to be larger than zero. Then the method checks whether the
basket already contains the product. If so, it adds the quantity on top of the quantity
already in the cart. It then calculates the value to add to the total value of the basket.
To do so, it calculates the value of that product based on the previous amount in the
basket, subtracts that from the total value, and then adds the new total value for that
product. Finally, it ensures that the invariant (the total value of the basket must be
positive) still holds.
 The remove method is simpler than the add method. It looks for the product in
the basket, calculates the amount it needs to remove from the total value of the bas-
ket, subtracts it, and removes the product (listing 5.13). The method also ensures
the same two pre-conditions we discussed before: the product cannot be null, and
the product has to be in the basket.
public void remove(Product product) {
    assert product != null : "product can't be null";                 
    assert basket.containsKey(product) : "Product must already be in  
    ➥ the basket";                                                   
    int qty = basket.get(product);
    BigDecimal productPrice = product.getPrice();             
    BigDecimal productTimesQuantity = productPrice.multiply(  
      ➥ valueOf(qty));                                       
    totalValue = totalValue.subtract(productTimesQuantity);   
Listing 5.13
Implementation of Baskets remove method
If the product 
is already in the 
cart, add to it.
Calculates the
previous and the
new value of the
product for the
relevant quantities
Subtracts the previous value of the 
product from the total value of the 
basket and adds the new final value 
of the product to it
Post-conditions and 
invariant checks
Pre-
conditions
check
Calculates the 
amount that 
should be removed 
from the basket


---
**Page 131**

131
Example 4: Testing the Basket class
    basket.remove(product); 
    assert !basket.containsKey(product) : "Product is still  
    ➥ in the basket";                                       
    assert invariant() : "Invariant does not hold";          
  }
A developer who did not read the chapters on specification-based testing and struc-
tural testing would come up with at least three tests: one to ensure that add() adds the
product to the cart, another to ensure that the method behaves correctly when
the same product is added twice, and one to ensure that remove() indeed removes
the product from the basket. Then they would probably add a few tests for the excep-
tional cases (which in this class are clearly specified in the contracts). Here are the
automated test cases.
import static java.math.BigDecimal.valueOf;
public class BasketTest {
  private Basket basket = new Basket();
  @Test
  void addProducts() { 
    basket.add(new Product("TV", valueOf(10)), 2);
    basket.add(new Product("Playstation", valueOf(100)), 1);
    assertThat(basket.getTotalValue())
        .isEqualByComparingTo(valueOf(10*2 + 100*1));
  }
  @Test
  void addSameProductTwice() { 
    Product p = new Product("TV", valueOf(10));
    basket.add(p, 2);
    basket.add(p, 3);
    assertThat(basket.getTotalValue())
        .isEqualByComparingTo(valueOf(10*5));
  }
  @Test
  void removeProducts() { 
    basket.add(new Product("TV", valueOf(100)), 1);
    Product p = new Product("PlayStation", valueOf(10));
    basket.add(p, 2);
    basket.remove(p);
    assertThat(basket.getTotalValue())
        .isEqualByComparingTo(valueOf(100)); 
  }
Listing 5.14
Non-systematic tests for the Basket class
Removes the product 
from the hashmap
Post-conditions 
and invariant 
check
Ensures that 
products are added 
to the basket
If the same product is 
added twice, the basket 
sums up the quantities.
Ensures that products are 
removed from the basket
Food for thought: is this 
assertion enough? You 
might also want to verify 
that PlayStation is not in 
the basket.


---
**Page 132**

132
CHAPTER 5
Property-based testing
  // tests for exceptional cases...
}
NOTE
I used the isEqualByComparingTo assert instruction. Remember that
BigDecimals are instances of a strange class, and the correct way to compare
one BigDecimal to another is with the compareTo() method. That is what the
isEqualByComparingTo assertion does. Again, the BigDecimal class is not
easy to handle.
The problem with these tests is that they do not exercise the feature extensively. If
there is a bug in our implementation, it is probably hidden and will only appear after
a long and unexpected sequence of adds and removes to and from the basket. Finding
this specific sequence might be hard to see, even after proper domain and structural
testing. However, we can express it as a property: given any arbitrary sequence of addi-
tions and removals, the basket still calculates the correct final amount. We have to cus-
tomize jqwik so that it understands how to randomly call a sequence of add()s and
remove()s, as shown in figure 5.2.
Fasten your seatbelt, because this takes a lot of code. The first step is to create a bunch
of jqwik Actions to represent the different actions that can happen with the basket.
Actions are a way to explain to the framework how to execute a more complex action.
In our case, two things can happen: we can add a product to the basket, or we can
remove a product from the basket. We define how these two actions work so that later,
jqwik can generate a random sequence of actions.
 Let’s start with the add action. It will receive a Product and a quantity and insert
the Product into the Basket. The action will then ensure that the Basket behaved as
expected by comparing its current total value against the expected value. Note that
everything happens in the run() method: this method is defined by jqwik’s Action
interface, which our action implements. In practice, jqwik will call this method when-
ever it generates an add action and passes the current basket to the run method. The
following listing shows the implementation of the AddAction class.
 
Add
Remove
Add
Add
Remove
Add
Add
Add
Remove
Add
Add
Add
Add
Remove
Add
Remove Remove
T1 =
T2 =
T3 =
We want to call arbitrary sequences
of adds and removes and assert that
the basket is still in a correct state.
T4 =
….
Figure 5.2
We want our test to call arbitrary sequences of add and remove 
actions.


---
**Page 133**

133
Example 4: Testing the Basket class
class AddAction
  implements Action<Basket> { 
  private final Product product;
  private final int qty;
  public AddAction(Product product, int qty) { 
    this.product = product;
    this.qty = qty;
  }
  @Override
  public Basket run(Basket basket) { 
    BigDecimal currentValue = basket.getTotalValue(); 
    basket.add(product, qty); 
    BigDecimal newProductValue = product.getPrice()
      .multiply(valueOf(qty));
    BigDecimal newValue = currentValue.add(newProductValue);
    assertThat(basket.getTotalValue())
      .isEqualByComparingTo(newValue); 
    return basket; 
  }
}
Now let’s implement the remove action. This is tricky: we need a way to get the set of
products that are already in the basket and their quantities. Note that we do not
have such a method in the Basket class. The simplest thing to do is add such a
method to the class.
 You might be thinking that adding more methods for the tests is a bad idea. It’s a
trade-off. I often favor anything that eases testing. An extra method will not hurt and
will help our testing, so I’d do it, as shown next.
class Basket {
  // ... the code of the class here ...
  public int quantityOf(Product product) { 
    assert basket.containsKey(product);
    return basket.get(product);
  }
  public Set<Product> products() { 
    return Collections.unmodifiableSet(basket.keySet());
  }
}
Listing 5.15
The AddAction action
Listing 5.16
Basket class modified to support the test
Actions have to implement the 
jqwik Action interface.
The constructor receives 
a product and a quantity. 
These values will be randomly 
generated later by jqwik.
The run method receives a 
Basket and, in this case, adds 
a new random product to it.
Gets the current total 
value of the basket, 
so we can make the 
assertion later
Adds the
product to
the basket
Asserts that the value of the basket 
is correct after the addition
Returns the current basket so 
the next action starts from it
We only return the quantity if 
the product is in the cart. Note 
that here, we could have gone 
for a weaker pre-condition: for 
example, if the product is not 
in the basket, return 0.
Returns a copy of 
the set, not the 
original one!


---
**Page 134**

134
CHAPTER 5
Property-based testing
The remove action picks a random product from the basket, removes it, and then
ensures that the current total value is the total value minus the value of the product
that was just removed. The pickRandom() method chooses a random product from
the set of products; I do not show the code here, to save space, but you can find it in
the book’s code repository.
class RemoveAction implements Action<Basket> {
  @Override
  public Basket run(Basket basket) {
    BigDecimal currentValue = basket.getTotalValue(); 
    Set<Product> productsInBasket = basket.products(); 
    if(productsInBasket.isEmpty()) {
      return basket;
    }
    Product randomProduct = pickRandom(productsInBasket); 
    double currentProductQty = basket.quantityOf(randomProduct);
    basket.remove(randomProduct);
    BigDecimal basketValueWithoutRandomProduct = currentValue
      .subtract(randomProduct.getPrice()
      .multiply(valueOf(currentProductQty))); 
    assertThat(basket.getTotalValue())
      .isEqualByComparingTo(basketValueWithoutRandomProduct); 
    return basket; 
  }
  // ...
}
Jqwik now knows how to call add() (via AddAction) and remove() (via RemoveAction).
The next step is to explain how to instantiate random products and sequences of
actions. Let’s start by explaining to jqwik how to instantiate an arbitrary AddAction.
First we randomly pick a product from a predefined list of products. Then we gener-
ate a random quantity value. Finally, we add the random product in the random quan-
tity to the basket.
class BasketTest {
  // ...
  private Arbitrary<AddAction> addAction() {
    Arbitrary<Product> products = Arbitraries.oneOf( 
      randomProducts
        .stream()
        .map(product -> Arbitraries.of(product))
        .collect(Collectors.toList()));
Listing 5.17
The RemoveAction class
Listing 5.18
Instantiating add actions
Gets the current
value of the
basket for the
assertion later
If the basket is 
empty, we skip this 
action. This may 
happen, as we do not 
control the sequence 
jqwik generates.
Picks a
random
element in
the basket
to be
removed
Calculates the new 
value of the basket
Asserts the value of the
basket without the random
product we removed
Returns the current 
basket so the next action 
can continue from here
Creates an arbitrary 
product out of the 
list of predefined 
products


---
**Page 135**

135
Example 4: Testing the Basket class
    Arbitrary<Integer> qtys =
      Arbitraries.integers().between(1, 100); 
    return Combinators
        .combine(products, qtys)
        .as((product, qty) -> new AddAction(product, qty)); 
  }
  static List<Product> randomProducts = new ArrayList<>() {{   
    add(new Product("TV", new BigDecimal("100")));
    add(new Product("PlayStation", new BigDecimal("150.3")));
    add(new Product("Refrigerator", new BigDecimal("180.27")));
    add(new Product("Soda", new BigDecimal("2.69")));
  }};
}
This is a complex piece of code, and it involves a lot of details about how jqwik works.
Let’s digest it step by step:
1
Our first goal is to randomly select an arbitrary Product from the list of products.
To do so, we use jqwik’s Arbitraries.oneOf() method, which randomly picks an
arbitrary element of a given set of options. Given that the oneOf method needs a
List<Arbitrary<Product>>, we have to convert our randomProducts (which
is a List<Product>). This is easily done using Java’s Stream API.
2
We generate a random integer that will serve as the quantity to pass to the add()
method. We define an Arbitrary<Integer> with numbers between 1 and 100
(random choices that I made after exploring the method’s source code).
3
We return an AddAction that is instantiated using a combination of arbitrary
products and quantities.
We can now create our test. The property test should receive an ActionSequence, which
we define as an arbitrary sequence of AddActions and RemoveActions. We do so with the
Arbitraries.sequences() method. Let’s define this in an addsAndRemoves method.
 We also need arbitrary remove actions, as we did for add actions, but this is much
simpler since the RemoveAction class does not receive anything in its constructor. So,
we use Arbitraries.of().
private Arbitrary<RemoveAction> removeAction() {
  return Arbitraries.of(new RemoveAction()); 
}
@Provide
Arbitrary<ActionSequence<Basket>> addsAndRemoves() {
  return Arbitraries.sequences(Arbitraries.oneOf( 
      addAction(),
      removeAction()));
}
Listing 5.19
Adding remove actions to the test
Creates arbitrary 
quantities
Combines products 
and quantities, and 
generates AddActions
A static list of 
hard-coded 
products
Returns an arbitrary 
remove action
This is where the magic 
happens: jqwik generates 
random sequences of add 
and remove actions.


---
**Page 136**

136
CHAPTER 5
Property-based testing
We now only need a @Property test method that runs the different sequences of
actions generated by the addsAndRemoves method.
@Property
void sequenceOfAddsAndRemoves(
  @ForAll("addsAndRemoves") 
  ActionSequence<Basket> actions) {
    actions.run(new Basket());
}
And we are finished. As soon as we run the test, jqwik randomly invokes sequences of
adds and removes, passing random Products and quantities and ensuring that the
value of the basket is always correct.
 This was a long, complex property-based test, and you may be wondering if it is
worth the effort. For this specific Basket implementation, I would probably write thor-
ough example-based tests. But I hope this example illustrates the power of property-
based testing. Although they tend to be more complicated than traditional example-
based tests, you will get used to it, and you will soon be writing them quickly. 
5.5
Example 5: Creating complex domain objects
Building more complex objects may come in handy when testing business systems.
This can be done using jqwik’s Combinators feature, which we’ll use in the following
listing. Imagine that we have the following Book class, and we need to generate differ-
ent books for a property-based test.
public class Book {
  private final String title;
  private final String author;
  private final int qtyOfPages;
  public Book(String title, String author, int qtyOfPages) {
    this.title = title;
    this.author = author;
    this.qtyOfPages = qtyOfPages;
  }
  // getters...
}
One way to do this would be to have a property test that receives three parameters: a
String for title, a String for author, and an Integer for quantity of pages. Inside
the property test, we would instantiate the Book class. Jqwik offers a better way to do
that, as shown in the next listing.
Listing 5.20
Property-based test that generates adds and removes
Listing 5.21
A simple Book class
The property receives 
a sequence of Basket 
actions defined by the 
addsAndRemoves method.


---
**Page 137**

137
Property-based testing in the real world
public class BookTest {
  @Property
  void differentBooks(@ForAll("books") Book book) {
    // different books!
    System.out.println(book);
    // write your test here!
  }
  @Provide
  Arbitrary<Book> books() {
    Arbitrary<String> titles = Arbitraries.strings().withCharRange(
      ➥ 'a', 'z')
        .ofMinLength(10).ofMaxLength(100); 
    Arbitrary<String> authors = Arbitraries.strings().withCharRange(
      ➥ 'a', 'z')
        .ofMinLength(5).ofMaxLength(21);   
    Arbitrary<Integer> qtyOfPages = Arbitraries.integers().between(
      ➥ 0, 450); 
    return Combinators.combine(titles, authors, qtyOfPages)
        .as((title, author, pages) -> new Book(title, author, pages)); 
  }
}
The Combinators API lets us combine different generators to build a more complex
object. All we have to do is to build specific Arbitrarys for each of the attributes of the
complex class we want to build: in this case, one Arbitrary<String> for the title,
another Arbitrary<String> for the author, and one Arbitrary<Integer> for the num-
ber of pages. After that, we use the Combinators.combine() method, which receives a
series of Arbitrarys and returns an Arbitrary of the complex object. The magic hap-
pens in the as() method, which gives us the values we use to instantiate the object.
 Note how flexible jqwik is. You can build virtually any object you want. Moreover,
nothing prevents you from building even more realistic input values: for example,
instead of building random author names, we could develop something that returns
real people’s names. Try implementing such an arbitrary yourself. 
5.6
Property-based testing in the real world
Let me give you some tips on writing property-based tests.
5.6.1
Example-based testing vs. property-based testing
Property-based testing seems much fancier than example-based testing. It also explores
the input domain much better. Should we only use property-based testing from now on?
 In practice, I mix example-based testing and property-based testing. In the testing
workflow I propose, I use example-based testing when doing specification-based and
structural testing. Example-based tests are naturally simpler than property-based tests,
Listing 5.22
Using the Combinators API to generate complex objects
Instantiates
one arbitrary
for each of the
Book’s fields
Combines them
to generate an
instance of Book


---
**Page 138**

138
CHAPTER 5
Property-based testing
and they require less creativity to automate. I like that: their simplicity allows me to
focus on understanding the requirements and engineer better test cases. When I am
done with both testing techniques and have a much better grasp of the program
under test, I evaluate which test cases would be better as property-based tests.
 Do I always write property-based tests for my programs? Honestly, no. In many of the
problems I work on, I feel pretty confident with example-based testing. I use property-
based testing when I do not feel entirely secure that my example-based tests were
enough. 
5.6.2
Common issues in property-based tests
I see three common issues in the property-based tests my students write when they
learn this technique. The first is requiring jqwik to generate data that is very expensive
or even impossible. If you ask jqwik to, say, generate an array of 100 elements in which
the numbers have to be unique and multiples of 2, 3, 5, and 15, such an array can be
difficult to find, given jqwik’s random approach. Or if you want an array with 10
unique elements, but you give jqwik a range of 2 to 8, the array is impossible to gener-
ate. In general, if jqwik is taking too long to generate the data for you, maybe you can
find a better way to generate the data or write the test.
 Second, we saw in previous chapters that boundaries are a perfect place for bugs.
So, we want to exercise those boundaries when writing property-based tests. Ensure
that you are expressing the boundaries of the property correctly. When we wrote the
tests for the passing-grade problem (section 5.1), we wrote arbitraries like Arbitraries
.floats().lessThan(1f) and Arbitraries.floats().greaterThan(10f). Jqwik will
do its best to generate boundary values: for example, the closest possible number to
1f or the smallest possible float. The default configuration for jqwik is to mix edge
cases with random data points. Again, all of this will work well only if you express the
properties and boundaries correctly.
 The third caveat is ensuring that the input data you pass to the method under test
is fairly distributed among all the possible options. Jqwik does its best to generate well-
distributed inputs. For example, if you ask for an integer between 0 and 10, all the
numbers in the interval will have the same probability of being generated. But I have
seen tests that manipulate the generated data and then harm this property. For exam-
ple, imagine testing a method that receives three integers, a, b, and c, and returns a
boolean indicating whether these three sides can form a triangle. The implementa-
tion of this method is simple, as shown in the following listing.
public class Triangle {
  public static boolean isTriangle(int a, int b, int c) {
    boolean hasABadSide = a >= (b + c) || c >= (b + a) || b >= (a + c);
    return !hasABadSide;
  }
}
Listing 5.23
Implementation of the isTriangle method


---
**Page 139**

139
Summary
To write a property-based test for this method, we need to express two properties:
valid triangles and invalid triangles. If the developer generates three random integer
values as shown next, there is a very low chance of them forming a valid triangle.
@Property
void triangleBadTest( 
  @ForAll @IntRange(max = 100) int a,
  @ForAll @IntRange(max = 100) int b,
  @ForAll @IntRange(max = 100) int c) {
   // ... test here ...
}
The test exercises the invalid triangle property more than the valid triangle property.
A good property-based test for this problem would ensure that jqwik generates the
same number of valid and invalid triangles. The easiest way to do that would be to split
it into two tests: one for valid triangles and one for invalid triangles. (The solution is
available in the code repository.) 
5.6.3
Creativity is key
Writing property-based tests requires a lot of creativity from the developer. Finding
ways to express the property, generating random data, and being able to assert the
expected behavior without knowing the concrete input is not easy. Property-based
testing requires more practice than traditional example-based testing: get your hands
dirty as soon as possible. I hope the examples have given you some ideas!
Exercises
5.1
What is the main difference between example-based testing and property-based
testing?
5.2
Suppose we have a method that returns true if the passed string is a palin-
drome or false otherwise. (A palindrome is a word or sentence that reads the
same backward and forward.) What properties do you see that could be tested
via property-based tests? Also describe how you would implement such tests.
5.3
Find out what fuzz testing or fuzzing is. What is the difference between property-
based testing and fuzzing?
Summary
In property-based testing, instead of coming up with concrete examples, we
express the property that should hold for that method. The framework then
randomly generates hundreds of different inputs.
Listing 5.24
A bad property-based test for isTriangle
Generates three different integers. The 
odds are that these a, b, and c will be 
an invalid triangle. We therefore do not 
exercise the valid triangle property as 
much as we wanted to.


---
**Page 140**

140
CHAPTER 5
Property-based testing
Property-based testing does not replace specification-based testing and struc-
tural testing. It is one more tool to have in your belt. Sometimes traditional
example-based testing is enough.
Writing property-based tests is a tad more challenging than example-based test-
ing. You have to be creative to express the properties. Practice is key.


---
**Page 141**

141
Test doubles and mocks
Until now, we have been testing classes and methods that were isolated from each
other. We passed the inputs to a single method call and asserted its output. Or,
when a class was involved, we set up the state of the class, called the method under
test, and asserted that the class was in the expected state.
 But some classes depend on other classes to do their job. Exercising (or testing)
many classes together may be desirable. We often break down complex behavior into
multiple classes to improve maintainability, each with a small part of the business
logic. We still want to ensure, however, that the whole thing works together; we will
discuss this in chapter 9. This chapter focuses on testing that unit in an isolated fash-
ion without caring too much about its dependencies. But why would we want that?
 The answer is simple: because exercising the class under test together with its
concrete dependencies might be too slow, too hard, or too much work. As an exam-
ple, consider an application that handles invoices. This system has a class called
This chapter covers
Using stubs, fakes, and mocks to simplify testing
Understanding what to mock, when to mock, and 
when not to mock
How to mock the unmockable



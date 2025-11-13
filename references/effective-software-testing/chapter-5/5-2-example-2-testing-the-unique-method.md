# 5.2 Example 2: Testing the unique method (pp.122-124)

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



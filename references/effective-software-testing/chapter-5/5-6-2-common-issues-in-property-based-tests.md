# 5.6.2 Common issues in property-based tests (pp.138-139)

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



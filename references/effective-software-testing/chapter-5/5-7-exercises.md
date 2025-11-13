# 5.7 Exercises (pp.139-139)

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



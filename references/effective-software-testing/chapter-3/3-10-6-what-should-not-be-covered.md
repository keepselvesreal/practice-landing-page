# 3.10.6 What should not be covered? (pp.90-90)

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



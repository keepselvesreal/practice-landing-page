# 7.3.2 Other forms of logic (pp.155-156)

---
**Page 155**

155
7.3
Avoiding logic in unit tests
higher-level tests should be considered a bit riskier; they often create expected results
dynamically, which you should try to avoid any time you can.
 “But Roy,” you might say, “Now we are repeating ourselves—the string "abc" is
repeated twice. We were able to avoid this in the previous test.” When push comes to
shove, trust should trump maintainability. What good is a highly maintainable test that
I cannot trust? You can read more about code duplication in tests in Vladimir
Khorikov’s article, “DRY vs. DAMP in Unit Tests,” (https://enterprisecraftsmanship
.com/posts/dry-damp-unit-tests/).
7.3.2
Other forms of logic
Here’s the opposite case: creating the inputs dynamically (using a loop) forces us to
dynamically decide what the expected output should be. Suppose we have the follow-
ing code to test.
const isName = (input) => {
  return input.split(" ").length === 2;
};
The following listing shows a clear antipattern for a test.
describe("isName", () => {
  const namesToTest = ["firstOnly", "first second", ""];   
  it("correctly finds out if it is a name", () => {
    namesToTest.forEach((name) => {
      const result = trust.isName(name);
      if (name.includes(" ")) {       
        expect(result).toBe(true);    
      } else {                        
        expect(result).toBe(false);   
      }
    });
  });
});
Notice how we’re using multiple inputs for the test. This forces us to loop over those
inputs, which in itself complicates the test. Remember, loops can have bugs too. 
 Additionally, because we have different scenarios for the values (with and without
spaces) we need an if/else to know what the assertion is expecting, and the if/else
can have bugs too. We are also repeating a part of the production algorithm, which
brings us back to the previous concatenation example and its problems.
 Finally, our test name is too generic. We can only title it as “it works” because we have
to account for multiple scenarios and expected outcomes. That’s bad for readability.
Listing 7.4
A name-finding function
Listing 7.5
Loops and ifs in a test
Declaring 
multiple inputs
Production code 
logic leaking into 
the test


---
**Page 156**

156
CHAPTER 7
Trustworthy tests
 This is an all-around bad test. It’s better to separate this into two or three tests,
each with its own scenario and name. This would allow us to use hardcoded inputs
and assertions and to remove any loops and if/else logic from the code. Anything
more complex causes the following problems:
The test is harder to read and understand.
The test is hard to recreate. For example, imagine a multithreaded test or a test
with random numbers that suddenly fails.
The test is more likely to have a bug or to verify the wrong thing.
Naming the test may be harder because it does multiple things.
Generally, monster tests replace original simpler tests, and that makes it harder to find
bugs in the production code. If you must create a monster test, it should be added as a
new test and not be a replacement for existing tests. Also, it should reside in a project
or folder explicitly titled to hold tests other than unit tests. I call these “integration
tests” or “complex tests” and try to keep their number to an acceptable minimum.
7.3.3
Even more logic
Logic can be found not only in tests but also in test helper methods, handwritten
fakes, and test utility classes. Remember, every piece of logic you add in these places
makes the code that much harder to read and increases the chances of a bug in a util-
ity method that your tests use. 
 If you find that you need to have complicated logic in your test suite for some rea-
son (though that’s generally something I do with integration tests, not unit tests), at
least make sure you have a couple of tests against the logic of your utility methods in
the test project. This will save you many tears down the road.
7.4
Smelling a false sense of trust in passing tests
We’ve now covered failed tests as a means of detecting tests we shouldn’t trust. What
about all those quiet, green tests we have lying all over the place? Should we trust
them? What about a test that we need to do a code review for, before it’s pushed into a
main branch? What should we look for?
 Let’s use the term “false-trust” to describe trusting a test that you really shouldn’t,
but you don’t know it yet. Being able to review tests and find possible false-trust issues
has immense value because, not only can you fix those tests yourself, you’re affecting
the trust of everyone else who’s ever going to read or run those tests. Here are some
reasons I reduce my trust in tests, even if they are passing:
The test contains no asserts.
I can’t understand the test.
Unit tests are mixed with flaky integration tests.
The test verifies multiple concerns or exit points.
The test keeps changing.



# 7.3.1 Logic in asserts: Creating dynamic expected values (pp.153-155)

---
**Page 153**

153
7.3
Avoiding logic in unit tests
WHAT CAN YOU DO NOW?
The root cause is that one of the tests has become irrelevant, which means it needs to
be removed. Which one should be removed? That’s a question we’d need to ask a
product owner, because the answer is related to which behavior is correct and
expected from the application. 
AVOIDING THIS IN THE FUTURE
I feel this is a healthy dynamic, and I’m fine with not avoiding it. 
7.2.5
The test is flaky
A test can fail inconsistently. Even if the production code under test hasn’t changed, a
test can suddenly fail without any apparent reason, then pass again, then fail again.
We call a test like that “flaky.” 
 Flaky tests are a special beast, and I’ll deal with them in section 7.5.
7.3
Avoiding logic in unit tests
The chances of having bugs in your tests increase almost exponentially as you include
more and more logic in them. I’ve seen plenty of tests that should have been simple
become dynamic, random-number-generating, thread-creating, file-writing monsters
that are little test engines in their own right. Sadly, because they were “tests,” the
writer didn’t consider that they might have bugs or didn’t write them in a maintain-
able manner. Those test monsters take more time to debug and verify than they save. 
 But all monsters start out small. Often, an experienced developer in the company
will look at a test and start thinking, “What if we made the function loop and create
random numbers as input? We’d surely find lots more bugs that way!” And you will,
especially in your tests. 
 Test bugs are one of the most annoying things for developers, because you’ll
almost never search for the cause of a failing test in the test itself. I’m not saying that
tests with logic don’t have any value. In fact, I’m likely to write such tests myself in
some special situations. But I try to avoid this practice as much as possible. 
 If you have any of the following inside a unit test, your test contains logic that I usu-
ally recommend be reduced or removed completely:

switch, if, or else statements

foreach, for, or while loops
Concatenations (+ sign, etc.)

try, catch
7.3.1
Logic in asserts: Creating dynamic expected values
Here’s a quick example of a concatenation to start us off.
describe("makeGreeting", () => {
  it("returns correct greeting for name", () => {
Listing 7.1
A test with logic in it


---
**Page 154**

154
CHAPTER 7
Trustworthy tests
    const name = "abc";
    const result = trust.makeGreeting(name);
    expect(result).toBe("hello" + name);    
  });
To understand the problem with this test, the following listing shows the code being
tested. Notice that the + sign makes an appearance in both. 
const makeGreeting = (name) => {
  return "hello" + name;      
};
Notice how the algorithm (very simple, but still an algorithm) of connecting a name
with a "hello" string is repeated in both the test and the code under test:
expect(result).toBe("hello" + name);   
return "hello" + name;   
My issue with this test is that the algorithm under test is repeated in the test itself. This
means that if there is a bug in the algorithm, the test also contains the same bug. The
test will not catch the bug, but instead will expect the incorrect result from the code
under test. 
 In this case, the incorrect result is that we’re missing a space character between the
concatenated words, but hopefully you can see how the same issue could become
much more complex with a more complex algorithm.
 This is a trust issue. We can’t trust this test to tell us the truth, since its logic is a
repeat of the logic being tested. The test might pass when the bug exists in the code,
so we can’t trust the test’s result.
WARNING
Avoid dynamically creating the expected value in your asserts; use
hardcoded values when possible. 
A more trustworthy version of this test can be rewritten as follows.
it("returns correct greeting for name 2", () => {
  const result = trust.makeGreeting("abc");
  expect(result).toBe("hello abc");    
});
Because the inputs in this test are so simple, it’s easy to write a hardcoded expected
value. This is what I usually recommend—make the test inputs so simple that it is triv-
ial to create a hardcoded version of the expected value. Note that this is mostly true of
unit tests. For higher-level tests, this is a bit harder to do, which is another reason why
Listing 7.2
Code under test
Listing 7.3
A more trustworthy test
Logic in the 
assertion part
The same logic as in 
the production code
Our test
The code under test
Using a hardcoded value


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



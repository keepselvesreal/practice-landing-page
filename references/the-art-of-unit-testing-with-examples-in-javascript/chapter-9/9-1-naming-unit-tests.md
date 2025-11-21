# 9.1 Naming unit tests (pp.188-189)

---
**Page 188**

188
CHAPTER 9
Readability
9.1
Naming unit tests
Naming standards are important because they give you comfortable rules and tem-
plates that outline what you should explain about the test. No matter how I order
them, or what specific framework or language I am using, I try to make sure these
three important pieces of information are present in the name of the test or in the
structure of the file in which the test exists:
The entry point to the unit of work (or the name of the feature being tested)
The scenario under which you’re testing the entry point
The expected behavior of the exit point of the unit of work
The name of the entry point (or unit of work) is essential, so that you can easily
understand the starting scope of the logic being tested. Having this as the first part of
the test name also allows for easy navigation and as-you-type completion (if your IDE
supports it) in the test file.
 The scenario under which it’s being tested gives you the “with” part of the name:
“When I call entry point X with a null value, then it should do Y.”
 The expected behavior from the exit point of the unit of work is where the test
specifies in plain English what the unit of work should do or return, or how it should
behave, based on the current scenario: “When I call entry point X with a null value,
then it should do Y as visible from this exit point of the unit of work.”
 These three elements have to exist somewhere close to the eyes of the person read-
ing the test. Sometimes they can all be encapsulated in the test’s function name, and
sometimes you can include them with nested describe structures. Sometimes you can
simply use a string description as a parameter or annotation for the test.
 Some examples are shown in the following listing, all with the same pieces of infor-
mation, but laid out differently. 
test('verifyPassword, with a failing rule, returns error based on 
rule.reason', () => { … }
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    it('returns error based on the rule.reason', () => { ... }
verifyPassword_withFailingRule_returnsErrorBasedonRuleReason()
You can, of course, come up with other ways to structure this. (Who says you have to
use underscores? That’s just my own preference for reminding me and others that
there are three pieces of information.). The key point to take away is that if you
remove one of these pieces of information, you’re forcing the person reading the test
to read the code inside the test to find out the answer, wasting precious time. 
 The following listing shows examples of tests with missing information.
Listing 9.1
Same information, different variations


---
**Page 189**

189
9.2
Magic values and naming variables
test(failing rule, returns error based on rule.reason', () => { ... }  
test('verifyPassword, returns error based on rule.reason', () => { ... }   
test('verifyPassword, with a failing rule', () => { ... }   
Your main goal with readability is to release the next developer from the burden of
reading the test code in order to understand what the test is testing.
 Another great reason to include all these pieces of information in the name of the
test is that the name is usually the only thing that shows up when an automated build
pipeline fails. You’ll see the names of the failed tests in the log of the build that failed,
but you won’t see any comments or the code of the tests. If the names are good
enough, you might not need to read the code of the tests or debug them; you may
understand the cause of the failure simply by reading the log of the failed build. This
can save precious debugging and reading time.
 A good test name also serves to contribute to the idea of executable documenta-
tion—if you can ask a developer who is new to the team to read the tests so they can
understand how a specific component or application works, that’s a good sign of read-
ability. If they can’t make sense of the application or the component’s behavior from
the tests alone, it might be a red flag for readability. 
9.2
Magic values and naming variables
Have you heard the term “magic values”? It sounds awesome, but it’s the opposite of
that. It should really be “witchcraft values” to convey the negative effects of using
them. What are they, you ask? They are hardcoded, undocumented, or poorly under-
stood constants or variables. The reference to magic indicates that these values work,
but you have no idea why.
 Consider the following test.
describe('password verifier', () => {
  test('on weekends, throws exceptions', () => {
    expect(() => verifyPassword('jhGGu78!', [], 0))   
      .toThrowError("It's the weekend!");
  });
});
This test contains three magic values. Can a person who didn’t write the test and
doesn't know the API being tested easily understand what the 0 value means? How
about the [] array? The first parameter to that function kind of looks like a password,
but even that has a magical quality to it. Let’s discuss:
Listing 9.2
Test names with missing information
Listing 9.3
A test with magic values
What is the thing under test?
When is this supposed to happen?
What’s supposed 
to happen then?
Magic 
values



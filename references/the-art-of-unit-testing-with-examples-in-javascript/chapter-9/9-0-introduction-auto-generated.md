# 9.0 Introduction [auto-generated] (pp.187-188)

---
**Page 187**

187
Readability
Without readability, the tests you write are almost meaningless to whoever reads
them later on. Readability is the connecting thread between the person who wrote
the test and the poor soul who must read it a few months or years later. Tests are
stories you tell the next generation of programmers on a project. They allow a
developer to see exactly what an application is made of and where it started.
 This chapter is all about making sure the developers who come after you will be
able to maintain the production code and the tests that you write. They’ll need to
understand what they’re doing and where they should be doing it.
 There are several facets to readability:
Naming unit tests
Naming variables
Separating asserts from actions
Setting up and tearing down
Let’s go through these one by one.
This chapter covers
Naming conventions for unit tests
Writing readable tests


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



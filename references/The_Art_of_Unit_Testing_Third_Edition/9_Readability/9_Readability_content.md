
--- 페이지 215 ---
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

--- 페이지 216 ---
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

--- 페이지 217 ---
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

--- 페이지 218 ---
190
CHAPTER 9
Readability
The 0 could mean so many things. As the reader, I might have to search around
in the code, or jump into the signature of the called function, to understand
that this specifies the day of the week. 
The [] forces me to look at the signature of the called function to understand
that the function expects a password verification rule array, which means the
test verifies the case with no rules.

jhGGu78! seems to be an obvious password value, but the big question I’ll have
as a reader is, why this specific value? What’s important about this specific pass-
word? It’s obviously important to use this value and not any other for this test,
because it seems so damned specific. In reality it isn’t, but the reader won’t
know this. They’ll likely end up using this password in other tests just to be safe.
Magic values tend to propagate themselves in tests.
The following listing shows the same test with the magic values fixed.
describe("verifier2 - dummy object", () => {
  test("on weekends, throws exceptions", () => {
    const SUNDAY = 0, NO_RULES = [];
    expect(() => verifyPassword2("anything", NO_RULES, SUNDAY))
      .toThrowError("It's the weekend!");
  });
});
By putting magic values into meaningfully named variables, we can remove the ques-
tions people will have when reading our test. For the password value, I’ve decided to
simply change the direct value to explain to the reader what is not important about
this test.
 Variable names and values are just as much about explaining to the reader what
they should not care about as they are about explaining what is important.
9.3
Separating asserts from actions
For the sake of readability and all that is holy, avoid writing assertions and the method
call in the same statement. The following listing shows what I mean.
expect(verifier.verify("any value")[0]).toContain("fake reason");   
const result = verifier.verify("any value");  
expect(result[0]).toContain("fake reason");   
See the difference between the two examples? The first example is much harder to
read and understand in the context of a real test because of the length of the line and
the nesting of the act and assert parts. 
Listing 9.4
Fixing magic values
Listing 9.5
Separating asserts from actions
Bad example
Good 
example

--- 페이지 219 ---
191
9.4
Setting up and tearing down
 It’s also much easier to debug the second example than the first one, if you wanted
to focus on the result value after the call. Don’t skimp on this small tip. The people
after you will whisper a small thank you when your test doesn’t make them feel stupid
for not understanding it.
9.4
Setting up and tearing down
Setup and teardown methods in unit tests can be abused to the point where the tests
or the setup and teardown methods are unreadable. The situation is usually worse in
the setup method than in the teardown method.
 The following listing shows one possible abuse that is very common: using the
setup (or beforeEach function) for setting up mocks or stubs.
describe("password verifier", () => {
  let mockLog;
  beforeEach(() => {
    mockLog = Substitute.for<IComplicatedLogger>();  
  });
  test("verify, with logger & passing, calls logger with PASS",() => {
    const verifier = new PasswordVerifier2([], mockLog);  
    verifier.verify("anything");
    mockLog.received().info(                              
      Arg.is((x) => x.includes("PASSED")),
      "verify"
    );
  });
}); 
If you set up mocks and stubs in a setup method, that means they don’t get set up in
the actual test. That, in turn, means that whoever is reading your test may not even
realize that there are mock objects in use, or what the test expects from them.
 The test in listing 9.6 uses the mockLog variable, which is initialized in the
beforeEach function (a setup method). Imagine you have dozens or more of these
tests in the file. The setup function is at the beginning of the file, and you are stuck
reading a test way down in the file. You come across the mockLog variable and you
have to start asking questions such as, “Where is this initialized? How will it behave
in the test?” and more. 
 Another problem that can arise if multiple mocks and stubs are used in various
tests in the same file is that the setup function becomes a dumping group for all the
various states used by your tests. It becomes a big mess, a soup of many parameters,
some used by one test and others used somewhere else. It becomes difficult to manage
and understand such a setup. 
 It’s much more readable to initialize mock objects directly in the test, with all their
expectations. The following listing is an example of initializing the mock in each test. 
Listing 9.6
Using a setup (beforeEach) function for mock setup
Setting up 
a mock
Using the
mock

--- 페이지 220 ---
192
CHAPTER 9
Readability
describe("password verifier", () => {
  test("verify, with logger & passing,calls logger with PASS",() => {
    const mockLog = Substitute.for<IComplicatedLogger>();   
    const verifier = new PasswordVerifier2([], mockLog);
    verifier.verify("anything");
    mockLog.received().info(
      Arg.is((x) => x.includes("PASSED")),
      "verify"
    );
  });
When I look at this test, everything is clear as day. I can see when the mock is created,
its behavior, and anything else I need to know. 
 If you’re worried about maintainability, you can refactor the creation of the mock
into a helper function that each test would call. That way, you’re avoiding the generic
setup function and are instead calling the same helper function from multiple tests.
As the following listing shows, you keep the readability and gain more maintainability.
describe("password verifier", () => {
  test("verify, with logger & passing,calls logger with PASS",() => {
    const mockLog = makeMockLogger();        
    const verifier = new PasswordVerifier2([], mockLog);
    verifier.verify("anything");
    mockLog.received().info(
      Arg.is((x) => x.includes("PASSED")),
      "verify"
    );
  });
And yes, if you follow this logic, you can see that I’m perfectly OK with you not having
any setup functions in your tests. I’ve often written full test suites that don’t have a
setup function, instead calling helper methods from each test, for the sake of main-
tainability. The tests were still readable and maintainable.
Summary
When naming a test, include the name of the unit of work under test, the cur-
rent test scenario, and the expected behavior of the unit of work.
Don’t leave magic values in your tests. Either wrap them in variables with mean-
ingful names, or put the description into the value itself, if it’s a string.
Listing 9.7
Avoiding a setup function
Listing 9.8
Using a helper function
Initializing 
the mock 
in the test 
Using a helper 
function to 
initialize the 
mock

--- 페이지 221 ---
193
Summary
Separate assertions from actions. Merging the two shortens the code but makes
it significantly harder to understand.
Try not to use test setups at all (such as beforeEach methods). Introduce helper
methods to simplify the test’s arrange part, and use those helper methods in
each test.

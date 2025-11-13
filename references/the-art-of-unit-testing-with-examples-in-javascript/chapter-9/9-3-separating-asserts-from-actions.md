# 9.3 Separating asserts from actions (pp.190-191)

---
**Page 190**

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


---
**Page 191**

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



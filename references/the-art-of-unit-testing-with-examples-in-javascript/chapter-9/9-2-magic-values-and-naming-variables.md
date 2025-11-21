# 9.2 Magic values and naming variables (pp.189-190)

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



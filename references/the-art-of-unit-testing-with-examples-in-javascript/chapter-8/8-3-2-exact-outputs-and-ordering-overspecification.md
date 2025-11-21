# 8.3.2 Exact outputs and ordering overspecification (pp.179-183)

---
**Page 179**

179
8.3
Avoid overspecification
test, for no real benefit. When the internal calls change (and they will) we will also
have to change all the tests associated with these calls, and that will not be a positive
experience. You can read more about mocks and their relation to test fragility in
chapter 5 of Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov (Man-
ning, 2020).
WHAT SHOULD WE DO INSTEAD?
Look for the exit point. The real exit point depends on the type of test we wish to
perform:
Value-based test—For a value-based test, which I would highly recommend you
lean toward when possible, we look for a return value from the called function.
In this case, the verify function returns a value, so it’s the perfect candidate for
a value-based test: pv4.verify("abc").
State-based test—For a state-based test, we look for a sibling function (a function
that exists at the same level of scope as the entry point) or a sibling property
that is affected by calling the verify() function. For example, firstname()
and lastname() could be considered sibling functions. That is where we should
be asserting. In this codebase, nothing is affected by calling verify() that is vis-
ible at the same level, so it is not a good candidate for state-based testing.
Third-party test—For a third-party test, we would have to use a mock, and that
would require us to find out where the fire-and-forget location is inside the
code. The findFailedRules function isn’t that, because it is actually delivering
information back to our verify() function. In this case, there’s no real third-
party dependency that we have to take over.
8.3.2
Exact outputs and ordering overspecification
A common antipattern is when a test overspecifies the order and the structure of a col-
lection of returned values. It’s often easier to specify the whole collection, along with
each of its items, in the assertion, but with this approach, we implicitly take on the
burden of fixing the test when any little detail of the collection changes. Instead of
using a single huge assertion, we should separate different aspects of the verification
into smaller, explicit asserts.
 The following listing shows a verify() function that takes on multiple inputs and
returns a list of result objects.
interface IResult {
  result: boolean;
  input: string;
}
export class PasswordVerifier5 {
  private _rules: ((input: string) => boolean)[];
Listing 8.13
A verifier that returns a list of outputs


---
**Page 180**

180
CHAPTER 8
Maintainability
  constructor(rules: ((input) => boolean)[]) {
    this._rules = rules;
  }
  verify(inputs: string[]): IResult[] {
    const failedResults = 
      inputs.map((input) => this.checkSingleInput(input));
    return failedResults;
  }
  private checkSingleInput(input: string): IResult {
    const failed = this.findFailedRules(input);
    return {
      input,
      result: failed.length === 0,
    };
  }
This verify() function returns an array of IResult objects with an input and result
in each. The following listing shows a test that makes an implicit check on both the
ordering of the results and the structure of each result, as well as checking the value of
the results.
test("overspecify order and schema", () => {
  const pv5 = 
    new PasswordVerifier5([input => input.includes("abc")]);
  const results = pv5.verify(["a", "ab", "abc", "abcd"]);
  expect(results).toEqual([           
    { input: "a", result: false },    
    { input: "ab", result: false },   
    { input: "abc", result: true },   
    { input: "abcd", result: true },  
  ]);
});
How might this test change in the future? Here are quite a few reasons for it to change:
When the length of the results array changes
When each result object gains or removes a property (even if the test doesn’t
care about those properties)
When the order of the results changes (even if it might not be important for
the current test)
If any of these changes happens in the future, but your test is just focused on checking
the logic of the verifier and the structure of its output, there’s going to be a lot of pain
involved in maintaining this test.
 We can reduce some of that pain by verifying only the parts that matter to us.
Listing 8.14
Overspecifying order and schema of the result 
A single 
huge assert


---
**Page 181**

181
8.3
Avoid overspecification
test("overspecify order but ignore schema", () => {
  const pv5 = 
    new PasswordVerifier5([(input) => input.includes("abc")]);
  const results = pv5.verify(["a", "ab", "abc", "abcd"]);
  expect(results.length).toBe(4);
  expect(results[0].result).toBe(false);
  expect(results[1].result).toBe(false);
  expect(results[2].result).toBe(true);
  expect(results[3].result).toBe(true);
});
Instead of providing the full expected output, we can simply assert on the values of
specific properties in the output. However, we’re still stuck if the order of the results
changes. If we don’t care about the order, we can simply check if the output contains a
specific result, as follows.
test("ignore order and schema", () => {
  const pv5 = 
    new PasswordVerifier5([(input) => input.includes("abc")]);
  const results = pv5.verify(["a", "ab", "abc", "abcd"]);
  expect(results.length).toBe(4);
  expect(findResultFor("a")).toBe(false);
  expect(findResultFor("ab")).toBe(false);
  expect(findResultFor("abc")).toBe(true);
  expect(findResultFor("abcd")).toBe(true);
});
Here we are using findResultFor() to find the specific result for a given input. Now
the order of the results can change, or extra values can be added, but our test will only
fail if the calculation of the true or false results changes. 
 Another common antipattern people tend to repeat is to assert against hardcoded
strings in the unit’s return value or properties, when only a specific part of a string is
necessary. Ask yourself, “Can I check if a string contains something rather than equals
something?” Here’s a password verifier that gives us a message describing how many
rules were broken during a verification.
export class PasswordVerifier6 {
  private _rules: ((input: string) => boolean)[];
  private _msg: string = "";
Listing 8.15
Ignoring the schema of the results
Listing 8.16
Ignoring order and schema
Listing 8.17
A verifier that returns a string message


---
**Page 182**

182
CHAPTER 8
Maintainability
  constructor(rules: ((input) => boolean)[]) {
    this._rules = rules;
  }
  getMsg(): string {
    return this._msg;
  }
  verify(inputs: string[]): IResult[] {
    const allResults = 
      inputs.map((input) => this.checkSingleInput(input));
    this.setDescription(allResults);
    return allResults;
  }
  private setDescription(results: IResult[]) {
    const failed = results.filter((res) => !res.result);
    this._msg = `you have ${failed.length} failed rules.`;
  }
The following listing shows two tests that use getMsg(). 
describe("verifier 6", () => {
  test("over specify string", () => {
    const pv5 = 
      new PasswordVerifier6([(input) => input.includes("abc")]);
    pv5.verify(["a", "ab", "abc", "abcd"]);
    const msg = pv5.getMsg();
    expect(msg).toBe("you have 2 failed rules.");   
  });
  //Here's a better way to write this test
  test("more future proof string checking", () => {
    const pv5 = 
      new PasswordVerifier6([(input) => input.includes("abc")]);
    pv5.verify(["a", "ab", "abc", "abcd"]);
    const msg = pv5.getMsg();
    expect(msg).toMatch(/2 failed/);    
  });
});
The first test checks that the string exactly equals another string. This backfires often,
because strings are a form of user interface. We tend to change them slightly and
embellish them over time. For example, do we care that there is a period at the end of
the string? Our test requires us to care, but the meat of the assert is the correct num-
ber being shown (especially since strings change in different computer languages or
cultures, but numbers usually stay the same).
Listing 8.18
Overspecifying a string using equality
Overly specific 
string expectation
A better way to assert 
against a string


---
**Page 183**

183
Summary
 The second test simply looks for the “2 failed” string inside the message. This
makes the test more future-proof: the string might change slightly, but the core mes-
sage remains without forcing us to change the test.
Summary
Tests grow and change with the system under test. If we don’t pay attention to
maintainability, our tests may require so many changes from us that it might not
be worth changing them. We may instead end up deleting them, and throwing
away all the hard work that went into creating them. For tests to be useful in the
long run, they should fail only for reasons we truly care about.
A true failure is when a test fails because it finds a bug in production code. A false
failure is when a test fails for any other reason.
To estimate test maintainability, we can measure the number of false test fail-
ures and the reason for each failure, over time.
A test may falsely fail for multiple reasons: it conflicts with another test (in
which case, you should just remove it); changes in the production code’s API
(this can be mitigated by using factory and helper methods); changes in other
tests (such tests should be decoupled from each other).
Avoid testing private methods. Private methods are implementation details, and
the resulting tests are going to be fragile. Tests should verify observable behavior—
behavior that is relevant for the end user. Sometimes, the need to test a private
method is a sign of a missing abstraction, which means the method should be
made public or even be extracted into a separate class.
Keep tests DRY. Use helper methods to abstract nonessential details of arrange
and assert sections. This will simplify your tests without coupling them to each
other.
Avoid setup methods such as the beforeEach function. Once again, use helper
methods instead. Another option is to parameterize your tests and therefore
move the content of the beforeEach block to the test’s arrange section.
Avoid overspecification. Examples of overspecification are asserting the private
state of the code under test, asserting against calls on stubs, or assuming the
specific order of elements in a result collection or exact string matches when
that isn’t required.



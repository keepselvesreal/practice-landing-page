# 8.3.1 Internal behavior overspecification with mocks (pp.177-179)

---
**Page 177**

177
8.3
Avoid overspecification
describe('sum with parameterized tests', () => {
    test.each([
        ['1', 1],   
        ['2', 2]    
    ])('add ,for %s, returns that number', (input, expected) => {
            const result = sum(input);       
            expect(result).toBe(expected);   
        }
    )
});
In the first describe block, we have two tests that repeat each other with different input
values and expected outputs. In the second describe block, we’re using test.each
to provide an array of arrays, where each subarray lists all the values needed for the
test function.
 Parameterized tests can help reduce a lot of duplication between tests, but we
should be careful to only use this technique in cases where we repeat the exact same
scenario and only change the input and output. 
8.3
Avoid overspecification
An overspecified test is one that contains assumptions about how a specific unit under
test (production code) should implement its internal behavior, instead of only check-
ing that the observable behavior (exit points) is correct. 
 Here are ways unit tests are often overspecified:
A test asserts purely internal state in an object under test.
A test uses multiple mocks.
A test uses stubs as mocks.
A test assumes a specific order or exact string matches when that isn’t required.
Let’s look at some examples of overspecified tests.
8.3.1
Internal behavior overspecification with mocks
A very common antipattern is to verify that an internal function in a class or module is
called, instead of checking the exit point of the unit of work. Here’s a password veri-
fier that calls an internal function, which the test shouldn’t care about.
export class PasswordVerifier4 {
  private _rules: ((input: string) => boolean)[];
  private _logger: IComplicatedLogger;
  constructor(rules: ((input) => boolean)[],
      logger: IComplicatedLogger) {
    this._rules = rules;
    this._logger = logger;
  }
Listing 8.11
Production code that calls a protected function
Test data used
for setup and
assertion
Setup and 
assertion without 
duplication


---
**Page 178**

178
CHAPTER 8
Maintainability
  verify(input: string): boolean {
    const failed = this.findFailedRules(input);   
    if (failed.length === 0) {
      this._logger.info("PASSED");
      return true;
    }
    this._logger.info("FAIL");
    return false;
  }
  protected findFailedRules(input: string) {  
    const failed = this._rules
      .map((rule) => rule(input))
      .filter((result) => result === false);
    return failed;
  }
}
Notice that we’re calling the protected findFailedRules function to get a result from
it, and then doing a calculation on the result. 
 Here’s our test.
describe("verifier 4", () => {
  describe("overspecify protected function call", () => {
    test("checkfailedFules is called", () => {
      const pv4 = new PasswordVerifier4(
        [], Substitute.for<IComplicatedLogger>()
      ); 
      const failedMock = jest.fn(() => []);    
      pv4["findFailedRules"] = failedMock;     
      pv4.verify("abc");
      expect(failedMock).toHaveBeenCalled();    
    });
  });
});
The antipattern here is that we’re proving something that isn’t an exit point. We’re
checking that the code calls some internal function, but what does that really prove?
We’re not checking that the calculation was correct on the result; we’re simply testing
for the sake of testing. 
 If the function is returning a value, usually that’s a strong indication that we
shouldn’t mock that function because the function call itself does not represent the
exit point. The exit point is the value returned from the verify() function. We
shouldn’t care whether the internal function even exists. 
 By verifying against a mock of a protected function that is not an exit point, we are
coupling our test implementation to the internal implementation of the code under
Listing 8.12
An overspecified test verifying a call to a protected function
Call to the 
internal 
function
Internal 
function
Mocking the 
internal function
Verifying the 
internal function 
call. Don’t do this.


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



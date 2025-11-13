# 2.7.0 Introduction [auto-generated] (pp.49-50)

---
**Page 49**

49
2.7
Trying the factory method route
Do we like this? I don’t. Now we’re seeing a couple of extra problems:
I can already start to see lots of repetition in the beforeEach() parts.
The potential for scroll fatigue has increased dramatically, with more options of
which beforeEach() affects which it() state.
In real projects, beforeEach() functions tend to be the garbage bin of the test file.
People throw all kinds of test-initialized stuff in there: things that only some tests need,
things that affect all the other tests, and things that nobody uses anymore. It’s human
nature to put things in the easiest place possible, especially if everyone else before you
has done so as well. 
 I’m not crazy about the beforeEach() approach. Let’s see if we can mitigate some
of these issues while still keeping duplication to a minimum. 
2.7
Trying the factory method route
Factory methods are simple helper functions that help us build objects or special states
and reuse the same logic in multiple places. Perhaps we can reduce some of the dupli-
cation and clunky-feeling code by using a couple of factory methods for the failing
and passing rules in listing 2.16.
describe('PasswordVerifier', () => {
  let verifier;
  beforeEach(() => verifier = new PasswordVerifier1());
  describe('with a failing rule', () => {
    let errors;
    beforeEach(() => {
      verifier.addRule(makeFailingRule('fake reason'));
      errors = verifier.verify('any value');
    });
    it('has an error message based on the rule.reason', () => {
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      expect(errors.length).toBe(1);
    });
  });
  describe('with a passing rule', () => {
    let errors;
    beforeEach(() => {
      verifier.addRule(makePassingRule());
      errors = verifier.verify('any value');
    });
    it('has no errors', () => {
      expect(errors.length).toBe(0);
    });
  });
  describe('with a failing and a passing rule', () => {
    let errors;
Listing 2.16
Adding a couple of factory methods to the mix


---
**Page 50**

50
CHAPTER 2
A first unit test
    beforeEach(() => {
      verifier.addRule(makePassingRule());
      verifier.addRule(makeFailingRule('fake reason'));
      errors = verifier.verify('any value');
    });
    it('has one error', () => {
      expect(errors.length).toBe(1);
    });
    it('error text belongs to failed rule', () => {
      expect(errors[0]).toContain('fake reason');
    });
  });
. . .
  const makeFailingRule = (reason) => {
    return (input) => {
      return { passed: false, reason: reason };
    };
  };
  const makePassingRule = () => (input) => {
    return { passed: true, reason: '' };
  };
}) 
The makeFailingRule() and makePassingRule() factory methods have made our
beforeEach() functions a little more clear.
2.7.1
Replacing beforeEach() completely with factory methods
What if we don’t use beforeEach() to initialize various things at all? What if we
switched to using small factory methods instead? Let’s see what that looks like.
const makeVerifier = () => new PasswordVerifier1();
const passingRule = (input) => ({passed: true, reason: ''});
const makeVerifierWithPassingRule = () => {
  const verifier = makeVerifier();
  verifier.addRule(passingRule);
  return verifier;
};
const makeVerifierWithFailedRule = (reason) => {
  const verifier = makeVerifier();
  const fakeRule = input => ({passed: false, reason: reason});
  verifier.addRule(fakeRule);
  return verifier;
};
describe('PasswordVerifier', () => {
  describe('with a failing rule', () => {
    it('has an error message based on the rule.reason', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
Listing 2.17
Replacing beforeEach() with factory methods



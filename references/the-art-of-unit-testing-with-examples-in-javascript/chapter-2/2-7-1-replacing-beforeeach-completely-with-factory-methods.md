# 2.7.1 Replacing beforeEach() completely with factory methods (pp.50-52)

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


---
**Page 51**

51
2.7
Trying the factory method route
      const errors = verifier.verify('any input');
      expect(errors[0]).toContain('fake reason');
    });
    it('has exactly one error', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
      const errors = verifier.verify('any input');
      expect(errors.length).toBe(1);
    });
  });
  describe('with a passing rule', () => {
    it('has no errors', () => {
      const verifier = makeVerifierWithPassingRule();
      const errors = verifier.verify('any input');
      expect(errors.length).toBe(0);
    });
  });
  describe('with a failing and a passing rule', () => {
    it('has one error', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
      verifier.addRule(passingRule);
      const errors = verifier.verify('any input');
      expect(errors.length).toBe(1);
    });
    it('error text belongs to failed rule', () => {
      const verifier = makeVerifierWithFailedRule('fake reason');
      verifier.addRule(passingRule);
      const errors = verifier.verify('any input');
      expect(errors[0]).toContain('fake reason');
    });
  });
});
The length here is about the same as in listing 2.16, but I find the code to be more
readable and thus more easily maintained. We’ve eliminated the beforeEach() func-
tions, but we didn’t lose maintainability. The amount of repetition we’ve eliminated is
negligible, but the readability has improved greatly due to the removal of the nested
beforeEach() blocks. 
 Furthermore, we’ve reduced the risk of scroll fatigue. As a reader of the test, I
don’t have to scroll up and down the file to find out when an object is created or
declared. I can glean all the information from the it(). We don’t need to know how
something is created, but we know when it is created and what important parameters it
is initialized with. Everything is explicitly explained.
 If the need arises, I can drill into specific factory methods, and I like that each
it() is encapsulating its own state. The nested describe() structure is a good way to
know where we are, but the state is all triggered from inside the it() blocks, not out-
side of them.


---
**Page 52**

52
CHAPTER 2
A first unit test
2.8
Going full circle to test()
The tests in listing 2.17 are self-encapsulated enough that the describe() blocks act
only as added sugar for understanding. They are no longer needed if we don’t want
them. If we wanted to, we could write the tests as in the following listing.
test('pass verifier, with failed rule, ' +
          'has an error message based on the rule.reason', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  const errors = verifier.verify('any input');
  expect(errors[0]).toContain('fake reason');
});
test('pass verifier, with failed rule, has exactly one error', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  const errors = verifier.verify('any input');
  expect(errors.length).toBe(1);
});
test('pass verifier, with passing rule, has no errors', () => {
  const verifier = makeVerifierWithPassingRule();
  const errors = verifier.verify('any input');
  expect(errors.length).toBe(0);
});
test('pass verifier, with passing  and failing rule,' +
          ' has one error', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  verifier.addRule(passingRule);
  const errors = verifier.verify('any input');
  expect(errors.length).toBe(1);
});
test('pass verifier, with passing  and failing rule,' +
          ' error text belongs to failed rule', () => {
  const verifier = makeVerifierWithFailedRule('fake reason');
  verifier.addRule(passingRule);
  const errors = verifier.verify('any input');
  expect(errors[0]).toContain('fake reason');
});
The factory methods provide us with all the functionality we need, without losing clar-
ity for each specific test. 
 I kind of like the terseness of listing 2.18. It’s easy to understand. We might lose a
bit of structure clarity here, so there are instances where I go with the describe-less
approach, and there are places where nested describes make things more readable.
The sweet spot of maintainability and readability for your project is probably some-
where between these two points. 
2.9
Refactoring to parameterized tests
Let’s move away from the verifier class to work on creating and testing a new custom
rule for the verifier. Listing 2.19 shows a simple rule for an uppercase letter (I realize
Listing 2.18
Removing nested describes



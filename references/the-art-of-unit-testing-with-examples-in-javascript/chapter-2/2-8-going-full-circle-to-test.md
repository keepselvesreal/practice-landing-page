# 2.8 Going full circle to test() (pp.52-52)

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



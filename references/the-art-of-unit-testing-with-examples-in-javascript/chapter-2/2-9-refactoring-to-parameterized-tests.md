# 2.9 Refactoring to parameterized tests (pp.52-55)

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


---
**Page 53**

53
2.9
Refactoring to parameterized tests
passwords with these requirements are no longer considered a great idea, but for
demonstration purposes I’m okay with it).
const oneUpperCaseRule = (input) => {
  return {
    passed: (input.toLowerCase() !== input),
    reason: 'at least one upper case needed'
  };
};
We could write a couple of tests as in the following listing.
describe('one uppercase rule', function () {
  test('given no uppercase, it fails', () => {
    const result = oneUpperCaseRule('abc');
    expect(result.passed).toEqual(false);
  });
  test('given one uppercase, it passes', () => {
    const result = oneUpperCaseRule('Abc');
    expect(result.passed).toEqual(true);
  });
  test('given a different uppercase, it passes', () => {
    const result = oneUpperCaseRule('aBc');
    expect(result.passed).toEqual(true);
  });
});
In listing 2.20 I highlighted some duplication we might have if we’re trying out the
same scenario with small variations in the input to the unit of work. In this case, we
want to test that it should not matter where the uppercase letter is, as long as it’s there.
But this duplication will hurt us down the road if we ever want to change the upper-
case logic, or if we need to correct the assertions in some way for that use case.
 There are a few ways to create parameterized tests in JavaScript, and Jest already
includes one that’s built in: test.each (also aliased to it.each). The next listing
shows how we could use this feature to remove duplication in our tests.
describe('one uppercase rule', () => {
  test('given no uppercase, it fails', () => {
    const result = oneUpperCaseRule('abc');
    expect(result.passed).toEqual(false);
  });
  test.each(['Abc',        
             'aBc'])       
    ('given one uppercase, it passes', (input) => {    
Listing 2.19
Password rules
Listing 2.20
Testing a rule with variations
Listing 2.21
Using test.each
Passing in an array 
of values that are 
mapped to the 
input parameter
Using each input 
parameter passed 
in the array


---
**Page 54**

54
CHAPTER 2
A first unit test
      const result = oneUpperCaseRule(input);
      expect(result.passed).toEqual(true);
    });
});
In this example, the test will repeat once for each value in the array. It’s a bit of a
mouthful at first, but once you’ve tried this approach, it becomes easy to use. It’s also
pretty readable. 
 If we want to pass in multiple parameters, we can enclose them in an array, as in
the following listing.
describe('one uppercase rule', () => {
  test.each([ ['Abc', true],           
              ['aBc', true],
              ['abc', false]])           
    ('given %s, %s ', (input, expected) => {   
      const result = oneUpperCaseRule(input);
      expect(result.passed).toEqual(expected);
    });
});
We don’t have to use Jest, though. JavaScript is versatile enough to allow us to roll out
our own parameterized test quite easily if we want to.
describe('one uppercase rule, with vanilla JS for', () => {
  const tests = {
    'Abc': true,
    'aBc': true,
    'abc': false,
  };
  for (const [input, expected] of Object.entries(tests)) {
    test('given ${input}, ${expected}', () => {
      const result = oneUpperCaseRule(input);
      expect(result.passed).toEqual(expected);
    });
  }
});
It’s up to you which one you want to use (I like to keep it simple and use test.each).
The point is, Jest is just a tool. The pattern of parameterized tests can be implemented
in multiple ways. This pattern gives us a lot of power, but also a lot of responsibility. It’s
really easy to abuse this technique and create tests that are harder to understand.
 I usually try to make sure that the same scenario (type of input) holds for the
entire table. If I were reviewing this test in a code review, I would have told the person
Listing 2.22
Refactoring test.each
Listing 2.23
Using a vanilla JavaScript for
Providing three arrays, 
each with two parameters
A new false expectation for a 
missing uppercase character
Jest maps the array values 
to arguments automatically.


---
**Page 55**

55
2.10
Checking for expected thrown errors
who wrote it that this test is actually testing two different scenarios: one with no upper-
case, and a couple with one uppercase. I would split those out into two different tests.
 In this example, I wanted to show that it’s very easy to get rid of many tests and put
them all in a big test.each—even when it hurts readability—so be careful when run-
ning with these specific scissors.
2.10
Checking for expected thrown errors
Sometimes we need to design a piece of code that throws an error at the right time
with the right data. What happens if we add code to the verify function that throws
an error if there are no rules configured, as in the next listing?
verify (input) {
  if (this.rules.length === 0) {
    throw new Error('There are no rules configured');
  }
  . . .
We could test it the old-fashioned way by using try/catch, and failing the test if we
don’t get an error.
test('verify, with no rules, throws exception', () => {
    const verifier = makeVerifier();
    try {
        verifier.verify('any input');
        fail('error was expected but not thrown');
    } catch (e) {
        expect(e.message).toContain('no rules configured');
    }
});
This try/catch pattern is an effective method but very verbose and annoying to type.
Jest, like most other frameworks, contains a shortcut to accomplish exactly this type of
scenario, using expect().toThrowError().
Listing 2.24
Throwing an error
Listing 2.25
Testing exceptions with try/catch
Using fail()
Technically, fail() is a leftover API from the original fork of Jasmine, which Jest is
based on. It’s a way to trigger a test failure, but it’s not in the official Jest API docs,
and they would recommend that you use expect.assertions(1) instead. This
would fail the test if you never reached the catch() expectation. I find that as long
as fail() still works, it does the job quite nicely for my purposes, which are to
demonstrate why you shouldn’t use the try/catch construct in a unit test if you can
help it.



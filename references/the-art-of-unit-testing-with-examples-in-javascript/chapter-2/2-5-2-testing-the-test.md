# 2.5.2 Testing the test (pp.39-39)

---
**Page 39**

39
2.5
The first Jest test for verifyPassword
2.5.2
Testing the test
Let’s put a bug in the production code and see if the test fails when it should.
const verifyPassword = (input, rules) => {
  const errors = [];
  rules.forEach(rule => {
    const result = rule(input);
    if (!result.passed) {
      // errors.push(`error ${result.reason}`);  
    }
  });
  return errors;
};
You should now see your test failing with a nice message. Let’s uncomment the line
and see the test pass again. This is a great way to gain some confidence in your tests, if
you’re not doing test-driven development and are writing the tests after the code.
2.5.3
USE naming
Our test has a really bad name. It doesn’t explain anything about what we’re trying to
accomplish here. I like to put three pieces of information in test names, so that the
reader of the test will be able to answer most of their mental questions just by looking
at the test name. These three parts include
The unit of work under test (the verifyPassword function, in this case)
The scenario or inputs to the unit (the failed rule)
The expected behavior or exit point (returns an error with a reason)
During the review process, Tyler Lemke, a reviewer of the book, came up with a nice
acronym for this, USE: unit under test, scenario, expectation. I like it, and it’s easy to
remember. Thanks Tyler!
 The following listing shows our next revision of the test with a USE name.
test('verifyPassword, given a failing rule, returns errors', () => {
  const fakeRule = input => ({ passed: false, reason: 'fake reason' });
  const errors = verifyPassword('any value', [fakeRule]);
  expect(errors[0]).toContain('fake reason');
});
This is a bit better. When a test fails, especially during a build process, you don’t see
comments or the full test code. You usually only see the name of the test. The name
should be so clear that you might not even have to look at the test code to understand
where the production code problem might be.
Listing 2.4
Adding a bug
Listing 2.5
Naming a test with USE
We've accidentally 
commented out 
this line.



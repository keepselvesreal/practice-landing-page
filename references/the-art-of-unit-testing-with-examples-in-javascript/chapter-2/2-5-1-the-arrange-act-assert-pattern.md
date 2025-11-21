# 2.5.1 The Arrange-Act-Assert pattern (pp.38-39)

---
**Page 38**

38
CHAPTER 2
A first unit test
alongside the code being tested. There are pros and cons to each approach, and we’ll
get into that in later parts of the book. For now, we’ll go with the defaults.
 Here’s a first version of a test against our new function.
test('badly named test', () => {
  const fakeRule = input =>                      
    ({ passed: false, reason: 'fake reason' });  
  const errors = verifyPassword('any value', [fakeRule]);   
  expect(errors[0]).toMatch('fake reason');  
});
2.5.1
The Arrange-Act-Assert pattern
The structure of the test in listing 2.3 is colloquially called the Arrange-Act-Assert (AAA)
pattern. It’s quite nice! I find it very easy to reason about the parts of a test by saying
things like “that ‘arrange’ part is too complicated” or “where is the ‘act’ part?”
 In the arrange part, we’re creating a fake rule that always returns false, so that we
can prove it’s actually used by asserting on its reason at the end of the test. We then
send it to verifyPassword along with a simple input. We check in the assert section
that the first error we get matches the fake reason we gave in the arrange part.
.toMatch(/string/) uses a regular expression to find a part of the string. It’s the
same as using .toContain('fake reason').
 It’s tedious to run Jest manually after we write a test or fix something, so let’s con-
figure npm to run Jest automatically. Go to package.json in the root folder of ch2 and
add the following items under the scripts item:
"scripts": {
   "test": "jest",
   "testw": "jest --watch" //if not using git, change to --watchAll
},
If you don’t have Git initialized in this folder, you can use the command --watchAll
instead of --watch.
 If everything went well, you can now type npm test in the command line from the
ch2 folder, and Jest will run the tests once. If you type npm run testw, Jest will run and
wait for changes in an endless loop, until you kill the process with Ctrl-C. (You need to
use the word run because testw is not one of the special keywords that npm recog-
nizes automatically.)
 If you run the test, you can see that it passes, since the function works as expected. 
Listing 2.3
The first test against verifyPassword()
Setting up inputs 
for the test
Invoking the 
entry point with 
the inputs
Checking the exit point


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



# 2.5.0 Introduction [auto-generated] (pp.37-38)

---
**Page 37**

37
2.5
The first Jest test for verifyPassword
 Now let’s move on and write something that feels a bit more like a real test with
Jest, shall we?
2.4
Introducing the Password Verifier project
The project that we’ll mostly use for testing examples in this book will start out simple,
containing only one function. As the book moves along, we’ll extend that project with
new features, modules, and classes to demonstrate different aspects of unit testing.
We’ll call it the Password Verifier project.
 The first scenario is pretty simple. We’ll be building a password verification library,
and it will just be a function at first. The function, verifyPassword(rules), allows us
to put in custom verification functions dubbed rules, and it outputs the list of errors,
according to the rules that have been input. Each rule function will output two fields: 
{
    passed: (boolean),
    reason: (string)
} 
In this book, I’ll teach you to write tests that check verifyPassword’s functionality in
multiple ways as we add more features to it.
 The following listing shows version 0 of this function, with a very naive implemen-
tation.
const verifyPassword = (input, rules) => {
  const errors = [];
  rules.forEach(rule => {
    const result = rule(input);
    if (!result.passed) {
      errors.push(`error ${result.reason}`);
    }
  });
  return errors;
};
Granted, this is not the most functional-style code, and we might refactor it a bit later,
but I wanted to keep things very simple here so we can focus on the tests.
 The function doesn’t really do much. It iterates over all the rules given and runs
each one with the supplied input. If the rule’s result is not passed, then an error is
added to the final errors array that is returned as the final result.
2.5
The first Jest test for verifyPassword
Assuming you have Jest installed, you can go ahead and create a new file named
password-verifier0.spec.js under the __tests__ folder. 
 Using the __tests__ folder is only one convention for organizing your tests, and it’s
part of Jest’s default configuration. There are many who prefer to place the test files
Listing 2.2
Password Verifier version 0


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



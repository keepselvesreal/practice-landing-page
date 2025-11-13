# 2.4 Introducing the Password Verifier project (pp.37-37)

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



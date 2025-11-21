# 2.5.4 String comparisons and maintainability (pp.40-40)

---
**Page 40**

40
CHAPTER 2
A first unit test
2.5.4
String comparisons and maintainability
We also made another small change in the following line:
expect(errors[0]).toContain('fake reason');
Instead of checking that one string is equal to another, as is very common in tests, we
are checking that a string is contained in the output. This makes our test less brittle
for future changes to the output. We can use .toContain or .toMatch(/fake reason/),
which uses a regular expression to match a part of the string, to achieve this. 
 Strings are a form of user interface. They are visible to humans, and they might
change—especially the edges of strings. We might add whitespace, tabs, asterisks, or
other embellishments to a string. We care that the core of the information contained in
the string exists. We don’t want to change our test every time someone adds a new line
to the end of a string. This is part of the thinking we want to encourage in our tests:
test maintainability over time, and resistance to test brittleness, are of high priority. 
 We’d ideally like the test to fail only when something is actually wrong in the pro-
duction code. We’d like to reduce the number of false positives to a minimum. Using
toContain() or toMatch() is a great way to move toward that goal. 
 I’ll talk about more ways to improve test maintainability throughout the book, and
especially in part 2 of the book.
2.5.5
Using describe()
We can use Jest’s describe() function to create a bit more structure around our test
and to start separating the three USE pieces of information from each other. This step
and the ones after it are completely up you—you can decide how you want to style
your test and its readability structure. I’m showing you these steps because many peo-
ple either don’t use describe() in an effective way, or they ignore it altogether. It can
be quite useful.
 The describe() functions wrap our tests with context: both logical context for the
reader, and functional context for the test itself. The next listing shows how we can
start using them.
describe('verifyPassword', () => {
  test('given a failing rule, returns errors', () => {
    const fakeRule = input =>
      ({ passed: false, reason: 'fake reason' });
    const errors = verifyPassword('any value', [fakeRule]);
    expect(errors[0]).toContain('fake reason');
  });
});
Listing 2.6
Adding a describe() block



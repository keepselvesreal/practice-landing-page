# 2.5.5 Using describe() (pp.40-41)

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


---
**Page 41**

41
2.5
The first Jest test for verifyPassword
I’ve made four changes here:
I’ve added a describe() block that describes the unit of work under test. To
me this looks clearer. It also feels like I can now add more nested tests under
that block. This describe() block also helps the command-line reporter create
nicer reports.
I’ve nested the test under the new block and removed the name of the unit of
work from the test.
I’ve added the input into the fake rule’s reason string. 
I’ve added an empty line between the arrange, act, and assert parts to make the
test more readable, especially to someone new to the team.
2.5.6
Structure implying context
The nice thing about describe() is that it can be nested under itself. So we can use it
to create another level that explains the scenario, and under that we’ll nest our test. 
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    test('returns errors', () => {
      const fakeRule = input => ({ passed: false,
                                   reason: 'fake reason' });
      const errors = verifyPassword('any value', [fakeRule]);
      expect(errors[0]).toContain('fake reason');
    });
  });
});
Some people will hate it, but I think there’s a certain elegance to it. This nesting
allows us to separate the three pieces of critical information to their own level. In
fact, we can also extract the false rule outside of the test right under the relevant
describe(), if we wish to.
describe('verifyPassword', () => {
  describe('with a failing rule', () => {
    const fakeRule = input => ({ passed: false,
                                 reason: 'fake reason' });
    test('returns errors', () => {
      const errors = verifyPassword('any value', [fakeRule]);
      expect(errors[0]).toContain('fake reason');
    });
  });
});
Listing 2.7
Nested describes for extra context
Listing 2.8
Nested describes with an extracted input



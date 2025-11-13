# 2.10 Checking for expected thrown errors (pp.55-56)

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


---
**Page 56**

56
CHAPTER 2
A first unit test
test('verify, with no rules, throws exception', () => {
    const verifier = makeVerifier();
    expect(() => verifier.verify('any input'))
        .toThrowError(/no rules configured/);   
});
Notice that I’m using a regular expression match to check that the error string con-
tains a specific string, and is not equal to it, so as to make the test a bit more future-
proof if the string changes on its sides. toThrowError has a few variations, and you can
go to https://jestjs.io/ find out all about them.
2.11
Setting test categories
If you’d like to run only a specific category of tests, such as only unit tests, or only inte-
gration tests, or only tests that touch a specific part of the application, Jest currently
doesn’t have the ability to define test case categories.
 All is not lost, though. Jest has a special --testPathPattern command-line flag,
which allows us to define how Jest will find our tests. We can trigger this command
with a different path for a specific type of test we’d like to run (such as “all tests under
the ‘integration’ folder”). You can get the full details at https://jestjs.io/docs/en/cli.
 Another alternative is to create a separate jest.config.js file for each test category,
each with its own testRegex configuration and other properties.
Listing 2.26
Using expect().toThrowError()
Jest snapshots
Jest has a unique feature called Snapshots. It allows you to render a component
(when working in a framework like React) and then match the current rendering to a
saved snapshot of that component, including all of its properties and HTML. 
I won’t be touching on this too much, but from what I’ve seen, this feature tends to
be abused quite heavily. You can use it to create hard-to-read tests that look some-
thing like this:
it('renders',()=>{
    expect(<MyComponent/>).toMatchSnapshot(); 
});
This is obtuse (hard to reason about what is being tested) and it’s testing many
things that might not be related to one another. It will also break for many reasons
that you might not care about, so the maintainability cost of that test will be higher
over time. It’s also a great excuse not to write readable and maintainable tests,
because you’re on a deadline but still have to show you write tests. Yes, it does serve
a purpose, but it’s easy to use in places where other types of tests are more relevant. 
If you need a variation of this, try using toMatchInlineSnapshot() instead. You can
find more info at https://jestjs.io/docs/en/snapshot-testing.
Using a regular expression 
instead of looking for the 
exact string



# 2.11 Setting test categories (pp.56-57)

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


---
**Page 57**

57
Summary
// jest.config.integration.js
var config = require('./jest.config')
config.testRegex = "integration\\.js$" 
module.exports = config
// jest.config.unit.js
var config = require('./jest.config')
config.testRegex = "unit\\.js$" 
module.exports = config
Then, for each category, you can create a separate npm script that invokes the Jest
command line with a custom config file: jest -c my.custom.jest.config.js.
//Package.json
. . .
"scripts": {
    "unit": "jest -c jest.config.unit.js",
    "integ": "jest -c jest.config.integration.js"
. . .
In the next chapter, we’ll look at code that has dependencies and testability problems,
and we’ll start discussing the idea of fakes, spies, mocks, and stubs, and how you can
use them to write tests against such code.
Summary
Jest is a popular, open source test framework for JavaScript applications. It
simultaneously acts as a test library to use when writing tests, an assertion library
for asserting inside the tests, a test runner, and a test reporter.
Arrange-Act-Assert (AAA) is a popular pattern for structuring tests. It provides a
simple, uniform layout for all tests. Once you get used to it, you can easily read
and understand any test.
In the AAA pattern, the arrange section is where you bring the system under test
and its dependencies to a desired state. In the act section, you call methods,
pass the prepared dependencies, and capture the output value (if any). In the
assert section, you verify the outcome.
A good pattern for naming tests is to include in the name of the test the unit
of work under test, the scenario or inputs to the unit, and the expected behav-
ior or exit point. A handy mnemonic for this pattern is USE (unit, scenario,
expectation).
Jest provides several functions that help create more structure around multiple
related tests. describe() is a scoping function that allows for grouping multiple
tests (or groups of tests) together. A good metaphor for describe() is a folder
Listing 2.27
Creating separate jest.config.js files
Listing 2.28
Using separate npm scripts



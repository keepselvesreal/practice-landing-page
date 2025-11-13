# 2.12 Summary (pp.57-61)

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


---
**Page 58**

58
CHAPTER 2
A first unit test
containing tests or other folders. test() is a function denoting an individual
test. it() is an alias for test(), but it provides better readability when used in
combination with describe().

beforeEach() helps avoid duplication by extracting code that is common for
the nested describe and it functions.
The use of beforeEach() often leads to scroll fatigue, when you have to look at
various places to understand what a test does.
Factory methods with plain tests (without any beforeEach()) improve readability
and help avoid scroll fatigue.
Parameterized tests help reduce the amount of code needed for similar tests. The
drawback is that the tests become less readable as you make them more generic.
To maintain a balance between test readability and code reuse, only parameter-
ize input values. Create separate tests for different output values.
Jest doesn’t support test categories, but you can run groups of tests using the
--testPathPattern flag. You can also set up testRegex in the configuration file.


---
**Page 59**

Part 2
Core techniques
Having covered the basics in part 1, I’ll now introduce the core testing
and refactoring techniques necessary for writing tests in the real world.
 In chapter 3, we’ll examine stubs and how they help break dependencies.
We’ll go over refactoring techniques that make code more testable, and you’ll
learn about seams in the process.
 In chapter 4, we’ll move on to mock objects and interaction testing, we’ll look
at how mock objects differ from stubs, and we’ll explore the concept of fakes.
 In chapter 5, we’ll look at isolation frameworks, also known as mocking
frameworks, and at how they solve some of the repetitive coding involved in
handwritten mocks and stubs. Chapter 6 deals with asynchronous code, such as
promises, timers, and events, and various approaches to testing such code. 


---
**Page 60**



---
**Page 61**

61
Breaking dependencies
with stubs
In the previous chapter, you wrote your first unit test using Jest, and we looked
more at the maintainability of the test itself. The scenario was pretty simple, and
more importantly, it was completely self-contained. The Password Verifier had no
reliance on outside modules, and we could focus on its functionality without worry-
ing about other things that might interfere with it. 
 In that chapter, we used the first two types of exit points for our examples:
return value exit points and state-based exit points. In this chapter, we’ll talk about
the final type—calling a third party. This chapter will also present a new require-
ment—having your code rely on time. We’ll look at two different approaches to
handling it—refactoring our code and monkey-patching it without refactoring.
 The reliance on outside modules or functions can and will make it harder to
write a test and to make the test repeatable, and it can also cause tests to be flaky.
This chapter covers
Types of dependencies—mocks, stubs, and more
Reasons to use stubs
Functional injection techniques
Modular injection techniques
Object-oriented injection techniques



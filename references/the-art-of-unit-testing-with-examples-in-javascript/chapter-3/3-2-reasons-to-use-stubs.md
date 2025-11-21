# 3.2 Reasons to use stubs (pp.64-66)

---
**Page 64**

64
CHAPTER 3
Breaking dependencies with stubs
and mocks (one should really only be used once in a test), and we should use the right
terms to ensure it’s clear what the other person is referring to. 
 When in doubt, use the term “test double” or “fake.” Often, a single fake depen-
dency can be used as a stub in one test, and it can be used as a mock in another test.
We’ll see an example of this later on. 
This might seem like a whole lot of information at once. I’ll dive deep into these defi-
nitions throughout this chapter. Let’s take a small bite and start with stubs.
3.2
Reasons to use stubs
What if we’re faced with the task of testing a piece of code like the following?
const moment = require('moment');
const SUNDAY = 0, SATURDAY = 6;
const verifyPassword = (input, rules) => {
    const dayOfWeek = moment().day();
    if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
        throw Error("It's the weekend!");
    }
    //more code goes here...
    //return list of errors found..
    return [];
};
Our password verifier has a new dependency: it can’t work on weekends. Go figure. Spe-
cifically, the module has a direct dependency on moment.js, which is a very common
date/time wrapper for JavaScript. Working with dates directly in JavaScript is not a pleas-
ant experience, so we can assume many shops out there have something like this. 
XUnit test patterns and naming things
xUnit Test Patterns: Refactoring Test Code by Gerard Meszaros (Addison-Wesley,
2007) is a classic pattern reference book for unit testing. It defines patterns for
things you fake in your tests in at least five ways. Once you’ve gotten a feel for the
three types I mention here, I encourage you to take a look at the extra details that
book provides. 
Note that xUnit Test Patterns has a definition for the word “fake”: “Replace a compo-
nent that the system under test (SUT) depends on with a much lighter-weight imple-
mentation.” For example, you might use an in-memory database instead of a full-
fledged production instance. 
I still consider this type of test double a “stub,” and I use the word “fake” to call out
anything that isn’t real, much like the term “test double,” but “fake” is shorter and
easier on the tongue.
Listing 3.1
verifyPassword using time


---
**Page 65**

65
3.2
Reasons to use stubs
 How does this direct use of a time-related library affect our unit tests? The unfor-
tunate issue here is that this direct dependency forces our tests, given no direct way
to affect date and time inside our application under test, to take into account the
correct date and time. The following listing shows an unfortunate test that only runs
on weekends.
const moment = require('moment');
const {verifyPassword} = require("./password-verifier-time00");
const SUNDAY = 0, SATURDAY = 6, MONDAY = 2;
describe('verifier', () => {
    const TODAY = moment().day();
    //test is always executed, but might not do anything
    test('on weekends, throws exceptions', () => {
        if ([SATURDAY, SUNDAY].includes(TODAY)) {    
            expect(()=> verifyPassword('anything',[]))
                .toThrow("It's the weekend!");
        }
    });
    //test is not even executed on week days
    if ([SATURDAY, SUNDAY].includes(TODAY)) {       
        test('on a weekend, throws an error', () => {
            expect(()=> verifyPassword('anything', []))
                .toThrow("It's the weekend!");
        });
    }
});
The preceding listing includes two variations on the same test. One checks for the cur-
rent date inside the test, and the other has the check outside the test, which means the
test never even executes unless it’s the weekend. This is bad. 
 Let’s revisit one of the good test qualities mentioned in chapter 1, consistency:
Every time I run a test, it is the same exact test that I ran before. The values being used
do not change. The asserts do not change. If no code has changed (in test or produc-
tion code), then the test should provide the exact same result as previous runs.
 The second test sometimes doesn’t even run. That’s a good enough reason to use a
fake to break the dependency right there. Furthermore, we can’t simulate a weekend
or a weekday, which gives us more than enough incentive to redesign the code under
test so it’s a bit more injectable for dependencies.
 But wait, there’s more. Tests that use time can often be flaky. They only fail
sometimes, without anything but the time changing. This test is a prime candidate
for this behavior, because we’ll only get feedback on one of its two states when we
run it locally. If you want to know how it behaves on a weekend, just wait a couple of
days. Ugh.
Listing 3.2
Initial unit tests for verifyPassword
Checking the 
date inside 
the test
Checking the 
date outside 
the test


---
**Page 66**

66
CHAPTER 3
Breaking dependencies with stubs
 Tests might become flaky due to edge cases that affect variables that are not under
our control in the test. Common examples are network issues during end-to-end testing,
database connectivity issues, or various server issues. When this happens, it’s easy to
dismiss the test failure by saying “just run it again” or “It’s OK. It’s just [insert variabil-
ity issue here].”
3.3
Generally accepted design approaches to stubbing
In the next few sections, we’ll discuss several common forms of injecting stubs into
our units of work. First, we’ll discuss basic parameterization as a first step, then we’ll
jump into the following approaches:
Functional approaches
– Function as parameter
– Partial application (currying)
– Factory functions 
– Constructor functions 
Modular approach
– Module injection
Object-oriented approaches
– Class constructor injection
– Object as parameter (aka duck typing)
– Common interface as parameter (for this we’ll use TypeScript)
We’ll tackle each of these by starting with the simple case of controlling time in our
tests.
3.3.1
Stubbing out time with parameter injection
I can think of at least two good reasons to control time based on what we’ve covered
so far:
To remove the variability from our tests
To easily simulate any time-related scenario we’d like to test our code with
Here’s the simplest refactoring I can think of that makes things a bit more repeatable.
Let’s add a currentDay parameter to our function to specify the current date. This will
remove the need to use the moment.js module in our function, and it will put that
responsibility on the caller of the function. That way, in our tests, we can determine
the time in a hardcoded manner and make the test and the function repeatable and
consistent. The following listing shows an example of such a refactoring.
const verifyPassword2 = (input, rules, currentDay) => {
    if ([SATURDAY, SUNDAY].includes(currentDay)) {
        throw Error("It's the weekend!");
Listing 3.3
verifyPassword with a currentDay parameter



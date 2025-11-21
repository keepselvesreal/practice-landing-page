# 3.3.1 Stubbing out time with parameter injection (pp.66-68)

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


---
**Page 67**

67
3.3
Generally accepted design approaches to stubbing
    }
    //more code goes here...
    //return list of errors found..
    return [];
};
const SUNDAY = 0, SATURDAY = 6, MONDAY = 1;
describe('verifier2 - dummy object', () => {
    test('on weekends, throws exceptions', () => {
        expect(() => verifyPassword2('anything',[],SUNDAY ))
            .toThrow("It's the weekend!");
    });
});
By adding the currentDay parameter, we’re essentially giving control over time to the
caller of the function (our test). What we’re injecting is formally called a “dummy”—
it’s just a piece of data with no behavior—but we can call it a “stub” from now on. 
 This is approach is a form of Dependency Inversion. It seems the term “Inversion of
Control” first came up in Johnson and Foote’s paper “Designing Reusable Classes,”
published by the Journal of Object-Oriented Programming in 1988. The term “Dependency
Inversion” is also one of the SOLID patterns described by Robert C. Martin in 2000, in
his “Design Principles and Design Patterns” paper. I’ll talk more about higher-level
design considerations in chapter 8. 
 Adding this parameter is a simple refactoring, but it’s quite effective. It provides a
couple of nice benefits other than consistency in the test:
We can now easily simulate any day we want.
The code under test is not responsible for managing time imports, so it has one
less reason to change if we ever use a different time library.
We’re doing “dependency injection” of time into our unit of work. We’ve changed the
design of the entry point to use a day value as a parameter. The function is now “pure”
by functional programming standards in that it has no side effects. Pure functions
have built-in injections of all of their dependencies, which is one of the reasons you’ll
find functional programming designs are typically much easier to test.
 It might feel weird to call the currentDay parameter a stub if it’s just a day integer
value, but based on the definitions from xUnit Test Patterns, we can say that this is a
“dummy” value, and as far as I’m concerned, it falls into the “stub” category. It does
not have to be complex in order to be a stub. It just has to be under our control. It’s a
stub because we are using it to simulate some input or behavior being passed into the
unit under test. Figure 3.2 shows this visually.


---
**Page 68**

68
CHAPTER 3
Breaking dependencies with stubs
3.3.2
Dependencies, injections, and control
Table 3.2 recaps some important terms we’ve discussed and are about to use through-
out the rest of the chapter.
Table 3.2
Terminology used in this chapter
Dependencies
The things that make our testing lives and code maintainability difficult, since we can-
not control them from our tests. Examples include time, the filesystem, the network, 
random values, and more.
Control
The ability to instruct a dependency how to behave. Whoever is creating the dependen-
cies is said to be in control of them, since they have the ability to configure them 
before they are used in the code under test. 
In listing 3.1, our test does not have control over time because the module under test 
has control over it. The module has chosen to always use the current date and time. This 
forces the test to do the exact same thing, and thus we lose consistency in our tests. 
In listing 3.3, we have gained access to the dependency by inverting the control over it 
via the currentDay parameter. Now the test has control over the time and can decide 
to use a hardcoded time. The module under test has to use the time provided, which 
makes things much easier for our test.
Inversion of 
control
Designing the code to remove the responsibility of creating the dependency internally, 
and externalizing it instead. Listing 3.3 shows one way of doing this with parameter 
injection.
Dependency 
injection
The act of sending a dependency through the design interface to be used internally by a 
piece of code. The place where you inject the dependency is the injection point. In our 
case, we are using a parameter injection point. Another word for this place where we 
can inject things is a seam.
Seam
Pronounced “s-ee-m,” and coined by Michael Feathers in his book Working Effectively 
with Legacy Code (Pearson, 2004).
Seams are where two pieces of software meet and something else can be injected. 
They are a place where you can alter behavior in your program without editing in that 
place. Examples include parameters, functions, module loaders, function rewriting, 
and, in the object-oriented world, class interfaces, public virtual methods, and more.
verify(input, rules, dayStub)
Return value
Test
Stub
Time
Figure 3.2
Injecting a stub 
for a time dependency



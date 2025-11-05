# 12.4 Summary (pp.236-241)

---
**Page 236**

236
CHAPTER 12
Working with legacy code
 As you can see, the process is relatively simple:
Add one or more integration tests (no mocks or stubs) to the system to prove
the original system works as needed.
Refactor or add a failing test for the feature you’re trying to add to the system.
Refactor and change the system in small chunks, and run the integration tests
as often as you can, to see if you break something.
Sometimes, integration tests may seem easier to write than unit tests, because you
don’t need to understand the internal structure of the code or where to inject various
dependencies. But making those tests run on your local system may prove annoying or
time consuming because you have to make sure every little thing the system needs is
in place.
 The trick is to work on the parts of the system that you need to fix or add features
to. Don’t focus on the other parts. That way, the system grows in the right places, leav-
ing other bridges to be crossed when you get to them.
 As you continue adding more and more tests, you can refactor the system and add
more unit tests to it, growing it into a more maintainable and testable system. This
takes time (sometimes months and months), but it’s worth it.
 Chapter 7 of Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov
(Manning, 2020) contains an in-depth example of such refactoring. Refer to that
book for more details.
12.3.1 Read Michael Feathers’ book on legacy code
Working Effectively with Legacy Code by Michael Feathers (Pearson, 2004) is another valu-
able source that deals with the issues you’ll encounter with legacy code. It shows many
refactoring techniques and gotchas in depth that this book doesn’t attempt to cover.
It’s worth its weight in gold. Get it. 
12.3.2 Use CodeScene to investigate your production code
Another tool called CodeScene allows you to discover lots of technical debt and hid-
den issues in legacy code, among many other things. It is a commercial tool, and while
I have not personally used it, I've heard great things. You can learn more about it at
https://codescene.com/. 
Summary
Before starting to write tests for legacy code, it’s important to map out the vari-
ous components according to their number of dependencies, their amount of
logic, and each component’s general priority in the project. A component’s log-
ical complexity (or cyclomatic complexity) refers to the amount of logic in the
component, such as nested ifs, switch cases, or recursion. 
Once you have that information, you can choose the components to work on
based on how easy or how hard it will be to get them under test.


---
**Page 237**

237
Summary
If your team has little or no experience in unit testing, it’s a good idea to start
with the easy components and let the team’s confidence grow as they add more
and more tests to the system.
If your team is experienced, getting the hard components under test first can
help you get through the rest of the system more quickly.
Before a large-scale refactoring, write integration tests that will sustain that
refactoring mostly unchanged. After the refactoring is completed, replace most
of these integration tests with smaller and more maintainable unit tests.


---
**Page 238**

238
appendix
Monkey-patching
functions and modules
In chapter 3, I introduced various stubbing techniques that I called “accepted,” in
that they are usually considered safe for both the maintainability and readability of
the code and the tests that they guide us to write. In this appendix, I’ll describe a
few of the less accepted and less safe ways in which we can fake whole modules in
our tests.
A.1
An obligatory warning
I have good news and bad news about global patching and stubbing out functions
and modules. Yes, you can do it—I’ll show you several ways to accomplish this. Is it
a great idea? I’m not convinced. The costs of maintaining your tests with the tech-
niques I’ll show you tend to be, from my experience, worse than maintaining code
that is well parameterized or has proper seams built in. 
 However, there might be special times when you need to use these techniques.
Such times include, but are not limited to, faking dependencies in code that you do
not own and cannot change, and sometimes when using immediately executable
functions or modules. Another case is when a module exposes only functions with-
out objects, which limits the faking options quite a bit.
 Try to avoid using the techniques I describe in this appendix as much as you
can. If you can find a way to write your tests or refactor your code so you don’t need
these approaches, use that way. If all else fails, the techniques in this appendix are a
necessary evil. If you must use them, try to minimize how much you use them. Your
tests will suffer and will become more fragile and harder to read. 
 Let’s dive in.


---
**Page 239**

239
A.2
Monkey-patching functions, globals, and possible issues
A.2
Monkey-patching functions, globals, 
and possible issues
Monkey-patching refers to the act of changing the behavior of a running program
instance at run time. I first encountered the term when I was working in Ruby, where
monkey-patching is very common. In JavaScript, it’s just as easy to “patch” a function
at run time.
 In chapter 3 we looked at the issue of time management in our tests and code.
With monkey-patching, we could look at any function, global or local, and replace it
(for a specific JavaScript scope) with a different implementation. If we wanted to
patch time, we could monkey-patch the global Date.now so that any code from that
point on would be affected by this change, both production and test code. 
 Listing A.1 shows a test that does this for the original production code that uses
Date.now directly. It fakes the global Date.now function to control time during the test.
describe('v1 findRecentlyRebooted', () => {
  test('given 1 of 2 machines under threshold, it is found', () => {
    const originalNow = Date.now;        
    const fromDate = new Date(2000,0,3);   
    Date.now = () => fromDate.getTime();   
    const rebootTwoDaysEarly = new Date(2000,0,1);
    const machines = [
      { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
      { lastBootTime: fromDate, name: 'found' }];
    const result = findRecentlyRebooted(machines, 1, fromDate);
    expect(result.length).toBe(1);
    expect(result[0].name).toContain('found');
    Date.now = originalNow;   
  });
}); 
In this listing, we’re replacing the global Date.now with a custom date. Because this is a
global function, other tests can be affected by it, so we clean up after ourselves at the
end of the test by restoring the original Date.now to its rightful place.
 There are several major issues in a test like this. First, these asserts throw excep-
tions when they fail, which means if they fail, the restoration of the original Date.now
might never be executed, and other tests will suffer a “dirty” global time that might
affect them.
 It’s also cumbersome to save the time function and then put it back. It’s making its
mark on the test and making it longer and harder to read, plus harder to write. It’s
easy to forget to reset the global state. 
Listing A.1
Issues in faking the global Date.now()
Saving the
original
Date.now
Replacing Date.now 
with a custom date
Restoring the 
original Date.now


---
**Page 240**

240
APPENDIX
Monkey-patching functions and modules
 Finally, we’ve impaired parallelism. Jest seems to handle this well, as it creates a
separate set of dependencies for each test file, but with other frameworks that might
run tests in parallel, there could be a race condition. Multiple tests can change or
expect the global time to have a certain value. When running in parallel, these tests
can collide and create race conditions in the global state and affect each other. It’s not
required in our case, but if you wanted to eliminate uncertainty, Jest allows you to run
the Jest command line with the extra --runInBand command-line parameter to avoid
parallelism.
 We can avoid some of these issues by resorting to the beforeEach() and afterEach()
helper functions.
describe('v2 findRecentlyRebooted', () => {
  let originalNow;
  beforeEach(() => originalNow = Date.now);   
  afterEach(() => Date.now = originalNow);   
  test('given 1 of 2 machines under threshold, it is found', () => {
    const fromDate = new Date(2000,0,3);
    Date.now = () => fromDate.getTime();
    const rebootTwoDaysEarly = new Date(2000,0,1);
    const machines = [
      { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
      { lastBootTime: fromDate, name: 'found' }];
    const result = findRecentlyRebooted(machines, 1, fromDate);
    expect(result.length).toBe(1);
    expect(result[0].name).toContain('found');
  });
});
Listing A.2 solves some of our issues but not all of them. The good part is that we
don’t need to remember to save and reset Date.now anymore, because beforeEach()
and afterEach() will take care of it. It’s also now easier to read the tests.
 But we still have a potential major issue with parallel tests. Jest is smart enough to
run parallel tests only per file, which means the tests in this spec file will run linearly,
but this behavior is not guaranteed for tests in other files. Any one of the parallel tests
might have their own beforeEach() and afterEach() that reset global state and might
affect our tests without realizing it.
 I’m not a fan of faking global objects (i.e., “singletons” in most typed languages)
when I can help it. There are always strings attached—extra coding, extra mainte-
nance, extra test fragility, or affecting other tests indirectly and worrying about clean-
ing up all the time are some reasons why. Most of the time, the code comes out better
Listing A.2
Resorting to beforeEach() and afterEach()
Saving the 
original Date.now
Restoring the 
original Date.now


---
**Page 241**

241
A.2
Monkey-patching functions, globals, and possible issues
when I factor seams into the design of the code under test instead of around it in an
implicit manner, such as what we just did.
 Especially when considering that more and more frameworks might start to copy
Jest’s features and run tests in parallel, global fakes become more and more dangerous.
A.2.1
Monkey-patching a function the Jest way
To make the picture more complete, Jest also supports the idea of monkey-patching
through the use of two functions that work in tandem: spyOn and mockImplementation.
Here’s spyOn:
Date.now = jest.spyOn(Date, 'now')
spyOn takes as parameters the scope and the function that requires tracking. Note that
we need to use a string as a parameter here, which is not really refactoring-friendly—
it’s easy to miss if we rename that function. 
A.2.2
Jest spies
The word “spy” has a slightly more interesting shade of grey to it than the terms we’ve
encountered so far in this book, which is why I don’t like to use it too much (or at all)
if I can help it. Unfortunately, this word is a major part of Jest’s API, so let’s make sure
we understand it. 
 xUnit Test Patterns (Addison-Wesley, 2007), by Gerard Meszaros, says this in its dis-
cussion of spies: “Use a Test Double to capture the indirect output calls made to
another component by the system under test (SUT) for later verification by the test.”
The only difference between a spy and a fake or test double is that a spy is calling the
real implementation of the function underneath, and it only tracks the inputs to and
outputs from that function, which we can later verify through the test. Fakes and test
doubles don’t use the real implementation of a function.
 My refined definition of a spy is pretty close: The act of wrapping a unit of work
with an invisible tracking layer on the entry points and exit points without changing
the underlying functionality, for the purpose of tracking its inputs and outputs
during testing.
A.2.3
spyOn with mockImplementation()
This “tracking without changing functionality” behavior that is inherent to spies also
explains why just using spyOn won’t be enough for us to fake Date.now. It’s only meant
for tracking, not faking. 
 To actually fake the Date.now function and turn it into a stub, we’ll use the confus-
ingly named mockImplementation to replace the underlying unit of work’s functionality:
jest.spyOn(Date, 'now').mockImplementation(() => /*return stub time*/);



# Working with legacy code (pp.231-Back cover)

---
**Page 231**

231
Working with legacy code
I once consulted for a large development shop that produced billing software.
They had over 10,000 developers and mixed .NET, Java, and C++ in products, sub-
products, and intertwined projects. The software had existed in one form or
another for over five years, and most of the developers were tasked with maintain-
ing and building on top of existing functionality. 
 My job was to help several divisions (using all languages) learn TDD techniques.
For about 90% of the developers I worked with, this never became a reality for sev-
eral reasons, some of which were a result of legacy code:
It was difficult to write tests against existing code.
It was next to impossible to refactor the existing code (or there wasn’t
enough time to do it).
Some people didn’t want to change their designs.
Tooling (or a lack of tooling) was getting in the way.
It was difficult to determine where to begin.
This chapter covers
Examining common problems with legacy code
Deciding where to begin writing tests


---
**Page 232**

232
CHAPTER 12
Working with legacy code
Anyone who’s ever tried to add tests to an existing system knows that most such sys-
tems are almost impossible to write tests for. They were usually written without proper
places (called seams) in the software to allow extensions or replacements to existing
components.
 There are two problems that need to be addressed when dealing with legacy code:
There’s so much work, where should you start to add tests? Where should you
focus your efforts?
How can you safely refactor your code if it has no tests to begin with?
This chapter will tackle these tough questions associated with approaching legacy
codebases by listing techniques, references, and tools that can help.
12.1
Where do you start adding tests?
Assuming you have existing code inside components, you’ll need to create a priority
list of components for which testing makes the most sense. There are several factors to
consider that can affect each component’s priority:
Logical complexity —This refers to the amount of logic in the component, such as
nested ifs, switch cases, or recursion. Such complexity is also called cyclomatic
complexity, and you can use various tools to check it automatically.
Dependency level—This refers to the number of dependencies in the component.
How many dependencies do you have to break in order to bring this class under
test? Does it communicate with an outside email component, perhaps, or does
it call a static log method somewhere?
Priority—This is the component’s general priority in the project.
You can give each component a rating for these factors, from 1 (low priority) to 10
(high priority). Table 12.1 shows classes with ratings for these factors. I call this a test-
feasibility table.
Table 12.1
A simple test-feasibility table
Component
Logical 
complexity
Dependency 
level
Priority
Notes
Utils
6
1
5
This utility class has few dependencies 
but contains a lot of logic. It will be easy 
to test, and it provides lots of value.
Person
2
1
1
This is a data-holder class with little 
logic and no dependencies. There’s 
little real value in testing this.
TextParser
8
4
6
This class has lots of logic and lots of 
dependencies. To top it off, it’s part of 
a high-priority task in the project. Test-
ing this will provide lots of value but 
will also be hard and time consuming.


---
**Page 233**

233
12.1
Where do you start adding tests?
From the data in table 12.1, you can create a diagram like the one shown in figure 12.1,
which graphs your components by the amount of value to the project and number of
dependencies. You can safely ignore items that are below your designated threshold of
logic (which I usually set at 2 or 3), so Person and ConfigManager can be ignored.
You’re left with only the top two components in figure 12.1.
 There are two basic ways to look at the graph and decide what you’d like to test
first (see figure 12.2):
Choose the one that’s more complex and easier to test (top left).
Choose the one that’s more complex and harder to test (top right).
The question now is what path you should take. Should you start with the easy stuff or
the hard stuff?
ConfigManager
1
6
1
This class holds configuration data 
and reads files from disk. It has little 
logic but many dependencies. Testing 
it will provide little value to the proj-
ect and will also be hard and time 
consuming.
Table 12.1
A simple test-feasibility table (continued)
Component
Logical 
complexity
Dependency 
level
Priority
Notes
Utils
Person
TextParser
ConfigManager
Logic
Dependencies
Figure 12.1
Mapping components for test 
feasibility
Logic-driven
(easy to test)
Dependency-
driven
(hard to test)
Ignore
Logic
Dependencies
Figure 12.2
Easy, hard, and irrelevant 
component mapping based on logic and 
dependencies


---
**Page 234**

234
CHAPTER 12
Working with legacy code
12.2
Choosing a selection strategy
As the previous section explained, you can start with the components that are easy to
test or the ones that are hard to test (because they have many dependencies). Each
strategy presents different challenges. 
12.2.1 Pros and cons of the easy-first strategy
Starting out with the components that have fewer dependencies will make writing the
tests initially much quicker and easier. But there’s a catch, as figure 12.3 demonstrates.
Figure 12.3 shows how long it takes to bring components under test during the life-
time of the project. Initially it’s easy to write tests, but as time goes by, you’re left with
components that are increasingly harder and harder to test, with the particularly
tough ones waiting for you at the end of the project cycle, just when everyone is
stressed about pushing a product out the door.
 If your team is relatively new to unit testing techniques, it’s worth starting with the
easy components. As time goes by, the team will learn the techniques needed to deal
with the more complex components and dependencies. For such a team, it may be
wise to initially avoid all components over a specific number of dependencies (with
four being a reasonable limit).
12.2.2 Pros and cons of the hard-first strategy
Starting with the more difficult components may seem like a losing proposition ini-
tially, but it has an upside as long as your team has experience with unit testing tech-
niques. Figure 12.4 shows the average time to write a test for a single component over
the lifetime of the project, if you start testing the components with the most depen-
dencies first.
 With this strategy, you could be spending a day or more to get even the simplest
tests going on the more complex components. But notice the quick decline in the
time required to write the tests relative to the slow incline in figure 12.3. Every time
you bring a component under test and refactor it to make it more testable, you may
Time to
write
test
Project lifetime
Figure 12.3
When starting with the easy 
components, the time required to test 
components increases more and more until 
the hardest components are done.


---
**Page 235**

235
12.3
Writing integration tests before refactoring
also be solving testability issues for the dependencies it uses or for other components.
Because that component has lots of dependencies, refactoring it can improve things
for other parts of the system. That’s the reason for the quick decline. 
 The hard-first strategy is only possible if your team has experience in unit testing
techniques, because it’s harder to implement. If your team does have experience, use
the priority aspect of components to choose whether to start with the hard or easy
components. You might want to choose a mix, but it’s important that you know in
advance how much effort will be involved and what the possible consequences are.
12.3
Writing integration tests before refactoring
If you do plan to refactor your code for testability (so you can write unit tests), a prac-
tical way to make sure you don’t break anything during the refactoring phase is to
write integration-style tests against your production system. 
 I consulted on a large legacy project, working with a developer who needed to
work on an XML configuration manager. The project had no tests and was hardly test-
able. It was also a C++ project, so we couldn’t use a tool to easily isolate components
from dependencies without refactoring the code.
 The developer needed to add another value attribute into the XML file and be
able to read and change it through the existing configuration component. We ended
up writing a couple of integration tests that used the real system to save and load con-
figuration data and that asserted on the values the configuration component was
retrieving and writing to the file. Those tests set the “original” working behavior of the
configuration manager as our base of work. 
 Next, we wrote an integration test that showed that once the component was reading
the file, it contained no attribute in memory with the name we were trying to add. We
proved that the feature was missing, and we now had a test that would pass once we
added the new attribute to the XML file and correctly wrote to it from the component.
 Once we wrote the code that saved and loaded the extra attribute, we ran the three
integration tests (two tests for the original base implementation and a new one that
tried to read the new attribute). All three passed, so we knew that we hadn’t broken
existing functionality while adding the new functionality. 
Time to
write
test
Project lifetime
Figure 12.4
When you use a hard-first 
strategy, the time required to test 
components is initially high, but then 
decreases as more dependencies are 
refactored away.


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


---
**Page 242**

242
APPENDIX
Monkey-patching functions and modules
Here’s how the spyOn and mockImplementation combo looks in our code.
describe('v4 findRecentlyRebooted with jest spyOn', () => {
  afterEach(() => jest.restoreAllMocks());
  test('given 1 of 2 machines under threshold, it is found', () => {
    const fromDate = new Date(2000,0,3);
    Date.now = jest.spyOn(Date, 'now')
      .mockImplementation(() => fromDate.getTime());
    const rebootTwoDaysEarly = new Date(2000,0,1);
    const machines = [
      { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
      { lastBootTime: fromDate, name: 'found' }];
You can see that the last piece of the puzzle in the code is inside afterEach(). We use
another function called jest.restoreAllMocks, which is Jest’s way of resetting any
global state that has been spied on to its original implementation with no extra fake
layers around it.
 Note that even though we are using a spy, we’re not verifying that the function was
actually called. Doing that would mean we’re using it as a mock object, which we are
not. We’re merely using it as a stub. With Jest, we have to go through a “spy” to stub
stuff out.
 All of the advantages and disadvantages I’ve listed before still apply here. I prefer
using parameters when it makes sense, instead of using global functions or variables.
A.3
Ignoring a whole module with Jest is simple
Of all the techniques mentioned in this appendix, this is the safest because it does
not deal with the internal workings of the unit under test. It just ignores things in a
broad manner.
Too much “mock”
If I were in a position to decide on a new name for mockImplementation, I’d name it
fakeImplementation, because it can easily be used to create either stubs that return
data or mocks that verify the data being sent into them as parameters. The word
“mock” is used far too often in our industry to signify anything that isn’t real, when
the distinction could help us make less brittle tests. “Mock” in the name immediately
implies that this is something we’ll verify against later on, at least when I look at it,
and given how I treat the ideas of mocks versus stubs in this book. 
Jest is littered with overuse of the word “mock,” especially when comparing its API
to an isolation framework such as Sinon.js, which uses naming that is less surprising
and avoids using “mock” where it’s not necessary.
Listing A.3
Using jest.SpyOn() to monkey-patch Date.now()


---
**Page 243**

243
A.4
Faking module behavior in each test
 If we don’t care about the module at all during our tests, and we just want to get it
out of the way of our scenario without getting any fake data back from it, a simple call
to jest.mock('module path') at the top of the test file will do just fine, without too
much fuss. 
 The next section helps if you want to simulate custom data in each test from a fake
module, which makes us go through more hoops.
A.4
Faking module behavior in each test
Faking a module basically means faking a global object that gets loaded whenever
import or require is used for the first time by the code under test. Depending on the
test framework we’re using, the module might be cached internally or through the stan-
dard Node.js require.cache mechanism. Since this only happens once, when our test
imports the system under test, we have a bit of an issue when we’re trying to fake dif-
ferent behavior or data for different tests in the same file.
 To fake custom behavior for our fake module, we need to take care of the follow-
ing in our tests: clean up the required module from memory, replace it, re-require it,
and get the code under test to use the new module instead of the original one by
requiring our code under test again. That’s quite a bit. I call this pattern Clear-Fake-
Require-Act (CFRA):
1
Clear—Before each test, clear all the cached or required modules in the test
runner’s memory.
2
During the arrange part of the test:
a
Fake—Fake the module that will be required by the require action invoked
by the test code.
b
Require—Require the code under test just before invoking it.
3
Act—Invoke the entry point.
If we forget any of these steps, or perform them in the wrong order, or not at the right
point in the test’s life cycle, there’ll be a lot of question marks when we execute the
test and things seem not to be faking correctly. Worse, they might sometimes work cor-
rectly. Shudder. 
 Let’s look at a real example, starting with the following code.
const { getAllMachines } = require('./my-data-module');   
const daysFrom = (from, to) => {
  const ms = from.getTime() - new Date(to).getTime();
  const diff = (ms / 1000) / 60 / 60 / 24; // secs * min * hrs
  console.log(diff);
  return diff;
};
Listing A.4
Code under test with a dependency
The dependency 
to fake


---
**Page 244**

244
APPENDIX
Monkey-patching functions and modules
const findRecentlyRebooted = (maxDays, fromDate) => {
  const machines = getAllMachines();
  return machines.filter(machine => {
    const daysDiff = daysFrom(fromDate, machine.lastBootTime);
    console.log(`${daysDiff} vs ${maxDays}`);
    return daysDiff < maxDays;
  });
};
The first line contains the dependency we need to break in our test. It’s the getAll-
Machines function, being destructured from my-data-module. Because we are using
the function detached from its parent module, we can’t just fake functions on the
parent module and expect our tests to pass. We have to get the destructured function
to get a fake function during the destructuring process, and that’s where the tricky
part comes in. 
A.4.1
Stubbing a module with vanilla require.cache
Before we use Jest and other frameworks to fake a whole module, let’s see how we can
achieve this effect and explore what’s going on in the various frameworks. 
 You can use the CFRA pattern without using any framework by using require.cache
directly.
const assert = require('assert');
const { check } = require('./custom-test-framework');
const dataModulePath = require.resolve('../my-data-module');
const fakeDataFromModule = fakeData => {
  delete require.cache[dataModulePath];   
  require.cache[dataModulePath] = {    
    id: dataModulePath,
    filename: dataModulePath,
    loaded: true,
    exports: {
      getAllMachines: () => fakeData
    }
  };
  require(dataModulePath);
};
const requireAndCall_findRecentlyRebooted = (maxDays, fromDate) => {
  const { findRecentlyRebooted } = require('../machine-scanner4');    
  return findRecentlyRebooted(maxDays, fromDate);   
};
check('given 1 of 2 machines under the threshold, it is found', () => {
  const rebootTwoDaysEarly = new Date(2000,0,1);
  const fromDate = new Date(2000,0,3);
Listing A.5
Stubbing with require.cache
Clear
Fake
Require
Act


---
**Page 245**

245
A.4
Faking module behavior in each test
  fakeDataFromModule([
    { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
    { lastBootTime: fromDate, name: 'found' }
  ]);
  const result = requireAndCall_findRecentlyRebooted(1, fromDate);
  assert(result.length === 1);
  assert(result[0].name.includes('found'));
});
Unfortunately, this code will not work with Jest, because Jest ignores require.cache
and implements its own caching algorithm internally. To execute this test, run it
directly through the Node.js command line. You’ll see that I’ve implemented my own
little check() function, so that I don’t use Jest’s API. This test will work just fine when
using a framework such as Jasmine.
 Remember this line in our code under test?
const { getAllMachines } = require('./my-data-module'); 
Our tests need to execute this destructuring every time we want to return a fake value.
That means we’ll need to execute a require or import of the unit under test from our
test code, not at the top of the file, but somewhere in the middle of our test execution.
You can see where this happens in the following part of listing A.5:
const requireAndCall_findRecentlyRebooted = (maxDays, fromDate) => {
  const { findRecentlyRebooted } = require('../machine-scanner4');
  return findRecentlyRebooted(maxDays, fromDate);
};
It is because of this destructuring code pattern that modules are not just objects with
properties, for which normal monkey-patching techniques can be used. We need to
jump through more hoops.
 Let’s map the four CFRA steps to the code in listing A.5:
Clear—This is part of the fakeDataFromModule function, which is invoked during
the test. 
Fake—we are telling require.cache’s dictionary entry to return a custom object
that seems to represent what a module looks like, but which has a custom imple-
mentation that returns fakeData. 
Require—We are requiring the code under test as part of the requireAndCall_
findRecentlyRebooted() function, which is invoked during the test.
ACT—This is part of the same requireAndCall_findRecentlyRebooted() function
that is invoked by the test.
Notice that we do not use beforeEach() for this test. We are doing everything directly
from the test, because each test will fake its own data from the module. 


---
**Page 246**

246
APPENDIX
Monkey-patching functions and modules
A.4.2
Stubbing custom module data with Jest is complicated 
We’ve seen the “vanilla” way of stubbing custom module data. That’s not usually how
you’d do it if you’re using Jest, though. Jest contains several confusingly and very
closely named functions that deal with clearing and faking modules, including mock,
doMock, genMockFromModule, resetAllMocks, clearAllMocks, restoreAllMocks, resetModules
and more. Yay!
 The code I’ll recommend here feels the cleanest and simplest of all of Jest’s APIs in
terms of readability and maintainability. I do cover other variations on it in the
GitHub repository at https://github.com/royosherove/aout3-samples and under the
“other-variations” folder at http://mng.bz/Jddo.
 This is the common pattern for faking a module with Jest:
1
Require the module you’d like to fake in your own tests.
2
Stub out the module above the tests with jest.mock(modulename).
3
In each test, tell Jest to override the behavior of one of the functions in that mod-
ule by using [modulename].function.mockImplementation() or mockImplementation-
Once().
The following is what it might look like.
const dataModule = require('../my-data-module');
const { findRecentlyRebooted } = require('../machine-scanner4');
const fakeDataFromModule = (fakeData) =>
    dataModule.getAllMachines.mockImplementation(() => fakeData);
jest.mock('../my-data-module');
describe('findRecentlyRebooted', () => {
  beforeEach(jest.resetAllMocks); //<- the cleanest way
  test('given no machines, returns empty results', () => {
    fakeDataFromModule([]);
    const someDate = new Date(2000,0,1);
    const result = findRecentlyRebooted(0, someDate);
    expect(result.length).toBe(0);
  });
  test('given 1 of 2 machines under threshold, it is found', () => {
    const fromDate = new Date(2000,0,3);
    const rebootTwoDaysEarly = new Date(2000,0,1);
    fakeDataFromModule([
      { lastBootTime: rebootTwoDaysEarly, name: 'ignored' },
      { lastBootTime: fromDate, name: 'found' }
    ]);
    const result = findRecentlyRebooted(1, fromDate);
Listing A.6
Stubbing a module with Jest


---
**Page 247**

247
A.4
Faking module behavior in each test
    expect(result.length).toBe(1);
    expect(result[0].name).toContain('found');
  });
Here’s how you can approach each part of CFRA with Jest.
The jest.mock and jest.resetAllMocks methods are all about faking the module and
resetting the fake implementation to an empty one. Note that the module is still fake
after resetAllMocks. Only its behavior is reset to the default fake implementation. Call-
ing it without telling it what to return will yield weird errors.
 With the FromModule method, we replace the default implementation with a func-
tion that returns our hardcoded values in each test. 
 We could have used mockImplementationOnce() to do mocking, instead of the fake-
DataFromModule() method, but I find that this can create very brittle tests. With stubs,
we normally shouldn’t care how many times they return the fake values. If we did care
how many times they were called, we would use them as mock objects, and that’s the
subject of chapter 4.
A.4.3
Avoid Jest’s manual mocks
Jest contains the idea of manual mocks, but don’t use them if you can help it. This tech-
nique requires you to put a special __mocks__ folder in your tests that contain hard-
coded fake module code, with a naming convention based on the module’s name.
This will work, but the maintainability costs are too high when you want to control the
fake data. The readability costs are too high as well, as it increases scroll fatigue to an
unneeded level, requiring us to switch between multiple files to understand a test. You
can read more about manual mocks in the Jest documentation: https://jestjs.io/docs/
en/manual-mocks.html.
A.4.4
Stubbing a module with Sinon.js
For comparison, and so that you can see that the pattern of CFRA repeats in other
frameworks, here’s an implementation of the same test with Sinon.js—a framework
dedicated to creating stubs.
const sinon = require('sinon');
let dataModule;
Clear
jest.resetAllMocks 
Fake
jest.mock()+
[fake].mockImplementation()
Require
Regularly at the top of the file
Act
Regularly
Listing A.7
Stubbing a module with Sinon.js


---
**Page 248**

248
APPENDIX
Monkey-patching functions and modules
const fakeDataFromModule = fakeData => {
  sinon.stub(dataModule, 'getAllMachines')
    .returns(fakeData);
};
const resetAndRequireModules = () => {
  jest.resetModules();
  dataModule = require('../my-data-module');
};
const requireAndCall_findRecentlyRebooted = (maxDays, someDate) => {
  const { findRecentlyRebooted } = require('../machine-scanner4');
  return findRecentlyRebooted(maxDays, someDate);
};
describe('4  sinon sandbox findRecentlyRebooted', () => {
  beforeEach(resetAndRequireModules);
  test('given no machines, returns empty results', () => {
    const someDate = new Date('01 01 2000');
    fakeDataFromModule([]);
    const result = requireAndCall_findRecentlyRebooted(2, someDate);
    expect(result.length).toBe(0);
  });
Let’s map the relevant parts with Sinon.
A.4.5
Stubbing a module with testdouble
Testdouble is another isolation framework that can easily be used to stub things out.
Due to the refactoring already done in previous tests, the code changes are minimal.
let td;
const resetAndRequireModules = () => {
  jest.resetModules();
  td = require('testdouble');
  require('testdouble-jest')(td, jest);
};
Clear
Before each test:
jest.resetModules + re-require fake module 
Fake
Before each test:
sinon.stub(module,'function')
.returns(fakeData)
Require (module under test)
Before invoking the entry point
Act
After re-requiring the module under test
Listing A.8
Stubbing a module with testdouble


---
**Page 249**

249
A.4
Faking module behavior in each test
const fakeDataFromModule = fakeData => {
  td.replace('../my-data-module', {
    getAllMachines: () => fakeData
  });
};
const requireAndCall_findRecentlyRebooted = (maxDays, fromDate) => {
  const { findRecentlyRebooted } = require('../machine-scanner4');
  return findRecentlyRebooted(maxDays, fromDate);
};
Here are the important parts with testdouble.
The test implementation is exactly the same as with the Sinon example. We’re also
using testdouble-jest, as it connects to the Jest module replacement facility. This is
not needed if we’re using a different test framework.
 These techniques will work, but I recommend staying away from them unless
there’s absolutely no other way. There is almost always another way, and you can see
many of those in chapter 3.
Clear
Before each test:
jest.resetModules +  require('testdouble');
require('testdouble-jest')
                     (td, jest);
Fake
Before each test:
Td.replace(module, fake object)
Require (module under test)
Before invoking the entry point
Act
After re-requiring the module under test


---
**Page 250**

 


---
**Page 251**

251
index
Symbols
<+> sign 154
A
AAA (Arrange-Act-Assert) pattern 38
add() function 142
addDefaultUser() function 173
Adder class 141
addRule() function 44
adopted process 217
advantages and traps of isolation frameworks
117–120
overspecifying tests 119
verifying wrong things 118
advocated process 217
afterAll() function 45
afterEach() function 45, 173, 240
alias to test() function 42
antipatterns
at test level 199
low-level-only test antipattern 202
test-level, end-to-end-only antipattern 199
API (application programming interface) 
tests 198
Arg.is() function 113
Array.prototype.every() method 40–41
describe() function 40–41
verifyPassword() function 40–41
assertEquals() function 14
assertion library 33
assertion roulette 89
assert module 14
async/await 124–125
async/await function structures 129
asynchronous code, unit testing 121–145
async/await mechanism 122
asynchronous data fetching 122
callback approach 124–125
dealing with 124–125
callback mechanism 122
common events 141–142
click events 142–144
dealing with event emitters 141–142
dealing with timers 138–139
DOM testing library 144–145
Extract Adapter pattern 125
functional adapter 135–136
modular adapter 133–134
object-oriented-interface-based adapter
136–138
Extract Entry Point pattern 125
extracting entry points 126
with await 129–131
making code unit-test friendly 125, 
127–129
timers 138–139
faking with Jest 139–141
stubbing out with monkey-patching
138–139
unit-test-friendly code 125–138
Extract Adapter pattern 131–133
functional adapter 135–136
unit testing 121–146
challenges with integration tests 125
DOM testing library 144–145
See also unit-test-friendly code


---
**Page 252**

INDEX
252
asynchronous processing, emulating with linear, 
synchronous tests 16
avoiding setup methods 175–176
B
BDD (behavior-driven development) 42–43
Beck, Kent 25
beforeAll() function 45
beforeEach() function 45–47, 50–51, 240
overview of 47–49
scroll fatigue and 47–49
blockers 215
bottom-up implementation 217
buggy tests, what to do once you’ve found 151
bugs, real bug in production code 151
build whisperers 201
business goals and metrics
breaking up into groups 221–222
leading indicators 221
C
calculator example, factory methods 49–50
callback mechanism 122
catch() expectation 55
CFRA (Clear-Fake-Require-Act) pattern 243
change agents
blockers 215
considering project feasibility 216
convincing insiders 214
change management
identifying starting points 215
making progress visible 219–220
changes
colleagues’ attitudes, being prepared for tough 
questions 214
forced by failing tests 166
in functionality, avoiding or preventing test 
failure due to 152
in other tests 169
testing culture and using code and test reviews 
as teaching tools 216
check() function 14, 245
Clean Code (Martin) 26
clearAllMocks() function 246
click events 142–144
code reviews, using as teaching tools 216
CodeScene, investigating production code 
with 236
code without tests 228
command 106
command/query separation 9, 106
common test types and levels, E2E/UI system 
tests 199
complicated interfaces, example of 98–99
component tests, overview of 196
concerns, testing multiple exit points 158–160
confidence 202
constrained test order 170–173
constructor functions 73–74
constructor injection 74–76
continuous testing 33
control 68
control flow code 22
_.curry() function 93
currying, not using 93
CUT (component, class, or code under test) 6
cyclomatic complexity 232
D
database, replacing with stubs 16
Date.now global 239–240
debug() function 88
debuggers, need for tests if code works 229
decoupling, factory functions decouple creation 
of object under test 168–169
delivery-blocking tests 208
delivery pipelines
delivery vs. discovery pipelines 208
test layer parallelization 210–211
dependencies 62, 68
breaking with stubs, object-oriented injection 
techniques 74
types of 62–64
dependencies object 71
dependencies variable 72
dependency injection (DI) 138
breaking with stubs 61
design approaches to stubbing 66
functional injection techniques 69–70
modular injection techniques 70–73
object-oriented injection techniques 79–81
Dependency Injection (DI) containers 77
Dependency Inversion 67
describe() block 41, 46
describe() function 30, 40–41, 52
describe-driven syntax 42
describe structure 188
destructured() function 244
differentiating between mocks and stubs 88–89
diminishing returns from E2E (end-to-end) 
tests 199


---
**Page 253**

INDEX
253
direct dependencies, abstracting away 109
discovery pipelines, vs. delivery pipelines 208
document.load event 144
DOM (Document Object Model) testing 
library 144–145
doMock() function 246
done() callback 124
done() function 124, 129, 142
DRY (don’t repeat yourself) principle 175
duck typing 79
dummy data 67
dummy value 67
dynamic mocks and stubs 104, 109–110
functional 109–110
dynamic stubbing 114–116
E
E2E (end-to-end) tests 198–199
avoiding completely 202
build whisperer 201
diminishing returns from 199
E2E/UI isolated tests 198
edge cases 205
end-to-end-only antipattern 199–201
avoiding build whisperers 201
avoiding E2E tests completely 202
throw it over the wall mentality 201
when it happens 202
entry points 6–10, 241
extracting, with await 129–131
errors array 46
event-driven programming 142–144
event emitters 141–142
exact:false flag 145
exceptions, checking for expected thrown 
errors 55–56
executing Jest 31–33
exit points 6, 9–11, 158–160, 241
different exit points, different techniques 12
expect 33
expect() function 30
expect().toThrowError() method 55
experiments
as door openers 218
metrics and 218
Extract Adapter pattern 131–133
functional adapter 135–136
modular adapter 133–134
object-oriented-interface-based adapter 136–138
extracting adapter pattern 125
extracting entry point pattern 125
F
factory functions 168–169
factory methods 49–50, 168
replacing beforeEach() completely with
50–51
failed tests
buggy tests 151
reasons tests fail 152
fake 241
FakeComplicatedLogger class 100
fakeDataFromModule() method 245, 247
fakeImplementation 242
FakeLogger class 96, 98, 168
fake module behavior
avoiding Jest’s manual mocks 247
stubbing modules with Sinon.js 247
fake modules, dynamically 106–108
fake objects and functions
faking module behavior in each test 248–249
stubbing with testdouble 248–249
FakeTimeProvider 78
fake (xUnit Test Patterns, Meszaros) 64
false failures 166
feature toggles 166
findFailedRules() function 178–179
findResultFor() function 181
first unit test, setting test categories 56–57
flaky tests 153, 161
dealing with 163
mixing unit tests and integration tests 158
preventing flakiness in higher-level tests 163
folders, preparing for Jest 29–30
Freeman, Steve 26
full control 15
functional dynamic mocks and stubs 109–110
functional injection techniques 69
injecting functions 69–70
partial application 70
functionality, change in, out of date tests 152
functional style
higher-order functions 93
mocks, currying 92–93
functions
injecting 69–70
injecting instead of objects 76–79
it() function 42
monkey-patching 238
faking module behavior in each test 243–244, 
247–249
globals and possible issues 239–241
ignoring whole modules with Jest 242


---
**Page 254**

INDEX
254
functions (continued)
setup 175–176
test() 52
verifyPassword 43–45
G
genMockFromModule() function 246
getDay() function 72, 76
getLogLevel() function 107
globals
Jest spies 241
monkey-patching functions and modules
239–241
goals, specific 220
good-to-know tests 208
Growing Object-Oriented Software, Guided by Tests 
(Freeman and Pryce) 26
guerrilla implementation 217
H
happy path 205
hard-first strategy, pros and cons of 234
hexagonal architecture 109
higher-order functions 93
high-level tests, disconnected low-level 
and 204
I
IComplicatedLogger interface 99
if/else 155
ILogger interface 96, 98, 166
incoming dependencies 62
indicators
breaking up into groups 221–222
lagging indicators 220
INetworkAdapter parameter 136
info function 88, 96, 107
info method 88
inject() function 72
injectDate() function 72
injectDependencies() function 91
inject function 72
injections 68
modular-style injection, example of 92
insiders, convincing 214
integration of unit testing
into organization, convincing management
217
metrics and experiments 218
integration testing
async/await 124–125
challenges with 125
unit testing, integrating into organization 228
integration tests 123, 197
flaky, mixing with unit tests 158
interaction testing
complicated interfaces 98–101
depending on loggers 85–86
differentiating between mocks and stubs 88–89
mock objects 83–103
functional style 92
in object-oriented style 94, 96
mocks and stubs 84
partial mocks 101
interfaces, complicated, ISP 101
interface segregation principle 131, 133
internal behavior, overspecification with 
mocks 177–179
Inversion of Control (IoC) containers 77
isolated tests 198
isolation facilities 33
isolation frameworks 104–120
advantages and traps of
overspecifying tests 119
unreadable test code 118
verifying wrong things 118
defining 105
loose vs. typed 105
faking modules dynamically 106–108
abstracting away direct dependencies 109
Jest API 108
functional dynamic mocks and stubs 109–110
object-oriented dynamic mocks and stubs 110
using loosely typed framework 110–112
stubbing behavior dynamically 114–117
object-oriented example with mock and 
stub 114–116
with substitute.js 116–117
type-friendly frameworks 112–113
ISP (interface segregation principle) 101
isWebsiteAlive() function 129, 133
it() function 30, 42, 51
it.each() function 53, 176
it.only keyword 172
IUserDetails interface 170
J
Jest 29
API of 108
avoiding manual mocks 247


---
**Page 255**

INDEX
255
Jest (continued)
creating test files 30–31
executing 31–33
fake timers with 139–141
ignoring whole modules with 242
installing 30
library, assert, runner, and reporter 33
monkey-patching functions 241
preparing environment 29
preparing working folder 29–30
spies 241
verifyPassword() function 37
for Jest syntax flavors 42
jest command 30
jest.fn() function 112
jest.mock() function 134
jest.mock API, abstracting away direct 
dependencies 109
jest.mock([module name]) function 108
jest.restoreAllMocks function 242
Jest snapshots 56
Jest unit testing framework 36
jest - -watch command 33
K
Khorikov, Vladimir 236
KPIs (key performance indicators) 208, 220
L
lagging indicators 220
leading indicators 221
breaking up into groups 221–222
legacy code 231–237
integration tests, writing before refactoring 236
selection strategies
easy-first strategy 234
hard-first strategy, pros and cons of 234
where to start adding tests 232–233
writing integration tests before refactoring 235
using CodeScene to investigate production 
code 236
loadHtmlAndGetUIElements method 144
loadHtml method 144
lodash library 92
logged variable 96
logger.debug 90
logger.info 90
loggers, depending on 85–86
loose isolation frameworks 105
loosely typed frameworks 110–112
low-level-only test antipattern 202
low-level tests, disconnected high-level and 204
LTS (long-term support) release 29
M
magic values 189–190
maintainability 89, 165–183
avoiding overspecification 177–179
changes forced by failing tests
changes in other tests 169
constrained test order 170–173
of code, exact outputs and ordering 
overspecification 179–183
of tests
changes forced by failing tests 166
changes in production code’s API 166–168
test is not relevant or conflicts with another 
test 166
refactoring to increase 173
avoiding setup methods 175–176
avoiding testing private or protected 
methods 175
keeping tests DRY 175
using parameterized tests to remove 
duplication 176–177
maintainable tests 36
MaintenanceWindow interface 115–116
makeFailingRule() method 50
makePassingRule() method 50
makePerson() function 160
makeSpecialApp() factory function 173
makeStubNetworkWithResult() helper 
function 136
makeVerifier() function 94
Meszaros, Gerard 11, 64, 89
methods, making public 174
metrics, experiments and 218
metrics and KPIs 222
mock functions 98, 246
mockImplementation() function 241–242
mockImplementation() method 114
mockImplementationOnce() method 114, 247
mockLog variable 191
mock objects 12, 83, 98–103, 247
advantages of isolation frameworks 118
complicated interfaces 98
downsides of using directly 100
example of 98–99
depending on loggers 85–86
differentiating between mocks and stubs 88–89
functional style 92


---
**Page 256**

INDEX
256
mock objects (continued)
in object-oriented style 94
interaction testing with complicated 
interfaces 99–100
modular-style mocks 89
refactoring production code in modular injec-
tion style 91
overview of 84
partial mocks 101
object-oriented partial mock example 102–103
standard style, introducing parameter 
refactoring 87–88
mockReturnValue() method 114
mockReturnValueOnce() method 114
mocks 63, 84
advantages of, having more than one mock per 
test 119
functional style
currying 92–93
higher-order functions and not currying 93
in object-oriented style
refactoring production code for injection 95
refactoring production code with interface 
injection 96
internal behavior overspecification with 177–179
object-oriented design example with 114–116
object-oriented dynamic mocks and stubs 110
modular adapter 133–134
modular injection techniques 70–73
modular-style mocks 89
example of production code 90–91
modular-style injection, example of 92
refactoring production code in modular injec-
tion style 91
modules
faking behavior in each test 243–249
stubbing with Sinon.js 247
stubbing with testdouble 248–249
faking dynamically 106–108
abstracting away direct dependencies 109
monkey-patching 238
moment.js 64
monkey-patching 138, 238
functions and modules
faking module behavior in each test 248–249
stubbing module with vanilla 
require.cache 244–245
stubbing with Sinon.js 247
stubbing with testdouble 248–249
possible issues 239–241
spyOn with mockImplementation() 241–242
warning about 238
N
network-adapter module 132–134
node-fetch module 132
Node.js 7
node package manager (NPM) 29
npm commands 30
NPM (node package manager) 4, 29
npm run testw command 38
npx jest command 30
numbers string 12
O
object-oriented design, example with mock and 
stub 114–116
object-oriented dynamic mocks and stubs 110
type-friendly frameworks 112–113
using loosely typed framework 110–112
object-oriented injection techniques 74–81
constructor injection 74–76
extracting common interface 79–81
injecting objects instead of functions 76–79
overview 79–81
object-oriented style, mocks in 94
obvious values 196
onion architecture 109
organization, integrating unut testing into 229
originalDependencies object 71
originalDependencies variable 91
outgoing dependencies 62
overspecification
avoiding 177–179
exact outputs and ordering 179–183
P
parameter injection 66–67
parameterized tests
refactoring to 53–55
removing duplication with 176–177
parameter refactoring 87–88
partial application, dependency injection via 70
partial mocks 101
functional example 101–102
object-oriented partial mock example 102–103
PASSED result 90
passVerify() function 94
password-verifier0.spec.js file 37
PasswordVerifier1 46
PasswordVerifier class 97
passwordVerifierFactory() function 76


---
**Page 257**

INDEX
257
Password Verifier project 37
patching functions and modules
avoiding Jest’s manual mocks 247
faking module behavior in each test 243–244
ignoring whole modules with Jest 242
person object 160
polymorphism 96
ports and adapters architecture 109
preconfigured verifier function 94
private and protected methods, avoiding 
testing 175
making methods public 174
production code
changing API of 166–167
modular-style mocks, example of 90–91
real bug in 151
refactoring for injection 95
refactoring in modular injection style 91
refactoring with interface injection 96
production code, investigating with 
CodeScene 236
production code, refactoring 43–45
production module 13
progress, making visible 219–220
protected methods 174
Pryce, Nat 26
Q
qualitative metrics 222
query 106
R
readability 89
magic values and naming variables 189–190
of unit tests 187–193
separating asserts from actions 190
readable tests 36
reason string 41
.received() function 113, 116
refactoring 24
avoiding testing private or protected 
methods 175
keeping tests DRY 175
making methods public 174
production code for injection 95
to increase maintainability
avoiding setup methods 175–176
avoiding testing private or protected 
methods 174
to parameterized tests 53–55
using parameterized tests to remove 
duplication 176–177
writing integration tests before 235
requireAndCall_findRecentlyRebooted() 
function 245
require.cache, stubbing module with vanilla
244–245
require.cache mechanism 243
reset() function 72
resetAllMocks() function 246
resetDependencies() function 91–92
resetModules() function 246
restoreAllMocks() function 246
.returns() function 116
rules array 166
rules verification functions 37
S
safe green zone 158
scripts item 38
seams 71, 232
abstracting dependencies using 86
selection strategies 234
easy-first strategy 234
setTimeout function 138–139
setTimeout method 138
setup methods 191–192
SimpleLogger class 96–97
Sinon.js, stubbing modules with 247
smaller teams 215
SpecialApp implementation 170–171
spies, Jest 241
spyOn() function 241–242
state-based test 179
stateless private methods, making public static 175
string comparisons 40
stringMatching function 110
strings, comparing 40
stub 88, 108, 241
stubbing
dynamically 114–117
modules 248–249
with Sinon.js 247
with substitute.js 116–117
with testdouble 248–249
stubs 61, 63, 84
constructor functions 73–74
design approaches to 66
dependencies, injections, and control 68
stubbing out time with parameter injection
66–67


---
**Page 258**

INDEX
258
stubs (continued)
functional injection techniques 69
injecting functions 69–70
modular injection techniques 70–73
object-oriented injection techniques 74–81
constructor injection 74–76
extracting common interface 79–81
injecting objects instead of functions 76–79
overview 79–81
overview of 84
reasons to use 64–66
replacing database (or another dependency) 
with 16
types of dependencies 62–64
subject, system, or suite under test (SUT) 6
Substitute.for<T>() function 116
substitute.js 116–117
subteams, creating 216
sum() function 12
SUnit 36
SUT (subject, system, or suite under test) 6
T
tape framework 36
TAP (Test Anything Protocol) 36
TDD (test-driven development) 5, 22, 152–229
core skills for 25
pitfalls of, not a substitute for good unit tests 24
teardown methods 191–192
test() function, overview of 52
testableLog variable 101
test categories 56–57
test conflicts with another test 152–153
testdouble-jest 249
test doubles 64, 243
stubbing modules with 248–249
test-driven development (TDD) 5, 25, 152
test.each function 53, 176
test failure
reasons for 152
test conflicts with another test 152–153
test out of date due to change in 
functionality 152
test-feasibility table 232
test-first development 22
test flakiness 82
test function 30
testing
reasons tests fail
buggy test gives false failure 151
test conflicts with another test 152
smelling false sense of trust in passing tests 156
trustworthy tests 164
testing strategy 194–212
common test types and levels 195
API tests 198
criteria for judging tests 196
E2E/UI isolated tests 198
E2E/UI system tests 199
integration tests 197
unit tests and component tests 196
developing, using test recipes 205
low-level-only test antipattern 202
managing delivery pipelines 208
delivery vs. discovery pipelines 208
test layer parallelization 210–211
test-level antipatterns
disconnected low-level and high-level 
tests 203
end-to-end-only antipattern 199, 201
test recipes
rules for 207–208
writing and using 207
test layer parallelization 210–211
test library 33
test maintainability, constrained test order
170–173
test method 13
testPathPattern command-line flag 56
- -testPathPattern flag 58
test recipes
as testing strategy 205
rules for 207–208
writing 205
writing and using 207
testRegex configuration 56
test reporter 33
test reviews, using as teaching tools 216
test runner 33
tests, criteria for judging 196
__tests__ folder 37–38
test syntax 42
then() callback 124
third-party test 179
time, added to process 226–227
TimeProviderInterface type 79
timers 138
faking with Jest 139–141
stubbing out with monkey-patching 138–139
.toContain('fake reason') function 38
.toContain matcher 40
toMatchInlineSnapshot() method 56
.toMatch matcher 40


---
**Page 259**

INDEX
259
.toMatch(/string/) function 38
top-down approach 217
totalSoFar() function 9
toThrowError method 56
transpiler 96
trend lines 222
true failures 166
trust 89
trustworthy tests 36, 149–164
avoiding logic in unit tests 153, 155–156
creating dynamic expected values 153–155
even more logic 156
buggy tests
criteria for judging tests 196
what to do once you’ve found 151
dealing with flaky tests 163
failed tests 151
flaky tests 161, 163
reasons for test failure 150–152
buggy test gives false failure 151
flaky tests 153
out of date due to change in functionality
152
real bug in production code 151
test conflicts with another test 152
smelling false sense of trust in passing 
tests 156
mixing unit tests and flaky integration 
tests 158
testing multiple exit points 158–160
tests that don’t assert anything 157
tests that keep changing 160
test conflicts with another test 153
type-friendly frameworks 112–113
U
UI (user interface) tests 198–199
unit of work 6, 241
unit test 15, 21
unit testing 3–27
asynchronous code 121–146
basics of 5
characteristics of good unit tests 15–16
creating unit tests from scratch 12–15
defining 5
different exit points, different techniques 12
educating colleagues about, being prepared 
for tough questions 214
entry points and exit points 6–10
exit point types 11
first unit test 28–58
frameworks, advantages of 34–36
integrating into organization 213–230
ad hoc implementations and first 
impressions 223
aiming for specific goals, metrics, and 
KPIs 220
code without tests 228
experiments as door openers 217
getting outside champion 218
guerrilla implementation 217
influence factors 224
lack of political support 223
need for tests if debugger shows that code 
works 229
steps to becoming agent of change 214–216
TDD (test-driven development) 25, 
226–230
time added to process 226–227
tough questions and answers 226–229
proof that unit testing helps 228
QA jobs at risk 227
ways to fail 223
lack of driving force 223
lack of team support 224
ways to succeed 216
convincing management 217
realize that there will be hurdles 222
interaction testing using mock objects
83–103
legacy code 237
selection strategies 234
where to start adding tests 232–233
writing integration tests before 
refactoring 235–236
maintainability 183
stubs, reasons to use 64–66
unit testing asynchronous code, example of 
extracting unit of work 127–129
Unit Testing Principles, Practices, and Patterns 
(Khorikov) 236
unit tests 28
avoiding logic in 153
creating dynamic expected values 153–155
other forms of logic 155–156
avoiding overspecification 177
characteristics of 15
checklist for 16
emulating asynchronous processing with lin-
ear, synchronous tests 16
overview 15
replacing database (or another dependency) 
with stub 16
characteristics of good unit tests 15


---
**Page 260**

INDEX
260
unit tests (continued)
creating
beforeEach() function 45–47
from scratch 12–15
using test() function 52
exceptions, checking for expected thrown 
errors 55–56
faking module behavior in each test 244–245
first unit test 28–58
factory method route 49–50
refactoring to beforeEach() function 47–49
replacing beforeEach() completely with fac-
tory methods 50–51
verifyPassword() function 37
Jest
creating test files 30–31
first test with, preparing working folder 29–30
library, assert, runner, and reporter 33
naming 188–189
overview of 196
parameterized tests, refactoring to 53–55
Password Verifier project 37
readability 187–193
magic values and naming variables 189–190
separating asserts from actions 190
setting up and tearing down 191–192
refactoring production code 43–45
setting test categories 56–57
unit testing frameworks 36
unreadable test code 118
UserCache object 170
USE (unit, scenario, expectation) naming 39
V
value-based test 179
vanilla require.cache 244–245
verification 87
verifier 78
verifier variable 46
verify() function 55, 95, 178–180
verifyPassword() function 45, 86, 90
Arrange-Act-Assert pattern 38
describe() function 40–41
first test for 37
Jest syntax flavors 42
Jest test for 42
refactoring production code 43–45
structure can imply context 41–42
testing strings, comparing 40
testing test 39
verifyPassword(rules) function 37
W
WebsiteVerifier class 136–137
website-verifier example 135–136
written class 98
X
xUnit frameworks 36
xUnit test patterns and naming things 64
xUnit Test Patterns: Refactoring Test Code 
(Meszaros) 11, 64, 89


---
**Page Back cover**

ISBN-13: 978-1-61729-748-9
T
he art of unit testing is more than just learning the right 
collection of tools and practices. It’s about understanding 
what makes great tests tick, fi nding the right strategy for each 
unique situation, and knowing what to do when the testing process 
gets messy. Th is book delivers insights and advice that will trans-
form the way you test your soft ware. 
The Art of Unit Testing, Third Edition shows you how to create 
readable and maintainable tests. It goes well beyond basic test 
creation into organization-wide test strategies, troubleshooting, 
working with legacy code, and “merciless” refactoring. You’ll love 
the practical examples and familiar scenarios that make testing 
come alive as you read. Th is third edition has been updated with 
techniques specifi c to object-oriented, functional, and modular 
coding styles. Th e examples use JavaScript.
What’s Inside
Deciding on test types and strategies 
Test Entry & Exit Points
Refactoring legacy code 
Fakes, stubs, mock objects, and isolation frameworks
Object-Oriented, Functional, and Modular testing styles
Examples use JavaScript, TypeScript, and Node.js.
Roy Osherove is an internationally-recognized expert 
in unit testing and agile soft ware methodology. 
Vladimir Khorikov is the author of Manning’s Unit 
Testing Principles, Practices, and Patterns, a Plural-
sight author, and a Microsoft  MVP. 
For print book owners, all ebook formats are free:
https://www.manning.com/freebook
The Art of Unit Testing THIRD EDITION
DEVELOPMENT
 
“
Our testing bible. Th e Java-
Script community is fortunate 
to have it adapted to our favorite 
language.”
 
—Yoni Goldberg, 
Node.js testing consultant, author of 
Node.js Best Practices 
“
A testing masterpiece!”
—Jaume López, Institut Guttmann
“
Teaches you the philosophy 
as well as the nuts and bolts 
  for eff ective unit testing.”
—Matteo Gildone
Springer Nature
“
A proper view of what 
to test, when, and how 
  to do it well.”
 
—Rich Yonts, Teradata
M A N N I N G
Osherove ● Khorikov
See first page
Roy Osherove



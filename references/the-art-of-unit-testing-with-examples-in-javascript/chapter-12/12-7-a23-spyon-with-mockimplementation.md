# 12.7 A.2.3 spyOn with mockImplementation() (pp.241-244)

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



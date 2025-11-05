# 12.8 A.4.1 Stubbing a module with vanilla require.cache (pp.244-246)

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



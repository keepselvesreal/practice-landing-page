# 4.5.2 Refactoring the production code in a modular injection style (pp.91-92)

---
**Page 91**

91
4.5
Modular-style mocks
because using these techniques leads to more pain and suffering than is usual when
dealing with code. 
4.5.2
Refactoring the production code in a modular injection style
We can abstract away the module dependencies into their own object and allow the
user of our module to replace that object as follows.
const originalDependencies = {             
    log: require('./complicated-logger'),  
};                                         
let dependencies = { ...originalDependencies };    
const resetDependencies = () => {                
    dependencies = { …originalDependencies };    
};                                               
const injectDependencies = (fakes) => {    
    Object.assign(dependencies, fakes);    
};                                         
const verifyPassword = (input, rules) => {
    const failed = rules
        .map(rule => rule(input))
        .filter(result => result === false);
    if (failed.length === 0) {
        dependencies.log.info('PASSED');
        return true;
    }
    dependencies.log.info('FAIL');
    return false;
};
module.exports = {
    verifyPassword,        
    injectDependencies,    
    resetDependencies      
};
There’s more production code here, and it seems more complex, but this allows us to
replace dependencies in our tests in a relatively easy manner if we are forced to work
in such a modular fashion. 
 The originalDependencies variable will always hold the original dependencies, so
that we never lose them between tests. dependencies is our layer of indirection. It
defaults to the original dependencies, but our tests can direct the code under test to
replace that variable with custom dependencies (without knowing anything about the
internals of the module). injectDependencies and resetDependencies are the pub-
lic API that the module exposes for overriding and resetting the dependencies. 
Listing 4.5
Refactoring to a modular injection pattern
Holding original 
dependencies
The layer of 
indirection
A function that resets 
the dependencies 
A function that overrides 
the dependencies
Exposing the API to the 
users of the module


---
**Page 92**

92
CHAPTER 4
Interaction testing using mock objects
4.5.3
A test example with modular-style injection
The following listing shows what a test for modular injection might look like.
const {
  verifyPassword,
  injectDependencies,
  resetDependencies,
} = require("./password-verifier-injectable");
describe("password verifier", () => {
  afterEach(resetDependencies);
  describe("given logger and passing scenario", () => {
    it("calls the logger with PASS", () => {
      let logged = "";
      const mockLog = { info: (text) => (logged = text) };
      injectDependencies({ log: mockLog });
      verifyPassword("anything", []);
      expect(logged).toMatch(/PASSED/);
    });
  });
});
As long as we don’t forget to use the resetDependencies function after each test, we
can now inject modules pretty easily for test purposes. The obvious main caveat is that
this approach requires each module to expose inject and reset functions that can be
used from the outside. This might or might not work with your current design limita-
tions, but if it does, you can abstract them both into reusable functions and save your-
self a lot of boilerplate code.
4.6
Mocks in a functional style 
Let’s jump into a few of the functional styles we can use to inject mocks into our code
under test.
4.6.1
Working with a currying style
Let’s implement the currying technique introduced in chapter 3 to perform a more
functional-style injection of our logger. In the following listing, we’ll use lodash, a
library that facilitates functional programming in JavaScript, to get currying working
without too much boilerplate code.
const verifyPassword3 = _.curry((rules, logger, input) => {
    const failed = rules
        .map(rule => rule(input))
        .filter(result => result === false);
Listing 4.6
Testing with modular injection
Listing 4.7
Applying currying to our function



# 4.5.1 Example of production code (pp.90-91)

---
**Page 90**

90
CHAPTER 4
Interaction testing using mock objects
4.5.1
Example of production code
Let’s look at a slightly more complicated example than we saw before. In this scenario,
our verifyPassword function depends on two external dependencies: 
 A logger 
 A configuration service
The configuration service provides the logging level that is required. Usually this type
of code would be moved into a special logger module, but for the purposes of this
book’s examples, I’m putting the logic that calls logger.info and logger.debug
directly in the code under test.
const { info, debug } = require("./complicated-logger");
const { getLogLevel } = require("./configuration-service");
const log = (text) => {
  if (getLogLevel() === "info") {
    info(text);
  }
  if (getLogLevel() === "debug") {
    debug(text);
  }
};
const verifyPassword = (input, rules) => {
  const failed = rules
    .map((rule) => rule(input))
    .filter((result) => result === false);
  if (failed.length === 0) {
    log("PASSED");   
    return true;
  }
  log("FAIL");       
  return false;
};
module.exports = {
  verifyPassword,
};
Let’s assume that we realized we have a bug when we call the logger. We’ve changed
the way we check for failures, and now we call the logger with a PASSED result when
the number of failures is positive instead of zero. How can we prove that this bug
exists, or that we’ve fixed it, with a unit test?
 Our problem here is that we are importing (or requiring) the modules directly in
our code. If we want to replace the logger module, we have to either replace the file or
perform some other dark magic through Jest’s API. I wouldn’t recommend that usually,
Listing 4.4
A hard modular dependency 
Calling the 
logger


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



# 4.5.3 A test example with modular-style injection (pp.92-92)

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



# 5.4.1 Using a loosely typed framework (pp.110-112)

---
**Page 110**

110
CHAPTER 5
Isolation frameworks
test("given logger and passing scenario", () => {
  let logged = "";                            
  const mockLog = { info: (text) => (logged = text) };   
  const passVerify = makeVerifier([], mockLog);
  passVerify("any input");
  expect(logged).toMatch(/PASSED/);   
});
It works—we’re able to verify that the logger function was called, but that’s a lot of work
that can become very repetitive. Enter isolation frameworks like Jest. jest.fn() is the
simplest way to get rid of such code. The following listing shows how we can use it.
test('given logger and passing scenario', () => {
  const mockLog = { info: jest.fn() };
  const verify = makeVerifier([], mockLog);
  verify('any input');
  expect(mockLog.info)
    .toHaveBeenCalledWith(stringMatching(/PASS/));
});
Compare this code with the previous example. It’s subtle, but it saves plenty of time.
Here we’re using jest.fn() to get back a function that is automatically tracked by
Jest, so that we can query it later using Jest’s API via toHaveBeenCalledWith(). It’s
small and cute, and it works well any time you need to track calls to a specific function.
The stringMatching function is an example of a matcher. A matcher is usually defined
as a utility function that can assert on the value of a parameter being sent into a func-
tion. The Jest docs use the term a bit more liberally, but you can find the full list of
matchers in the Jest documentation at https://jestjs.io/docs/en/expect. 
 To summarize, jest.fn() works well for single-function-based mocks and stubs.
Let’s move on to a more object-oriented challenge.
5.4
Object-oriented dynamic mocks and stubs
As we’ve just seen, jest.fn() is an example of a single-function faking utility func-
tion. It works well in a functional world, but it breaks down a bit when we try to use it
on full-blown API interfaces or classes that contain multiple functions. 
5.4.1
Using a loosely typed framework
I mentioned before that there are two categories of isolation frameworks. To start, we’ll
use the first (loosely typed, function-friendly) kind. The following listing is an example
of trying to tackle the IComplicatedLogger we looked at in the previous chapter. 
Listing 5.3
Manually mocking a function to verify it was called
Listing 5.4
Using jest.fn() for simple function mocks
Declaring a custom variable 
to hold the value passed in
Saving the 
passed-in value 
to that variable
Asserting on the 
value of the variable


---
**Page 111**

111
5.4
Object-oriented dynamic mocks and stubs
export interface IComplicatedLogger {
    info(text: string, method: string)
    debug(text: string, method: string)
    warn(text: string, method: string)
    error(text: string, method: string)
}
Creating a handwritten stub or mock for this interface may be very time consuming,
because you’d need to remember the parameters on a per-method basis, as the next
listing shows.
describe("working with long interfaces", () => {
  describe("password verifier", () => {
    class FakeLogger implements IComplicatedLogger {
      debugText = "";
      debugMethod = "";
      errorText = "";
      errorMethod = "";
      infoText = "";
      infoMethod = "";
      warnText = "";
      warnMethod = "";
      debug(text: string, method: string) {
        this.debugText = text;
        this.debugMethod = method;
      }
      error(text: string, method: string) {
        this.errorText = text;
        this.errorMethod = method;
      }
      ...
    }
    test("verify, w logger & passing, calls logger with PASS", () => {
      const mockLog = new FakeLogger();
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(mockLog.infoText).toMatch(/PASSED/);
    });
  });
});
What a mess. Not only is this handwritten fake time consuming and cumbersome to
write, what happens if you want it to return a specific value somewhere in the test, or
Listing 5.5
The IComplicatedLogger interface
Listing 5.6
Handwritten stubs creating lots of boilerplate code


---
**Page 112**

112
CHAPTER 5
Isolation frameworks
simulate an error from a function call on the logger? We can do it, but the code gets
ugly fast.
 Using an isolation framework, the code for doing this becomes trivial, more read-
able, and much shorter. Let’s use jest.fn() for the same task and see where we end up.
import stringMatching = jasmine.stringMatching;
describe("working with long interfaces", () => {
  describe("password verifier", () => {
    test("verify, w logger & passing, calls logger with PASS", () => {
      const mockLog: IComplicatedLogger = {    
        info: jest.fn(),                       
        warn: jest.fn(),                       
        debug: jest.fn(),                      
        error: jest.fn(),                      
      };
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(mockLog.info)
        .toHaveBeenCalledWith(stringMatching(/PASS/));
    });
  });
});
Not too shabby. Here we simply outline our own object and attach a jest.fn() func-
tion to each of the functions in the interface. This saves a lot of typing, but it has one
important caveat: whenever the interface changes (a function is added, for example),
we’ll have to go back to the code that defines this object and add that function. With
plain JavaScript, this would be less of an issue, but it can still create some complica-
tions if the code under test uses a function we didn’t define in the test. 
 In any case, it might be wise to push the creation of such a fake object into a fac-
tory helper method, so that the creation only exists in a single place.
5.4.2
Switching to a type-friendly framework
Let’s switch to the second category of frameworks and try substitute.js (www.npmjs
.com/package/@fluffy-spoon/substitute). We have to choose one, and I like the C#
version of this framework a lot and used it in the previous edition of this book. 
 With substitute.js (and the assumption of working with TypeScript), we can write
code like the following.
import { Substitute, Arg } from "@fluffy-spoon/substitute";
describe("working with long interfaces", () => {
  describe("password verifier", () => {
Listing 5.7
Mocking individual interface functions with jest.fn()
Listing 5.8
Using substitute.js to fake a full interface
Setting up the 
mock using Jest



# 4.9.1 A functional example of a partial mock (pp.101-102)

---
**Page 101**

101
4.9
Partial mocks
4.8.4
The interface segregation principle
The second of the preceding conditions might need a bit of explanation. It relates
to the interface segregation principle (ISP; https://en.wikipedia.org/wiki/Interface_
segregation_principle). ISP means that if we have an interface that contains more
functionality than we require, we should create a small, simpler adapter interface that
contains just the functionality we need, preferably with fewer functions, better names,
and fewer parameters. 
 This will end up making our tests much simpler. By abstracting away the real
dependencies, we won’t need to change our tests when the complicated interfaces
change—only a single adapter class file somewhere. We’ll see an example of this in
chapter 5.
4.9
Partial mocks
It’s possible, in JavaScript and in most other languages and associated test frameworks,
to take over existing objects and functions and “spy” on them. By spying on them, we
can later check if they were called, how many times, and with which arguments. 
 This essentially can turn parts of a real object into mock functions, while keeping
the rest of the object as a real object. This can create more complicated tests that are
more brittle, but it can sometimes be a viable option, especially if you’re dealing with
legacy code (see chapter 12 for more on legacy code). 
4.9.1
A functional example of a partial mock
The following listing shows what such a test might look like. We create the real logger,
and then we simply override one of its existing real functions using a custom function.
describe("password verifier with interfaces", () => {
  test("verify, with logger, calls logger", () => {
    const testableLog: RealLogger = new RealLogger();   
    let logged = "";
    testableLog.info = (text) => (logged = text);   
    const verifier = new PasswordVerifier([], testableLog);
    verifier.verify("any input");
    expect(logged).toMatch(/PASSED/);
  });
});
In this test, I’m instantiating a RealLogger, and in the next line I’m replacing one of
its existing functions with a fake one. More specifically, I’m using a mock function that
allows me to track its latest invocation parameter using a custom variable.
 The important part here is that the testableLog variable is a partial mock. That
means that at least some of its internal implementation is not fake and might have real
dependencies and logic in it.
Listing 4.17
A partial mock example 
Instantiating a 
real logger
Mocking one of 
its functions


---
**Page 102**

102
CHAPTER 4
Interaction testing using mock objects
 Sometimes it makes sense to use partial mocks, especially when you’re working
with legacy code and you might need to isolate some existing code from its dependen-
cies. I’ll touch more on that in chapter 12.
4.9.2
An object-oriented partial mock example
One object-oriented version of a partial mock uses inheritance to override functions
from real classes so that we can verify they were called. The following listing shows
how we can do this using inheritance and overrides in JavaScript.
class TestableLogger extends RealLogger {    
  logged = "";
  info(text) {             
    this.logged = text;    
  }                        
  // the error() and debug() functions
  // are still "real"
}
describe("partial mock with inheritance", () => {
  test("verify with logger, calls logger", () => {
    const mockLog: TestableLogger = new TestableLogger();
    const verifier = new PasswordVerifier([], mockLog);
    verifier.verify("any input");
    expect(mockLog.logged).toMatch(/PASSED/);
  });
});
I inherit from the real logger class in my tests and then use the inherited class, not the
original class, in my tests. This technique is commonly called Extract and Override,
and you can find more about this in Michael Feathers’ book Working Effectively with
Legacy Code (Pearson, 2004). 
 Note that I’ve named the fake logger class “TestableXXX” because it’s a testable
version of real production code, containing a mix of fake and real code, and this
convention helps me make this explicit for the reader. I also put the class right
alongside my tests. My production code doesn’t need to know that this class exists.
This Extract and Override style requires that my class in production code allows
inheritance and that the function allows overriding. In JavaScript this is less of an
issue, but in Java and C# these are explicit design choices that need to be made
(although there are frameworks that allow us to circumvent this rule; we’ll discuss
them in the next chapter).
 In this scenario, we’re inheriting from a class that we’re not testing directly (Real-
Logger). We use that class to test another class (PasswordVerifier). However, this
technique can be used quite effectively to isolate and stub or mock single functions
Listing 4.18
An object-oriented partial mock example 
Inheriting from 
the real logger
Overriding one 
of its functions



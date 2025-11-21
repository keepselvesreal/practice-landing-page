# 4.9.2 An object-oriented partial mock example (pp.102-103)

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


---
**Page 103**

103
Summary
from classes that you’re directly testing. We’ll touch more on that later in the book
when we talk about legacy code and refactoring techniques.
Summary
Interaction testing is a way to check how a unit of work interacts with its outgoing
dependencies: what calls were made and with which parameters. Interaction
testing relates to the third type of exit points: a third-party module, object, or
system. (The first two types are a return value and a state change.)
To do interaction testing, you should use mocks, which are test doubles that replace
outgoing dependencies. Stubs replace incoming dependencies. You should ver-
ify interactions with mocks in tests, but not with stubs. Unlike with mocks, inter-
actions with stubs are implementation details and shouldn't be checked.
It’s OK to have multiple stubs in a test, but you don’t usually want to have more
than a single mock per test, because that means you’re testing more than one
requirement in a single test.
Just like with stubs, there are multiple ways to inject a mock into a unit of work:
– Standard—By introducing a parameter
– Functional—Using a partial application or factory functions
– Modular—Abstracting the module dependency
– Object-oriented—Using an untyped object (in languages like JavaScript) or a
typed interface (in TypeScript)
In JavaScript, a complicated interface can be implemented partially, which
helps reduce the amount of boilerplate. There’s also the option of using partial
mocks, where you inherit from a real class and replace only some of its methods
with fakes.



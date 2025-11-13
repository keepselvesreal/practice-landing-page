# 4.8.3 Downsides of using complicated interfaces directly (pp.100-101)

---
**Page 100**

100
CHAPTER 4
Interaction testing using mock objects
      }
    }
    ...
    test("verify passing, with logger, calls logger with PASS", () => {
      const mockLog = new FakeComplicatedLogger();
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(mockLog.infoWritten).toMatch(/PASSED/);
    });
    test("A more JS oriented variation on this test", () => {
      const mockLog = {} as IComplicatedLogger;
      let logged = "";
      mockLog.info = (text) => (logged = text);
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      expect(logged).toMatch(/PASSED/);
    });
  });
});
Here, we’re declaring, again, a fake logger class (FakeComplicatedLogger) that imple-
ments the IComplicatedLogger interface. Look at how much boilerplate code we
have. This will be especially true if we’re working in strongly typed object-oriented lan-
guages such as Java, C#, or C++. There are ways around all this boilerplate code, which
we’ll touch on in the next chapter. 
4.8.3
Downsides of using complicated interfaces directly
There are other downsides to using long, complicated interfaces in our tests:
If we’re saving arguments being sent in manually, it’s more cumbersome to ver-
ify multiple arguments across multiple methods and calls. 
It’s likely that we are depending on third-party interfaces instead of internal
ones, and this will end up making our tests more brittle as time goes by. 
Even if we are depending on internal interfaces, long interfaces have more rea-
sons to change, and now so do our tests. 
What does this mean for us? I highly recommend using only fake interfaces that meet
both of these conditions:
You control the interfaces (they are not made by a third party).
They are adapted to the needs of your unit of work or component. 


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



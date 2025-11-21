# 5.4.2 Switching to a type-friendly framework (pp.112-114)

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


---
**Page 113**

113
5.4
Object-oriented dynamic mocks and stubs
    test("verify, w logger & passing, calls logger w PASS", () => {
      const mockLog = Substitute.for<IComplicatedLogger>();   
      const verifier = new PasswordVerifier2([], mockLog);
      verifier.verify("anything");
      mockLog.received().info(                 
        Arg.is((x) => x.includes("PASSED")),   
        "verify"                               
      );
    });
  });
});
In the preceding listing, we generate the fake object, which absolves us of caring
about any functions other than the one we’re testing against, even if the object’s signa-
ture changes in the future. We then use .received() as our verification mechanism,
as well as another argument matcher, Arg.is, this time from substitute.js’s API, which
works just like string matches from Jasmine. The added benefit here is that if new
functions are added to the object’s signature, we will be less likely to need to change
the test, and there’s no need to add those functions to any tests that use the same
object signature.  
OK, that was mocks. What about stubs?
Isolation frameworks and the Arrange-Act-Assert pattern
Notice that the way you use the isolation framework matches nicely with the Arrange-
Act-Assert structure, which we discussed in chapter 1. You start by arranging a fake
object, you act on the thing you’re testing, and then you assert on something at the
end of the test. 
It wasn’t always this easy, though. In the olden days (around 2006), most of the open
source isolation frameworks didn’t support the idea of Arrange-Act-Assert and instead
used a concept called Record-Replay (we’re talking about Java and C#). Record-
Replay was a nasty mechanism where you’d have to tell the isolation API that its fake
object was in record mode, and then you’d have to call the methods on that object
as you expected them to be called from production code. Then you’d have to tell the
isolation API to switch into replay mode, and only then could you send your fake object
into the heart of your production code. An example can be seen on the Baeldung site
at www.baeldung.com/easymock.
Compared to today’s ability to write tests that use the far more readable Arrange-Act-
Assert model, this tragedy cost many developers millions of combined hours in pains-
taking test reading to figure out exactly where tests failed.
If you have the first edition of this book, you can see an example of Record-Replay
when I showed Rhino Mocks (which initially had the same design).
Generating 
the fake 
object
Verifying the 
fake object 
was called


---
**Page 114**

114
CHAPTER 5
Isolation frameworks
5.5
Stubbing behavior dynamically
Jest has a very simple API for simulating return values for modular and functional
dependencies: mockReturnValue() and mockReturnValueOnce().
test("fake same return values", () => {
  const stubFunc = jest.fn()
    .mockReturnValue("abc");
  //value remains the same
  expect(stubFunc()).toBe("abc");
  expect(stubFunc()).toBe("abc");
  expect(stubFunc()).toBe("abc");
});
test("fake multiple return values", () => {
  const stubFunc = jest.fn()
    .mockReturnValueOnce("a")
    .mockReturnValueOnce("b")
    .mockReturnValueOnce("c");
  //value remains the same
  expect(stubFunc()).toBe("a");
  expect(stubFunc()).toBe("b");
  expect(stubFunc()).toBe("c");
  expect(stubFunc()).toBe(undefined);
});
Notice that, in the first test, we’re setting a permanent return value for the duration of
the test. This is my preferred method of writing tests if I can use it, because it makes
the tests simple to read and maintain. If we do need to simulate multiple values, we
can use mockReturnValueOnce. 
 If you need to simulate an error or do anything more complicated, you can use
mockImplementation() and mockImplementationOnce():
yourStub.mockImplementation(() => {
  throw new Error();
});
5.5.1
An object-oriented example with a mock and a stub
Let’s add another ingredient into our Password Verifier equation. 
Let’s say that the Password Verifier is not active during a special maintenance
window, when software is being updated. 
When a maintenance window is active, calling verify() on the verifier will
cause it to call logger.info() with “under maintenance.” 
Otherwise it will call logger.info() with a “passed” or “failed” result. 
Listing 5.9
Stubbing a value from a fake function with jest.fn() 



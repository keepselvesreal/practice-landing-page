# 7.4.4 Testing multiple exit points (pp.158-160)

---
**Page 158**

158
CHAPTER 7
Trustworthy tests
7.4.3
Mixing unit tests and flaky integration tests
They say that one rotten apple spoils the bunch. The same is true for flaky tests
mixed in with nonflaky tests. Integration tests are much more likely to be flaky than
unit tests because they have more dependencies. If you find that you have a mix of
integration and unit tests in the same folder or test execution command, you should
be suspicious.
 Humans like to take the path of least resistance, and it’s no different when it comes
to coding. Suppose that a developer runs all the tests and one of them fails—if there’s
a way to blame a missing configuration or a network issue instead of spending time
investigating and fixing a real problem, they will. That’s especially true if they’re under
serious time pressure or they’re overcommitted to delivering things they’re already
late on.
 The easiest thing is to accuse any failing test of being a flaky test. Because flaky and
nonflaky tests are mixed up with each other, that’s a simple thing to do, and it’s a good
way to ignore the issue and work on something more fun. Because of this human fac-
tor, it’s best to remove the option to blame a test for being flaky. What should you do
to prevent this? Aim to have a safe green zone by keeping your integration and unit tests
in separate places.
 A safe green test area should contain only nonflaky, fast tests, where developers
know that they can get the latest code version, they can run all the tests in that name-
space or folder, and the tests should all be green (given no changes to production
code). If some tests in the safe green zone don’t pass, a developer is much more likely
to be concerned.
 An added benefit to this separation is that developers are more likely to run the
unit tests more often, now that the run time is faster without the integration tests. It’s
better to have some feedback than no feedback, right? The automated build pipeline
should take care of running any of the “missing” feedback tests that developers can’t
or won’t run on their local machines.
7.4.4
Testing multiple exit points
An exit point (I’ll also refer to it as a concern) is explained in chapter 1. It’s a single end
result from a unit of work: a return value, a change to system state, or a call to a third-
party object.
 Here’s a simple example of a function that has two exit points, or two concerns. It
both returns a value and triggers a passed-in callback function:
const trigger = (x, y, callback) => {
  callback("I'm triggered");
  return x + y;
};
We could write a test that checks both of these exit points at the same time.
 


---
**Page 159**

159
7.4
Smelling a false sense of trust in passing tests
describe("trigger", () => {
  it("works", () => {
    const callback = jest.fn();
    const result = trigger(1, 2, callback);
    expect(result).toBe(3);
    expect(callback).toHaveBeenCalledWith("I'm triggered");
  });
});
The first reason testing more than one concern in a test can backfire is that your test
name suffers. I’ll discuss readability in chapter 9, but here’s a quick note on naming:
naming tests is hugely important for both debugging and documentation purposes. I
spend a lot of time thinking about good names for tests, and I’m not ashamed to admit it. 
 Naming a test may seem like a simple task, but if you’re testing more than one
thing, giving the test a good name that indicates what’s being tested is difficult. Often
you end up with a very generic test name that forces the reader to read the test code.
When you test just one concern, naming the test is easy. But wait, there’s more. 
 More disturbingly, in most unit test frameworks, a failed assert throws a special type
of exception that’s caught by the test framework runner. When the test framework
catches that exception, it means the test has failed. Most exceptions in most lan-
guages, by design, don’t let the code continue. So if this line,
expect(result).toBe(3);
fails the assert, this line will not execute at all:
expect(callback).toHaveBeenCalledWith("I'm triggered");
The test method exits on the same line where the exception is thrown. Each of these
asserts can and should be considered different requirements, and they can also, and in
this case likely should, be implemented separately and incrementally, one after the other.
 Consider assert failures as symptoms of a disease. The more symptoms you can
find, the easier the disease will be to diagnose. After a failure, subsequent asserts
aren’t executed, and you’ll miss seeing other possible symptoms that could provide
valuable data (symptoms) that would help you narrow your focus and discover the
underlying problem. Checking multiple concerns in a single unit test adds complexity
with little value. You should run additional concern checks in separate, self-contained
unit tests so that you can see what really fails.
 Let’s break it up into two separate tests.
describe("trigger", () => {
  it("triggers a given callback", () => {
    const callback = jest.fn();
Listing 7.6
Checking two exit points in the same test
Listing 7.7
Checking the two exit points in separate tests


---
**Page 160**

160
CHAPTER 7
Trustworthy tests
    trigger(1, 2, callback);
    expect(callback).toHaveBeenCalledWith("I'm triggered");
  });
  it("sums up given values", () => {
    const result = trigger(1, 2, jest.fn());
    expect(result).toBe(3);
  });
});
Now we can clearly separate the concerns, and each one can fail separately.
 Sometimes it’s perfectly okay to assert multiple things in the same test, as long as
they are not multiple concerns. Take the following function and its associated test as an
example. makePerson is designed to build a new person object with some properties. 
const makePerson = (x, y) => {
  return {
    name: x,
    age: y,
    type: "person",
  };
};
describe("makePerson", () => {
  it("creates person given passed in values", () => {
    const result = makePerson("name", 1);
    expect(result.name).toBe("name");
    expect(result.age).toBe(1);
  });
});
In our test, we are asserting on both name and age together, because they are part of
the same concern (building the person object). If the first assert fails, we likely don’t
care about the second assert because something might have gone terribly wrong while
building the object in the first place.
TIP
Here’s a test break-up hint: If the first assert fails, do you still care what
the result of the next assert is? If you do, you should probably separate the test
into two tests.
7.4.5
Tests that keep changing
If a test is using the current date and time as part of its execution or assertions, then we
can claim that every time the test runs, it’s a different test. The same can be said of tests
that use random numbers, machine names, or anything that depends on grabbing a
current value from outside the test’s environment. There’s a big chance its results won’t
be consistent, and that means they can be flaky. For us, as developers, flaky tests reduce
our trust in the failed results of the test (as I’ll discuss in the next section). 
Listing 7.8
Using multiple asserts to verify a single exit point



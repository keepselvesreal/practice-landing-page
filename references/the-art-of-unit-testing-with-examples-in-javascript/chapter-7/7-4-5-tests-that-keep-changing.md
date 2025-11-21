# 7.4.5 Tests that keep changing (pp.160-161)

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


---
**Page 161**

161
7.5
Dealing with flaky tests
 Another huge potential issue with dynamically generated values is that if we don’t
know ahead of time what the input into the system might be, we also have to compute
the expected output of the system, and that can lead to a buggy test that depends on
repeating production logic, as mentioned in section 7.3. 
7.5
Dealing with flaky tests
I’m not sure who came up with the term flaky tests, but it does fit the bill. It’s used to
describe tests that, given no changes to the code, return inconsistent results. This
might happen frequently or very rarely, but it does happen. 
 Figure 7.1 illustrates where flakiness comes from. The figure is based on the num-
ber of real dependencies the tests have. Another way to think about this is how many
moving parts the tests have. For this book, we’re mostly concerning ourselves with the
Flakiness caused by
• Shared memory resources
• Threads
• Random values
• Dynamically generated inputs/outputs
• Time
• Logic bugs
Flakiness also caused by
• Shared resources
• Network issues
• Conﬁguration issues
• Permission issues
• Load issues
• Security issues
• Other systems are down
• And more...
Conﬁdence/Flakiness
E2E/UI system tests
E2E/UI isolated tests
API tests (out of process)
Integration tests (in memory)
Component tests (in memory)
Unit tests (in memory)
Figure 7.1
The higher the level of the tests, the more real dependencies they use, which 
gives us confidence in the overall system correctness but results in more flakiness.



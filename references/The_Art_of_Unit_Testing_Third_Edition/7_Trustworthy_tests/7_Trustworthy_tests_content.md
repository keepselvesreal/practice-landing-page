
--- 페이지 177 ---
149
Trustworthy tests
No matter how you organize your tests, or how many you have, they’re worth very
little if you can’t trust them, maintain them, or read them. The tests that you write
should have three properties that together make them good:
Trustworthiness—Developers will want to run trustworthy tests, and they’ll
accept the test results with confidence. Trustworthy tests don’t have bugs,
and they test the right things. 
Maintainability—Unmaintainable tests are nightmares because they can ruin
project schedules, or they may be sidelined when the project is put on a
more aggressive schedule. Developers will simply stop maintaining and fix-
ing tests that take too long to change or that need to change often on very
minor production code changes.
Readability—This refers not only to being able to read a test but also figuring
out the problem if the test seems to be wrong. Without readability, the other
This chapter covers
How to know you trust a test
Detecting untrustworthy failing tests
Detecting untrustworthy passing tests
Dealing with flaky tests

--- 페이지 178 ---
150
CHAPTER 7
Trustworthy tests
two pillars fall pretty quickly. Maintaining tests becomes harder, and you can’t
trust them anymore because you don’t understand them.
This chapter and the next two present a series of practices related to each of these pil-
lars that you can use when doing test reviews. Together, the three pillars ensure your
time is well used. Drop one of them, and you run the risk of wasting everyone’s time.
 Trust is the first of the three pillars that I like to evaluate good unit tests on, so it’s
fitting that we start with it. If we don’t trust the tests, what’s the point in running
them? What’s the point in fixing them or fixing the code if they fail? What’s the point
of maintaining them? 
7.1
How to know you trust a test
What does “trust” mean for a software developer in the context of a test? Perhaps it’s
easier to explain based on what we do or don’t do when a test fails or passes. 
 You might not trust a test if
It fails and you’re not worried (you believe it’s a false positive).
You feel like it’s fine to ignore the results of this test, either because it passes
every once in a while or because you feel it’s not relevant or buggy. 
It passes and you are worried (you believe it’s a false negative).
You still feel the need to manually debug or test the software “just in case.”
You might trust the test if
The test fails and you’re genuinely worried that something broke. You don’t
move on, assuming the test is wrong.
The test passes and you feel relaxed, not feeling the need to test or debug
manually.
In the next few sections, we’ll look at test failures as a way to identify untrustworthy tests,
and we’ll look at passing tests’ code and see how to detect untrustworthy test code.
Finally, we’ll cover a few generic practices that can enhance trustworthiness in tests.
7.2
Why tests fail
Ideally, your tests (any tests, not just unit tests) should only be failing for a good reason.
That good reason is, of course, that a real bug was uncovered in the underlying pro-
duction code. 
 Unfortunately, tests can fail for a multitude of reasons. We can assume that a test
failing for any reason other than that one good reason should trigger an “untrust-
worthy” warning, but not all tests fail the same way, and recognizing the reasons tests
may fail can help us build a roadmap for what we’d like to do in each case.
 Here are some reasons that tests fail:
A real bug has been uncovered in the production code
A buggy test gives a false failure
The test is out of date due to a change in functionality

--- 페이지 179 ---
151
7.2
Why tests fail
The test conflicts with another test
The test is flaky
Except for the first point here, all these reasons are the test telling you it should not
be trusted in its current form. Let’s go through them.
7.2.1
A real bug has been uncovered in the production code
The first reason a test will fail is when there is a bug in the production code. That’s
good! That’s why we have tests. Let’s move on to the other reasons tests fail.
7.2.2
A buggy test gives a false failure
A test will fail if the test is buggy. The production code might be correct, but that
doesn’t matter if the test itself has a bug that causes the test to fail. It could be that
you’re asserting on the wrong expected result of an exit point, or that you’re using the
system under test incorrectly. It could be that you’re setting up the context for the test
wrong or that you misunderstand what you were supposed to test. 
 Either way, a buggy test can be quite dangerous, because a bug in a test can also
cause it to pass and leave you unsuspecting of what’s really going on. We’ll talk more
about tests that don’t fail but should later in the chapter.
HOW TO RECOGNIZE A BUGGY TEST
You have a failing test, but you might have already debugged the production code and
couldn’t find any bug there. This is when you should start suspecting the failing test.
There’s no way around it. You’re going to have to slowly debug the test code. 
 Here are some potential causes of false failures:
Asserting on the wrong thing or on the wrong exit point
Injecting a wrong value into the entry point
Invoking the entry point incorrectly
It could also be some other small mistake that happens when you write code at 2 A.M.
(That’s not a sustainable coding strategy, by the way. Stop doing that.)
WHAT DO YOU DO ONCE YOU’VE FOUND A BUGGY TEST?
When you find a buggy test, don’t panic. This might be the millionth time you’ve
found one, so you might be panicking and thinking “our tests suck.” You might also be
right about that. But that doesn’t mean you should panic. Fix the bug, and run the
test to see if it now passes.
 If the test passes, don’t be happy too soon! Go to the production code and place an
obvious bug that should be caught by the newly fixed test. For example, change a
Boolean to always be true. Or false. Then run the test again, and make sure it fails. If
it doesn’t, you might still have a bug in your test. Fix the test until it can find the pro-
duction bug and you can see it fail.
 Once you are sure the test is failing for an obvious production code issue, fix the
production code issue you just made and run the test again. It should pass. If the test

--- 페이지 180 ---
152
CHAPTER 7
Trustworthy tests
is now passing, you’re done. You’ve now seen the test passing when it should and fail-
ing when it should. Commit the code and move on.
 If the test is still failing, it might have another bug. Repeat the whole process again
until you verify that the test fails and passes when it should. If the test is still failing, you
might have come across a real bug in production code. In which case, good for you!
HOW TO AVOID BUGGY TESTS IN THE FUTURE
One of the best ways I know to detect and prevent buggy tests is to write your code in a
test-driven manner. I explained a bit about this technique in chapter 1 of this book. I
also practice this technique in real life.
 Test-driven development (TDD) allows us to see both states of a test: both that it
fails when it should (that’s the initial state we start in) and that it passes when it should
(when the production code under test is written to make the test pass). If the test con-
tinues to fail, we’ve found a bug in the production code. If the test starts out passing,
we have a bug in the test. 
 Another great way to reduce the likelihood of bugs in tests is to remove logic from
them. More on this in section 7.3.
7.2.3
The test is out of date due to a change in functionality
A test can fail if it’s no longer compatible with the current feature that’s being tested.
Say you have a login feature, and in an earlier version, you needed to provide a user-
name and a password to log in. In the new version, a two-factor authentication scheme
replaced the old login. The existing test will start failing because it’s not providing the
right parameters to the login functions.
WHAT CAN YOU DO NOW?
You now have two options:
Adapt the test to the new functionality.
Write a new test for the new functionality, and remove the old test because it has
now become irrelevant.
AVOIDING OR PREVENTING THIS IN THE FUTURE
Things change. I don’t think it’s possible to not have out-of-date tests at some point in
time. We’ll deal with change in the next chapter, relating to the maintainability of
tests and how well tests can handle changes in the application. 
7.2.4
The test conflicts with another test
Let’s say you have two tests: one of them is failing and one is passing. Let’s also say they
cannot pass together. You’ll usually only see the failing test, because the passing one is,
well, passing.
 For instance, a test may fail because it suddenly conflicts with a new behavior. On
the other hand, a conflicting test may expect a new behavior but doesn’t find it. The
simplest example is when the first test verifies that calling a function with two parame-
ters produces “3,” whereas the second test expects the same function to produce “4.”

--- 페이지 181 ---
153
7.3
Avoiding logic in unit tests
WHAT CAN YOU DO NOW?
The root cause is that one of the tests has become irrelevant, which means it needs to
be removed. Which one should be removed? That’s a question we’d need to ask a
product owner, because the answer is related to which behavior is correct and
expected from the application. 
AVOIDING THIS IN THE FUTURE
I feel this is a healthy dynamic, and I’m fine with not avoiding it. 
7.2.5
The test is flaky
A test can fail inconsistently. Even if the production code under test hasn’t changed, a
test can suddenly fail without any apparent reason, then pass again, then fail again.
We call a test like that “flaky.” 
 Flaky tests are a special beast, and I’ll deal with them in section 7.5.
7.3
Avoiding logic in unit tests
The chances of having bugs in your tests increase almost exponentially as you include
more and more logic in them. I’ve seen plenty of tests that should have been simple
become dynamic, random-number-generating, thread-creating, file-writing monsters
that are little test engines in their own right. Sadly, because they were “tests,” the
writer didn’t consider that they might have bugs or didn’t write them in a maintain-
able manner. Those test monsters take more time to debug and verify than they save. 
 But all monsters start out small. Often, an experienced developer in the company
will look at a test and start thinking, “What if we made the function loop and create
random numbers as input? We’d surely find lots more bugs that way!” And you will,
especially in your tests. 
 Test bugs are one of the most annoying things for developers, because you’ll
almost never search for the cause of a failing test in the test itself. I’m not saying that
tests with logic don’t have any value. In fact, I’m likely to write such tests myself in
some special situations. But I try to avoid this practice as much as possible. 
 If you have any of the following inside a unit test, your test contains logic that I usu-
ally recommend be reduced or removed completely:

switch, if, or else statements

foreach, for, or while loops
Concatenations (+ sign, etc.)

try, catch
7.3.1
Logic in asserts: Creating dynamic expected values
Here’s a quick example of a concatenation to start us off.
describe("makeGreeting", () => {
  it("returns correct greeting for name", () => {
Listing 7.1
A test with logic in it

--- 페이지 182 ---
154
CHAPTER 7
Trustworthy tests
    const name = "abc";
    const result = trust.makeGreeting(name);
    expect(result).toBe("hello" + name);    
  });
To understand the problem with this test, the following listing shows the code being
tested. Notice that the + sign makes an appearance in both. 
const makeGreeting = (name) => {
  return "hello" + name;      
};
Notice how the algorithm (very simple, but still an algorithm) of connecting a name
with a "hello" string is repeated in both the test and the code under test:
expect(result).toBe("hello" + name);   
return "hello" + name;   
My issue with this test is that the algorithm under test is repeated in the test itself. This
means that if there is a bug in the algorithm, the test also contains the same bug. The
test will not catch the bug, but instead will expect the incorrect result from the code
under test. 
 In this case, the incorrect result is that we’re missing a space character between the
concatenated words, but hopefully you can see how the same issue could become
much more complex with a more complex algorithm.
 This is a trust issue. We can’t trust this test to tell us the truth, since its logic is a
repeat of the logic being tested. The test might pass when the bug exists in the code,
so we can’t trust the test’s result.
WARNING
Avoid dynamically creating the expected value in your asserts; use
hardcoded values when possible. 
A more trustworthy version of this test can be rewritten as follows.
it("returns correct greeting for name 2", () => {
  const result = trust.makeGreeting("abc");
  expect(result).toBe("hello abc");    
});
Because the inputs in this test are so simple, it’s easy to write a hardcoded expected
value. This is what I usually recommend—make the test inputs so simple that it is triv-
ial to create a hardcoded version of the expected value. Note that this is mostly true of
unit tests. For higher-level tests, this is a bit harder to do, which is another reason why
Listing 7.2
Code under test
Listing 7.3
A more trustworthy test
Logic in the 
assertion part
The same logic as in 
the production code
Our test
The code under test
Using a hardcoded value

--- 페이지 183 ---
155
7.3
Avoiding logic in unit tests
higher-level tests should be considered a bit riskier; they often create expected results
dynamically, which you should try to avoid any time you can.
 “But Roy,” you might say, “Now we are repeating ourselves—the string "abc" is
repeated twice. We were able to avoid this in the previous test.” When push comes to
shove, trust should trump maintainability. What good is a highly maintainable test that
I cannot trust? You can read more about code duplication in tests in Vladimir
Khorikov’s article, “DRY vs. DAMP in Unit Tests,” (https://enterprisecraftsmanship
.com/posts/dry-damp-unit-tests/).
7.3.2
Other forms of logic
Here’s the opposite case: creating the inputs dynamically (using a loop) forces us to
dynamically decide what the expected output should be. Suppose we have the follow-
ing code to test.
const isName = (input) => {
  return input.split(" ").length === 2;
};
The following listing shows a clear antipattern for a test.
describe("isName", () => {
  const namesToTest = ["firstOnly", "first second", ""];   
  it("correctly finds out if it is a name", () => {
    namesToTest.forEach((name) => {
      const result = trust.isName(name);
      if (name.includes(" ")) {       
        expect(result).toBe(true);    
      } else {                        
        expect(result).toBe(false);   
      }
    });
  });
});
Notice how we’re using multiple inputs for the test. This forces us to loop over those
inputs, which in itself complicates the test. Remember, loops can have bugs too. 
 Additionally, because we have different scenarios for the values (with and without
spaces) we need an if/else to know what the assertion is expecting, and the if/else
can have bugs too. We are also repeating a part of the production algorithm, which
brings us back to the previous concatenation example and its problems.
 Finally, our test name is too generic. We can only title it as “it works” because we have
to account for multiple scenarios and expected outcomes. That’s bad for readability.
Listing 7.4
A name-finding function
Listing 7.5
Loops and ifs in a test
Declaring 
multiple inputs
Production code 
logic leaking into 
the test

--- 페이지 184 ---
156
CHAPTER 7
Trustworthy tests
 This is an all-around bad test. It’s better to separate this into two or three tests,
each with its own scenario and name. This would allow us to use hardcoded inputs
and assertions and to remove any loops and if/else logic from the code. Anything
more complex causes the following problems:
The test is harder to read and understand.
The test is hard to recreate. For example, imagine a multithreaded test or a test
with random numbers that suddenly fails.
The test is more likely to have a bug or to verify the wrong thing.
Naming the test may be harder because it does multiple things.
Generally, monster tests replace original simpler tests, and that makes it harder to find
bugs in the production code. If you must create a monster test, it should be added as a
new test and not be a replacement for existing tests. Also, it should reside in a project
or folder explicitly titled to hold tests other than unit tests. I call these “integration
tests” or “complex tests” and try to keep their number to an acceptable minimum.
7.3.3
Even more logic
Logic can be found not only in tests but also in test helper methods, handwritten
fakes, and test utility classes. Remember, every piece of logic you add in these places
makes the code that much harder to read and increases the chances of a bug in a util-
ity method that your tests use. 
 If you find that you need to have complicated logic in your test suite for some rea-
son (though that’s generally something I do with integration tests, not unit tests), at
least make sure you have a couple of tests against the logic of your utility methods in
the test project. This will save you many tears down the road.
7.4
Smelling a false sense of trust in passing tests
We’ve now covered failed tests as a means of detecting tests we shouldn’t trust. What
about all those quiet, green tests we have lying all over the place? Should we trust
them? What about a test that we need to do a code review for, before it’s pushed into a
main branch? What should we look for?
 Let’s use the term “false-trust” to describe trusting a test that you really shouldn’t,
but you don’t know it yet. Being able to review tests and find possible false-trust issues
has immense value because, not only can you fix those tests yourself, you’re affecting
the trust of everyone else who’s ever going to read or run those tests. Here are some
reasons I reduce my trust in tests, even if they are passing:
The test contains no asserts.
I can’t understand the test.
Unit tests are mixed with flaky integration tests.
The test verifies multiple concerns or exit points.
The test keeps changing.

--- 페이지 185 ---
157
7.4
Smelling a false sense of trust in passing tests
7.4.1
Tests that don’t assert anything
We all agree that a test that doesn’t actually verify that something is true or false is less
than helpful, right? Less than helpful because it also costs in maintenance time, refac-
toring, and reading time, and sometimes unnecessary noise if it needs changing due
to API changes in production code. 
 If you see a test with no asserts, consider that there may be hidden asserts in a func-
tion call. This causes a readability problem if the function is not named to explain
this. Sometimes people also write a test that exercises a piece of code simply to make
sure that the code does not throw an exception. This does have some value, and if
that’s the test you choose to write, make sure that the name of the test indicates this
with a term such as “does not throw.” To be even more specific, many test APIs support
the ability to specify that something does not throw an exception. This is how you can
do this in Jest:
expect(() => someFunction()).not.toThrow(error)
If you do have such tests, make sure there’s a very small number of them. I don’t rec-
ommend it as a standard, but only for really special cases.
 Sometimes people simply forget to write an assert due to lack of experience. Con-
sider adding the missing assert or removing the test if it brings no value. People may
also actively write tests to achieve some imagined test coverage goal set by manage-
ment. Those tests usually serve no real value except to get management off people’s
backs so they can do real work.
TIP
Code coverage shouldn’t ever be a goal on its own. It doesn’t mean
“code quality.” In fact, it often causes developers to write meaningless tests
that will cost even more time to maintain. Instead, measure “escaped bugs,”
“time to fix,” and other metrics that we’ll discuss in chapter 11.
7.4.2
Not understanding the tests
This is a huge issue, and I’ll deal with it in depth in chapter 9. There are several possi-
ble issues:
Tests with bad names
Tests that are too long or have convoluted code
Tests containing confusing variable names
Tests containing hidden logic or assumptions that cannot be understood easily
Test results that are inconclusive (neither failed nor passed)
Test messages that don’t provide enough information
If you don’t understand the test that’s failing or passing, you don’t know if you should
be worried or not.

--- 페이지 186 ---
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
 

--- 페이지 187 ---
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

--- 페이지 188 ---
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

--- 페이지 189 ---
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

--- 페이지 190 ---
162
CHAPTER 7
Trustworthy tests
bottom third of this diagram: unit and component tests. However, I want to touch on
the higher-level flakiness so I can give you some pointers on what to research.
 At the lowest level, our tests have full control over all of their dependencies and
therefore have no moving parts, either because they’re faking them or because they
run purely in memory and can be configured. We did this in chapters 3 and 4. Execu-
tion paths in the code are fully deterministic because all the initial states and expected
return values from various dependencies have been predetermined. The code path is
almost static—if it returns the wrong expected result, then something important
might have changed in the production code’s execution path or logic. 
 As we go up the levels, our tests shed more and more stubs and mocks and start
using more and more real dependencies, such as databases, networks, configura-
tion, and more. This, in turn, means more moving parts that we have less control
over and that might change our execution path, return unexpected values, or fail to
execute at all. 
 At the highest level, there are no fake dependencies. Everything our tests rely on
is real, including any third-party services, security and network layers, and configura-
tion. These types of tests usually require us to set up an environment that is as close
to a production scenario as possible, if they’re not running right on the production
environments.
 The higher up we go in the test diagram, we should get higher confidence that our
code works, unless we don’t trust the tests’ results. Unfortunately, the higher up we go
in the diagram, the more chances there are for our tests to become flaky because of
how many moving parts are involved.
 We might assume that tests at the lowest level shouldn’t have any flakiness issues
because there shouldn’t be any moving parts that cause flakiness. That’s theoretically
true, but in reality people still manage to add moving parts in lower-level tests: using
the current date and time, the machine name, the network, the filesystem, and more
can cause a test to be flaky.
 A test fails sometimes without us touching production code. For example:
A test fails every third run.
A test fails once every unknown number of times.
A test fails when various external conditions fail, such as network or database
availability, other APIs not being available, environment configuration, and more.
To add to that salad of pain, each dependency the test uses (network, filesystem,
threads, etc.) usually adds time to the test run. Calls to the network and the database
take time. The same goes for waiting for threads to finish, reading configurations, and
waiting for asynchronous tasks.
 It also takes longer to figure out why a test is failing. Debugging a test or reading
through huge amounts of logs is heartbreakingly time consuming and will drain your
soul slowly into the abyss of “time to update my resume” land.

--- 페이지 191 ---
163
7.5
Dealing with flaky tests
7.5.1
What can you do once you’ve found a flaky test?
It’s important to realize that flaky tests can be costly to an organization. You should
aim to have zero flaky tests as a long-term goal. Here are some ways to reduce the costs
associated with handling flaky tests:
Define—Agree on what “flaky” means to your organization. For example, run
your test suite 10 times without any production code changes, and count all the
tests that were not consistent in their results (i.e., ones that did not fail all 10
times or did not pass all 10 times).
Place any test deemed flaky in a special category or folder of tests that can be
run separately. I recommend removing all flaky tests from the regular delivery
build so they do not create noise, and quarantining them in their own little
pipeline temporarily. Then, go over each of the flaky tests and play my favorite
flaky game, “fix, convert, or kill”:
– Fix—Make the test not flaky by controlling its dependencies, if possible. For
example, if it requires data in the database, insert the data into the database
as part of the test. 
– Convert—Remove flakiness by converting the test into a lower-level test by
removing and controlling one or more of its dependencies. For example,
simulate a network endpoint with a stub instead of using a real one. 
– Kill—Seriously consider whether the value the test brings is enough to con-
tinue to run it and pay the maintenance costs it creates. Sometimes old flaky
tests are better off dead and buried. Sometimes they are already covered by
newer, better tests, and the old tests are pure technical debt that we can get
rid of. Sadly, many engineering managers are reluctant to remove these old
tests because of the sunken cost fallacy—there was so much effort put into
them that it would be a waste to delete them. However, at this point, it might
cost you more to keep the test than to delete it, so I recommend seriously
considering this option for many of your flaky tests. 
7.5.2
Preventing flakiness in higher-level tests
If you’re interested in preventing flakiness in higher-level tests, your best bet is to
make sure that your tests are repeatable on any environment after any deployment.
That could involve the following:
Roll back any changes your tests have made to external shared resources.
Do not depend on other tests changing external state.
Gain some control over external systems and dependencies by ensuring you
have the ability to recreate them at will (do an internet search on “infrastruc-
ture as code”), creating dummies of them that you can control, or creating spe-
cial test accounts on them and pray that they stay safe.

--- 페이지 192 ---
164
CHAPTER 7
Trustworthy tests
On this last point, controlling external dependencies can be difficult or impossible
when using external systems managed by other companies. When that’s true, it’s
worth considering these options:
Remove some of the higher-level tests if some low-level tests already cover those
scenarios.
Convert some of the higher-level tests to a set of lower-level tests.
If you’re writing new tests, consider a pipeline-friendly testing strategy with test
recipes (such as the one I’ll explain in chapter 10).
Summary
If you don’t trust a test when it’s failing, you might ignore a real bug, and if you
don’t trust a test when it’s passing, you’ll end up doing lots of manual debug-
ging and testing. Both of these outcomes are supposed to be reduced by having
good tests, but if we don’t reduce them, and we spend all this time writing tests
that we don’t trust, what’s the point in writing them in the first place? 
Tests might fail for multiple reasons: a real bug found in production code, a bug
in the test resulting in a false failure, a test being out of date due to a change in
functionality, a test conflicting with another test, or test flakiness. Only the first
reason is a valid one. All the others tell us the test shouldn’t be trusted.
Avoid complexity in tests, such as creating dynamic expected values or duplicat-
ing logic from the underlying production code. Such complexity increases the
chances of introducing bugs in tests and the time it takes to understand them.
If a test doesn’t have any asserts, you can’t understand what's it’s doing, it runs
alongside flaky tests (even if this test itself isn’t flaky), it verifies multiple exit
points, or it keeps changing, it can’t be fully trusted.
Flaky tests are tests that fail unpredictably. The higher the level of the test, the
more real dependencies it uses, which gives us confidence in the overall sys-
tem’s correctness but results in more flakiness. To better identify flaky tests, put
them in a special category or folder that can be run separately.
To reduce test flakiness, either fix the tests, convert flaky higher-level tests into
less flaky lower-level ones, or delete them.

# 2.1.5 Executing Jest (pp.31-33)

---
**Page 31**

31
2.1
Introducing Jest
test('hello jest', () => {
    expect('hello').toEqual('goodbye');
});
We haven’t used describe and it yet, but we’ll get to them soon. 
2.1.5
Executing Jest
To run this test, we need to be able to execute Jest. For Jest to be recognized from the
command line, we need to do either of the following:
Install Jest globally on the machine by running npm install jest -g.
Use npx to execute Jest from the node_modules directory by typing jest in the
root of the ch2 folder.
If all the stars lined up correctly, you should see the results of the Jest test run and a fail-
ure. Your first failure. Yay! Figure 2.1 shows the output on my terminal when I run the
command. It’s pretty cool to see such lovely, colorful (if you’re reading the e-book), use-
ful output from a test tool. It looks even cooler if your terminal is in dark mode.
 Let’s take a closer look at the details. Figure 2.2 shows the same output, but with
numbers to follow along. Let’s see how many pieces of information are presented
here:
b
A quick list of all the failing tests (with names) with nice red Xs next to them
c
A detailed report on the expectation that failed (aka our assertion)
d
The exact difference between the actual value and expected value
e
The type of comparison that was executed
f
The code for the test
g
The exact line (visually) where the test failed
h
A report of how many tests ran, failed, and passed
i
The time it took
j
The number of snapshots (not relevant to our discussion)
Test file locations
There are two main patterns I see for placing test files: Some people prefer to place
the test files directly next to the files or modules being tested. Others prefer to place
all the files under a test directory. Which approach you choose doesn’t really matter;
just be consistent in your choice throughout a project, so it’s easy to know where to
find the tests for a specific item. 
I find that placing tests in a test folder allows me to also put helper files under the
test folder close to the tests. As for easily navigating between tests and the code
under test, there are plugins for most IDEs today that allow you to navigate between
code and its tests with a keyboard shortcut.
Listing 2.1
Hello Jest


---
**Page 32**

32
CHAPTER 2
A first unit test
Figure 2.1
Terminal output from Jest
1
2
3
4
5
6
7
8
9
Figure 2.2
Annotated terminal output from Jest


---
**Page 33**

33
2.2
The library, the assert, the runner, and the reporter
Imagine trying to write all this reporting functionality yourself. It’s possible, but who’s
got the time and the inclination? Plus, you’d have to take care of any bugs in the
reporting mechanism. 
 If we change goodbye to hello in the test, we can see what happens when the test
passes (figure 2.3). Nice and green, as all things should be (again, in the digital ver-
sion—otherwise it’s nice and grey).
You might note that it takes 1.5 seconds to run this single Hello World test. If we used
the command jest --watch instead, we could have Jest monitor filesystem activity in
our folder and automatically run tests for files that have changed without re-initializ-
ing itself every time. This can save a considerable amount of time, and it really helps
with the whole notion of continuous testing. Set a terminal in the other window of your
workstation with jest --watch on it, and you can keep coding and getting fast feed-
back on issues you might be creating. That’s a good way to get into the flow of things.
 Jest also supports async-style testing and callbacks. I’ll touch on these when we get
to those topics later in the book, but if you’d like to learn more about this style now,
head over to the Jest documentation on the subject: https://jestjs.io/docs/en/asyn-
chronous.
2.2
The library, the assert, the runner, and the reporter
Jest has acted in several capacities for us:
It acted as a test library to use when writing the test.
It acted as an assertion library for asserting inside the test (expect).
It acted as the test runner.
It acted as the test reporter for the test run.
Jest also provides isolation facilities to create mocks, stubs, and spies, though we
haven’t seen that yet. We’ll touch on these ideas in later chapters. 
 Other than isolation facilities, it’s very common in other languages for a test frame-
work to fill all the roles I just mentioned—library, assertions, test runner, and test
reporter—but the JavaScript world seems a bit more fragmented. Many other test
frameworks provide only some of these facilities. Perhaps this is because the mantra of
Figure 2.3
Jest terminal 
output for a passing test 



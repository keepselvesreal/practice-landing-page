# 2.1.4 Creating a test file (pp.30-31)

---
**Page 30**

30
CHAPTER 2
A first unit test
anything but the default package.json file. If you’d like to learn more about the Jest
configuration options, refer to https://jestjs.io/docs/en/configuration.
2.1.3
Installing Jest
Next, we’ll install Jest. To install Jest as a dev dependency (which means it does not get
distributed to production) we can use this command:
npm install --save-dev jest
//or
yarn add jest –dev
This will create a new jest.js file under our [root folder]/node_modules/bin. We can
then execute Jest using the npx jest command.
 We can also install Jest globally on the local machine (I recommend doing this on
top of the save-dev installation) by executing this command:
npm install -g jest
This will give us the freedom to execute the jest command directly from the com-
mand line in any folder that has tests, without going through npm to execute it.
 In real projects, it is common to use npm commands to run tests instead of using
the global jest. I’ll show how this is done in the next few pages. 
2.1.4
Creating a test file
Jest has a couple of default ways to find test files: 
If there’s a __tests__ folder, it loads all the files in it as test files, regardless of
their naming conventions. 
It tries to find any file that ends with *.spec.js or *.test.js, in any folder under the
root folder of your project, recursively. 
We’ll use the first variation, but we’ll also name our files with either *test.js or *.spec.js
to make things a bit more consistent in case we want to move them around later (and
stop using the __tests_ folder altogether). 
 You can also configure Jest to your heart’s content, specifying how to find which
files where, with a jest.config.js file or through package.json. You can look up the Jest
docs at https://jestjs.io/docs/en/configuration to find all the gory details.
 The next step is to create a special folder under our ch2 folder called __tests__.
Under this folder, create a file that ends with either test.js or spec.js—my-compo-
nent.test.js, for example. Which suffix you choose is up to you—it’s about your own
style. I’ll use them interchangeably in this book because I think of “test” as the sim-
plest version of “spec,” so I use it when showing very simple things.
 We don’t need require() at the top of the file to start using Jest. It automatically
imports global functions for us to use. The main functions you should be interested
in include test, describe, it, and expect. Listing 2.1 shows what a simple test might
look like.


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



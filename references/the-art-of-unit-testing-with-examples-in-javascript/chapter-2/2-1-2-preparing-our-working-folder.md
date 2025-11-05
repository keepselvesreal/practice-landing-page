# 2.1.2 Preparing our working folder (pp.29-30)

---
**Page 29**

29
2.1
Introducing Jest
2.1
Introducing Jest
Jest is an open source test framework created by Facebook. It’s easy to use, easy to
remember, and has lots of great features. Jest was originally created for testing front-
end React components in JavaScript. These days it’s widely used in many parts of the
industry for both backend and frontend project testing. It supports two major flavors
of test syntax (one that uses the word test and another that’s based on the Jasmin syn-
tax, a framework that has inspired many of Jest’s features). We’ll try both of them to
see which one we like better. 
 Aside from Jest, there are many other testing frameworks in JavaScript, pretty
much all open source as well. There are some differences between them in style and
APIs, but for the purposes of this book, that shouldn’t matter too much. 
2.1.1
Preparing our environment
Make sure you have Node.js installed locally. You can follow the instructions at
https://nodejs.org/en/download/ to get it up and running on your machine. The
site will provide you with the option of either a long-term support (LTS) release or a
current release. The LTS release is geared toward enterprises, whereas the current
release has more frequent updates. Either will work for the purposes of this book.
 Make sure that the node package manager (npm) is installed on your machine. It
is included with Node.js, so run the command npm -v on the command line, and if you
see a version of 6.10.2 or higher, you should be good to go. If not, make sure Node.js
is installed.
2.1.2
Preparing our working folder
To get started with Jest, let’s create a new empty folder named “ch2” and initialize it
with a package manager of your choice. I’ll use npm, since I have to choose one. Yarn
is an alternative package manager. It shouldn’t matter, for the purposes of this book,
which one you use. 
 Jest expects either a jest.config.js or a package.json file. We’re going with the latter,
and npm init will generate one for us:
mkdir ch2
cd ch2
npm init --yes
//or
yarn init –yes 
git init
I’m also initializing Git in this folder. This would be recommended anyway, to track
changes, but for Jest this file is used under the covers to track changes to files and run
specific tests. It makes Jest’s life easier. 
 By default, Jest will look for its configuration either in the package.json file that is
created by this command or in a special jest.config.js file. For now, we won’t need


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



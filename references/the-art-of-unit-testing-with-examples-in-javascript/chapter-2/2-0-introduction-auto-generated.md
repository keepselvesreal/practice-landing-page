# 2.0 Introduction [auto-generated] (pp.28-29)

---
**Page 28**

28
A first unit test
When I first started writing unit tests with a real unit testing framework, there was
little documentation, and the frameworks I worked with didn’t have proper exam-
ples. (I was mostly coding in VB 5 and 6 at the time.) It was a challenge learning to
work with them, and I started out writing rather poor tests. Fortunately, times have
changed. In JavaScript, and in practically any language out there, there’s a wide
range of choices and plenty of documentation and support from the community
for trying out these bundles of helpfulness.
 In the previous chapter, we wrote a very simple home-grown test framework.
In this chapter, we’ll take a look at Jest, which will be our framework of choice for
this book. 
This chapter covers
Writing your first test with Jest
Test structure and naming conventions
Working with the assertion library
Refactoring tests and reducing repetitive code


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



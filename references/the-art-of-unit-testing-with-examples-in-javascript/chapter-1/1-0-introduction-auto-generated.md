# 1.0 Introduction [auto-generated] (pp.3-5)

---
**Page 3**

3
The basics of unit testing
Manual tests suck. You write your code, you run it in the debugger, you hit all the
right keys in your app to get things just right, and then you repeat all this the next
time you write new code. And you have to remember to check all the other code
that might have been affected by the new code. More manual work. Great.
 Doing tests and regression testing completely manually, repeating the same
actions again and again like a monkey, is error prone and time consuming, and
people seem to hate doing that as much as anything can be hated in software devel-
opment. These problems are alleviated by tooling and our decision to use it for
good, by writing automated tests that save us precious time and debugging pain.
Integration and unit testing frameworks help developers write tests more quickly
with a set of known APIs, execute those tests automatically, and review the results of
This chapter covers
Identifying entry points and exit points
The definitions of unit test and unit of work
The difference between unit testing and 
integration testing
A simple example of unit testing
Understanding test-driven development


---
**Page 4**

4
CHAPTER 1
The basics of unit testing
those tests easily. And they never forget! I’m assuming you’re reading this book
because either you feel the same way, or because someone forced you to read it, and
that someone feels the same way. Or maybe that someone was forced to force you into
reading this book. Doesn’t matter. If you believe repetitive manual testing is awesome,
this book will be very difficult to read. The assumption is that you want to learn how to
write good unit tests. 
 This book also assumes that you know how to write code using JavaScript or Type-
Script, using at least ECMAScript 6 (ES6) features, and that you are comfortable with
node package manager (npm). Another assumption is that you are familiar with Git
source control. If you’ve seen github.com before and you know how to clone a reposi-
tory from there, you are good to go.
 Although all the book’s code listings are in JavaScript and TypeScript, you don’t
have to be a JavaScript programmer to read this book. The previous editions of this
book were in C#, and I’ve found that about 80% of the patterns there have transferred
over quite easily. You should be able to read this book even if you come from Java,
.NET, Python, Ruby, or other languages. The patterns are just patterns. The language
is used to demonstrate those patterns, but they are not language-specific.
JavaScript vs. TypeScript in this book
This book contains both vanilla JavaScript and TypeScript examples throughout. I
take full responsibility for creating such a Tower of Babel (no pun intended), but I prom-
ise, there’s a good reason: this book is dealing with three programming paradigms in
JavaScript: procedural, functional, and object-oriented design. 
I use regular JavaScript for the samples dealing with procedural and functional
designs. I use TypeScript for the object-oriented examples, because it provides the
structure needed to express these ideas. 
In previous editions of this book, when I was working in C#, this wasn’t an issue.
When moving to JavaScript, which supports these multiple paradigms, using Type-
Script makes sense.
Why not just use TypeScript for all the paradigms, you ask? Both to show that Type-
Script is not needed to write unit tests and that the concepts of unit testing do not
depend on one language or another, or on any type of compiler or linter, to work.
This means that if you’re into functional programming, some of the examples in this
book will make sense, and others will seem like they are overcomplicated or need-
lessly verbose. Feel free to focus only on the functional examples.
If you’re into object-oriented programming or are coming from a C#/Java background,
you’ll find that some of the non-object-oriented examples are simplistic and don’t rep-
resent your day-to-day work in your own projects. Fear not, there will be plenty of sec-
tions relating to the object-oriented style. 


---
**Page 5**

5
1.2
Defining unit testing, step by step
1.1
The first step
There’s always a first step: the first time you wrote a program, the first time you failed
a project, and the first time you succeeded in what you were trying to accomplish. You
never forget your first time, and I hope you won’t forget your first tests. 
 You may have come across tests in some form. Some of your favorite open source
projects come with bundled “test” folders—you have them in your own projects at
work. You might have already written a few tests yourself, and you may even remember
them as being bad, awkward, slow, or unmaintainable. Even worse, you might have felt
they were useless and a waste of time. (Many people sadly do.) Or you may have had a
great first experience with unit tests, and you’re reading this book to see what more
you might be missing. 
 This chapter will analyze the “classic” definition of a unit test and compare it to the
concept of integration testing. This distinction is confusing to many, but it’s very
important to learn, because, as you’ll learn later in the book, separating unit tests
from other types of tests can be crucial to having high confidence in your tests when
they fail or pass.
 We’ll also discuss the pros and cons of unit testing versus integration testing, and
we’ll develop a better definition of what might be a “good” unit test. We’ll finish with a
look at test-driven development (TDD), because it’s often associated with unit testing
but is a separate skill that I highly recommend giving a chance (it’s not the main topic
of this book, though). Throughout this chapter, I’ll also touch on concepts that are
explained more thoroughly elsewhere in the book.
 First, let’s define what a unit test should be.
1.2
Defining unit testing, step by step
Unit testing isn’t a new concept in software development. It’s been floating around
since the early days of the Smalltalk programming language in the 1970s, and it
proves itself time and time again as one of the best ways a developer can improve code
quality while gaining a deeper understanding of the functional requirements of a
module, class, or function. Kent Beck introduced the concept of unit testing in Small-
talk, and it has carried on into many other programming languages, making unit test-
ing an extremely useful practice. 
 To see what we don’t want to use as our definition of unit testing, let’s look to Wiki-
pedia as a starting point. I’ll use its definition with reservations, because, in my opin-
ion, there are many important parts missing, but it is largely accepted by many for lack
of other good definitions. Our definition will slowly evolve throughout this chapter,
with the final definition appearing in section 1.9. 
Unit tests are typically automated tests written and run by software developers to ensure
that a section of an application (known as the “unit”) meets its design and behaves as
intended. In procedural programming, a unit could be an entire module, but it is more
commonly an individual function or procedure. In object-oriented programming, a unit



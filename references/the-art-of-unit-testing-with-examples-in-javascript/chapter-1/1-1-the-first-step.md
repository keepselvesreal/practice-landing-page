# 1.1 The first step (pp.5-5)

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



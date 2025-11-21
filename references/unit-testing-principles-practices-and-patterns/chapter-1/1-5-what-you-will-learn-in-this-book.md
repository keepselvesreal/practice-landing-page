# 1.5 What you will learn in this book (pp.17-18)

---
**Page 17**

17
What you will learn in this book
efforts on that domain model exclusively. We talk about all this in detail in part 2 of
the book. 
1.4.3
It provides maximum value with minimum maintenance costs
The most difficult part of unit testing is achieving maximum value with minimum
maintenance costs. That’s the main focus of this book.
 It’s not enough to incorporate tests into a build system, and it’s not enough to
maintain high test coverage of the domain model. It’s also crucial to keep in the suite
only the tests whose value exceeds their upkeep costs by a good margin.
 This last attribute can be divided in two:
Recognizing a valuable test (and, by extension, a test of low value)
Writing a valuable test
Although these skills may seem similar, they’re different by nature. To recognize a test
of high value, you need a frame of reference. On the other hand, writing a valuable
test requires you to also know code design techniques. Unit tests and the underlying
code are highly intertwined, and it’s impossible to create valuable tests without put-
ting significant effort into the code base they cover.
 You can view it as the difference between recognizing a good song and being able
to compose one. The amount of effort required to become a composer is asymmetri-
cally larger than the effort required to differentiate between good and bad music. The
same is true for unit tests. Writing a new test requires more effort than examining an
existing one, mostly because you don’t write tests in a vacuum: you have to take into
account the underlying code. And so although I focus on unit tests, I also devote a sig-
nificant portion of this book to discussing code design. 
1.5
What you will learn in this book
This book teaches a frame of reference that you can use to analyze any test in your test
suite. This frame of reference is foundational. After learning it, you’ll be able to look
at many of your tests in a new light and see which of them contribute to the project
and which must be refactored or gotten rid of altogether.
 After setting this stage (chapter 4), the book analyzes the existing unit testing tech-
niques and practices (chapters 4–6, and part of 7). It doesn’t matter whether you’re
familiar with those techniques and practices. If you are familiar with them, you’ll see
them from a new angle. Most likely, you already get them at the intuitive level. This
book can help you articulate why the techniques and best practices you’ve been using
all along are so helpful.
 Don’t underestimate this skill. The ability to clearly communicate your ideas to col-
leagues is priceless. A software developer—even a great one—rarely gets full credit for
a design decision if they can’t explain why, exactly, that decision was made. This book
can help you transform your knowledge from the realm of the unconscious to some-
thing you are able to talk about with anyone.


---
**Page 18**

18
CHAPTER 1
The goal of unit testing
 If you don’t have much experience with unit testing techniques and best practices,
you’ll learn a lot. In addition to the frame of reference that you can use to analyze any
test in a test suite, the book teaches
How to refactor the test suite along with the production code it covers
How to apply different styles of unit testing
Using integration tests to verify the behavior of the system as a whole
Identifying and avoiding anti-patterns in unit tests
In addition to unit tests, this book covers the entire topic of automated testing, so
you’ll also learn about integration and end-to-end tests.
 I use C# and .NET in my code samples, but you don’t have to be a C# professional
to read this book; C# is just the language that I happen to work with the most. All
the concepts I talk about are non-language-specific and can be applied to any other
object-oriented language, such as Java or C++.
Summary
Code tends to deteriorate. Each time you change something in a code base, the
amount of disorder in it, or entropy, increases. Without proper care, such as
constant cleaning and refactoring, the system becomes increasingly complex
and disorganized. Tests help overturn this tendency. They act as a safety net— a
tool that provides insurance against the vast majority of regressions.
It’s important to write unit tests. It’s equally important to write good unit tests.
The end result for projects with bad tests or no tests is the same: either stagna-
tion or a lot of regressions with every new release.
The goal of unit testing is to enable sustainable growth of the software project.
A good unit test suite helps avoid the stagnation phase and maintain the devel-
opment pace over time. With such a suite, you’re confident that your changes
won’t lead to regressions. This, in turn, makes it easier to refactor the code or
add new features.
All tests are not created equal. Each test has a cost and a benefit component,
and you need to carefully weigh one against the other. Keep only tests of posi-
tive net value in the suite, and get rid of all others. Both the application code
and the test code are liabilities, not assets.
The ability to unit test code is a good litmus test, but it only works in one direc-
tion. It’s a good negative indicator (if you can’t unit test the code, it’s of poor
quality) but a bad positive one (the ability to unit test the code doesn’t guaran-
tee its quality).
Likewise, coverage metrics are a good negative indicator but a bad positive one.
Low coverage numbers are a certain sign of trouble, but a high coverage num-
ber doesn’t automatically mean your test suite is of high quality.
Branch coverage provides better insight into the completeness of the test suite
but still can’t indicate whether the suite is good enough. It doesn’t take into



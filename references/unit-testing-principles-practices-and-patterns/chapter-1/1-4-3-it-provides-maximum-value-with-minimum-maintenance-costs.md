# 1.4.3 It provides maximum value with minimum maintenance costs (pp.17-17)

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



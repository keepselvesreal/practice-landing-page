# 1.4.2 It targets only the most important parts of your code base (pp.16-17)

---
**Page 16**

16
CHAPTER 1
The goal of unit testing
once; that could be quite a large undertaking and require significant upfront effort.
You can perform this evaluation gradually. The point is that there’s no automated
way to see how good your test suite is. You have to apply your personal judgment.
 Let’s look at a broader picture of what makes a test suite successful as a whole.
(We’ll dive into the specifics of differentiating between good and bad tests in chapter 4.)
A successful test suite has the following properties:
It’s integrated into the development cycle.
It targets only the most important parts of your code base.
It provides maximum value with minimum maintenance costs.
1.4.1
It’s integrated into the development cycle
The only point in having automated tests is if you constantly use them. All tests should
be integrated into the development cycle. Ideally, you should execute them on every
code change, even the smallest one. 
1.4.2
It targets only the most important parts of your code base
Just as all tests are not created equal, not all parts of your code base are worth the
same attention in terms of unit testing. The value the tests provide is not only in how
those tests themselves are structured, but also in the code they verify.
 It’s important to direct your unit testing efforts to the most critical parts of the sys-
tem and verify the others only briefly or indirectly. In most applications, the most
important part is the part that contains business logic—the domain model.1 Testing
business logic gives you the best return on your time investment.
 All other parts can be divided into three categories:
Infrastructure code
External services and dependencies, such as the database and third-party systems
Code that glues everything together
Some of these other parts may still need thorough unit testing, though. For example,
the infrastructure code may contain complex and important algorithms, so it would
make sense to cover them with a lot of tests, too. But in general, most of your attention
should be spent on the domain model.
 Some of your tests, such as integration tests, can go beyond the domain model and
verify how the system works as a whole, including the noncritical parts of the code
base. And that’s fine. But the focus should remain on the domain model.
 Note that in order to follow this guideline, you should isolate the domain model
from the non-essential parts of the code base. You have to keep the domain model
separated from all other application concerns so you can focus your unit testing
1 See Domain-Driven Design: Tackling Complexity in the Heart of Software by Eric Evans (Addison-Wesley, 2003).


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



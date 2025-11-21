# 1.2.0 Introduction [auto-generated] (pp.5-7)

---
**Page 5**

5
The goal of unit testing
today. You’ll find a few articles and conference talks online, but I’ve yet to see any
comprehensive material on this topic.
 The situation in books isn’t any better; most of them focus on the basics of unit
testing but don’t go much beyond that. Don’t get me wrong. There’s a lot of value in
such books, especially when you are just starting out with unit testing. However, the
learning doesn’t end with the basics. There’s a next level: not just writing tests, but
doing unit testing in a way that provides you with the best return on your efforts.
When you reach this point, most books pretty much leave you to your own devices to
figure out how to get to that next level.
 This book takes you there. It teaches a precise, scientific definition of the ideal
unit test. You’ll see how this definition can be applied to practical, real-world exam-
ples. My hope is that this book will help you understand why your particular project
may have gone sideways despite having a good number of tests, and how to correct its
course for the better.
 You’ll get the most value out of this book if you work in enterprise application
development, but the core ideas are applicable to any software project.
1.2
The goal of unit testing
Before taking a deep dive into the topic of unit testing, let’s step back and consider
the goal that unit testing helps you to achieve. It’s often said that unit testing practices
lead to a better design. And it’s true: the necessity to write unit tests for a code base
normally leads to a better design. But that’s not the main goal of unit testing; it’s
merely a pleasant side effect.
What is an enterprise application?
An enterprise application is an application that aims at automating or assisting an
organization’s inner processes. It can take many forms, but usually the characteris-
tics of an enterprise software are
High business logic complexity
Long project lifespan
Moderate amounts of data
Low or moderate performance requirements 
The relationship between unit testing and code design
The ability to unit test a piece of code is a nice litmus test, but it only works in one
direction. It’s a good negative indicator—it points out poor-quality code with relatively
high accuracy. If you find that code is hard to unit test, it’s a strong sign that the code
needs improvement. The poor quality usually manifests itself in tight coupling, which
means different pieces of production code are not decoupled from each other
enough, and it’s hard to test them separately.


---
**Page 6**

6
CHAPTER 1
The goal of unit testing
What is the goal of unit testing, then? The goal is to enable sustainable growth of the
software project. The term sustainable is key. It’s quite easy to grow a project, especially
when you start from scratch. It’s much harder to sustain this growth over time.
 Figure 1.1 shows the growth dynamic of a typical project without tests. You start
off quickly because there’s nothing dragging you down. No bad architectural deci-
sions have been made yet, and there isn’t any existing code to worry about. As time
goes by, however, you have to put in more and more hours to make the same amount
of progress you showed at the beginning. Eventually, the development speed slows
down significantly, sometimes even to the point where you can’t make any progress
whatsoever.
This phenomenon of quickly decreasing development speed is also known as software
entropy. Entropy (the amount of disorder in a system) is a mathematical and scientific
concept that can also apply to software systems. (If you’re interested in the math and
science of entropy, look up the second law of thermodynamics.)
 In software, entropy manifests in the form of code that tends to deteriorate. Each
time you change something in a code base, the amount of disorder in it, or entropy,
increases. If left without proper care, such as constant cleaning and refactoring, the
system becomes increasingly complex and disorganized. Fixing one bug introduces
more bugs, and modifying one part of the software breaks several others—it’s like a
(continued)
Unfortunately, the ability to unit test a piece of code is a bad positive indicator. The
fact that you can easily unit test your code base doesn’t necessarily mean it’s of
good quality. The project can be a disaster even when it exhibits a high degree of
decoupling.
Without tests
With tests
Progress
hours
spent
Work
Figure 1.1
The difference in growth 
dynamics between projects with and 
without tests. A project without tests 
has a head start but quickly slows down 
to the point that it’s hard to make any 
progress.


---
**Page 7**

7
The goal of unit testing
domino effect. Eventually, the code base becomes unreliable. And worst of all, it’s
hard to bring it back to stability.
 Tests help overturn this tendency. They act as a safety net—a tool that provides
insurance against a vast majority of regressions. Tests help make sure the existing
functionality works, even after you introduce new features or refactor the code to bet-
ter fit new requirements.
DEFINITION
A regression is when a feature stops working as intended after a cer-
tain event (usually, a code modification). The terms regression and software bug
are synonyms and can be used interchangeably.
The downside here is that tests require initial—sometimes significant—effort. But they
pay for themselves in the long run by helping the project to grow in the later stages.
Software development without the help of tests that constantly verify the code base
simply doesn’t scale.
 Sustainability and scalability are the keys. They allow you to maintain development
speed in the long run.
1.2.1
What makes a good or bad test?
Although unit testing helps maintain project growth, it’s not enough to just write tests.
Badly written tests still result in the same picture.
 As shown in figure 1.2, bad tests do help to slow down code deterioration at the
beginning: the decline in development speed is less prominent compared to the situa-
tion with no tests at all. But nothing really changes in the grand scheme of things. It
might take longer for such a project to enter the stagnation phase, but stagnation is
still inevitable.
Without tests
With good tests
With bad tests
Progress
Work
hours
spent
Figure 1.2
The difference in 
growth dynamics between 
projects with good and bad 
tests. A project with badly 
written tests exhibits the 
properties of a project with 
good tests at the beginning, 
but it eventually falls into 
the stagnation phase.



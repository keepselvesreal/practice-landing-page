# 1.2.3 Focusing on development and then on testing (pp.14-15)

---
**Page 14**

14
CHAPTER 1
Effective and systematic software testing
new unit. Domain testing, boundary testing, and structural testing are the go-to
techniques.
5
Some parts of the system may require the developer to write larger tests (integra-
tion or system tests). To devise larger test cases, the developer uses the same
three techniques—domain testing, boundary testing, and structural testing—
but looking at larger parts of the software system.
6
When the developer has engineered test cases using the various techniques,
they apply automated, intelligent testing tools to look for tests that humans are
not good at spotting. Popular techniques include test case generation, mutation
testing, and static analysis. In this book, we cover mutation testing.
7
Finally, after this rigorous testing, the developer feels comfortable releasing
the feature. 
1.2.2
Effective testing as an iterative process
While the previous description may sound like a sequential/waterfall process, it is
more iterative. A developer may be rigorously testing a class and suddenly notice that
a coding decision they made a few hours ago was not ideal. They then go back and
redesign the code. They may be performing TDD cycles and realize the requirement
is unclear about something. The developer then goes back to the requirement analy-
sis to better grasp the expectations. Quite commonly, while testing, the developer
finds a bug. They go back to the code, fix it, and continue testing. Or the developer
may have implemented only half of the feature, but they feel it would be more pro-
ductive to rigorously test it now than to continue the implementation.
 The development workflow I propose throughout this book is not meant to
restrain you. Feel free to go back and forth between techniques or change the order
in which you apply them. In practice, you have to find what works best for you and
makes you the most productive. 
1.2.3
Focusing on development and then on testing
I find it liberating to focus separately on developing and testing. When I am coding a
feature, I do not want to be distracted by obscure corner cases. If I think of one, I take
notes so I do not forget to test it later. However, I prefer to focus all my energy on the
business rules I am implementing and, at the same time, ensure that the code is easy
for future developers to maintain.
 Once I am finished with the coding decisions, I focus on testing. First I follow the
different techniques as if I were working my way down a systematic checklist. As you
saw in the example with Eleanor, she did not have to think much about what to exer-
cise when the method received a list: she responded as if she had a checklist that said
“null, empty list, one element, many elements.” Only then do I use my creativity and
domain knowledge to exercise other cases I find relevant.


---
**Page 15**

15
Effective software testing for developers
1.2.4
The myth of “correctness by design”
Now that you have a clearer picture of what I mean by effective and systematic soft-
ware testing, let me debunk a myth. There is a perception among software developers
that if you design code in a simple way, it will not have bugs, as if the secret of bug-free
code is simplicity.
 Empirical research in software engineering has repeatedly shown that simple,
non-smelly code is less prone to defects than complex code (see, for example, the
2006 paper by Shatnawi and Li). However, simplicity is far from enough. It is naive
to believe that testing can be fully replaced by simplicity. The same is true for
“correctness by design”: designing your code well does not mean you avoid all pos-
sible bugs.
1.2.5
The cost of testing
You may be thinking that forcing developers to apply rigorous testing may be too
costly. Figure 1.4 shows the many techniques developers have to apply if they follow
the flow I am proposing. It is true: testing software properly is more work than not
doing so. Let me convince you why it is worth it:
The cost of bugs that happen in production often outweighs the cost of preven-
tion (as shown by Boehm and Papaccio, 1988). Think of a popular web shop
and how much it would cost the shop if the payment application goes down for
30 minutes due to a bug that could have been easily prevented via testing.
Teams that produce many bugs tend to waste time in an eternal loop where
developers write bugs, customers (or dedicated QAs) find the bugs, developers
fix the bugs, customers find a different set of bugs, and so on.
Practice is key. Once developers are used to engineering test cases, they can do
it much faster. 
1.2.6
The meaning of effective and systematic
I have been using two words to describe how I expect a developer to test: effectively and
systematically. Being effective means we focus on writing the right tests. Software testing
is all about trade-offs. Testers want to maximize the number of bugs they find while
minimizing the effort required to find the bugs. How do we achieve this? By knowing
what to test.
 All the techniques I present in this book have a clear beginning (what to test) and
a clear end (when to stop). Of course, I do not mean your systems will be bug-free if you
follow these techniques. As a community, we still do not know how to build bug-free
systems. But I can confidently say that the number of bugs will be reduced, hopefully
to tolerable levels.
 Being systematic means that for a given piece of code, any developer should come
up with the same test suite. Testing often happens in an ad hoc manner. Developers
engineer the test cases that come to mind. It is common to see two developers devel-



# 1.2.2 Effective testing as an iterative process (pp.14-14)

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



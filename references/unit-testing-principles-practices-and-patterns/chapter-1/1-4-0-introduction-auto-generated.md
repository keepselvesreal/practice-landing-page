# 1.4.0 Introduction [auto-generated] (pp.15-16)

---
**Page 15**

15
What makes a successful test suite?
You can fall into numerous edge cases, and there’s no way to see if your tests account
for all of them.
 This is not to say that coverage metrics should take into account code paths in
external libraries (they shouldn’t), but rather to show you that you can’t rely on
those metrics to see how good or bad your unit tests are. Coverage metrics can’t
possibly tell whether your tests are exhaustive; nor can they say if you have enough
tests. 
1.3.4
Aiming at a particular coverage number
At this point, I hope you can see that relying on coverage metrics to determine the
quality of your test suite is not enough. It can also lead to dangerous territory if you
start making a specific coverage number a target, be it 100%, 90%, or even a moder-
ate 70%. The best way to view a coverage metric is as an indicator, not a goal in and
of itself.
 Think of a patient in a hospital. Their high temperature might indicate a fever and
is a helpful observation. But the hospital shouldn’t make the proper temperature of
this patient a goal to target by any means necessary. Otherwise, the hospital might end
up with the quick and “efficient” solution of installing an air conditioner next to the
patient and regulating their temperature by adjusting the amount of cold air flowing
onto their skin. Of course, this approach doesn’t make any sense.
 Likewise, targeting a specific coverage number creates a perverse incentive that
goes against the goal of unit testing. Instead of focusing on testing the things that
matter, people start to seek ways to attain this artificial target. Proper unit testing is dif-
ficult enough already. Imposing a mandatory coverage number only distracts develop-
ers from being mindful about what they test, and makes proper unit testing even
harder to achieve.
TIP
It’s good to have a high level of coverage in core parts of your system.
It’s bad to make this high level a requirement. The difference is subtle but
critical.
Let me repeat myself: coverage metrics are a good negative indicator, but a bad posi-
tive one. Low coverage numbers—say, below 60%—are a certain sign of trouble. They
mean there’s a lot of untested code in your code base. But high numbers don’t mean
anything. Thus, measuring the code coverage should be only a first step on the way to
a quality test suite. 
1.4
What makes a successful test suite?
I’ve spent most of this chapter discussing improper ways to measure the quality of a
test suite: using coverage metrics. What about a proper way? How should you mea-
sure your test suite’s quality? The only reliable way is to evaluate each test in the
suite individually, one by one. Of course, you don’t have to evaluate all of them at


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



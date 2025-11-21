# 1.4.1 It’s integrated into the development cycle (pp.16-16)

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



# 1.3.6 Context is king (pp.18-18)

---
**Page 18**

18
CHAPTER 1
Effective and systematic software testing
other files in the system. As a software developer, you may have to watch and learn
from your software system. Data other than the source code may help you prioritize
your testing efforts. 
1.3.5
No matter what testing you do, it will never be perfect or enough
As Dijkstra used to say, “Program testing can be used to show the presence of bugs, but
never to show their absence.” In other words, while we may find more bugs by simply
testing more, our test suites, however large they may be, will never ensure that the soft-
ware system is 100% bug-free. They will only ensure that the cases we test for behave
as expected.
 This is an important principle to understand, as it will help you set your (and your
customers’) expectations. Bugs will still happen, but (hopefully) the money you pay
for testing and prevention will pay off by allowing only the less impactful bugs to go
through. “You cannot test everything” is something we must accept.
NOTE
Although monitoring is not a major topic in this book, I recommend
investing in monitoring systems. Bugs will happen, and you need to be sure
you find them the second they manifest in production. That is why tools such
as the ELK stack (Elasticsearch, Logstash, and Kibana; www.elastic.co) are
becoming so popular. This approach is sometimes called testing in production
(Wilsenach, 2017). 
1.3.6
Context is king
The context plays an important role in how we devise test cases. For example, devising
test cases for a mobile app is very different from devising test cases for a web applica-
tion or software used in a rocket. In other words, testing is context-dependent.
 Most of this book tries to be agnostic about context. The techniques I discuss
(domain testing, structural testing, property-based testing, and so on) can be applied
in any type of software system. Nevertheless, if you are working on a mobile app, I rec-
ommend reading a book dedicated to mobile testing after you read this one. I give
some context-specific tips in chapter 9, where I discuss larger tests. 
1.3.7
Verification is not validation
Finally, note that a software system that works flawlessly but is of no use to its users is
not a good software system. As a reviewer of this book said to me, “Coverage of code is
easy to measure; coverage of requirements is another matter.” Software testers face
this absence-of-errors fallacy when they focus solely on verification and not on validation.
 A popular saying that may help you remember the difference is, “Verification is
about having the system right; validation is about having the right system.” This book
primarily covers verification techniques. In other words, I do not focus on techniques
to, for example, collaborate with customers to understand their real needs; rather, I
present techniques to ensure that, given a specific requirement, the software system
implements it correctly.



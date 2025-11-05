# 1.6 Summary (pp.29-30)

---
**Page 29**

29
Summary
A Unit testing
B Integration testing
C System testing
D Stress testing
1.8
Choosing the level of a test involves a trade-off, because each test level has
advantages and disadvantages. Which one of the following is the main advan-
tage of a test at the system level?
A The interaction with the system is much closer to reality.
B In a continuous integration environment, system tests provide real feed-
back to developers.
C Because system tests are never flaky, they provide developers with more
stable feedback.
D A system test is written by product owners, making it closer to reality.
1.9
What is the main reason the number of recommended system tests in the test-
ing pyramid is smaller than the number of unit tests?
A Unit tests are as good as system tests.
B System tests tend to be slow and are difficult to make deterministic.
C There are no good tools for system tests.
D System tests do not provide developers with enough quality feedback. 
Summary
Testing and test code can guide you through software development. But soft-
ware testing is about finding bugs, and that is what this book is primarily about.
Systematic and effective software testing helps you design test cases that exer-
cise all the corners of your code and (hopefully) leaves no space for unex-
pected behavior.
Although being systematic helps, you can never be certain that a program does
not have bugs.
Exhaustive testing is impossible. The life of a tester involves making trade-offs
about how much testing is needed.
You can test programs on different levels, ranging from testing small methods
to testing entire systems with databases and web services. Each level has advan-
tages and disadvantages.


---
**Page 30**

30
Specification-based
testing
Software requirements are undoubtedly the most valuable artifact of software test-
ing. By requirements, I mean any textual document that describes what a functional-
ity should do. Requirements tell us precisely what the software needs to do and
what it should not do. They describe the intricacies of the business rules that the
software has to implement and we need to validate. Therefore, requirements
should be the first artifact you go for when it comes to testing!
 In this chapter, we explore specification-based testing. These techniques use the
program requirements—such as agile user stories or UML use cases—as testing
input. We will discuss how to use all the information available in a requirement to
systematically derive a set of tests that exercise that requirement extensively.
 Where does specification-based testing fit into the entire testing process? Imag-
ine that a software developer receives a new feature to implement. The developer
writes the implementation code, guided by test-driven development (TDD)
This chapter covers
Creating test cases using specification-based 
testing
Identifying and creating test cases for program 
boundaries



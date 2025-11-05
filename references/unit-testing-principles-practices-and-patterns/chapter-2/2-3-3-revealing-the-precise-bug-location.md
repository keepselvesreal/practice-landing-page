# 2.3.3 Revealing the precise bug location (pp.36-36)

---
**Page 36**

36
CHAPTER 2
What is a unit test?
2.3.3
Revealing the precise bug location
If you introduce a bug to a system with London-style tests, it normally causes only tests
whose SUT contains the bug to fail. However, with the classical approach, tests that
target the clients of the malfunctioning class can also fail. This leads to a ripple effect
where a single bug can cause test failures across the whole system. As a result, it
becomes harder to find the root of the issue. You might need to spend some time
debugging the tests to figure it out.
 It’s a valid concern, but I don’t see it as a big problem. If you run your tests regu-
larly (ideally, after each source code change), then you know what caused the bug—
it’s what you edited last, so it’s not that difficult to find the issue. Also, you don’t have
to look at all the failing tests. Fixing one automatically fixes all the others.
 Furthermore, there’s some value in failures cascading all over the test suite. If a
bug leads to a fault in not only one test but a whole lot of them, it shows that the piece
of code you have just broken is of great value—the entire system depends on it. That’s
useful information to keep in mind when working with the code. 
2.3.4
Other differences between the classical and London schools
Two remaining differences between the classical and London schools are
Their approach to system design with test-driven development (TDD)
The issue of over-specification
The London style of unit testing leads to outside-in TDD, where you start from the
higher-level tests that set expectations for the whole system. By using mocks, you spec-
ify which collaborators the system should communicate with to achieve the expected
result. You then work your way through the graph of classes until you implement every
one of them. Mocks make this design process possible because you can focus on one
Test-driven development
Test-driven development is a software development process that relies on tests to
drive the project development. The process consists of three (some authors specify
four) stages, which you repeat for every test case:
1
Write a failing test to indicate which functionality needs to be added and how
it should behave.
2
Write just enough code to make the test pass. At this stage, the code doesn’t
have to be elegant or clean.
3
Refactor the code. Under the protection of the passing test, you can safely
clean up the code to make it more readable and maintainable.
Good sources on this topic are the two books I recommended earlier: Kent Beck’s
Test-Driven Development: By Example, and Growing Object-Oriented Software, Guided
by Tests by Steve Freeman and Nat Pryce.



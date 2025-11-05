# 9.6 Summary (pp.257-258)

---
**Page 257**

257
Summary
B In web testing, end-to-end testing is more important than unit testing.
C End-to-end testing can be used to verify whether the frontend and back-
end work together well.
D End-to-end tests are, like unit tests, not very realistic.
9.3
Which of the following is true about page objects?
A POs abstract the HTML page to facilitate the engineering of end-to-end
tests.
B POs cannot be used in highly complex web applications.
C By introducing a PO, we no longer need libraries like Selenium.
D POs usually make the test code more complex.
9.4
Which of the following are important recommendations for developers who are
engineering integration and system test suites? Choose all that apply.
A What can be tested via unit testing should be tested via unit testing. Use
integration and system tests for bugs that can only be caught at that level.
B It is fundamental for developers to have a solid infrastructure to write
such tests, as otherwise, they would feel unproductive.
C If something is already covered via unit testing, you should not cover it
(again) via integration testing.
D Too many integration tests may mean your application is badly designed.
Focus on unit tests.
9.5
Which of the following can cause web tests to be flaky (that is, sometimes pass,
sometimes fail)? Choose all that apply.
A AJAX requests that take longer than expected
B The use of LESS and SASS instead of pure CSS
C The database of the web app under test is not being cleaned up after every
test run
D Some components of the web app were unavailable at the time
Summary
Developers benefit from writing larger tests, ranging from testing entire compo-
nents together, to integrating with external parties, to entire systems.
Engineering larger tests is more challenging than writing unit tests, because the
component under test is probably much bigger and more complex than a sin-
gle unit of the system.
All the test case engineering techniques we have discussed—specification-based
testing, boundary testing, structural testing, and property-based testing—apply
to larger tests.
Investing in a good test infrastructure for large tests is a requirement. Without
it, you will spend too much time writing a single test case.


---
**Page 258**

258
Test code quality
You have probably noticed that once test infected, the number of JUnit tests a soft-
ware development team writes and maintains can become significant. In practice,
test code bases grow quickly. Moreover, we have observed that Lehman’s law of evo-
lution, “Code tends to rot, unless one actively works against it” (1980), also applies
to test code. A 2018 literature review by Garousi and Küçük shows that our body of
knowledge about things that can go wrong with test code is already comprehensive.
 As with production code, we must put extra effort into writing high-quality test code
bases so they can be maintained and developed sustainably. In this chapter, I discuss two
opposite perspectives of writing test code. First, we examine what constitutes good
and maintainable test code, and best practices that can help you keep complexity
under control. Then we look at what constitutes problematic test code. We focus on
key test smells that hinder test code comprehension and evolution.
 I have discussed some of this material informally in previous chapters. This
chapter consolidates that knowledge.
This chapter covers
Principles and best practices of good and 
maintainable test code
Avoiding test smells that hinder the 
comprehension and evolution of test code



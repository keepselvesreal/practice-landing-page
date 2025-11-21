# 4.1.1 The first pillar: Protection against regressions (pp.68-69)

---
**Page 68**

68
CHAPTER 4
The four pillars of a good unit test
As we discussed in chapter 1, recognizing a valuable test and writing a valuable test are two
separate skills. The latter skill requires the former one, though; so, in this chapter, I’ll
show how to recognize a valuable test. You’ll see a universal frame of reference with
which you can analyze any test in the suite. We’ll then use this frame of reference to
go over some popular unit testing concepts: the Test Pyramid and black-box versus
white-box testing.
 Buckle up: we are starting out.
4.1
Diving into the four pillars of a good unit test
A good unit test has the following four attributes:
Protection against regressions
Resistance to refactoring
Fast feedback
Maintainability
These four attributes are foundational. You can use them to analyze any automated
test, be it unit, integration, or end-to-end. Every such test exhibits some degree of
each attribute. In this section, I define the first two attributes; and in section 4.2, I
describe the intrinsic connection between them.
4.1.1
The first pillar: Protection against regressions
Let’s start with the first attribute of a good unit test: protection against regressions. As you
know from chapter 1, a regression is a software bug. It’s when a feature stops working as
intended after some code modification, usually after you roll out new functionality.
 Such regressions are annoying (to say the least), but that’s not the worst part about
them. The worst part is that the more features you develop, the more chances there are
that you’ll break one of those features with a new release. An unfortunate fact of pro-
gramming life is that code is not an asset, it’s a liability. The larger the code base, the more
exposure it has to potential bugs. That’s why it’s crucial to develop a good protection
against regressions. Without such protection, you won’t be able to sustain the project
growth in a long run—you’ll be buried under an ever-increasing number of bugs.
 To evaluate how well a test scores on the metric of protecting against regressions,
you need to take into account the following:
The amount of code that is executed during the test
The complexity of that code
The code’s domain significance
Generally, the larger the amount of code that gets executed, the higher the chance
that the test will reveal a regression. Of course, assuming that this test has a relevant
set of assertions, you don’t want to merely execute the code. While it helps to know
that this code runs without throwing exceptions, you also need to validate the out-
come it produces.


---
**Page 69**

69
Diving into the four pillars of a good unit test
 Note that it’s not only the amount of code that matters, but also its complexity and
domain significance. Code that represents complex business logic is more important
than boilerplate code—bugs in business-critical functionality are the most damaging.
 On the other hand, it’s rarely worthwhile to test trivial code. Such code is short and
doesn’t contain a substantial amount of business logic. Tests that cover trivial code
don’t have much of a chance of finding a regression error, because there’s not a lot of
room for a mistake. An example of trivial code is a single-line property like this:
public class User
{
public string Name { get; set; }
}
Furthermore, in addition to your code, the code you didn’t write also counts: for
example, libraries, frameworks, and any external systems used in the project. That
code influences the working of your software almost as much as your own code. For
the best protection, the test must include those libraries, frameworks, and external sys-
tems in the testing scope, in order to check that the assumptions your software makes
about these dependencies are correct.
TIP
To maximize the metric of protection against regressions, the test needs
to aim at exercising as much code as possible. 
4.1.2
The second pillar: Resistance to refactoring
The second attribute of a good unit test is resistance to refactoring—the degree to which
a test can sustain a refactoring of the underlying application code without turning red
(failing).
DEFINITION
Refactoring means changing existing code without modifying its
observable behavior. The intention is usually to improve the code’s nonfunc-
tional characteristics: increase readability and reduce complexity. Some exam-
ples of refactoring are renaming a method and extracting a piece of code into
a new class.
Picture this situation. You developed a new feature, and everything works great. The
feature itself is doing its job, and all the tests are passing. Now you decide to clean up
the code. You do some refactoring here, a little bit of modification there, and every-
thing looks even better than before. Except one thing—the tests are failing. You look
more closely to see exactly what you broke with the refactoring, but it turns out that
you didn’t break anything. The feature works perfectly, just as before. The problem is
that the tests are written in such a way that they turn red with any modification of the
underlying code. And they do that regardless of whether you actually break the func-
tionality itself.
 This situation is called a false positive. A false positive is a false alarm. It’s a result
indicating that the test fails, although in reality, the functionality it covers works as



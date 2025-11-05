# 4.4.1 Is it possible to create an ideal test? (pp.81-81)

---
**Page 81**

81
In search of an ideal test
4.4.1
Is it possible to create an ideal test?
An ideal test is a test that scores the maximum in all four attributes. If you take the
minimum and maximum values as 0 and 1 for each of the attributes, an ideal test must
get 1 in all of them.
 Unfortunately, it’s impossible to create such an ideal test. The reason is that the
first three attributes—protection against regressions, resistance to refactoring, and fast feedback—
are mutually exclusive. It’s impossible to maximize them all: you have to sacrifice one
of the three in order to max out the remaining two.
 Moreover, because of the multiplication principle (see the calculation of the value
estimate in the previous section), it’s even trickier to keep the balance. You can’t just
forgo one of the attributes in order to focus on the others. As I mentioned previously,
a test that scores zero in one of the four categories is worthless. Therefore, you have to
maximize these attributes in such a way that none of them is diminished too much.
Let’s look at some examples of tests that aim at maximizing two out of three attributes
at the expense of the third and, as a result, have a value that’s close to zero. 
4.4.2
Extreme case #1: End-to-end tests
The first example is end-to-end tests. As you may remember from chapter 2, end-to-end
tests look at the system from the end user’s perspective. They normally go through all of
the system’s components, including the UI, database, and external applications.
 Since end-to-end tests exercise a lot of code, they provide the best protection
against regressions. In fact, of all types of tests, end-to-end tests exercise the most
code—both your code and the code you didn’t write but use in the project, such as
external libraries, frameworks, and third-party applications.
 End-to-end tests are also immune to false positives and thus have a good resistance
to refactoring. A refactoring, if done correctly, doesn’t change the system’s observable
behavior and therefore doesn’t affect the end-to-end tests. That’s another advantage
of such tests: they don’t impose any particular implementation. The only thing end-to-
end tests look at is how a feature behaves from the end user’s point of view. They are
as removed from implementation details as tests could possibly be.
 However, despite these benefits, end-to-end tests have a major drawback: they are
slow. Any system that relies solely on such tests would have a hard time getting rapid
feedback. And that is a deal-breaker for many development teams. This is why it’s
pretty much impossible to cover your code base with only end-to-end tests.
 Figure 4.6 shows where end-to-end tests stand with regard to the first three unit
testing metrics. Such tests provide great protection against both regression errors and
false positives, but lack speed. 



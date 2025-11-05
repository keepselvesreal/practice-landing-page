# 4.5.2 Choosing between black-box and white-box testing (pp.89-90)

---
**Page 89**

89
Exploring well-known test automation concepts
which you don’t ever want to see any bugs—and only when you can’t get the same
degree of protection with unit or integration tests. The use of end-to-end tests for any-
thing else shouldn’t pass your minimum required value threshold. Unit tests are usu-
ally more balanced, and hence you normally have many more of them.
 There are exceptions to the Test Pyramid. For example, if all your application does
is basic create, read, update, and delete (CRUD) operations with very few business
rules or any other complexity, your test “pyramid” will most likely look like a rectangle
with an equal number of unit and integration tests and no end-to-end tests.
 Unit tests are less useful in a setting without algorithmic or business complexity—
they quickly descend into trivial tests. At the same time, integration tests retain their
value—it’s still important to verify how code, however simple it is, works in integration
with other subsystems, such as the database. As a result, you may end up with fewer
unit tests and more integration tests. In the most trivial examples, the number of inte-
gration tests may even be greater than the number of unit tests.
 Another exception to the Test Pyramid is an API that reaches out to a single out-of-
process dependency—say, a database. Having more end-to-end tests may be a viable
option for such an application. Since there’s no user interface, end-to-end tests will
run reasonably fast. The maintenance costs won’t be too high, either, because you
only work with the single external dependency, the database. Basically, end-to-end
tests are indistinguishable from integration tests in this environment. The only thing
that differs is the entry point: end-to-end tests require the application to be hosted
somewhere to fully emulate the end user, while integration tests normally host the
application in the same process. We’ll get back to the Test Pyramid in chapter 8, when
we’ll be talking about integration testing. 
4.5.2
Choosing between black-box and white-box testing
The other well-known test automation concept is black-box versus white-box testing.
In this section, I show when to use each of the two approaches:
Black-box testing is a method of software testing that examines the functionality
of a system without knowing its internal structure. Such testing is normally built
around specifications and requirements: what the application is supposed to do,
rather than how it does it.
White-box testing is the opposite of that. It’s a method of testing that verifies the
application’s inner workings. The tests are derived from the source code, not
requirements or specifications.
There are pros and cons to both of these methods. White-box testing tends to be more
thorough. By analyzing the source code, you can uncover a lot of errors that you may
miss when relying solely on external specifications. On the other hand, tests resulting
from white-box testing are often brittle, as they tend to tightly couple to the specific
implementation of the code under test. Such tests produce many false positives and
thus fall short on the metric of resistance to refactoring. They also often can’t be traced


---
**Page 90**

90
CHAPTER 4
The four pillars of a good unit test
back to a behavior that is meaningful to a business person, which is a strong sign that
these tests are fragile and don’t add much value. Black-box testing provides the oppo-
site set of pros and cons (table 4.1).
As you may remember from section 4.4.5, you can’t compromise on resistance to refac-
toring: a test either possesses resistance to refactoring or it doesn’t. Therefore, choose black-
box testing over white-box testing by default. Make all tests—be they unit, integration, or
end-to-end—view the system as a black box and verify behavior meaningful to the
problem domain. If you can’t trace a test back to a business requirement, it’s an indi-
cation of the test’s brittleness. Either restructure or delete this test; don’t let it into the
suite as-is. The only exception is when the test covers utility code with high algorith-
mic complexity (more on this in chapter 7).
 Note that even though black-box testing is preferable when writing tests, you can
still use the white-box method when analyzing the tests. Use code coverage tools to see which
code branches are not exercised, but then turn around and test them as if you know nothing about
the code’s internal structure. Such a combination of the white-box and black-box meth-
ods works best. 
Summary
A good unit test has four foundational attributes that you can use to analyze any
automated test, whether unit, integration, or end-to-end:
– Protection against regressions
– Resistance to refactoring
– Fast feedback
– Maintainability
Protection against regressions is a measure of how good the test is at indicating the
presence of bugs (regressions). The more code the test executes (both your
code and the code of libraries and frameworks used in the project), the higher
the chance this test will reveal a bug.
Resistance to refactoring is the degree to which a test can sustain application code
refactoring without producing a false positive.
A false positive is a false alarm—a result indicating that the test fails, whereas
the functionality it covers works as intended. False positives can have a devastat-
ing effect on the test suite:
– They dilute your ability and willingness to react to problems in code, because
you get accustomed to false alarms and stop paying attention to them.
Table 4.1
The pros and cons of white-box and black-box testing
Protection against regressions
Resistance to refactoring
White-box testing
Good
Bad
Black-box testing
Bad
Good



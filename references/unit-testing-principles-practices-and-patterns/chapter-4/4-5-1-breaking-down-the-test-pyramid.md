# 4.5.1 Breaking down the Test Pyramid (pp.87-89)

---
**Page 87**

87
Exploring well-known test automation concepts
4.5
Exploring well-known test automation concepts
The four attributes of a good unit test shown earlier are foundational. All existing,
well-known test automation concepts can be traced back to these four attributes. In
this section, we’ll look at two such concepts: the Test Pyramid and white-box versus
black-box testing.
4.5.1
Breaking down the Test Pyramid
The Test Pyramid is a concept that advocates for a certain ratio of different types of
tests in the test suite (figure 4.11):
Unit tests
Integration tests
End-to-end tests
The Test Pyramid is often represented visually as a pyramid with those three types of
tests in it. The width of the pyramid layers refers to the prevalence of a particular type
The choice, then, also boils down to a trade-off between consistency and availability.
In some parts of the system, it’s preferable to concede a little consistency to gain
more availability. For example, when displaying a product catalog, it’s generally fine
if some parts of the catalog are out of date. Availability is of higher priority in this sce-
nario. On the other hand, when updating a product description, consistency is more
important than availability: network nodes must have a consensus on what the most
recent version of that description is, in order to avoid merge conflicts. 
End-
to-end
Integration
tests
Unit tests
Test count
Emulating
user
Figure 4.11
The Test Pyramid advocates for a certain ratio of unit, 
integration, and end-to-end tests.


---
**Page 88**

88
CHAPTER 4
The four pillars of a good unit test
of test in the suite. The wider the layer, the greater the test count. The height of the
layer is a measure of how close these tests are to emulating the end user’s behavior.
End-to-end tests are at the top—they are the closest to imitating the user experience.
Different types of tests in the pyramid make different choices in the trade-off between
fast feedback and protection against regressions. Tests in higher pyramid layers favor protec-
tion against regressions, while lower layers emphasize execution speed (figure 4.12).
Notice that neither layer gives up resistance to refactoring. Naturally, end-to-end and inte-
gration tests score higher on this metric than unit tests, but only as a side effect of
being more detached from the production code. Still, even unit tests should not con-
cede resistance to refactoring. All tests should aim at producing as few false positives as
possible, even when working directly with the production code. (How to do that is the
topic of the next chapter.)
 The exact mix between types of tests will be different for each team and project.
But in general, it should retain the pyramid shape: end-to-end tests should be the
minority; unit tests, the majority; and integration tests somewhere in the middle.
 The reason end-to-end tests are the minority is, again, the multiplication rule
described in section 4.4. End-to-end tests score extremely low on the metric of fast feed-
back. They also lack maintainability: they tend to be larger in size and require addi-
tional effort to maintain the involved out-of-process dependencies. Thus, end-to-end
tests only make sense when applied to the most critical functionality—features in
refactoring
Max
out
Protection against
regressions
Fast feedback
End-to-end
Integration
Unit tests
Resistance to
Figure 4.12
Different types of tests in the pyramid make different choices 
between fast feedback and protection against regressions. End-to-end tests 
favor protection against regressions, unit tests emphasize fast feedback, and 
integration tests lie in the middle.


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



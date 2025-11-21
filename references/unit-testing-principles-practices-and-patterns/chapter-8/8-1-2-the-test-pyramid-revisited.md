# 8.1.2 The Test Pyramid revisited (pp.187-188)

---
**Page 187**

187
What is an integration test?
Note that tests covering the controllers quadrant can sometimes be unit tests too. If all
out-of-process dependencies are replaced with mocks, there will be no dependencies
shared between tests, which will allow those tests to remain fast and maintain their iso-
lation from each other. Most applications do have an out-of-process dependency that
can’t be replaced with a mock, though. It’s usually a database—a dependency that is
not visible to other applications.
 As you may also remember from chapter 7, the other two quadrants from figure 8.1
(trivial code and overcomplicated code) shouldn’t be tested at all. Trivial code isn’t
worth the effort, while overcomplicated code should be refactored into algorithms
and controllers. Thus, all your tests must focus on the domain model and the control-
lers quadrants exclusively. 
8.1.2
The Test Pyramid revisited
It’s important to maintain a balance between unit and integration tests. Working
directly with out-of-process dependencies makes integration tests slow. Such tests are
also more expensive to maintain. The increase in maintainability costs is due to
The necessity to keep the out-of-process dependencies operational
The greater number of collaborators involved, which inflates the test’s size
On the other hand, integration tests go through a larger amount of code (both your
code and the code of the libraries used by the application), which makes them better
than unit tests at protecting against regressions. They are also more detached from
the production code and therefore have better resistance to refactoring.
 The ratio between unit and integration tests can differ depending on the project’s
specifics, but the general rule of thumb is the following: check as many of the business
scenario’s edge cases as possible with unit tests; use integration tests to cover one
happy path, as well as any edge cases that can’t be covered by unit tests.
DEFINITION
A happy path is a successful execution of a business scenario. An
edge case is when the business scenario execution results in an error.
Shifting the majority of the workload to unit tests helps keep maintenance costs low.
At the same time, having one or two overarching integration tests per business sce-
nario ensures the correctness of your system as a whole. This guideline forms the pyr-
amid-like ratio between unit and integration tests, as shown in figure 8.2 (as discussed
in chapter 2, end-to-end tests are a subset of integration tests).
 The Test Pyramid can take different shapes depending on the project’s complexity.
Simple applications have little (if any) code in the domain model and algorithms
quadrant. As a result, tests form a rectangle instead of a pyramid, with an equal num-
ber of unit and integration tests (figure 8.3). In the most trivial cases, you might have
no unit tests whatsoever.
 Note that integration tests retain their value even in simple applications. Regard-
less of how simple your code is, it’s still important to verify how it works in integration
with other subsystems. 


---
**Page 188**

188
CHAPTER 8
Why integration testing?
8.1.3
Integration testing vs. failing fast
This section elaborates on the guideline of using integration tests to cover one happy
path per business scenario and any edge cases that can’t be covered by unit tests. 
 For an integration test, select the longest happy path in order to verify interactions
with all out-of-process dependencies. If there’s no one path that goes through all such
interactions, write additional integration tests—as many as needed to capture commu-
nications with every external system.
 As with the edge cases that can’t be covered by unit tests, there are exceptions to
this part of the guideline, too. There’s no need to test an edge case if an incorrect
execution of that edge case immediately fails the entire application. For example, you
saw in chapter 7 how User from the sample CRM system implemented a CanChange-
Email method and made its successful execution a precondition for ChangeEmail():
End-
to-end
Integration
tests
Unit tests
Test count
Protection against
regressions,
resistance to
refactoring
Fast feedback,
maintainability
Figure 8.2
The Test Pyramid represents a trade-off that works best for most 
applications. Fast, cheap unit tests cover the majority of edge cases, while a 
smaller number of slow, more expensive integration tests ensure the correctness 
of the system as a whole.
Figure 8.3
The Test Pyramid of a simple project. 
Little complexity requires a smaller number of unit 
tests compared to a normal pyramid.
Unit tests
Integration tests



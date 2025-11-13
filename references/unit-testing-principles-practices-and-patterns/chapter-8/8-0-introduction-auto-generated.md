# 8.0 Introduction [auto-generated] (pp.185-186)

---
**Page 185**

185
Why integration testing?
You can never be sure your system works as a whole if you rely on unit tests exclu-
sively. Unit tests are great at verifying business logic, but it’s not enough to check
that logic in a vacuum. You have to validate how different parts of it integrate with
each other and external systems: the database, the message bus, and so on.
 In this chapter, you’ll learn the role of integration tests: when you should apply
them and when it’s better to rely on plain old unit tests or even other techniques
such as the Fail Fast principle. You will see which out-of-process dependencies to
use as-is in integration tests and which to replace with mocks. You will also see inte-
gration testing best practices that will help improve the health of your code base in
general: making domain model boundaries explicit, reducing the number of layers
in the application, and eliminating circular dependencies. Finally, you’ll learn why
interfaces with a single implementation should be used sporadically, and how and
when to test logging functionality.
This chapter covers
Understanding the role of integration testing
Diving deeper into the Test Pyramid concept
Writing valuable integration tests


---
**Page 186**

186
CHAPTER 8
Why integration testing?
8.1
What is an integration test?
Integration tests play an important role in your test suite. It’s also crucial to balance
the number of unit and integration tests. You will see shortly what that role is and how
to maintain the balance, but first, let me give you a refresher on what differentiates an
integration test from a unit test.
8.1.1
The role of integration tests
As you may remember from chapter 2, a unit test is a test that meets the following three
requirements:
Verifies a single unit of behavior,
Does it quickly,
And does it in isolation from other tests.
A test that doesn’t meet at least one of these three requirements falls into the category
of integration tests. An integration test then is any test that is not a unit test.
 In practice, integration tests almost always verify how your system works in integra-
tion with out-of-process dependencies. In other words, these tests cover the code from
the controllers quadrant (see chapter 7 for more details about code quadrants). The
diagram in figure 8.1 shows the typical responsibilities of unit and integration tests.
Unit tests cover the domain model, while integration tests check the code that glues
that domain model with out-of-process dependencies.
Domain model,
algorithms
Overcomplicated
code
Trivial code
Controllers
Complexity,
domain
signiﬁcance
Number of
collaborators
Integration
tests
Unit tests
Figure 8.1
Integration tests cover controllers, while unit tests cover the domain 
model and algorithms. Trivial and overcomplicated code shouldn’t be tested at all.



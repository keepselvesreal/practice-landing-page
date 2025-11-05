# 8.4 Summary (pp.183-187)

---
**Page 183**

183
Summary
 The second test simply looks for the “2 failed” string inside the message. This
makes the test more future-proof: the string might change slightly, but the core mes-
sage remains without forcing us to change the test.
Summary
Tests grow and change with the system under test. If we don’t pay attention to
maintainability, our tests may require so many changes from us that it might not
be worth changing them. We may instead end up deleting them, and throwing
away all the hard work that went into creating them. For tests to be useful in the
long run, they should fail only for reasons we truly care about.
A true failure is when a test fails because it finds a bug in production code. A false
failure is when a test fails for any other reason.
To estimate test maintainability, we can measure the number of false test fail-
ures and the reason for each failure, over time.
A test may falsely fail for multiple reasons: it conflicts with another test (in
which case, you should just remove it); changes in the production code’s API
(this can be mitigated by using factory and helper methods); changes in other
tests (such tests should be decoupled from each other).
Avoid testing private methods. Private methods are implementation details, and
the resulting tests are going to be fragile. Tests should verify observable behavior—
behavior that is relevant for the end user. Sometimes, the need to test a private
method is a sign of a missing abstraction, which means the method should be
made public or even be extracted into a separate class.
Keep tests DRY. Use helper methods to abstract nonessential details of arrange
and assert sections. This will simplify your tests without coupling them to each
other.
Avoid setup methods such as the beforeEach function. Once again, use helper
methods instead. Another option is to parameterize your tests and therefore
move the content of the beforeEach block to the test’s arrange section.
Avoid overspecification. Examples of overspecification are asserting the private
state of the code under test, asserting against calls on stubs, or assuming the
specific order of elements in a result collection or exact string matches when
that isn’t required.


---
**Page 184**



---
**Page 185**

Part 4
Design and process
These final chapters cover the problems you’ll face and the techniques you’ll
need when introducing unit testing to an existing organization or codebase.
 In chapter 9, we’ll talk about test readability. We’ll discuss naming conven-
tions for tests and input values for them. We’ll also cover best practices for test
structuring and writing better assertion messages.
 Chapter 10 explains how to develop a testing strategy. We’ll look at which test
levels you should prefer when testing a new feature, discuss common antipat-
terns in test levels, and talk about the test recipe strategy.
 In chapter 11, we’ll deal with the tough issue of implementing unit testing in
an organization, and we’ll cover techniques that can make your job easier. This
chapter provides answers to some tough questions that are common when first
implementing unit testing.
 In chapter 12, we’ll look at common problems associated with legacy code
and examine some tools for working with it.


---
**Page 186**



---
**Page 187**

187
Readability
Without readability, the tests you write are almost meaningless to whoever reads
them later on. Readability is the connecting thread between the person who wrote
the test and the poor soul who must read it a few months or years later. Tests are
stories you tell the next generation of programmers on a project. They allow a
developer to see exactly what an application is made of and where it started.
 This chapter is all about making sure the developers who come after you will be
able to maintain the production code and the tests that you write. They’ll need to
understand what they’re doing and where they should be doing it.
 There are several facets to readability:
Naming unit tests
Naming variables
Separating asserts from actions
Setting up and tearing down
Let’s go through these one by one.
This chapter covers
Naming conventions for unit tests
Writing readable tests



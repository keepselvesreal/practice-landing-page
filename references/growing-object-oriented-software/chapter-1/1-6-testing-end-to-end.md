# 1.6 Testing End-to-End (pp.8-9)

---
**Page 8**

Figure 1.2
Inner and outer feedback loops in TDD
The outer test loop is a measure of demonstrable progress, and the growing
suite of tests protects us against regression failures when we change the system.
Acceptance tests often take a while to make pass, certainly more than one check-in
episode, so we usually distinguish between acceptance tests we’re working on
(which are not yet included in the build) and acceptance tests for the features
that have been ﬁnished (which are included in the build and must always pass).
The inner loop supports the developers. The unit tests help us maintain the
quality of the code and should pass soon after they’ve been written. Failing unit
tests should never be committed to the source repository.
Testing End-to-End
Wherever possible, an acceptance test should exercise the system end-to-end
without directly calling its internal code. An end-to-end test interacts with the
system only from the outside: through its user interface, by sending messages as
if from third-party systems, by invoking its web services, by parsing reports, and
so on. As we discuss in Chapter 10, the whole behavior of the system includes
its interaction with its external environment. This is often the riskiest and most
difﬁcult aspect; we ignore it at our peril. We try to avoid acceptance tests that
just exercise the internal objects of the system, unless we really need the speed-up
and already have a stable set of end-to-end tests to provide cover.
The Importance of End-to-End Testing: A Horror Story
Nat was once brought onto a project that had been using TDD since its inception.
The team had been writing acceptance tests to capture requirements and show
progress to their customer representatives. They had been writing unit tests for
the classes of the system, and the internals were clean and easy to change.They
had been making great progress, and the customer representatives had signed
off all the implemented features on the basis of the passing acceptance tests.
Chapter 1
What Is the Point of Test-Driven Development?
8


---
**Page 9**

But the acceptance tests did not run end-to-end—they instantiated the system’s
internal objects and directly invoked their methods. The application actually did
nothing at all. Its entry point contained only a single comment:
// TODO implement this
Additional feedback loops, such as regular show-and-tell sessions, should have
been in place and would have caught this problem.
For us, “end-to-end” means more than just interacting with the system from
the outside—that might be better called “edge-to-edge” testing. We prefer to
have the end-to-end tests exercise both the system and the process by which it’s
built and deployed. An automated build, usually triggered by someone checking
code into the source repository, will: check out the latest version; compile and
unit-test the code; integrate and package the system; perform a production-like
deployment into a realistic environment; and, ﬁnally, exercise the system through
its external access points. This sounds like a lot of effort (it is), but has to be
done anyway repeatedly during the software’s lifetime. Many of the steps might
be ﬁddly and error-prone, so the end-to-end build cycle is an ideal candidate for
automation. You’ll see in Chapter 10 how early in a project we get this working.
A system is deployable when the acceptance tests all pass, because they should
give us enough conﬁdence that everything works. There’s still, however, a ﬁnal
step of deploying to production. In many organizations, especially large or
heavily regulated ones, building a deployable system is only the start of a release
process. The rest, before the new features are ﬁnally available to the end users,
might involve different kinds of testing, handing over to operations and data
groups, and coordinating with other teams’ releases. There may also be additional,
nontechnical costs involved with a release, such as training, marketing, or an
impact on service agreements for downtime. The result is a more difﬁcult release
cycle than we would like, so we have to understand our whole technical and
organizational environment.
Levels of Testing
We build a hierarchy of tests that correspond to some of the nested feedback
loops we described above:
Acceptance:  Does the whole system work?
Integration:  Does our code work against code we can't change?
Unit:  Do our objects do the right thing, are they convenient to work with?
9
Levels of Testing



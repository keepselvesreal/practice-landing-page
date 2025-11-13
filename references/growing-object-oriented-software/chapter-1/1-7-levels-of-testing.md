# 1.7 Levels of Testing (pp.9-10)

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


---
**Page 10**

There’s been a lot of discussion in the TDD world over the terminology for
what we’re calling acceptance tests: “functional tests,” “customer tests,” “system
tests.” Worse, our deﬁnitions are often not the same as those used by professional
software testers. The important thing is to be clear about our intentions. We use
“acceptance tests” to help us, with the domain experts, understand and agree on
what we are going to build next. We also use them to make sure that we haven’t
broken any existing features as we continue developing.
Our preferred implementation of the “role” of acceptance testing is to write
end-to-end tests which, as we just noted, should be as end-to-end as possible;
our bias often leads us to use these terms interchangeably although, in some
cases, acceptance tests might not be end-to-end.
We use the term integration tests to refer to the tests that check how some of
our code works with code from outside the team that we can’t change. It might
be a public framework, such as a persistence mapper, or a library from another
team within our organization. The distinction is that integration tests make sure
that any abstractions we build over third-party code work as we expect. In a
small system, such as the one we develop in Part III, acceptance tests might be
enough. In most professional development, however, we’ll want integration tests
to help tease out conﬁguration issues with the external packages, and to give
quicker feedback than the (inevitably) slower acceptance tests.
We won’t write much more about techniques for acceptance and integration
testing, since both depend on the technologies involved and even the culture of
the organization. You’ll see some examples in Part III which we hope give a sense
of the motivation for acceptance tests and show how they ﬁt in the development
cycle. Unit testing techniques, however, are speciﬁc to a style of programming,
and so are common across all systems that take that approach—in our case, are
object-oriented.
External and Internal Quality
There’s another way of looking at what the tests can tell us about a system. We
can make a distinction between external and internal quality: External quality
is how well the system meets the needs of its customers and users (is it functional,
reliable, available, responsive, etc.), and internal quality is how well it meets the
needs of its developers and administrators (is it easy to understand, easy to change,
etc.). Everyone can understand the point of external quality; it’s usually part of
the contract to build. The case for internal quality is equally important but is
often harder to make. Internal quality is what lets us cope with continual and
unanticipated change which, as we saw at the beginning of this chapter, is a fact
of working with software. The point of maintaining internal quality is to allow
us to modify the system’s behavior safely and predictably, because it minimizes
the risk that a change will force major rework.
Chapter 1
What Is the Point of Test-Driven Development?
10



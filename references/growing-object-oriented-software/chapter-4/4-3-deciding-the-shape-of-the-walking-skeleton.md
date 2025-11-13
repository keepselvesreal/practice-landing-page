# 4.3 Deciding the Shape of the Walking Skeleton (pp.33-35)

---
**Page 33**

a dummy server, not the real site. At some point before going live, we would
have had to test against Southabee’s On-Line; the earlier we can do that, the
easier it will be for us to respond to any surprises that turn up.
Whilst building the “walking skeleton,” we concentrate on the structure and
don’t worry too much about cleaning up the test to be beautifully expressive.
The walking skeleton and its supporting infrastructure are there to help us work
out how to start test-driven development. It’s only the ﬁrst step toward a complete
end-to-end acceptance-testing solution. When we write the test for the ﬁrst feature,
then we need to “write the test you want to read” (page 42) to make sure that
it’s a clear expression of the behavior of the system.
The Importance of Early End-to-End Testing
We joined a project that had been running for a couple of years but had never
tested their entire system end-to-end. There were frequent production outages
and deployments often failed. The system was large and complex, reﬂecting the
complicated business transactions it managed.The effort of building an automated,
end-to-end test suite was so large that an entire new team had to be formed to
perform the work. It took them months to build an end-to-end test environment,
and they never managed to get the entire system covered by an end-to-end
test suite.
Because the need for end-to-end testing had not inﬂuenced its design, the system
was difﬁcult to test. For example, the system’s components used internal timers
to schedule activities, some of them days or weeks into the future. This made it
very difﬁcult to write end-to-end tests: It was impractical to run the tests in real-
time but the scheduling could not be inﬂuenced from outside the system. The
developers had to redesign the system itself so that periodic activities were trig-
gered by messages sent from a remote scheduler which could be replaced in the
test environment; see “Externalize Event Sources” (page 326).This was a signiﬁ-
cant architectural change—and it was very risky because it had to be performed
without end-to-end test coverage.
Deciding the Shape of the Walking Skeleton
The development of a “walking skeleton” is the moment when we start to make
choices about the high-level structure of our application. We can’t automate the
build, deploy, and test cycle without some idea of the overall structure. We don’t
need much detail yet, just a broad-brush picture of what major system components
will be needed to support the ﬁrst planned release and how they will communicate.
Our rule of thumb is that we should be able to draw the design for the “walking
skeleton” in a few minutes on a whiteboard.
33
Deciding the Shape of the Walking Skeleton


---
**Page 34**

Mappa Mundi
We ﬁnd that maintaining a public drawing of the structure of the system, for example
on the wall in the team’s work area as in Figure 4.1, helps the team stay oriented
when working on the code.
Figure 4.1
A broad-brush architecture diagram drawn on the
wall of a team’s work area
To design this initial structure, we have to have some understanding of the
purpose of the system, otherwise the whole exercise risks being meaningless. We
need a high-level view of the client’s requirements, both functional and non-
functional, to guide our choices. This preparatory work is part of the chartering
of the project, which we must leave as outside the scope of this book.
The point of the “walking skeleton” is to use the writing of the ﬁrst test to
draw out the context of the project, to help the team map out the landscape of
their solution—the essential decisions that they must take before they can write
any code; Figure 4.2 shows how the TDD process we drew in Figure 1.2 ﬁts into
this context.
Chapter 4
Kick-Starting the Test-Driven Cycle
34


---
**Page 35**

Figure 4.2
The context of the ﬁrst test
Please don’t confuse this with doing “Big Design Up Front” (BDUF) which
has such a bad reputation in the Agile Development community. We’re not trying
to elaborate the whole design down to classes and algorithms before we start
coding. Any ideas we have now are likely to be wrong, so we prefer to discover
those details as we grow the system. We’re making the smallest number of
decisions we can to kick-start the TDD cycle, to allow us to start learning and
improving from real feedback.
Build Sources of Feedback
We have no guarantees that the decisions we’ve taken about the design of our
application, or the assumptions on which they’re based, are right. We do the best
we can, but the only thing we can rely on is validating them as soon as possible
by building feedback into our process. The tools we build to implement the
“walking skeleton” are there to support this learning process. Of course, these
tools too will not be perfect, and we expect we will improve them incrementally
as we learn how well they support the team.
Our ideal situation is where the team releases regularly to a real production
system, as in Figure 4.3. This allows the system’s stakeholders to respond to how
well the system meets their needs, at the same time allowing us to judge its
implementation.
Figure 4.3
Requirements feedback
35
Build Sources of Feedback



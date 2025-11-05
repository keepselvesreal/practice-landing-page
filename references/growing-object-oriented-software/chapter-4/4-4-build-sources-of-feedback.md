# 4.4 Build Sources of Feedback (pp.35-36)

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


---
**Page 36**

We use the automation of building and testing to give us feedback on qualities
of the system, such as how easily we can cut a version and deploy, how well the
design works, and how good the code is. The automated deployment helps us
release frequently to real users, which gives us feedback on how well we have
understood the domain and whether seeing the system in practice has changed
our customer’s priorities.
The great beneﬁt is that we will be able to make changes in response to what-
ever we learn, because writing everything test-ﬁrst means that we will have a
thorough set of regression tests. No tests are perfect, of course, but in practice
we’ve found that a substantial test suite allows us to make major changes safely.
Expose Uncertainty Early
All this effort means that teams are frequently surprised by the time it takes to
get a “walking skeleton” working, considering that it does hardly anything.
That’s because this ﬁrst step involves establishing a lot of infrastructure and
asking (and answering) many awkward questions. The time to implement the
ﬁrst few features will be unpredictable as the team discovers more about its re-
quirements and target environment. For a new team, this will be compounded
by the social stresses of learning how to work together.
Fred Tingey, a colleague, once observed that incremental development can be
disconcerting for teams and management who aren’t used to it because it front-
loads the stress in a project. Projects with late integration start calmly but gener-
ally turn difﬁcult towards the end as the team tries to pull the system together
for the ﬁrst time. Late integration is unpredictable because the team has to
assemble a great many moving parts with limited time and budget to ﬁx any
failures. The result is that experienced stakeholders react badly to the instability
at the start of an incremental project because they expect that the end of the
project will be much worse.
Our experience is that a well-run incremental development runs in the opposite
direction. It starts unsettled but then, after a few features have been implemented
and the project automation has been built up, settles in to a routine. As a project
approaches delivery, the end-game should be a steady production of functionality,
perhaps with a burst of activity before the ﬁrst release. All the mundane but
brittle tasks, such as deployment and upgrades, will have been automated so that
they “just work.” The contrast looks rather like Figure 4.4.
This aspect of test-driven development, like others, may appear counter-
intuitive, but we’ve always found it worth taking enough time to structure and
automate the basics of the system—or at least a ﬁrst cut. Of course, we don’t
want to spend the whole project setting up a perfect “walking skeleton,” so we
limit ourselves to whiteboard-level decisions and reserve the right to change our
mind when we have to. But the most important thing is to have a sense of direction
and a concrete implementation to test our assumptions.
Chapter 4
Kick-Starting the Test-Driven Cycle
36



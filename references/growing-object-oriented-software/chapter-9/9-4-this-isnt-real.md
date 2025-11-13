# 9.4 This Isn't Real (pp.81-83)

---
**Page 81**

We don’t know if this is exactly the order of steps we’ll take, but we believe
we need all of this, and we can adjust as we go along. To keep ourselves
focused, we’ve written the plan on an index card, as in Figure 9.4.
This Isn’t Real
By now you may be raising objections about all the practicalities we’ve skipped
over. We saw them too. We’ve taken shortcuts with the process and design to
give you a feel of how a real project works while remaining within the limits of
a book. In particular:
•
This isn’t a realistic architecture: XMPP is neither reliable nor secure, and
so is unsuitable for transactions. Ensuring any of those qualities is outside
our scope. That said, the fundamental techniques that we describe still apply
whatever the underlying architecture may be. (In our defense, we see that
major systems have been built on a protocol as inappropriate as HTTP, so
perhaps we’re not as unrealistic as we fear.)
•
This isn’t Agile Planning: We rushed through the planning of the project
to produce a single to-do list. In a real project, we’d likely have a view of
the whole deliverable (a release plan) before jumping in. There are good
descriptions of how to do agile planning in other books, such as [Shore07]
and [Cohn05].
•
This isn’t realistic usability design: Good user experience design investigates
what the end user is really trying to achieve and uses that to create a con-
sistent experience. The User Experience community has been engaging with
the Agile Development community for some time on how to do this itera-
tively. This project is simple enough that we can draft a vision of what we
want to achieve and work towards it.
81
This Isn’t Real


---
**Page 82**

This page intentionally left blank 


---
**Page 83**

Chapter 10
The Walking Skeleton
In which we set up our development environment and write our ﬁrst
end-to-end test. We make some infrastructure choices that allow us to
get started, and construct a build. We’re surprised, yet again, at how
much effort this takes.
Get the Skeleton out of the Closet
So now we’ve got an idea of what to build, can we get on with it and write our
ﬁrst unit test?
Not yet.
Our ﬁrst task is to create the “walking skeleton” we described in “First, Test
a Walking Skeleton” (page 32). Again, the point of the walking skeleton is to
help us understand the requirements well enough to propose and validate a broad-
brush system structure. We can always change our minds later, when we learn
more, but it’s important to start with something that maps out the landscape of
our solution. Also, it’s very important to be able to assess the approach we’ve
chosen and to test our decisions so we can make changes with conﬁdence later.
For most projects, developing the walking skeleton takes a surprising amount
of effort. First, because deciding what to do will ﬂush out all sorts of questions
about the application and its place in the world. Second, because the automation
of building, packaging, and deploying into a production-like environment (once
we know what that means) will ﬂush out all sorts of technical and organizational
questions.
Iteration Zero
In most Agile projects, there’s a ﬁrst stage where the team is doing initial analysis,
setting up its physical and technical environments, and otherwise getting started.
The team isn’t adding much visible functionality since almost all the work is infra-
structure, so it might not make sense to count this as a conventional iteration for
scheduling purposes. A common practice is to call this step iteration zero: “iteration”
because the team still needs to time-box its activities and “zero” because it’s before
functional development starts in iteration one. One important task for iteration zero
is to use the walking skeleton to test-drive the initial architecture.
Of course, we start our walking skeleton by writing a test.
83



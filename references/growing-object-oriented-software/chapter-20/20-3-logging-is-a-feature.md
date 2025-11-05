# 20.3 Logging Is a Feature (pp.233-235)

---
**Page 233**

One goal of object orientation as a technique for structuring code is to make
the boundaries of an object clearly visible. An object should only deal with values
and instances that are either local—created and managed within its scope—or
passed in explicitly, as we emphasized in “Context Independence” (page 54).
In the example above, the act of making date checking testable forced us to
make the Receiver’s requirements more explicit and to think more clearly about
the domain.
Use the Same Techniques to Break Dependencies in Unit Tests
as in Production Code
There are several frameworks available that use techniques such as manipulating
class loaders or bytecodes to allow unit tests to break dependencies without
changing the target code. As a rule, these are advanced techniques that most
developers would not use when writing production code. Sometimes these tools
really are necessary, but developers should be aware that they come with a
hidden cost.
Unit-testing tools that let the programmer sidestep poor dependency management
in the design waste a valuable source of feedback.When the developers eventually
do need to address these design weaknesses to add some urgent feature, they
will ﬁnd it harder to do. The poor structure will have inﬂuenced other parts of the
system that rely on it, and any understanding of the original intent will have
evaporated. As with dirty pots and pans, it’s easier to get the grease off before it’s
been baked in.
Logging Is a Feature
We have a more contentious example of working with objects that are hard to
replace: logging. Take a look at these two lines of code:
log.error("Lost touch with Reality after " + timeout + "seconds");
log.trace("Distance traveled in the wilderness: " + distance);
These are two separate features that happen to share an implementation. Let
us explain.
•
Support logging (errors and info) is part of the user interface of the appli-
cation. These messages are intended to be tracked by support staff, as well
as perhaps system administrators and operators, to diagnose a failure or
monitor the progress of the running system.
•
Diagnostic logging (debug and trace) is infrastructure for programmers.
These messages should not be turned on in production because they’re in-
tended to help the programmers understand what’s going on inside the
system they’re developing.
233
Logging Is a Feature


---
**Page 234**

Given this distinction, we should consider using different techniques for these
two type of logging. Support logging should be test-driven from somebody’s re-
quirements, such as auditing or failure recovery. The tests will make sure we’ve
thought about what each message is for and made sure it works. The tests will
also protect us from breaking any tools and scripts that other people write to
analyze these log messages. Diagnostic logging, on the other hand, is driven by
the programmers’ need for ﬁne-grained tracking of what’s happening in the sys-
tem. It’s scaffolding—so it probably doesn’t need to be test-driven and the mes-
sages might not need to be as consistent as those for support logs. After all, didn’t
we just agree that these messages are not to be used in production?
Notiﬁcation Rather Than Logging
To get back to the point of the chapter, writing unit tests against static global
objects, including loggers, is clumsy. We have to either read from the ﬁle system
or manage an extra appender object for testing; we have to remember to clean
up afterwards so that tests don’t interfere with each other and set the right level
on the right logger. The noise in the test reminds us that our code is working at
two levels: our domain and the logging infrastructure. Here’s a common example
of code with logging:
Location location = tracker.getCurrentLocation();
for (Filter filter : filters) {
  filter.selectFor(location);
if (logger.isInfoEnabled()) {
    logger.info("Filter " + filter.getName() + ", " + filter.getDate()
                 + " selected for " + location.getName() 
                 + ", is current: " + tracker.isCurrent(location));
  }
}
Notice the shift in vocabulary and style between the functional part of the
loop and the (emphasized) logging part. The code is doing two things at
once—something to do with locations and rendering support information—which
breaks the single responsibility principle. Maybe we could do this instead:
Location location = tracker.getCurrentLocation();
for (Filter filter : filters) {
  filter.selectFor(location);
support.notifyFiltering(tracker, location, filter);}
where the support object might be implemented by a logger, a message bus,
pop-up windows, or whatever’s appropriate; this detail is not relevant to the
code at this level.
This code is also easier to test, as you saw in Chapter 19. We, not the logging
framework, own the support object, so we can pass in a mock implementation
at our convenience and keep it local to the test case. The other simpliﬁcation is
that now we’re testing for objects, rather than formatted contents of a string. Of
Chapter 20
Listening to the Tests
234


---
**Page 235**

course, we will still need to write an implementation of support and some focused
integration tests to go with it.
But That’s Crazy Talk…
The idea of encapsulating support reporting sounds like over-design, but it’s
worth thinking about for a moment. It means we’re writing code in terms of our
intent (helping the support people) rather than implementation (logging), so it’s
more expressive. All the support reporting is handled in a few known places, so
it’s easier to be consistent about how things are reported and to encourage reuse.
It can also help us structure and control our reporting in terms of the application
domain, rather than in terms of Java packages. Finally, the act of writing a test
for each report helps us avoid the “I don’t know what to do with this exception,
so I’ll log it and carry on” syndrome, which leads to log bloat and production
failures because we haven’t handled obscure error conditions.
One objection we’ve heard is, “I can’t pass in a logger for testing because I’ve
got logging all over my domain objects. I’d have to pass one around everywhere.”
We think this is a test smell that is telling us that we haven’t clariﬁed our design
enough. Perhaps some of our support logging should really be diagnostic logging,
or we’re logging more than we need because of something that we wrote when
we hadn’t yet understood the behavior. Most likely, there’s still too much dupli-
cation in our domain code and we haven’t yet found the “choke points” where
most of the production logging should go.
So what about diagnostic logging? Is it disposable scaffolding that should be
taken down once the job is done, or essential infrastructure that should be tested
and maintained? That depends on the system, but once we’ve made the distinction
we have more freedom to think about using different techniques for support and
diagnostic logging. We might even decide that in-line code is the wrong technique
for diagnostic logging because it interferes with the readability of the production
code that matters. Perhaps we could weave in some aspects instead (since that’s
the canonical example of their use); perhaps not—but at least we’ve now
clariﬁed the choice.
One ﬁnal data point. One of us once worked on a system where so much
content was written to the logs that they had to be deleted after a week to ﬁt on
the disks. This made maintenance very difﬁcult as the relevant logs were usually
gone by the time a bug was assigned to be ﬁxed. If they’d logged nothing at all,
the system would have run faster with no loss of useful information.
Mocking Concrete Classes
One approach to interaction testing is to mock concrete classes rather than inter-
faces. The technique is to inherit from the class you want to mock and override
the methods that will be called within the test, either manually or with any of
235
Mocking Concrete Classes



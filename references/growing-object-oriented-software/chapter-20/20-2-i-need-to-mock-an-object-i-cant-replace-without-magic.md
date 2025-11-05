# 20.2 I Need to Mock an Object I Can't Replace (without Magic) (pp.230-233)

---
**Page 230**

I Need to Mock an Object I Can’t Replace (without Magic)
Singletons Are Dependencies
One interpretation of reducing complexity in code is making commonly useful
objects accessible through a global structure, usually implemented as a singleton.
Any code that needs access to a feature can just refer to it by its global name
instead of receiving it as an argument. Here’s a common example:
Date now = new Date();
Under the covers, the constructor calls the singleton System and sets the new
instance to the current time using System.currentTimeMillis(). This is a conve-
nient technique, but it comes at a cost. Let’s say we want to write a test like this:
@Test public void rejectsRequestsNotWithinTheSameDay() {
  receiver.acceptRequest(FIRST_REQUEST);
// the next day
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
The implementation looks like this:
public boolean acceptRequest(Request request) {
  final Date now = new Date();
  if (dateOfFirstRequest == null) {
    dateOfFirstRequest = now;
   } else if (firstDateIsDifferentFrom(now)) {
    return false;
  }
// process the request
  return true;
}
where dateOfFirstRequest is a ﬁeld and firstDateIsDifferentFrom() is a helper
method that hides the unpleasantness of working with the Java date library.
To test this timeout, we must either make the test wait overnight or do some-
thing clever (perhaps with aspects or byte-code manipulation) to intercept the
constructor and return suitable Date values for the test. This difﬁculty in testing
is a hint that we should change the code. To make the test easier, we need to
control how Date objects are created, so we introduce a Clock and pass it into
the Receiver. If we stub Clock, the test might look like this:
@Test public void rejectsRequestsNotWithinTheSameDay() {
  Receiver receiver = new Receiver(stubClock);
  stubClock.setNextDate(TODAY);
  receiver.acceptRequest(FIRST_REQUEST);
  stubClock.setNextDate(TOMORROW);
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
Chapter 20
Listening to the Tests
230


---
**Page 231**

and the implementation like this:
public boolean acceptRequest(Request request) {
  final Date now = clock.now();
  if (dateOfFirstRequest == null) {
   dateOfFirstRequest = now;
  } else if (firstDateIsDifferentFrom(now)) {
   return false;
  }
// process the request
  return true;
}
Now we can test the Receiver without any special tricks. More importantly,
however, we’ve made it obvious that Receiver is dependent on time—we can’t
even create one without a Clock. Some argue that this is breaking encapsulation
by exposing the internals of a Receiver—we should be able to just create an in-
stance and not worry—but we’ve seen so many systems that are impossible to
test because the developers did not isolate the concept of time. We want to know
about this dependency, especially when the service is rolled out across the world,
and New York and London start complaining about different results.
From Procedures to Objects
Having taken the trouble to introduce a Clock object, we start wondering if our
code is missing a concept: date checking in terms of our domain. A Receiver
doesn’t need to know all the details of a calendar system, such as time zones and
locales; it just need to know if the date has changed for this application. There’s
a clue in the fragment:
firstDateIsDifferentFrom(now)
which means that we’ve had to wrap up some date manipulation code in Receiver.
It’s the wrong object; that kind of work should be done in Clock. We write the
test again:
@Test public void rejectsRequestsNotWithinTheSameDay() {
  Receiver receiver = new Receiver(clock);
  context.checking(new Expectations() {{
   allowing(clock).now(); will(returnValue(NOW));
one(clock).dayHasChangedFrom(NOW); will(returnValue(false));
  }});
  receiver.acceptRequest(FIRST_REQUEST);
  assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
}
The implementation looks like this:
231
I Need to Mock an Object I Can’t Replace (without Magic)


---
**Page 232**

public boolean acceptRequest(Request request) {
  if (dateOfFirstRequest == null) {
   dateOfFirstRequest = clock.now();
  } else if (clock.dayHasChangedFrom(dateOfFirstRequest)) {
   return false;
  }
// process the request
  return true;
}
This version of Receiver is more focused: it doesn’t need to know how to dis-
tinguish one date from another and it only needs to get a date to set the ﬁrst
value. The Clock interface deﬁnes exactly those date services Receiver needs from
its environment.
But we think we can push this further. Receiver only retains a date so that it
can detect a change of day; perhaps we should delegate all the date functionality
to another object which, for want of a better name, we’ll call a SameDayChecker.
@Test public void rejectsRequestsOutsideAllowedPeriod() {
  Receiver receiver = new Receiver(sameDayChecker);
  context.checking(new Expectations() {{
allowing(sameDayChecker).hasExpired(); will(returnValue(false));
  }});
  assertFalse("too late now", receiver.acceptRequest(REQUEST));
}
with an implementation like this:
public boolean acceptRequest(Request request) {
  if (sameDayChecker.hasExpired()) {
   return false;
  }
// process the request
  return true;
}
All the logic about dates has been separated out from Receiver, which can
concentrate on processing the request. With two objects, we can make sure that
each behavior (date checking and request processing) is unit-tested cleanly.
Implicit Dependencies Are Still Dependencies
We can hide a dependency from the caller of a component by using a global
value to bypass encapsulation, but that doesn’t make the dependency go away—it
just makes it inaccessible. For example, Steve once had to work with a Microsoft
.Net library that couldn’t be loaded without installing ActiveDirectory—which
wasn’t actually required for the features he wanted to use and which he couldn’t
install on his machine anyway. The library developer was trying to be helpful
and to make it “just work,” but the result was that Steve couldn’t get it to work
at all.
Chapter 20
Listening to the Tests
232


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



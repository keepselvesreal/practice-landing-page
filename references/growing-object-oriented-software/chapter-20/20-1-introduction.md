# 20.1 Introduction (pp.229-230)

---
**Page 229**

Chapter 20
Listening to the Tests
You can see a lot just by observing.
—Yogi Berra
Introduction
Sometimes we ﬁnd it difﬁcult to write a test for some functionality we want to
add to our code. In our experience, this usually means that our design can be
improved—perhaps the class is too tightly coupled to its environment or does
not have clear responsibilities. When this happens, we ﬁrst check whether it’s an
opportunity to improve our code, before working around the design by making
the test more complicated or using more sophisticated tools. We’ve found
that the qualities that make an object easy to test also make our code responsive
to change.
The trick is to let our tests drive our design (that’s why it’s called test-driven
development). TDD is about testing code, verifying its externally visible qualities
such as functionality and performance. TDD is also about feedback on the code’s
internal qualities: the coupling and cohesion of its classes, dependencies that are
explicit or hidden, and effective information hiding—the qualities that keep the
code maintainable.
With practice, we’ve become more sensitive to the rough edges in our tests, so
we can use them for rapid feedback about the design. Now when we ﬁnd a feature
that’s difﬁcult to test, we don’t just ask ourselves how to test it, but also why is
it difﬁcult to test.
In this chapter, we look at some common “test smells” that we’ve encountered
and discuss what they might imply about the design of the code. There are two
categories of test smell to consider. One is where the test itself is not well
written—it may be unclear or brittle. Meszaros [Meszaros07] covers several such
patterns in his “Test Smells” chapter. This chapter is concerned with the other
category, where a test is highlighting that the target code is the problem. Meszaros
has one pattern for this, called “Hard-to-Test Code.” We’ve picked out some
common cases that we’ve seen that are relevant to our approach to TDD.
229


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



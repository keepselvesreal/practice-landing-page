# 2.6 Unit-Testing the Collaborating Objects (pp.18-19)

---
**Page 18**

public class Train {
  private final List<Carriage> carriages […]
  private int percentReservedBarrier = 70;
  public void reserveSeats(ReservationRequest request) {
    for (Carriage carriage : carriages) {
      if (carriage.getSeats().getPercentReserved() < percentReservedBarrier) {
        request.reserveSeatsIn(carriage);
        return;
      }
    }
    request.cannotFindSeats();
  }
}
We shouldn’t expose the internal structure of Carriage to implement this, not
least because there may be different types of carriages within a train. Instead, we
should ask the question we really want answered, instead of asking for the
information to help us ﬁgure out the answer ourselves:
public void reserveSeats(ReservationRequest request) {
  for (Carriage carriage : carriages) {
    if (carriage.hasSeatsAvailableWithin(percentReservedBarrier)) {
      request.reserveSeatsIn(carriage);
      return;
    }
  }
  request.cannotFindSeats();
} 
Adding a query method moves the behavior to the most appropriate object,
gives it an explanatory name, and makes it easier to test.
We try to be sparing with queries on objects (as opposed to values) because
they can allow information to “leak” out of the object, making the system a little
bit more rigid. At a minimum, we make a point of writing queries that describe
the intention of the calling object, not just the implementation.
Unit-Testing the Collaborating Objects
We appear to have painted ourselves into a corner. We’re insisting on focused
objects that send commands to each other and don’t expose any way to query
their state, so it looks like we have nothing available to assert in a unit test. For
example, in Figure 2.4, the circled object will send messages to one or more of
its three neighbors when invoked. How can we test that it does so correctly
without exposing any of its internal state?
One option is to replace the target object’s neighbors in a test with substitutes,
or mock objects, as in Figure 2.5. We can specify how we expect the target object
to communicate with its mock neighbors for a triggering event; we call these
speciﬁcations expectations. During the test, the mock objects assert that they
Chapter 2
Test-Driven Development with Objects
18


---
**Page 19**

Figure 2.4
Unit-testing an object in isolation
Figure 2.5
Testing an object with mock objects
have been called as expected; they also implement any stubbed behavior needed
to make the rest of the test work.
With this infrastructure in place, we can change the way we approach TDD.
Figure 2.5 implies that we’re just trying to test the target object and that we al-
ready know what its neighbors look like. In practice, however, those collaborators
don’t need to exist when we’re writing a unit test. We can use the test to help us
tease out the supporting roles our object needs, deﬁned as Java interfaces, and
ﬁll in real implementations as we develop the rest of the system. We call this in-
terface discovery; you’ll see an example when we extract an AuctionEventListener
in Chapter 12.
Support for TDD with Mock Objects
To support this style of test-driven programming, we need to create mock in-
stances of the neighboring objects, deﬁne expectations on how they’re called and
then check them, and implement any stub behavior we need to get through the
test. In practice, the runtime structure of a test with mock objects usually looks
like Figure 2.6.
19
Support for TDD with Mock Objects



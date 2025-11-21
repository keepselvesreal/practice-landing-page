# 2.5 But Sometimes Ask (pp.17-18)

---
**Page 17**

Tell, Don’t Ask
We have objects sending each other messages, so what do they say? Our experi-
ence is that the calling object should describe what it wants in terms of the role
that its neighbor plays, and let the called object decide how to make that happen.
This is commonly known as the “Tell, Don’t Ask” style or, more formally, the
Law of Demeter. Objects make their decisions based only on the information
they hold internally or that which came with the triggering message; they avoid
navigating to other objects to make things happen. Followed consistently, this
style produces more ﬂexible code because it’s easy to swap objects that play the
same role. The caller sees nothing of their internal structure or the structure of
the rest of the system behind the role interface.
When we don’t follow the style, we can end up with what’s known as “train
wreck” code, where a series of getters is chained together like the carriages in a
train. Here’s one case we found on the Internet:
((EditSaveCustomizer) master.getModelisable()
  .getDockablePanel()
    .getCustomizer())
      .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
After some head scratching, we realized what this fragment was meant to say:
master.allowSavingOfCustomisations();
This wraps all that implementation detail up behind a single call. The client of
master no longer needs to know anything about the types in the chain. We’ve
reduced the risk that a design change might cause ripples in remote parts of the
codebase.
As well as hiding information, there’s a more subtle beneﬁt from “Tell, Don’t
Ask.” It forces us to make explicit and so name the interactions between objects,
rather than leaving them implicit in the chain of getters. The shorter version
above is much clearer about what it’s for, not just how it happens to be
implemented.
But Sometimes Ask
Of course we don’t “tell” everything;1 we “ask” when getting information from
values and collections, or when using a factory to create new objects. Occasion-
ally, we also ask objects about their state when searching or ﬁltering, but we still
want to maintain expressiveness and avoid “train wrecks.”
For example (to continue with the metaphor), if we naively wanted to spread
reserved seats out across the whole of a train, we might start with something like:
1. Although that’s an interesting exercise to try, to stretch your technique.
17
But Sometimes Ask


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



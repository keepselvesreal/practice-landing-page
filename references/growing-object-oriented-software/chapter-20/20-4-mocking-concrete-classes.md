# 20.4 Mocking Concrete Classes (pp.235-237)

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


---
**Page 236**

the mocking frameworks. We think this is a technique that should be used only
when you really have no other options.
Here’s an example of mocking by hand. The test veriﬁes that the music centre
starts the CD player at the requested time. Assume that setting the schedule on
a CdPlayer object involves triggering some behavior we don’t want in the test,
so we override scheduleToStartAt() and verify afterwards that we’ve called it
with the right argument.
public class MusicCentreTest {
  @Test public void 
startsCdPlayerAtTimeRequested() {
    final MutableTime scheduledTime = new MutableTime();
    CdPlayer player = new CdPlayer() {
      @Override public void scheduleToStartAt(Time startTime) {
        scheduledTime.set(startTime);
      }
    }
    MusicCentre centre = new MusicCentre(player);
    centre.startMediaAt(LATER);
    assertEquals(LATER, scheduledTime.get());
  }
}
The problem with this approach is that it leaves the relationship between the
CdPlayer and MusicCentre implicit. We hope we’ve made clear by now that our
intention in test-driven development is to use mock objects to bring out relation-
ships between objects. If we subclass, there’s nothing in the domain code to make
such a relationship visible—just methods on an object. This makes it harder to
see if the service that supports this relationship might be relevant elsewhere, and
we’ll have to do the analysis again next time we work with the class. To make
the point, here’s a possible implementation of CdPlayer:
public class CdPlayer {
  public void scheduleToStartAt(Time startTime) { […]
  public void stop() { […]
  public void gotoTrack(int trackNumber) { […]
  public void spinUpDisk() { […]
  public void eject() { […]
}
It turns out that our MusicCentre only uses the starting and stopping methods
on the CdPlayer; the rest are used by some other part of the system. We would
be overspecifying the MusicCentre by requiring it to talk to a CdPlayer; what it
actually needs is a ScheduledDevice. Robert Martin made the point (back in
1996) in his Interface Segregation Principle that “Clients should not be forced
to depend upon interfaces that they do not use,” but that’s exactly what we do
when we mock a concrete class.
Chapter 20
Listening to the Tests
236


---
**Page 237**

There’s a more subtle but powerful reason for not mocking concrete classes.
When we extract an interface as part of our test-driven development process, we
have to think up a name to describe the relationship we’ve just discovered—in
this example, the ScheduledDevice. We ﬁnd that this makes us think harder about
the domain and teases out concepts that we might otherwise miss. Once something
has a name, we can talk about it.
“Break Glass in Case of Emergency”
There are a few occasions when we have to put up with this smell. The least un-
acceptable situation is where we’re working with legacy code that we control
but can’t change all at once. Alternatively, we might be working with third-party
code that we can’t change at all (see Chapter 8). We ﬁnd that it’s almost always
better to write a veneer over an external library rather than mock it directly—but
occasionally, it’s just not worth it. We broke the rule with Logger in Chapter 19
but apologized a lot and felt bad about it. In any case, these are unfortunate but
necessary compromises that we would try to work our way out of when possible.
The longer we leave them in the code, the more likely it is that some brittleness
in the design will cause us grief.
Above all, do not override a class’ internal features—this just locks down your
test to the quirks of the current implementation. Only override visible methods.
This rule also prohibits exposing internal methods just to override them in a test.
If you can’t get to the structure you need, then the tests are telling you that it’s
time to break up the class into smaller, composable features.
Don’t Mock Values
There’s no point in writing mocks for values (which should be immutable any-
way). Just create an instance and use it. For example, in this test Video holds
details of a part of a show:
@Test public void sumsTotalRunningTime() {
  Show show = new Show();
  Video video1 = context.mock(Video.class); // Don't do this
  Video video2 = context.mock(Video.class);
  context.checking(new Expectations(){{
    one(video1).time(); will(returnValue(40));
    one(video2).time(); will(returnValue(23));
  }});
  show.add(video1);
  show.add(video2);
  assertEqual(63, show.runningTime())
}
237
Don’t Mock Values



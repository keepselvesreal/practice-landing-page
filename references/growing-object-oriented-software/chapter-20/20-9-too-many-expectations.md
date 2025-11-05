# 20.9 Too Many Expectations (pp.242-244)

---
**Page 242**

It turns out that track is the only dependency of a RacingCar; the hint is that
it’s the only ﬁeld that’s ﬁnal. The listener is a notiﬁcation, and everything else
is an adjustment; all of these can be modiﬁed by the user before or during the
race. Here’s a reworked constructor:
public class RacingCar {
  private final Track track;
  private DrivingStrategy driver = DriverTypes.borderlineAggressiveDriving();
  private Tyres tyres = TyreTypes.mediumSlicks();
  private Suspension suspension = SuspensionTypes.mediumStiffness();
  private Wing frontWing = WingTypes.mediumDownforce();
  private Wing backWing = WingTypes.mediumDownforce();
  private double fuelLoad = 0.5;
  private CarListener listener = CarListener.NONE;
  public RacingCar(Track track) {
    this.track = track;
  }
  public void setSuspension(Suspension suspension) { […]
  public void setTyres(Tyres tyres) { […]
  public void setEngine(Engine engine) { […]
  public void setListener(CarListener listener) { […]
}
Now we’ve initialized these peers to common defaults; the user can conﬁgure
them later through the user interface, and we can conﬁgure them in our unit tests.
We’ve initialized the listener to a null object, again this can be changed later
by the object’s environment.
Too Many Expectations
When a test has too many expectations, it’s hard to see what’s important and
what’s really under test. For example, here’s a test:
@Test public void 
decidesCasesWhenFirstPartyIsReady() {
  context.checking(new Expectations(){{
    one(firstPart).isReady(); will(returnValue(true));
    one(organizer).getAdjudicator(); will(returnValue(adjudicator));
    one(adjudicator).findCase(firstParty, issue); will(returnValue(case));
    one(thirdParty).proceedWith(case);
  }});
  claimsProcessor.adjudicateIfReady(thirdParty, issue);
}
that might be implemented like this:
Chapter 20
Listening to the Tests
242


---
**Page 243**

public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    Adjudicator adjudicator = organization.getAdjudicator();
    Case case = adjudicator.findCase(firstParty, issue);
    thirdParty.proceedWith(case);
  } else{
    thirdParty.adjourn();
  }
}
What makes the test hard to read is that everything is an expectation, so every-
thing looks equally important. We can’t tell what’s signiﬁcant and what’s just
there to get through the test.
In fact, if we look at all the methods we call, there are only two that
have any side effects outside this class: thirdParty.proceedWith() and
thirdParty.adjourn(); it would be an error to call these more than once. All the
other methods are queries; we can call organization.getAdjudicator() repeat-
edly without breaking any behavior. adjudicator.findCase() might go either
way, but it happens to be a lookup so it has no side effects.
We can make our intentions clearer by distinguishing between stubs, simulations
of real behavior that help us get the test to pass, and expectations, assertions we
want to make about how an object interacts with its neighbors. There’s a longer
discussion of this distinction in “Allowances and Expectations” (page 277).
Reworking the test, we get:
@Test public void decidesCasesWhenFirstPartyIsReady() {
  context.checking(new Expectations(){{
allowing(firstPart).isReady(); will(returnValue(true));
allowing(organizer).getAdjudicator(); will(returnValue(adjudicator));
allowing(adjudicator).findCase(firstParty, issue); will(returnValue(case));
    one(thirdParty).proceedWith(case);
  }});
  claimsProcessor.adjudicateIfReady(thirdParty, issue);
}
which is more explicit about how we expect the object to change the world
around it.
Write Few Expectations
A colleague, Romilly Cocking, when he ﬁrst started working with us, was surprised
by how few expectations we usually write in a unit test. Just like “everyone” has
now learned to avoid too many assertions in a test, we try to avoid too many
expectations. If we have more than a few, then either we’re trying to test too large
a unit, or we’re locking down too many of the object’s interactions.
243
Too Many Expectations


---
**Page 244**

Special Bonus Prize
We always have problems coming up with good examples. There’s actually a
better improvement to this code, which is to notice that we’ve pulled out a chain
of objects to get to the case object, exposing dependencies that aren’t relevant
here. Instead, we should have told the nearest object to do the work for us,
like this:
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
organization.adjudicateBetween(firstParty, thirdParty, issue);
  } else {
    thirdParty.adjourn();
  }
}
or, possibly,
public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
  if (firstParty.isReady()) {
    thirdParty.startAdjudication(organization, firstParty, issue);
  } else{
    thirdParty.adjourn();
  }
}
which looks more balanced. If you spotted this, we award you a Moment of
Smugness™ to be exercised at your convenience.
What the Tests Will Tell Us (If We’re Listening)
We’ve found these beneﬁts from learning to listen to test smells:
Keep knowledge local
Some of the test smells we’ve identiﬁed, such as needing “magic” to create
mocks, are to do with knowledge leaking between components. If we can
keep knowledge local to an object (either internal or passed in), then its im-
plementation is independent of its context; we can safely move it wherever
we like. Do this consistently and your application, built out of pluggable
components, will be easy to change.
If it’s explicit, we can name it
One reason why we don’t like mocking concrete classes is that we like to
have names for the relationships between objects as well the objects them-
selves. As the legends say, if we have something’s true name, we can control
it. If we can see it, we have a better chance of ﬁnding its other uses and so
reducing duplication.
Chapter 20
Listening to the Tests
244



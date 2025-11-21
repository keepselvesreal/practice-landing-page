# 20.8 Too Many Dependencies (pp.241-242)

---
**Page 241**

put up with these compromises in a handset because we don’t have enough
pockets for all the devices it includes, but that doesn’t apply to code. This class
should be broken up; Michael Feathers describes some techniques for doing so
in Chapter 20 of [Feathers04].
An associated smell for this kind of class is that its test suite will look confused
too. The tests for its various features will have no relationship with each other,
so we’ll be able to make major changes in one area without touching others. If
we can break up the test class into slices that don’t share anything, it might be
best to go ahead and slice up the object too.
Too Many Dependencies
A third diagnosis for a bloated constructor might be that not all of the arguments
are dependencies, one of the peer stereotypes we deﬁned in “Object Peer
Stereotypes” (page 52). As discussed in that section, we insist on dependencies
being passed in to the constructor, but notiﬁcations and adjustments can be set
to defaults and reconﬁgured later. When a constructor is too large, and we don’t
believe there’s an implicit new type amongst the arguments, we can use more
default values and only overwrite them for particular test cases.
Here’s an example—it’s not quite bad enough to need ﬁxing, but it’ll do to
make the point. The application is a racing game; players can try out different
conﬁgurations of car and driving style to see which one wins.1 A RacingCar
represents a competitor within a race:
public class RacingCar {
  private final Track track;
  private Tyres tyres;
  private Suspension suspension;
  private Wing frontWing;
  private Wing backWing;
  private double fuelLoad;
  private CarListener listener;
  private DrivingStrategy driver;
  public RacingCar(Track track, DrivingStrategy driver, Tyres tyres, 
                  Suspension suspension, Wing frontWing, Wing backWing, 
                  double fuelLoad, CarListener listener)
  {
    this.track = track;
    this.driver = driver;
    this.tyres = tyres;
    this.suspension = suspension;
    this.frontWing = frontWing;
    this.backWing = backWing;
    this.fuelLoad = fuelLoad;
    this.listener = listener;
  }
}
1. Nat once worked in a job that involved following the Formula One circuit.
241
Too Many Dependencies


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



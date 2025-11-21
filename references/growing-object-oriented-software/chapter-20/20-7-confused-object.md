# 20.7 Confused Object (pp.240-241)

---
**Page 240**

messageProcessor = 
  new MessageProcessor(new XmlMessageUnpacker(), 
                       auditor, counterpartyFinder, 
                       locationFinder, domesticNotifier,
                       importedNotifier);
to this:
messageProcessor = 
  new MessageProcessor(new XmlMessageUnpacker(counterpartyFinder),
                       auditor,
new MessageDispatcher(
                         locationFinder, 
                         domesticNotifier, importedNotifier));
Later we can reduce the syntax noise by extracting out the creation of the
MessageDispatcher.
Confused Object
Another diagnosis for a “bloated constructor” might be that the object itself is
too large because it has too many responsibilities. For example,
public class Handset {
  public Handset(Network network, Camera camera, Display display, 
                DataNetwork dataNetwork, AddressBook addressBook,
                Storage storage, Tuner tuner, …)
  {
// set the fields here
  }
  public void placeCallTo(DirectoryNumber number) { 
    network.openVoiceCallTo(number);
  }
  public void takePicture() { 
    Frame frame = storage.allocateNewFrame();
    camera.takePictureInto(frame);
    display.showPicture(frame);
  }
  public void showWebPage(URL url) {
    display.renderHtml(dataNetwork.retrievePage(url));
  }
  public void showAddress(SearchTerm searchTerm) {
    display.showAddress(addressBook.findAddress(searchTerm));
  } 
  public void playRadio(Frequency frequency) {
    tuner.tuneTo(frequency);
    tuner.play();
  }
// and so on
}
Like our mobile phones, this class has several unrelated responsibilities which
force it to pull in many dependencies. And, like our phones, the class is confusing
to use because unrelated features interfere with each other. We’re prepared to
Chapter 20
Listening to the Tests
240


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



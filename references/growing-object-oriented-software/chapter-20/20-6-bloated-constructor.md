# 20.6 Bloated Constructor (pp.238-240)

---
**Page 238**

Here, it’s not worth creating an interface/implementation pair to control which
time values are returned; just create instances with the appropriate times and
use them.
There are a couple of heuristics for when a class is likely to be a value and so
not worth mocking. First, its values are immutable—although that might also
mean that it’s an adjustment object, as described in “Object Peer Stereotypes”
(page 52). Second, we can’t think of a meaningful name for a class that would
implement an interface for the type. If Video were an interface, what would we
call its class other than VideoImpl or something equally vague? We discuss class
naming in “Impl Classes Are Meaningless” on page 63.
If you’re tempted to mock a value because it’s too complicated to set up an
instance, consider writing a builder; see Chapter 22.
Bloated Constructor
Sometimes during the TDD process, we end up with a constructor that has a
long, unwieldy list of arguments. We most likely got there by adding the object’s
dependencies one at a time, and it got out of hand. This is not dreadful, since
the process helped us sort out the design of the class and its neighbors, but now
it’s time to clean up. We will still need the functionality that depends on all the
current constructor arguments, so we should see if there’s any implicit structure
there that we can tease out.
One possibility is that some of the arguments together deﬁne a concept that
should be packaged up and replaced with a new object to represent it. Here’s a
small example:
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker, 
                          AuditTrail auditor, 
                          CounterPartyFinder counterpartyFinder,
                          LocationFinder locationFinder,
                          DomesticNotifier domesticNotifier,
                          ImportedNotifier importedNotifier) 
  {
// set the fields here
  }
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage, counterpartyFinder);
    auditor.recordReceiptOf(unpacked);
// some other activity here
    if (locationFinder.isDomestic(unpacked)) {
      domesticNotifier.notify(unpacked.asDomesticMessage());
    } else {
      importedNotifier.notify(unpacked.asImportedMessage())
    }
  }
}
Chapter 20
Listening to the Tests
238


---
**Page 239**

Just the thought of writing expectations for all these objects makes us wilt,
which suggests that things are too complicated. A ﬁrst step is to notice that the
unpacker and counterpartyFinder are always used together—they’re ﬁxed at
construction and one calls the other. We can remove one argument by pushing
the counterpartyFinder into the unpacker.
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker, 
                          AuditTrail auditor, 
                          LocationFinder locationFinder,
                          DomesticNotifier domesticNotifier,
                          ImportedNotifier importedNotifier) { […]
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage);
// etc.
  }
Then there’s the triple of locationFinder and the two notiﬁers, which seem
to go together. It might make sense to package them into a MessageDispatcher.
public class MessageProcessor {
  public MessageProcessor(MessageUnpacker unpacker, 
                          AuditTrail auditor, 
MessageDispatcher dispatcher) { […]
  public void onMessage(Message rawMessage) {
    UnpackedMessage unpacked = unpacker.unpack(rawMessage);
    auditor.recordReceiptOf(unpacked);
// some other activity here
dispatcher.dispatch(unpacked);
  }
}
Although we’ve forced this example to ﬁt within a section, it shows that being
sensitive to complexity in the tests can help us clarify our designs. Now we have
a message handling object that clearly performs the usual three stages:
receive, process, and forward. We’ve pulled out the message routing code (the
MessageDispatcher), so the MessageProcessor has fewer responsibilities and we
know where to put routing decisions when things get more complicated. You
might also notice that this code is easier to unit-test.
When extracting implicit components, we start by looking for two conditions:
arguments that are always used together in the class, and those that have the
same lifetime. Once we’ve found a coincidence, we have the harder task of ﬁnding
a good name that explains the concept.
As an aside, one sign that a design is developing nicely is that this kind of
change is easy to integrate. All we have to do is ﬁnd where the MessageProcessor
is created and change this:
239
Bloated Constructor


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



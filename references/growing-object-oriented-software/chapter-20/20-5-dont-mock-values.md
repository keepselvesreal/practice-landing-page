# 20.5 Don't Mock Values (pp.237-238)

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



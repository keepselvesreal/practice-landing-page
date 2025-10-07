Line 1: 
Line 2: --- 페이지 254 ---
Line 3: Chapter 20
Line 4: Listening to the Tests
Line 5: You can see a lot just by observing.
Line 6: —Yogi Berra
Line 7: Introduction
Line 8: Sometimes we ﬁnd it difﬁcult to write a test for some functionality we want to
Line 9: add to our code. In our experience, this usually means that our design can be
Line 10: improved—perhaps the class is too tightly coupled to its environment or does
Line 11: not have clear responsibilities. When this happens, we ﬁrst check whether it’s an
Line 12: opportunity to improve our code, before working around the design by making
Line 13: the test more complicated or using more sophisticated tools. We’ve found
Line 14: that the qualities that make an object easy to test also make our code responsive
Line 15: to change.
Line 16: The trick is to let our tests drive our design (that’s why it’s called test-driven
Line 17: development). TDD is about testing code, verifying its externally visible qualities
Line 18: such as functionality and performance. TDD is also about feedback on the code’s
Line 19: internal qualities: the coupling and cohesion of its classes, dependencies that are
Line 20: explicit or hidden, and effective information hiding—the qualities that keep the
Line 21: code maintainable.
Line 22: With practice, we’ve become more sensitive to the rough edges in our tests, so
Line 23: we can use them for rapid feedback about the design. Now when we ﬁnd a feature
Line 24: that’s difﬁcult to test, we don’t just ask ourselves how to test it, but also why is
Line 25: it difﬁcult to test.
Line 26: In this chapter, we look at some common “test smells” that we’ve encountered
Line 27: and discuss what they might imply about the design of the code. There are two
Line 28: categories of test smell to consider. One is where the test itself is not well
Line 29: written—it may be unclear or brittle. Meszaros [Meszaros07] covers several such
Line 30: patterns in his “Test Smells” chapter. This chapter is concerned with the other
Line 31: category, where a test is highlighting that the target code is the problem. Meszaros
Line 32: has one pattern for this, called “Hard-to-Test Code.” We’ve picked out some
Line 33: common cases that we’ve seen that are relevant to our approach to TDD.
Line 34: 229
Line 35: 
Line 36: --- 페이지 255 ---
Line 37: I Need to Mock an Object I Can’t Replace (without Magic)
Line 38: Singletons Are Dependencies
Line 39: One interpretation of reducing complexity in code is making commonly useful
Line 40: objects accessible through a global structure, usually implemented as a singleton.
Line 41: Any code that needs access to a feature can just refer to it by its global name
Line 42: instead of receiving it as an argument. Here’s a common example:
Line 43: Date now = new Date();
Line 44: Under the covers, the constructor calls the singleton System and sets the new
Line 45: instance to the current time using System.currentTimeMillis(). This is a conve-
Line 46: nient technique, but it comes at a cost. Let’s say we want to write a test like this:
Line 47: @Test public void rejectsRequestsNotWithinTheSameDay() {
Line 48:   receiver.acceptRequest(FIRST_REQUEST);
Line 49: // the next day
Line 50:   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line 51: }
Line 52: The implementation looks like this:
Line 53: public boolean acceptRequest(Request request) {
Line 54:   final Date now = new Date();
Line 55:   if (dateOfFirstRequest == null) {
Line 56:     dateOfFirstRequest = now;
Line 57:    } else if (firstDateIsDifferentFrom(now)) {
Line 58:     return false;
Line 59:   }
Line 60: // process the request
Line 61:   return true;
Line 62: }
Line 63: where dateOfFirstRequest is a ﬁeld and firstDateIsDifferentFrom() is a helper
Line 64: method that hides the unpleasantness of working with the Java date library.
Line 65: To test this timeout, we must either make the test wait overnight or do some-
Line 66: thing clever (perhaps with aspects or byte-code manipulation) to intercept the
Line 67: constructor and return suitable Date values for the test. This difﬁculty in testing
Line 68: is a hint that we should change the code. To make the test easier, we need to
Line 69: control how Date objects are created, so we introduce a Clock and pass it into
Line 70: the Receiver. If we stub Clock, the test might look like this:
Line 71: @Test public void rejectsRequestsNotWithinTheSameDay() {
Line 72:   Receiver receiver = new Receiver(stubClock);
Line 73:   stubClock.setNextDate(TODAY);
Line 74:   receiver.acceptRequest(FIRST_REQUEST);
Line 75:   stubClock.setNextDate(TOMORROW);
Line 76:   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line 77: }
Line 78: Chapter 20
Line 79: Listening to the Tests
Line 80: 230
Line 81: 
Line 82: --- 페이지 256 ---
Line 83: and the implementation like this:
Line 84: public boolean acceptRequest(Request request) {
Line 85:   final Date now = clock.now();
Line 86:   if (dateOfFirstRequest == null) {
Line 87:    dateOfFirstRequest = now;
Line 88:   } else if (firstDateIsDifferentFrom(now)) {
Line 89:    return false;
Line 90:   }
Line 91: // process the request
Line 92:   return true;
Line 93: }
Line 94: Now we can test the Receiver without any special tricks. More importantly,
Line 95: however, we’ve made it obvious that Receiver is dependent on time—we can’t
Line 96: even create one without a Clock. Some argue that this is breaking encapsulation
Line 97: by exposing the internals of a Receiver—we should be able to just create an in-
Line 98: stance and not worry—but we’ve seen so many systems that are impossible to
Line 99: test because the developers did not isolate the concept of time. We want to know
Line 100: about this dependency, especially when the service is rolled out across the world,
Line 101: and New York and London start complaining about different results.
Line 102: From Procedures to Objects
Line 103: Having taken the trouble to introduce a Clock object, we start wondering if our
Line 104: code is missing a concept: date checking in terms of our domain. A Receiver
Line 105: doesn’t need to know all the details of a calendar system, such as time zones and
Line 106: locales; it just need to know if the date has changed for this application. There’s
Line 107: a clue in the fragment:
Line 108: firstDateIsDifferentFrom(now)
Line 109: which means that we’ve had to wrap up some date manipulation code in Receiver.
Line 110: It’s the wrong object; that kind of work should be done in Clock. We write the
Line 111: test again:
Line 112: @Test public void rejectsRequestsNotWithinTheSameDay() {
Line 113:   Receiver receiver = new Receiver(clock);
Line 114:   context.checking(new Expectations() {{
Line 115:    allowing(clock).now(); will(returnValue(NOW));
Line 116: one(clock).dayHasChangedFrom(NOW); will(returnValue(false));
Line 117:   }});
Line 118:   receiver.acceptRequest(FIRST_REQUEST);
Line 119:   assertFalse("too late now", receiver.acceptRequest(SECOND_REQUEST));
Line 120: }
Line 121: The implementation looks like this:
Line 122: 231
Line 123: I Need to Mock an Object I Can’t Replace (without Magic)
Line 124: 
Line 125: --- 페이지 257 ---
Line 126: public boolean acceptRequest(Request request) {
Line 127:   if (dateOfFirstRequest == null) {
Line 128:    dateOfFirstRequest = clock.now();
Line 129:   } else if (clock.dayHasChangedFrom(dateOfFirstRequest)) {
Line 130:    return false;
Line 131:   }
Line 132: // process the request
Line 133:   return true;
Line 134: }
Line 135: This version of Receiver is more focused: it doesn’t need to know how to dis-
Line 136: tinguish one date from another and it only needs to get a date to set the ﬁrst
Line 137: value. The Clock interface deﬁnes exactly those date services Receiver needs from
Line 138: its environment.
Line 139: But we think we can push this further. Receiver only retains a date so that it
Line 140: can detect a change of day; perhaps we should delegate all the date functionality
Line 141: to another object which, for want of a better name, we’ll call a SameDayChecker.
Line 142: @Test public void rejectsRequestsOutsideAllowedPeriod() {
Line 143:   Receiver receiver = new Receiver(sameDayChecker);
Line 144:   context.checking(new Expectations() {{
Line 145: allowing(sameDayChecker).hasExpired(); will(returnValue(false));
Line 146:   }});
Line 147:   assertFalse("too late now", receiver.acceptRequest(REQUEST));
Line 148: }
Line 149: with an implementation like this:
Line 150: public boolean acceptRequest(Request request) {
Line 151:   if (sameDayChecker.hasExpired()) {
Line 152:    return false;
Line 153:   }
Line 154: // process the request
Line 155:   return true;
Line 156: }
Line 157: All the logic about dates has been separated out from Receiver, which can
Line 158: concentrate on processing the request. With two objects, we can make sure that
Line 159: each behavior (date checking and request processing) is unit-tested cleanly.
Line 160: Implicit Dependencies Are Still Dependencies
Line 161: We can hide a dependency from the caller of a component by using a global
Line 162: value to bypass encapsulation, but that doesn’t make the dependency go away—it
Line 163: just makes it inaccessible. For example, Steve once had to work with a Microsoft
Line 164: .Net library that couldn’t be loaded without installing ActiveDirectory—which
Line 165: wasn’t actually required for the features he wanted to use and which he couldn’t
Line 166: install on his machine anyway. The library developer was trying to be helpful
Line 167: and to make it “just work,” but the result was that Steve couldn’t get it to work
Line 168: at all.
Line 169: Chapter 20
Line 170: Listening to the Tests
Line 171: 232
Line 172: 
Line 173: --- 페이지 258 ---
Line 174: One goal of object orientation as a technique for structuring code is to make
Line 175: the boundaries of an object clearly visible. An object should only deal with values
Line 176: and instances that are either local—created and managed within its scope—or
Line 177: passed in explicitly, as we emphasized in “Context Independence” (page 54).
Line 178: In the example above, the act of making date checking testable forced us to
Line 179: make the Receiver’s requirements more explicit and to think more clearly about
Line 180: the domain.
Line 181: Use the Same Techniques to Break Dependencies in Unit Tests
Line 182: as in Production Code
Line 183: There are several frameworks available that use techniques such as manipulating
Line 184: class loaders or bytecodes to allow unit tests to break dependencies without
Line 185: changing the target code. As a rule, these are advanced techniques that most
Line 186: developers would not use when writing production code. Sometimes these tools
Line 187: really are necessary, but developers should be aware that they come with a
Line 188: hidden cost.
Line 189: Unit-testing tools that let the programmer sidestep poor dependency management
Line 190: in the design waste a valuable source of feedback.When the developers eventually
Line 191: do need to address these design weaknesses to add some urgent feature, they
Line 192: will ﬁnd it harder to do. The poor structure will have inﬂuenced other parts of the
Line 193: system that rely on it, and any understanding of the original intent will have
Line 194: evaporated. As with dirty pots and pans, it’s easier to get the grease off before it’s
Line 195: been baked in.
Line 196: Logging Is a Feature
Line 197: We have a more contentious example of working with objects that are hard to
Line 198: replace: logging. Take a look at these two lines of code:
Line 199: log.error("Lost touch with Reality after " + timeout + "seconds");
Line 200: log.trace("Distance traveled in the wilderness: " + distance);
Line 201: These are two separate features that happen to share an implementation. Let
Line 202: us explain.
Line 203: •
Line 204: Support logging (errors and info) is part of the user interface of the appli-
Line 205: cation. These messages are intended to be tracked by support staff, as well
Line 206: as perhaps system administrators and operators, to diagnose a failure or
Line 207: monitor the progress of the running system.
Line 208: •
Line 209: Diagnostic logging (debug and trace) is infrastructure for programmers.
Line 210: These messages should not be turned on in production because they’re in-
Line 211: tended to help the programmers understand what’s going on inside the
Line 212: system they’re developing.
Line 213: 233
Line 214: Logging Is a Feature
Line 215: 
Line 216: --- 페이지 259 ---
Line 217: Given this distinction, we should consider using different techniques for these
Line 218: two type of logging. Support logging should be test-driven from somebody’s re-
Line 219: quirements, such as auditing or failure recovery. The tests will make sure we’ve
Line 220: thought about what each message is for and made sure it works. The tests will
Line 221: also protect us from breaking any tools and scripts that other people write to
Line 222: analyze these log messages. Diagnostic logging, on the other hand, is driven by
Line 223: the programmers’ need for ﬁne-grained tracking of what’s happening in the sys-
Line 224: tem. It’s scaffolding—so it probably doesn’t need to be test-driven and the mes-
Line 225: sages might not need to be as consistent as those for support logs. After all, didn’t
Line 226: we just agree that these messages are not to be used in production?
Line 227: Notiﬁcation Rather Than Logging
Line 228: To get back to the point of the chapter, writing unit tests against static global
Line 229: objects, including loggers, is clumsy. We have to either read from the ﬁle system
Line 230: or manage an extra appender object for testing; we have to remember to clean
Line 231: up afterwards so that tests don’t interfere with each other and set the right level
Line 232: on the right logger. The noise in the test reminds us that our code is working at
Line 233: two levels: our domain and the logging infrastructure. Here’s a common example
Line 234: of code with logging:
Line 235: Location location = tracker.getCurrentLocation();
Line 236: for (Filter filter : filters) {
Line 237:   filter.selectFor(location);
Line 238: if (logger.isInfoEnabled()) {
Line 239:     logger.info("Filter " + filter.getName() + ", " + filter.getDate()
Line 240:                  + " selected for " + location.getName() 
Line 241:                  + ", is current: " + tracker.isCurrent(location));
Line 242:   }
Line 243: }
Line 244: Notice the shift in vocabulary and style between the functional part of the
Line 245: loop and the (emphasized) logging part. The code is doing two things at
Line 246: once—something to do with locations and rendering support information—which
Line 247: breaks the single responsibility principle. Maybe we could do this instead:
Line 248: Location location = tracker.getCurrentLocation();
Line 249: for (Filter filter : filters) {
Line 250:   filter.selectFor(location);
Line 251: support.notifyFiltering(tracker, location, filter);}
Line 252: where the support object might be implemented by a logger, a message bus,
Line 253: pop-up windows, or whatever’s appropriate; this detail is not relevant to the
Line 254: code at this level.
Line 255: This code is also easier to test, as you saw in Chapter 19. We, not the logging
Line 256: framework, own the support object, so we can pass in a mock implementation
Line 257: at our convenience and keep it local to the test case. The other simpliﬁcation is
Line 258: that now we’re testing for objects, rather than formatted contents of a string. Of
Line 259: Chapter 20
Line 260: Listening to the Tests
Line 261: 234
Line 262: 
Line 263: --- 페이지 260 ---
Line 264: course, we will still need to write an implementation of support and some focused
Line 265: integration tests to go with it.
Line 266: But That’s Crazy Talk…
Line 267: The idea of encapsulating support reporting sounds like over-design, but it’s
Line 268: worth thinking about for a moment. It means we’re writing code in terms of our
Line 269: intent (helping the support people) rather than implementation (logging), so it’s
Line 270: more expressive. All the support reporting is handled in a few known places, so
Line 271: it’s easier to be consistent about how things are reported and to encourage reuse.
Line 272: It can also help us structure and control our reporting in terms of the application
Line 273: domain, rather than in terms of Java packages. Finally, the act of writing a test
Line 274: for each report helps us avoid the “I don’t know what to do with this exception,
Line 275: so I’ll log it and carry on” syndrome, which leads to log bloat and production
Line 276: failures because we haven’t handled obscure error conditions.
Line 277: One objection we’ve heard is, “I can’t pass in a logger for testing because I’ve
Line 278: got logging all over my domain objects. I’d have to pass one around everywhere.”
Line 279: We think this is a test smell that is telling us that we haven’t clariﬁed our design
Line 280: enough. Perhaps some of our support logging should really be diagnostic logging,
Line 281: or we’re logging more than we need because of something that we wrote when
Line 282: we hadn’t yet understood the behavior. Most likely, there’s still too much dupli-
Line 283: cation in our domain code and we haven’t yet found the “choke points” where
Line 284: most of the production logging should go.
Line 285: So what about diagnostic logging? Is it disposable scaffolding that should be
Line 286: taken down once the job is done, or essential infrastructure that should be tested
Line 287: and maintained? That depends on the system, but once we’ve made the distinction
Line 288: we have more freedom to think about using different techniques for support and
Line 289: diagnostic logging. We might even decide that in-line code is the wrong technique
Line 290: for diagnostic logging because it interferes with the readability of the production
Line 291: code that matters. Perhaps we could weave in some aspects instead (since that’s
Line 292: the canonical example of their use); perhaps not—but at least we’ve now
Line 293: clariﬁed the choice.
Line 294: One ﬁnal data point. One of us once worked on a system where so much
Line 295: content was written to the logs that they had to be deleted after a week to ﬁt on
Line 296: the disks. This made maintenance very difﬁcult as the relevant logs were usually
Line 297: gone by the time a bug was assigned to be ﬁxed. If they’d logged nothing at all,
Line 298: the system would have run faster with no loss of useful information.
Line 299: Mocking Concrete Classes
Line 300: One approach to interaction testing is to mock concrete classes rather than inter-
Line 301: faces. The technique is to inherit from the class you want to mock and override
Line 302: the methods that will be called within the test, either manually or with any of
Line 303: 235
Line 304: Mocking Concrete Classes
Line 305: 
Line 306: --- 페이지 261 ---
Line 307: the mocking frameworks. We think this is a technique that should be used only
Line 308: when you really have no other options.
Line 309: Here’s an example of mocking by hand. The test veriﬁes that the music centre
Line 310: starts the CD player at the requested time. Assume that setting the schedule on
Line 311: a CdPlayer object involves triggering some behavior we don’t want in the test,
Line 312: so we override scheduleToStartAt() and verify afterwards that we’ve called it
Line 313: with the right argument.
Line 314: public class MusicCentreTest {
Line 315:   @Test public void 
Line 316: startsCdPlayerAtTimeRequested() {
Line 317:     final MutableTime scheduledTime = new MutableTime();
Line 318:     CdPlayer player = new CdPlayer() {
Line 319:       @Override public void scheduleToStartAt(Time startTime) {
Line 320:         scheduledTime.set(startTime);
Line 321:       }
Line 322:     }
Line 323:     MusicCentre centre = new MusicCentre(player);
Line 324:     centre.startMediaAt(LATER);
Line 325:     assertEquals(LATER, scheduledTime.get());
Line 326:   }
Line 327: }
Line 328: The problem with this approach is that it leaves the relationship between the
Line 329: CdPlayer and MusicCentre implicit. We hope we’ve made clear by now that our
Line 330: intention in test-driven development is to use mock objects to bring out relation-
Line 331: ships between objects. If we subclass, there’s nothing in the domain code to make
Line 332: such a relationship visible—just methods on an object. This makes it harder to
Line 333: see if the service that supports this relationship might be relevant elsewhere, and
Line 334: we’ll have to do the analysis again next time we work with the class. To make
Line 335: the point, here’s a possible implementation of CdPlayer:
Line 336: public class CdPlayer {
Line 337:   public void scheduleToStartAt(Time startTime) { […]
Line 338:   public void stop() { […]
Line 339:   public void gotoTrack(int trackNumber) { […]
Line 340:   public void spinUpDisk() { […]
Line 341:   public void eject() { […]
Line 342: }
Line 343: It turns out that our MusicCentre only uses the starting and stopping methods
Line 344: on the CdPlayer; the rest are used by some other part of the system. We would
Line 345: be overspecifying the MusicCentre by requiring it to talk to a CdPlayer; what it
Line 346: actually needs is a ScheduledDevice. Robert Martin made the point (back in
Line 347: 1996) in his Interface Segregation Principle that “Clients should not be forced
Line 348: to depend upon interfaces that they do not use,” but that’s exactly what we do
Line 349: when we mock a concrete class.
Line 350: Chapter 20
Line 351: Listening to the Tests
Line 352: 236
Line 353: 
Line 354: --- 페이지 262 ---
Line 355: There’s a more subtle but powerful reason for not mocking concrete classes.
Line 356: When we extract an interface as part of our test-driven development process, we
Line 357: have to think up a name to describe the relationship we’ve just discovered—in
Line 358: this example, the ScheduledDevice. We ﬁnd that this makes us think harder about
Line 359: the domain and teases out concepts that we might otherwise miss. Once something
Line 360: has a name, we can talk about it.
Line 361: “Break Glass in Case of Emergency”
Line 362: There are a few occasions when we have to put up with this smell. The least un-
Line 363: acceptable situation is where we’re working with legacy code that we control
Line 364: but can’t change all at once. Alternatively, we might be working with third-party
Line 365: code that we can’t change at all (see Chapter 8). We ﬁnd that it’s almost always
Line 366: better to write a veneer over an external library rather than mock it directly—but
Line 367: occasionally, it’s just not worth it. We broke the rule with Logger in Chapter 19
Line 368: but apologized a lot and felt bad about it. In any case, these are unfortunate but
Line 369: necessary compromises that we would try to work our way out of when possible.
Line 370: The longer we leave them in the code, the more likely it is that some brittleness
Line 371: in the design will cause us grief.
Line 372: Above all, do not override a class’ internal features—this just locks down your
Line 373: test to the quirks of the current implementation. Only override visible methods.
Line 374: This rule also prohibits exposing internal methods just to override them in a test.
Line 375: If you can’t get to the structure you need, then the tests are telling you that it’s
Line 376: time to break up the class into smaller, composable features.
Line 377: Don’t Mock Values
Line 378: There’s no point in writing mocks for values (which should be immutable any-
Line 379: way). Just create an instance and use it. For example, in this test Video holds
Line 380: details of a part of a show:
Line 381: @Test public void sumsTotalRunningTime() {
Line 382:   Show show = new Show();
Line 383:   Video video1 = context.mock(Video.class); // Don't do this
Line 384:   Video video2 = context.mock(Video.class);
Line 385:   context.checking(new Expectations(){{
Line 386:     one(video1).time(); will(returnValue(40));
Line 387:     one(video2).time(); will(returnValue(23));
Line 388:   }});
Line 389:   show.add(video1);
Line 390:   show.add(video2);
Line 391:   assertEqual(63, show.runningTime())
Line 392: }
Line 393: 237
Line 394: Don’t Mock Values
Line 395: 
Line 396: --- 페이지 263 ---
Line 397: Here, it’s not worth creating an interface/implementation pair to control which
Line 398: time values are returned; just create instances with the appropriate times and
Line 399: use them.
Line 400: There are a couple of heuristics for when a class is likely to be a value and so
Line 401: not worth mocking. First, its values are immutable—although that might also
Line 402: mean that it’s an adjustment object, as described in “Object Peer Stereotypes”
Line 403: (page 52). Second, we can’t think of a meaningful name for a class that would
Line 404: implement an interface for the type. If Video were an interface, what would we
Line 405: call its class other than VideoImpl or something equally vague? We discuss class
Line 406: naming in “Impl Classes Are Meaningless” on page 63.
Line 407: If you’re tempted to mock a value because it’s too complicated to set up an
Line 408: instance, consider writing a builder; see Chapter 22.
Line 409: Bloated Constructor
Line 410: Sometimes during the TDD process, we end up with a constructor that has a
Line 411: long, unwieldy list of arguments. We most likely got there by adding the object’s
Line 412: dependencies one at a time, and it got out of hand. This is not dreadful, since
Line 413: the process helped us sort out the design of the class and its neighbors, but now
Line 414: it’s time to clean up. We will still need the functionality that depends on all the
Line 415: current constructor arguments, so we should see if there’s any implicit structure
Line 416: there that we can tease out.
Line 417: One possibility is that some of the arguments together deﬁne a concept that
Line 418: should be packaged up and replaced with a new object to represent it. Here’s a
Line 419: small example:
Line 420: public class MessageProcessor {
Line 421:   public MessageProcessor(MessageUnpacker unpacker, 
Line 422:                           AuditTrail auditor, 
Line 423:                           CounterPartyFinder counterpartyFinder,
Line 424:                           LocationFinder locationFinder,
Line 425:                           DomesticNotifier domesticNotifier,
Line 426:                           ImportedNotifier importedNotifier) 
Line 427:   {
Line 428: // set the fields here
Line 429:   }
Line 430:   public void onMessage(Message rawMessage) {
Line 431:     UnpackedMessage unpacked = unpacker.unpack(rawMessage, counterpartyFinder);
Line 432:     auditor.recordReceiptOf(unpacked);
Line 433: // some other activity here
Line 434:     if (locationFinder.isDomestic(unpacked)) {
Line 435:       domesticNotifier.notify(unpacked.asDomesticMessage());
Line 436:     } else {
Line 437:       importedNotifier.notify(unpacked.asImportedMessage())
Line 438:     }
Line 439:   }
Line 440: }
Line 441: Chapter 20
Line 442: Listening to the Tests
Line 443: 238
Line 444: 
Line 445: --- 페이지 264 ---
Line 446: Just the thought of writing expectations for all these objects makes us wilt,
Line 447: which suggests that things are too complicated. A ﬁrst step is to notice that the
Line 448: unpacker and counterpartyFinder are always used together—they’re ﬁxed at
Line 449: construction and one calls the other. We can remove one argument by pushing
Line 450: the counterpartyFinder into the unpacker.
Line 451: public class MessageProcessor {
Line 452:   public MessageProcessor(MessageUnpacker unpacker, 
Line 453:                           AuditTrail auditor, 
Line 454:                           LocationFinder locationFinder,
Line 455:                           DomesticNotifier domesticNotifier,
Line 456:                           ImportedNotifier importedNotifier) { […]
Line 457:   public void onMessage(Message rawMessage) {
Line 458:     UnpackedMessage unpacked = unpacker.unpack(rawMessage);
Line 459: // etc.
Line 460:   }
Line 461: Then there’s the triple of locationFinder and the two notiﬁers, which seem
Line 462: to go together. It might make sense to package them into a MessageDispatcher.
Line 463: public class MessageProcessor {
Line 464:   public MessageProcessor(MessageUnpacker unpacker, 
Line 465:                           AuditTrail auditor, 
Line 466: MessageDispatcher dispatcher) { […]
Line 467:   public void onMessage(Message rawMessage) {
Line 468:     UnpackedMessage unpacked = unpacker.unpack(rawMessage);
Line 469:     auditor.recordReceiptOf(unpacked);
Line 470: // some other activity here
Line 471: dispatcher.dispatch(unpacked);
Line 472:   }
Line 473: }
Line 474: Although we’ve forced this example to ﬁt within a section, it shows that being
Line 475: sensitive to complexity in the tests can help us clarify our designs. Now we have
Line 476: a message handling object that clearly performs the usual three stages:
Line 477: receive, process, and forward. We’ve pulled out the message routing code (the
Line 478: MessageDispatcher), so the MessageProcessor has fewer responsibilities and we
Line 479: know where to put routing decisions when things get more complicated. You
Line 480: might also notice that this code is easier to unit-test.
Line 481: When extracting implicit components, we start by looking for two conditions:
Line 482: arguments that are always used together in the class, and those that have the
Line 483: same lifetime. Once we’ve found a coincidence, we have the harder task of ﬁnding
Line 484: a good name that explains the concept.
Line 485: As an aside, one sign that a design is developing nicely is that this kind of
Line 486: change is easy to integrate. All we have to do is ﬁnd where the MessageProcessor
Line 487: is created and change this:
Line 488: 239
Line 489: Bloated Constructor
Line 490: 
Line 491: --- 페이지 265 ---
Line 492: messageProcessor = 
Line 493:   new MessageProcessor(new XmlMessageUnpacker(), 
Line 494:                        auditor, counterpartyFinder, 
Line 495:                        locationFinder, domesticNotifier,
Line 496:                        importedNotifier);
Line 497: to this:
Line 498: messageProcessor = 
Line 499:   new MessageProcessor(new XmlMessageUnpacker(counterpartyFinder),
Line 500:                        auditor,
Line 501: new MessageDispatcher(
Line 502:                          locationFinder, 
Line 503:                          domesticNotifier, importedNotifier));
Line 504: Later we can reduce the syntax noise by extracting out the creation of the
Line 505: MessageDispatcher.
Line 506: Confused Object
Line 507: Another diagnosis for a “bloated constructor” might be that the object itself is
Line 508: too large because it has too many responsibilities. For example,
Line 509: public class Handset {
Line 510:   public Handset(Network network, Camera camera, Display display, 
Line 511:                 DataNetwork dataNetwork, AddressBook addressBook,
Line 512:                 Storage storage, Tuner tuner, …)
Line 513:   {
Line 514: // set the fields here
Line 515:   }
Line 516:   public void placeCallTo(DirectoryNumber number) { 
Line 517:     network.openVoiceCallTo(number);
Line 518:   }
Line 519:   public void takePicture() { 
Line 520:     Frame frame = storage.allocateNewFrame();
Line 521:     camera.takePictureInto(frame);
Line 522:     display.showPicture(frame);
Line 523:   }
Line 524:   public void showWebPage(URL url) {
Line 525:     display.renderHtml(dataNetwork.retrievePage(url));
Line 526:   }
Line 527:   public void showAddress(SearchTerm searchTerm) {
Line 528:     display.showAddress(addressBook.findAddress(searchTerm));
Line 529:   } 
Line 530:   public void playRadio(Frequency frequency) {
Line 531:     tuner.tuneTo(frequency);
Line 532:     tuner.play();
Line 533:   }
Line 534: // and so on
Line 535: }
Line 536: Like our mobile phones, this class has several unrelated responsibilities which
Line 537: force it to pull in many dependencies. And, like our phones, the class is confusing
Line 538: to use because unrelated features interfere with each other. We’re prepared to
Line 539: Chapter 20
Line 540: Listening to the Tests
Line 541: 240
Line 542: 
Line 543: --- 페이지 266 ---
Line 544: put up with these compromises in a handset because we don’t have enough
Line 545: pockets for all the devices it includes, but that doesn’t apply to code. This class
Line 546: should be broken up; Michael Feathers describes some techniques for doing so
Line 547: in Chapter 20 of [Feathers04].
Line 548: An associated smell for this kind of class is that its test suite will look confused
Line 549: too. The tests for its various features will have no relationship with each other,
Line 550: so we’ll be able to make major changes in one area without touching others. If
Line 551: we can break up the test class into slices that don’t share anything, it might be
Line 552: best to go ahead and slice up the object too.
Line 553: Too Many Dependencies
Line 554: A third diagnosis for a bloated constructor might be that not all of the arguments
Line 555: are dependencies, one of the peer stereotypes we deﬁned in “Object Peer
Line 556: Stereotypes” (page 52). As discussed in that section, we insist on dependencies
Line 557: being passed in to the constructor, but notiﬁcations and adjustments can be set
Line 558: to defaults and reconﬁgured later. When a constructor is too large, and we don’t
Line 559: believe there’s an implicit new type amongst the arguments, we can use more
Line 560: default values and only overwrite them for particular test cases.
Line 561: Here’s an example—it’s not quite bad enough to need ﬁxing, but it’ll do to
Line 562: make the point. The application is a racing game; players can try out different
Line 563: conﬁgurations of car and driving style to see which one wins.1 A RacingCar
Line 564: represents a competitor within a race:
Line 565: public class RacingCar {
Line 566:   private final Track track;
Line 567:   private Tyres tyres;
Line 568:   private Suspension suspension;
Line 569:   private Wing frontWing;
Line 570:   private Wing backWing;
Line 571:   private double fuelLoad;
Line 572:   private CarListener listener;
Line 573:   private DrivingStrategy driver;
Line 574:   public RacingCar(Track track, DrivingStrategy driver, Tyres tyres, 
Line 575:                   Suspension suspension, Wing frontWing, Wing backWing, 
Line 576:                   double fuelLoad, CarListener listener)
Line 577:   {
Line 578:     this.track = track;
Line 579:     this.driver = driver;
Line 580:     this.tyres = tyres;
Line 581:     this.suspension = suspension;
Line 582:     this.frontWing = frontWing;
Line 583:     this.backWing = backWing;
Line 584:     this.fuelLoad = fuelLoad;
Line 585:     this.listener = listener;
Line 586:   }
Line 587: }
Line 588: 1. Nat once worked in a job that involved following the Formula One circuit.
Line 589: 241
Line 590: Too Many Dependencies
Line 591: 
Line 592: --- 페이지 267 ---
Line 593: It turns out that track is the only dependency of a RacingCar; the hint is that
Line 594: it’s the only ﬁeld that’s ﬁnal. The listener is a notiﬁcation, and everything else
Line 595: is an adjustment; all of these can be modiﬁed by the user before or during the
Line 596: race. Here’s a reworked constructor:
Line 597: public class RacingCar {
Line 598:   private final Track track;
Line 599:   private DrivingStrategy driver = DriverTypes.borderlineAggressiveDriving();
Line 600:   private Tyres tyres = TyreTypes.mediumSlicks();
Line 601:   private Suspension suspension = SuspensionTypes.mediumStiffness();
Line 602:   private Wing frontWing = WingTypes.mediumDownforce();
Line 603:   private Wing backWing = WingTypes.mediumDownforce();
Line 604:   private double fuelLoad = 0.5;
Line 605:   private CarListener listener = CarListener.NONE;
Line 606:   public RacingCar(Track track) {
Line 607:     this.track = track;
Line 608:   }
Line 609:   public void setSuspension(Suspension suspension) { […]
Line 610:   public void setTyres(Tyres tyres) { […]
Line 611:   public void setEngine(Engine engine) { […]
Line 612:   public void setListener(CarListener listener) { […]
Line 613: }
Line 614: Now we’ve initialized these peers to common defaults; the user can conﬁgure
Line 615: them later through the user interface, and we can conﬁgure them in our unit tests.
Line 616: We’ve initialized the listener to a null object, again this can be changed later
Line 617: by the object’s environment.
Line 618: Too Many Expectations
Line 619: When a test has too many expectations, it’s hard to see what’s important and
Line 620: what’s really under test. For example, here’s a test:
Line 621: @Test public void 
Line 622: decidesCasesWhenFirstPartyIsReady() {
Line 623:   context.checking(new Expectations(){{
Line 624:     one(firstPart).isReady(); will(returnValue(true));
Line 625:     one(organizer).getAdjudicator(); will(returnValue(adjudicator));
Line 626:     one(adjudicator).findCase(firstParty, issue); will(returnValue(case));
Line 627:     one(thirdParty).proceedWith(case);
Line 628:   }});
Line 629:   claimsProcessor.adjudicateIfReady(thirdParty, issue);
Line 630: }
Line 631: that might be implemented like this:
Line 632: Chapter 20
Line 633: Listening to the Tests
Line 634: 242
Line 635: 
Line 636: --- 페이지 268 ---
Line 637: public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line 638:   if (firstParty.isReady()) {
Line 639:     Adjudicator adjudicator = organization.getAdjudicator();
Line 640:     Case case = adjudicator.findCase(firstParty, issue);
Line 641:     thirdParty.proceedWith(case);
Line 642:   } else{
Line 643:     thirdParty.adjourn();
Line 644:   }
Line 645: }
Line 646: What makes the test hard to read is that everything is an expectation, so every-
Line 647: thing looks equally important. We can’t tell what’s signiﬁcant and what’s just
Line 648: there to get through the test.
Line 649: In fact, if we look at all the methods we call, there are only two that
Line 650: have any side effects outside this class: thirdParty.proceedWith() and
Line 651: thirdParty.adjourn(); it would be an error to call these more than once. All the
Line 652: other methods are queries; we can call organization.getAdjudicator() repeat-
Line 653: edly without breaking any behavior. adjudicator.findCase() might go either
Line 654: way, but it happens to be a lookup so it has no side effects.
Line 655: We can make our intentions clearer by distinguishing between stubs, simulations
Line 656: of real behavior that help us get the test to pass, and expectations, assertions we
Line 657: want to make about how an object interacts with its neighbors. There’s a longer
Line 658: discussion of this distinction in “Allowances and Expectations” (page 277).
Line 659: Reworking the test, we get:
Line 660: @Test public void decidesCasesWhenFirstPartyIsReady() {
Line 661:   context.checking(new Expectations(){{
Line 662: allowing(firstPart).isReady(); will(returnValue(true));
Line 663: allowing(organizer).getAdjudicator(); will(returnValue(adjudicator));
Line 664: allowing(adjudicator).findCase(firstParty, issue); will(returnValue(case));
Line 665:     one(thirdParty).proceedWith(case);
Line 666:   }});
Line 667:   claimsProcessor.adjudicateIfReady(thirdParty, issue);
Line 668: }
Line 669: which is more explicit about how we expect the object to change the world
Line 670: around it.
Line 671: Write Few Expectations
Line 672: A colleague, Romilly Cocking, when he ﬁrst started working with us, was surprised
Line 673: by how few expectations we usually write in a unit test. Just like “everyone” has
Line 674: now learned to avoid too many assertions in a test, we try to avoid too many
Line 675: expectations. If we have more than a few, then either we’re trying to test too large
Line 676: a unit, or we’re locking down too many of the object’s interactions.
Line 677: 243
Line 678: Too Many Expectations
Line 679: 
Line 680: --- 페이지 269 ---
Line 681: Special Bonus Prize
Line 682: We always have problems coming up with good examples. There’s actually a
Line 683: better improvement to this code, which is to notice that we’ve pulled out a chain
Line 684: of objects to get to the case object, exposing dependencies that aren’t relevant
Line 685: here. Instead, we should have told the nearest object to do the work for us,
Line 686: like this:
Line 687: public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line 688:   if (firstParty.isReady()) {
Line 689: organization.adjudicateBetween(firstParty, thirdParty, issue);
Line 690:   } else {
Line 691:     thirdParty.adjourn();
Line 692:   }
Line 693: }
Line 694: or, possibly,
Line 695: public void adjudicateIfReady(ThirdParty thirdParty, Issue issue) {
Line 696:   if (firstParty.isReady()) {
Line 697:     thirdParty.startAdjudication(organization, firstParty, issue);
Line 698:   } else{
Line 699:     thirdParty.adjourn();
Line 700:   }
Line 701: }
Line 702: which looks more balanced. If you spotted this, we award you a Moment of
Line 703: Smugness™ to be exercised at your convenience.
Line 704: What the Tests Will Tell Us (If We’re Listening)
Line 705: We’ve found these beneﬁts from learning to listen to test smells:
Line 706: Keep knowledge local
Line 707: Some of the test smells we’ve identiﬁed, such as needing “magic” to create
Line 708: mocks, are to do with knowledge leaking between components. If we can
Line 709: keep knowledge local to an object (either internal or passed in), then its im-
Line 710: plementation is independent of its context; we can safely move it wherever
Line 711: we like. Do this consistently and your application, built out of pluggable
Line 712: components, will be easy to change.
Line 713: If it’s explicit, we can name it
Line 714: One reason why we don’t like mocking concrete classes is that we like to
Line 715: have names for the relationships between objects as well the objects them-
Line 716: selves. As the legends say, if we have something’s true name, we can control
Line 717: it. If we can see it, we have a better chance of ﬁnding its other uses and so
Line 718: reducing duplication.
Line 719: Chapter 20
Line 720: Listening to the Tests
Line 721: 244
Line 722: 
Line 723: --- 페이지 270 ---
Line 724: More names mean more domain information
Line 725: We ﬁnd that when we emphasize how objects communicate, rather than
Line 726: what they are, we end up with types and roles deﬁned more in terms of the
Line 727: domain than of the implementation. This might be because we have a greater
Line 728: number of smaller abstractions, which gets us further away from the under-
Line 729: lying language. Somehow we seem to get more domain vocabulary into
Line 730: the code.
Line 731: Pass behavior rather than data
Line 732: We ﬁnd that by applying “Tell, Don’t Ask” consistently, we end up with a
Line 733: coding style where we tend to pass behavior (in the form of callbacks) into
Line 734: the system instead of pulling values up through the stack. For example, in
Line 735: Chapter 17, we introduced a SniperCollector that responds when told about
Line 736: a new Sniper. Passing this listener into the Sniper creation code gives us
Line 737: better information hiding than if we’d exposed a collection to be added
Line 738: to. More precise interfaces give us better information-hiding and clearer
Line 739: abstractions.
Line 740: We care about keeping the tests and code clean as we go, because it helps to
Line 741: ensure that we understand our domain and reduces the risk of being unable
Line 742: to cope when a new requirement triggers changes to the design. It’s much easier to
Line 743: keep a codebase clean than to recover from a mess. Once a codebase starts
Line 744: to “rot,” the developers will be under pressure to botch the code to get the next
Line 745: job done. It doesn’t take many such episodes to dissipate a team’s good intentions.
Line 746: We once had a posting to the jMock user list that included this comment:
Line 747: I was involved in a project recently where jMock was used quite heavily. Looking
Line 748: back, here’s what I found:
Line 749: 1.
Line 750: The unit tests were at times unreadable (no idea what they were doing).
Line 751: 2.
Line 752: Some tests classes would reach 500 lines in addition to inheriting an abstract
Line 753: class which also would have up to 500 lines.
Line 754: 3.
Line 755: Refactoring would lead to massive changes in test code.
Line 756: A unit test shouldn’t be 1000 lines long! It should focus on at most a few
Line 757: classes and should not need to create a large ﬁxture or perform lots of preparation
Line 758: just to get the objects into a state where the target feature can be exercised. Such
Line 759: tests are hard to understand—there’s just so much to remember when reading
Line 760: them. And, of course, they’re brittle, all the objects in play are too tightly coupled
Line 761: and too difﬁcult to set to the state the test requires.
Line 762: Test-driven development can be unforgiving. Poor quality tests can slow devel-
Line 763: opment to a crawl, and poor internal quality of the system being tested will result
Line 764: in poor quality tests. By being alert to the internal quality feedback we get from
Line 765: 245
Line 766: What the Tests Will Tell Us (If We’re Listening)
Line 767: 
Line 768: --- 페이지 271 ---
Line 769: writing tests, we can nip this problem in the bud, long before our unit tests ap-
Line 770: proach 1000 lines of code, and end up with tests we can live with. Conversely,
Line 771: making an effort to write tests that are readable and ﬂexible gives us more feed-
Line 772: back about the internal quality of the code we are testing. We end up with tests
Line 773: that help, rather than hinder, continued development.
Line 774: Chapter 20
Line 775: Listening to the Tests
Line 776: 246
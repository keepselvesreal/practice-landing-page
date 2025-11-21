# 19.5 Recording the Failure (pp.221-225)

---
**Page 221**

Recording the Failure
Now we want to return to the end-to-end test and the reportsInvalidMessage()
method that we parked. Our requirement is that the Sniper application must log
a message about these failures so that the user’s organization can recover the
situation. This means that our test should look for a log ﬁle and check its contents.
Filling In the Test
We implement the missing check and ﬂush the log before each test, delegating
the management of the log ﬁle to an AuctionLogDriver class which uses the
Apache Commons IO library. It also cheats slightly by resetting the log manager
(we’re not really supposed to be in the same address space), since deleting the
log ﬁle can confuse a cached logger.
public class ApplicationRunner { […]
private AuctionLogDriver logDriver = new AuctionLogDriver();
  public void reportsInvalidMessage(FakeAuctionServer auction, String message)
    throws IOException 
  {
logDriver.hasEntry(containsString(message));
  }
  public void startBiddingWithStopPrice(FakeAuctionServer auction, int stopPrice) {
    startSniper();
    openBiddingFor(auction, stopPrice);
  }  
  private startSniper() {
logDriver.clearLog()
    Thread thread = new Thread("Test Application") {
      @Override public void run() { // Start the application […]
  }
}
public class AuctionLogDriver {
  public static final String LOG_FILE_NAME = "auction-sniper.log";
  private final File logFile = new File(LOG_FILE_NAME);
  public void hasEntry(Matcher<String> matcher) throws IOException  {
    assertThat(FileUtils.readFileToString(logFile), matcher); 
  }
  public void clearLog() {
    logFile.delete();
    LogManager.getLogManager().reset(); 
  }
}
This new check only reassures us that we’ve fed a message through the system
and into some kind of log record—it tells us that the pieces ﬁt together. We’ll
write a more thorough test of the contents of a log record later. The end-to-end
test now fails because, of course, there’s no log ﬁle to read.
221
Recording the Failure


---
**Page 222**

Failure Reporting in the Translator
Once again, the ﬁrst change is in the AuctionMessageTranslator. We’d like
the record to include the auction identiﬁer, the received message, and
the thrown exception. The “single responsibility” principle suggests that the
AuctionMessageTranslator should not be responsible for deciding how to report
the event, so we invent a new collaborator to handle this task. We call it
XMPPFailureReporter:
public interface XMPPFailureReporter {
  void cannotTranslateMessage(String auctionId, String failedMessage, 
                              Exception exception);
}
We amend our existing failure tests, wrapping up message creation and common
expectations in helper methods, for example:
@Test public void
notifiesAuctionFailedWhenBadMessageReceived() {
  String badMessage = "a bad message";
expectFailureWithMessage(badMessage);
  translator.processMessage(UNUSED_CHAT, message(badMessage));
}
private Message message(String body) {
  Message message = new Message();
  message.setBody(body);
  return message;
}
private void expectFailureWithMessage(final String badMessage) {
  context.checking(new Expectations() {{  
    oneOf(listener).auctionFailed(); 
oneOf(failureReporter).cannotTranslateMessage(
                             with(SNIPER_ID), with(badMessage),
                             with(any(Exception.class)));
  }});
}
The new reporter is a dependency for the translator, so we feed it in through
the constructor and call it just before notifying any listeners. We know that
message.getBody() will not throw an exception, it’s just a simple bean, so we
can leave it outside the catch block.
public class AuctionMessageTranslator implements MessageListener {
  public void processMessage(Chat chat, Message message) {
    String messageBody = message.getBody();
    try {
      translate(messageBody);
    } catch (RuntimeException exception) {
failureReporter.cannotTranslateMessage(sniperId, messageBody, exception);
      listener.auctionFailed();
    }
  }  […]
The unit test passes.
Chapter 19
Handling Failure
222


---
**Page 223**

Generating the Log Message
The next stage is to implement the XMPPFailureReporter with something that
generates a log ﬁle. This is where we actually check the format and contents of
a log entry. We start a class LoggingXMPPFailureReporter and decide to use Java’s
built-in logging framework. We could make the tests for this new class write and
read from a real ﬁle. Instead, we decide that ﬁle access is sufﬁciently covered by
the end-to-end test we’ve just set up, so we’ll run everything in memory to
reduce the test’s dependencies. We’re conﬁdent we can take this shortcut, because
the example is so simple; for more complex behavior we would write some
integration tests.
The Java logging framework has no interfaces, so we have to be more concrete
than we’d like. Exceptionally, we decide to use a class-based mock to override
the relevant method in Logger; in jMock we turn on class-based mocking
with the setImposteriser() call. The AfterClass annotation tells JUnit to call
resetLogging() after all the tests have run to ﬂush any changes we might have
made to the logging environment.
@RunWith(JMock.class)
public class LoggingXMPPFailureReporterTest {
  private final Mockery context = new Mockery() {{
setImposteriser(ClassImposteriser.INSTANCE);
  }};
  final Logger logger = context.mock(Logger.class);
  final LoggingXMPPFailureReporter reporter = new LoggingXMPPFailureReporter(logger);
@AfterClass
  public static void resetLogging() {
    LogManager.getLogManager().reset();
  }
  @Test public void
writesMessageTranslationFailureToLog() {
    context.checking(new Expectations() {{
      oneOf(logger).severe("<auction id> "
                         + "Could not translate message \"bad message\" "
                         + "because \"java.lang.Exception: bad\"");
    }});
    reporter.cannotTranslateMessage("auction id", "bad message", new Exception("bad"));
  }
}
We pass this test with an implementation that just calls the logger with a string
formatted from the inputs to cannotTranslateMessage().
Breaking Our Own Rules?
We already wrote that we don’t like to mock classes, and we go on about it further
in Chapter 20. So, how come we’re doing it here?
223
Recording the Failure


---
**Page 224**

What we care about in this test is the rendering of the values into a failure message
with a severity level. The class is very limited, just a shim above the logging layer,
so we don’t think it’s worth introducing another level of indirection to deﬁne the
logging role. As we wrote before, we also don’t think it worth running against a real
ﬁle since that introduces dependencies (and, even worse, asynchrony) not really
relevant to the functionality we’re developing. We also believe that, as part of the
Java runtime, the logging API is unlikely to change.
So, just this once, as a special favor, setting no precedents, making no promises,
we mock the Logger class. There are a couple more points worth making before we
move on. First, we would not do this for a class that is internal to our code, because
then we would be able write an interface to describe the role it’s playing. Second,
if the LoggingXMPPFailureReporter were to grow in complexity, we would probably
ﬁnd ourselves discovering a supporting message formatter class that could be
tested directly.
Closing the Loop
Now we have the pieces in place to make the whole end-to-end test pass. We
plug an instance of the LoggingXMPPFailureReporter into the XMPPAuctionHouse
so that, via its XMPPAuctions, every AuctionMessageTranslator is constructed
with the reporter. We also move the constant that deﬁnes the log ﬁle name there
from AuctionLogDriver, and deﬁne a new XMPPAuctionException to gather up
any failures within the package.
public class XMPPAuctionHouse implements AuctionHouse {
  public XMPPAuctionHouse(XMPPConnection connection) 
    throws XMPPAuctionException 
  {
    this.connection = connection;
this.failureReporter = new LoggingXMPPFailureReporter(makeLogger());
  }
  public Auction auctionFor(String itemId) {
    return new XMPPAuction(connection, auctionId(itemId, connection), failureReporter);
  } 
  private Logger makeLogger() throws XMPPAuctionException {
    Logger logger = Logger.getLogger(LOGGER_NAME);
    logger.setUseParentHandlers(false);
    logger.addHandler(simpleFileHandler());
    return logger;
  }
  private FileHandler simpleFileHandler() throws XMPPAuctionException {
    try {
      FileHandler handler = new FileHandler(LOG_FILE_NAME);
      handler.setFormatter(new SimpleFormatter());
      return handler;
    } catch (Exception e) {
      throw new XMPPAuctionException("Could not create logger FileHandler " 
                                   + getFullPath(LOG_FILE_NAME), e);
    }
  } […]
Chapter 19
Handling Failure
224


---
**Page 225**

The end-to-end test passes completely and we can cross another item off our
list: Figure 19.2.
Figure 19.2
The Sniper reports failed messages from an auction
Observations
“Inverse Salami” Development
We hope that by now you’re getting a sense of the rhythm of incrementally
growing software, adding functionality in thin but coherent slices. For each new
feature, write some tests that show what it should do, work through each of
those tests changing just enough code to make it pass, restructure the code as
needed either to open up space for new functionality or to reveal new
concepts—then ship it. We discuss how this ﬁts into the larger development picture
in Chapter 5. In static languages, such as Java and C#, we can often use the
compiler to help us navigate the chain of implementation dependencies: change
the code to accept the new triggering event, see what breaks, ﬁx that breakage,
see what that change breaks in turn, and repeat the process until the
functionality works.
The skill is in learning how to divide requirements up into incremental slices,
always having something working, always adding just one more feature. The
process should feel relentless—it just keeps moving. To make this work, we have
to understand how to change the code incrementally and, critically, keep the
code well structured so that we can take it wherever we need to go (and we
don’t know where that is yet). This is why the refactoring part of a test-driven
225
Observations



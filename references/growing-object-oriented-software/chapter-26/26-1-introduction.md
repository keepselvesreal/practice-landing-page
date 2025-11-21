# 26.1 Introduction (pp.301-302)

---
**Page 301**

Chapter 26
Unit Testing and Threads
It is decreed by a merciful Nature that the human brain cannot think
of two things simultaneously.
—Sir Arthur Conan Doyle
Introduction
There’s no getting away from it: concurrency complicates matters. It is a challenge
when doing test-driven development. Unit tests cannot give you as much
conﬁdence in system quality because concurrency and synchronization are system-
wide concerns. When writing tests, you have to worry about getting the synchro-
nization right within the system and between the test and the system. Test failures
are harder to diagnose because exceptions may be swallowed by background
threads or tests may just time out with no clear explanation.
It’s hard to diagnose and correct synchronization problems in existing code,
so it’s worth thinking about the system’s concurrency architecture ahead of
time. You don’t need to design it in great detail, just decide on a broad-brush
architecture and principles by which the system will cope with concurrency.
This design is often prescribed by the frameworks or libraries that an
application uses. For example:
•
Swing dispatches user events on its own thread. If an event handler runs
for a long time, the user interface becomes unresponsive because Swing
does not process user input while the event handler is running. Event call-
backs must spawn “worker” threads to perform long-running tasks, and
those worker threads must synchronize with the event dispatch thread to
update the user interface.
•
A servlet container has a pool of threads that receive HTTP requests and
pass them to servlets for processing. Many threads can be active in the same
servlet instance at once.
•
Java EE containers manage all the threading in the application. The contain-
er guarantees that only one thread will call into a component at a time.
Components cannot start their own threads.
•
The Smack library used by the Auction Sniper application starts a daemon
thread to receive XMPP messages. It will deliver messages on a single thread,
301


---
**Page 302**

but the application must synchronize the Smack thread and the Swing thread
to avoid the GUI components being corrupted.
When you must design a system’s concurrency architecture from scratch, you
can use modeling tools to prove your design free of certain classes of synchroniza-
tion errors, such as deadlock, livelock, or starvation. Design tools that help you
model concurrency are becoming increasingly easy to use. The book Concurrency:
State Models & Java Programs [Magee06] is an introduction to concurrent pro-
gramming that stresses a combination of formal modeling and implementation
and describes how to do the formal modeling with the LTSA analysis tool.
Even with a proven design, however, we have to cross the chasm between design
and implementation. We need to ensure that our components conform to the
architectural constraints of the system. Testing can help at this point. Once we’ve
designed how the system will manage concurrency, we can test-drive the objects
that will ﬁt into that architecture. Unit tests give us conﬁdence that an object
performs its synchronization responsibilities, such as locking its state or blocking
and waking threads. Coarser-grained tests, such as system tests, give us conﬁdence
that the entire system manages concurrency correctly.
Separating Functionality and Concurrency Policy
Objects that cope with multiple threads mix functional concerns with synchro-
nization concerns, either of which can be the cause of test failures. Tests must
also synchronize with the background threads, so that they don’t make assertions
before the threads have ﬁnished working or leave threads running that might
interfere with later tests. Worse, in the presence of threads, unit tests do not
usually report failures well. Exceptions get thrown on the hidden threads, killing
them unexpectedly and breaking the behavior of the tested object. If a test times
out waiting for background threads to ﬁnish, there’s often no diagnostic other
than a basic timeout message. All this makes unit testing difﬁcult.
Searching for Auctions Concurrently
Let’s look at an example. We will extend our Auction Sniper application to let
the user search for auctions of interest. When the user enters search
keywords, the application will run the search concurrently on all auction houses
that the application can connect to. Each AuctionHouse will return a list of
AuctionDescriptions that contain information about its auctions matching the
search keywords. The application will combine the results it receives from all
AuctionHouses and display a single list of auctions to the user. The user can then
decide which of them to bid for.
The concurrent search is performed by an AuctionSearch object which passes
the search keywords to each AuctionHouse and announces the results they return
Chapter 26
Unit Testing and Threads
302



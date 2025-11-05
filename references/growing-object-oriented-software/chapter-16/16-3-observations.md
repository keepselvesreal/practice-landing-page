# 16.3 Observations (pp.189-191)

---
**Page 189**

Observations
Making Steady Progress
We’re starting to see more payback from some of our restructuring work. It was
pretty easy to convert the end-to-end test to handle multiple items, and most of
the implementation consisted of teasing apart code that was already working.
We’ve been careful to keep class responsibilities focused—except for the one
place, Main, where we’ve put all our working compromises.
We made an effort to stay honest about writing enough tests, which has forced
us to consider a couple of edge cases we might otherwise have left. We also intro-
duced a new intermediate-level “integration” test to allow us to work out the
implementation of the user interface without dragging in the rest of the system.
TDD Conﬁdential
We don’t write up everything that went into the development of our
examples—that would be boring and waste paper—but we think it’s worth a
note about what happened with this one. It took us a couple of attempts to get
this design pointing in the right direction because we were trying to allocate be-
havior to the wrong objects. What kept us honest was that for each attempt to
write tests that were focused and made sense, the setup and our assertions kept
drifting apart. Once we’d broken through our inadequacies as programmers, the
tests became much clearer.
Ship It?
So now that everything works we can get on with more features, right? Wrong.
We don’t believe that “working” is the same thing as “ﬁnished.” We’ve left quite
a design mess in Main as we sorted out our ideas, with functionality from various
slices of the application all jumbled into one, as in Figure 16.3.  Apart from the
confusion this leaves, most of this code is not really testable except through the
end-to-end tests. We can get away with that now, while the code is still small,
but it will be difﬁcult to sustain as the application grows. More importantly,
perhaps, we’re not getting any unit-test feedback about the internal quality of
the code.
We might put this code into production if we knew the code was never going
to change or there was an emergency. We know that the ﬁrst isn’t true, because
the application isn’t ﬁnished yet, and being in a hurry is not really a crisis. We
know we will be working in this code again soon, so we can either clean up now,
while it’s still fresh in our minds, or re-learn it every time we touch it. Given that
we’re trying to make an educational point here, you’ve probably guessed
what we’ll do next.
189
Observations


---
**Page 190**

This page intentionally left blank 


---
**Page 191**

Chapter 17
Teasing Apart Main
In which we slice up our application, shufﬂing behavior around to
isolate the XMPP and user interface code from the sniping logic. We
achieve this incrementally, changing one concept at a time without
breaking the whole application. We ﬁnally put a stake through the
heart of notToBeGCd.
Finding a Role
We’ve convinced ourselves that we need to do some surgery on Main, but what
do we want our improved Main to do?
For programs that are more than trivial, we like to think of our top-level class
as a “matchmaker,” ﬁnding components and introducing them to each other.
Once that job is done it drops into the background and waits for the application to
ﬁnish. On a larger scale, this what the current generation of application containers
do, except that the relationships are often encoded in XML.
In its current form, Main acts as a matchmaker but it’s also implementing some
of the components, which means it has too many responsibilities. One clue is to
look at its imports:
import java.awt.event.WindowAdapter;
import java.awt.event.WindowEvent;
import java.util.ArrayList;
import javax.swing.SwingUtilities;
import org.jivesoftware.smack.Chat;
import org.jivesoftware.smack.XMPPConnection;
import org.jivesoftware.smack.XMPPException;
import auctionsniper.ui.MainWindow;
import auctionsniper.ui.SnipersTableModel;
import auctionsniper.AuctionMessageTranslator;
import auctionsniper.XMPPAuction;
We’re importing code from three unrelated packages, plus the auctionsniper
package itself. In fact, we have a package loop in that the top-level and
UI packages depend on each other. Java, unlike some other languages, tolerates
package loops, but they’re not something we should be pleased with.
191



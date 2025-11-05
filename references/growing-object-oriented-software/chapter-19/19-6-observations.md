# 19.6 Observations (pp.225-229)

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


---
**Page 226**

development cycle is so critical—we always get into trouble when we don’t keep
up that side of the bargain.
Small Methods to Express Intent
We have a habit of writing helper methods to wrap up small amounts of code—for
two reasons. First, this reduces the amount of syntactic noise in the calling code
that languages like Java force upon us. For example, when we disconnect
the Sniper, the translatorFor() method means we don’t have to type
"AuctionMessageTranslator" twice in the same line. Second, this gives a mean-
ingful name to a structure that would not otherwise be obvious. For example,
chatDisconnectorFor() describes what its anonymous class does and is less
intrusive than deﬁning a named inner class.
Our aim is to do what we can to make each level of code as readable and self-
explanatory as possible, repeating the process all the way down until we actually
have to use a Java construct.
Logging Is Also a Feature
We deﬁned XMPPFailureReporter to package up failure reporting for the
AuctionMessageTranslator. Many teams would regard this as overdesign and
just write the log message in place. We think this would weaken the design by
mixing levels (message translation and logging) in the same code.
We’ve seen many systems where logging has been added ad hoc by developers
wherever they ﬁnd a need. However, production logging is an external interface
that should be driven by the requirements of those who will depend on it, not
by the structure of the current implementation. We ﬁnd that when we take the
trouble to describe runtime reporting in the caller’s terms, as we did with
the XMPPFailureReporter, we end up with more useful logs. We also ﬁnd that
we end up with the logging infrastructure clearly isolated, rather than scattered
throughout the code, which makes it easier to work with.
This topic is such a bugbear (for Steve at least) that we devote a whole section
to it in Chapter 20.
Chapter 19
Handling Failure
226


---
**Page 227**

Part IV
Sustainable Test-Driven
Development
This part discusses the qualities we look for in test code that
keep the development “habitable.” We want to make sure the
tests pull their weight by making them expressive, so that we
can tell what’s important when we read them and when they
fail, and by making sure they don’t become a maintenance drag
themselves. We need to apply as much care and attention to the
tests as we do to the production code, although the coding styles
may differ. Difﬁculty in testing might imply that we need to
change our test code, but often it’s a hint that our design ideas
are wrong and that we ought to change the production code.
We’ve written up these guidelines as separate chapters, but
that has more to do with our need for a linear structure that
will ﬁt into a book. In practice, these qualities are all related to
and support each other. Test-driven development combines
testing, speciﬁcation, and design into one holistic activity.1
1. For us, a sign of this interrelatedness was the difﬁculty we had in breaking up the
material into coherent chapters.


---
**Page 228**

This page intentionally left blank 


---
**Page 229**

Chapter 20
Listening to the Tests
You can see a lot just by observing.
—Yogi Berra
Introduction
Sometimes we ﬁnd it difﬁcult to write a test for some functionality we want to
add to our code. In our experience, this usually means that our design can be
improved—perhaps the class is too tightly coupled to its environment or does
not have clear responsibilities. When this happens, we ﬁrst check whether it’s an
opportunity to improve our code, before working around the design by making
the test more complicated or using more sophisticated tools. We’ve found
that the qualities that make an object easy to test also make our code responsive
to change.
The trick is to let our tests drive our design (that’s why it’s called test-driven
development). TDD is about testing code, verifying its externally visible qualities
such as functionality and performance. TDD is also about feedback on the code’s
internal qualities: the coupling and cohesion of its classes, dependencies that are
explicit or hidden, and effective information hiding—the qualities that keep the
code maintainable.
With practice, we’ve become more sensitive to the rough edges in our tests, so
we can use them for rapid feedback about the design. Now when we ﬁnd a feature
that’s difﬁcult to test, we don’t just ask ourselves how to test it, but also why is
it difﬁcult to test.
In this chapter, we look at some common “test smells” that we’ve encountered
and discuss what they might imply about the design of the code. There are two
categories of test smell to consider. One is where the test itself is not well
written—it may be unclear or brittle. Meszaros [Meszaros07] covers several such
patterns in his “Test Smells” chapter. This chapter is concerned with the other
category, where a test is highlighting that the target code is the problem. Meszaros
has one pattern for this, called “Hard-to-Test Code.” We’ve picked out some
common cases that we’ve seen that are relevant to our approach to TDD.
229



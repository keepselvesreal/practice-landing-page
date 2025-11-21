# 6.4 No And's, Or's, or But's (pp.51-52)

---
**Page 51**

((EditSaveCustomizer) master.getModelisable()
  .getDockablePanel()
    .getCustomizer())
      .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
Every getter in this example exposes a structural detail. If we wanted to change,
say, the way customizations on the master are enabled, we’d have to change all
the intermediate relationships.
Different Levels of Language
As you’ll see in Part III, we often write helper methods to make code more readable.
We’re not afraid of adding very small methods if they clarify the meaning of the
feature they represent. We name these methods to make the calling code read
as naturally as possible; we don’t have to conform to external conventions since
these methods are only there to support other code. For example, in Chapter 15
we have a line in a test that reads:
allowing(sniperListener).sniperStateChanged(with(aSniperThatIs(BIDDING)));
We’ll explain what this means at the time. What’s relevant here is that
aSniperThatIs() is a local method that constructs a value to be passed to the
with() method, and that its name is intended to describe its intent in this context.
In effect, we’re constructing a very small embedded language that deﬁnes, in this
case, a part of a test.
As well as distinguishing between value and object types (page 13), we ﬁnd that
we tend towards different programming styles at different levels in the code.
Loosely speaking, we use the message-passing style we’ve just described between
objects, but we tend to use a more functional style within an object, building up
behavior from methods and values that have no side effects.
Features without side effects mean that we can assemble our code from smaller
components, minimizing the amount of risky shared state. Writing large-scale
functional programs is a topic for a different book, but we ﬁnd that a little
immutability within the implementation of a class leads to much safer code and
that, if we do a good job, the code reads well too.
So how do we choose the right features for an object?
No And’s, Or’s, or But’s
Every object should have a single, clearly deﬁned responsibility; this is the “single
responsibility” principle [Martin02]. When we’re adding behavior to a system,
this principle helps us decide whether to extend an existing object or create a
new service for an object to call.
51
No And’s, Or’s, or But’s


---
**Page 52**

Our heuristic is that we should be able to describe what an object does without
using any conjunctions (“and,” “or”). If we ﬁnd ourselves adding clauses to the
description, then the object probably should be broken up into collaborating
objects, usually one for each clause.
This principle also applies when we’re combining objects into new abstractions.
If we’re packaging up behavior implemented across several objects into a single
construct, we should be able to describe its responsibility clearly; there are some
related ideas below in the “Composite Simpler Than the Sum of Its Parts” and
“Context Independence” sections.
Object Peer Stereotypes
We have objects with single responsibilities, communicating with their peers
through messages in clean APIs, but what do they say to each other?
We categorize an object’s peers (loosely) into three types of relationship. An
object might have:
Dependencies
Services that the object requires from its peers so it can perform its responsi-
bilities. The object cannot function without these services. It should not be
possible to create the object without them. For example, a graphics package
will need something like a screen or canvas to draw on—it doesn’t make
sense without one.
Notiﬁcations
Peers that need to be kept up to date with the object’s activity. The object
will notify interested peers whenever it changes state or performs a signiﬁcant
action. Notiﬁcations are “ﬁre and forget”; the object neither knows nor cares
which peers are listening. Notiﬁcations are so useful because they decouple
objects from each other. For example, in a user interface system, a button
component promises to notify any registered listeners when it’s clicked, but
does not know what those listeners will do. Similarly, the listeners expect to
be called but know nothing of the way the user interface dispatches its events.
Adjustments
Peers that adjust the object’s behavior to the wider needs of the system. This
includes policy objects that make decisions on the object’s behalf (the Strat-
egy pattern in [Gamma94]) and component parts of the object if it’s a com-
posite. For example, a Swing JTable will ask a TableCellRenderer to draw
a cell’s value, perhaps as RGB (Red, Green, Blue) values for a color. If we
change the renderer, the table will change its presentation, now displaying
the HSB (Hue, Saturation, Brightness) values.
Chapter 6
Object-Oriented Style
52



# 6.5 Object Peer Stereotypes (pp.52-53)

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


---
**Page 53**

These stereotypes are only heuristics to help us think about the design, not
hard rules, so we don’t obsess about ﬁnding just the right classiﬁcation of an
object’s peers. What matters most is the context in which the collaborating objects
are used. For example, in one application an auditing log could be a dependency,
because auditing is a legal requirement for the business and no object should be
created without an audit trail. Elsewhere, it could be a notiﬁcation, because
auditing is a user choice and objects will function perfectly well without it.
Another way to look at it is that notiﬁcations are one-way: A notiﬁcation lis-
tener may not return a value, call back the caller, or throw an exception, since
there may be other listeners further down the chain. A dependency or adjustment,
on the other hand, may do any of these, since there’s a direct relationship.
“New or new not. There is no try.”4
We try to make sure that we always create a valid object. For dependencies, this
means that we pass them in through the constructor. They’re required, so there’s
no point in creating an instance of an object until its dependencies are available,
and using the constructor enforces this constraint in the object’s deﬁnition.
Partially creating an object and then ﬁnishing it off by setting properties is brittle
because the programmer has to remember to set all the dependencies.When the
object changes to add new dependencies, the existing client code will still compile
even though it no longer constructs a valid instance. At best this will cause a
NullPointerException, at worst it will fail misleadingly.
Notiﬁcations and adjustments can be passed to the constructor as a convenience.
Alternatively, they can be initialized to safe defaults and overwritten later (note
that there is no safe default for a dependency). Adjustments can be initialized to
common values, and notiﬁcations to a null object [Woolf98] or an empty collection.
We then add methods to allow callers to change these default values, and add or
remove listeners.
Composite Simpler Than the Sum of Its Parts
All objects in a system, except for primitive types built into the language, are
composed of other objects. When composing objects into a new type, we want
the new type to exhibit simpler behavior than all of its component parts considered
together. The composite object’s API must hide the existence of its component
parts and the interactions between them, and expose a simpler abstraction to its
peers. Think of a mechanical clock: It has two or three hands for output and one
pull-out wheel for input but packages up dozens of moving parts.
4. Attributed to Yoda.
53
Composite Simpler Than the Sum of Its Parts



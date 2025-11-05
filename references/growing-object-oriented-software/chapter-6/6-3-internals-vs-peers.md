# 6.3 Internals vs. Peers (pp.50-51)

---
**Page 50**

Many object-oriented languages support encapsulation by providing control over
the visibility of an object’s features to other objects, but that’s not enough. Objects
can break encapsulation by sharing references to mutable objects, an effect known
as aliasing. Aliasing is essential for conventional object- oriented systems (other-
wise no two objects would be able to communicate), but accidental aliasing can
couple unrelated parts of a system so it behaves mysteriously and is inﬂexible to
change.
We follow standard practices to maintain encapsulation when coding: deﬁne
immutable value types, avoid global variables and singletons, copy collections
and mutable values when passing them between objects, and so on. We have
more about information hiding later in this chapter.
Internals vs. Peers
As we organize our system, we must decide what is inside and outside each object,
so that the object provides a coherent abstraction with a clear API. Much of the
point of an object, as we discussed above, is to encapsulate access to its internals
through its API and to hide these details from the rest of the system. An object
communicates with other objects in the system by sending and receiving messages,
as in Figure 6.2; the objects it communicates with directly are its peers.
Figure 6.2
Objects communicate by sending and receiving messages
This decision matters because it affects how easy an object is to use, and so
contributes to the internal quality of the system. If we expose too much of an
object’s internals through its API, its clients will end up doing some of its work.
We’ll have distributed behavior across too many objects (they’ll be coupled to-
gether), increasing the cost of maintenance because any changes will now ripple
across the code. This is the effect of the “train wreck” example on page 17:
Chapter 6
Object-Oriented Style
50


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



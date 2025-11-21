# 2.3 Follow the Messages (pp.14-17)

---
**Page 14**

Figure 2.1
A web of objects
object-oriented languages that most of us use, the confusion is that both concepts
are implemented by the same language construct: classes.
Values are immutable instances that model ﬁxed quantities. They have no in-
dividual identity, so two value instances are effectively the same if they have the
same state. This means that it makes no sense to compare the identity of two
values; doing so can cause some subtle bugs—think of the different ways of
comparing two copies of new Integer(999). That’s why we’re taught to use
string1.equals(string2) in Java rather than string1 == string2.
Objects, on the other hand, use mutable state to model their behavior over
time. Two objects of the same type have separate identities even if they have ex-
actly the same state now, because their states can diverge if they receive different
messages in the future.
In practice, this means that we split our system into two “worlds”: values,
which are treated functionally, and objects, which implement the stateful behavior
of the system. In Part III, you’ll see how our coding style varies depending on
which world we’re working in.
In this book, we will use the term object to refer only to instances with identity,
state, and processing—not values. There doesn’t appear to be another accepted
term that isn’t overloaded with other meanings (such as entity and process).
Follow the Messages
We can beneﬁt from this high-level, declarative approach only if our objects are
designed to be easily pluggable. In practice, this means that they follow common
communication patterns and that the dependencies between them are made ex-
plicit. A communication pattern is a set of rules that govern how a group of ob-
jects talk to each other: the roles they play, what messages they can send and
when, and so on. In languages like Java, we identify object roles with (abstract)
interfaces, rather than (concrete) classes—although interfaces don’t deﬁne
everything we need to say.
Chapter 2
Test-Driven Development with Objects
14


---
**Page 15**

In our view, the domain model is in these communication patterns, because
they are what gives meaning to the universe of possible relationships between
the objects. Thinking of a system in terms of its dynamic, communication structure
is a signiﬁcant mental shift from the static classiﬁcation that most of us learn
when being introduced to objects. The domain model isn’t even obviously visible
because the communication patterns are not explicitly represented in the program-
ming languages we get to work with. We hope to show, in this book, how tests
and mock objects help us see the communication between our objects more
clearly.
Here’s a small example of how focusing on the communication between objects
guides design.
In a video game, the objects in play might include: actors, such as the player
and the enemies; scenery, which the player ﬂies over; obstacles, which the
player can crash into; and effects, such as explosions and smoke. There are also
scripts spawning objects behind the scenes as the game progresses.
This is a good classiﬁcation of the game objects from the players’ point of view
because it supports the decisions they need to make when playing the game—when
interacting with the game from outside. This is not, however, a useful classiﬁcation
for the implementers of the game. The game engine has to display objects that
are visible, tell objects that are animated about the passing of time, detect colli-
sions between objects that are physical, and delegate decisions about what to do
when physical objects collide to collision resolvers.
Figure 2.2
Roles and objects in a video game
As you can see in Figure 2.2, the two views, one from the game engine and
one from the implementation of the in-play objects, are not the same. An Obstacle,
for example, is Visible and Physical, while a Script is a Collision Resolver and
Animated but not Visible. The objects in the game play different roles depending
15
Follow the Messages


---
**Page 16**

on what the engine needs from them at the time. This mismatch between static
classiﬁcation and dynamic communication means that we’re unlikely to come
up with a tidy class hierarchy for the game objects that will also suit the needs
of the engine.
At best, a class hierarchy represents one dimension of an application, providing
a mechanism for sharing implementation details between objects; for example,
we might have a base class to implement the common features of frame-based
animation. At worst, we’ve seen too many codebases (including our own) that
suffer complexity and duplication from using one mechanism to represent multiple
concepts.
Roles, Responsibilities, Collaborators
We try to think about objects in terms of roles, responsibilities, and collaborators,
as best described by Wirfs-Brock and McKean in [Wirfs-Brock03]. An object is an
implementation of one or more roles; a role is a set of related responsibilities;
and a responsibility is an obligation to perform a task or know information. A
collaboration is an interaction of objects or roles (or both).
Sometimes we step away from the keyboard and use an informal design technique
that Wirfs-Brock and McKean describe, called CRC cards (Candidates, Responsi-
bilities, Collaborators). The idea is to use low-tech index cards to explore the po-
tential object structure of an application, or a part of it. These index cards allow
us to experiment with structure without getting stuck in detail or becoming too
attached to an early solution.
Figure 2.3
CRC card for a video game
Chapter 2
Test-Driven Development with Objects
16


---
**Page 17**

Tell, Don’t Ask
We have objects sending each other messages, so what do they say? Our experi-
ence is that the calling object should describe what it wants in terms of the role
that its neighbor plays, and let the called object decide how to make that happen.
This is commonly known as the “Tell, Don’t Ask” style or, more formally, the
Law of Demeter. Objects make their decisions based only on the information
they hold internally or that which came with the triggering message; they avoid
navigating to other objects to make things happen. Followed consistently, this
style produces more ﬂexible code because it’s easy to swap objects that play the
same role. The caller sees nothing of their internal structure or the structure of
the rest of the system behind the role interface.
When we don’t follow the style, we can end up with what’s known as “train
wreck” code, where a series of getters is chained together like the carriages in a
train. Here’s one case we found on the Internet:
((EditSaveCustomizer) master.getModelisable()
  .getDockablePanel()
    .getCustomizer())
      .getSaveItem().setEnabled(Boolean.FALSE.booleanValue());
After some head scratching, we realized what this fragment was meant to say:
master.allowSavingOfCustomisations();
This wraps all that implementation detail up behind a single call. The client of
master no longer needs to know anything about the types in the chain. We’ve
reduced the risk that a design change might cause ripples in remote parts of the
codebase.
As well as hiding information, there’s a more subtle beneﬁt from “Tell, Don’t
Ask.” It forces us to make explicit and so name the interactions between objects,
rather than leaving them implicit in the chain of getters. The shorter version
above is much clearer about what it’s for, not just how it happens to be
implemented.
But Sometimes Ask
Of course we don’t “tell” everything;1 we “ask” when getting information from
values and collections, or when using a factory to create new objects. Occasion-
ally, we also ask objects about their state when searching or ﬁltering, but we still
want to maintain expressiveness and avoid “train wrecks.”
For example (to continue with the metaphor), if we naively wanted to spread
reserved seats out across the whole of a train, we might start with something like:
1. Although that’s an interesting exercise to try, to stretch your technique.
17
But Sometimes Ask



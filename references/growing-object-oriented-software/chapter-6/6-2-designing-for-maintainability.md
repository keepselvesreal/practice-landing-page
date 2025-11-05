# 6.2 Designing for Maintainability (pp.47-50)

---
**Page 47**

Chapter 6
Object-Oriented Style
Always design a thing by considering it in its next larger
context—a chair in a room, a room in a house, a house in an
environment, an environment in a city plan.
—Eliel Saarinen
Introduction
So far in Part II, we’ve talked about how to get started with the development
process and how to keep going. Now we want to take a more detailed look at
our design goals and our use of TDD, and in particular mock objects, to guide
the structure of our code.
We value code that is easy to maintain over code that is easy to write.1 Imple-
menting a feature in the most direct way can damage the maintainability of the
system, for example by making the code difﬁcult to understand or by introducing
hidden dependencies between components. Balancing immediate and longer-term
concerns is often tricky, but we’ve seen too many teams that can no longer deliver
because their system is too brittle.
In this chapter, we want to show something of what we’re trying to achieve
when we design software, and how that looks in an object-oriented language;
this is the “opinionated” part of our approach to software. In the next chapter,
we’ll look at the mechanics of how to guide code in this direction with TDD.
Designing for Maintainability
Following the process we described in Chapter 5, we grow our systems a slice of
functionality at a time. As the code scales up, the only way we can continue to
understand and maintain it is by structuring the functionality into objects, objects
into packages,2 packages into programs, and programs into systems. We use two
principal heuristics to guide this structuring:
1. As the Agile Manifesto might have put it.
2. We’re being vague about the meaning of “package” here since we want it to include
concepts such as modules, libraries, and namespaces, which tend to be confounded
in the Java world—but you know what we mean.
47


---
**Page 48**

Separation of concerns
When we have to change the behavior of a system, we want to change as
little code as possible. If all the relevant changes are in one area of code, we
don’t have to hunt around the system to get the job done. Because we cannot
predict when we will have to change any particular part of the system, we
gather together code that will change for the same reason. For example, code
to unpack messages from an Internet standard protocol will not change for
the same reasons as business code that interprets those messages, so we
partition the two concepts into different packages.
Higher levels of abstraction
The only way for humans to deal with complexity is to avoid it, by working
at higher levels of abstraction. We can get more done if we program by
combining components of useful functionality rather than manipulating
variables and control ﬂow; that’s why most people order food from a menu
in terms of dishes, rather than detail the recipes used to create them.
Applied consistently, these two forces will push the structure of an appli-
cation towards something like Cockburn’s “ports and adapters” architecture
[Cockburn08], in which the code for the business domain is isolated from its
dependencies on technical infrastructure, such as databases and user interfaces.
We don’t want technical concepts to leak into the application model, so we write
interfaces to describe its relationships with the outside world in its terminology
(Cockburn’s ports). Then we write bridges between the application core and each
technical domain (Cockburn’s adapters). This is related to what Eric Evans calls
an “anticorruption layer” [Evans03].
The bridges implement the interfaces deﬁned by the application model and
map between application-level and technical-level objects (Figure 6.1). For exam-
ple, a bridge might map an order book object to SQL statements so that orders
are persisted in a database. To do so, it might query values from the application
object or use an object-relational tool like Hibernate3 to pull values out of objects
using Java reﬂection. We’ll show an example of refactoring to this architecture
in Chapter 17.
The next question is how to ﬁnd the facets in the behavior where the interfaces
should be, so that we can divide up the code cleanly. We have some second-level
heuristics to help us think about that.
3. http://www.hibernate.org
Chapter 6
Object-Oriented Style
48


---
**Page 49**

Figure 6.1
An application’s core domain model is mapped onto
technical infrastructure
Encapsulation and Information Hiding
We want to be careful with the distinction between “encapsulation” and “information
hiding.” The terms are often used interchangeably but actually refer to two separate,
and largely orthogonal, qualities:
Encapsulation
Ensures that the behavior of an object can only be affected through its API.
It lets us control how much a change to one object will impact other parts of
the system by ensuring that there are no unexpected dependencies between
unrelated components.
Information hiding
Conceals how an object implements its functionality behind the abstraction
of its API. It lets us work with higher abstractions by ignoring lower-level details
that are unrelated to the task at hand.
We’re most aware of encapsulation when we haven’t got it. When working with
badly encapsulated code, we spend too much time tracing what the potential
effects of a change might be, looking at where objects are created, what common
data they hold, and where their contents are referenced. The topic has inspired
two books that we know of, [Feathers04] and [Demeyer03].
49
Designing for Maintainability


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



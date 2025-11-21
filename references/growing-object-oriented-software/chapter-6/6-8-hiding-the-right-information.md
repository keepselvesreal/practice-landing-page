# 6.8 Hiding the Right Information (pp.55-56)

---
**Page 55**

“permanent” (passed in on construction) or “transient” (passed in to the method
that needs them).
In this “paternalistic” approach, each object is told just enough to do its job
and wrapped up in an abstraction that matches its vocabulary. Eventually, the
chain of objects reaches a process boundary, which is where the system will ﬁnd
external details such as host names, ports, and user interface events.
One Domain Vocabulary
A class that uses terms from multiple domains might be violating context
independence, unless it’s part of a bridging layer.
The effect of the “context independence” rule on a system of objects is to make
their relationships explicit, deﬁned separately from the objects themselves. First,
this simpliﬁes the objects, since they don’t need to manage their own relationships.
Second, this simpliﬁes managing the relationships, since objects at the same
scale are often created and composed together in the same places, usually in
mapping-layer factory objects.
Context independence guides us towards coherent objects that can be applied
in different contexts, and towards systems that we can change by reconﬁguring
how their objects are composed.
Hiding the Right Information
Encapsulation is almost always a good thing to do, but sometimes information
can be hidden in the wrong place. This makes the code difﬁcult to understand,
to integrate, or to build behavior from by composing objects. The best defense
is to be clear about the difference between the two concepts when discussing a
design. For example, we might say:
•
“Encapsulate the data structure for the cache in the CachingAuctionLoader
class.”
•
“Encapsulate the name of the application’s log ﬁle in the PricingPolicy
class.”
These sound reasonable until we recast them in terms of information hiding:
•
“Hide the data structure used for the cache in the CachingAuctionLoader
class.”
•
“Hide the name of the application’s log ﬁle in the PricingPolicy class.”
55
Hiding the Right Information


---
**Page 56**

Context independence tells us that we have no business hiding details of the
log ﬁle in the PricingPolicy class—they’re concepts from different levels in
the “Russian doll” structure of nested domains. If the log ﬁle name is necessary,
it should be packaged up and passed in from a level that understands external
conﬁguration.
An Opinionated View
We’ve taken the time to describe what we think of as “good” object-oriented
design because it underlies our approach to development and we ﬁnd that it helps
us write code that we can easily grow and adapt to meet the changing needs of
its users. Now we want to show how our approach to test-driven development
supports these principles.
Chapter 6
Object-Oriented Style
56



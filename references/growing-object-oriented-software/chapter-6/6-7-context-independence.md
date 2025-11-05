# 6.7 Context Independence (pp.54-55)

---
**Page 54**

In software, a user interface component for editing money values might have
two subcomponents: one for the amount and one for the currency. For the
component to be useful, its API should manage both values together, otherwise
the client code could just control it subcomponents directly.
moneyEditor.getAmountField().setText(String.valueOf(money.amount());
moneyEditor.getCurrencyField().setText(money.currencyCode());
The “Tell, Don’t Ask” convention can start to hide an object’s structure from
its clients but is not a strong enough rule by itself. For example, we could replace
the getters in the ﬁrst version with setters:
moneyEditor.setAmountField(money.amount());
moneyEditor.setCurrencyField(money.currencyCode());
This still exposes the internal structure of the component, which its client still
has to manage explicitly.
We can make the API much simpler by hiding within the component everything
about the way money values are displayed and edited, which in turn simpliﬁes
the client code:
moneyEditor.setValue(money);
This suggests a rule of thumb:
Composite Simpler Than the Sum of Its Parts
The API of a composite object should not be more complicated than that of any of
its components.
Composite objects can, of course, be used as components in larger-scale, more
sophisticated composite objects. As we grow the code, the “composite simpler
than the sum of its parts” rule contributes to raising the level of abstraction.
Context Independence
While the “composite simpler than the sum of its parts” rule helps us decide
whether an object hides enough information, the “context independence” rule
helps us decide whether an object hides too much or hides the wrong information.
A system is easier to change if its objects are context-independent; that is, if
each object has no built-in knowledge about the system in which it executes. This
allows us to take units of behavior (objects) and apply them in new situations.
To be context-independent, whatever an object needs to know about the larger
environment it’s running in must be passed in. Those relationships might be
Chapter 6
Object-Oriented Style
54


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



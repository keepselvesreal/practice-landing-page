# 6.6 Composite Simpler Than the Sum of Its Parts (pp.53-54)

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



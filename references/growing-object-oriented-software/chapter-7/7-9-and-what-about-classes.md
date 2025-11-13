# 7.9 And What about Classes? (pp.67-69)

---
**Page 67**

And What about Classes?
One last point. Unusually for a book on object-oriented software, we haven’t
said much about classes and inheritance. It should be obvious by now that we’ve
been pushing the application domain into the gaps between the objects, the
communication protocols. We emphasize interfaces more than classes because
that’s what other objects see: an object’s type is deﬁned by the roles it plays.
We view classes for objects as an “implementation detail”—a way of imple-
menting types, not the types themselves. We discover object class hierarchies by
factoring out common behavior, but prefer to refactor to delegation if possible
since we ﬁnd that it makes our code more ﬂexible and easier to understand.5
Value types, on the other hand, are less likely to use delegation since they don’t
have peers.
There’s plenty of good advice on how to work with classes in, for example,
[Fowler99], [Kerievsky04], and [Evans03].
5. The design forces, of course, are different in languages that support multiple
inheritance well, such as Eiffel [Meyer91].
67
And What about Classes?


---
**Page 68**

This page intentionally left blank 


---
**Page 69**

Chapter 8
Building on Third-Party Code
Programming today is all about doing science on the parts you have
to work with.
—Gerald Jay Sussman
Introduction
We’ve shown how we pull a system’s design into existence: discovering what our
objects need and writing interfaces and further objects to meet those needs. This
process works well for new functionality. At some point, however, our design
will come up against a need that is best met by third-party code: standard APIs,
open source libraries, or vendor products. The critical point about third-party
code is that we don’t control it, so we cannot use our process to guide its design.
Instead, we must focus on the integration between our design and the
external code.
In integration, we have an abstraction to implement, discovered while we de-
veloped the rest of the feature. With the third-party API pushing back at our
design, we must ﬁnd the best balance between elegance and practical use of
someone else’s ideas. We must check that we are using the third-party API cor-
rectly, and adjust our abstraction to ﬁt if we ﬁnd that our assumptions are
incorrect.
Only Mock Types That You Own
Don’t Mock Types You Can’t Change
When we use third-party code we often do not have a deep understanding of
how it works. Even if we have the source available, we rarely have time to read
it thoroughly enough to explore all its quirks. We can read its documentation,
which is often incomplete or incorrect. The software may also have bugs that we
will need to work around. So, although we know how we want our abstraction
to behave, we don’t know if it really does so until we test it in combination with
the third-party code.
We also prefer not to change third-party code, even when we have the sources.
It’s usually too much trouble to apply private patches every time there’s a new
version. If we can’t change an API, then we can’t respond to any design feedback
we get from writing unit tests that touch it. Whatever alarm bells the unit tests
69



# 6.9 An Opinionated View (pp.56-57)

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


---
**Page 57**

Chapter 7
Achieving Object-Oriented
Design
In matters of style, swim with the current; in matters of principle, stand
like a rock.
—Thomas Jefferson
How Writing a Test First Helps the Design
The design principles we outlined in the previous chapter apply to ﬁnding the
right boundaries for an object so that it plays well with its neighbors—a caller
wants to know what an object does and what it depends on, but not how it
works. We also want an object to represent a coherent unit that makes sense in
its larger environment. A system built from such components will have the
ﬂexibility to reconﬁgure and adapt as requirements change.
There are three aspects of TDD that help us achieve this scoping. First, starting
with a test means that we have to describe what we want to achieve before we
consider how. This focus helps us maintain the right level of abstraction for the
target object. If the intention of the unit test is unclear then we’re probably
mixing up concepts and not ready to start coding. It also helps us with information
hiding as we have to decide what needs to be visible from outside the object.
Second, to keep unit tests understandable (and, so, maintainable), we have to
limit their scope. We’ve seen unit tests that are dozens of lines long, burying the
point of the test somewhere in its setup. Such tests tell us that the component
they’re testing is too large and needs breaking up into smaller components. The
resulting composite object should have a clearer separation of concerns as we
tease out its implicit structure, and we can write simpler tests for the extracted
objects.
Third, to construct an object for a unit test, we have to pass its dependencies
to it, which means that we have to know what they are. This encourages context
independence, since we have to be able to set up the target object’s environment
before we can unit-test it—a unit test is just another context. We’ll notice that
an object with implicit (or just too many) dependencies is painful to prepare for
testing—and make a point of cleaning it up.
In this chapter, we describe how we use an incremental, test-driven approach
to nudge our code towards the design principles we described in the previous
chapter.
57



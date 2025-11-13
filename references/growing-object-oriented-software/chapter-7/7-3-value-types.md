# 7.3 Value Types (pp.59-60)

---
**Page 59**

Value Types
Before we go further, we want to revisit the distinction we described in “Values
and Objects” (page 13): values are immutable, so they’re simpler and have no
meaningful identity; objects have state, so they have identity and relationships
with each other.
The more code we write, the more we’re convinced that we should deﬁne
types to represent value concepts in the domain, even if they don’t do much. It
helps to create a consistent domain model that is more self-explanatory. If we
create, for example, an Item type in a system, instead of just using String, we can
ﬁnd all the code that’s relevant for a change without having to chase through the
method calls. Speciﬁc types also reduce the risk of confusion—as the Mars Climate
Orbiter disaster showed, feet and metres may both be represented as numbers
but they’re different things.1 Finally, once we have a type to represent a concept,
it usually turns out to be a good place to hang behavior, guiding us towards using
a more object-oriented approach instead of scattering related behavior across
the code.
We use three basic techniques for introducing value types, which we’ve called
(in a ﬁt of alliteration): breaking out, budding off, and bundling up.
Breaking out
When we ﬁnd that the code in an object is becoming complex, that’s often
a sign that it’s implementing multiple concerns and that we can break out
coherent units of behavior into helper types. There’s an example in “Tidying
Up the Translator” (page 135) where we break a class that handles incoming
messages into two parts: one to parse the message string, and one to interpret
the result of the parsing.
Budding off
When we want to mark a new domain concept in the code, we often introduce
a placeholder type that wraps a single ﬁeld, or maybe has no ﬁelds at all. As
the code grows, we ﬁll in more detail in the new type by adding ﬁelds and
methods. With each type that we add, we’re raising the level of abstraction
of the code.
Bundling up
When we notice that a group of values are always used together, we take
that as a suggestion that there’s a missing construct. A ﬁrst step might be to
create a new type with ﬁxed public ﬁelds—just giving the group a name
highlights the missing concept. Later we can migrate behavior to the new
1. In 1999, NASA’s Mars Climate Orbiter burned up in the planet’s atmosphere because,
amongst other problems, the navigation software confused metric with imperial units.
There’s a brief description at http://news.bbc.co.uk/1/hi/sci/tech/514763.stm.
59
Value Types


---
**Page 60**

type, which might eventually allow us to hide its ﬁelds behind a clean
interface, satisfying the “composite simpler than the sum of its parts” rule.
We ﬁnd that the discovery of value types is usually motivated by trying to
follow our design principles, rather than by responding to code stresses when
writing tests.
Where Do Objects Come From?
The categories for discovering object types are similar (which is why we shoe-
horned them into these names), except that the design guidance we get from
writing unit tests tends to be more important. As we wrote in “External and
Internal Quality” (page 10), we use the effort of unit testing to maintain the
code’s internal quality. There are more examples of the inﬂuence of testing on
design in Chapter 20.
Breaking Out: Splitting a Large Object into a Group of
Collaborating Objects
When starting a new area of code, we might temporarily suspend our design
judgment and just write code without attempting to impose much structure. This
allows us to gain some experience in the area and test our understanding of any
external APIs we’re developing against. After a short while, we’ll ﬁnd our code
becoming too complex to understand and will want to clean it up. We can start
pulling out cohesive units of functionality into smaller collaborating objects,
which we can then unit-test independently. Splitting out a new object also forces
us to look at the dependencies of the code we’re pulling out.
We have two concerns about deferring cleanup. The ﬁrst is how long we should
wait before doing something. Under time pressure, it’s tempting to leave the un-
structured code as is and move on to the next thing (“after all, it works and it’s
just one class…”). We’ve seen too much code where the intention wasn’t clear
and the cost of cleanup kicked in when the team could least afford it. The second
concern is that occasionally it’s better to treat this code as a spike—once we
know what to do, just roll it back and reimplement cleanly. Code isn’t sacred
just because it exists, and the second time won’t take as long.
The Tests Say…
Break up an object if it becomes too large to test easily, or if its test failures become
difﬁcult to interpret. Then unit-test the new parts separately.
Chapter 7
Achieving Object-Oriented Design
60



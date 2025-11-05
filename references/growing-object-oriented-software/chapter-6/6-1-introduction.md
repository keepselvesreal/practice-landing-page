# 6.1 Introduction (pp.47-47)

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



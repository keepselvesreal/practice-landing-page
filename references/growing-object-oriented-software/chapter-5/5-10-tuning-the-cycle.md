# 5.10 Tuning the Cycle (pp.45-47)

---
**Page 45**

Figure 5.3
Difﬁculties writing tests may suggest a need to ﬁx
production code
This is an example of how our maxim—“Expect Unexpected Changes”—guides
development. If we keep up the quality of the system by refactoring when we see
a weakness in the design, we will be able to make it respond to whatever changes
turn up. The alternative is the usual “software rot” where the code decays until
the team just cannot respond to the needs of its customers. We’ll return to this
topic in Chapter 20.
Tuning the Cycle
There’s a balance between exhaustively testing execution paths and testing inte-
gration. If we test at too large a grain, the combinatorial explosion of trying all
the possible paths through the code will bring development to a halt. Worse,
some of those paths, such as throwing obscure exceptions, will be impractical to
test from that level. On the other hand, if we test at too ﬁne a grain—just at the
class level, for example—the testing will be easier but we’ll miss problems that
arise from objects not working together.
How much unit testing should we do, using mock objects to break external
dependencies, and how much integration testing? We don’t think there’s a single
answer to this question. It depends too much on the context of the team and its
environment. The best we can get from the testing part of TDD (which is a lot)
is the conﬁdence that we can change the code without breaking it: Fear kills
progress. The trick is to make sure that the conﬁdence is justiﬁed.
So, we regularly reﬂect on how well TDD is working for us, identify any
weaknesses, and adapt our testing strategy. Fiddly bits of logic might need more
unit testing (or, alternatively, simpliﬁcation); unhandled exceptions might need
more integration-level testing; and, unexpected system failures will need more
investigation and, possibly, more testing throughout.
45
Tuning the Cycle


---
**Page 46**

This page intentionally left blank 


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



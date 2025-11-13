# 5.9 Listen to the Tests (pp.44-45)

---
**Page 44**

The Importance of Describing Behavior, Not API Features
Nat used to run a company that produced online advertising and branded content
for clients sponsoring sports teams. One of his clients sponsored a Formula One
racing team. Nat wrote a fun little game that simulated Formula One race strategies
for the client to put on the team’s website. It took him two weeks to write, from
initial idea to ﬁnal deliverable, and once he handed it over to the client he forgot
all about it.
It turned out, however, that the throw-away game was by far the most popular
content on the team’s website. For the next F1 season, the client wanted to capi-
talize on its success. They wanted the game to model the track of each Grand
Prix, to accommodate the latest F1 rules, to have a better model of car physics,
to simulate dynamic weather, overtaking, spin-outs, and more.
Nat had written the original version test-ﬁrst, so he expected it to be easy to
change. However, going back to the code, he found the tests very hard to under-
stand. He had written a test for each method of each object but couldn’t understand
from those tests how each object was meant to behave—what the responsibilities
of the object were and how the different methods of the object worked together.
It helps to choose test names that describe how the object behaves in the
scenario being tested. We look at this in more detail in “Test Names Describe
Features” (page 248).
Listen to the Tests
When writing unit and integration tests, we stay alert for areas of the code that
are difﬁcult to test. When we ﬁnd a feature that’s difﬁcult to test, we don’t just
ask ourselves how to test it, but also why is it difﬁcult to test.
Our experience is that, when code is difﬁcult to test, the most likely cause is
that our design needs improving. The same structure that makes the code difﬁcult
to test now will make it difﬁcult to change in the future. By the time that future
comes around, a change will be more difﬁcult still because we’ll have forgotten
what we were thinking when we wrote the code. For a successful system, it might
even be a completely different team that will have to live with the consequences
of our decisions.
Our response is to regard the process of writing tests as a valuable early
warning of potential maintenance problems and to use those hints to ﬁx a problem
while it’s still fresh. As Figure 5.3 shows, if we’re ﬁnding it hard to write the next
failing test, we look again at the design of the production code and often refactor
it before moving on.
Chapter 5
Maintaining the Test-Driven Cycle
44


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



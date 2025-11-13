# 1.3 Practices That Support Change (pp.5-6)

---
**Page 5**

Practices That Support Change
We’ve found that we need two technical foundations if we want to grow a system
reliably and to cope with the unanticipated changes that always happen. First,
we need constant testing to catch regression errors, so we can add new features
without breaking existing ones. For systems of any interesting size, frequent
manual testing is just impractical, so we must automate testing as much as we
can to reduce the costs of building, deploying, and modifying versions of the
system.
Second, we need to keep the code as simple as possible, so it’s easier to under-
stand and modify. Developers spend far more time reading code than writing it,
so that’s what we should optimize for.1 Simplicity takes effort, so we constantly
refactor [Fowler99] our code as we work with it—to improve and simplify its
design, to remove duplication, and to ensure that it clearly expresses what it does.
The test suites in the feedback loops protect us against our own mistakes as we
improve (and therefore change) the code.
The catch is that few developers enjoy testing their code. In many development
groups, writing automated tests is seen as not “real” work compared to adding
features, and boring as well. Most people do not do as well as they should at
work they ﬁnd uninspiring.
Test-Driven Development (TDD) turns this situation on its head. We write
our tests before we write the code. Instead of just using testing to verify our work
after it’s done, TDD turns testing into a design activity. We use the tests to clarify
our ideas about what we want the code to do. As Kent Beck described it to us,
“I was ﬁnally able to separate logical from physical design. I’d always been told
to do that but no one ever explained how.” We ﬁnd that the effort of writing a
test ﬁrst also gives us rapid feedback about the quality of our design ideas—that
making code accessible for testing often drives it towards being cleaner and more
modular.
If we write tests all the way through the development process, we can build
up a safety net of automated regression tests that give us the conﬁdence to make
changes.
“… you have nothing to lose but your bugs”
We cannot emphasize strongly enough how liberating it is to work on test-driven
code that has thorough test coverage.We ﬁnd that we can concentrate on the task
in hand, conﬁdent that we’re doing the right work and that it’s actually quite hard
to break the system—as long as we follow the practices.
1. Begel and Simon [Begel08] showed that new graduates at Microsoft spend most of
their ﬁrst year just reading code.
5
Practices That Support Change


---
**Page 6**

Test-Driven Development in a Nutshell
The cycle at the heart of TDD is: write a test; write some code to get it working;
refactor the code to be as simple an implementation of the tested features as
possible. Repeat.
Figure 1.1
The fundamental TDD cycle
As we develop the system, we use TDD to give us feedback on the quality of
both its implementation (“Does it work?”) and design (“Is it well structured?”).
Developing test-ﬁrst, we ﬁnd we beneﬁt twice from the effort. Writing tests:
•
makes us clarify the acceptance criteria for the next piece of work—we
have to ask ourselves how we can tell when we’re done (design);
•
encourages us to write loosely coupled components, so they can easily be
tested in isolation and, at higher levels, combined together (design);
•
adds an executable description of what the code does (design); and,
•
adds to a complete regression suite (implementation);
whereas running tests:
•
detects errors while the context is fresh in our mind (implementation); and,
•
lets us know when we’ve done enough, discouraging “gold plating” and
unnecessary features (design).
This feedback cycle can be summed up by the Golden Rule of TDD:
The Golden Rule of Test-Driven Development
Never write new functionality without a failing test.
Chapter 1
What Is the Point of Test-Driven Development?
6



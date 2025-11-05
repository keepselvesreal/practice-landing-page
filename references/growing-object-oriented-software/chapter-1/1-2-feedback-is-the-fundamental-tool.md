# 1.2 Feedback Is the Fundamental Tool (pp.4-5)

---
**Page 4**

Feedback Is the Fundamental Tool
We think that the best approach a team can take is to use empirical feedback to
learn about the system and its use, and then apply that learning back to the system.
A team needs repeated cycles of activity. In each cycle it adds new features and
gets feedback about the quantity and quality of the work already done. The team
members split the work into time boxes, within which they analyze, design,
implement, and deploy as many features as they can.
Deploying completed work to some kind of environment at each cycle is critical.
Every time a team deploys, its members have an opportunity to check their as-
sumptions against reality. They can measure how much progress they’re really
making, detect and correct any errors, and adapt the current plan in response to
what they’ve learned. Without deployment, the feedback is not complete.
In our work, we apply feedback cycles at every level of development, organizing
projects as a system of nested loops ranging from seconds to months, such as:
pair programming, unit tests, acceptance tests, daily meetings, iterations, releases,
and so on. Each loop exposes the team’s output to empirical feedback so that
the team can discover and correct any errors or misconceptions. The nested
feedback loops reinforce each other; if a discrepancy slips through an inner loop,
there is a good chance an outer loop will catch it.
Each feedback loop addresses different aspects of the system and development
process. The inner loops are more focused on the technical detail: what a unit of
code does, whether it integrates with the rest of the system. The outer loops are
more focused on the organization and the team: whether the application serves
its users’ needs, whether the team is as effective as it could be.
The sooner we can get feedback about any aspect of the project, the better.
Many teams in large organizations can release every few weeks. Some teams re-
lease every few days, or even hours, which gives them an order of magnitude
increase in opportunities to receive and respond to feedback from real users.
Incremental and Iterative Development
In a project organized as a set of nested feedback loops, development is
incremental and iterative.
Incremental development builds a system feature by feature, instead of building
all the layers and components and integrating them at the end. Each feature is
implemented as an end-to-end “slice” through all the relevant parts of the system.
The system is always integrated and ready for deployment.
Iterative development progressively reﬁnes the implementation of features in
response to feedback until they are good enough.
Chapter 1
What Is the Point of Test-Driven Development?
4


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



# 1.1 Software Development as a Learning Process (pp.3-4)

---
**Page 3**

Chapter 1
What Is the Point of
Test-Driven Development?
One must learn by doing the thing; for though you think you know it,
you have no certainty, until you try.
—Sophocles
Software Development as a Learning Process
Almost all software projects are attempting something that nobody has done
before (or at least that nobody in the organization has done before). That some-
thing may refer to the people involved, the application domain, the technology
being used, or (most likely) a combination of these. In spite of the best efforts of
our discipline, all but the most routine projects have elements of surprise. Inter-
esting projects—those likely to provide the most beneﬁt—usually have a lot
of surprises.
Developers often don’t completely understand the technologies they’re using.
They have to learn how the components work whilst completing the project.
Even if they have a good understanding of the technologies, new applications
can force them into unfamiliar corners. A system that combines many signiﬁcant
components (which means most of what a professional programmer works on)
will be too complex for any individual to understand all of its possibilities.
For customers and end users, the experience is worse. The process of building
a system forces them to look at their organization more closely than they have
before. They’re often left to negotiate and codify processes that, until now,
have been based on convention and experience.
Everyone involved in a software project has to learn as it progresses. For the
project to succeed, the people involved have to work together just to understand
what they’re supposed to achieve, and to identify and resolve misunderstandings
along the way. They all know there will be changes, they just don’t know what
changes. They need a process that will help them cope with uncertainty as their
experience grows—to anticipate unanticipated changes.
3


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



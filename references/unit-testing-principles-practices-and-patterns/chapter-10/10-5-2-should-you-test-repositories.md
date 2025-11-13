# 10.5.2 Should you test repositories? (pp.253-254)

---
**Page 253**

253
Common database testing questions
Because there are hardly any abstraction layers in reads (the domain model is one
such layer), unit tests aren’t of any use there. If you decide to test your reads, do so
using integration tests on a real database. 
10.5.2 Should you test repositories?
Repositories provide a useful abstraction on top of the database. Here’s a usage exam-
ple from our sample CRM project:
User user = _userRepository.GetUserById(userId);
_userRepository.SaveUser(user);
Should you test repositories independently of other integration tests? It might seem
beneficial to test how repositories map domain objects to the database. After all,
there’s significant room for a mistake in this functionality. Still, such tests are a net loss
to your test suite due to high maintenance costs and inferior protection against
regressions. Let’s discuss these two drawbacks in more detail.
HIGH MAINTENANCE COSTS
Repositories fall into the controllers quadrant on the types-of-code diagram from
chapter 7 (figure 10.8). They exhibit little complexity and communicate with an out-
of-process dependency: the database. The presence of that out-of-process dependency
is what inflates the tests’ maintenance costs.
 When it comes to maintenance costs, testing repositories carries the same burden
as regular integration tests. But does such testing provide an equal amount of benefits
in return? Unfortunately, it doesn’t.
Writes
Database
Client
Reads
Application
. . . not here
Domain model goes here . . .
Figure 10.7
There’s no need for a domain model in reads. And because the cost of a 
mistake in reads is lower than it is in writes, there’s also not as much need for integration 
testing.


---
**Page 254**

254
CHAPTER 10
Testing the database
INFERIOR PROTECTION AGAINST REGRESSIONS
Repositories don’t carry that much complexity, and a lot of the gains in protection
against regressions overlap with the gains provided by regular integration tests. Thus,
tests on repositories don’t add significant enough value.
 The best course of action in testing a repository is to extract the little complexity it
has into a self-contained algorithm and test that algorithm exclusively. That’s what
UserFactory and CompanyFactory were for in earlier chapters. These two classes per-
formed all the mappings without taking on any collaborators, out-of-process or other-
wise. The repositories (the Database class) only contained simple SQL queries.
 Unfortunately, such a separation between data mapping (formerly performed by
the factories) and interactions with the database (formerly performed by Database) is
impossible when using an ORM. You can’t test your ORM mappings without calling
the database, at least not without compromising resistance to refactoring. Therefore,
adhere to the following guideline: don’t test repositories directly, only as part of the overarch-
ing integration test suite.
 Don’t test EventDispatcher separately, either (this class converts domain events
into calls to unmanaged dependencies). There are too few gains in protection against
regressions in exchange for the too-high costs required to maintain the complicated
mock machinery. 
10.6
Conclusion
Well-crafted tests against the database provide bulletproof protection from bugs. In
my experience, they are one of the most effective tools, without which it’s impossible
Domain model,
algorithms
Overcomplicated
code
Trivial code
Controllers
Complexity,
domain
signiﬁcance
Number of
collaborators
Repositories
Figure 10.8
Repositories exhibit little complexity and communicate with the 
out-of-process dependency, thus falling into the controllers quadrant on the 
types-of-code diagram.



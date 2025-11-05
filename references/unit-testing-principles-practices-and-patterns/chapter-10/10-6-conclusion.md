# 10.6 Conclusion (pp.254-255)

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


---
**Page 255**

255
Summary
to gain full confidence in your software. Such tests help enormously when you refac-
tor the database, switch the ORM, or change the database vendor.
 In fact, our sample project transitioned to the Entity Framework ORM earlier in
this chapter, and I only needed to modify a couple of lines of code in the integration
test to make sure the transition was successful. Integration tests working directly with
managed dependencies are the most efficient way to protect against bugs resulting
from large-scale refactorings. 
Summary
Store database schema in a source control system, along with your source code.
Database schema consists of tables, views, indexes, stored procedures, and any-
thing else that forms a blueprint of how the database is constructed.
Reference data is also part of the database schema. It is data that must be pre-
populated in order for the application to operate properly. To differentiate
between reference and regular data, look at whether your application can mod-
ify that data. If so, it’s regular data; otherwise, it’s reference data.
Have a separate database instance for every developer. Better yet, host that
instance on the developer’s own machine for maximum test execution speed.
The state-based approach to database delivery makes the state explicit and lets a
comparison tool implicitly control migrations. The migration-based approach
emphasizes the use of explicit migrations that transition the database from one
state to another. The explicitness of the database state makes it easier to handle
merge conflicts, while explicit migrations help tackle data motion.
Prefer the migration-based approach over state-based, because handling data
motion is much more important than merge conflicts. Apply every modification
to the database schema (including reference data) through migrations.
Business operations must update data atomically. To achieve atomicity, rely on
the underlying database’s transaction mechanism.
Use the unit of work pattern when possible. A unit of work relies on the under-
lying database’s transactions; it also defers all updates to the end of the business
operation, thus improving performance.
Don’t reuse database transactions or units of work between sections of the
test. Each arrange, act, and assert section should have its own transaction or
unit of work.
Execute integration tests sequentially. Parallel execution involves significant
effort and usually is not worth it.
Clean up leftover data at the start of a test. This approach works fast, doesn’t
result in inconsistent behavior, and isn’t prone to accidentally skipping the
cleanup phase. With this approach, you don’t have to introduce a separate tear-
down phase, either.



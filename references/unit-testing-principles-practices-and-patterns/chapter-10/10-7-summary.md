# 10.7 Summary (pp.255-259)

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


---
**Page 256**

256
CHAPTER 10
Testing the database
Avoid in-memory databases such as SQLite. You’ll never gain good protection if
your tests run against a database from a different vendor. Use the same database
management system in tests as in production.
Shorten tests by extracting non-essential parts into private methods or helper
classes:
– For the arrange section, choose Object Mother over Test Data Builder.
– For act, create decorator methods.
– For assert, introduce a fluent interface.
The threshold for testing reads should be higher than that for writes. Test only
the most complex or important read operations; disregard the rest.
Don’t test repositories directly, but only as part of the overarching integration
test suite. Tests on repositories introduce too high maintenance costs for too
few additional gains in protection against regressions.


---
**Page 257**

Part 4
Unit testing anti-patterns
This final part of the book covers common unit testing anti-patterns. You’ve
most likely encountered some of them in the past. Still, it’s interesting to look at
this topic using the four attributes of a good unit test defined in chapter 4. You
can use those attributes to analyze any unit testing concepts or patterns; anti-
patterns aren’t an exception.


---
**Page 258**

 


---
**Page 259**

259
Unit testing anti-patterns
This chapter is an aggregation of lesser related topics (mostly anti-patterns) that
didn’t fit in earlier in the book and are better served on their own. An anti-pattern is
a common solution to a recurring problem that looks appropriate on the surface
but leads to problems further down the road.
 You will learn how to work with time in tests, how to identify and avoid such anti-
patterns as unit testing of private methods, code pollution, mocking concrete
classes, and more. Most of these topics follow from the first principles described in
part 2. Still, they are well worth spelling out explicitly. You’ve probably heard of at
least some of these anti-patterns in the past, but this chapter will help you connect
the dots, so to speak, and see the foundations they are based on.
This chapter covers
Unit testing private methods
Exposing private state to enable unit testing
Leaking domain knowledge to tests
Mocking concrete classes



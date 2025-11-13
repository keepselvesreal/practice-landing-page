# 10.0 Introduction [auto-generated] (pp.229-230)

---
**Page 229**

229
Testing the database
The last piece of the puzzle in integration testing is managed out-of-process depen-
dencies. The most common example of a managed dependency is an application
database—a database no other application has access to.
 Running tests against a real database provides bulletproof protection against
regressions, but those tests aren’t easy to set up. This chapter shows the preliminary
steps you need to take before you can start testing your database: it covers keeping
track of the database schema, explains the difference between the state-based and
migration-based database delivery approaches, and demonstrates why you should
choose the latter over the former.
 After learning the basics, you’ll see how to manage transactions during the test,
clean up leftover data, and keep tests small by eliminating insignificant parts and
amplifying the essentials. This chapter focuses on relational databases, but many of
This chapter covers
Prerequisites for testing the database
Database testing best practices
Test data life cycle
Managing database transactions in tests


---
**Page 230**

230
CHAPTER 10
Testing the database
the same principles are applicable to other types of data stores such as document-ori-
ented databases or even plain text file storages.
10.1
Prerequisites for testing the database
As you might recall from chapter 8, managed dependencies should be included as-is
in integration tests. That makes working with those dependencies more laborious
than unmanaged ones because using a mock is out of the question. But even before
you start writing tests, you must take preparatory steps to enable integration testing. In
this section, you’ll see these prerequisites:
Keeping the database in the source control system
Using a separate database instance for every developer
Applying the migration-based approach to database delivery
Like almost everything in testing, though, practices that facilitate testing also improve
the health of your database in general. You’ll get value out of those practices even if
you don’t write integration tests.
10.1.1 Keeping the database in the source control system
The first step on the way to testing the database is treating the database schema as reg-
ular code. Just as with regular code, a database schema is best stored in a source con-
trol system such as Git.
 I’ve worked on projects where programmers maintained a dedicated database
instance, which served as a reference point (a model database). During development,
all schema changes accumulated in that instance. Upon production deployments, the
team compared the production and model databases, used a special tool to generate
upgrade scripts, and ran those scripts in production (figure 10.1).
Model
database
Production
database
Compare
Modiﬁcations by
programmers
Upgrade
scripts
Generate
Apply
Comparison
tool
Figure 10.1
Having a dedicated instance as a model database is an anti-pattern. The database 
schema is best stored in a source control system.



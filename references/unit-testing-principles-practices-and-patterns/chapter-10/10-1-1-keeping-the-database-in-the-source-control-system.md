# 10.1.1 Keeping the database in the source control system (pp.230-231)

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


---
**Page 231**

231
Prerequisites for testing the database
Using a model database is a horrible way to maintain database schema. That’s because
there’s
No change history—You can’t trace the database schema back to some point in
the past, which might be important when reproducing bugs in production.
No single source of truth—The model database becomes a competing source of
truth about the state of development. Maintaining two such sources (Git and
the model database) creates an additional burden.
On the other hand, keeping all the database schema updates in the source control sys-
tem helps you to maintain a single source of truth and also to track database changes
along with the changes of regular code. No modifications to the database structure
should be made outside of the source control. 
10.1.2 Reference data is part of the database schema
When it comes to the database schema, the usual suspects are tables, views, indexes,
stored procedures, and anything else that forms a blueprint of how the database is
constructed. The schema itself is represented in the form of SQL scripts. You
should be able to use those scripts to create a fully functional, up-to-date database
instance of your own at any time during development. However, there’s another
part of the database that belongs to the database schema but is rarely viewed as
such: reference data.
DEFINITION
Reference data is data that must be prepopulated in order for the
application to operate properly.
Take the CRM system from the earlier chapters, for example. Its users can be either of
type Customer or type Employee. Let’s say that you want to create a table with all user
types and introduce a foreign key constraint from User to that table. Such a constraint
would provide an additional guarantee that the application won’t ever assign a user a
nonexistent type. In this scenario, the content of the UserType table would be refer-
ence data because the application relies on its existence in order to persist users in the
database.
TIP
There’s a simple way to differentiate reference data from regular data.
If your application can modify the data, it’s regular data; if not, it’s refer-
ence data.
Because reference data is essential for your application, you should keep it in the
source control system along with tables, views, and other parts of the database schema,
in the form of SQL INSERT statements.
 Note that although reference data is normally stored separately from regular data,
the two can sometimes coexist in the same table. To make this work, you need to intro-
duce a flag differentiating data that can be modified (regular data) from data that can’t
be modified (reference data) and forbid your application from changing the latter. 



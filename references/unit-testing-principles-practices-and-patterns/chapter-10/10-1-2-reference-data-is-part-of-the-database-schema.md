# 10.1.2 Reference data is part of the database schema (pp.231-232)

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


---
**Page 232**

232
CHAPTER 10
Testing the database
10.1.3 Separate instance for every developer
It’s difficult enough to run tests against a real database. It becomes even more difficult
if you have to share that database with other developers. The use of a shared database
hinders the development process because
Tests run by different developers interfere with each other.
Non-backward-compatible changes can block the work of other developers.
Keep a separate database instance for every developer, preferably on that developer’s
own machine in order to maximize test execution speed. 
10.1.4 State-based vs. migration-based database delivery
There are two major approaches to database delivery: state-based and migration-based.
The migration-based approach is more difficult to implement and maintain initially,
but it works much better than the state-based approach in the long run.
THE STATE-BASED APPROACH
The state-based approach to database delivery is similar to what I described in figure
10.1. You also have a model database that you maintain throughout development.
During deployments, a comparison tool generates scripts for the production database
to bring it up to date with the model database. The difference is that with the state-
based approach, you don’t actually have a physical model database as a source of
truth. Instead, you have SQL scripts that you can use to create that database. The
scripts are stored in the source control.
 In the state-based approach, the comparison tool does all the hard lifting. What-
ever the state of the production database, the tool does everything needed to get it in
sync with the model database: delete unnecessary tables, create new ones, rename col-
umns, and so on. 
THE MIGRATION-BASED APPROACH
On the other hand, the migration-based approach emphasizes the use of explicit
migrations that transition the database from one version to another (figure 10.2).
With this approach, you don’t use tools to automatically synchronize the production
and development databases; you come up with upgrade scripts yourself. However, a
database comparison tool can still be useful when detecting undocumented changes
in the production database schema.
CREATE TABLE
dbo.Customer (…)
ALTER TABLE
dbo.Customer (…)
CREATE TABLE
dbo.User (…)
Migration 1
Migration 2
Migration 3
Figure 10.2
The migration-based approach to database delivery emphasizes the use of explicit 
migrations that transition the database from one version to another.



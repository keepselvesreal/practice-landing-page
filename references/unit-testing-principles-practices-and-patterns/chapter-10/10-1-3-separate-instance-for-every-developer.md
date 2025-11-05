# 10.1.3 Separate instance for every developer (pp.232-232)

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



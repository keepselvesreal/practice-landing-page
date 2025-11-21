# 10.1.4 State-based vs. migration-based database delivery (pp.232-234)

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


---
**Page 233**

233
Prerequisites for testing the database
In the migration-based approach, migrations and not the database state become the
artifacts you store in the source control. Migrations are usually represented with
plain SQL scripts (popular tools include Flyway [https://flywaydb.org] and Liquibase
[https://liquibase.org]), but they can also be written using a DSL-like language that
gets translated into SQL. The following example shows a C# class that represents a
database migration with the help of the FluentMigrator library (https://github.com/
fluentmigrator/fluentmigrator):
[Migration(1)]
          
public class CreateUserTable : Migration
{
public override void Up()       
{
Create.Table("Users");
}
public override void Down()    
{
Delete.Table("Users");
}
}
PREFER THE MIGRATION-BASED APPROACH OVER THE STATE-BASED ONE
The difference between the state-based and migration-based approaches to database
delivery comes down to (as their names imply) state versus migrations (see figure 10.3):
The state-based approach makes the state explicit (by virtue of storing that
state in the source control) and lets the comparison tool implicitly control the
migrations.
The migration-based approach makes the migrations explicit but leaves the state
implicit. It’s impossible to view the database state directly; you have to assemble
it from the migrations.
Migration 
number
Forward 
migration
Backward migration (helpful 
when downgrading to an 
earlier database version to 
reproduce a bug)
State-based
approach
State of the database
Migration mechanism
Migration-based
approach
Implicit
Implicit
Explicit
Explicit
Figure 10.3
The state-based approach makes the state explicit and 
migrations implicit; the migration-based approach makes the opposite choice.


---
**Page 234**

234
CHAPTER 10
Testing the database
Such a distinction leads to different sets of trade-offs. The explicitness of the database
state makes it easier to handle merge conflicts, while explicit migrations help to tackle
data motion.
DEFINITION
Data motion is the process of changing the shape of existing data
so that it conforms to the new database schema.
Although the alleviation of merge conflicts and the ease of data motion might look
like equally important benefits, in the vast majority of projects, data motion is much more
important than merge conflicts. Unless you haven’t yet released your application to pro-
duction, you always have data that you can’t simply discard.
 For example, when splitting a Name column into FirstName and LastName, you not
only have to drop the Name column and create the new FirstName and LastName col-
umns, but you also have to write a script to split all existing names into two pieces.
There is no easy way to implement this change using the state-driven approach; com-
parison tools are awful when it comes to managing data. The reason is that while the
database schema itself is objective, meaning there is only one way to interpret it, data
is context-dependent. No tool can make reliable assumptions about data when gener-
ating upgrade scripts. You have to apply domain-specific rules in order to implement
proper transformations.
 As a result, the state-based approach is impractical in the vast majority of projects.
You can use it temporarily, though, while the project still has not been released to pro-
duction. After all, test data isn’t that important, and you can re-create it every time you
change the database. But once you release the first version, you will have to switch to
the migration-based approach in order to handle data motion properly.
TIP
Apply every modification to the database schema (including reference
data) through migrations. Don’t modify migrations once they are committed
to the source control. If a migration is incorrect, create a new migration
instead of fixing the old one. Make exceptions to this rule only when the
incorrect migration can lead to data loss. 
10.2
Database transaction management
Database transaction management is a topic that’s important for both production and
test code. Proper transaction management in production code helps you avoid data
inconsistencies. In tests, it helps you verify integration with the database in a close-to-
production setting.
 In this section, I’ll first show how to handle transactions in the production code
(the controller) and then demonstrate how to use them in integration tests. I’ll con-
tinue using the same CRM project you saw in the earlier chapters as an example.



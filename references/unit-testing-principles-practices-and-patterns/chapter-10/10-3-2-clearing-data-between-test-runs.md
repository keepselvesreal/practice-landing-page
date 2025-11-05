# 10.3.2 Clearing data between test runs (pp.244-246)

---
**Page 244**

244
CHAPTER 10
Testing the database
trickier. It’s more practical to run integration tests sequentially rather than spend time
trying to squeeze additional performance out of them.
 Most unit testing frameworks allow you to define separate test collections and
selectively disable parallelization in them. Create two such collections (for unit and
integration tests), and then disable test parallelization in the collection with the inte-
gration tests.
 As an alternative, you could parallelize tests using containers. For example, you
could put the model database on a Docker image and instantiate a new container
from that image for each integration test. In practice, though, this approach creates
too much of an additional maintenance burden. With Docker, you not only have to
keep track of the database itself, but you also need to
Maintain Docker images
Make sure each test gets its own container instance
Batch integration tests (because you most likely won’t be able to create all con-
tainer instances at once)
Dispose of used-up containers
I don’t recommend using containers unless you absolutely need to minimize your
integration tests’ execution time. Again, it’s more practical to have just one database
instance per developer. You can run that single instance in Docker, though. I advocate
against premature parallelization, not the use of Docker per se. 
10.3.2 Clearing data between test runs
There are four options to clean up leftover data between test runs:
Restoring a database backup before each test—This approach addresses the problem
of data cleanup but is much slower than the other three options. Even with con-
tainers, the removal of a container instance and creation of a new one usually
takes several seconds, which quickly adds to the total test suite execution time.
Cleaning up data at the end of a test—This method is fast but susceptible to skip-
ping the cleanup phase. If the build server crashes in the middle of the test, or
you shut down the test in the debugger, the input data remains in the database
and affects further test runs.
Wrapping each test in a database transaction and never committing it—In this case, all
changes made by the test and the SUT are rolled back automatically. This
approach solves the problem of skipping the cleanup phase but poses another
issue: the introduction of an overarching transaction can lead to inconsistent
behavior between the production and test environments. It’s the same problem
as with reusing a unit of work: the additional transaction creates a setup that’s
different than that in production.
Cleaning up data at the beginning of a test—This is the best option. It works fast,
doesn’t result in inconsistent behavior, and isn’t prone to accidentally skipping
the cleanup phase.


---
**Page 245**

245
Test data life cycle
TIP
There’s no need for a separate teardown phase; implement that phase as
part of the arrange section.
The data removal itself must be done in a particular order, to honor the database’s
foreign key constraints. I sometimes see people use sophisticated algorithms to figure
out relationships between tables and automatically generate the deletion script or
even disable all integrity constraints and re-enable them afterward. This is unneces-
sary. Write the SQL script manually: it’s simpler and gives you more granular control
over the deletion process.
 Introduce a base class for all integration tests, and put the deletion script there. With
such a base class, you will have the script run automatically at the start of each test, as
shown in the following listing.
public abstract class IntegrationTests
{
private const string ConnectionString = "...";
protected IntegrationTests()
{
ClearDatabase();
}
private void ClearDatabase()
{
string query =
"DELETE FROM dbo.[User];" +    
"DELETE FROM dbo.Company;";    
using (var connection = new SqlConnection(ConnectionString))
{
var command = new SqlCommand(query, connection)
{
CommandType = CommandType.Text
};
connection.Open();
command.ExecuteNonQuery();
}
}
}
TIP
The deletion script must remove all regular data but none of the refer-
ence data. Reference data, along with the rest of the database schema, should
be controlled solely by migrations. 
Listing 10.6
Base class for integration tests
Deletion 
script


---
**Page 246**

246
CHAPTER 10
Testing the database
10.3.3 Avoid in-memory databases
Another way to isolate integration tests from each other is by replacing the database
with an in-memory analog, such as SQLite. In-memory databases can seem beneficial
because they
Don’t require removal of test data
Work faster
Can be instantiated for each test run
Because in-memory databases aren’t shared dependencies, integration tests in effect
become unit tests (assuming the database is the only managed dependency in the
project), similar to the approach with containers described in section 10.3.1.
 In spite of all these benefits, I don’t recommend using in-memory databases
because they aren’t consistent functionality-wise with regular databases. This is, once
again, the problem of a mismatch between production and test environments. Your
tests can easily run into false positives or (worse!) false negatives due to the differ-
ences between the regular and in-memory databases. You’ll never gain good protec-
tion with such tests and will have to do a lot of regression testing manually anyway.
TIP
Use the same database management system (DBMS) in tests as in pro-
duction. It’s usually fine for the version or edition to differ, but the vendor
must remain the same. 
10.4
Reusing code in test sections
Integration tests can quickly grow too large and thus lose ground on the maintainabil-
ity metric. It’s important to keep integration tests as short as possible but without cou-
pling them to each other or affecting readability. Even the shortest tests shouldn’t
depend on one another. They also should preserve the full context of the test scenario
and shouldn’t require you to examine different parts of the test class to understand
what’s going on.
 The best way to shorten integration is by extracting technical, non-business-related
bits into private methods or helper classes. As a side bonus, you’ll get to reuse those
bits. In this section, I’ll show how to shorten all three sections of the test: arrange, act,
and assert.
10.4.1 Reusing code in arrange sections
The following listing shows how our integration test looks after providing a separate
database context (unit of work) for each of its sections.
[Fact]
public void Changing_email_from_corporate_to_non_corporate()
{
// Arrange
User user;
Listing 10.7
Integration test with three database contexts



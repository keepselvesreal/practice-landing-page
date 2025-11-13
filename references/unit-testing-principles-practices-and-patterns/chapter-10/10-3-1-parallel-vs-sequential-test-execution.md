# 10.3.1 Parallel vs. sequential test execution (pp.243-244)

---
**Page 243**

243
Test data life cycle
Assert.Equal("new@gmail.com", userFromDb.Email);
Assert.Equal(UserType.Customer, userFromDb.Type);
Company companyFromDb = companyRepository     
.GetCompany();
     
Assert.Equal(0, companyFromDb.NumberOfEmployees);
busSpy.ShouldSendNumberOfMessages(1)
.WithEmailChangedMessage(user.UserId, "new@gmail.com");
loggerMock.Verify(
x => x.UserTypeHasChanged(
user.UserId, UserType.Employee, UserType.Customer),
Times.Once);
}
}
This test uses the same instance of CrmContext in all three sections: arrange, act, and
assert. This is a problem because such reuse of the unit of work creates an environment
that doesn’t match what the controller experiences in production. In production, each
business operation has an exclusive instance of CrmContext. That instance is created
right before the controller method invocation and is disposed of immediately after.
 To avoid the risk of inconsistent behavior, integration tests should replicate the
production environment as closely as possible, which means the act section must not
share CrmContext with anyone else. The arrange and assert sections must get their
own instances of CrmContext too, because, as you might remember from chapter 8,
it’s important to check the state of the database independently of the data used as
input parameters. And although the assert section does query the user and the com-
pany independently of the arrange section, these sections still share the same database
context. That context can (and many ORMs do) cache the requested data for perfor-
mance improvements.
TIP
Use at least three transactions or units of work in an integration test: one
per each arrange, act, and assert section. 
10.3
Test data life cycle
The shared database raises the problem of isolating integration tests from each other.
To solve this problem, you need to
Execute integration tests sequentially.
Remove leftover data between test runs.
Overall, your tests shouldn’t depend on the state of the database. Your tests should
bring that state to the required condition on their own.
10.3.1 Parallel vs. sequential test execution
Parallel execution of integration tests involves significant effort. You have to ensure
that all test data is unique so no database constraints are violated and tests don’t acci-
dentally pick up input data after each other. Cleaning up leftover data also becomes
. . . and in assert


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



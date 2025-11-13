# 10.3.3 Avoid in-memory databases (pp.246-246)

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



# 4.4.4 Extreme case #3: Brittle tests (pp.83-84)

---
**Page 83**

83
In search of an ideal test
Figure 4.7 shows where trivial tests stand. They have good resistance to refactoring
and provide fast feedback, but they don’t protect you from regressions. 
4.4.4
Extreme case #3: Brittle tests
Similarly, it’s pretty easy to write a test that runs fast and has a good chance of catching
a regression but does so with a lot of false positives. Such a test is called a brittle test: it
can’t withstand a refactoring and will turn red regardless of whether the underlying
functionality is broken.
 You already saw an example of a brittle test in listing 4.2. Here’s another one.
public class UserRepository
{
public User GetById(int id)
{
/* ... */
}
public string LastExecutedSqlStatement { get; set; }
}
[Fact]
public void GetById_executes_correct_SQL_code()
{
var sut = new UserRepository();
User user = sut.GetById(5);
Assert.Equal(
"SELECT * FROM dbo.[User] WHERE UserID = 5",
sut.LastExecutedSqlStatement);
}
Listing 4.6
Test verifying which SQL statement is executed
Resistance to
refactoring
Fast
feedback
Protection
against
regressions
End-to-end tests
Trivial tests
Figure 4.7
Trivial tests have good 
resistance to refactoring, and they 
provide fast feedback, but such tests 
don’t protect you from regressions.


---
**Page 84**

84
CHAPTER 4
The four pillars of a good unit test
This test makes sure the UserRepository class generates a correct SQL statement
when fetching a user from the database. Can this test catch a bug? It can. For exam-
ple, a developer can mess up the SQL code generation and mistakenly use ID instead
of UserID, and the test will point that out by raising a failure. But does this test have
good resistance to refactoring? Absolutely not. Here are different variations of the
SQL statement that lead to the same result:
SELECT * FROM dbo.[User] WHERE UserID = 5
SELECT * FROM dbo.User WHERE UserID = 5
SELECT UserID, Name, Email FROM dbo.[User] WHERE UserID = 5
SELECT * FROM dbo.[User] WHERE UserID = @UserID
The test in listing 4.6 will turn red if you change the SQL script to any of these varia-
tions, even though the functionality itself will remain operational. This is once again
an example of coupling the test to the SUT’s internal implementation details. The test
is focusing on hows instead of whats and thus ingrains the SUT’s implementation
details, preventing any further refactoring.
 Figure 4.8 shows that brittle tests fall into the third bucket. Such tests run fast and
provide good protection against regressions but have little resistance to refactoring. 
4.4.5
In search of an ideal test: The results
The first three attributes of a good unit test (protection against regressions, resistance to
refactoring, and fast feedback) are mutually exclusive. While it’s quite easy to come up
with a test that maximizes two out of these three attributes, you can only do that at the
expense of the third. Still, such a test would have a close-to-zero value due to the mul-
tiplication rule. Unfortunately, it’s impossible to create an ideal test that has a perfect
score in all three attributes (figure 4.9).
Resistance to
refactoring
Fast
feedback
Protection
against
regressions
End-to-end tests
Trivial tests
Brittle tests
Figure 4.8
Brittle tests run fast and they 
provide good protection against regressions, 
but they have little resistance to refactoring.



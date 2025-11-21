# 4.4.3 Extreme case #2: Trivial tests (pp.82-83)

---
**Page 82**

82
CHAPTER 4
The four pillars of a good unit test
4.4.3
Extreme case #2: Trivial tests
Another example of maximizing two out of three attributes at the expense of the third
is a trivial test. Such tests cover a simple piece of code, something that is unlikely to
break because it’s too trivial, as shown in the following listing.
public class User
{
public string Name { get; set; }    
}
[Fact]
public void Test()
{
var sut = new User();
sut.Name = "John Smith";
Assert.Equal("John Smith", sut.Name);
}
Unlike end-to-end tests, trivial tests do provide fast feedback—they run very quickly.
They also have a fairly low chance of producing a false positive, so they have good
resistance to refactoring. Trivial tests are unlikely to reveal any regressions, though,
because there’s not much room for a mistake in the underlying code.
 Trivial tests taken to an extreme result in tautology tests. They don’t test anything
because they are set up in such a way that they always pass or contain semantically
meaningless assertions.
Listing 4.5
Trivial test covering a simple piece of code
Resistance to
refactoring
Fast
feedback
Protection
against
regressions
End-to-end tests
Figure 4.6
End-to-end tests 
provide great protection against 
both regression errors and false 
positives, but they fail at the 
metric of fast feedback.
One-liners like 
this are unlikely 
to contain bugs.


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



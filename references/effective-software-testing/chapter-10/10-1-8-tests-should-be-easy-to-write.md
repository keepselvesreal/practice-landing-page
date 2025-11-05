# 10.1.8 Tests should be easy to write (pp.262-262)

---
**Page 262**

262
CHAPTER 10
Test code quality
if the behavior does not exist or is incorrect.” I am not afraid of purposefully intro-
ducing a bug in the code, running the tests, and seeing them red (and then revert-
ing the bug). 
10.1.7
Tests should have a single and clear reason to fail
We love tests that fail. They indicate problems in our code, usually long before the
code is deployed. But the test failure is the first step toward understanding and fixing
the bug. Your test code should help you understand what caused the bug.
 There are many ways you can do that. If your test follows the earlier principles, the
test is cohesive and exercises only one (hopefully small) behavior of the software sys-
tem. Give your test a name that indicates its intention and the behavior it exercises.
Make sure anyone can understand the input values passed to the method under test.
If the input values are complex, use good variable names that explain what they are
about and code comments in natural language. Finally, make sure the assertions are
clear, and explain why a value is expected. 
10.1.8
Tests should be easy to write
There should be no friction when it comes to writing tests. If it is hard to do so (per-
haps writing an integration test requires you to set up the database, create complex
objects one by one, and so on), it is too easy for you to give up and not do it.
 Writing unit tests tends to be easy most of the time, but it may get complicated
when the class under test requires too much setup or depends on too many other
classes. Integration and system tests also require each test to set up and tear down the
(external) infrastructure.
 Make sure tests are always easy to write. Give developers all the tools to do that. If
tests require a database to be set up, provide developers with an API that requires one
or two method calls and voilà—the database is ready for tests.
 Investing time in writing good test infrastructure is fundamental and pays off in
the long term. Remember the test base classes we created to facilitate SQL integra-
tion tests and all the POs we created to facilitate web testing in chapter 9? This is the
type of infrastructure I am talking about. After the test infrastructure was in place,
the rest was easy. 
10.1.9
Tests should be easy to read
I touched on this point when I said that tests should have a clear reason to fail. I will
reinforce it now. Your test code base will grow significantly. But you probably will not
read it until there is a bug or you add another test to the suite.
 It is well known that developers spend more time reading than writing code. There-
fore, saving reading time will make you more productive. All the things you know about
code readability and use in your production code apply to test code, as well. Do not be
afraid to invest some time in refactoring it. The next developer will thank you.



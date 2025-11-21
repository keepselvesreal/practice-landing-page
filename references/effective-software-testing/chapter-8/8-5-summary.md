# 8.5 Summary (pp.214-215)

---
**Page 214**

214
CHAPTER 8
Test-driven development
Write a program that receives the results of the 10 frames and returns the
game’s final score. Use the TDD cycle: write a test, make it pass, and repeat.
Summary
Writing a test that fails, making it pass, and then refactoring is what test-driven
development is all about.
The red-green-refactor cycle brings different advantages to the coding process,
such as more control over the pace of development, and quick feedback.
All the schools of TDD make sense, and all should be used depending on the
current context.
Empirical research does not find clear benefits from TDD. The current consen-
sus is that working on small parts of a feature and making steady progress makes
developers more productive. Therefore, while TDD is a matter of taste, using
short implementation cycles and testing is the way to go.
Deciding whether to use TDD 100% of the time is also a personal choice. You
should determine when TDD makes you more productive.
Baby steps are key to TDD. Do not be afraid to go slowly when you are in doubt
about what to do next. And do not be afraid to go faster when you feel confident!


---
**Page 215**

215
Writing larger tests
Most of the code we tested in previous chapters could be tested via unit tests. When
that was not possible because, say, the class depended on something else, we used
stubs and mocks to replace the dependency, and we still wrote a unit test. As I said
when we discussed the testing pyramid in chapter 1, I favor unit tests as much as
possible when testing business rules.
 But not everything in our systems can (or should) be tested via unit tests. Writ-
ing unit tests for some pieces of code is a waste of time. Forcing yourself to write
unit tests for them would result in test suites that are not good enough to find bugs,
are hard to write, or are flaky and break when you make small changes in the code.
 This chapter discusses how to identify which parts of the system should be tested
with integration or system tests. Then I will illustrate how I write these tests for three
common situations: (1) components (or sets of classes) that should be exercised
together, because otherwise, the test suite would be too weak; (2) components that
communicate with external infrastructure, such as classes that communicate with
databases and are full of SQL queries; and (3) the entire system, end to end.
This chapter covers
Deciding when to write a larger test
Engineering reliable integration and system tests



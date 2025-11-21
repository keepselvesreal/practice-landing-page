# 3.11 Summary (pp.68-71)

---
**Page 68**

• Use test data that you know is not what a production call would return.
Your test passed neat, whole numbers for latitude and longitude. You
also know Anywhere is not a real city in Colorado. If you were using the
real HttpImpl class, your test expectations would fail.
• The code you’re mocking is getting replaced with a test double and is not
getting tested. A mock represents gaps in test coverage. Make sure you
have an appropriate higher-level test (perhaps an integration test) that
demonstrates end-to-end use of the real class.
• Using DI frameworks can slow down your test runs considerably. Consider
injecting your dependencies by hand—it turns out to be fairly easy to do.
• When using DI frameworks, prefer injecting via a real, exposed interface
point—typically the constructor. Cleverness creates complexity and culti-
vates contempt.
A mock creates a hole in unit testing coverage. Write integration
tests to cover these gaps.
Possibly the most important when it comes to test doubles: avoid using them,
or at least minimize their pervasiveness. If a large number of tests require
test doubles, you’re allowing your troublesome dependencies to proliferate
too much. Reconsider the design.
A couple of avoidance policies:
• Rather than have a class depend on the persistence layer, push the
responsibility out. Have a client retrieve the relevant data, then inject that.
• If collaborator classes don’t have troublesome dependencies, let your tests
interact with their real code rather than mock them.
Mocks are great tools, but they can also create great headaches. Take care.
Summary
In this chapter, you learned the important technique of introducing stubs
and mocks to emulate the behavior of dependent objects. Your tests don’t
have to interact with live services, files, databases, and other troublesome
dependencies! You also learned how to use Mockito to simplify your effort in
creating and injecting mocks.
Chapter 3. Using Test Doubles • 68
report erratum  •  discuss


---
**Page 69**

You also learned Mockito’s core features, but it can do much more:
• Verify that methods were called in order
• Capture and assert against an argument passed to a mock method
• Spy on a method, which results in the real method getting called
Now that you’re empowered with enough unit testing fundamentals to survive,
it’s time to explore some bigger-picture unit testing topics: code coverage,
integration testing, and tests for multithreaded code.
report erratum  •  discuss
Summary • 69


---
**Page 71**

CHAPTER 4
Expanding Your Testing Horizons
At this point, you’ve worked through the core topics in unit testing, including
JUnit and unit testing fundamentals, how to test various scenarios, and how
to use test doubles to deal with dependencies.
In this chapter, you’ll review a few topics that begin to move outside the sphere
of “doing unit testing”:
• Code coverage and how it can help (or hurt)
• Challenges with writing tests for multithreaded code
• Writing integration tests
Improving Unit Testing Skills Using Code Coverage
Code coverage metrics measure the percentage of code that your unit tests
execute (exercise) when run. Ostensibly, code that is covered is working, and
code that is not covered represents the risk of breakage.
From a high level, tests that exhaust all relevant pieces of code provide 100
percent coverage. Code with no tests whatsoever has 0 percent coverage. Most
code lies somewhere in between.
Many tools exist that will calculate coverage metrics for Java code, including
JaCoCo, OpenClover, SonarQube, and Cobertura. IntelliJ IDEA ships with a
coverage tool built into the IDE.
Numerous coverage metrics exist to measure various code aspects. Function
coverage, for example, measures the percentage of functions (methods) exer-
cised by tests. Some of the other metrics include line, statement, branch,
condition, and path coverage.
report erratum  •  discuss



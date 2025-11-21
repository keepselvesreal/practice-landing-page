# 3.10 A Mélange of Important Test Double Tips (pp.67-68)

---
**Page 67**

With an eight-minute suite, you might also concede and run a small subset
after making changes. But you’ll start unwittingly breaking code elsewhere,
not finding out until much later.
Keep your tests fast! Minimize dependencies on code that executes slowly. If
all your tests interact with code that makes one or more database calls,
directly or indirectly, all your tests will be slow.
Fast tests support the most effective way to build software: incrementally.
Testing as you go verifies that each new behavior works and doesn’t break
other code, letting you frequently and confidently integrate code changes.
Fast tests empower continual, confident software development.
A Mélange of Important Test Double Tips
• A good mock-based test is three lines: a one-line arrange step with a
highly readable smart stub declaration, followed by one-line act and assert
steps. That’s a test anyone can quickly read, understand, and trust.
• In answersAppropriateAddressForValidCoordinates, the expected parameter string
of "lat=38.000000&lon=-104.000000" correlates clearly with the act arguments of
38.0 and -104.0. Creating correlation between arrange and assert isn’t easy
sometimes, but it saves developers from digging about for understanding.
Without such correlation, tests using mocks can be hard to follow.
• Mocks supplant real behavior. Ask yourself if you’re using them safely.
Does your mock really emulate the way the production code works? Does
the production code return other formats you’re not thinking of? Does it
throw exceptions? Does it return null? You’ll want a different test for each
of these conditions.
• Does your test really trigger use of a mock, or does it run real production
code? Try turning off the mock and letting your code interact with the
production class to see what happens (it might be as subtle as a slightly
slower test run). Step-debug if needed.
• Try temporarily throwing a runtime exception from the production code.
If your test bombs as a result, you know you’re hitting the production
code. (Don’t forget and accidentally push that throw into production!)
report erratum  •  discuss
A Mélange of Important Test Double Tips • 67


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



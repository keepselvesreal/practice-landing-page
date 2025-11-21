# 5.9 Summary (pp.122-123)

---
**Page 122**

search results (“is that a real test we need to update or do we not need to
worry about it?”), and when you must update them to keep them running
(for example, when a method signature gets changed).
Eliminate tests that verify nothing.
Summary
You’ve learned numerous assertion forms in this chapter. You also learned
about AssertJ, an alternate assertions library.
Initially, you’ll survive if you predominantly use assertEquals for most assertions,
along with an occasional assertTrue or assertFalse. You’ll want to move to the next
level quickly, however, and learn to use the most concise and expressive
assertion for the situation at hand.
Armed with a solid understanding of how to write assertions, you’ll next dig
into the organization of test classes so that you can most effectively run and
maintain related groups of tests.
Chapter 5. Examining Outcomes with Assertions • 122
report erratum  •  discuss


---
**Page 123**

CHAPTER 6
Establishing Organization in JUnit Tests
Your JUnit learnings so far include:
• How to run JUnit and understand its results
• How to group related test methods within a test class
• How to group common test initialization into a @BeforeEach method
• A deep dive into JUnit assertions (the previous chapter)
Generally, you want at least one test class for each production class you
develop. In this chapter, you’ll dig into the topic of test organization within a
test class. You’ll learn about:
• The parts of a test
• Initializing and cleaning up using lifecycle methods
• Grouping related tests with nested classes
• The JUnit test execution lifecycle
• Avoiding dependency challenges by never ordering tests
• Executing multiple test cases for a single test using parameterized tests
The Parts of an Individual Test
A handful of chapters ago (see Scannability: Arrange—Act—Assert, on page
18), you learned how AAA provides a great visual mnemonic to help readers
quickly understand the core parts of a test.
Some developers refer to a “four-phase test,”
1 where each test can be broken
into (wait for it) four parts or phases:
• Set up state/data in what’s sometimes called a fixture. Think of a fixture
as the context in which a test runs—its world, so to speak. The fixture is
1.
http://xunitpatterns.com/Four%20Phase%20Test.html
report erratum  •  discuss



# 6.1 The Parts of an Individual Test (pp.123-124)

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


---
**Page 124**

managed for you by JUnit; you’ll learn more about that in this chapter
as part of the JUnit test execution lifecycle.
• Interact with the system to execute what you want to verify.
• Do the verification (assert).
• Tear down the fixture—clean up any side effects, if necessary. This typi-
cally involves cleaning up resources that a test might have used and that
could impact the execution of other tests. In this chapter, you’ll read
about doing such clean-up with @AfterEach and @AfterAll JUnit hooks.
For every intent and purpose, AAA is the first three parts of a four-part test.
Arrange, act, assert ≈ setup, execute, verify.
Turns out that the fourth part, “tear down,” is and should be rare in unit
tests, in which you seek to avoid (mostly by design) interaction with the things
that you must clean up. If you feel AAA cheats you out of that fourth phase,
you can add a fourth “A”…for ANNIHILATION! (If the violence disturbs you,
just mentally go with “After.” Keep calm and carry on.)
Setting Up and Tearing Down Using Lifecycle Methods
You learned about @BeforeEach in your first JUnit example (see Chapter 1,
Building Your First JUnit Test, on page 3). Let’s take a closer look at this
initialization hook, as well as some other useful hooks that JUnit provides.
Initializing with @BeforeEach and @BeforeAll
In Abstraction: Eliminating Boring Details, on page 20, you learned to use
@BeforeEach to put common initialization in one place. Methods annotated
with @BeforeEach are executed before each test in scope.
JUnit also provides another initialization hook known as @BeforeAll, which you
must declare as a static method. Each method annotated with @BeforeAll gets
executed once per test class and prior to the execution of anything else
within that class. Its primary use is to ensure that slowly executing initializa-
tions (for example, anything involving a database) only have to execute once.
Otherwise, prefer using @BeforeEach.
If you find yourself using @BeforeAll more than once in a blue moon, you may
be testing behaviors bigger than units. That may be okay, but it might suggest
you have opportunities for reducing the dependencies in your system. See
Chapter 3, Using Test Doubles, on page 53 for ideas on how to do that.
Chapter 6. Establishing Organization in JUnit Tests • 124
report erratum  •  discuss



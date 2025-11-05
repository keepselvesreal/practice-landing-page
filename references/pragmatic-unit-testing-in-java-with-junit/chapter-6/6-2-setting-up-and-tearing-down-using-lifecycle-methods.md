# 6.2 Setting Up and Tearing Down Using Lifecycle Methods (pp.124-126)

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


---
**Page 125**

If your test needs demand that you initialize a few things before each test is
run, you can declare multiple @BeforeEach methods in the test class’s scope,
each with a different name. These don’t run in any useful order, just as test
methods do not.
Creating additional @BeforeEach methods allows you to use their methods name
to describe what’s going on in each initialization. Of course, you can also
lump all your initialization into a single @BeforeEach method as long as it’s easy
for other developers to understand what’s going on when reading through
your lump.
You can have multiple (static) @BeforeAll methods in a test class.
Using @AfterEach and @AfterAll for Cleanup
JUnit bookends the initialization hooks @BeforeEach and @BeforeAll with corre-
sponding “teardown” lifecycle methods @AfterEach and @AfterAll. These methods
allow you to clean up resources on test completion. Both @AfterEach and
@AfterAll are guaranteed to run (as long as the JUnit process itself doesn’t
crash), even if any tests throw exceptions.
Within @AfterEach, for example, you might close a database connection or delete
a file. If you write integration (non-unit) tests in JUnit, these teardown hooks
are essential.
Most unit tests, however, shouldn’t interact with code that requires clean-up.
The typical, hopefully rare case is when multiple tests alter the state of a
static field.
If you do have a clean-up need, try to redesign your code to eliminate it. Use
dependency injection (see Injecting Dependencies into Production Code, on
page 56) and/or mock objects (see Chapter 3, Using Test Doubles, on page
53) as appropriate.
Even when you do have a legitimate clean-up need, adding code to @AfterEach
or @AfterAll is mostly only being nice. Suppose the general assumption is that
all tests clean up after themselves—seems like a fair testing standard, yes?
The problem is that eventually, someone will forget to properly clean up in
another test elsewhere. If your test fails as a result, it may take some real
time to figure out which one of possibly thousands of tests is the culprit.
Each of your tests is responsible for ensuring it executes in a
clean, expected state.
report erratum  •  discuss
Setting Up and Tearing Down Using Lifecycle Methods • 125


---
**Page 126**

You can usually design your code so almost no unit tests require clean-up,
but you may still need @AfterEach in a tiny number of places.
Organizing Related Tests into Nested Classes
As your classes grow by taking on more behaviors, you’ll need more and more
tests to describe the new behaviors. Use your test class size as a hint: if you
declare several dozen tests in one test source file, chances are good that the
class under test is too large. Consider splitting the production class up into
two or more classes, which also means you’ll want to split the test methods
across at least two or more test classes.
You may still end up with a couple dozen test methods in one test class. A
larger test class can not only be daunting from a navigational sense, but it
can also make it harder to find all tests that relate to each other.
To help group related tests, you might consider starting each related test’s
name with the same thing. Here are three tests describing how withdrawals
work in the Account class:
@Test void withdrawalReducesAccountBalance() { /* ... */ }
@Test void withdrawalThrowsWhenAmountExceedsBalance() { /* ... */ }
@Test void withdrawalNotifiesIRSWhenAmountExceedsThreshold() { /* ... */ }
A better solution, however, is to group related tests within a JUnit @Nested
class:
@Nested
class Withdrawal {
@Test void reducesAccountBalance() { /* ... */ }
@Test void throwsWhenAmountExceedsBalance() { /* ... */ }
@Test void notifiesIRSWhenAmountExceedsThreshold() { /* ... */ }
}
You can create a number of @Nested classes within your test class, similarly
grouping all methods within it. The name of the nested class, which describes
the common behavior, can be removed from each test name.
You can also use @Nested classes to group tests by context—the state estab-
lished by the arrange part of a test. For example:
class AnAccount
@Nested
class WithZeroBalance {
@Test void doesNotAccrueInterest() { /* ... */ }
@Test void throwsOnWithdrawal() { /* ... */ }
}
Chapter 6. Establishing Organization in JUnit Tests • 126
report erratum  •  discuss



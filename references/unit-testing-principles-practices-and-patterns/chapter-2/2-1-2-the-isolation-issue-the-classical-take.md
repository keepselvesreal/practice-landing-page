# 2.1.2 The isolation issue: The classical take (pp.27-30)

---
**Page 27**

27
The definition of “unit test”
 The assertion phase has changed too, and that’s where the key difference lies. We
still check the output from customer.Purchase as before, but the way we verify that
the customer did the right thing to the store is different. Previously, we did that by
asserting against the store’s state. Now, we examine the interactions between Customer
and Store: the tests check to see if the customer made the correct call on the store.
We do this by passing the method the customer should call on the store (x.Remove-
Inventory) as well as the number of times it should do that. If the purchases succeeds,
the customer should call this method once (Times.Once). If the purchases fails, the
customer shouldn’t call it at all (Times.Never). 
2.1.2
The isolation issue: The classical take
To reiterate, the London style approaches the isolation requirement by segregating the
piece of code under test from its collaborators with the help of test doubles: specifically,
mocks. Interestingly enough, this point of view also affects your standpoint on what con-
stitutes a small piece of code (a unit). Here are all the attributes of a unit test once again:
A unit test verifies a small piece of code (a unit),
Does it quickly,
And does it in an isolated manner.
In addition to the third attribute leaving room for interpretation, there’s some room
in the possible interpretations of the first attribute as well. How small should a small
piece of code be? As you saw from the previous section, if you adopt the position of
isolating every individual class, then it’s natural to accept that the piece of code under
test should also be a single class, or a method inside that class. It can’t be more than
that due to the way you approach the isolation issue. In some cases, you might test a
couple of classes at once; but in general, you’ll always strive to maintain this guideline
of unit testing one class at a time.
 As I mentioned earlier, there’s another way to interpret the isolation attribute—
the classical way. In the classical approach, it’s not the code that needs to be tested in
an isolated manner. Instead, unit tests themselves should be run in isolation from
each other. That way, you can run the tests in parallel, sequentially, and in any order,
whatever fits you best, and they still won’t affect each other’s outcome.
 Isolating tests from each other means it’s fine to exercise several classes at once as
long as they all reside in the memory and don’t reach out to a shared state, through
which the tests can communicate and affect each other’s execution context. Typical
examples of such a shared state are out-of-process dependencies—the database, the
file system, and so on.
 For instance, one test could create a customer in the database as part of its arrange
phase, and another test would delete it as part of its own arrange phase, before the
first test completes executing. If you run these two tests in parallel, the first test will
fail, not because the production code is broken, but rather because of the interfer-
ence from the second test.


---
**Page 28**

28
CHAPTER 2
What is a unit test?
This take on the isolation issue entails a much more modest view on the use of mocks
and other test doubles. You can still use them, but you normally do that for only those
dependencies that introduce a shared state between tests. Figure 2.3 shows how it looks.
 Note that shared dependencies are shared between unit tests, not between classes
under test (units). In that sense, a singleton dependency is not shared as long as you
are able to create a new instance of it in each test. While there’s only one instance of a
Shared, private, and out-of-process dependencies 
A shared dependency is a dependency that is shared between tests and provides
means for those tests to affect each other’s outcome. A typical example of shared
dependencies is a static mutable field. A change to such a field is visible across all
unit tests running within the same process. A database is another typical example of
a shared dependency.
A private dependency is a dependency that is not shared.
An out-of-process dependency is a dependency that runs outside the application’s
execution process; it’s a proxy to data that is not yet in the memory. An out-of-process
dependency corresponds to a shared dependency in the vast majority of cases, but
not always. For example, a database is both out-of-process and shared. But if you
launch that database in a Docker container before each test run, that would make
this dependency out-of-process but not shared, since tests no longer work with the
same instance of it. Similarly, a read-only database is also out-of-process but not
shared, even if it’s reused by tests. Tests can’t mutate data in such a database and
thus can’t affect each other’s outcome.
Private dependency; keep
Shared dependency; replace
File system
System under test
Database
Test
Shared dependency; replace
Another class
Figure 2.3
Isolating unit tests from each other entails isolating the class under test 
from shared dependencies only. Private dependencies can be kept intact.


---
**Page 29**

29
The definition of “unit test”
singleton in the production code, tests may very well not follow this pattern and not
reuse that singleton. Thus, such a dependency would be private.
 For example, there’s normally only one instance of a configuration class, which is
reused across all production code. But if it’s injected into the SUT the way all other
dependencies are, say, via a constructor, you can create a new instance of it in each
test; you don’t have to maintain a single instance throughout the test suite. You can’t
create a new file system or a database, however; they must be either shared between
tests or substituted away with test doubles.
Another reason for substituting shared dependencies is to increase the test execution
speed. Shared dependencies almost always reside outside the execution process, while
private dependencies usually don’t cross that boundary. Because of that, calls to
shared dependencies, such as a database or the file system, take more time than calls
to private dependencies. And since the necessity to run quickly is the second attribute
of the unit test definition, such calls push the tests with shared dependencies out of
the realm of unit testing and into the area of integration testing. I talk more about
integration testing later in this chapter.
 This alternative view of isolation also leads to a different take on what constitutes a
unit (a small piece of code). A unit doesn’t necessarily have to be limited to a class.
Shared vs. volatile dependencies 
Another term has a similar, yet not identical, meaning: volatile dependency. I recom-
mend Dependency Injection: Principles, Practices, Patterns by Steven van Deursen and
Mark Seemann (Manning Publications, 2018) as a go-to book on the topic of depen-
dency management.
A volatile dependency is a dependency that exhibits one of the following properties:
It introduces a requirement to set up and configure a runtime environment in
addition to what is installed on a developer’s machine by default. Databases
and API services are good examples here. They require additional setup and
are not installed on machines in your organization by default.
It contains nondeterministic behavior. An example would be a random num-
ber generator or a class returning the current date and time. These depen-
dencies are non-deterministic because they provide different results on each
invocation.
As you can see, there’s an overlap between the notions of shared and volatile depen-
dencies. For example, a dependency on the database is both shared and volatile. But
that’s not the case for the file system. The file system is not volatile because it is
installed on every developer’s machine and it behaves deterministically in the vast
majority of cases. Still, the file system introduces a means by which the unit tests
can interfere with each other’s execution context; hence it is shared. Likewise, a ran-
dom number generator is volatile, but because you can supply a separate instance
of it to each test, it isn’t shared.


---
**Page 30**

30
CHAPTER 2
What is a unit test?
You can just as well unit test a group of classes, as long as none of them is a shared
dependency. 
2.2
The classical and London schools of unit testing
As you can see, the root of the differences between the London and classical schools is
the isolation attribute. The London school views it as isolation of the system under test
from its collaborators, whereas the classical school views it as isolation of unit tests
themselves from each other.
 This seemingly minor difference has led to a vast disagreement about how to
approach unit testing, which, as you already know, produced the two schools of thought.
Overall, the disagreement between the schools spans three major topics:
The isolation requirement
What constitutes a piece of code under test (a unit)
Handling dependencies
Table 2.1 sums it all up.
2.2.1
How the classical and London schools handle dependencies
Note that despite the ubiquitous use of test doubles, the London school still allows
for using some dependencies in tests as-is. The litmus test here is whether a depen-
dency is mutable. It’s fine not to substitute objects that don’t ever change—
immutable objects.
 And you saw in the earlier examples that, when I refactored the tests toward the
London style, I didn’t replace the Product instances with mocks but rather used
the real objects, as shown in the following code (repeated from listing 2.2 for your
convenience):
[Fact]
public void Purchase_fails_when_not_enough_inventory()
{
// Arrange
var storeMock = new Mock<IStore>();
storeMock
.Setup(x => x.HasEnoughInventory(Product.Shampoo, 5))
.Returns(false);
var customer = new Customer();
Table 2.1
The differences between the London and classical schools of unit testing, summed up by the
approach to isolation, the size of a unit, and the use of test doubles
Isolation of
A unit is
Uses test doubles for
London school
Units
A class
All but immutable dependencies
Classical school
Unit tests
A class or a set of classes
Shared dependencies



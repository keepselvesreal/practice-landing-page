# 2.2.1 How the classical and London schools handle dependencies (pp.30-34)

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


---
**Page 31**

31
The classical and London schools of unit testing
// Act
bool success = customer.Purchase(storeMock.Object, Product.Shampoo, 5);
// Assert
Assert.False(success);
storeMock.Verify(
x => x.RemoveInventory(Product.Shampoo, 5),
Times.Never);
}
Of the two dependencies of Customer, only Store contains an internal state that can
change over time. The Product instances are immutable (Product itself is a C#
enum). Hence I substituted the Store instance only.
 It makes sense, if you think about it. You wouldn’t use a test double for the 5
number in the previous test either, would you? That’s because it is also immutable—
you can’t possibly modify this number. Note that I’m not talking about a variable
containing the number, but rather the number itself. In the statement Remove-
Inventory(Product.Shampoo, 5), we don’t even use a variable; 5 is declared right
away. The same is true for Product.Shampoo.
 Such immutable objects are called value objects or values. Their main trait is that
they have no individual identity; they are identified solely by their content. As a corol-
lary, if two such objects have the same content, it doesn’t matter which of them you’re
working with: these instances are interchangeable. For example, if you’ve got two 5
integers, you can use them in place of one another. The same is true for the products
in our case: you can reuse a single Product.Shampoo instance or declare several of
them—it won’t make any difference. These instances will have the same content and
thus can be used interchangeably.
 Note that the concept of a value object is language-agnostic and doesn’t require a
particular programming language or framework. You can read more about value
objects in my article “Entity vs. Value Object: The ultimate list of differences” at
http://mng.bz/KE9O.
 Figure 2.4 shows the categorization of dependencies and how both schools of unit
testing treat them. A dependency can be either shared or private. A private dependency, in
turn, can be either mutable or immutable. In the latter case, it is called a value object. For
example, a database is a shared dependency—its internal state is shared across all
automated tests (that don’t replace it with a test double). A Store instance is a private
dependency that is mutable. And a Product instance (or an instance of a number 5,
for that matter) is an example of a private dependency that is immutable—a value
object. All shared dependencies are mutable, but for a mutable dependency to be
shared, it has to be reused by tests.
 
 
 
 


---
**Page 32**

32
CHAPTER 2
What is a unit test?
I’m repeating table 2.1 with the differences between the schools for your convenience.
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
Collaborator vs. dependency
A collaborator is a dependency that is either shared or mutable. For example, a class
providing access to the database is a collaborator since the database is a shared
dependency. Store is a collaborator too, because its state can change over time.
Product and number 5 are also dependencies, but they’re not collaborators. They’re
values or value objects.
A typical class may work with dependencies of both types: collaborators and values.
Look at this method call:
customer.Purchase(store, Product.Shampoo, 5)
Here we have three dependencies. One of them (store) is a collaborator, and the
other two (Product.Shampoo, 5) are not.
Private
Value object
Mutable
Collaborator,
replaced in the
London school
Replaced in the
classic school
Shared
Dependency
Figure 2.4
The hierarchy of dependencies. The classical school advocates for 
replacing shared dependencies with test doubles. The London school advocates for the 
replacement of private dependencies as well, as long as they are mutable.


---
**Page 33**

33
The classical and London schools of unit testing
And let me reiterate one point about the types of dependencies. Not all out-of-process
dependencies fall into the category of shared dependencies. A shared dependency
almost always resides outside the application’s process, but the opposite isn’t true (see
figure 2.5). In order for an out-of-process dependency to be shared, it has to provide
means for unit tests to communicate with each other. The communication is done
through modifications of the dependency’s internal state. In that sense, an immutable
out-of-process dependency doesn’t provide such a means. The tests simply can’t mod-
ify anything in it and thus can’t interfere with each other’s execution context.
For example, if there’s an API somewhere that returns a catalog of all products the orga-
nization sells, this isn’t a shared dependency as long as the API doesn’t expose the
functionality to change the catalog. It’s true that such a dependency is volatile and sits
outside the application’s boundary, but since the tests can’t affect the data it returns, it
isn’t shared. This doesn’t mean you have to include such a dependency in the testing
scope. In most cases, you still need to replace it with a test double to keep the test fast.
But if the out-of-process dependency is quick enough and the connection to it is stable,
you can make a good case for using it as-is in the tests.
 Having that said, in this book, I use the terms shared dependency and out-of-process
dependency interchangeably unless I explicitly state otherwise. In real-world projects,
you rarely have a shared dependency that isn’t out-of-process. If a dependency is in-
process, you can easily supply a separate instance of it to each test; there’s no need to
share it between tests. Similarly, you normally don’t encounter an out-of-process
Shared
dependencies
Out-of-process
dependencies
Singleton
Database
Read-only API service
Figure 2.5
The relation between shared and out-of-process dependencies. An example of a 
dependency that is shared but not out-of-process is a singleton (an instance that is reused by 
all tests) or a static field in a class. A database is shared and out-of-process—it resides outside 
the main process and is mutable. A read-only API is out-of-process but not shared, since tests 
can’t modify it and thus can’t affect each other’s execution flow.


---
**Page 34**

34
CHAPTER 2
What is a unit test?
dependency that’s not shared. Most such dependencies are mutable and thus can be
modified by tests.
 With this foundation of definitions, let’s contrast the two schools on their merits. 
2.3
Contrasting the classical and London schools 
of unit testing
To reiterate, the main difference between the classical and London schools is in how
they treat the isolation issue in the definition of a unit test. This, in turn, spills over to
the treatment of a unit—the thing that should be put under test—and the approach
to handling dependencies.
 As I mentioned previously, I prefer the classical school of unit testing. It tends to
produce tests of higher quality and thus is better suited for achieving the ultimate goal
of unit testing, which is the sustainable growth of your project. The reason is fragility:
tests that use mocks tend to be more brittle than classical tests (more on this in chap-
ter 5). For now, let’s take the main selling points of the London school and evaluate
them one by one.
 The London school’s approach provides the following benefits:
Better granularity. The tests are fine-grained and check only one class at a time.
It’s easier to unit test a larger graph of interconnected classes. Since all collaborators
are replaced by test doubles, you don’t need to worry about them at the time of
writing the test.
If a test fails, you know for sure which functionality has failed. Without the class’s
collaborators, there could be no suspects other than the class under test itself.
Of course, there may still be situations where the system under test uses a
value object and it’s the change in this value object that makes the test fail.
But these cases aren’t that frequent because all other dependencies are elimi-
nated in tests.
2.3.1
Unit testing one class at a time
The point about better granularity relates to the discussion about what constitutes a
unit in unit testing. The London school considers a class as such a unit. Coming from
an object-oriented programming background, developers usually regard classes as the
atomic building blocks that lie at the foundation of every code base. This naturally
leads to treating classes as the atomic units to be verified in tests, too. This tendency is
understandable but misleading.
TIP
Tests shouldn’t verify units of code. Rather, they should verify units of
behavior: something that is meaningful for the problem domain and, ideally,
something that a business person can recognize as useful. The number of
classes it takes to implement such a unit of behavior is irrelevant. The unit
could span across multiple classes or only one class, or even take up just a
tiny method.



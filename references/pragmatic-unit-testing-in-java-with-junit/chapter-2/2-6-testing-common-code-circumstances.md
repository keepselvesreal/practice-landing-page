# 2.6 Testing Common Code Circumstances (pp.41-51)

---
**Page 41**

Testing Common Code Circumstances
As you write more tests, you’ll realize that you’re often facing a number of
common circumstances. Here’s a handful of them:
• Add an item to a list
• Do something if a conditional is met
• Update all items in a list that match a predicate
• Remove all items matching a predicate from a list
• Throw an exception when a conditional is met
Lists and other collection types are a heavy part of most software development.
You should be able to bang out tests involving lists without much thought.
In this section, you’ll work through how you might write tests for each of
those common needs. Hopefully, these examples will help you extrapolate
and learn to write tests for other data structures (Maps, Sets, arrays, etc.) and
operations (loops, streams, math, etc.).
Add an Item to a List
Here’s some trivial code for a container class—DestinationList—that allows clients
to add FixedLocation objects to it, one by one.
utj3-units/06/src/main/java/units/DestinationList.java
import java.util.ArrayList;
import java.util.List;
public class DestinationList {
private List<FixedLocation> locations = new ArrayList<>();
public void add(FixedLocation location) {
locations.add(location);
}
public List<FixedLocation> getLocations() {
return locations;
}
}
At a glance, you pretty much know the code in DestinationList works. Doesn’t matter,
though—it’s always possible for such a small amount of code to hide a mistake.
The singular concept implemented in DestinationList—adding a location—involves
three separate code points: a method to add the location to a list, a field that
creates and initializes the list, and a method that returns the list. That lack
of concision only increases the possibility of a defect.
DestinationList will change and grow as requirements for “add location” change
or as other behaviors are added. Defects will be increasingly harder to spot.
report erratum  •  discuss
Testing Common Code Circumstances • 41


---
**Page 42**

Start testing now, before that “obvious” code sinks into a sea of “I’m not sure
exactly what’s going on!”
The Z in ZOM provides a good starting point and results in a guardrail test
that will forever protect you:
utj3-units/06/src/test/java/units/ADestinationList.java
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;
import static units.FixedLocation.Heading.East;
import static units.FixedLocation.Heading.North;
class ADestinationList {
private DestinationList list;
@BeforeEach
void create() {
list = new DestinationList();
}
@Test
void isEmptyWhenCreated() {
assertTrue(list.getLocations().isEmpty());
}
}
Do you really need both one and many tests? The only interesting behavior
you’ve coded is your call to the add method defined on ArrayList:
utj3-units/06/src/main/java/units/DestinationList.java
locations.add(location);
You trust ArrayList and its ability to support one location or scads of them.
None of your code (for now) does anything differently when only one location
is involved. Move directly to adding a many test:
utj3-units/06/src/test/java/units/ADestinationList.java
@Test
void allowsAddingLocations() {
list.add(new FixedLocation(1, 2, North));
list.add(new FixedLocation(1, 3, East));
assertEquals(
List.of(
new FixedLocation(1, 2, North),
new FixedLocation(1, 3, East)),
list.getLocations());
}
Chapter 2. Testing the Building Blocks • 42
report erratum  •  discuss


---
**Page 43**

While it looks cut-and-dry, allowsAddingLocations involves some choices worth
discussing. The test contains only two visual chunks. The second chunk
represents the assert step, of course. Its assertion compares the result of
calling getLocations to a List of two FixedLocation objects. The two objects in this
comparison list are instantiated inline with the exact same values as when
you constructed them in the arrange step.
In the assert, you are calling getLocations. By doing so, you are implying that
getLocations isn’t really what you’re trying to verify (it’s just an accessor), but
you’re instead using it to support your need to inspect the locations list.
Is the first chunk the arrange step or the act step? The test name says what
behavior your test is trying to verify—the act of adding locations. That the
two statements in the first chunk trigger the add behavior on the list means
that they represent your act step. It’s a subtle distinction. Some developers
might consider the first chunk to be the test’s arrange step, and maybe that’s
okay, but then there’s no act step. It ain’t much of a test without an act step.
The redundant FixedLocation instantiations may compel you to introduce a
couple of local variables to help clarify the test. Creating such test objects can
make it easier to correlate your test’s inputs to the expected outcomes:
utj3-units/07/src/test/java/units/ADestinationList.java
@Test
void allowsAddingLocations() {
var locationOne = new FixedLocation(1, 2, North);
var locationTwo = new FixedLocation(1, 3, East);
list.add(locationOne);
list.add(locationTwo);
assertEquals(List.of(locationOne, locationTwo), list.getLocations());
}
Test objects are particularly useful when most, if not all, tests involve them.
You can declare them as test-class-level constants with more memorable,
domain-appropriate names:
utj3-units/08/src/test/java/units/ADestinationList.java
static final FixedLocation ORIGIN = new FixedLocation(0, 0, East);
static final FixedLocation NORTHEAST = new FixedLocation(3, 3, North);
@Test
void allowsAddingLocations() {
list.add(ORIGIN);
list.add(NORTHEAST);
assertEquals(List.of(ORIGIN, NORTHEAST), list.getLocations());
}
report erratum  •  discuss
Testing Common Code Circumstances • 43


---
**Page 44**

Such test objects also help de-emphasize details where they don’t matter.
That the northeast location is at (3, 3) and facing north is irrelevant in your
allowsAddingLocations test. It only matters that NORTHEAST references an object
distinct from ORIGIN.
Useful here, yet creating sample objects can be overkill. It’s often easier to
eyeball-compare the data by looking back and forth between the arrange and
assert statements. As long as test intent remains clear, such trimmer tests
can speed up efforts in both writing and understanding.
utj3-units/09/src/test/java/units/ADestinationList.java
@Test
void doesNotAddLocationAlreadyContained() {
list.add(new FixedLocation(0, 0, East));
list.add(new FixedLocation(3, 3, North));
list.add(new FixedLocation(0, 0, East));
assertEquals(
List.of(new FixedLocation(0, 0, East),
new FixedLocation(3, 3, North)),
list.getLocations());
}
Any of the three forms (raw inline declarations, locally declared test objects,
and globally accessible test objects) is acceptable. Here, the inline declarations
clutter the tests a little too much. For now, use the constants.
Do Something if a Conditional Is Met
If the code you’re testing involves a conditional (an if statement), you need at
least two sets of tests: one set involving all the ways that the conditional can
pass (in other words, return true), and one set involving all the ways that it
can fail (return false). That way, your tests will cover both what happens if the
if block executes and what happens if it does not.
A common behavioral need is to ensure that a collection doesn’t take on
duplicate elements. Here’s a change to DestinationList that introduces such a
conditional to the add method:
utj3-units/09/src/main/java/units/DestinationList.java
public void add(FixedLocation location) {
if (locations.contains(location)) return;
locations.add(location);
}
You already have one test that allows adding objects. Here it is again:
Chapter 2. Testing the Building Blocks • 44
report erratum  •  discuss


---
**Page 45**

utj3-units/09/src/test/java/units/ADestinationList.java
@Test
void allowsAddingLocations() {
list.add(ORIGIN);
list.add(NORTHEAST);
assertEquals(List.of(ORIGIN, NORTHEAST), list.getLocations());
}
The distinct names ORIGIN and DESTINATION imply that the two sample objects
are distinct from each other. Write an additional test that involves attempting
to add one of them, ORIGIN, a second time:
utj3-units/09/src/test/java/units/ADestinationList.java
@Test
void doesNotAddLocationWhenAlreadyContained() {
list.add(ORIGIN);
list.add(NORTHEAST);
list.add(ORIGIN);
assertEquals(List.of(ORIGIN, NORTHEAST), list.getLocations());
}
A final note on the Arrange—Act—Assert (AAA) organization here: you are
still trying to verify the behavior of adding (or not adding) locations. The first
two lines in the test arrange things by adding a couple of locations. You then
see the act step that isolates the addition of a duplicate location. This breakout
helps readers focus on how to trigger the happy path of the if statement—you
attempt to add an object whose details match those of one already added.
Update All Items in a List That Match a Predicate
The job of the method moveLocationsWithHeading is to iterate all locations and
update those whose heading matches a target (passed-in) heading. The update
involves changing to new x and y coordinates.
A map operation suits your needs. Each location is mapped either to the same
location, if its heading does not match, or to a new FixedLocation with updated
coordinates (since FixedLocations are immutable). The collected stream is then
assigned back to the DestinationList’s locations field.
utj3-units/09/src/main/java/units/DestinationList.java
public void moveLocationsWithHeading(Heading heading, int x, int y) {
this.locations = locations.stream()
.map(location -> location.heading().equals(heading)
? new FixedLocation(x, y, heading)
: location)
.toList();
}
report erratum  •  discuss
Testing Common Code Circumstances • 45


---
**Page 46**

Here’s an approach for testing the moveLocationsWithHeading:
• Create a list with two FixedLocation objects, one with the heading you want
to target (for example, East). The other object should have a different
heading.
• Call the method moveLocationsWithHeading and pass it the targeted heading
(East); also pass new values for x and y.
• Ensure that the updated list in DestinationList contains a list of two elements.
The location with the targeted location should reflect the new x and y
values; the other location should remain unchanged.
Here’s what the new test looks like:
utj3-units/09/src/test/java/units/ADestinationList.java
@Test
void updatesMatchingLocationsWithNewCoordinates() {
list.add(new FixedLocation(0, 0, East));
list.add(new FixedLocation(1, 1, North));
list.moveLocationsWithHeading(East, 2, 3);
assertEquals(List.of(
new FixedLocation(2, 3, East),
new FixedLocation(1, 1, North)),
list.getLocations());
}
You’ll note you’re not using test objects here. Test objects de-emphasize most
details, but for this test, you need to show whether specific values (x and y)
change, or don’t, based on another value (the heading). By directly instantiat-
ing FixedLocation objects, you can visually correlate the details between arrange
inputs and assert expected outputs.
Remove All Items Matching a Predicate from a List
Another method on DestinationList allows clients to remove all locations that
exceed a specified distance from a point:
utj3-units/09/src/main/java/units/DestinationList.java
public void removeLocationsFurtherThan(int x, int y, int distance) {
this.locations = locations.stream()
.filter(location -> distanceBetween(location, x, y) < distance)
.toList();
}
private double distanceBetween(FixedLocation point, int x, int y) {
return Math.sqrt(
Math.pow(x - point.x(), 2) + Math.pow(y - point.y(), 2));
}
Chapter 2. Testing the Building Blocks • 46
report erratum  •  discuss


---
**Page 47**

Your test looks similar to the test for moveLocationsWithHeading. It creates three
locations, two of which have a distance from (0, 0) that is greater than the
value of 9 passed in the act step. The assertion verifies that only the location
with a shorter distance remains.
utj3-units/09/src/test/java/units/ADestinationList.java
@Test
void retainsLocationsLessThanDistance() {
list.add(new FixedLocation(0, 5, North));
➤
list.add(new FixedLocation(0, 10, North));
➤
list.add(new FixedLocation(0, 15, North));
➤
list.removeLocationsFurtherThan(0, 0, 9);
assertEquals(List.of(
new FixedLocation(0, 5, North)),
list.getLocations());
}
This test purposefully uses simplistic test data. Each of the three highlighted
locations added as part of arranging the test is on the vertical (y) axis. As a
result, the distance between each location and (0, 0) (the passed-in point) is
the same as its y coordinate.
The simple-data approach to removeLocationsFurtherThan keeps the test easy to
understand, but it means you’re ignoring the complexity in distanceBetween.
That means you’ll need to demonstrate that the logic in distanceBetween is correct
for non-zero values of x.
You have a few options for verifying the distance calculations:
• You can write more tests that interact with removeLocationsFurtherThan. These
tests represent a slightly indirect way to verify the distance calculation
and demand a few more lines of code.
• You can expose distanceBetween as a package-level method, which would
allow ADestinationList to directly test it. But distanceBetween as a concept is out
of place in DestinationList. The job of DestinationList is to manage a list of desti-
nations, not to calculate distances between a FixedLocation and a point.
• You can make distanceBetween a concept better associated with FixedLocation,
and move the method to that class. After moving the method, you can
test it directly in FixedLocation.
report erratum  •  discuss
Testing Common Code Circumstances • 47


---
**Page 48**

Here’s the relevant code after the move:
utj3-units/10/src/main/java/units/DestinationList.java
public void removeLocationsFurtherThan(int x, int y, int distance) {
this.locations = locations.stream()
.filter(location -> location.distanceFrom(x, y) < distance)
➤
.toList();
}
utj3-units/10/src/main/java/units/FixedLocation.java
double distanceFrom(int x, int y) {
return Math.sqrt(Math.pow(x - x(), 2) + Math.pow(y - y(), 2));
}
In the context of FixedLocation, the method name distanceBetween could use a little
improvement. It’s been renamed to distanceFrom here. (A trick for deriving names:
utter the phrase that describes how the method is used in context, for
example, “we ask for the distance from a fixed location for a point.”)
Now, you can quickly write a number of very focused tests that exhaust your
ideas about how to test the distance calculation:
utj3-units/10/src/test/java/units/AFixedLocation.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static units.FixedLocation.Heading.*;
public class AFixedLocation {
final static FixedLocation.Heading h = North;
@Test
void is0WhenCoordinatesAreTheSame() {
assertEquals(0, new FixedLocation(1, 2, h).distanceFrom(1, 2));
}
@Test
void is5InClassicHypotenuseCase() {
assertEquals(5.0, new FixedLocation(0, 0, h).distanceFrom(3, 4));
}
@Test
void isNearSomeDoubleValue() {
assertEquals(5.6568, new FixedLocation(10, 13, h).distanceFrom(14, 9),
0.0001);
}
@Test
void worksWithNegativeNumbers() {
assertEquals(23.7697,
new FixedLocation(-7, 13, h).distanceFrom(2, -9),
0.0001);
}
}
Chapter 2. Testing the Building Blocks • 48
report erratum  •  discuss


---
**Page 49**

The first two tests verify the zero case and a simple example. The last two
involve distance calculations that return interesting floating point quantities.
(Stylistic note: since the heading is irrelevant to these tests, naming it h helps
de-emphasize it.)
Assertions against code involving complex calculations too often provide
insufficient insight into what the code is doing. The expected value is mathe-
matically correct, but there’s no easy way to correlate it to the input values
from just reading the act and assert.
To derive the expected value for such a calculation, you can hand-calculate
it. You can also cross-check by using an independent source for verification,
such as an online app.
Due to limitations on how floating point values are captured, comparing two
floating point values can result in unexpected discrepancies. For this reason,
JUnit provides a form of assertEquals that takes a delta value as the third
argument. This delta represents a tolerance. How much can the two numbers
be off before JUnit fails the assertion?
In the test, define a heading constant arbitrarily set to North. While the heading
is required each time you construct a FixedLocation, it’s completely irrelevant
to the tests. Name this constant h, to de-emphasize the constructor argument
and thus minimize the clutter it otherwise adds to the tests.
Throw an Exception When a Conditional Is Met
In Chapter 1, Building Your First JUnit Test, on page 3, you wrote tests for
arithmeticMean in CreditHistory. The first test you wrote was a zero case:
utj3-credit-history/10/src/test/java/credit/ACreditHistory.java
@Test
void withNoCreditRatingsHas0Mean() {
var result = creditHistory.arithmeticMean();
assertEquals(0, result);
}
That test described and verified the highlighted behavior in arithmeticMean:
utj3-credit-history/10/src/main/java/credit/CreditHistory.java
public int arithmeticMean() {
if (ratings.isEmpty()) return 0;
➤
var total = ratings.stream().mapToInt(CreditRating::rating).sum();
return total / ratings.size();
}
report erratum  •  discuss
Testing Common Code Circumstances • 49


---
**Page 50**

You’ve been asked to change the code—oh no! The product owner has been
schooled by a mathematician and wants arithmeticMean to throw an exception
when there are no credit ratings.
Pretend to panic for a moment (“But I’ll have to retest everything!”), then make
the trivial change:
utj3-credit-history/11/src/main/java/credit/CreditHistory.java
public int arithmeticMean() {
if (ratings.isEmpty()) throw new IllegalStateException();
➤
var total = ratings.stream().mapToInt(CreditRating::rating).sum();
return total / ratings.size();
}
Because you changed your code, run your tests. Hope at least one test will
fail due to your change of the behavior that the tests cover. Dream that only
the test ACreditHistory::withNoCreditRatingsHas0Mean fails since it’s the only test
directly related to the changed behavior. Rejoice when your hopes and dreams
(paltry as they are) come true: withNoCreditRatingsHas0Mean fails and for the right
reason—an IllegalStateException was thrown. Hooray!
The desired behavior is in place. A test is failing. Time to fix the incorrect test.
JUnit 5 gives you a way to verify that a piece of test code throws an exception:
utj3-credit-history/12/src/test/java/credit/ACreditHistory.java
@Test
void withNoCreditRatingsThrows() {
assertThrows(IllegalStateException.class,
() -> creditHistory.arithmeticMean());
}
In its simplest form, JUnit’s assertThrows method takes on two arguments. The
first represents the type of exception you expect to be thrown (IllegalStateExcep-
tion.class in this case). The second argument is a lambda whose body contains
the code that you expect will throw the appropriate exception. In your case,
you’re expecting the call to arithmeticMean to throw the exception.
When handling an assertThrows statement within a test, JUnit executes the
lambda in the context of a try/catch block. If the lambda barfs an exception,
the catch block catches the barfage and JUnit marks the test as passing as
long as the exception type matches. Otherwise, JUnit marks the test as a
failure since no exception was thrown.
Because your requirements changed, you updated the code and then verified
that your change broke a specific test. That seems so…reactionary. Maybe
you should take control of things.
Chapter 2. Testing the Building Blocks • 50
report erratum  •  discuss


---
**Page 51**

If you view the unit tests as a way of characterizing all your code units, collec-
tively they become the requirements in an odd but useful little “requirements
by example” manner. Your test names describe the behavioral needs. Each
test provides an example of one of those behaviors.
Such well-named requirements-by-example (tests) can quickly answer ques-
tions others (or even you) might ask: “hey, what does the system do when we
try to calculate the arithmetic mean and there are no credit ratings?” Everyone
is happy, you have an immediate answer, and you’re highly confident it’s
correct because all of your tests are passing.
One way to take control: invert your approach to unit testing—drive a
requirements change by first updating the tests that relate to the change.
After observing that the updated tests fail (because you’ve not yet updated
the system with the new requirement), you can make the necessary changes
and then run all tests to ensure you’re still happy.
Once you feel increased control by test-driving changes, your next thought
might be, “what if I drove in all new functionality this way?” You can, and
doing so is known as Test-Driven Development (TDD). See Chapter 11,
Advancing with Test-Driven Development (TDD), on page 211 for a rundown
of what TDD looks like and why it might help even more. Get a little excited
about it—because TDD is also a lot of fun—but for now, you should continue
your unit testing journey.
Testing that an exception is thrown when expected is as important as testing
any other code. You’ll also want to verify that other code responds properly
to the situation when an exception is thrown. Doing so is a slightly trickier
technique; visit Testing Exception Handling, on page 65 for details.
Exploring Boundaries with CORRECT
The zero, one, many, and exception-based tests will cover most of your typical
needs when testing code. But you’ll also want to consider adding tests for
cases that a happy path through the code might not hit. These boundary
conditions represent scenarios that involve the edges of the input domain.
You can employ the CORRECT acronym, devised by Andy Hunt and Dave
Thomas for the first edition of this book [HT03], to help you think about
potential boundary conditions. For each of these items, consider whether or
not similar conditions can exist in the method that you want to test and what
might happen if these conditions are violated:
report erratum  •  discuss
Exploring Boundaries with CORRECT • 51



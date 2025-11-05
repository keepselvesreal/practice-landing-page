# Testing the Building Blocks (pp.25-53)

---
**Page 25**

CHAPTER 2
Testing the Building Blocks
In the previous chapter, you took a small piece of code and wrote a few JUnit
tests around it. In the process, you learned how to structure your tests, exe-
cute them, how to interpret results, and what test to write next.
You’ve only scratched the surface of what it means to write tests for code. In
this chapter, you’ll examine several common code constructs and learn how
to test them. These are the topics you’ll cover:
• Testing pure functions
• Testing code with side effects
• How different designs can impact unit tests
• Writing tests for code involving lists
• Writing tests for code that throws exceptions
• Covering boundary conditions with tests
First, however, let’s talk about the word unit in unit test.
Units
A software system is an organized collection of many units. A unit is the
smallest piece of code that accomplishes a specific behavioral goal—a concept.
Here are some examples of concepts:
• Capitalize the first letter of a word
• Move a passenger from the standby list to the boarding list
• Mark a passenger as upgraded
• Calculate the mean credit rating for an individual
• Throw an exception when a user is under 18 years old
report erratum  •  discuss


---
**Page 26**

Concepts can also represent generic or very common ideas in software:
• Add an item to a list
• Remove all items matching a predicate from a list
• Throw an exception when a string is non-numeric
Each of the above concepts requires perhaps one to three or four “atomic
code concepts.” Think of an atomic code concept (let’s call it an ACC) as
closer to an expression—the biggest chunk of code that you can read and
understand at a glance. Each additional statement represents an additional
ACC, as does each new lambda or function call in a pipeline.
An if statement with a single-line body would count as two ACCs: the condi-
tional plus the statement that executes if it evaluates to true. The key notion
is that both parts of the if must be read and understood separately.
A concise implementation of a concept uses no more ACCs than
needed.
Of course, you’ll inevitably need to implement concepts requiring a handful
or more ACCs. But for now, let’s establish a fairly sensitive and arbitrary
threshold. If your method requires five or more ACCs, consider the possibility
that it’s larger than a unit—that you could decompose it into smaller behav-
ioral units (perhaps other methods or classes, which might be non-public).
Concise is great, but the code must also clearly impart all contextually perti-
nent intents. Succeeding requires that you are skilled in crafting clear, concise
code. You’ll see many examples of how to do that in this book.
You can implement any unit as a single method—a named block of code that
can return a value and/or alter the state of an object. (Let’s hope it’s only one
or the other—read about command-query separation in Command-Query
Separation, on page 180.)
You can also choose to string a series of concepts together in a larger method
rather than isolate each concept in a separate method. This is one of countless
choices you make as a system designer. Each design choice has tradeoffs and
implications, particularly when it comes to writing unit tests.
A system’s design is the complete set of choices made by its
developers.
Chapter 2. Testing the Building Blocks • 26
report erratum  •  discuss


---
**Page 27**

Let’s discuss some of those design tradeoffs, starting with the question about
representing units as a single method or not.
A Wee Bit Bigger Than a Unit?
Given the preceding definition of unit, does the following concept conform?
• Return a list of error messages for each field that fails validation checks
One practical scenario involving that concept is validating data in a (simplistic)
flight booking. Booking data includes passenger name, departure date, age,
and a list of airports representing an itinerary. The passenger name is
required, the date must be later than right now, the age must be at least 18
(the airline disallows unaccompanied minors for a single-person booking),
the itinerary must contain at least two airport codes (for example, DEN and
PRG), and each of those airport codes must be valid.
To gather errors for these five requirements, the code must process five validation
expressions. For each failing validation, the code must add a corresponding
error message to a list.
Each validation would seemingly require two atomic code concepts—an if
conditional and an addError expression—for a total of at least ten ACCs. Based
on the dubious idea of an ACC count threshold, the validation concept is
more than a unit. Here’s a possible implementation:
utj3-bookings/01/src/main/java/units/Booking.java
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;
import java.util.Set;
public record Booking(
String name,
int age,
LocalDateTime departureDate,
List<String> itinerary) {
private static final Set<String> AIRPORT_CODES = Set.of(
"COS", "DEN", "DUB", "PRG");
public List<String> validate() {
var errorMessages = new ArrayList<String>();
if (name == null || name.trim().isEmpty())
errorMessages.add("Name is empty");
if (age < 18)
errorMessages.add("Minor cannot fly unaccompanied");
if (!departureDate.isAfter(LocalDateTime.now()))
errorMessages.add("Too late!");
report erratum  •  discuss
A Wee Bit Bigger Than a Unit? • 27


---
**Page 28**

if (itinerary.size() < 2)
errorMessages.add("Itinerary needs 2+ airport codes");
if (!itinerary.stream().allMatch(
airportCode -> AIRPORT_CODES.contains(airportCode)))
errorMessages.add("Itinerary contains invalid airport code");
return errorMessages;
}
}
Simplification of the rules aside, validate looks like validation code you’d see
in many real systems. The code itself isn’t necessarily awful, but the high
number of ACCs does beg for a cleaner approach. More validations are likely
to come, and validate will only get worse.
You can write validation code in an infinite number of other ways. Some of
those ways will represent much better choices—at least for certain contexts.
If five requirements represent all the validation you’ll ever do in your project,
the code here is fine. Chances are good, though, that you have dozens more
fields that need validating and dozens of new validations forthcoming. If that’s
your context, you have many better implementations. Some of them might
involve the Javax validation framework.
An ACC limit is arbitrary but provides a good threshold that should remind
you to stop and think. With practice, you’ll quickly recognize when you can
break methods into smaller chunks (a better solution most of the time). You
can indeed write a sufficiently short unit that collects a list of error messages
for each field that fails validation:
utj3-bookings/02/src/main/java/units/Booking.java
public List<String> validate() {
return asList(
new NameRequired(),
new AgeMinimum(),
new FutureDate(),
new ItinerarySize(),
new ItineraryAirports()).stream()
.filter(Validation::isInvalid)
.map(Validation::errorMessage)
.toList();
}
The body of validate contains three smaller concepts:
• Create a stream referencing a list of validation objects
• Filter the stream down to a list of invalid validation objects
• Gather the error messages from each (invalid) validation object
Chapter 2. Testing the Building Blocks • 28
report erratum  •  discuss


---
**Page 29**

Unfortunately, it reads as about eight ACCs since its concepts aren’t cleanly
separated. Understanding it requires stepwise reading.
The validation objects are instantiated from a set of five validation classes,
each one of which isolates the conditional and error message. Here’s one:
utj3-bookings/02/src/main/java/units/Booking.java
class AgeMinimum implements Validation {
@Override
public boolean isInvalid() {
return age < 18;
}
@Override
public String errorMessage() {
return "Minor cannot fly unaccompanied";
}
}
Each of the validation classes conforms to the Validation interface.
utj3-bookings/02/src/main/java/units/Validation.java
interface Validation {
boolean isInvalid();
String errorMessage();
}
The updated validate method won’t be easier to test than it was before…yet.
But you can further decompose it into two separate concepts:
• Pass a list of validation objects off to a validator
• Validate a list of validation objects (using the filter and gather steps
described earlier)
You can move the validation concept to a new class, where it can be re-used
by other validation interests:
utj3-bookings/03/src/main/java/units/Validator.java
import java.util.List;
public class Validator {
public List<String> validate(List<Validation> validations) {
return validations.stream()
.filter(Validation::isInvalid)
.map(Validation::errorMessage)
.toList();
}
}
report erratum  •  discuss
A Wee Bit Bigger Than a Unit? • 29


---
**Page 30**

Some tests for the Validator class:
utj3-bookings/03/src/test/java/units/AValidator.java
import org.junit.jupiter.api.Test;
import java.util.Collections;
import java.util.List;
import static org.junit.jupiter.api.Assertions.assertEquals;
public class AValidator {
Validation passingValidation = new Validation() {
@Override public boolean isInvalid() { return false; }
@Override public String errorMessage() { return ""; }
};
Validation failingValidation = new Validation() {
@Override public boolean isInvalid() { return true; }
@Override public String errorMessage() { return "fail"; }
};
@Test
void returnsEmptyListWhenAllValidationsPass() {
assertEquals(Collections.emptyList(),
new Validator().validate(List.of(passingValidation)));
}
@Test
void returnsListOfFailingValidationMessages() {
assertEquals(List.of(failingValidation.errorMessage()),
new Validator().validate(List.of(
failingValidation,
passingValidation)));
}
}
The logic for the Booking class method validate simplifies greatly:
utj3-bookings/03/src/main/java/units/Booking.java
public List<String> validate(Validator validator) {
return validator.validate(validations());
}
List<Validation> validations() {
return asList(
new NameRequired(this),
new AgeMinimum(this),
new FutureDate(this),
new ItinerarySize(this),
new ItineraryAirports(this));
}
Each piece of the solution for validate now involves, at most, a handful of ACCs.
The Validator class involves filtering a list on the predicate isInvalid, mapping
each validation to an error message, then returning the result as a list. Each
Chapter 2. Testing the Building Blocks • 30
report erratum  •  discuss


---
**Page 31**

validation class contains two methods, each of which involves at most a
couple of ACCs. In Booking, validate contains a single ACC, and validations declares
a list of validator objects, which reads as a single ACC.
All of the units in the solution can now be understood at a glance. Most of
them can be tested directly, resulting in simpler tests. (There are many ways
to approach testing validate. Once you’ve worked through the first section of
this book, read my adjunct article “Unit Testing Approaches”
1 for an in-depth
discussion.)
Small, single-purpose methods are the cornerstone of good design,
which fosters easier unit testing.
Concepts as Building Blocks
One concept might be the basis for another. If you’ve provided an implemen-
tation of “capitalize a word” as a standalone method, you can incorporate it
into the slightly larger concept of capitalizing all words within a sentence:
public String capitalizeAllWords(String sentence) {
return Arrays.stream(sentence.split(" "))
.map(this::capitalize)
.collect(joining(" "));
}
Implementing smaller concepts as methods provides numerous benefits:
• It’s easy to derive a name that concisely summarizes the concept.
• You can re-use them in larger contexts without diminishing clarity.
• You can often digest their implementation at a glance.
• You can move them elsewhere more easily.
• You can write simpler, focused tests. Read on!
Testing the Simpler Things
A method that consistently returns the same value given the same arguments
and that has no side effects is a pure function. A method has side effects when
it results in any fields or arguments being changed or results in any external
effects (such as a database or API call). These characteristics make pure
functions easier to test than their opposite ilk—impure functions.
1.
https://langrsoft.com/2024/07/03/unit-testing-approaches/
report erratum  •  discuss
Concepts as Building Blocks • 31


---
**Page 32**

Code designed around (predominantly) pure functions is…wait for it…func-
tional code. You’ll look next at testing simple pure functions.
Test Pure Functions: Revisiting ZOM
In your first stab at unit testing in Chapter 1, Building Your First JUnit Test,
on page 3, you started with a Zero-based test, moved onto a One-based
test, then a Many-based test before moving on to other tests. Tim Ottinger
created the mnemonic ZOM
2 to capture this useful progression.
Following ZOM is sometimes all you need to do. It’s not a panacea, though.
Once you’ve worked through the progression, you’ll want to explore Boundary
and Exceptional behaviors. (If you add “Iterate the interface definition” and
“focus on creating Simple solutions” to the mix and move around some letters,
you have James Grenning’s spookier ZOMBIES acronym.)
3
The capitalize method should uppercase the first letter of the word passed to
it. You’ve also decided it must lowercase all other letters in the word.
utj3-units/01/src/main/java/units/StringUtils.java
public class StringUtils {
static String capitalize(String word) {
var head = word.substring(0, 1);
var tail = word.substring(1);
return head.toUpperCase() + tail.toLowerCase();
}
}
To verify capitalize, start with a zero-based test. That doesn’t mean your test
has to explicitly involve the number 0. A zero-based test can involve some
other form of nothingness: an empty array or a null value, for example. A zero-
based test for capitalize involves passing it an empty string:
utj3-units/01/src/test/java/units/SomeStringUtils.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static units.StringUtils.capitalize;
public class SomeStringUtils {
@Test
void returnsEmptyStringWhenEmpty() {
assertEquals("", capitalize(""));
}
}
2.
https://agileinaflash.blogspot.com/2012/06/simplify-design-with-zero-one-many.html
3.
http://blog.wingman-sw.com/tdd-guided-by-zombies
Chapter 2. Testing the Building Blocks • 32
report erratum  •  discuss


---
**Page 33**

Empty string in, empty string out—simple stuff. It fails due to a StringIndex-
OutOfBoundsException, a hiccup you can fix with a guard clause.
utj3-units/02/src/main/java/units/StringUtils.java
static String capitalize(String word) {
if (word.isEmpty()) return "";
➤
var head = word.substring(0, 1);
var tail = word.substring(1);
return head.toUpperCase() + tail.toLowerCase();
}
Writing a test for the null value can sometimes be thought of as a zero-based
test. Here, the code ignores null inputs completely—the assumption is that
other code or mechanisms have ensured the string argument is not null. The
behavior is undefined if capitalize gets called with null.
The choice to avoid a null check in capitalize might fly for some systems but not
others. It’s usually a valid choice for systems with good control over input.
You end up with a lot fewer paranoid checks for null.
If you instead wanted capitalize to explicitly handle null inputs, you’d write a
test for that case. And that test would document your choice.
Tests capture intent. Absence of a test implies undefined (acciden-
tal) behavior. Write tests for all intents.
Moving to a test for one—one letter, that is. When passed a lowercase letter,
capitalize should return an uppercase one:
utj3-units/02/src/test/java/units/SomeStringUtils.java
@Test
void uppercasesSingleLetter() {
assertEquals("A", capitalize("a"));
}
Then a many-based test, in which you pass a bunch of letters to capitalize:
utj3-units/02/src/test/java/units/SomeStringUtils.java
@Test
void uppercasesFirstLetterOfLowercaseWord() {
assertEquals("Alpha", capitalize("alpha"));
}
To test the last wrinkle—that the remainder of the letters are lowercased—you
write a test for that variant of the input data:
report erratum  •  discuss
Testing the Simpler Things • 33


---
**Page 34**

utj3-units/02/src/test/java/units/SomeStringUtils.java
@Test
void lowercasesRemainderOfLetters() {
assertEquals("Omega", capitalize("OMEGA"));
}
Testing pure functions is conceptually easy: call a method with
some values, then assert against the result it returns.
Verifying Side Effects
An impure function creates side effects. The prototypical side effect: you call
a void method that changes the value of one or more fields in the containing
object. The Location class does just that in its move method (highlighted):
utj3-units/02/src/main/java/units/Location.java
import java.util.Objects;
public class Location {
enum Heading {North, East, South, West}
private int x, y;
private Heading heading;
public Location(int x, int y, Heading heading) {
this.x = x;
this.y = y;
this.heading = heading;
}
public void move(int distance) {
➤
switch (heading) {
➤
case North -> y = y + distance;
➤
case East -> x = x + distance;
➤
case South -> y = y - distance;
➤
case West -> x = x - distance;
➤
}
➤
}
➤
public int getX() { return x; }
public int getY() { return y; }
public Heading getHeading() { return heading; }
@Override
public boolean equals(Object o) {
if (this == o) return true;
if (o == null || getClass() != o.getClass()) return false;
Location location = (Location) o;
return x == location.x && y == location.y && heading == location.heading;
}
Chapter 2. Testing the Building Blocks • 34
report erratum  •  discuss


---
**Page 35**

@Override
public int hashCode() { return Objects.hash(x, y, heading); }
@Override
public String toString() {
return "(" + x + ", " + y + ", => " + heading + ')';
}
}
Oh dear, that’s a pile of code. While Location appears to have a lot going on,
most of its code is boilerplate.
The Location class would be the sort of thing Java records are made for, but
for one unfortunate circumstance: it creates mutable objects. A Location object’s
x and y fields are mutated (changed) when client code executes the move
method.
Location looks like it demands a significant amount of testing. It’s a lot longer
than the CreditHistory class, for one (though probably nowhere near the size of
a typical class in so many production systems). But let’s see just what the
testing effort will involve.
Testing gives you the guts to ship. You increase this confidence by ensuring
that your code’s unit behaviors work as expected.
You gain the confidence to ship through testing.
You don’t need to test code you didn’t write as long as you think you can trust
it. The equals and hashCode methods here were generated by an IDE, which
should provide very high confidence that they work. If you later must manu-
ally change or directly invoke these methods, cover them with tests.
Developers wrote Location’s toString method to help developers decipher problems
and clarify failing tests. Don’t feel compelled to test it, either. Do test toString
if other production code depends on it, either explicitly or implicitly.
The only real behaviors in Location that remain for consideration are its ability
to capture a location and to move to another location.
A first test for Location might create a location with an (x, y) coordinate and a
heading, then ensure that it returns those initial values correctly. But that’s
terribly uninteresting and barely “behavior.” The getters will get exercised
(executed) as part of tests for other Location behavior. These tests will expose
problems with the getters, however inconceivable.
report erratum  •  discuss
Verifying Side Effects • 35


---
**Page 36**

Focus, then, on testing the one thing that could really break: move.
utj3-units/02/src/test/java/units/ALocation.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static units.Location.Heading.North;
public class ALocation {
@Test
void increasesYCoordinateWhenMovingNorth() {
var location = new Location(0, 0, North);
location.move(42);
assertEquals(0, location.getX());
assertEquals(42, location.getY());
assertEquals(North, location.getHeading());
}
}
The test first creates a location and then tells the location to move. It finally
asserts that the y coordinate has changed appropriately (since you’re moving
north), but neither x nor the heading have changed.
Earlier, you learned to verify only one behavior per test method. This test
does just that—it verifies that a move operation updates the x coordinate of
a location and nothing else.
It would be nice and concise if you could consolidate the three assertions into
a single line. You can, by comparing the altered location object to a newly-
created instance:
utj3-units/03/src/test/java/units/ALocation.java
@Test
void increasesYCoordinateWhenMovingNorth() {
var location = new Location(0, 0, North);
location.move(42);
assertEquals(new Location(0, 42, North), location);
➤
}
One fewer test statement means less extraneous cognitive load.
The move method is a void method; in other words, it returns no value. It’s also
a command (or action method)—its purpose is to allow you to tell an object to
do something.
A command method can’t return anything, so it must otherwise create some
side effect to have a raison d’etre. It can alter any objects passed to it as
Chapter 2. Testing the Building Blocks • 36
report erratum  •  discuss


---
**Page 37**

arguments, it can alter the object’s fields, or it can interact with something
external that affects behavior. Or it can interact with another method that
does one of those three things.
The code in move assigns new values to x and y depending on which case in the
switch statement gets executed. These switch cases represent the potential
side effects. It’s the job of your tests to verify each one of these possible cases
by tracking the state of both x and y.
Four cases, four tests. Here are the remaining three:
utj3-units/03/src/test/java/units/ALocation.java
@Test
void increasesXCoordinateWhenMovingEast() {
➤
var location = new Location(-2, 0, East);
location.move(5);
assertEquals(new Location(3, 0, East), location);
}
@Test
void decreasesYCoordinateWhenMovingSouth() {
➤
var location = new Location(-2, 5, South);
location.move(9);
assertEquals(new Location(-2, -4, South), location);
}
@Test
void decreasesXCoordinateWhenMovingWest() {
➤
var location = new Location(-2, 5, West);
location.move(12);
assertEquals(new Location(-14, 5, West), location);
}
You can create each test from scratch. Or you can copy a working test, paste
it, and change the test data—as long as you go back and seek to eliminate
redundancies across the tests.
All four tests contain the same three statements: create a location,
call move on it, and then compare it to a new, expected location.
When only the data varies from test to test, you can use a parame-
terized test (see Executing Multiple Data Cases with Parameterized
Tests, on page 131) to instead run one test many times, each with
a different set of inputs and expected outcomes.
report erratum  •  discuss
Verifying Side Effects • 37


---
**Page 38**

Let’s consider, then discard, a couple more possibilities for testing the Location
class:
1.
The switch statement suggests a possibility that heading contains a value
not represented in the case statements. But in this case, heading is an enum
with four values, and you already have tests for all four values. (The
compiler would also give you a warning otherwise.)
2.
The heading parameter could be null. You could write a test that shows
nothing happens if move gets called with a null heading. However, the notion
of having no heading is probably nonsensical in the bigger application.
Better solutions:
• Default the heading to, say, North.
• Throw an exception in the constructor if it’s null.
• Assume a responsible client calls move and never passes a null heading.
For now, make that last assumption, and don’t worry about a null test.
Reflecting on Design
The more side effects your code creates, the more challenging it becomes to
verify. If one method changes a field, its new value can unexpectedly break
the behavior in other methods that interact with the field. These intertwinings
of object state are one of the reasons you write tests.
How you design your code has a direct impact on how easy it is to change. A
simpler design—more direct, more concise, and less intertwined—is better
because it makes change cheaper.
A simpler design usually makes tests far easier to write, too. Fewer intertwin-
ings of object state mean fewer pathways through the code that you must
concern yourself with.
A simpler design makes for simpler testing.
The corollary to that important tip:
Tests that are hard to write usually imply less-than-ideal design.
Fix the design.
Chapter 2. Testing the Building Blocks • 38
report erratum  •  discuss


---
**Page 39**

Your tests for Location weren’t so hard to write, and that’s because there’s not
much entanglement within its code. Still, you’ll want to look at a functional
version. In Java, records provide the best place to get started—they create
immutable objects by definition—objects whose state does not change after
instantiation. It’s a lot easier to reason about, and therefore test, when you
don’t have reason about complex ways in which the state can change.
utj3-units/03/src/main/java/units/FixedLocation.java
public record FixedLocation(int x, int y, Heading heading) {
public FixedLocation move(int distance) {
return switch (heading) {
case North -> new FixedLocation(x, y + distance, heading);
case East -> new FixedLocation(x + distance, y, heading);
case South -> new FixedLocation(x, y - distance, heading);
case West -> new FixedLocation(x - distance, y, heading);
};
}
}
Holy hand grenade! Using Java records, all that other near-boilerplate gets
blown away. You automagically get equals, hashCode, a useful toString, a construc-
tor, and accessors. The code shrinks to a fraction of its stateful version. Take
a look at what comparable tests look like.
utj3-units/03/src/test/java/units/AFixedLocation.java
public class AFixedLocation {
@Test
void increasesYCoordinateWhenMovingNorth() {
var location = new FixedLocation(0, 0, North);
var newLocation = location.move(42);
assertEquals(new FixedLocation(0, 42, North), newLocation);
}
@Test
void increasesXCoordinateWhenMovingEast() {
var location = new FixedLocation(-2, 0, East);
var newLocation = location.move(5);
assertEquals(new FixedLocation(3, 0, East), newLocation);
}
@Test
void decreasesYCoordinateWhenMovingSouth() {
var location = new FixedLocation(-2, 5, South);
var newLocation = location.move(9);
assertEquals(new FixedLocation(-2, -4, South), newLocation);
}
report erratum  •  discuss
Verifying Side Effects • 39


---
**Page 40**

@Test
void decreasesXCoordinateWhenMovingWest() {
var location = new FixedLocation(-2, 5, West);
var newLocation = location.move(12);
assertEquals(new FixedLocation(-14, 5, West),newLocation);
}
}
Hmm. Not any better, really. But due to the functional nature of FixedLocation,
you can inline all local variables to create single-statement assertions:
utj3-units/04/src/test/java/units/AFixedLocation.java
public class AFixedLocation {
@Test
void increasesYCoordinateWhenMovingNorth() {
assertEquals(new FixedLocation(0, 42, North),
new FixedLocation(0, 0, North).move(42));
}
@Test
void increasesXCoordinateWhenMovingEast() {
assertEquals(new FixedLocation(3, 0, East),
new FixedLocation(-2, 0, East).move(5));
}
@Test
void decreasesYCoordinateWhenMovingSouth() {
assertEquals(new FixedLocation(-2, -4, South),
new FixedLocation(-2, 5, South).move(9));
}
@Test
void decreasesXCoordinateWhenMovingWest() {
assertEquals(new FixedLocation(-14, 5, West),
new FixedLocation(-2, 5, West).move(12));
}
}
Each assertion now contains all the information needed to understand how
the test example demonstrates what the test’s name states. The tests are
direct, and digestible almost at a glance.
You don’t want to make Java into something it’s not—a functional language.
But moving in the direction of less state makes many things easier.
While each of the four tests involves a different set of data, their code is
exactly the same. Each test creates a location, calls move, and asserts against
a new location. You can cover the four data cases with a single test method
that you inject data variants into—see Executing Multiple Data Cases with
Parameterized Tests, on page 131).
Chapter 2. Testing the Building Blocks • 40
report erratum  •  discuss


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


---
**Page 52**

• Conformance—Does the value conform to an expected format, such as
an email address or filename? What does the method do when passed an
invalid format? Does a string parameter support upper or mixed case?
• Ordering—Is the set of values ordered or unordered as appropriate? What
happens if things happen out of chronological order, such as an HTTP
server that returns an OPTIONS response after a POST instead of before?
• Range—Is the value within reasonable minimum and maximum values?
Can any computations result in numeric overflow?  range
• Reference—Does the object need to be in a certain state? What happens
if it’s in an unexpected state? What if the code references something
external that’s not under its direct control?
• Existence—Does the value exist (is it non-null, nonzero, present in a set)?
What if you pass a method empty values (0, 0.0, "", null)?
• Cardinality—Are there exactly enough values? Have you covered all your
bases with ZOM? Can it handle large volumes? Is there a notion of too
many? What if there are duplicates in a list that shouldn’t allow them (for
example, a roster of classroom students)?
• Time (absolute and relative)—Is everything happening in order? At the
right time? In time?
Many of the defects you’ll code in your career will involve similar corner cases,
so you’ll positively want to cover them with tests.
Summary
You have worked through writing tests for a number of common unit
scenarios. Your own “real” code test will, of course, be different and often
more involved. Still, how you approach writing tests for your code will be
similar to the approaches you’ve learned here.
Much of the code you try to test will be dependent on other classes that are vol-
atile, slow, or even incomplete. In the next chapter, you’ll learn how to use
test doubles (colloquially referred to as mock objects or mocks) to break those
dependencies so that you can test.
Chapter 2. Testing the Building Blocks • 52
report erratum  •  discuss


---
**Page 53**

CHAPTER 3
Using Test Doubles
You can test a lot of your system using the information you’ve learned over
the prior two chapters. But not all units are going to be similarly easy to test.
It’s a safe bet you find your own system hard to test. Perhaps you think the first
two chapters made it look too easy. “It must be nice to have a system that sup-
ports writing unit tests out of the box, but it doesn’t match my reality,” says Joe.
In this chapter, you’ll learn how to employ test doubles to break dependencies
on pain-inducing collaborators. A test double is a stand-in (think “stunt
double”) for the dependencies that make your code hard to test. You’re prob-
ably already familiar with the name of one kind of test double—a mock object.
With test doubles, you gain a tool that will help you get past the ever-present
unit testing hurdle of troublesome dependencies.
A Testing Challenge
You’re testing an AddressRetriever. Given a latitude and longitude, its retrieve
method returns an appropriately populated Address object.
utj3-mock-objects/01/src/main/java/com/langrsoft/domain/AddressRetriever.java
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.langrsoft.util.HttpImpl;
public class AddressRetriever {
private static final String SERVER =
"https://nominatim.openstreetmap.org";
public Address retrieve(double latitude, double longitude) {
var locationParams =
"lon=%.6f&lat=%.6f".formatted(latitude, longitude);
var url =
"%s/reverse?%s&format=json".formatted(SERVER, locationParams);
report erratum  •  discuss



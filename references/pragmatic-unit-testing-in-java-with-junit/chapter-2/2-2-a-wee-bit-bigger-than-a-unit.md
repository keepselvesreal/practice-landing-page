# 2.2 A Wee Bit Bigger Than a Unit? (pp.27-31)

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



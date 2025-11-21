# 2.1 Units (pp.25-27)

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



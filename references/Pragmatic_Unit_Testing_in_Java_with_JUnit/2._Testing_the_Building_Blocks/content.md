Line 1: 
Line 2: --- 페이지 46 ---
Line 3: CHAPTER 2
Line 4: Testing the Building Blocks
Line 5: In the previous chapter, you took a small piece of code and wrote a few JUnit
Line 6: tests around it. In the process, you learned how to structure your tests, exe-
Line 7: cute them, how to interpret results, and what test to write next.
Line 8: You’ve only scratched the surface of what it means to write tests for code. In
Line 9: this chapter, you’ll examine several common code constructs and learn how
Line 10: to test them. These are the topics you’ll cover:
Line 11: • Testing pure functions
Line 12: • Testing code with side effects
Line 13: • How different designs can impact unit tests
Line 14: • Writing tests for code involving lists
Line 15: • Writing tests for code that throws exceptions
Line 16: • Covering boundary conditions with tests
Line 17: First, however, let’s talk about the word unit in unit test.
Line 18: Units
Line 19: A software system is an organized collection of many units. A unit is the
Line 20: smallest piece of code that accomplishes a specific behavioral goal—a concept.
Line 21: Here are some examples of concepts:
Line 22: • Capitalize the first letter of a word
Line 23: • Move a passenger from the standby list to the boarding list
Line 24: • Mark a passenger as upgraded
Line 25: • Calculate the mean credit rating for an individual
Line 26: • Throw an exception when a user is under 18 years old
Line 27: report erratum  •  discuss
Line 28: 
Line 29: --- 페이지 47 ---
Line 30: Concepts can also represent generic or very common ideas in software:
Line 31: • Add an item to a list
Line 32: • Remove all items matching a predicate from a list
Line 33: • Throw an exception when a string is non-numeric
Line 34: Each of the above concepts requires perhaps one to three or four “atomic
Line 35: code concepts.” Think of an atomic code concept (let’s call it an ACC) as
Line 36: closer to an expression—the biggest chunk of code that you can read and
Line 37: understand at a glance. Each additional statement represents an additional
Line 38: ACC, as does each new lambda or function call in a pipeline.
Line 39: An if statement with a single-line body would count as two ACCs: the condi-
Line 40: tional plus the statement that executes if it evaluates to true. The key notion
Line 41: is that both parts of the if must be read and understood separately.
Line 42: A concise implementation of a concept uses no more ACCs than
Line 43: needed.
Line 44: Of course, you’ll inevitably need to implement concepts requiring a handful
Line 45: or more ACCs. But for now, let’s establish a fairly sensitive and arbitrary
Line 46: threshold. If your method requires five or more ACCs, consider the possibility
Line 47: that it’s larger than a unit—that you could decompose it into smaller behav-
Line 48: ioral units (perhaps other methods or classes, which might be non-public).
Line 49: Concise is great, but the code must also clearly impart all contextually perti-
Line 50: nent intents. Succeeding requires that you are skilled in crafting clear, concise
Line 51: code. You’ll see many examples of how to do that in this book.
Line 52: You can implement any unit as a single method—a named block of code that
Line 53: can return a value and/or alter the state of an object. (Let’s hope it’s only one
Line 54: or the other—read about command-query separation in Command-Query
Line 55: Separation, on page 180.)
Line 56: You can also choose to string a series of concepts together in a larger method
Line 57: rather than isolate each concept in a separate method. This is one of countless
Line 58: choices you make as a system designer. Each design choice has tradeoffs and
Line 59: implications, particularly when it comes to writing unit tests.
Line 60: A system’s design is the complete set of choices made by its
Line 61: developers.
Line 62: Chapter 2. Testing the Building Blocks • 26
Line 63: report erratum  •  discuss
Line 64: 
Line 65: --- 페이지 48 ---
Line 66: Let’s discuss some of those design tradeoffs, starting with the question about
Line 67: representing units as a single method or not.
Line 68: A Wee Bit Bigger Than a Unit?
Line 69: Given the preceding definition of unit, does the following concept conform?
Line 70: • Return a list of error messages for each field that fails validation checks
Line 71: One practical scenario involving that concept is validating data in a (simplistic)
Line 72: flight booking. Booking data includes passenger name, departure date, age,
Line 73: and a list of airports representing an itinerary. The passenger name is
Line 74: required, the date must be later than right now, the age must be at least 18
Line 75: (the airline disallows unaccompanied minors for a single-person booking),
Line 76: the itinerary must contain at least two airport codes (for example, DEN and
Line 77: PRG), and each of those airport codes must be valid.
Line 78: To gather errors for these five requirements, the code must process five validation
Line 79: expressions. For each failing validation, the code must add a corresponding
Line 80: error message to a list.
Line 81: Each validation would seemingly require two atomic code concepts—an if
Line 82: conditional and an addError expression—for a total of at least ten ACCs. Based
Line 83: on the dubious idea of an ACC count threshold, the validation concept is
Line 84: more than a unit. Here’s a possible implementation:
Line 85: utj3-bookings/01/src/main/java/units/Booking.java
Line 86: import java.time.LocalDateTime;
Line 87: import java.util.ArrayList;
Line 88: import java.util.List;
Line 89: import java.util.Set;
Line 90: public record Booking(
Line 91: String name,
Line 92: int age,
Line 93: LocalDateTime departureDate,
Line 94: List<String> itinerary) {
Line 95: private static final Set<String> AIRPORT_CODES = Set.of(
Line 96: "COS", "DEN", "DUB", "PRG");
Line 97: public List<String> validate() {
Line 98: var errorMessages = new ArrayList<String>();
Line 99: if (name == null || name.trim().isEmpty())
Line 100: errorMessages.add("Name is empty");
Line 101: if (age < 18)
Line 102: errorMessages.add("Minor cannot fly unaccompanied");
Line 103: if (!departureDate.isAfter(LocalDateTime.now()))
Line 104: errorMessages.add("Too late!");
Line 105: report erratum  •  discuss
Line 106: A Wee Bit Bigger Than a Unit? • 27
Line 107: 
Line 108: --- 페이지 49 ---
Line 109: if (itinerary.size() < 2)
Line 110: errorMessages.add("Itinerary needs 2+ airport codes");
Line 111: if (!itinerary.stream().allMatch(
Line 112: airportCode -> AIRPORT_CODES.contains(airportCode)))
Line 113: errorMessages.add("Itinerary contains invalid airport code");
Line 114: return errorMessages;
Line 115: }
Line 116: }
Line 117: Simplification of the rules aside, validate looks like validation code you’d see
Line 118: in many real systems. The code itself isn’t necessarily awful, but the high
Line 119: number of ACCs does beg for a cleaner approach. More validations are likely
Line 120: to come, and validate will only get worse.
Line 121: You can write validation code in an infinite number of other ways. Some of
Line 122: those ways will represent much better choices—at least for certain contexts.
Line 123: If five requirements represent all the validation you’ll ever do in your project,
Line 124: the code here is fine. Chances are good, though, that you have dozens more
Line 125: fields that need validating and dozens of new validations forthcoming. If that’s
Line 126: your context, you have many better implementations. Some of them might
Line 127: involve the Javax validation framework.
Line 128: An ACC limit is arbitrary but provides a good threshold that should remind
Line 129: you to stop and think. With practice, you’ll quickly recognize when you can
Line 130: break methods into smaller chunks (a better solution most of the time). You
Line 131: can indeed write a sufficiently short unit that collects a list of error messages
Line 132: for each field that fails validation:
Line 133: utj3-bookings/02/src/main/java/units/Booking.java
Line 134: public List<String> validate() {
Line 135: return asList(
Line 136: new NameRequired(),
Line 137: new AgeMinimum(),
Line 138: new FutureDate(),
Line 139: new ItinerarySize(),
Line 140: new ItineraryAirports()).stream()
Line 141: .filter(Validation::isInvalid)
Line 142: .map(Validation::errorMessage)
Line 143: .toList();
Line 144: }
Line 145: The body of validate contains three smaller concepts:
Line 146: • Create a stream referencing a list of validation objects
Line 147: • Filter the stream down to a list of invalid validation objects
Line 148: • Gather the error messages from each (invalid) validation object
Line 149: Chapter 2. Testing the Building Blocks • 28
Line 150: report erratum  •  discuss
Line 151: 
Line 152: --- 페이지 50 ---
Line 153: Unfortunately, it reads as about eight ACCs since its concepts aren’t cleanly
Line 154: separated. Understanding it requires stepwise reading.
Line 155: The validation objects are instantiated from a set of five validation classes,
Line 156: each one of which isolates the conditional and error message. Here’s one:
Line 157: utj3-bookings/02/src/main/java/units/Booking.java
Line 158: class AgeMinimum implements Validation {
Line 159: @Override
Line 160: public boolean isInvalid() {
Line 161: return age < 18;
Line 162: }
Line 163: @Override
Line 164: public String errorMessage() {
Line 165: return "Minor cannot fly unaccompanied";
Line 166: }
Line 167: }
Line 168: Each of the validation classes conforms to the Validation interface.
Line 169: utj3-bookings/02/src/main/java/units/Validation.java
Line 170: interface Validation {
Line 171: boolean isInvalid();
Line 172: String errorMessage();
Line 173: }
Line 174: The updated validate method won’t be easier to test than it was before…yet.
Line 175: But you can further decompose it into two separate concepts:
Line 176: • Pass a list of validation objects off to a validator
Line 177: • Validate a list of validation objects (using the filter and gather steps
Line 178: described earlier)
Line 179: You can move the validation concept to a new class, where it can be re-used
Line 180: by other validation interests:
Line 181: utj3-bookings/03/src/main/java/units/Validator.java
Line 182: import java.util.List;
Line 183: public class Validator {
Line 184: public List<String> validate(List<Validation> validations) {
Line 185: return validations.stream()
Line 186: .filter(Validation::isInvalid)
Line 187: .map(Validation::errorMessage)
Line 188: .toList();
Line 189: }
Line 190: }
Line 191: report erratum  •  discuss
Line 192: A Wee Bit Bigger Than a Unit? • 29
Line 193: 
Line 194: --- 페이지 51 ---
Line 195: Some tests for the Validator class:
Line 196: utj3-bookings/03/src/test/java/units/AValidator.java
Line 197: import org.junit.jupiter.api.Test;
Line 198: import java.util.Collections;
Line 199: import java.util.List;
Line 200: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 201: public class AValidator {
Line 202: Validation passingValidation = new Validation() {
Line 203: @Override public boolean isInvalid() { return false; }
Line 204: @Override public String errorMessage() { return ""; }
Line 205: };
Line 206: Validation failingValidation = new Validation() {
Line 207: @Override public boolean isInvalid() { return true; }
Line 208: @Override public String errorMessage() { return "fail"; }
Line 209: };
Line 210: @Test
Line 211: void returnsEmptyListWhenAllValidationsPass() {
Line 212: assertEquals(Collections.emptyList(),
Line 213: new Validator().validate(List.of(passingValidation)));
Line 214: }
Line 215: @Test
Line 216: void returnsListOfFailingValidationMessages() {
Line 217: assertEquals(List.of(failingValidation.errorMessage()),
Line 218: new Validator().validate(List.of(
Line 219: failingValidation,
Line 220: passingValidation)));
Line 221: }
Line 222: }
Line 223: The logic for the Booking class method validate simplifies greatly:
Line 224: utj3-bookings/03/src/main/java/units/Booking.java
Line 225: public List<String> validate(Validator validator) {
Line 226: return validator.validate(validations());
Line 227: }
Line 228: List<Validation> validations() {
Line 229: return asList(
Line 230: new NameRequired(this),
Line 231: new AgeMinimum(this),
Line 232: new FutureDate(this),
Line 233: new ItinerarySize(this),
Line 234: new ItineraryAirports(this));
Line 235: }
Line 236: Each piece of the solution for validate now involves, at most, a handful of ACCs.
Line 237: The Validator class involves filtering a list on the predicate isInvalid, mapping
Line 238: each validation to an error message, then returning the result as a list. Each
Line 239: Chapter 2. Testing the Building Blocks • 30
Line 240: report erratum  •  discuss
Line 241: 
Line 242: --- 페이지 52 ---
Line 243: validation class contains two methods, each of which involves at most a
Line 244: couple of ACCs. In Booking, validate contains a single ACC, and validations declares
Line 245: a list of validator objects, which reads as a single ACC.
Line 246: All of the units in the solution can now be understood at a glance. Most of
Line 247: them can be tested directly, resulting in simpler tests. (There are many ways
Line 248: to approach testing validate. Once you’ve worked through the first section of
Line 249: this book, read my adjunct article “Unit Testing Approaches”
Line 250: 1 for an in-depth
Line 251: discussion.)
Line 252: Small, single-purpose methods are the cornerstone of good design,
Line 253: which fosters easier unit testing.
Line 254: Concepts as Building Blocks
Line 255: One concept might be the basis for another. If you’ve provided an implemen-
Line 256: tation of “capitalize a word” as a standalone method, you can incorporate it
Line 257: into the slightly larger concept of capitalizing all words within a sentence:
Line 258: public String capitalizeAllWords(String sentence) {
Line 259: return Arrays.stream(sentence.split(" "))
Line 260: .map(this::capitalize)
Line 261: .collect(joining(" "));
Line 262: }
Line 263: Implementing smaller concepts as methods provides numerous benefits:
Line 264: • It’s easy to derive a name that concisely summarizes the concept.
Line 265: • You can re-use them in larger contexts without diminishing clarity.
Line 266: • You can often digest their implementation at a glance.
Line 267: • You can move them elsewhere more easily.
Line 268: • You can write simpler, focused tests. Read on!
Line 269: Testing the Simpler Things
Line 270: A method that consistently returns the same value given the same arguments
Line 271: and that has no side effects is a pure function. A method has side effects when
Line 272: it results in any fields or arguments being changed or results in any external
Line 273: effects (such as a database or API call). These characteristics make pure
Line 274: functions easier to test than their opposite ilk—impure functions.
Line 275: 1.
Line 276: https://langrsoft.com/2024/07/03/unit-testing-approaches/
Line 277: report erratum  •  discuss
Line 278: Concepts as Building Blocks • 31
Line 279: 
Line 280: --- 페이지 53 ---
Line 281: Code designed around (predominantly) pure functions is…wait for it…func-
Line 282: tional code. You’ll look next at testing simple pure functions.
Line 283: Test Pure Functions: Revisiting ZOM
Line 284: In your first stab at unit testing in Chapter 1, Building Your First JUnit Test,
Line 285: on page 3, you started with a Zero-based test, moved onto a One-based
Line 286: test, then a Many-based test before moving on to other tests. Tim Ottinger
Line 287: created the mnemonic ZOM
Line 288: 2 to capture this useful progression.
Line 289: Following ZOM is sometimes all you need to do. It’s not a panacea, though.
Line 290: Once you’ve worked through the progression, you’ll want to explore Boundary
Line 291: and Exceptional behaviors. (If you add “Iterate the interface definition” and
Line 292: “focus on creating Simple solutions” to the mix and move around some letters,
Line 293: you have James Grenning’s spookier ZOMBIES acronym.)
Line 294: 3
Line 295: The capitalize method should uppercase the first letter of the word passed to
Line 296: it. You’ve also decided it must lowercase all other letters in the word.
Line 297: utj3-units/01/src/main/java/units/StringUtils.java
Line 298: public class StringUtils {
Line 299: static String capitalize(String word) {
Line 300: var head = word.substring(0, 1);
Line 301: var tail = word.substring(1);
Line 302: return head.toUpperCase() + tail.toLowerCase();
Line 303: }
Line 304: }
Line 305: To verify capitalize, start with a zero-based test. That doesn’t mean your test
Line 306: has to explicitly involve the number 0. A zero-based test can involve some
Line 307: other form of nothingness: an empty array or a null value, for example. A zero-
Line 308: based test for capitalize involves passing it an empty string:
Line 309: utj3-units/01/src/test/java/units/SomeStringUtils.java
Line 310: import org.junit.jupiter.api.Test;
Line 311: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 312: import static units.StringUtils.capitalize;
Line 313: public class SomeStringUtils {
Line 314: @Test
Line 315: void returnsEmptyStringWhenEmpty() {
Line 316: assertEquals("", capitalize(""));
Line 317: }
Line 318: }
Line 319: 2.
Line 320: https://agileinaflash.blogspot.com/2012/06/simplify-design-with-zero-one-many.html
Line 321: 3.
Line 322: http://blog.wingman-sw.com/tdd-guided-by-zombies
Line 323: Chapter 2. Testing the Building Blocks • 32
Line 324: report erratum  •  discuss
Line 325: 
Line 326: --- 페이지 54 ---
Line 327: Empty string in, empty string out—simple stuff. It fails due to a StringIndex-
Line 328: OutOfBoundsException, a hiccup you can fix with a guard clause.
Line 329: utj3-units/02/src/main/java/units/StringUtils.java
Line 330: static String capitalize(String word) {
Line 331: if (word.isEmpty()) return "";
Line 332: ➤
Line 333: var head = word.substring(0, 1);
Line 334: var tail = word.substring(1);
Line 335: return head.toUpperCase() + tail.toLowerCase();
Line 336: }
Line 337: Writing a test for the null value can sometimes be thought of as a zero-based
Line 338: test. Here, the code ignores null inputs completely—the assumption is that
Line 339: other code or mechanisms have ensured the string argument is not null. The
Line 340: behavior is undefined if capitalize gets called with null.
Line 341: The choice to avoid a null check in capitalize might fly for some systems but not
Line 342: others. It’s usually a valid choice for systems with good control over input.
Line 343: You end up with a lot fewer paranoid checks for null.
Line 344: If you instead wanted capitalize to explicitly handle null inputs, you’d write a
Line 345: test for that case. And that test would document your choice.
Line 346: Tests capture intent. Absence of a test implies undefined (acciden-
Line 347: tal) behavior. Write tests for all intents.
Line 348: Moving to a test for one—one letter, that is. When passed a lowercase letter,
Line 349: capitalize should return an uppercase one:
Line 350: utj3-units/02/src/test/java/units/SomeStringUtils.java
Line 351: @Test
Line 352: void uppercasesSingleLetter() {
Line 353: assertEquals("A", capitalize("a"));
Line 354: }
Line 355: Then a many-based test, in which you pass a bunch of letters to capitalize:
Line 356: utj3-units/02/src/test/java/units/SomeStringUtils.java
Line 357: @Test
Line 358: void uppercasesFirstLetterOfLowercaseWord() {
Line 359: assertEquals("Alpha", capitalize("alpha"));
Line 360: }
Line 361: To test the last wrinkle—that the remainder of the letters are lowercased—you
Line 362: write a test for that variant of the input data:
Line 363: report erratum  •  discuss
Line 364: Testing the Simpler Things • 33
Line 365: 
Line 366: --- 페이지 55 ---
Line 367: utj3-units/02/src/test/java/units/SomeStringUtils.java
Line 368: @Test
Line 369: void lowercasesRemainderOfLetters() {
Line 370: assertEquals("Omega", capitalize("OMEGA"));
Line 371: }
Line 372: Testing pure functions is conceptually easy: call a method with
Line 373: some values, then assert against the result it returns.
Line 374: Verifying Side Effects
Line 375: An impure function creates side effects. The prototypical side effect: you call
Line 376: a void method that changes the value of one or more fields in the containing
Line 377: object. The Location class does just that in its move method (highlighted):
Line 378: utj3-units/02/src/main/java/units/Location.java
Line 379: import java.util.Objects;
Line 380: public class Location {
Line 381: enum Heading {North, East, South, West}
Line 382: private int x, y;
Line 383: private Heading heading;
Line 384: public Location(int x, int y, Heading heading) {
Line 385: this.x = x;
Line 386: this.y = y;
Line 387: this.heading = heading;
Line 388: }
Line 389: public void move(int distance) {
Line 390: ➤
Line 391: switch (heading) {
Line 392: ➤
Line 393: case North -> y = y + distance;
Line 394: ➤
Line 395: case East -> x = x + distance;
Line 396: ➤
Line 397: case South -> y = y - distance;
Line 398: ➤
Line 399: case West -> x = x - distance;
Line 400: ➤
Line 401: }
Line 402: ➤
Line 403: }
Line 404: ➤
Line 405: public int getX() { return x; }
Line 406: public int getY() { return y; }
Line 407: public Heading getHeading() { return heading; }
Line 408: @Override
Line 409: public boolean equals(Object o) {
Line 410: if (this == o) return true;
Line 411: if (o == null || getClass() != o.getClass()) return false;
Line 412: Location location = (Location) o;
Line 413: return x == location.x && y == location.y && heading == location.heading;
Line 414: }
Line 415: Chapter 2. Testing the Building Blocks • 34
Line 416: report erratum  •  discuss
Line 417: 
Line 418: --- 페이지 56 ---
Line 419: @Override
Line 420: public int hashCode() { return Objects.hash(x, y, heading); }
Line 421: @Override
Line 422: public String toString() {
Line 423: return "(" + x + ", " + y + ", => " + heading + ')';
Line 424: }
Line 425: }
Line 426: Oh dear, that’s a pile of code. While Location appears to have a lot going on,
Line 427: most of its code is boilerplate.
Line 428: The Location class would be the sort of thing Java records are made for, but
Line 429: for one unfortunate circumstance: it creates mutable objects. A Location object’s
Line 430: x and y fields are mutated (changed) when client code executes the move
Line 431: method.
Line 432: Location looks like it demands a significant amount of testing. It’s a lot longer
Line 433: than the CreditHistory class, for one (though probably nowhere near the size of
Line 434: a typical class in so many production systems). But let’s see just what the
Line 435: testing effort will involve.
Line 436: Testing gives you the guts to ship. You increase this confidence by ensuring
Line 437: that your code’s unit behaviors work as expected.
Line 438: You gain the confidence to ship through testing.
Line 439: You don’t need to test code you didn’t write as long as you think you can trust
Line 440: it. The equals and hashCode methods here were generated by an IDE, which
Line 441: should provide very high confidence that they work. If you later must manu-
Line 442: ally change or directly invoke these methods, cover them with tests.
Line 443: Developers wrote Location’s toString method to help developers decipher problems
Line 444: and clarify failing tests. Don’t feel compelled to test it, either. Do test toString
Line 445: if other production code depends on it, either explicitly or implicitly.
Line 446: The only real behaviors in Location that remain for consideration are its ability
Line 447: to capture a location and to move to another location.
Line 448: A first test for Location might create a location with an (x, y) coordinate and a
Line 449: heading, then ensure that it returns those initial values correctly. But that’s
Line 450: terribly uninteresting and barely “behavior.” The getters will get exercised
Line 451: (executed) as part of tests for other Location behavior. These tests will expose
Line 452: problems with the getters, however inconceivable.
Line 453: report erratum  •  discuss
Line 454: Verifying Side Effects • 35
Line 455: 
Line 456: --- 페이지 57 ---
Line 457: Focus, then, on testing the one thing that could really break: move.
Line 458: utj3-units/02/src/test/java/units/ALocation.java
Line 459: import org.junit.jupiter.api.Test;
Line 460: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 461: import static units.Location.Heading.North;
Line 462: public class ALocation {
Line 463: @Test
Line 464: void increasesYCoordinateWhenMovingNorth() {
Line 465: var location = new Location(0, 0, North);
Line 466: location.move(42);
Line 467: assertEquals(0, location.getX());
Line 468: assertEquals(42, location.getY());
Line 469: assertEquals(North, location.getHeading());
Line 470: }
Line 471: }
Line 472: The test first creates a location and then tells the location to move. It finally
Line 473: asserts that the y coordinate has changed appropriately (since you’re moving
Line 474: north), but neither x nor the heading have changed.
Line 475: Earlier, you learned to verify only one behavior per test method. This test
Line 476: does just that—it verifies that a move operation updates the x coordinate of
Line 477: a location and nothing else.
Line 478: It would be nice and concise if you could consolidate the three assertions into
Line 479: a single line. You can, by comparing the altered location object to a newly-
Line 480: created instance:
Line 481: utj3-units/03/src/test/java/units/ALocation.java
Line 482: @Test
Line 483: void increasesYCoordinateWhenMovingNorth() {
Line 484: var location = new Location(0, 0, North);
Line 485: location.move(42);
Line 486: assertEquals(new Location(0, 42, North), location);
Line 487: ➤
Line 488: }
Line 489: One fewer test statement means less extraneous cognitive load.
Line 490: The move method is a void method; in other words, it returns no value. It’s also
Line 491: a command (or action method)—its purpose is to allow you to tell an object to
Line 492: do something.
Line 493: A command method can’t return anything, so it must otherwise create some
Line 494: side effect to have a raison d’etre. It can alter any objects passed to it as
Line 495: Chapter 2. Testing the Building Blocks • 36
Line 496: report erratum  •  discuss
Line 497: 
Line 498: --- 페이지 58 ---
Line 499: arguments, it can alter the object’s fields, or it can interact with something
Line 500: external that affects behavior. Or it can interact with another method that
Line 501: does one of those three things.
Line 502: The code in move assigns new values to x and y depending on which case in the
Line 503: switch statement gets executed. These switch cases represent the potential
Line 504: side effects. It’s the job of your tests to verify each one of these possible cases
Line 505: by tracking the state of both x and y.
Line 506: Four cases, four tests. Here are the remaining three:
Line 507: utj3-units/03/src/test/java/units/ALocation.java
Line 508: @Test
Line 509: void increasesXCoordinateWhenMovingEast() {
Line 510: ➤
Line 511: var location = new Location(-2, 0, East);
Line 512: location.move(5);
Line 513: assertEquals(new Location(3, 0, East), location);
Line 514: }
Line 515: @Test
Line 516: void decreasesYCoordinateWhenMovingSouth() {
Line 517: ➤
Line 518: var location = new Location(-2, 5, South);
Line 519: location.move(9);
Line 520: assertEquals(new Location(-2, -4, South), location);
Line 521: }
Line 522: @Test
Line 523: void decreasesXCoordinateWhenMovingWest() {
Line 524: ➤
Line 525: var location = new Location(-2, 5, West);
Line 526: location.move(12);
Line 527: assertEquals(new Location(-14, 5, West), location);
Line 528: }
Line 529: You can create each test from scratch. Or you can copy a working test, paste
Line 530: it, and change the test data—as long as you go back and seek to eliminate
Line 531: redundancies across the tests.
Line 532: All four tests contain the same three statements: create a location,
Line 533: call move on it, and then compare it to a new, expected location.
Line 534: When only the data varies from test to test, you can use a parame-
Line 535: terized test (see Executing Multiple Data Cases with Parameterized
Line 536: Tests, on page 131) to instead run one test many times, each with
Line 537: a different set of inputs and expected outcomes.
Line 538: report erratum  •  discuss
Line 539: Verifying Side Effects • 37
Line 540: 
Line 541: --- 페이지 59 ---
Line 542: Let’s consider, then discard, a couple more possibilities for testing the Location
Line 543: class:
Line 544: 1.
Line 545: The switch statement suggests a possibility that heading contains a value
Line 546: not represented in the case statements. But in this case, heading is an enum
Line 547: with four values, and you already have tests for all four values. (The
Line 548: compiler would also give you a warning otherwise.)
Line 549: 2.
Line 550: The heading parameter could be null. You could write a test that shows
Line 551: nothing happens if move gets called with a null heading. However, the notion
Line 552: of having no heading is probably nonsensical in the bigger application.
Line 553: Better solutions:
Line 554: • Default the heading to, say, North.
Line 555: • Throw an exception in the constructor if it’s null.
Line 556: • Assume a responsible client calls move and never passes a null heading.
Line 557: For now, make that last assumption, and don’t worry about a null test.
Line 558: Reflecting on Design
Line 559: The more side effects your code creates, the more challenging it becomes to
Line 560: verify. If one method changes a field, its new value can unexpectedly break
Line 561: the behavior in other methods that interact with the field. These intertwinings
Line 562: of object state are one of the reasons you write tests.
Line 563: How you design your code has a direct impact on how easy it is to change. A
Line 564: simpler design—more direct, more concise, and less intertwined—is better
Line 565: because it makes change cheaper.
Line 566: A simpler design usually makes tests far easier to write, too. Fewer intertwin-
Line 567: ings of object state mean fewer pathways through the code that you must
Line 568: concern yourself with.
Line 569: A simpler design makes for simpler testing.
Line 570: The corollary to that important tip:
Line 571: Tests that are hard to write usually imply less-than-ideal design.
Line 572: Fix the design.
Line 573: Chapter 2. Testing the Building Blocks • 38
Line 574: report erratum  •  discuss
Line 575: 
Line 576: --- 페이지 60 ---
Line 577: Your tests for Location weren’t so hard to write, and that’s because there’s not
Line 578: much entanglement within its code. Still, you’ll want to look at a functional
Line 579: version. In Java, records provide the best place to get started—they create
Line 580: immutable objects by definition—objects whose state does not change after
Line 581: instantiation. It’s a lot easier to reason about, and therefore test, when you
Line 582: don’t have reason about complex ways in which the state can change.
Line 583: utj3-units/03/src/main/java/units/FixedLocation.java
Line 584: public record FixedLocation(int x, int y, Heading heading) {
Line 585: public FixedLocation move(int distance) {
Line 586: return switch (heading) {
Line 587: case North -> new FixedLocation(x, y + distance, heading);
Line 588: case East -> new FixedLocation(x + distance, y, heading);
Line 589: case South -> new FixedLocation(x, y - distance, heading);
Line 590: case West -> new FixedLocation(x - distance, y, heading);
Line 591: };
Line 592: }
Line 593: }
Line 594: Holy hand grenade! Using Java records, all that other near-boilerplate gets
Line 595: blown away. You automagically get equals, hashCode, a useful toString, a construc-
Line 596: tor, and accessors. The code shrinks to a fraction of its stateful version. Take
Line 597: a look at what comparable tests look like.
Line 598: utj3-units/03/src/test/java/units/AFixedLocation.java
Line 599: public class AFixedLocation {
Line 600: @Test
Line 601: void increasesYCoordinateWhenMovingNorth() {
Line 602: var location = new FixedLocation(0, 0, North);
Line 603: var newLocation = location.move(42);
Line 604: assertEquals(new FixedLocation(0, 42, North), newLocation);
Line 605: }
Line 606: @Test
Line 607: void increasesXCoordinateWhenMovingEast() {
Line 608: var location = new FixedLocation(-2, 0, East);
Line 609: var newLocation = location.move(5);
Line 610: assertEquals(new FixedLocation(3, 0, East), newLocation);
Line 611: }
Line 612: @Test
Line 613: void decreasesYCoordinateWhenMovingSouth() {
Line 614: var location = new FixedLocation(-2, 5, South);
Line 615: var newLocation = location.move(9);
Line 616: assertEquals(new FixedLocation(-2, -4, South), newLocation);
Line 617: }
Line 618: report erratum  •  discuss
Line 619: Verifying Side Effects • 39
Line 620: 
Line 621: --- 페이지 61 ---
Line 622: @Test
Line 623: void decreasesXCoordinateWhenMovingWest() {
Line 624: var location = new FixedLocation(-2, 5, West);
Line 625: var newLocation = location.move(12);
Line 626: assertEquals(new FixedLocation(-14, 5, West),newLocation);
Line 627: }
Line 628: }
Line 629: Hmm. Not any better, really. But due to the functional nature of FixedLocation,
Line 630: you can inline all local variables to create single-statement assertions:
Line 631: utj3-units/04/src/test/java/units/AFixedLocation.java
Line 632: public class AFixedLocation {
Line 633: @Test
Line 634: void increasesYCoordinateWhenMovingNorth() {
Line 635: assertEquals(new FixedLocation(0, 42, North),
Line 636: new FixedLocation(0, 0, North).move(42));
Line 637: }
Line 638: @Test
Line 639: void increasesXCoordinateWhenMovingEast() {
Line 640: assertEquals(new FixedLocation(3, 0, East),
Line 641: new FixedLocation(-2, 0, East).move(5));
Line 642: }
Line 643: @Test
Line 644: void decreasesYCoordinateWhenMovingSouth() {
Line 645: assertEquals(new FixedLocation(-2, -4, South),
Line 646: new FixedLocation(-2, 5, South).move(9));
Line 647: }
Line 648: @Test
Line 649: void decreasesXCoordinateWhenMovingWest() {
Line 650: assertEquals(new FixedLocation(-14, 5, West),
Line 651: new FixedLocation(-2, 5, West).move(12));
Line 652: }
Line 653: }
Line 654: Each assertion now contains all the information needed to understand how
Line 655: the test example demonstrates what the test’s name states. The tests are
Line 656: direct, and digestible almost at a glance.
Line 657: You don’t want to make Java into something it’s not—a functional language.
Line 658: But moving in the direction of less state makes many things easier.
Line 659: While each of the four tests involves a different set of data, their code is
Line 660: exactly the same. Each test creates a location, calls move, and asserts against
Line 661: a new location. You can cover the four data cases with a single test method
Line 662: that you inject data variants into—see Executing Multiple Data Cases with
Line 663: Parameterized Tests, on page 131).
Line 664: Chapter 2. Testing the Building Blocks • 40
Line 665: report erratum  •  discuss
Line 666: 
Line 667: --- 페이지 62 ---
Line 668: Testing Common Code Circumstances
Line 669: As you write more tests, you’ll realize that you’re often facing a number of
Line 670: common circumstances. Here’s a handful of them:
Line 671: • Add an item to a list
Line 672: • Do something if a conditional is met
Line 673: • Update all items in a list that match a predicate
Line 674: • Remove all items matching a predicate from a list
Line 675: • Throw an exception when a conditional is met
Line 676: Lists and other collection types are a heavy part of most software development.
Line 677: You should be able to bang out tests involving lists without much thought.
Line 678: In this section, you’ll work through how you might write tests for each of
Line 679: those common needs. Hopefully, these examples will help you extrapolate
Line 680: and learn to write tests for other data structures (Maps, Sets, arrays, etc.) and
Line 681: operations (loops, streams, math, etc.).
Line 682: Add an Item to a List
Line 683: Here’s some trivial code for a container class—DestinationList—that allows clients
Line 684: to add FixedLocation objects to it, one by one.
Line 685: utj3-units/06/src/main/java/units/DestinationList.java
Line 686: import java.util.ArrayList;
Line 687: import java.util.List;
Line 688: public class DestinationList {
Line 689: private List<FixedLocation> locations = new ArrayList<>();
Line 690: public void add(FixedLocation location) {
Line 691: locations.add(location);
Line 692: }
Line 693: public List<FixedLocation> getLocations() {
Line 694: return locations;
Line 695: }
Line 696: }
Line 697: At a glance, you pretty much know the code in DestinationList works. Doesn’t matter,
Line 698: though—it’s always possible for such a small amount of code to hide a mistake.
Line 699: The singular concept implemented in DestinationList—adding a location—involves
Line 700: three separate code points: a method to add the location to a list, a field that
Line 701: creates and initializes the list, and a method that returns the list. That lack
Line 702: of concision only increases the possibility of a defect.
Line 703: DestinationList will change and grow as requirements for “add location” change
Line 704: or as other behaviors are added. Defects will be increasingly harder to spot.
Line 705: report erratum  •  discuss
Line 706: Testing Common Code Circumstances • 41
Line 707: 
Line 708: --- 페이지 63 ---
Line 709: Start testing now, before that “obvious” code sinks into a sea of “I’m not sure
Line 710: exactly what’s going on!”
Line 711: The Z in ZOM provides a good starting point and results in a guardrail test
Line 712: that will forever protect you:
Line 713: utj3-units/06/src/test/java/units/ADestinationList.java
Line 714: import org.junit.jupiter.api.BeforeEach;
Line 715: import org.junit.jupiter.api.Test;
Line 716: import java.util.List;
Line 717: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 718: import static org.junit.jupiter.api.Assertions.assertTrue;
Line 719: import static units.FixedLocation.Heading.East;
Line 720: import static units.FixedLocation.Heading.North;
Line 721: class ADestinationList {
Line 722: private DestinationList list;
Line 723: @BeforeEach
Line 724: void create() {
Line 725: list = new DestinationList();
Line 726: }
Line 727: @Test
Line 728: void isEmptyWhenCreated() {
Line 729: assertTrue(list.getLocations().isEmpty());
Line 730: }
Line 731: }
Line 732: Do you really need both one and many tests? The only interesting behavior
Line 733: you’ve coded is your call to the add method defined on ArrayList:
Line 734: utj3-units/06/src/main/java/units/DestinationList.java
Line 735: locations.add(location);
Line 736: You trust ArrayList and its ability to support one location or scads of them.
Line 737: None of your code (for now) does anything differently when only one location
Line 738: is involved. Move directly to adding a many test:
Line 739: utj3-units/06/src/test/java/units/ADestinationList.java
Line 740: @Test
Line 741: void allowsAddingLocations() {
Line 742: list.add(new FixedLocation(1, 2, North));
Line 743: list.add(new FixedLocation(1, 3, East));
Line 744: assertEquals(
Line 745: List.of(
Line 746: new FixedLocation(1, 2, North),
Line 747: new FixedLocation(1, 3, East)),
Line 748: list.getLocations());
Line 749: }
Line 750: Chapter 2. Testing the Building Blocks • 42
Line 751: report erratum  •  discuss
Line 752: 
Line 753: --- 페이지 64 ---
Line 754: While it looks cut-and-dry, allowsAddingLocations involves some choices worth
Line 755: discussing. The test contains only two visual chunks. The second chunk
Line 756: represents the assert step, of course. Its assertion compares the result of
Line 757: calling getLocations to a List of two FixedLocation objects. The two objects in this
Line 758: comparison list are instantiated inline with the exact same values as when
Line 759: you constructed them in the arrange step.
Line 760: In the assert, you are calling getLocations. By doing so, you are implying that
Line 761: getLocations isn’t really what you’re trying to verify (it’s just an accessor), but
Line 762: you’re instead using it to support your need to inspect the locations list.
Line 763: Is the first chunk the arrange step or the act step? The test name says what
Line 764: behavior your test is trying to verify—the act of adding locations. That the
Line 765: two statements in the first chunk trigger the add behavior on the list means
Line 766: that they represent your act step. It’s a subtle distinction. Some developers
Line 767: might consider the first chunk to be the test’s arrange step, and maybe that’s
Line 768: okay, but then there’s no act step. It ain’t much of a test without an act step.
Line 769: The redundant FixedLocation instantiations may compel you to introduce a
Line 770: couple of local variables to help clarify the test. Creating such test objects can
Line 771: make it easier to correlate your test’s inputs to the expected outcomes:
Line 772: utj3-units/07/src/test/java/units/ADestinationList.java
Line 773: @Test
Line 774: void allowsAddingLocations() {
Line 775: var locationOne = new FixedLocation(1, 2, North);
Line 776: var locationTwo = new FixedLocation(1, 3, East);
Line 777: list.add(locationOne);
Line 778: list.add(locationTwo);
Line 779: assertEquals(List.of(locationOne, locationTwo), list.getLocations());
Line 780: }
Line 781: Test objects are particularly useful when most, if not all, tests involve them.
Line 782: You can declare them as test-class-level constants with more memorable,
Line 783: domain-appropriate names:
Line 784: utj3-units/08/src/test/java/units/ADestinationList.java
Line 785: static final FixedLocation ORIGIN = new FixedLocation(0, 0, East);
Line 786: static final FixedLocation NORTHEAST = new FixedLocation(3, 3, North);
Line 787: @Test
Line 788: void allowsAddingLocations() {
Line 789: list.add(ORIGIN);
Line 790: list.add(NORTHEAST);
Line 791: assertEquals(List.of(ORIGIN, NORTHEAST), list.getLocations());
Line 792: }
Line 793: report erratum  •  discuss
Line 794: Testing Common Code Circumstances • 43
Line 795: 
Line 796: --- 페이지 65 ---
Line 797: Such test objects also help de-emphasize details where they don’t matter.
Line 798: That the northeast location is at (3, 3) and facing north is irrelevant in your
Line 799: allowsAddingLocations test. It only matters that NORTHEAST references an object
Line 800: distinct from ORIGIN.
Line 801: Useful here, yet creating sample objects can be overkill. It’s often easier to
Line 802: eyeball-compare the data by looking back and forth between the arrange and
Line 803: assert statements. As long as test intent remains clear, such trimmer tests
Line 804: can speed up efforts in both writing and understanding.
Line 805: utj3-units/09/src/test/java/units/ADestinationList.java
Line 806: @Test
Line 807: void doesNotAddLocationAlreadyContained() {
Line 808: list.add(new FixedLocation(0, 0, East));
Line 809: list.add(new FixedLocation(3, 3, North));
Line 810: list.add(new FixedLocation(0, 0, East));
Line 811: assertEquals(
Line 812: List.of(new FixedLocation(0, 0, East),
Line 813: new FixedLocation(3, 3, North)),
Line 814: list.getLocations());
Line 815: }
Line 816: Any of the three forms (raw inline declarations, locally declared test objects,
Line 817: and globally accessible test objects) is acceptable. Here, the inline declarations
Line 818: clutter the tests a little too much. For now, use the constants.
Line 819: Do Something if a Conditional Is Met
Line 820: If the code you’re testing involves a conditional (an if statement), you need at
Line 821: least two sets of tests: one set involving all the ways that the conditional can
Line 822: pass (in other words, return true), and one set involving all the ways that it
Line 823: can fail (return false). That way, your tests will cover both what happens if the
Line 824: if block executes and what happens if it does not.
Line 825: A common behavioral need is to ensure that a collection doesn’t take on
Line 826: duplicate elements. Here’s a change to DestinationList that introduces such a
Line 827: conditional to the add method:
Line 828: utj3-units/09/src/main/java/units/DestinationList.java
Line 829: public void add(FixedLocation location) {
Line 830: if (locations.contains(location)) return;
Line 831: locations.add(location);
Line 832: }
Line 833: You already have one test that allows adding objects. Here it is again:
Line 834: Chapter 2. Testing the Building Blocks • 44
Line 835: report erratum  •  discuss
Line 836: 
Line 837: --- 페이지 66 ---
Line 838: utj3-units/09/src/test/java/units/ADestinationList.java
Line 839: @Test
Line 840: void allowsAddingLocations() {
Line 841: list.add(ORIGIN);
Line 842: list.add(NORTHEAST);
Line 843: assertEquals(List.of(ORIGIN, NORTHEAST), list.getLocations());
Line 844: }
Line 845: The distinct names ORIGIN and DESTINATION imply that the two sample objects
Line 846: are distinct from each other. Write an additional test that involves attempting
Line 847: to add one of them, ORIGIN, a second time:
Line 848: utj3-units/09/src/test/java/units/ADestinationList.java
Line 849: @Test
Line 850: void doesNotAddLocationWhenAlreadyContained() {
Line 851: list.add(ORIGIN);
Line 852: list.add(NORTHEAST);
Line 853: list.add(ORIGIN);
Line 854: assertEquals(List.of(ORIGIN, NORTHEAST), list.getLocations());
Line 855: }
Line 856: A final note on the Arrange—Act—Assert (AAA) organization here: you are
Line 857: still trying to verify the behavior of adding (or not adding) locations. The first
Line 858: two lines in the test arrange things by adding a couple of locations. You then
Line 859: see the act step that isolates the addition of a duplicate location. This breakout
Line 860: helps readers focus on how to trigger the happy path of the if statement—you
Line 861: attempt to add an object whose details match those of one already added.
Line 862: Update All Items in a List That Match a Predicate
Line 863: The job of the method moveLocationsWithHeading is to iterate all locations and
Line 864: update those whose heading matches a target (passed-in) heading. The update
Line 865: involves changing to new x and y coordinates.
Line 866: A map operation suits your needs. Each location is mapped either to the same
Line 867: location, if its heading does not match, or to a new FixedLocation with updated
Line 868: coordinates (since FixedLocations are immutable). The collected stream is then
Line 869: assigned back to the DestinationList’s locations field.
Line 870: utj3-units/09/src/main/java/units/DestinationList.java
Line 871: public void moveLocationsWithHeading(Heading heading, int x, int y) {
Line 872: this.locations = locations.stream()
Line 873: .map(location -> location.heading().equals(heading)
Line 874: ? new FixedLocation(x, y, heading)
Line 875: : location)
Line 876: .toList();
Line 877: }
Line 878: report erratum  •  discuss
Line 879: Testing Common Code Circumstances • 45
Line 880: 
Line 881: --- 페이지 67 ---
Line 882: Here’s an approach for testing the moveLocationsWithHeading:
Line 883: • Create a list with two FixedLocation objects, one with the heading you want
Line 884: to target (for example, East). The other object should have a different
Line 885: heading.
Line 886: • Call the method moveLocationsWithHeading and pass it the targeted heading
Line 887: (East); also pass new values for x and y.
Line 888: • Ensure that the updated list in DestinationList contains a list of two elements.
Line 889: The location with the targeted location should reflect the new x and y
Line 890: values; the other location should remain unchanged.
Line 891: Here’s what the new test looks like:
Line 892: utj3-units/09/src/test/java/units/ADestinationList.java
Line 893: @Test
Line 894: void updatesMatchingLocationsWithNewCoordinates() {
Line 895: list.add(new FixedLocation(0, 0, East));
Line 896: list.add(new FixedLocation(1, 1, North));
Line 897: list.moveLocationsWithHeading(East, 2, 3);
Line 898: assertEquals(List.of(
Line 899: new FixedLocation(2, 3, East),
Line 900: new FixedLocation(1, 1, North)),
Line 901: list.getLocations());
Line 902: }
Line 903: You’ll note you’re not using test objects here. Test objects de-emphasize most
Line 904: details, but for this test, you need to show whether specific values (x and y)
Line 905: change, or don’t, based on another value (the heading). By directly instantiat-
Line 906: ing FixedLocation objects, you can visually correlate the details between arrange
Line 907: inputs and assert expected outputs.
Line 908: Remove All Items Matching a Predicate from a List
Line 909: Another method on DestinationList allows clients to remove all locations that
Line 910: exceed a specified distance from a point:
Line 911: utj3-units/09/src/main/java/units/DestinationList.java
Line 912: public void removeLocationsFurtherThan(int x, int y, int distance) {
Line 913: this.locations = locations.stream()
Line 914: .filter(location -> distanceBetween(location, x, y) < distance)
Line 915: .toList();
Line 916: }
Line 917: private double distanceBetween(FixedLocation point, int x, int y) {
Line 918: return Math.sqrt(
Line 919: Math.pow(x - point.x(), 2) + Math.pow(y - point.y(), 2));
Line 920: }
Line 921: Chapter 2. Testing the Building Blocks • 46
Line 922: report erratum  •  discuss
Line 923: 
Line 924: --- 페이지 68 ---
Line 925: Your test looks similar to the test for moveLocationsWithHeading. It creates three
Line 926: locations, two of which have a distance from (0, 0) that is greater than the
Line 927: value of 9 passed in the act step. The assertion verifies that only the location
Line 928: with a shorter distance remains.
Line 929: utj3-units/09/src/test/java/units/ADestinationList.java
Line 930: @Test
Line 931: void retainsLocationsLessThanDistance() {
Line 932: list.add(new FixedLocation(0, 5, North));
Line 933: ➤
Line 934: list.add(new FixedLocation(0, 10, North));
Line 935: ➤
Line 936: list.add(new FixedLocation(0, 15, North));
Line 937: ➤
Line 938: list.removeLocationsFurtherThan(0, 0, 9);
Line 939: assertEquals(List.of(
Line 940: new FixedLocation(0, 5, North)),
Line 941: list.getLocations());
Line 942: }
Line 943: This test purposefully uses simplistic test data. Each of the three highlighted
Line 944: locations added as part of arranging the test is on the vertical (y) axis. As a
Line 945: result, the distance between each location and (0, 0) (the passed-in point) is
Line 946: the same as its y coordinate.
Line 947: The simple-data approach to removeLocationsFurtherThan keeps the test easy to
Line 948: understand, but it means you’re ignoring the complexity in distanceBetween.
Line 949: That means you’ll need to demonstrate that the logic in distanceBetween is correct
Line 950: for non-zero values of x.
Line 951: You have a few options for verifying the distance calculations:
Line 952: • You can write more tests that interact with removeLocationsFurtherThan. These
Line 953: tests represent a slightly indirect way to verify the distance calculation
Line 954: and demand a few more lines of code.
Line 955: • You can expose distanceBetween as a package-level method, which would
Line 956: allow ADestinationList to directly test it. But distanceBetween as a concept is out
Line 957: of place in DestinationList. The job of DestinationList is to manage a list of desti-
Line 958: nations, not to calculate distances between a FixedLocation and a point.
Line 959: • You can make distanceBetween a concept better associated with FixedLocation,
Line 960: and move the method to that class. After moving the method, you can
Line 961: test it directly in FixedLocation.
Line 962: report erratum  •  discuss
Line 963: Testing Common Code Circumstances • 47
Line 964: 
Line 965: --- 페이지 69 ---
Line 966: Here’s the relevant code after the move:
Line 967: utj3-units/10/src/main/java/units/DestinationList.java
Line 968: public void removeLocationsFurtherThan(int x, int y, int distance) {
Line 969: this.locations = locations.stream()
Line 970: .filter(location -> location.distanceFrom(x, y) < distance)
Line 971: ➤
Line 972: .toList();
Line 973: }
Line 974: utj3-units/10/src/main/java/units/FixedLocation.java
Line 975: double distanceFrom(int x, int y) {
Line 976: return Math.sqrt(Math.pow(x - x(), 2) + Math.pow(y - y(), 2));
Line 977: }
Line 978: In the context of FixedLocation, the method name distanceBetween could use a little
Line 979: improvement. It’s been renamed to distanceFrom here. (A trick for deriving names:
Line 980: utter the phrase that describes how the method is used in context, for
Line 981: example, “we ask for the distance from a fixed location for a point.”)
Line 982: Now, you can quickly write a number of very focused tests that exhaust your
Line 983: ideas about how to test the distance calculation:
Line 984: utj3-units/10/src/test/java/units/AFixedLocation.java
Line 985: import org.junit.jupiter.api.Test;
Line 986: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 987: import static units.FixedLocation.Heading.*;
Line 988: public class AFixedLocation {
Line 989: final static FixedLocation.Heading h = North;
Line 990: @Test
Line 991: void is0WhenCoordinatesAreTheSame() {
Line 992: assertEquals(0, new FixedLocation(1, 2, h).distanceFrom(1, 2));
Line 993: }
Line 994: @Test
Line 995: void is5InClassicHypotenuseCase() {
Line 996: assertEquals(5.0, new FixedLocation(0, 0, h).distanceFrom(3, 4));
Line 997: }
Line 998: @Test
Line 999: void isNearSomeDoubleValue() {
Line 1000: assertEquals(5.6568, new FixedLocation(10, 13, h).distanceFrom(14, 9),
Line 1001: 0.0001);
Line 1002: }
Line 1003: @Test
Line 1004: void worksWithNegativeNumbers() {
Line 1005: assertEquals(23.7697,
Line 1006: new FixedLocation(-7, 13, h).distanceFrom(2, -9),
Line 1007: 0.0001);
Line 1008: }
Line 1009: }
Line 1010: Chapter 2. Testing the Building Blocks • 48
Line 1011: report erratum  •  discuss
Line 1012: 
Line 1013: --- 페이지 70 ---
Line 1014: The first two tests verify the zero case and a simple example. The last two
Line 1015: involve distance calculations that return interesting floating point quantities.
Line 1016: (Stylistic note: since the heading is irrelevant to these tests, naming it h helps
Line 1017: de-emphasize it.)
Line 1018: Assertions against code involving complex calculations too often provide
Line 1019: insufficient insight into what the code is doing. The expected value is mathe-
Line 1020: matically correct, but there’s no easy way to correlate it to the input values
Line 1021: from just reading the act and assert.
Line 1022: To derive the expected value for such a calculation, you can hand-calculate
Line 1023: it. You can also cross-check by using an independent source for verification,
Line 1024: such as an online app.
Line 1025: Due to limitations on how floating point values are captured, comparing two
Line 1026: floating point values can result in unexpected discrepancies. For this reason,
Line 1027: JUnit provides a form of assertEquals that takes a delta value as the third
Line 1028: argument. This delta represents a tolerance. How much can the two numbers
Line 1029: be off before JUnit fails the assertion?
Line 1030: In the test, define a heading constant arbitrarily set to North. While the heading
Line 1031: is required each time you construct a FixedLocation, it’s completely irrelevant
Line 1032: to the tests. Name this constant h, to de-emphasize the constructor argument
Line 1033: and thus minimize the clutter it otherwise adds to the tests.
Line 1034: Throw an Exception When a Conditional Is Met
Line 1035: In Chapter 1, Building Your First JUnit Test, on page 3, you wrote tests for
Line 1036: arithmeticMean in CreditHistory. The first test you wrote was a zero case:
Line 1037: utj3-credit-history/10/src/test/java/credit/ACreditHistory.java
Line 1038: @Test
Line 1039: void withNoCreditRatingsHas0Mean() {
Line 1040: var result = creditHistory.arithmeticMean();
Line 1041: assertEquals(0, result);
Line 1042: }
Line 1043: That test described and verified the highlighted behavior in arithmeticMean:
Line 1044: utj3-credit-history/10/src/main/java/credit/CreditHistory.java
Line 1045: public int arithmeticMean() {
Line 1046: if (ratings.isEmpty()) return 0;
Line 1047: ➤
Line 1048: var total = ratings.stream().mapToInt(CreditRating::rating).sum();
Line 1049: return total / ratings.size();
Line 1050: }
Line 1051: report erratum  •  discuss
Line 1052: Testing Common Code Circumstances • 49
Line 1053: 
Line 1054: --- 페이지 71 ---
Line 1055: You’ve been asked to change the code—oh no! The product owner has been
Line 1056: schooled by a mathematician and wants arithmeticMean to throw an exception
Line 1057: when there are no credit ratings.
Line 1058: Pretend to panic for a moment (“But I’ll have to retest everything!”), then make
Line 1059: the trivial change:
Line 1060: utj3-credit-history/11/src/main/java/credit/CreditHistory.java
Line 1061: public int arithmeticMean() {
Line 1062: if (ratings.isEmpty()) throw new IllegalStateException();
Line 1063: ➤
Line 1064: var total = ratings.stream().mapToInt(CreditRating::rating).sum();
Line 1065: return total / ratings.size();
Line 1066: }
Line 1067: Because you changed your code, run your tests. Hope at least one test will
Line 1068: fail due to your change of the behavior that the tests cover. Dream that only
Line 1069: the test ACreditHistory::withNoCreditRatingsHas0Mean fails since it’s the only test
Line 1070: directly related to the changed behavior. Rejoice when your hopes and dreams
Line 1071: (paltry as they are) come true: withNoCreditRatingsHas0Mean fails and for the right
Line 1072: reason—an IllegalStateException was thrown. Hooray!
Line 1073: The desired behavior is in place. A test is failing. Time to fix the incorrect test.
Line 1074: JUnit 5 gives you a way to verify that a piece of test code throws an exception:
Line 1075: utj3-credit-history/12/src/test/java/credit/ACreditHistory.java
Line 1076: @Test
Line 1077: void withNoCreditRatingsThrows() {
Line 1078: assertThrows(IllegalStateException.class,
Line 1079: () -> creditHistory.arithmeticMean());
Line 1080: }
Line 1081: In its simplest form, JUnit’s assertThrows method takes on two arguments. The
Line 1082: first represents the type of exception you expect to be thrown (IllegalStateExcep-
Line 1083: tion.class in this case). The second argument is a lambda whose body contains
Line 1084: the code that you expect will throw the appropriate exception. In your case,
Line 1085: you’re expecting the call to arithmeticMean to throw the exception.
Line 1086: When handling an assertThrows statement within a test, JUnit executes the
Line 1087: lambda in the context of a try/catch block. If the lambda barfs an exception,
Line 1088: the catch block catches the barfage and JUnit marks the test as passing as
Line 1089: long as the exception type matches. Otherwise, JUnit marks the test as a
Line 1090: failure since no exception was thrown.
Line 1091: Because your requirements changed, you updated the code and then verified
Line 1092: that your change broke a specific test. That seems so…reactionary. Maybe
Line 1093: you should take control of things.
Line 1094: Chapter 2. Testing the Building Blocks • 50
Line 1095: report erratum  •  discuss
Line 1096: 
Line 1097: --- 페이지 72 ---
Line 1098: If you view the unit tests as a way of characterizing all your code units, collec-
Line 1099: tively they become the requirements in an odd but useful little “requirements
Line 1100: by example” manner. Your test names describe the behavioral needs. Each
Line 1101: test provides an example of one of those behaviors.
Line 1102: Such well-named requirements-by-example (tests) can quickly answer ques-
Line 1103: tions others (or even you) might ask: “hey, what does the system do when we
Line 1104: try to calculate the arithmetic mean and there are no credit ratings?” Everyone
Line 1105: is happy, you have an immediate answer, and you’re highly confident it’s
Line 1106: correct because all of your tests are passing.
Line 1107: One way to take control: invert your approach to unit testing—drive a
Line 1108: requirements change by first updating the tests that relate to the change.
Line 1109: After observing that the updated tests fail (because you’ve not yet updated
Line 1110: the system with the new requirement), you can make the necessary changes
Line 1111: and then run all tests to ensure you’re still happy.
Line 1112: Once you feel increased control by test-driving changes, your next thought
Line 1113: might be, “what if I drove in all new functionality this way?” You can, and
Line 1114: doing so is known as Test-Driven Development (TDD). See Chapter 11,
Line 1115: Advancing with Test-Driven Development (TDD), on page 211 for a rundown
Line 1116: of what TDD looks like and why it might help even more. Get a little excited
Line 1117: about it—because TDD is also a lot of fun—but for now, you should continue
Line 1118: your unit testing journey.
Line 1119: Testing that an exception is thrown when expected is as important as testing
Line 1120: any other code. You’ll also want to verify that other code responds properly
Line 1121: to the situation when an exception is thrown. Doing so is a slightly trickier
Line 1122: technique; visit Testing Exception Handling, on page 65 for details.
Line 1123: Exploring Boundaries with CORRECT
Line 1124: The zero, one, many, and exception-based tests will cover most of your typical
Line 1125: needs when testing code. But you’ll also want to consider adding tests for
Line 1126: cases that a happy path through the code might not hit. These boundary
Line 1127: conditions represent scenarios that involve the edges of the input domain.
Line 1128: You can employ the CORRECT acronym, devised by Andy Hunt and Dave
Line 1129: Thomas for the first edition of this book [HT03], to help you think about
Line 1130: potential boundary conditions. For each of these items, consider whether or
Line 1131: not similar conditions can exist in the method that you want to test and what
Line 1132: might happen if these conditions are violated:
Line 1133: report erratum  •  discuss
Line 1134: Exploring Boundaries with CORRECT • 51
Line 1135: 
Line 1136: --- 페이지 73 ---
Line 1137: • Conformance—Does the value conform to an expected format, such as
Line 1138: an email address or filename? What does the method do when passed an
Line 1139: invalid format? Does a string parameter support upper or mixed case?
Line 1140: • Ordering—Is the set of values ordered or unordered as appropriate? What
Line 1141: happens if things happen out of chronological order, such as an HTTP
Line 1142: server that returns an OPTIONS response after a POST instead of before?
Line 1143: • Range—Is the value within reasonable minimum and maximum values?
Line 1144: Can any computations result in numeric overflow?  range
Line 1145: • Reference—Does the object need to be in a certain state? What happens
Line 1146: if it’s in an unexpected state? What if the code references something
Line 1147: external that’s not under its direct control?
Line 1148: • Existence—Does the value exist (is it non-null, nonzero, present in a set)?
Line 1149: What if you pass a method empty values (0, 0.0, "", null)?
Line 1150: • Cardinality—Are there exactly enough values? Have you covered all your
Line 1151: bases with ZOM? Can it handle large volumes? Is there a notion of too
Line 1152: many? What if there are duplicates in a list that shouldn’t allow them (for
Line 1153: example, a roster of classroom students)?
Line 1154: • Time (absolute and relative)—Is everything happening in order? At the
Line 1155: right time? In time?
Line 1156: Many of the defects you’ll code in your career will involve similar corner cases,
Line 1157: so you’ll positively want to cover them with tests.
Line 1158: Summary
Line 1159: You have worked through writing tests for a number of common unit
Line 1160: scenarios. Your own “real” code test will, of course, be different and often
Line 1161: more involved. Still, how you approach writing tests for your code will be
Line 1162: similar to the approaches you’ve learned here.
Line 1163: Much of the code you try to test will be dependent on other classes that are vol-
Line 1164: atile, slow, or even incomplete. In the next chapter, you’ll learn how to use
Line 1165: test doubles (colloquially referred to as mock objects or mocks) to break those
Line 1166: dependencies so that you can test.
Line 1167: Chapter 2. Testing the Building Blocks • 52
Line 1168: report erratum  •  discuss
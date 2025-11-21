# 2.4 Testing the Simpler Things (pp.31-34)

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



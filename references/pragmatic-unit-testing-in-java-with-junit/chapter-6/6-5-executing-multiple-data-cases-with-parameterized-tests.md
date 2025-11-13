# 6.5 Executing Multiple Data Cases with Parameterized Tests (pp.131-134)

---
**Page 131**

Executing Multiple Data Cases with Parameterized Tests
Many of your system’s behaviors will demand several distinct test cases. For
example, you’ll often end up with at least three tests as you work through
the progression of zero-one-many.
Defining separate test methods allows you to explicitly summarize their distinct
behaviors in the test names:
storesEmptyStringWhenEmpty
storesInputStringWhenContainingOneElement
storesCommaSeparatedStringWhenContainingManyElements
Often, the three test cases will be structured exactly the same—all the state-
ments within it are the same, but the input and expected output data differ.
You can streamline the redundancies across these tests with things like helper
methods and @BeforeEach methods if it bothers you.
Sometimes, when you have such redundancy across tests, there’s no interest-
ing way to name them distinctly. For example, suppose you have tests for
code that converts Arabic numbers into Roman equivalents:
utj3-junit/01/src/main/java/util/RomanNumberConverter.java
public class RomanNumberConverter {
record Digit(int arabic, String roman) {}
Digit[] conversions = {
new Digit(1000, "M"),
new Digit(900, "CM"),
new Digit(500, "D"),
new Digit(400, "CD"),
new Digit(100, "C"),
new Digit(90, "XC"),
new Digit(50, "L"),
new Digit(40, "XL"),
new Digit(10, "X"),
new Digit(9, "IX"),
new Digit(5, "V"),
new Digit(4, "IV"),
new Digit(1, "I")
};
public String toRoman(int arabic) {
return Arrays.stream(conversions).reduce(
new Digit(arabic, ""),
(acc, conversion) -> {
var digitsRequired = acc.arabic / conversion.arabic;
report erratum  •  discuss
Executing Multiple Data Cases with Parameterized Tests • 131


---
**Page 132**

return new Digit(
acc.arabic - digitsRequired * conversion.arabic,
acc.roman + conversion.roman.repeat(digitsRequired));
}).roman();
}
}
Neither the algorithm nor the behavior changes based on the inputs. Were
you to code this as separate JUnit tests, there’d be little useful distinction
between the test names:
utj3-junit/01/src/test/java/util/ARomanNumberConverter.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
class ARomanNumberConverter {
RomanNumberConverter converter = new RomanNumberConverter();
@Test
void convertsOne() {
assertEquals("I", converter.toRoman(1));
}
@Test
void convertsTwo() {
assertEquals("II", converter.toRoman(2));
}
@Test
void convertsThree() {
assertEquals("III", converter.toRoman(3));
}
// ... so wordy!
}
It’s tedious to create separate tests for each case, and their names add little
real value. You could lump them all in a single test method but then the
individual cases wouldn’t be isolated from each other.
Fortunately, JUnit supports a special form of test known as a parameterized
test. You create a parameterized test by annotating your test method with
@ParameterizedTest instead of @Test. You must also provide a data source, which
is essentially a list of data rows. For each data row, JUnit calls the test method
with data from the row as parameters.
The parameterized test method for the RomanNumberConverter needs two pieces
of information: the Arabic number to be passed to the toRoman method and
the expected Roman equivalent to be used in an assertEquals statement. You
can use a @CsvSource to provide data rows for the test; each row is a CSV
(comma-separated values) string.
Chapter 6. Establishing Organization in JUnit Tests • 132
report erratum  •  discuss


---
**Page 133**

Here’s a parameterized test for the RomanNumberConverter:
utj3-junit/01/src/test/java/util/ARomanNumberConverter.java
@ParameterizedTest
@CsvSource({
"1,
I",
➤
"2,
II",
"3,
III",
"10,
X",
"20,
XX",
"11,
XI",
"200,
CC",
"732,
DCCXXXII",
"2275, MMCCLXXV",
"999,
CMXCIX",
"444,
CDXLIVI", // failure
})
void convertAll(int arabic, String roman) {
➤
assertEquals(roman, converter.toRoman(arabic));
}
The first data row in the @CsvSource (highlighted) contains the CSV string "1,
I".
JUnit splits this string on the comma and trims the resulting values. It passes
these values—the number 1 and the string "I"—to the convertAll test method
(highlighted).
JUnit takes the CSV values and uses them, left to right, as arguments to the
test method. So when the test method is executed, 1 gets assigned to the int
arabic parameter (with JUnit converting the string to an int), and "I" gets assigned
to the String roman parameter.
Since the above example shows eleven CSV data rows, JUnit will run convertAll
eleven times. IntelliJ shows the parameters for each of the eleven cases:
Note how JUnit indicates the failing (incorrectly specified) case.
The JUnit documentation
2 goes into considerable detail about the various
data source mechanisms available.
2.
https://junit.org/junit5/docs/current/user-guide/#writing-tests-parameterized-tests-sources
report erratum  •  discuss
Executing Multiple Data Cases with Parameterized Tests • 133


---
**Page 134**

Here’s a quick summary:
A single array of values. Useful only if your test takes one
parameter (which implies that the expected outcome is the
same for every source value)
@ValueSource
Iterates all the possible enum values, with some options for
inclusion/exclusion and regex matching
@EnumSource
Expects the name of a method, which must return all data
rows in a stream
@MethodSource
Mostly the same thing as @CsvSource, except that you specify
a filename containing the CSV rows
@CsvFileSource
Allows you to create a custom, reusable data source in a
class that extends an interface named ArgumentsProvider
@ArgumentsSource
While parameterized tests in JUnit are sophisticated and flexible beasts,
@CsvSource will suit most of your needs. I’ve never needed another data source
variant (though I don’t frequently use parameterized tests).
In summary, parameterized tests are great when you need to demonstrate
data (not behavioral) variants. These are a couple of pervasive needs:
• Code that conditionally executes if a parameter is null or an empty string.
A parameterized test with two inputs (null and "") lets you avoid test
duplication.
• Code around border conditions, particularly because such code often
breeds defects. For example, for code that conditionally executes if n <= 0,
use a parameterized test with the values n - 1 and n.
Otherwise, create a new @Test that describes a distinct behavior.
Summary
On most systems, you’ll end up with many hundreds or thousands of unit
tests. You’ll want to keep your maintenance costs low by taking advantage
of a few JUnit features, including lifecycle methods, nested classes, and param-
eterized tests. These features allow you to reduce redundant code and make
it easy to run a related set of tests.
Now that you’ve learned how to best organize your tests, in the next chapter,
you’ll dig into topics that relate to executing tests using JUnit. You’ll pick up
some good habits for deciding how many tests to run (and when to not run
tests). You’ll learn how to run subsets of tests as well as how to temporarily
disable tests.
Chapter 6. Establishing Organization in JUnit Tests • 134
report erratum  •  discuss



# 8.1 Our first TDD session (pp.199-206)

---
**Page 199**

199
Our first TDD session
8.1
Our first TDD session
For this example, we will create a program that converts Roman numerals to integers.
Roman numerals represent numbers with seven symbols:
I, unus, 1, (one)
V, quinque, 5 (five)
X, decem, 10 (ten)
L, quinquaginta, 50 (fifty)
C, centum, 100 (one hundred)
D, quingenti, 500 (five hundred)
M, mille, 1,000 (one thousand)
To represent all possible numbers, the Romans combined the symbols, following
these two rules:
Digits of lower or equal value on the right are added to the higher-value digit.
Digits of lower value on the left are subtracted from the higher-value digit.
For instance, the number XV represents 15 (10 + 5), and the number XXIV rep-
resents 24 (10 + 10 – 1 + 5).
 The goal of our TDD session is to implement the following requirement:
Implement a program that receives a Roman numeral (as a string) and
returns its representation in the Arabic numeral system (as an integer).
Coming up with examples is part of TDD. So, think about different inputs you can
give the program, and their expected outputs. For example, if we input "I" to the
program, we expect it to return 1. If we input "XII" to the program, we expect it to
return 12. Here are the cases I can think of:
Simple cases, such as numbers with single characters:
– If we input "I", the program must return 1.
– If we input "V", the program must return 5.
– If we input "X", the program must return 10.
Numbers composed of more than one character (without using the subtrac-
tive notation):
– If we input "II", the program must return 2.
– If we input "III", the program must return 3.
– If we input "VI", the program must return 6.
– If we input "XVII", the program must return 17.
Numbers that use simple subtractive notation:
– If we input "IV", the program must return 4.
– If we input "IX", the program must return 9.


---
**Page 200**

200
CHAPTER 8
Test-driven development
Numbers that are composed of many characters and use subtractive notation:
– If we input "XIV", the program must return 14.
– If we input "XXIX", the program must return 29.
NOTE
You may wonder about corner cases: What about an empty string? or
null? Those cases are worth testing. However, when doing TDD, I first focus
on the happy path and the business rules; I consider corners and boundar-
ies later.
Remember, we are not in testing mode. We are in development mode, coming up with
inputs and outputs (or test cases) that will guide us through the implementation. In
the development flow I introduced in figure 1.4, TDD is part of “testing to guide
development.” When we are finished with the implementation, we can dive into rigor-
ous testing using all the techniques we have discussed.
 Now that we have a (short) list of examples, we can write some code. Let’s do it
this way:
1
Select the simplest example from our list of examples.
2
Write an automated test case that exercises the program with the given input
and asserts its expected output. The code may not even compile at this point.
And if it does, the test will fail, as the functionality is not implemented.
3
Write as much production code as needed to make that test pass.
4
Stop and reflect on what we have done so far. We may improve the production
code. We may improve the test code. We may add more examples to our list.
5
Repeat the cycle.
The first iteration of the cycle focuses on ensuring that if we give "I" as input, the out-
put is 1. The RomanNumeralConverterTest class contains our first test case.
public class RomanNumberConverterTest {
  @Test
  void shouldUnderstandSymbolI() {
    RomanNumeralConverter roman = new RomanNumeralConverter(); 
    int number = roman.convert("I");
    assertThat(number).isEqualTo(1);
  }
}
At this moment, the test code does not compile, because the RomanNumberConverter
class and its convert() method do not exist. To solve the compilation error, let’s cre-
ate some skeleton code with no real implementation.
public class RomanNumeralConverter {
  public int convert(String numberInRoman) {
Listing 8.1
Our first test method
Listing 8.2
Skeleton implementation of the class
We will get compilation errors here,
as the RomanNumeralConverter
class does not exist!


---
**Page 201**

201
Our first TDD session
    return 0; 
  }
}
The test code now compiles. When we run it, it fails: the test expected 1, but the pro-
gram returned 0. This is not a problem, as we expected it to fail. Steps 1 and 2 of our
cycle are finished. It is now time to write as much code as needed to make the test
pass—and it looks weird.
public class RomanNumeralConverter {
  public int convert(String numberInRoman) {
    return 1; 
  }
}
The test passes, but it only works in a single case. Again, this is not a problem: we are
still working on the implementation. We are taking baby steps.
 Let’s move on to the next iteration of the cycle. The next-simplest example in the
list is “If we input "V", the program must return 5.” Let’s again begin with the test.
@Test
void shouldUnderstandSymbolV() {
  RomanNumeralConverter roman = new RomanNumeralConverter();
  int number = roman.convert("V");
  assertThat(number).isEqualTo(5);
}
The new test code compiles and fails. Now let’s make it pass. In the implementation,
we can, for example, make the method convert() verify the content of the number to
be converted. If the value is "I", the method returns 1. If the value is "V", it returns 5.
public int convert(String numberInRoman) {
  if(numberInRoman.equals("I")) return 1; 
  if(numberInRoman.equals("V")) return 5;
  return 0;
}
The two tests pass. We could repeat the cycle for X, L, C, M, and so on, but we already
have a good idea about the first thing our implementation needs to generalize: when
the Roman numeral has only one symbol, return the integer associated with it. How
can we implement such an algorithm?
Write a set of if statements. The number of characters we need to handle is not
excessive.
Listing 8.3
Making the test pass
Listing 8.4
Our second test
Listing 8.5
Making the tests pass
We do not want to return 0, but 
this makes the test code compile.
Returning 1 makes the 
test pass. But is this the 
implementation we want?
Hard-coded ifs are the easiest 
way to make both tests pass.


---
**Page 202**

202
CHAPTER 8
Test-driven development
Write a switch statement, similar to the if implementation.
Use a map that is initialized with all the symbols and their respective integer
values.
The choice is a matter of taste. I will use the third option because I like it best.
public class RomanNumeralConverter {
  private static Map<String, Integer> table =
      new HashMap<>() {{ 
        put("I", 1);
        put("V", 5);
        put("X", 10);
        put("L", 50);
        put("C", 100);
        put("D", 500);
        put("M", 1000);
      }};
  public int convert(String numberInRoman) {
    return table.get(numberInRoman); 
  }
}
How do we make sure our implementation works? We have our (two) tests, and we
can run them. Both pass. The production code is already general enough to work
for single-character Roman numbers. But our test code is not: we have a test called
shouldUnderstandSymbolI and another called shouldUnderstandSymbolV. This specific
case would be better represented in a parameterized test called shouldUnderstandOne-
CharNumbers.
public class RomanNumeralConverterTest {
  @ParameterizedTest
  @CsvSource({"I,1","V,5", "X,10","L,50",
  "C, 100", "D, 500", "M, 1000"}) 
  void shouldUnderstandOneCharNumbers(String romanNumeral,
    ➥ int expectedNumberAfterConversion) {
    RomanNumeralConverter roman = new RomanNumeralConverter();
    int convertedNumber = roman.convert(romanNumeral);
    assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
  }
}
NOTE
The test code now has some duplicate code compared to the produc-
tion code. The test inputs and outputs somewhat match the map in the pro-
duction code. This is a common phenomenon when doing testing by
example, and it will be mitigated when we write more complex tests.
Listing 8.6
RomanNumeralConverter for single-character numbers
Listing 8.7
Generalizing our first test
Declares a conversion table that 
contains the Roman numerals 
and their corresponding 
decimal numbers
Gets the 
number from 
the table
Passes the inputs as a comma-separated 
value to the parameterized test. JUnit 
then runs the test method for each of 
the inputs.


---
**Page 203**

203
Our first TDD session
We are finished with the first set of examples. Let’s consider the second scenario: two
or more characters in a row, such as II or XX. Again, we start with the test code.
@Test
void shouldUnderstandMultipleCharNumbers() {
  RomanNumeralConverter roman = new RomanNumeralConverter();
  int convertedNumber = roman.convert("II");
  assertThat(convertedNumber).isEqualTo(2);
}
To make the test pass in a simple way, we could add the string “II” to the map.
private static Map<String, Integer> table =
  new HashMap<>() {{
    put("I", 1);
    put("II", 2); 
    put("V", 5);
    put("X", 10);
    put("L", 50);
    put("C", 100);
    put("D", 500);
    put("M", 1000);
  }};
If we did this, the test would succeed. But it does not seem like a good idea for imple-
mentation, because we would have to include all possible symbols in the map. It is
time to generalize our implementation again. The first idea that comes to mind is to
iterate over each symbol in the Roman numeral we’re converting, accumulate the
value, and return the total value. A simple loop should do.
public class RomanNumeralConverter {
  private static Map<Character, Integer> table =
      new HashMap<>() {{ 
        put('I', 1);
        put('V', 5);
        put('X', 10);
        put('L', 50);
        put('C', 100);
        put('D', 500);
        put('M', 1000);
      }};
  public int convert(String numberInRoman) {
    int finalNumber = 0; 
Listing 8.8
Tests for Roman numerals with multiple characters
Listing 8.9
Map with all the Roman numerals
Listing 8.10
Looping through each character in the Roman numeral
Adds II. But that means 
we would need to add III, 
IV, and so on—not a 
good idea!
The conversion table 
only contains the 
unique Roman 
numeral.
Variable that aggregates 
the value of each Roman 
numeral


---
**Page 204**

204
CHAPTER 8
Test-driven development
    for(int i = 0; i < numberInRoman.length(); i++) { 
      finalNumber += table.get(numberInRoman.charAt(i));
    }
    return finalNumber;
  }
}
Note that the type of key in the map has changed from String to Character. The
algorithm iterates over each character of the string numberInRoman using the
charAt() method, which returns a char type. We could convert the char to String,
but doing so would add an extra, unnecessary step.
 The three tests continue passing. It is important to realize that our focus in this cycle
was to make our algorithm work with Roman numerals with more than one character—
we were not thinking about the previous examples. This is one of the main advantages
of having the tests: we are sure that each step we take is sound. Any bugs we introduce to
previously working behavior (regression bugs) will be captured by our tests.
 We can now generalize the test code and exercise other examples that are similar to
the previous one. We again use parameterized tests, as they work well for the purpose.
@ParameterizedTest
@CsvSource({"II,2","III,3", "VI, 6", "XVIII, 18",
"XXIII, 23", "DCCLXVI, 766"}) 
void shouldUnderstandMultipleCharNumbers(String romanNumeral,
  ➥ int expectedNumberAfterConversion) {
  RomanNumeralConverter roman = new RomanNumeralConverter();
  int convertedNumber = roman.convert(romanNumeral);
  assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
}
NOTE
I chose the examples I passed to the test at random. Our goal is not to
be fully systematic when coming up with examples but only to use the test
cases as a safety net for developing the feature. When we’re finished, we will
perform systematic testing.
Listing 8.11
Parameterizing the test for multiple characters
A single test method or many?
This test method is very similar to the previous one. We could combine them into a
single test method, as shown here:
@ParameterizedTest
@CsvSource({ 
  // single character numbers
  "I,1","V,5", "X,10","L,50", "C, 100", "D, 500", "M, 1000",
  // multiple character numbers
  "II,2","III,3", "V,5","VI, 6", "XVIII, 18", "XXIII, 23", "DCCLXVI, 766"
})
Gets each 
character’s 
corresponding 
decimal value 
and adds it to 
the total sum
Tries many inputs 
with multiple 
characters. Again, 
CSVSource is the 
simplest way to 
do this.
All the inputs from the different tests 
are combined into a single method.


---
**Page 205**

205
Our first TDD session
Our next step is to make the subtractive notation work: for example, IV should return 4.
As always, let’s start with the test. This time, we add multiple examples: we understand
the problem and can take a bigger step. If things go wrong, we can take a step back.
@ParameterizedTest
@CsvSource({"IV,4","XIV,14", "XL, 40",
"XLI,41", "CCXCIV, 294"}) 
void shouldUnderstandSubtractiveNotation(String romanNumeral,
  ➥ int expectedNumberAfterConversion) {
  RomanNumeralConverter roman = new RomanNumeralConverter();
  int convertedNumber = roman.convert(romanNumeral);
  assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
}
Implementing this part of the algorithm requires more thought. The characters in a
Roman numeral, from right to left, increase in terms of value. However, when a numeral
is smaller than its neighbor on the right, it must be subtracted from instead of added to
the accumulator. Listing 8.13 uses a trick to accomplish this: the multiplier variable
becomes -1 if the current numeral (that is, the current character we are looking at) is
smaller than the last neighbor (that is, the character we looked at previously). We
then multiply the current digit by multiplier to make the digit negative.
public int convert(String numberInRoman) {
  int finalNumber = 0;
  int lastNeighbor = 0; 
  for(int i = numberInRoman.length() - 1; i >= 0; i--) { 
   int current = table.get(numberInRoman.charAt(i)); 
   int multiplier = 1;
   if(current < lastNeighbor) multiplier = -1; 
void convertRomanNumerals(String romanNumeral,
  ➥ int expectedNumberAfterConversion) {
  RomanNumeralConverter roman = new RomanNumeralConverter();
  int convertedNumber = roman.convert(romanNumeral);
  assertThat(convertedNumber).isEqualTo(expectedNumberAfterConversion);
}
This is a matter of taste and your team’s preference. For the remainder of the chap-
ter, I keep the test methods separated.
Listing 8.12
Test for the subtractive notation
Listing 8.13
Implementation for the subtractive notation
Provides many inputs that exercise 
the subtractive notation rule
Keeps the last 
visited digit
Loops through the 
characters, but now 
from right to left
Gets the decimal value of 
the current Roman digit
If the previous digit was 
higher than the current one, 
multiplies the current digit 
by -1 to make it negative


---
**Page 206**

206
CHAPTER 8
Test-driven development
   finalNumber +=
     table.get(numberInRoman.charAt(i)) * multiplier; 
   lastNeighbor = current; 
  }
  return finalNumber;
}
The tests pass. Is there anything we want to improve in the production code? We use
numberInRoman.charAt(i) when summing the final number, but this value is already
stored in the current variable, so we can reuse it. Also, extracting a variable to store
the current digit after it is multiplied by 1 or -1 will help developers understand the
algorithm. We can refactor the code, as shown in the following listing, and run the
tests again.
public int convert(String numberInRoman) {
  int finalNumber = 0;
  int lastNeighbor = 0; 
  for(int i = numberInRoman.length() - 1; i >= 0; i--) {
   int current = table.get(numberInRoman.charAt(i));
   int multiplier = 1;
   if(current < lastNeighbor) multiplier = -1;
   int currentNumeralToBeAdded = current * multiplier; 
   finalNumber += currentNumeralToBeAdded;
   lastNeighbor = current;
  }
  return finalNumber;
}
Now that we have implemented all the examples in our initial list, we can think of other
cases to handle. We are not handling invalid numbers, for example. The program must
reject inputs such as "VXL" and "ILV". When we have new examples, we repeat the
entire procedure until the whole program is implemented. I will leave that as an exer-
cise for you—we have done enough that we are ready to more formally discuss TDD. 
8.2
Reflecting on our first TDD experience
Abstractly, the cycle we repeated in the previous section’s development process was
as follows:
1
We wrote a (unit) test for the next piece of functionality we wanted to imple-
ment. The test failed.
Listing 8.14
Refactored version
Adds the current digit 
to the finalNumber 
variable. The current 
digit is positive or 
negative depending on 
whether we should 
add or subtract it, 
respectively.
Updates 
lastNeighbor 
to be the 
current digit
Keeps the last 
digit visited
Uses the current
variable and introduces the
currentNumeralToBeAdded variable



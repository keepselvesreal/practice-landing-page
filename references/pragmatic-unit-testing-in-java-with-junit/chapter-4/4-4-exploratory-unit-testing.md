# 4.4 Exploratory Unit Testing (pp.90-95)

---
**Page 90**

Ensure you run coverage tools to verify that all the code is getting tested. The
tests for QuestionRepository show that it’s completely covered with tests. Also, if
you use integration tests to cover some small portions of code rather than
unit tests, your system-wide unit test code coverage numbers will suffer a
little. If that concerns you, you might be able to merge the numbers properly
(the tool jacoco:merge
1 works for JaCoCo).
Exploratory Unit Testing
The unit tests you’ve learned to build capture your best understanding of the
intents in the code. They cover known edge cases and typical use cases.
Some code may demand further exploration. For example, complex code, code
that seems to keep breaking as you uncover more nuances about the input
data, or code that incurs a high cost if it were to fail. Systems requiring high
reliability or security might incur significant costs from unit-level failures.
Numerous kinds of developer-focused tests exist to help you with such
exploratory testing. Many of them verify at the integration level—load tests,
failover tests, performance tests, and contract tests, to name a few. You can
learn about some of these in Alexander Tarlinder’s book Developer Testing.
2
Following is an overview of two unit-level testing tactics: fuzz testing and
property testing, which can be considered forms of what’s known as generative
testing. These sorts of tests require additional tooling above and beyond JUnit,
and thus, you’re only getting an introduction to them in this book. (That’s
one excuse among a few, and I’m sticking with it.)
Not covered at all: mutation testing, which involves tools that make small
changes to your production code to see if such changes break your tests. If
your tests don’t break, the mutation tests suggest you might have insufficient
test coverage.
Fuzz Testing
With fuzz testing, you use a tool to provide a wide range of random, unexpected,
or invalid inputs to your code. It can help you identify edge cases in your
code that you’re otherwise unlikely to think of when doing traditional unit
testing.
1.
https://www.jacoco.org/jacoco/trunk/doc/merge-mojo.html
2.
https://www.informit.com/store/developer-testing-building-quality-into-software-9780134431802
Chapter 4. Expanding Your Testing Horizons • 90
report erratum  •  discuss


---
**Page 91**

This URL creator code combines server and document strings into a valid
URL string:
utj3-iloveyouboss2/03/src/main/java/util/URLCreator.java
import java.net.MalformedURLException;
import java.net.URL;
import static java.lang.String.format;
public class URLCreator {
public String create(String server, String document)
throws MalformedURLException {
if (isEmpty(document))
return new URL(format("https://%s", server)).toString();
return new URL(
format("https://%s/%s", server, clean(document))).toString();
}
private boolean isEmpty(String document) {
return document == null || document.trim().equals("");
}
private String clean(String document) {
return document.charAt(0) == '/'
? document.substring(1)
: document;
}
}
Here are the tests:
utj3-iloveyouboss2/03/src/test/java/util/AURLCreator.java
import org.junit.jupiter.api.Test;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.NullSource;
import org.junit.jupiter.params.provider.ValueSource;
import java.net.MalformedURLException;
import static org.junit.jupiter.api.Assertions.assertEquals;
class AURLCreator {
URLCreator urlCreator = new URLCreator();
@Test
void returnsCombinedURLStringGivenServerAndDocument()
throws MalformedURLException {
assertEquals(
"https://example.com/customer?id=123",
urlCreator.create("example.com", "customer?id=123"));
}
@ParameterizedTest
@NullSource
report erratum  •  discuss
Exploratory Unit Testing • 91


---
**Page 92**

@ValueSource(strings = { "", " \n\t\r " })
void buildsURLGivenServerOnly(String document)
throws MalformedURLException {
assertEquals(
"https://example.com",
urlCreator.create("example.com", document));
}
@Test
void eliminatesRedundantLeadingSlash() throws MalformedURLException {
assertEquals(
"https://example.com/customer?id=123",
urlCreator.create("example.com", "/customer?id=123"));
}
}
Code like this tends to grow over time as you think of additional protections
to add. The third test deals with the case where the caller of the create method
prepends the document with a forward slash—"/employee?id=42", for example.
Someone likely wasn’t sure if the slash needed to be provided or not. The
developer, as a result, updated the code to allow either circumstance.
With fuzz testing, you’ll likely add more protections and corresponding tests
as the fuzzing effort uncovers additional problems.
You can write fuzz tests using the tool Jazzer:
3
utj3-iloveyouboss2/03/src/test/java/util/AURLCreatorFuzzer.java
import com.code_intelligence.jazzer.api.FuzzedDataProvider;
import com.code_intelligence.jazzer.junit.FuzzTest;
import java.net.MalformedURLException;
public class AURLCreatorFuzzer {
@FuzzTest
public void fuzzTestIsValidURL(FuzzedDataProvider data)
throws MalformedURLException {
var server = data.consumeString(32);
var document = data.consumeRemainingAsString();
new URLCreator().create(server, document);
}
}
Fuzz test methods are annotated with @FuzzTest, and passed a data provider.
From this data provider (a wrapper around some random stream of data),
you can extract the data you need. The test fuzzTestIsValidUrl first extracts a 32-
character string to be passed as the server, then uses the remaining incoming
data as the document.
3.
https://github.com/CodeIntelligenceTesting/jazzer
Chapter 4. Expanding Your Testing Horizons • 92
report erratum  •  discuss


---
**Page 93**

To run fuzzing with Jazzer, first create a directory in your project’s test
resources. Derive its name from your fuzzer class’s package plus the fuzzer
class name plus the word Inputs:
utj3-iloveyouboss2/src/test/resources/util/AURLCreatorFuzzerInputs
Then run your tests with the environment variable setting JAZZER_FUZZ=1. The
fuzzing tool will display failures and add the inputs causing the failures to
files within the resource directory you created.
The fuzzer should report that an input containing an LF (line feed character;
ASCII value 10) represents an invalid character for a URL. You, as the devel-
oper, get to decide how you want the code to deal with that, if at all.
You can also collect a number of inputs in the test resources directory. With
the JAZZER_FUZZ environment variable turned off, Jazzer will use these inputs
to run what effectively become regression test inputs.
Property Testing
Another form of unit testing is property testing, where your tests describe
invariants and postconditions, or properties, about the expected behavior of
code. Property testing tools, such as jqwik,
4 will test these invariants using
a wide range of automatically generated inputs.
Your primary reason for using property tests is to uncover edge cases and
unexpected behaviors by virtue of exploring a broader range of inputs.
Here’s an implementation for the insertion sort algorithm, which performs
terribly but is a reasonable choice if your input array is small (or if your inputs
are generally almost sorted already):
utj3-iloveyouboss2/03/src/main/java/util/ArraySorter.java
public class ArraySorter {
public void inPlaceInsertionSort(int[] arr) {
for (var i = 1; i < arr.length - 1; i++) {
var key = arr[i];
var j = i - 1;
while (j >= 0 && arr[j] > key) {
arr[j + 1] = arr[j];
j = j - 1;
}
arr[j + 1] = key;
}
}
}
4.
https://jqwik.net
report erratum  •  discuss
Exploratory Unit Testing • 93


---
**Page 94**

Using jqwik, you define @Property methods that get executed by the JUnit test
runner. The following set of properties for ArraySorter describes three properties:
an already-sorted array should remain sorted, an array with all the same
elements should remain unchanged, and a random array should be sorted
in ascending order:
utj3-iloveyouboss2/03/src/test/java/util/ArraySorterProperties.java
import static java.util.Arrays.fill;
import static java.util.Arrays.sort;
import net.jqwik.api.*;
import java.util.Arrays;
public class ArraySorterProperties {
ArraySorter arraySorter = new ArraySorter();
@Property
boolean returnsSameArrayWhenAlreadySorted(@ForAll int[] array) {
sort(array);
var expected = array.clone();
arraySorter.inPlaceInsertionSort(array);
return Arrays.equals(expected, array);
}
@Property
boolean returnsSameArrayWhenAllSameElements(@ForAll int element) {
var array = new int[12];
fill(array, element);
var expected = array.clone();
arraySorter.inPlaceInsertionSort(array);
return Arrays.equals(expected, array);
}
@Property
boolean sortsAscendingWhenRandomUnsortedArray(@ForAll int[] array) {
var expected = array.clone();
sort(expected);
arraySorter.inPlaceInsertionSort(array);
return Arrays.equals(expected, array);
}
}
Taking the last method as an example: sortsAscendingForRandomUnsortedArray rep-
resents a postcondition that should hold true for all (@ForAll) input arrays (array).
The property implementation clones the incoming array and sorts it using
Java’s built-in sort, capturing the result as expected. It sorts the incoming
array, then returns the result of comparing that sort to expected.
Chapter 4. Expanding Your Testing Horizons • 94
report erratum  •  discuss


---
**Page 95**

Jqwik, a sophisticated and highly flexible tool, calls the property one thousand
times by default. And, beauty! The last property fails, and consistently so,
given those thousand inputs.
The array sort code represents a good fit for property testing. You might think
to write a handful of test cases (ZOM, certainly). But there are some cases
that can be hard to think of. Property testing can help uncover those cases.
Yes, there’s a defect in the insertion sort. The jqwik tool should identify the
problem. See if you can figure out and fix the defective code.
Summary
In this chapter, you rounded out your knowledge of core unit testing concepts
with a few (mostly unrelated) topics that look at bigger concerns surrounding
unit testing:
• Code coverage, a concept that can help you learn where your unit testing
is deficient
• Testing multithreaded code, a tricky and sophisticated challenge
• Integration tests, which verify code and its interaction with external
dependencies that might be out of your control
Now that you’ve worked through foundational concepts regarding unit testing,
you’ll take a deeper look into the preferred tool for Java unit testing, JUnit.
The next three chapters will explore JUnit in-depth, providing useful insights
and nuggets on how to best take advantage of its wealth of features.
report erratum  •  discuss
Summary • 95



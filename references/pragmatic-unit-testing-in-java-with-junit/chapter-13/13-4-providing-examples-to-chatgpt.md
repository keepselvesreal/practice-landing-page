# 13.4 Providing Examples to ChatGPT (pp.248-251)

---
**Page 248**

4. In general, create very short, intention-revealing functions for any complexity.
5. Avoid the use of temporaries in most cases unless there is a strong reason to use
them (for example, to use them more than once within a single expression). Instead,
extract the temporary’s initialization to a separate function with the same name as
the temporary, then inline the temporary to remove it.
ChatGPT affirmed my request:
CHAT-GPT:
Understood! Blah blah blah...
You might wonder why I even bothered telling my LLM to improve the code.
If an LLM can generate the code I need, I shouldn’t have to read it.
However, hearken back to the earlier mentioned limitations of LLMs like
ChatGPT. They’re gonna be wrong at times…just like you and me. You’ll have
to read and manually update some amount of code. Even as that need likely
diminishes over time, keeping your code organized (by predominantly creating
small classes and methods) appears to increase the odds that the LLM-
generated code is correct.
Providing Examples to ChatGPT
Incrementally test driving small, unit behaviors into a system remains the
best choice for humans. For an LLM, maybe not.
I first tried getting ChatGPT to consume all my requirements for the name
normalizer at once. The code was a mess, and it didn’t work. I took the next-
smaller step, which was to first give it a subset containing the four core cases
it needed to cover. I helped ChatGPT focus on what I believe to be a proper
design—one that, in general, is based on small classes and small methods.
With such an improved design, I believe ChatGPT had a much better chance
to correctly generate new increments.
One of the best ways to get good results from an LLM is to provide examples
in your prompts. I followed that advice for the name normalizer after first
describing in English what I wanted. My prompt provided five examples for
four core cases:
YOU:
Write Java code for a feature known as the name normalizer. Given a per-
son’s name, the name normalizer should return the last name first, followed by a
comma, then the first name.
If there is one or more middle names, return the initial of each. The initial is the first
letter followed by a period.
Assume that the name provided to the method is never empty or null.
Chapter 13. Keeping AI Honest with Unit Tests • 248
report erratum  •  discuss


---
**Page 249**

Examples:
input: Plato
output: Plato
input: Leonard Cohen
output: Cohen, Leonard
input: Samuel Leroy Jackson
output: Jackson, Samuel L.
input: George Raymond Richard Martin
output: Martin, George R. R.
input: Emma Azalia Smith Hackley
output: Hackley, Emma A. S.
Unit tests and examples are birds of a feather—remember this tip from
Chapter 10, Streamlining Your Tests, on page 189:
Good tests provide examples of how clients interact with the
system.
Accordingly, I told my LLM to translate the examples into tests:
YOU:
Also, provide JUnit tests for the core cases.
I took a few seconds to vet the tests that ChatGPT generated to ensure that
they correctly aligned with my examples. ChatGPT did a decent job, generating
tests that used the same data as the examples I provided:
utj3-ai/01/src/test/java/util/NameNormalizerTest.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
public class NameNormalizerTest {
@Test
public void testSingleName() {
assertEquals("Plato",
NameNormalizer.normalizeName("Plato"));
}
@Test
public void testFirstNameLastName() {
assertEquals("Cohen, Leonard",
NameNormalizer.normalizeName("Leonard Cohen"));
}
report erratum  •  discuss
Providing Examples to ChatGPT • 249


---
**Page 250**

@Test
public void testMultipleMiddleNames() {
assertEquals("Jackson, Samuel L.",
NameNormalizer.normalizeName("Samuel Leroy Jackson"));
assertEquals("Martin, George R. R.",
NameNormalizer.normalizeName("George Raymond Richard Martin"));
}
@Test
public void testLongName() {
assertEquals("Hackley, Emma A. S.",
NameNormalizer.normalizeName("Emma Azalia Smith Hackley"));
}
}
ChatGPT got a little confused regarding the tests testMultipleMiddleNames and
testLongName. I had ChatGPT fix this later (as I also did with the unnecessary test
prefix for each test).
ChatGPT did a job (in other words, not a fine one) generating the corresponding
normalizer implementation:
utj3-ai/01/src/main/java/util/NameNormalizer.java
import java.util.Arrays;
import java.util.stream.Collectors;
public class NameNormalizer {
public static String normalizeName(String name) {
var nameParts = name.split(" ");
if (nameParts.length == 1) {
return name;
}
var lastName = nameParts[nameParts.length - 1];
var firstName = nameParts[0];
var middleNames =
Arrays.copyOfRange(nameParts, 1, nameParts.length - 1);
return formatLastNameFirst(lastName, firstName, middleNames);
}
private static String formatLastNameFirst(
String lastName, String firstName, String[] middleNames) {
var middleInitials = Arrays.stream(middleNames)
.map(NameNormalizer::extractInitial)
.collect(Collectors.joining(" "));
return middleInitials.isEmpty() ?
String.format("%s, %s", lastName, firstName) :
String.format("%s, %s %s", lastName, firstName, middleInitials);
}
Chapter 13. Keeping AI Honest with Unit Tests • 250
report erratum  •  discuss


---
**Page 251**

private static String extractInitial(String name) {
return name.charAt(0) + ".";
}
}
Telling Your LLM to Clean Up Its Act
The LLM’s solution passed the tests, and it wasn’t bad, actually, but there
were a few wrinkles to iron out. First, it didn’t include a package name, which
forced me to copy only part of its solution rather than wholesale copy-and-
replace the generated code, which is a lot faster. (I’m imagining a near future
where integration with IDEs is a lot better, and, in fact, I’ve begun building
such a plugin myself.)
Here’s my prompt to tell the LLM to add the package name, as well as smooth
out the aforementioned wrinkles:
YOU:
The code should live in a Java package named util.
The Jeff-Java standard indicates that you should avoid the use of temporaries in
methods, but normalizeName has three temps that should be eliminated.
Do not include the word test in the test name; it is redundant.
Do not use static methods for the implementation. Prefer using instance methods
for generated code.
Update the Jeff-Java standard where appropriate to fix these problems for any code
generated going forward.
ChatGPT did a good job of delivering:
utj3-ai/02/src/test/java/util/NameNormalizerTest.java
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
public class NameNormalizerTest {
private final NameNormalizer normalizer = new NameNormalizer();
@Test
public void singleName() {
assertEquals("Plato", normalizer.normalizeName("Plato"));
}
@Test
public void firstNameLastName() {
assertEquals("Cohen, Leonard",
normalizer.normalizeName("Leonard Cohen"));
}
report erratum  •  discuss
Telling Your LLM to Clean Up Its Act • 251



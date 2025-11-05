# 13.5 Telling Your LLM to Clean Up Its Act (pp.251-255)

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


---
**Page 252**

@Test
public void multipleMiddleNames() {
assertEquals("Jackson, Samuel L.",
normalizer.normalizeName("Samuel Leroy Jackson"));
assertEquals("Martin, George R. R.",
normalizer.normalizeName("George Raymond Richard Martin"));
}
@Test
public void longName() {
assertEquals("Hackley, Emma A. S.",
normalizer.normalizeName("Emma Azalia Smith Hackley"));
}
}
utj3-ai/02/src/main/java/util/NameNormalizer.java
import java.util.Arrays;
import java.util.stream.Collectors;
public class NameNormalizer {
public String normalizeName(String name) {
var nameParts = name.split(" ");
if (nameParts.length == 1) {
return name;
}
return formatLastNameFirst(nameParts[0],
nameParts[nameParts.length - 1],
Arrays.copyOfRange(
nameParts, 1, nameParts.length - 1));
}
private String formatLastNameFirst(
String firstName, String lastName, String[] middleNames) {
var middleInitials = Arrays.stream(middleNames)
.map(this::extractInitial)
.collect(Collectors.joining(" "));
return middleInitials.isEmpty() ?
String.format("%s, %s", lastName, firstName) :
String.format("%s, %s %s", lastName, firstName, middleInitials);
}
private String extractInitial(String name) {
return name.charAt(0) + ".";
}
}
And once again, all tests passed.
I disliked a few of its choices, but found the code fairly easy to follow and…
almost good enough. I complained immediately:
Chapter 13. Keeping AI Honest with Unit Tests • 252
report erratum  •  discuss


---
**Page 253**

YOU:
The arguments to formatLastNameFirst should have first been extracted to new
functions, perhaps named firstName, middleNames, and lastName respectively.
Update the Jeff-Java standard to indicate that the right-hand side of an assignment
should first be extracted to a new function before inlining, if it is anything that
involves "implementation-specific details," i.e., anything that might need to be
explained.
Now we were talking! ChatGPT was doing a pretty good job of listening.
utj3-ai/03/src/main/java/util/NameNormalizer.java
import java.util.Arrays;
import java.util.stream.Collectors;
public class NameNormalizer {
public String normalizeName(String name) {
var nameParts = name.split(" ");
if (nameParts.length == 1) {
return name;
}
return formatLastNameFirst(
➤
firstName(nameParts),
➤
lastName(nameParts),
➤
middleNames(nameParts));
➤
}
private String firstName(String[] nameParts) {
➤
return nameParts[0];
➤
}
➤
private String lastName(String[] nameParts) {
➤
return nameParts[nameParts.length - 1];
➤
}
➤
private String[] middleNames(String[] nameParts) {
➤
return Arrays.copyOfRange(
➤
nameParts, 1, nameParts.length - 1);
➤
}
➤
private String formatLastNameFirst(
String firstName, String lastName, String[] middleNames) {
var middleInitials = Arrays.stream(middleNames)
.map(this::extractInitial)
.collect(Collectors.joining(" "));
return middleInitials.isEmpty() ?
String.format("%s, %s", lastName, firstName) :
String.format("%s, %s %s", lastName, firstName, middleInitials);
}
private String extractInitial(String name) {
return name.charAt(0) + ".";
}
}
report erratum  •  discuss
Telling Your LLM to Clean Up Its Act • 253


---
**Page 254**

The code was at the point where I could easily reason about exactly what was
going on. It took only a moment to understand any one method and trust
that it did what it said.
I prompted ChatGPT to fix a few more things:
YOU:
Simplify the method named extractInitial to initial.
Move the assertion for "Samuel Leroy Jackson" to a new test initializesMiddleName.
Move the assertion for "Emma Azalia Smith Hackley" to the test multipleMiddleNames.
Eliminate the arguments to formatLastNameFirst. Instead, have its code directly access
the functions firstName, lastName, and middleNames.
ChatGPT complied:
utj3-ai/04/src/test/java/util/NameNormalizerTest.java
@Test
public void initializesMiddleName() {
assertEquals("Jackson, Samuel L.",
normalizer.normalizeName("Samuel Leroy Jackson"));
}
@Test
public void multipleMiddleNames() {
assertEquals("Martin, George R. R.",
normalizer.normalizeName("George Raymond Richard Martin"));
assertEquals("Hackley, Emma A. S.",
normalizer.normalizeName("Emma Azalia Smith Hackley"));
}
utj3-ai/04/src/main/java/util/NameNormalizer.java
public String normalizeName(String name) {
this.nameParts = name.split(" ");
if (nameParts.length == 1) {
return name;
}
return formatLastNameFirst();
}
// ...
private String formatLastNameFirst() {
➤
var middleInitials = Arrays.stream(middleNames())
.map(this::initial)
.collect(Collectors.joining(" "));
return middleInitials.isEmpty() ?
String.format("%s, %s", lastName(), firstName()) :
➤
String.format("%s, %s %s", lastName(), firstName(), middleInitials);
➤
}
private String initial(String name) {
➤
return name.charAt(0) + ".";
}
Chapter 13. Keeping AI Honest with Unit Tests • 254
report erratum  •  discuss


---
**Page 255**

Adding a New Feature: Suffixes
I moved on to the next code increment, again providing an example for the
LLM to translate into a test.
YOU:
Alter both the code and the tests to support suffixes. A suffix appears after
a comma at the end of a name.
Examples
input: Martin Luther King, Jr.
output: King, Martin L., Jr.
Here’s what ChatGPT spewed out:
utj3-ai/05/src/test/java/util/NameNormalizerTest.java
@Test
public void nameWithSuffix() {
assertEquals("King, Martin L., Jr.",
normalizer.normalizeName("Martin Luther King, Jr."));
}
utj3-ai/05/src/main/java/util/NameNormalizer.java
public class NameNormalizer {
private String[] nameParts;
private String suffix = "";
➤
public String normalizeName(String name) {
if (name.contains(",")) {
➤
var parts = name.split(", ");
➤
this.nameParts = parts[0].split(" ");
➤
this.suffix = ", " + parts[1];
➤
} else {
➤
this.nameParts = name.split(" ");
➤
}
➤
➤
if (nameParts.length == 1) {
➤
return name;
➤
}
➤
➤
return formatLastNameFirst() + suffix;
➤
}
// ...
}
That went to pot pretty quickly. It did work, at least for the test case I gave
it, but the code was back to stepwise, intertwined logic that was hard to follow.
Also, ChatGPT seemed to have forgotten my Jeff-Java style rules.
report erratum  •  discuss
Adding a New Feature: Suffixes • 255



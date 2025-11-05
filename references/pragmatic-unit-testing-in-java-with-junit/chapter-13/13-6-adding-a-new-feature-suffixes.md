# 13.6 Adding a New Feature: Suffixes (pp.255-260)

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


---
**Page 256**

Letting Your LLM Discover Missing Tests
Before I asked ChatGPT to fix the code, I took a little detour. I thought it might
be useful to ask ChatGPT to generate test cases for its own code but in a new
conversation. It produced this:
utj3-ai/05/src/test/java/util/NameNormalizerAITest.java
public class NameNormalizerAITest {
private NameNormalizer normalizer = new NameNormalizer();
@Test
public void testSimpleTwoPartName() {
assertEquals("Doe, John", normalizer.normalizeName("John Doe"));
}
@Test
public void testNameWithMiddleInitial() {
assertEquals("Doe, John A.",
normalizer.normalizeName("John A. Doe"));
}
@Test
public void testNameWithSuffix() {
assertEquals("Doe, John Jr.",
normalizer.normalizeName("John Doe, Jr."));
}
@Test
public void testSingleName() {
assertEquals("John", normalizer.normalizeName("John"));
}
@Test
public void testNameWithMiddleNames() {
assertEquals("Doe, John A. B.",
normalizer.normalizeName("John Adam Bernard Doe"));
}
@Test
public void testEmptyString() {
assertEquals("", normalizer.normalizeName(""));
}
// Optional: If handling null is expected
@Test
public void testNullInput() {
assertEquals(null, normalizer.normalizeName(null));
}
}
The generated test cases were decent, though again, they ignored the Jeff-
Java rule around test names. When I ran them, I discovered two test failures:
Chapter 13. Keeping AI Honest with Unit Tests • 256
report erratum  •  discuss


---
**Page 257**

testNameWithSuffix and testNullInput. I ignored testNullInput since I’d decided the input
to normalizeName couldn’t ever be null.
The other failing test, testNameWithSuffix, involved a two-part name, whereas I’d
only provided a three-part name to ChatGPT as an example. When I copied
the test code for testNameWithSuffix into NameNormalizerTest, it still failed.
ChatGPT indeed had discerned the need for a test case that I’d missed! The
failing test didn’t point out a problem with the code, though—its expected
output for “John Doe, Jr.” was incorrect (it should have been “Doe, John,
Jr.”, with a comma after the first name).
I considered what I knew about iterating via ZOM (see ZOM: Zero and One
Done, Now Testing Many, on page 22) and gave ChatGPT a one-two-three set
of examples.
YOU:
Try again with the following changes.
Alter both the code and the tests to support suffixes. A suffix appears after a comma
at the end of a name.
Examples
input: Madonna, Esq.
output: Madonna, Esq.
input: John Doe, Sr.
output: Doe, John, Sr.
input: Martin Luther King, Jr.
output: King, Martin L., Jr.
Ensure you use the Jeff-Java standard. Most importantly, find a way to keep the
suffix code isolated from as much of the existing code within NameNormalizer as
possible.
Do not include any tests around a null name.
At first glance, the result looked promising:
utj3-ai/06/src/test/java/util/NameNormalizerTest.java
@Test
public void nameWithSuffix() {
assertEquals("King, Martin L., Jr.",
normalizer.normalizeName("Martin Luther King, Jr."));
assertEquals("Doe, John, Sr.",
normalizer.normalizeName("John Doe, Sr."));
}
report erratum  •  discuss
Adding a New Feature: Suffixes • 257


---
**Page 258**

@Test
public void singleNameWithSuffix() {
assertEquals("Madonna, Esq.",
normalizer.normalizeName("Madonna, Esq."));
}
utj3-ai/06/src/main/java/util/NameNormalizer.java
public class NameNormalizer {
private String[] nameParts;
private String suffix = "";
public String normalizeName(String name) {
extractSuffix(name);
if (nameParts.length == 1 && suffix.isEmpty()) {
return name;
}
return formatLastNameFirst() + suffix;
}
private void extractSuffix(String name) {
if (name.contains(",")) {
var parts = name.split(", ", 2);
this.nameParts = parts[0].split(" ");
this.suffix = ", " + parts[1];
} else {
this.nameParts = name.split(" ");
}
}
// ...
}
The AI solution was awkward. The method extractSuffix did extract the suffix,
but it also set a value into nameParts, making the logic much harder to follow.
A better solution would involve a pure function named extractSuffix that does
only that—given a name, return the suffix or empty string.
I ignored the deficiency. ChatGPT was teaching me not to sweat the small
stuff as much—unlike building my own code, where tending to all the
small things speeds me up over time.
It had also become apparent that nitpicking every nuance of what the LLM
produced seemed like it would take hours. I decided I’d prompt ChatGPT to
fix the problem if I needed to revisit the extractSuffix method.
From AI, “good enough to have an easy conversation about” is
good enough.
Chapter 13. Keeping AI Honest with Unit Tests • 258
report erratum  •  discuss


---
**Page 259**

ChatGPT Breaks the Code
On the surface, the code ChatGPT produced was reasonable, except for the way
it had designed extractSuffix. Alas, I now had a test failure involving poor Madonna.
Expected :Madonna, Esq.
Actual
:Madonna, Madonna, Esq.
“Madonna, Madonna, Esquire?” Sounds like a potential song, maybe a blatant
ripoff of “Vogue.” Maybe I should get ChatGPT to write some lyrics. (I did.)
1
I went with the lazy flow—I asked ChatGPT to fix its mistake. (It broke stuff,
so why should I fix it?) ChatGPT has had the effect of making me lazy, but
maybe that’s the good kind of lazy.
YOU:
Expected :Madonna, Esq.
Actual :Madonna, Madonna, Esq.
See if you can fix the problem.
The LLM had a sense of what was going on and how to fix it:
CHAT-GPT:
The issue with the Madonna-based test case failing is due to how the
normalization logic is applied even when there’s only a single name part before
the suffix, leading to the repetition of the name. To fix this, we need to adjust the
logic to correctly handle cases where there’s only a single name part (i.e., no first
and last name separation, but potentially a suffix).
The fix offered did pass the tests:
utj3-ai/07/src/main/java/util/NameNormalizer.java
public String normalizeName(String name) {
extractSuffix(name);
// Handle case for 1 name w/ no middle names but possible a suffix
if (nameParts.length == 1) {
➤
return nameParts[0] + suffix;
➤
}
➤
return formatLastNameFirst() + suffix;
}
Defects in code are often good at hiding themselves—broken things may look
reasonable. But reasonable isn’t correct.
Don’t ship code just because it looks good.
1.
https://langrsoft.com/2024/01/23/madonna/
report erratum  •  discuss
Adding a New Feature: Suffixes • 259


---
**Page 260**

Getting the LLM to Do Final Design Cleanup
The last thing to tackle was some final code cleanup.
YOU:
The solution works. The method extractSuffix should be reworked, however,
into a pure function (i.e., with no side effects). The side effects, if needed, should
occur in normalizeName.
Also, I just noticed the silliness in formatLastNameFirst. Inline the temporaries, please.
Oh my. I don’t want to show you the abomination it produced, but I suppose
I must. Here’s a small piece of it:
utj3-ai/08/src/main/java/util/NameNormalizer.java
public String normalizeName(String name) {
var extractedResult = extractSuffix(name);
var nameParts = extractedResult[0].split(" ");
var suffix = extractedResult[1];
if (nameParts.length == 1) {
return nameParts[0] + suffix;
}
var middleInitials = Arrays.stream(middleNames(nameParts))
.map(this::initial)
.collect(Collectors.joining(" "));
return (nameParts[nameParts.length - 1] + ", " + nameParts[0] +
(middleInitials.isEmpty() ? "" : " " + middleInitials)) + suffix;
}
I was a little upset at this point. My message to ChatGPT wasn’t very pleasant.
YOU:
Undo that last change. It’s horrible. You inlined the helper functions like
last(). Show me the prior version.
Thankfully, ChatGPT only undid the inlining mess. It retained the conversion
of extractSuffix to a functional method:
utj3-ai/09/src/main/java/util/NameNormalizer.java
public String normalizeName(String name) {
var result = extractSuffix(name);
this.nameParts = result[0].split(" ");
this.suffix = result[1];
if (nameParts.length == 1) {
return nameParts[0] + suffix;
}
return formatLastNameFirst() + suffix;
}
Chapter 13. Keeping AI Honest with Unit Tests • 260
report erratum  •  discuss



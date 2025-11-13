# 13.7 Getting the LLM to Do Final Design Cleanup (pp.260-262)

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


---
**Page 261**

private String[] extractSuffix(String name) {
if (name.contains(",")) {
var parts = name.split(", ", 2);
return new String[] {parts[0], ", " + parts[1]};
} else {
return new String[] {name, ""};
}
}
private String formatLastNameFirst() {
return lastName() + ", " + firstName() + middleInitialsString();
}
private String firstName() {
return nameParts[0];
}
private String lastName() {
return nameParts[nameParts.length - 1];
}
private String middleInitialsString() {
if (nameParts.length > 2) {
return " " + Arrays.stream(middleNames())
.map(this::initial)
.collect(Collectors.joining(" "));
}
return "";
}
private String[] middleNames() {
if (nameParts.length > 2) {
return Arrays.copyOfRange(nameParts, 1, nameParts.length - 1);
}
return new String[]{};
}
private String initial(String name) {
return name.charAt(0) + ".";
}
}
Its new solution clarified to me what ChatGPT was trying to do all along, but
I hadn’t noticed. The extractSuffix method was now returning a tuple—or Java’s
code-heavy version of one—a two-dimensional array containing the base name
and suffix. With modern Java, using a record seemed a better choice.
YOU:
Replace the tuple returned by extractSuffix with a version that uses a Java
record, defined as a nested class within NameNormalizer.
report erratum  •  discuss
Getting the LLM to Do Final Design Cleanup • 261


---
**Page 262**

ChatGPT did the job:
utj3-ai/10/src/main/java/util/NameNormalizer.java
private record ExtractedNameParts(String[] nameParts, String suffix) {}
public String normalizeName(String name) {
var extractedNameParts = extractSuffix(name);
this.nameParts = extractedNameParts.nameParts();
this.suffix = extractedNameParts.suffix();
if (nameParts.length == 1) {
return nameParts[0] + suffix;
}
return formatLastNameFirst() + suffix;
}
private ExtractedNameParts extractSuffix(String name) {
if (name.contains(",")) {
var parts = name.split(", ", 2);
return new ExtractedNameParts(parts[0].split(" "), ", " + parts[1]);
} else {
return new ExtractedNameParts(name.split(" "), "");
}
}
I’ll take it. I felt that the code still had numerous little problems, particularly
some bits where the code didn’t declare well what was going on. For example,
what’s nameParts[0]? What’s parts[0]?
But maybe that’s okay. I reminded myself that I wasn’t trying to create “perfect”
code. (As if there was such a thing.)
It is important that an AI solution is composed of focused units. (Huh!) Small,
single-purpose methods allow ChatGPT to employ intention-revealing, accurate
method and variable names. In turn, those small, accurately named concepts
allow both the LLM and you (or me) to continue with a sensible conversation
as you add more increments and fix problems.
For Extra Credit
Start a similar conversation with your LLM of choice to build the name nor-
malizer. Then, see how effective a solution it can produce by prompting a
couple more features.
1.
Harry Truman had a single-letter middle name, sort of, implying that it
should not be abbreviated with a period.
input: Harry S Truman
output: Truman, Harry S
Chapter 13. Keeping AI Honest with Unit Tests • 262
report erratum  •  discuss



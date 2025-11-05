# 13.8 For Extra Credit (pp.262-263)

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


---
**Page 263**

2.
If a person has a salutation, it should precede the first name in the result.
Known salutations include Dr, Mr, Mrs, Ms, Sir, Miss, Lord, and Esq.
Each salutation may optionally be terminated by a period. Retain the
period if it exists.
input: Dr. Martin Luther King, Jr.
output: King, Jr., Dr. Martin L.
input: Sir Patrick Stewart
output: Stewart, Sir Patrick
If you really want to get wild, a version supporting non-Western names would
no doubt involve numerous additional rules.
Increasing Odds of Success with AI-Generated Code
The most important thing to remember when developing software with an LLM
is you can’t trust the code it generates. The skills you obtained in Pragmatic
Unit Testing in Java with JUnit, however, provide you with a basis for verifying
the code. Consider always following the CAX cycle, as demonstrated in this
chapter, for generating code:
• Create both production code and tests when prompting the LLM, using
(ZOM-inclusive) examples as the basis for the tests.
• Assess the fidelity of the generated tests with the examples you provided.
• e*Xecute the tests. Repeat the cycle (with alterations) if they don’t all pass.
Also, provide a small set of programming style guidelines to your LLM to
improve the solution’s design and potentially increase the likelihood of a
correct solution. Jeff-Java style represents a good starting point.
Will I Go Faster?
AI tools are only now emerging from their infancy, but they show a lot of
promise. As with human toddlers, they thrive when you provide them with
some direction and safeguards, but they can also surprise you with their
cleverness, particularly when you let them explore.
Good design makes so many things easier: writing tests around code, under-
standing code, extending code, and so on. Generating code via an LLM is also
easier when you direct it to follow a small set of guidelines for design that
promote small, focused methods and intention-revealing names.
report erratum  •  discuss
Increasing Odds of Success with AI-Generated Code • 263



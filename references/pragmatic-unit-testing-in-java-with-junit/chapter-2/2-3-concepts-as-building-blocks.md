# 2.3 Concepts as Building Blocks (pp.31-31)

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



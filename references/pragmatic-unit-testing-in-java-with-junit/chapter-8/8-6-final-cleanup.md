# 8.6 Final Cleanup (pp.166-167)

---
**Page 166**

A clean design is your best starting point for optimization.
Note: this probe is intended to be throw-away code. However, you might need
to elevate it to your integration test suite, where it would fail if someone
pushed a solution that violated the execution time threshold. To do so, you’d
add an assertion that the probe finished in under x milliseconds. The challenge
is determining what x should be, given likely varying execution contexts (dif-
fering machines and differing loads, for example). One approach would involve
calculating the threshold dynamically as part of test execution, using a
baseline measurement of a simple, stable operation.
Next up, you’ll change the for-each loops to use the Java streams interface.
This refactoring, afforded by the tests, would allow you to parallelize the
execution of a stream as one way to improve performance.
Final Cleanup
Let’s return to the fun and see how tight you can make the code.
First, replace the old-school loops with Java streams. Start with anyMatches:
utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
private boolean anyMatches(Criteria criteria) {
return criteria.stream()
.anyMatch(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)));
}
To get that compiling and passing, you’ll need to add a stream method to the
Criteria record:
utj3-refactor/13/src/main/java/iloveyouboss/Criteria.java
public Stream<Criterion> stream() {
return criteria.stream();
}
Next, rework the calculateScore method:
utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
private void calculateScore(Criteria criteria) {
score = criteria.stream()
.filter(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)))
.mapToInt(criterion -> criterion.weight().value())
.sum();
}
Chapter 8. Refactoring to Cleaner Code • 166
report erratum  •  discuss


---
**Page 167**

After cleaning up anyRequiredCriteriaNotMet similarly, it’s much simpler to follow
without the (horribly named) kill temporary variable:
utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
return criteria.stream()
.filter(criterion ->
!criterion.isMatch(profileAnswerMatching(criterion)))
.anyMatch(criterion -> criterion.weight() == REQUIRED);
}
You’ve supplanted all three loops. Delete the iterator method in the Criteria
record.
Finally, inline kill in the core matches method:
utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
calculateScore(criteria);
if (anyRequiredCriteriaNotMet(criteria)) return false;
return anyMatches(criteria);
}
You can capture that core four-line policy in a few other ways, but this
approach reads fine.
Summary
It’s easy to write a lot of code quickly. It’s just as easy to let that code get dirty
to the point where it becomes difficult to comprehend and navigate. Unit tests
provide the safeguards you need to clean up messy code without breaking
things.
In this chapter, you learned techniques for keeping your system clean contin-
ually to help you keep your system from degrading into a frustrating mess.
You renamed variables and methods, you extracted smaller methods, you in-
lined variables, and you replaced older Java constructs with newer ones. You
might call this very incremental method-level cleanup “micro” refactoring—a
programmer’s version of the continuous editing that a writer performs.
Don’t let your code get to the point of the convoluted matches methods. Do
recognize that difficult code like matches is rampant in most systems, and it
doesn’t take long for developers to create it.
As you begin to sweep away the small bits of dust in your system, you’ll start
to see larger design concerns—problems related to the overall structure of
the system and how its responsibilities are organized. Next up, you’ll learn
report erratum  •  discuss
Summary • 167



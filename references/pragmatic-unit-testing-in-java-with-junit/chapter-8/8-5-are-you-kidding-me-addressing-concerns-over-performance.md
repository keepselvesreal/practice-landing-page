# 8.5 Are You Kidding Me? Addressing Concerns over Performance (pp.162-166)

---
**Page 162**

utj3-refactor/12/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
calculateScore(criteria);
var kill = anyRequiredCriteriaNotMet(criteria);
➤
if (kill)
return false;
return anyMatches(criteria);
}
private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
➤
var kill = false;
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
}
return kill;
}
Matches is now five lines of code and fairly easy to follow! But some cleanup
work remains, particularly in the three newly extracted methods. For one,
the loops are all old-school for-each loops. You’ll clean up these problems
after we address the performance elephant in the room.
The implementation for matches now involves three loops spread across three
methods instead of a single loop through the criteria. That might seem horri-
fying to you. We’ll come back to discuss the performance implications; for
now, let’s talk about the benefits you gain with the new design.
Earlier, you invested some time in carefully reading the original code in order
to glean its three intents. The Boolean logic throughout created opportunities
for confusion along the way. Now, matches (almost) directly states the method’s
high-level goals.
The implementation details for each of the three steps in the algorithm are
hidden in the corresponding helper methods calculateScore, anyRequiredCriteriaNotMet,
and anyMatches. Each helper method allows the necessary behavior to be
expressed in a concise, isolated fashion, not cluttered with other concerns.
Are You Kidding Me? Addressing Concerns
over Performance
At this point, you might be feeling a little perturbed. After refactoring the
matches method, each of anyMatches, calculateScore, and anyRequiredCriteriaNotMet
Chapter 8. Refactoring to Cleaner Code • 162
report erratum  •  discuss


---
**Page 163**

iterates through the criterion collection. Your code now loops three times instead
of one. You’ve potentially tripled the time to execute matches.
Do you have a real performance problem relevant to the real requirements,
or do you only suspect one exists? Many programmers speculate about where
performance problems might lie and about what the best resolution might
be. Unfortunately, such speculations can be quite wrong.
Base all performance optimization attempts on real data, not
speculation.
The first answer to any potential performance problem is to measure. If under-
standing performance characteristics is a pervasive and critical application
concern, you want to do that analysis from the perspective of end-to-end
functionality—more holistically—rather than at the level of individual unit or
method performance. (You’ll still ultimately be narrowing down to a hopefully
small number of methods that need to be fixed.) For such needs, you’ll want
a tool like JMeter.
1 You can also incorporate JUnitPerf,
2 which allows you to
write performance tests using JUnit.
If you have an occasional concern about the performance of an individual
unit, you can create a few “roll your own” performance probes. As long as
you’re careful with your conclusions, they’ll be adequate for your needs.
The following code runs in the context of a JUnit test (though it has no assertions
and is currently not a test) and displays the number of milliseconds elapsed. The
probe code creates a Criteria object with answers to 20 questions. It then loops a
million times. Each loop creates a new Profile, adds randomized answers to the 20
questions, and then determines whether or not the profile matches the criteria.
utj3-refactor/12/src/test/java/iloveyouboss/AProfilePerformance.java
import org.junit.jupiter.api.Test;
import java.util.List;
import java.util.Random;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Consumer;
import static iloveyouboss.YesNo.*;
import static java.util.stream.IntStream.range;
class AProfilePerformance {
int questionCount = 20;
Random random = new Random();
1.
http://jmeter.apache.org/
2.
https://github.com/noconnor/JUnitPerf
report erratum  •  discuss
Are You Kidding Me? Addressing Concerns over Performance • 163


---
**Page 164**

@Test
void executionTime() {
➤
var questions = createQuestions();
var criteria = new Criteria(createCriteria(questions));
var iterations = 1_000_000;
var matchCount = new AtomicInteger(0);
var elapsedMs = time(iterations, i -> {
var profile = new Profile("");
profile.add(createAnswers(questions));
if (profile.matches(criteria))
matchCount.incrementAndGet();
});
System.out.println("elapsed: " + elapsedMs);
System.out.println("matches: " + matchCount.get());
}
long time(int times, Consumer<Integer> func) {
var start = System.nanoTime();
range(0, times).forEach(i -> func.accept(i + 1));
return (System.nanoTime() - start) / 1_000_000;
}
int numberOfWeights = Weight.values().length;
Weight randomWeight() {
if (isOneInTenTimesRandomly()) return Weight.REQUIRED;
var nonRequiredWeightIndex =
random.nextInt(numberOfWeights - 1) + 1;
return Weight.values()[nonRequiredWeightIndex];
}
private boolean isOneInTenTimesRandomly() {
return random.nextInt(10) == 0;
}
YesNo randomAnswer() {
return random.nextInt() % 2 == 0 ? NO : YES;
}
Answer[] createAnswers(List<Question> questions) {
return range(0, questionCount)
.mapToObj(i -> new Answer(questions.get(i), randomAnswer()))
.toArray(Answer[]::new);
}
List<Question> createQuestions() {
String[] noYes = {NO.toString(), YES.toString()};
return range(0, questionCount)
.mapToObj(i -> new Question("" + i, noYes, i))
.toList();
}
Chapter 8. Refactoring to Cleaner Code • 164
report erratum  •  discuss


---
**Page 165**

List<Criterion> createCriteria(List<Question> questions) {
return range(0, questionCount)
.mapToObj(i -> new Criterion(new Answer(
questions.get(i), randomAnswer()), randomWeight()))
.toList();
}
}
I ran the probe on an old laptop five times to shake out any issues around
timing and the clock cycle. Execution time averaged at 1470ms.
The iterations (1,000,000) and data size (20 questions) are arbitrary choices.
You might choose numbers with some real-world credibility using actual
production characteristics, but that’s not critical. Mostly, you want a sense
of whether or not the degradation is significant enough to be concerned
about.
I also ran the probe against version 8 of the profile, which represents the code
right before you started factoring into multiple loops. Execution time averaged
at 1318ms (with a low standard deviation, under 3 percent).
Execution time for the cleaner design represents an 11.5 percent increase for
the new solution. It’s a sizeable amount, percentage-wise, but it’s not anywhere
near three times worse due to the triple looping. For most people, it’s a non-
issue, but you must decide if the degradation will create a real problem
regarding end-user impact.
Take care when doing this kind of probe. It’s possible to craft a probe that
mischaracterizes reality. For example, Java can, at times, optimize out parts
of the code you’re profiling.
If you process very high volumes, performance may indeed be critical to the
point where the degradation is too much. Ensure you measure after each
optimization attempt and validate whether or not the optimization made
enough of a difference.
Optimized code can easily increase the cost of both understanding and
changing a solution by an order of magnitude. A clean design can reveal intent
in a handful of seconds, as opposed to a minute or more with an optimized
design. Always derive a clean design and then optimize your code only if
necessary.
A clean design can provide more flexibility and opportunities for optimizing
the code. Caching, for example, is a lot easier if the things being cached are
isolated from other bits of code.
report erratum  •  discuss
Are You Kidding Me? Addressing Concerns over Performance • 165


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



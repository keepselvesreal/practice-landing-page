# Refactoring to Cleaner Code (pp.147-169)

---
**Page 147**

CHAPTER 8
Refactoring to Cleaner Code
In Parts I and II, you dug deep into how to write unit tests and take advantage
of JUnit. In this part, you’ll learn to take advantage of unit tests to help shape
the design of your system, as well as document the numerous unit-level
behavioral choices you’ve made. Your ability to keep your system simpler and
your tests clearer can reduce your development costs considerably.
You’ll start by focusing on design “in the small,” addressing the lack of clarity
and excessive complexity that’s commonplace in most systems. You’ll
accomplish this by learning to refactor—making small, frequent edits to the
code you write. Your design improvements will help reduce the cost of change.
In a clear, well-designed system, it might take seconds to locate a point of
change and understand the surrounding code. In a more typically convoluted
system, the navigation and comprehension tasks often require minutes
instead. Once you’ve understood the code well enough to change it, a well-
designed system might accommodate your change readily. In the convoluted
system, weaving in your changes might take hours.
Convoluted systems can increase your maintenance costs by an
order of magnitude or more.
You can, with relative ease, create systems that embody clean code. In brief,
this describes clean code:
• Concise: It imparts the solution without unnecessary code.
• Clear: It can be directly understood.
report erratum  •  discuss


---
**Page 148**

• Cohesive: It groups related concepts together and apart from unrelated
concepts.
• Confirmable: It can be easily verified with tests.
Your unit tests provide you with that last facet of clean code.
A Little Bit o’ Refactor
Refactoring is a fancy way to indicate that you’re transforming the underlying
structure of your code—its implementation details—while retaining its existing
functional behavior. Since refactoring involves reshaping and moving code,
you must ensure your system still works after such manipulations. Unit tests
are the cheapest, fastest way to do so.
Refactoring is to coding as editing is to writing. Even the best (expository)
writers edit most sentences they write to make them immediately clear to
readers. Coding is no different. Once you capture a solution in an editor, your
code is often harder to follow than necessary.
Writers follow the mindset to write first for themselves and then for others.
To do so as a programmer, first, code your solution in a way that makes sense to
you. Then, consider your teammates who must revisit your code at some
point in the future. Rework your code to provide a clearer solution now while
it still makes sense to you.
Code in two steps: first, capture your thoughts in a correct solu-
tion. Second, clarify your solution for others.
Confidence is the key consideration when it comes to refactoring. Without
the confidence that good unit tests provide, you’d want to be extremely cau-
tious about “fixing” code that’s already working. In fact, without unit tests,
you might think, “it ain’t broke. Don’t fix it.” Your code would start its life
unedited—with deficiencies—and would get a little worse with each change.
If you’ve followed the recommendations in this book, however, you can make
changes willy-nilly. Did you think of a new name for a method, one that makes
more sense? Rename it (ten seconds in a good IDE; perhaps minutes other-
wise), run your tests, and know seconds later that nothing broke. Method too
long and hard to follow? Extract a chunk of it to a new method, and run your
tests. Method in the wrong place? Move it, run tests. You can make small
improvements to your codebase all day long, each making it incrementally
easier (cheaper) to work with.
Chapter 8. Refactoring to Cleaner Code • 148
report erratum  •  discuss


---
**Page 149**

An Opportunity for Refactoring
The code you’ll clean up comes from iloveyouboss (albeit a different version
of it). See Exacerbating a Threading Issue, on page 80 for an overview of the
application. Take a look at the Profile class in iloveyouboss:
utj3-refactor/01/src/main/java/iloveyouboss/Profile.java
import java.util.*;
import static iloveyouboss.Weight.*;
public class Profile {
private final Map<String,Answer> answers = new HashMap<>();
private final String name;
private int score;
public Profile(String name) { this.name = name; }
public void add(Answer... newAnswers) {
for (var answer: newAnswers)
answers.put(answer.questionText(), answer);
}
public boolean matches(Criteria criteria) {
score = 0;
var kill = false;
var anyMatches = false;
for (var criterion: criteria) {
var answer = answers.get(criterion.answer().questionText());
var match = criterion.weight() == IRRELEVANT ||
➤
answer.match(criterion.answer());
➤
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
if (match) {
score += criterion.weight().value();
}
anyMatches |= match;
}
if (kill) {
return false;
}
return anyMatches;
}
public int score() { return score; }
@Override
public String toString() { return name; }
}
report erratum  •  discuss
A Little Bit o’ Refactor • 149


---
**Page 150**

This class provides the beginnings of the core matching functionality. A Profile
is comprised of answers to questions that prospective employees might ask
about a company: Do you provide bonuses? Do you hire remote workers? Will
you wash my dog for me? It exposes the core matching functionality through
its matches method. The matches method takes on a Criteria object containing the
preferred answers that a would-be employee has specified.
The matches method isn’t particularly long, weighing in at around a dozen total
lines of expressions and/or statements. Yet it’s reasonably dense, requiring
attentive, stepwise reading. Spend a little time looking at matches to see if you
can pin down what it does.
Testing the class’s behavior sufficiently required seven unit tests:
utj3-refactor/01/src/test/java/iloveyouboss/AProfile.java
import org.junit.jupiter.api.*;
import static iloveyouboss.Weight.*;
import static iloveyouboss.YesNo.*;
import static org.junit.jupiter.api.Assertions.*;
class AProfile {
Profile profile = new Profile("Geeks Inc.");
Criteria criteria;
Question freeLunch;
Answer freeLunchYes;
Answer freeLunchNo;
Question bonus;
Answer bonusYes;
Answer bonusNo;
Question hasGym;
Answer hasGymNo;
Answer hasGymYes;
String[] NO_YES = {NO.toString(), YES.toString()};
@BeforeEach
void createQuestionsAndAnswers() {
bonus = new Question("Bonus?", NO_YES, 1);
bonusYes = new Answer(bonus, YES);
bonusNo = new Answer(bonus, NO);
freeLunch = new Question("Free lunch?", NO_YES, 1);
freeLunchYes = new Answer(freeLunch, YES);
freeLunchNo = new Answer(freeLunch, NO);
hasGym = new Question("Gym?", NO_YES, 1);
hasGymYes = new Answer(hasGym, YES);
hasGymNo = new Answer(hasGym, NO);
}
Chapter 8. Refactoring to Cleaner Code • 150
report erratum  •  discuss


---
**Page 151**

@Nested
class DoesNotMatch {
@Test
void whenAnyRequiredCriteriaNotMet() {
profile.add(freeLunchNo, bonusYes);
criteria = new Criteria(
new Criterion(freeLunchYes, REQUIRED),
new Criterion(bonusYes, IMPORTANT));
var matches = profile.matches(criteria);
assertFalse(matches);
}
@Test
void whenNoneOfMultipleCriteriaMatch() {
profile.add(bonusNo, freeLunchNo);
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT),
new Criterion(freeLunchYes, IMPORTANT));
var matches = profile.matches(criteria);
assertFalse(matches);
}
}
@Nested
class Matches {
@Test
void whenCriteriaIrrelevant() {
profile.add(freeLunchNo);
criteria = new Criteria(
new Criterion(freeLunchYes, IRRELEVANT));
var matches = profile.matches(criteria);
assertTrue(matches);
}
@Test
void whenAnyOfMultipleCriteriaMatch() {
profile.add(bonusYes, freeLunchNo);
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT),
new Criterion(freeLunchYes, IMPORTANT));
var matches = profile.matches(criteria);
assertTrue(matches);
}
}
report erratum  •  discuss
A Little Bit o’ Refactor • 151


---
**Page 152**

@Nested
class Score {
@Test
void isZeroWhenThereAreNoMatches() {
profile.add(bonusNo);
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT));
profile.matches(criteria);
assertEquals(0, profile.score());
}
@Test
void doesNotIncludeUnmetRequiredCriteria() {
profile.add(bonusNo, freeLunchYes);
criteria = new Criteria(
new Criterion(bonusYes, REQUIRED),
new Criterion(freeLunchYes, IMPORTANT));
profile.matches(criteria);
assertEquals(IMPORTANT.value(), profile.score());
}
@Test
void equalsCriterionValueForSingleMatch() {
profile.add(bonusYes);
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT));
profile.matches(criteria);
assertEquals(IMPORTANT.value(), profile.score());
}
@Test
void sumsCriterionValuesForMatches() {
profile.add(bonusYes, freeLunchYes, hasGymNo);
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT),
new Criterion(freeLunchYes, NICE_TO_HAVE),
new Criterion(hasGymYes, VERY_IMPORTANT));
profile.matches(criteria);
assertEquals(IMPORTANT.value() + NICE_TO_HAVE.value(),
profile.score());
}
}
}
The tests’ examples should help you understand the Profile class.
Chapter 8. Refactoring to Cleaner Code • 152
report erratum  •  discuss


---
**Page 153**

Extract Method: Your Second-Best Refactoring Friend
Before this section’s heading sends you digging in the index, your best
refactoring friend is rename, whether it be a class, method, or variable of any
sort. Clarity is largely about declaration of intent, and good names are what
impart clarity best in code.
Your goal: reduce complexity in matches so you can readily understand what
it’s responsible for. The method is currently a jumble of code that obscures
the overall set of steps required—its algorithm or policy. You’ll shift the code
from “implementation detail” to “clear declarations” by extracting detailed bits
of logic to new, separate methods.
Conditional expressions often read poorly, particularly when they are com-
plex. An example is the assignment to match that appears atop the for loop
in matches:
utj3-refactor/01/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
// ...
for (var criterion: criteria) {
var answer = answers.get(criterion.answer().questionText());
var match = criterion.weight() == IRRELEVANT ||
➤
answer.match(criterion.answer());
➤
// ...
}
}
The right-hand side of the assignment seemingly defines when there’s a match.
Specifically, it says there’s a match either when the criterion is irrelevant or
when the criterion’s answer matches the corresponding answer in the profile.
Isolate this complexity by extracting it to a separate method named isMatch.
In IntelliJ IDEA, extract methods by following these mouse-heavy steps:
1.
Highlight the appropriate code.
2.
Open the context menu (via right-click).
3.
Select Refactor ▶ Extract Method from the menu.
4.
Type a name for the new method (or accept the one suggested).
5.
Press Enter.
IntelliJ creates a method containing the highlighted code and then replaces
the highlighted code with a call to the new method.
report erratum  •  discuss
A Little Bit o’ Refactor • 153


---
**Page 154**

After extracting isMatches, you’re left with a simple declaration in matches and
a short helper method in the Profile class:
utj3-refactor/02/src/main/java/iloveyouboss/Profile.java
for (var criterion: criteria) {
var answer = answers.get(criterion.answer().questionText());
var match = isMatch(criterion, answer);
➤
// ...
}
utj3-refactor/02/src/main/java/iloveyouboss/Profile.java
private boolean isMatch(Criterion criterion, Answer answer) {
return criterion.weight() == IRRELEVANT ||
answer.match(criterion.answer());
}
The loop’s code is one step closer to showing only high-level policy and de-
emphasizing lower-level details. The isMatch method provides the specifics
about whether an individual criterion is a match for an answer.
It’s too easy to break behavior when moving code about, sometimes, even
when your IDE moves it for you. After making this change, run all the tests
to ensure they still pass. Good tests provide confidence to make countless
small changes. You’ll know the moment you introduce a sneaky little defect.
With each small change, run your fast set of tests for confidence.
It’s cheap, easy, and gratifying.
The ability to move code about safely is one of the most important benefits
of unit testing. You can add new features safely as well as shape the code
toward a better design. In the absence of sufficient tests, you’ll tend to make
fewer changes or changes that are highly risky.
Finding Better Homes for Your Methods
Your loop is a bit easier to read—great! But code in the newly extracted isMatch
method has nothing to do with the Profile object itself—it interacts with Answer
and Criterion objects. One of those two classes is probably a better place for
the isMatch behavior.
Criterion objects already know about Answer objects, but Answer isn’t dependent
on Criterion. As such, move the newly extracted matches method to the Criterion
record. Moving it to Answer would create a bidirectional dependency with Answer
and Criterion objects depending on each other. Such a tight coupling would
Chapter 8. Refactoring to Cleaner Code • 154
report erratum  •  discuss


---
**Page 155**

mean that changes to either type could propagate to the other, which in turn
could create other problems.
In IntelliJ IDEA, move the method by following these steps:
1.
Click its name.
2.
Open the context menu (via right-click).
3.
Select Refactor ▶ Move Instance Method from the menu.
4.
Select the instance expression Criterion criterion.
5.
Press Enter.
Here’s isMatch in its new home:
utj3-refactor/03/src/main/java/iloveyouboss/Criterion.java
import static iloveyouboss.Weight.IRRELEVANT;
public record Criterion(Answer answer, Weight weight) {
boolean isMatch(Answer answer) {
➤
return weight() == IRRELEVANT || answer.match(answer());
}
}
And here’s what the loop looks like after the move:
utj3-refactor/03/src/main/java/iloveyouboss/Profile.java
for (var criterion: criteria) {
var answer = answers.get(criterion.answer().questionText());
var match = criterion.isMatch(answer);
➤
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
if (match) {
score += criterion.weight().value();
}
anyMatches |= match;
}
The expression assigned to the answer local variable is hard to read because
of the method chaining:
utj3-refactor/03/src/main/java/iloveyouboss/Profile.java
var answer = answers.get(criterion.answer().questionText());
The code asks criterion for its answer object and then asks the answer for its
question text. Better: ask the criterion to directly return the question text. As
the first step toward that goal, extract the expression criterion.answer().questionText()
to a new method named questionText:
utj3-refactor/04/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
// ...
report erratum  •  discuss
Finding Better Homes for Your Methods • 155


---
**Page 156**

for (var criterion: criteria) {
var answer = answers.get(questionText(criterion));
➤
// ...
}
// ...
}
private String questionText(Criterion criterion) {
➤
return criterion.answer().questionText();
}
Now move questionText to the Criterion class. If you move it via IDEA’s automated
refactoring support, select Criterion criterion as the instance expression.
The method disappears from Profile. The expression assigned to the answer local
variable no longer involves method chaining:
utj3-refactor/05/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
// ...
for (var criterion: criteria) {
var answer = answers.get(criterion.questionText());
➤
// ...
}
// ...
}
Criterion is now responsible for retrieving and returning the question text:
utj3-refactor/05/src/main/java/iloveyouboss/Criterion.java
import static iloveyouboss.Weight.IRRELEVANT;
public record Criterion(Answer answer, Weight weight) {
// ...
String questionText() {
return answer().questionText();
}
}
Next, extract the whole right-hand side of the answer assignment to a method
that helps explain what the answer represents:
utj3-refactor/06/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
// ...
for (var criterion: criteria) {
var answer = profileAnswerMatching(criterion);
➤
var match = criterion.isMatch(answer);
// ...
}
// ...
}
Chapter 8. Refactoring to Cleaner Code • 156
report erratum  •  discuss


---
**Page 157**

private Answer profileAnswerMatching(Criterion criterion) {
➤
return answers.get(criterion.questionText());
}
Each extract method you do increases the conciseness of matches bit by bit.
Using intention-revealing names for the new methods also increases the
clarity of matches. The new methods also represent opportunities to move
responsibilities to where they belong. Profile gets simpler while the previously
barren Criterion builds up its usefulness.
Removing Temporaries of Little Value
Temporary variables (“temps”) have a number of uses. They can cache the
value of an expensive computation or collect things that change throughout
the body of a method. A temp can also clarify the intent of code—a valid choice
even if it’s used only once.
In matches, the answer local variable provides none of those three benefits. You
can inline such a pointless variable by replacing any occurrences of it with
the answerMatching(criterion) expression. In IntelliJ IDEA, inline a variable by fol-
lowing these steps:
1.
Click its name.
2.
Open the context menu (via right-click).
3.
Select Refactor ▶ Inline Variable from the menu.
Any references to the variable are replaced with the right-hand side of the
assignment. The assignment statement disappears:
utj3-refactor/07/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
// ...
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
➤
// ...
}
// ...
}
The true intent for match can be understood directly. Paraphrasing: a match
exists when the criterion is a match for the corresponding profile answer.
Speeding Up with Automated Refactoring
You can, of course, do this or any other refactoring manually, cutting and
pasting little bits of code until you reach the same outcome. But once you’ve
report erratum  •  discuss
Removing Temporaries of Little Value • 157


---
**Page 158**

learned that a good IDE can do the job at least ten times as fast, it makes
little sense not to take advantage of that power.
More importantly, you can trust that (in Java, at least) an automated refac-
toring generally will not break code. You’re far more likely to mess up along
the way through a manual refactoring. Java automated refactorings are code
transformations that have been proven in all senses of the word.
You can further speed up by using the keyboard shortcuts for each automated
refactoring rather than click through menus and dialogs. Throughout your
development day, you’ll find heavy use for a small number of core automated
refactorings: introduce variable/constant/field/parameter, extract method,
inline method, inline variable, move method, and change signature. It won’t
take long to ingrain the corresponding shortcuts. You can reduce most
refactoring operations to about three to four seconds from 10 seconds or more
(clicking through the UI) or from several minutes (manually).
Lucky you: 20 years ago, most Java programmers manually moved code about
in highly unsafe ways. Thirty years ago, automated refactoring tools didn’t
exist. Today, the power and speed they grant can’t be overstated. You can
watch the computer do the dirty work and know that your code still works.
Amplifying the Core Intent of Code
Let’s re-examine the slightly improved matches method:
utj3-refactor/07/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = 0;
var kill = false;
var anyMatches = false;
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
if (match) {
score += criterion.weight().value();
}
anyMatches |= match;
}
if (kill)
return false;
return anyMatches;
}
Chapter 8. Refactoring to Cleaner Code • 158
report erratum  •  discuss


---
**Page 159**

Careful reading reveals the following outcomes:
• Return true if any criterion matches, false if none do.
• Calculate the score by summing the weights of matching criteria.
• Return false when any required criterion does not match the corresponding
profile answer.
Let’s restructure matches to directly emphasize these three core concepts.
Extract Concept: Any Matches Exist?
The determination of whether any matches exist is scattered through the
method. It involves both the anyMatches and matches local variables:
utj3-refactor/08/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = 0;
var kill = false;
var anyMatches = false;
➤
for (var criterion: criteria) {
➤
var match = criterion.isMatch(profileAnswerMatching(criterion));
➤
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
if (match) {
score += criterion.weight().value();
}
anyMatches |= match;
➤
}
if (kill)
return false;
return anyMatches;
➤
}
Your goal: move all the logic related to making that determination to its own
method. Here are the steps:
1.
Change the return statement to return the result of calling a new method,
anyMatches().
2.
Create a new method, anyMatches, that returns a Boolean value.
3.
Copy (don’t cut) the relevant logic into the new method.
The result:
utj3-refactor/09/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = 0;
report erratum  •  discuss
Amplifying the Core Intent of Code • 159


---
**Page 160**

var kill = false;
var anyMatches = false;
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
if (match) {
score += criterion.weight().value();
}
anyMatches |= match;
}
if (kill)
return false;
return anyMatches(criteria);
➤
}
private boolean anyMatches(Criteria criteria) {
➤
var anyMatches = false;
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
anyMatches |= match;
}
return anyMatches;
}
There’s no automated refactoring for this change. You’re making riskier
manual changes, so run your tests! Once they pass, remove the two lines of
code in matches that reference the anyMatches variable:
utj3-refactor/10/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = 0;
var kill = false;
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
if (match) {
score += criterion.weight().value();
}
}
if (kill)
return false;
return anyMatches(criteria);
}
Chapter 8. Refactoring to Cleaner Code • 160
report erratum  •  discuss


---
**Page 161**

The loop, of course, must remain and so must the line of code that assigns
to the match variable.
You might be concerned about that method extraction and its performance
implications. We’ll discuss.
Extract Concept: Calculate Score for Matches
Now that you’ve isolated the anyMatches logic by extracting it to a new method,
you can do the same for the code that calculates the score. If you put the call
to calculateScore below if (kill) return false, however, the tests break. (The score
needs to be calculated before any unmet required criterion results in an
aborted method.)
utj3-refactor/11/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
calculateScore(criteria);
➤
var kill = false;
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
if (!match && criterion.weight() == REQUIRED) {
kill = true;
}
}
if (kill)
return false;
return anyMatches(criteria);
}
private void calculateScore(Criteria criteria) {
➤
score = 0;
for (var criterion: criteria) {
var match = criterion.isMatch(profileAnswerMatching(criterion));
if (match) {
score += criterion.weight().value();
}
}
}
Hmmm. You might be wondering if you’re creating performance problems.
Extract Concept: Return False When Required Criterion Not Met
The code remaining in the loop aborts method execution if the profile doesn’t
match a required criterion, returning false. Similarly, extract this logic to a
new method, anyRequiredCriteriaNotMet:
report erratum  •  discuss
Amplifying the Core Intent of Code • 161


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


---
**Page 168**

how to lean on unit tests again to address these larger design concerns
through “macro” refactoring.
Right now, the code you refactored in matches clearly states what’s going on.
But it also poses some concerns about the bigger design picture. The Profile
class, for example, might be doing too much.
In the next chapter, you’ll explore where your design falls flat. You’ll take
advantage of your tests to support getting things back on track.
Chapter 8. Refactoring to Cleaner Code • 168
report erratum  •  discuss


---
**Page 169**

CHAPTER 9
Refactoring Your Code’s Structure
In the last chapter, you focused on refactoring the matches method into a
number of more composed methods. You also focused on the clarity and
conciseness of each method. This continual editing of small bits of code is a
fundamental piece of design—you are making choices about how to implement
a solution in a manner that keeps code comprehension and maintenance
costs low.
These are examples of “micro” design concerns:
• How you capture state in fields
• How you organize code into methods
• How those methods interact with each other
• How those methods interact with the external world
To many developers, a software system’s design is mostly a “macro” concern:
• How you organize classes into packages
• How you organize methods into classes
• How those classes interact with each other
Both sets of concerns are relevant to the long-term maintainability of a system.
One or both can be impacted any time you make a decision about how to
organize and implement your code.
A software system’s design is the combined collection of choices made at both
macro and micro levels.
You might be thinking, “This is a unit testing book. Why is this guy talking
about design so much?”
It turns out that writing unit tests isn’t an exercise that occurs in a vacuum.
Your system’s design impacts your ability to write tests and vice versa. You
might even consider the tests themselves a piece of the larger, continually
report erratum  •  discuss



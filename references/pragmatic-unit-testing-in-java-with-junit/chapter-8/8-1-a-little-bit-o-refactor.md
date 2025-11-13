# 8.1 A Little Bit o’ Refactor (pp.148-154)

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



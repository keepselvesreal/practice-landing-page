# 9.4 The Costs of Maintaining Unit Tests (pp.182-187)

---
**Page 182**

As a result of the change to Profile, three tests in AProfile no longer compile.
Calls to the score method on a Profile instance now require a criteria object as
an argument. Here’s an example of one fixed test showing the changed
assertion statement:
utj3-refactor/22/src/test/java/iloveyouboss/AProfile.java
@Test
void isZeroWhenThereAreNoMatches() {
profile.add(bonusNo);
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT));
var score = profile.score(criteria);
➤
assertEquals(0, score);
➤
}
The Costs of Maintaining Unit Tests
Refactoring—changing the implementation of a solution without changing
its behavior—should not normally break tests. Here, however, you did make
a behavioral change due to a deficiency in the Profile interface. Your updated
design now exposes the score method’s behavior in a different manner than
before, hence the broken tests. You might consider that your refactoring
“pushed out a change to the interface.”
Sure, you must spend time to fix the tests. In this case, having tests in the
first place enabled you to recognize and fix a faulty design.
You’ve learned throughout this book the potential benefits of unit tests:
• Releasing fewer defects
• Changing your code at will with high confidence
• Knowing exactly and rapidly what behaviors the system embodies
This book can help you attain those benefits and increase your ROI.
The return on investment from well-designed tests outweighs
their cost.
Moving forward, when your tests break as you refactor, think about it as a
design smell. The more tests that break simultaneously, the bigger the chance
you missed an opportunity to improve the design, whether of the tests or
production code.
Chapter 9. Refactoring Your Code’s Structure • 182
report erratum  •  discuss


---
**Page 183**

Refocusing Tests
After moving behavior from Profile to Matcher, the tests in AProfile now have nothing
to do with Profile. You’ll want to move the tests to a new class—AMatcher—and
then adapt them to interact with Matcher, not Profile.
Currently, Matcher’s constructor requires a Map<String,Answer> (where the String
key represents a question’s text) as its second parameter. The tests in AProfile
involve adding a list of Answer objects to a profile, however:
utj3-refactor/21/src/test/java/iloveyouboss/AProfile.java
@Test
void whenNoneOfMultipleCriteriaMatch() {
profile.add(bonusNo, freeLunchNo);
➤
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT),
new Criterion(freeLunchYes, IMPORTANT));
var matches = profile.matches(criteria);
assertFalse(matches);
}
It’d be nice to only have to minimally change the tests. Right now, however,
they’d need to convert each list of answers into a Map<String,Answer> before
constructing the Matcher.
Instead, think about the most concise way to express your tests. Here’s what
you’d like Matcher’s tests to look like—very similar to the tests in AProfile:
utj3-refactor/22/src/test/java/iloveyouboss/AMatcher.java
@Test
void whenNoneOfMultipleCriteriaMatch() {
criteria = new Criteria(
new Criterion(bonusYes, IMPORTANT),
new Criterion(freeLunchYes, IMPORTANT));
matcher = new Matcher(criteria, bonusNo, freeLunchNo);
➤
var matches = matcher.matches();
➤
assertFalse(matches);
}
Note that the test necessarily creates a matcher object after the criteria. Also,
the call to matches no longer requires any arguments.
The test assumes it can create a Matcher object using the same list of answers
added to a profile by tests in AProfile. Make that happen by adding a constructor
and helper method to Matcher, letting it do the dirty work:
report erratum  •  discuss
The Costs of Maintaining Unit Tests • 183


---
**Page 184**

utj3-refactor/22/src/main/java/iloveyouboss/Matcher.java
public Matcher(Criteria criteria, Answer... matcherAnswers) {
this.criteria = criteria;
this.answers = toMap(matcherAnswers);
}
private Map<String, Answer> toMap(Answer[] answers) {
return Stream.of(answers).collect(
Collectors.toMap(Answer::questionText, answer -> answer));
}
Getting all of the tests to that adapted shape is maybe 15-20 minutes of work.
You’ll need to:
• Declare a Matcher field named matcher.
• Eliminate the profile field.
• For each test:
– Assign a new Matcher instance to matcher. Create it using the test’s cri-
teria plus the list of answers previously provided to the profile’s add
method. Ensure this assignment statement appears after the line that
creates the Criteria.
– Remove the statement that adds answers to the profile (for example,
profile.add(freeLunch, bonusYes);).
If you get stuck—or just want to give up—go ahead and copy in the code from
the distribution for this book.
You can now revisit and clean up the tests in AProfile.
Revisiting the Profile Class: Delegation Tests
Someone created nice, exhaustive tests for the Profile class. (Hey…that was
me. You’re welcome.) But you copied them over to AMatcher, without really
changing the essence of the logic they verify. You also removed all that
interesting logic from Profile.
The Profile class still contains three methods with logic. Out of these, the
matches and score methods do nothing but delegate to Matcher. Still, you should
feel compelled to provide tests for these methods. They’ll probably never break,
but would at least help describe what’s going on.
Were you to test the score and matches methods, you’d have at least a couple
of options. You could introduce mock objects (see Chapter 3, Using Test
Doubles, on page 53) to verify that the work was delegated to the Matcher in
each case. You could also choose a simple, representative case involving the
scoring and matching. Both have their merits and demerits.
Chapter 9. Refactoring Your Code’s Structure • 184
report erratum  •  discuss


---
**Page 185**

Would, should, could. Maybe you’re sensing I’m not going to have you write
tests for these methods. You’ll instead push out the work of interacting with
the Matcher directly to the client of Profile—a service class, perhaps—as a sim-
plifying design choice. The service class can handle the coordination between
the profile, matcher, and criteria. That code might look like this:
utj3-refactor/23/src/main/java/iloveyouboss/MatcherService.java
public class MatcherService {
public boolean matches(int profileId, int criteriaId) {
var profile = profileData.retrieve(profileId);
var criteria = criteriaData.retrieve(criteriaId);
return new Matcher(criteria, profile.answers()).matches();
}
public int score(int profileId, int criteriaId) {
var profile = profileData.retrieve(profileId);
var criteria = criteriaData.retrieve(criteriaId);
return new Matcher(criteria, profile.answers()).score();
}
// ...
}
You’ll want to (and have to) make a few more changes, but everything is now
a little simpler in the other three classes impacted.
After pushing out the matches and score methods, the only logic remaining in
the Profile class appears in its add(Answer) method. Since no code in Profile cares
about the answers, you can simplify the class to store a list of Answer objects
rather than create a Map. Here’s the cleaned-up version of Profile:
utj3-refactor/23/src/main/java/iloveyouboss/Profile.java
import java.util.ArrayList;
import java.util.List;
public class Profile {
private final List<Answer> answers = new ArrayList<>();
private final String name;
public Profile(String name) {
this.name = name;
}
public void add(Answer... newAnswers) {
for (var answer: newAnswers)
answers.add(answer);
}
public List<Answer> answers() {
return answers;
}
report erratum  •  discuss
The Costs of Maintaining Unit Tests • 185


---
**Page 186**

public String name() {
return name;
}
}
And here’s a simple test to add:
utj3-refactor/23/src/test/java/iloveyouboss/AProfile.java
import org.junit.jupiter.api.Test;
import java.util.List;
import static org.junit.jupiter.api.Assertions.assertEquals;
class AProfile {
Question question = new Question("?", new String[] {"Y","N"}, 1);
Profile profile = new Profile("x");
@Test
void supportsAddingIndividualAnswers() {
var answer = new Answer(question, "Y");
profile.add(answer);
assertEquals(List.of(answer), profile.answers());
}
}
Your changes impact the constructors in Matcher again. While updating the
class, you can also change Matcher to be a Java record instead of a class. Here’s
the final code (minus imports):
utj3-refactor/23/src/main/java/iloveyouboss/Matcher.java
public record Matcher(Criteria criteria, Map<String, Answer> answers) {
public Matcher(Criteria criteria, List<Answer> matcherAnswers) {
this(criteria, asMap(matcherAnswers));
}
public Matcher(Criteria criteria, Answer... matcherAnswers) {
this(criteria, asList(matcherAnswers));
}
private static Map<String, Answer> asMap(List<Answer> answers) {
return answers.stream().collect(
Collectors.toMap(Answer::questionText, answer -> answer));
}
public boolean matches() {
return allRequiredCriteriaMet() && anyMatches();
}
private boolean allRequiredCriteriaMet() {
return criteria.stream()
.filter(criterion -> criterion.weight() == REQUIRED)
.allMatch(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)));
}
Chapter 9. Refactoring Your Code’s Structure • 186
report erratum  •  discuss


---
**Page 187**

private boolean anyMatches() {
return criteria.stream()
.anyMatch(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)));
}
private Answer profileAnswerMatching(Criterion criterion) {
return answers.get(criterion.questionText());
}
public int score() {
return criteria.stream()
.filter(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)))
.mapToInt(criterion -> criterion.weight().value())
.sum();
}
}
Left to you, dear reader: combining both matching logic and scoring logic in
Matcher decreases cohesion. Your mission: split off the scoring logic into a new
class, Scorer. It should take at most 15 minutes. Don’t forget to split off the
tests!
Summary
In this chapter, you improved the design of iloveyouboss, leaning mostly on
a couple of simple design concepts for guidance: the SRP and command-query
separation. You owe it to yourself to know as much as possible about these
and other concepts in design. (Take a look at Clean Code [Mar08], for example,
but keep reading.) And don’t forget what you learned in Chapter 8, Refactoring
to Cleaner Code, on page 147: small, continual code edits make a big difference.
Armed with a stockpile of design smarts, your unit tests will allow you to
reshape your system so that it more easily supports the inevitable changes
coming.
Your system’s design quality also inversely correlates to your pain and frus-
tration level. The worse your design, the longer it will take to understand the
code and make changes. Keeping the design incrementally clean will keep
costs to a small fraction of what they’ll become otherwise.
Be flexible. Be willing to create new, smaller classes and methods. Automated
refactoring tools make doing so easy. Even without such tools, it takes only
minutes. It’s worth the modest effort. Design flexibility starts with smaller,
more composed building blocks.
report erratum  •  discuss
Summary • 187



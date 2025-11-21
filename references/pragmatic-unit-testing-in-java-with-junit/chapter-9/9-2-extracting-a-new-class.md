# 9.2 Extracting a New Class (pp.173-180)

---
**Page 173**

each other, with other considerations (like performance), and with other cir-
cumstances or constraints of your reality.
Extracting a New Class
The Profile class defines two responsibilities:
• Track information about a profile.
• Determine whether and to what extent a set of criteria matches a profile.
To improve your system’s design, you’ll split responsibilities into two classes,
each small and adherent to the SRP. To do so, you’ll extract the code related
to the profile-matching behavior to another class, Matcher. As with all refactor-
ing, you’ll take an incremental path—make a small change and then run the
tests to make sure they still pass.
For your first change, move the calculateScore logic into Matcher. Start by changing
the code in matches to declare your intent: rather than call calculateScore directly
from matches, construct a new Matcher object with the information it needs—the
hash map of answers and the criteria—and ask it for the score. Assign that
returned score to the score field:
utj3-refactor/14/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = new Matcher(criteria, answers).score();
➤
if (anyRequiredCriteriaNotMet(criteria)) return false;
return anyMatches(criteria);
}
Copy (don’t cut it just yet) the calculateScore method from Profile into Matcher. In
the constructor of Matcher, first, store the answers argument in a field. Then,
call the calculateStore method, passing it the Criteria object that was passed to
the constructor.
Add a score field and a score() accessor method to return it.
Compilation at this point reveals that calculateScore() needs to call profileAnswer-
Matching(). Copy over that method.
Your Matcher class should now look like the following:
utj3-refactor/14/src/main/java/iloveyouboss/Matcher.java
import java.util.Map;
public class Matcher {
private final Map<String, Answer> answers;
private int score;
report erratum  •  discuss
Extracting a New Class • 173


---
**Page 174**

public Matcher(Criteria criteria, Map<String, Answer> answers) {
this.answers = answers;
calculateScore(criteria);
}
private void calculateScore(Criteria criteria) {
score = criteria.stream()
.filter(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)))
.mapToInt(criterion -> criterion.weight().value())
.sum();
}
private Answer profileAnswerMatching(Criterion criterion) {
return answers.get(criterion.questionText());
}
public int score() {
return score;
}
}
Both Profile and Matcher now compile. Your tests should run successfully.
The code in Profile no longer uses the calculateScore private method. Delete it. The
profileAnswerMatching method is still used by code in Profile. Indicate that it’s
duplicated elsewhere with a comment. If profileAnswerMatching is still needed by
both classes after you finish moving code about, you’ll want to factor that
code to a single place.
Moving Matches Functionality to Matcher
You’ve delegated the scoring responsibility to Matcher and invoked it from
matches. The other code in matches represents the second goal of the method—to
answer true or false depending on whether the criteria match the set of answers.
Matcher represents a more appropriate home for that matches logic. Let’s simi-
larly delegate the matching responsibility to the Matcher class.
You can tackle this refactoring in many ways. Let’s take one small step at a
time.
utj3-refactor/15/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = new Matcher(criteria, answers).score();
if (anyRequiredCriteriaNotMet(criteria)) return false;
➤
➤
return anyMatches(criteria);
➤
}
Chapter 9. Refactoring Your Code’s Structure • 174
report erratum  •  discuss


---
**Page 175**

Extract the two highlighted lines to a method with a name other than matches,
which is already used. How about isMatchFor?
utj3-refactor/16/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = new Matcher(criteria, answers).score();
return isMatchFor(criteria);
➤
}
private boolean isMatchFor(Criteria criteria) {
➤
if (anyRequiredCriteriaNotMet(criteria)) return false;
return anyMatches(criteria);
}
Move isMatchFor to Matcher. Your IDE should let you know that the two methods
called by isMatchFor—anyRequiredCriteriaNotMet and anyMatches—must come along
for the ride. Move them too.
Here is isMatchFor in its new home, along with the related methods:
utj3-refactor/17/src/main/java/iloveyouboss/Matcher.java
public class Matcher {
// ...
public boolean isMatchFor(Criteria criteria) {
➤
if (anyRequiredCriteriaNotMet(criteria))
return false;
return anyMatches(criteria);
}
private boolean anyMatches(Criteria criteria) {
➤
return criteria.stream()
.anyMatch(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)));
}
private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
➤
return criteria.stream()
.filter(criterion ->
!criterion.isMatch(profileAnswerMatching(criterion)))
.anyMatch(criterion -> criterion.weight() == REQUIRED);
}
Answer profileAnswerMatching(Criterion criterion) {
return answers.get(criterion.questionText());
}
// ...
}
report erratum  •  discuss
Extracting a New Class • 175


---
**Page 176**

The matches method in Profile should be down to two statements:
utj3-refactor/17/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
score = new Matcher(criteria, answers).score();
return new Matcher(criteria, answers).isMatchFor(criteria);
}
Tests still pass? Good. Extract the common initialization of Matcher in matches
to a local variable:
utj3-refactor/18/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
var matcher = new Matcher(criteria, answers);
score = matcher.score();
return matcher.isMatchFor(criteria);
}
Moving all the matching logic into Matcher trims the Profile class nicely:
utj3-refactor/18/src/main/java/iloveyouboss/Profile.java
import java.util.HashMap;
import java.util.Map;
public class Profile {
private final Map<String,Answer> answers = new HashMap<>();
private final String name;
private int score;
public Profile(String name) {
this.name = name;
}
public void add(Answer... newAnswers) {
for (var answer: newAnswers)
answers.put(answer.questionText(), answer);
}
public boolean matches(Criteria criteria) {
var matcher = new Matcher(criteria, answers);
score = matcher.score();
return matcher.isMatchFor(criteria);
}
public int score() {
return score;
}
@Override
public String toString() {
return name;
}
}
Chapter 9. Refactoring Your Code’s Structure • 176
report erratum  •  discuss


---
**Page 177**

The Profile class now appears to adhere to the SRP. Its methods are all small
and straightforward—you can gather a sense of everything that’s going on in
each of them at a glance.
Profile is also fairly cohesive: changes to matching or scoring logic will be made
in Matcher. Changes to the Profile class itself (for example, it needs to store
additional attributes) will not be triggered by changes to matching/scoring
logic and will unlikely require changes to Matcher.
Cleaning Up After a Move
Shift your focus back to Matcher, into which you moved a bunch of methods.
Any time you move a method, you’ll want to determine if opportunities exist
for improving the code in its new home.
The moved anyRequiredCriteriaNotMet and anyMatches methods both require access
to the criteria instance. Alter the constructor in Matcher to store criteria as a new
field. Once criteria is available as a field, there’s no reason to pass criteria around
to the calculateScore, anyRequiredCriteriaNotMet, and anyMatches methods.
The removal of the criteria argument from the matches method requires you to
change the calling code in Profile. After you make that change, note that without
the criteria argument, return matcher.isMatchFor() reads poorly. Rename the isMatchFor
method back to matches:
utj3-refactor/19/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
var matcher = new Matcher(criteria, answers);
score = matcher.score();
return matcher.matches();
➤
}
Here’s the cleaned-up Matcher class:
utj3-refactor/19/src/main/java/iloveyouboss/Matcher.java
public class Matcher {
private final Criteria criteria;
➤
private final Map<String, Answer> answers;
private int score;
public Matcher(Criteria criteria, Map<String, Answer> answers) {
this.criteria = criteria;
this.answers = answers;
➤
calculateScore();
➤
}
report erratum  •  discuss
Extracting a New Class • 177


---
**Page 178**

private void calculateScore() {
➤
score = criteria.stream()
.filter(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)))
.mapToInt(criterion -> criterion.weight().value())
.sum();
}
public boolean matches() {
if (anyRequiredCriteriaNotMet()) return false;
➤
return anyMatches();
➤
}
private boolean anyMatches() {
➤
return criteria.stream()
.anyMatch(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)));
}
private boolean anyRequiredCriteriaNotMet() {
➤
return criteria.stream()
.filter(criterion ->
!criterion.isMatch(profileAnswerMatching(criterion)))
.anyMatch(criterion -> criterion.weight() == REQUIRED);
}
private Answer profileAnswerMatching(Criterion criterion) {
return answers.get(criterion.questionText());
}
public int score() {
return score;
}
}
A couple more tasks and then you can consider the class sufficiently cleaned
up…for now. You can improve the matches method in Matcher, and you can
tighten up the scoring logic.
First, the matches method in Matcher requires three lines to express what could
be phrased as a single complex conditional:
utj3-refactor/19/src/main/java/iloveyouboss/Matcher.java
public boolean matches() {
if (anyRequiredCriteriaNotMet()) return false;
➤
return anyMatches();
➤
}
As short as this method is, it remains stepwise rather than declarative. It
requires readers to think about how to piece together three elements.
Chapter 9. Refactoring Your Code’s Structure • 178
report erratum  •  discuss


---
**Page 179**

Combine these separate conditionals into a single expression. Invert the result
of anyRequiredCriteriaNotMet and combine it with the result of anyMatches using the
and (&&) operator:
utj3-refactor/20/src/main/java/iloveyouboss/Matcher.java
public boolean matches() {
return !anyRequiredCriteriaNotMet() && anyMatches();
}
But double-negatives read poorly. (Boolean logic, in general, is tough for many
of us; you want to avoid making things worse.) Eliminate the double-negative
by doing the following:
1.
Flip the logic in anyRequiredCriteriaNotMet to return true if all required criteria
are met.
2.
Invert the name of anyRequiredCriteriaNotMet to allRequiredCriteriaMet.
3.
Remove the not (!) operator.
utj3-refactor/21/src/main/java/iloveyouboss/Matcher.java
public boolean matches() {
return allRequiredCriteriaMet() && anyMatches();
➤
}
private boolean allRequiredCriteriaMet() {
return criteria.stream()
.filter(criterion -> criterion.weight() == REQUIRED)
➤
.allMatch(criterion ->
➤
criterion.isMatch(profileAnswerMatching(criterion)));
➤
}
That should make a lot more immediate sense to virtually all readers of the
code. You might also change the order of the expression to first ask if there
are any matches and then ensure that all required criteria are met—it logically
flows a little better.
For your second final bit of cleanup, the scoring logic is unnecessarily split
across the class. Move the calculateScore logic into the score accessor and then
remove calculateScore and the now-unused score field. Your change also carries the
benefit of not incurring the score calculation cost if it is not used by the client.
utj3-refactor/21/src/main/java/iloveyouboss/Matcher.java
public int score() {
return criteria.stream()
.filter(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)))
.mapToInt(criterion -> criterion.weight().value())
.sum();
}
report erratum  •  discuss
Extracting a New Class • 179


---
**Page 180**

When you first learned about object-oriented design, you might have picked
up a recommendation to design your classes like “the real world.” It’s an okay
starting point, particularly for folks new to OO design, but don’t take it too
far. Dogmatically “real-world” designs may seem appealing, but they create
systems that are more difficult to maintain.
The Profile class could be construed as a “real-world” entity. A simplistic real-
world implementation would result in the Profile class containing all the logic
related to matching on criteria. The version of Profile that you saw at the start
of the refactoring exercises is such a real-world implementation. A system
full of such larger, overly responsible classes will be hard to understand and
change. It will provide virtually no opportunities for re-use and contain con-
siderable duplication,
Create classes that map to concepts, not concrete notions. The Matcher concept
allows you to isolate the code related to matching, which keeps its code sim-
pler. The Profile code from which it came gets simpler as well.
Every code change you make alters the design of a system. Some of those
changes can have negative impacts on behavior elsewhere in the system. So
far, in this chapter, you’ve focused on such macro design considerations.
As you start to correct design flaws, whether micro or macro, you’ll more readily
spot additional problems. For example, sometimes extracting a small amount
of code to a new method will highlight a glaringly obvious deficiency—one
that was not so obvious when surrounded by a lot of other code.
The methods in Profile are now all very small, and one of them indeed exposes
a design flaw. Let’s return to the micro design space and discuss the concept
of command-query separation.
Command-Query Separation
The only remaining oddity in Profile is how it handles scoring logic. Examine
its matches method:
utj3-refactor/21/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
var matcher = new Matcher(criteria, answers);
score = matcher.score();
return matcher.matches();
}
As a side effect, Profile stores a score. But a profile doesn’t have a single fixed
score. It only references a calculated score that’s associated with an attempt
to match on criteria.
Chapter 9. Refactoring Your Code’s Structure • 180
report erratum  •  discuss



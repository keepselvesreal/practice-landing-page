# Refactoring Your Code’s Structure (pp.169-189)

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


---
**Page 170**

shifting puzzle we call design. They provide confidence that your system’s
design exhibits the most important aspect of design—that it supports a correct
solution, working as intended.
The most important aspect of a system’s design is that it works
as intended.
In this chapter, you’ll focus on bigger design concerns:
• The Single Responsibility Principle (SRP) guides you to small classes that
do one core thing to increase flexibility and ease of testing, among other
things.
• The command-query separation (CQS) principle says to design methods
that do one of creating a side effect or returning a value but never both
• Refactoring the production code toward a better design. When refactoring,
change one of either production code or tests at a time and never both.
Perhaps you noticed a focus on the notion of “one” in that list. It’s not a
coincidence; it’s a core mentality in incremental software development.
One Thing At A Time (OTAAT).
You’ll apply these principles by refactoring code in the Profile class.
The Profile Class and the SRP
Take a look at the Profile class:
utj3-refactor/13/src/main/java/iloveyouboss/Profile.java
import java.util.HashMap;
import java.util.Map;
import static iloveyouboss.Weight.REQUIRED;
public class Profile {
private final Map<String,Answer> answers = new HashMap<>();
private final String name;
private int score;
public Profile(String name) { this.name = name; }
public void add(Answer... newAnswers) {
for (var answer: newAnswers)
answers.put(answer.questionText(), answer);
}
Chapter 9. Refactoring Your Code’s Structure • 170
report erratum  •  discuss


---
**Page 171**

public boolean matches(Criteria criteria) {
calculateScore(criteria);
if (anyRequiredCriteriaNotMet(criteria)) return false;
return anyMatches(criteria);
}
private boolean anyRequiredCriteriaNotMet(Criteria criteria) {
return criteria.stream()
.filter(criterion ->
!criterion.isMatch(profileAnswerMatching(criterion)))
.anyMatch(criterion -> criterion.weight() == REQUIRED);
}
private void calculateScore(Criteria criteria) {
score = criteria.stream()
.filter(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)))
.mapToInt(criterion -> criterion.weight().value())
.sum();
}
private boolean anyMatches(Criteria criteria) {
return criteria.stream()
.anyMatch(criterion ->
criterion.isMatch(profileAnswerMatching(criterion)));
}
private Answer profileAnswerMatching(Criterion criterion) {
return answers.get(criterion.questionText());
}
public int score() { return score; }
@Override
public String toString() { return name; }
}
At under seventy source lines, Profile doesn’t seem inordinately large or
excessively complex. But it hints at less-than-ideal design.
Profile tracks and manages information for a company or person, including a
name and a collection of answers to questions. This set of information that
Profile captures will need to change over time—more information will need to
be added, and some might need to be removed or altered.
As a secondary responsibility, Profile calculates a score to indicate if—and to
what extent—a set of criteria matches the profile. With the refactoring you
accomplished in the previous chapter, you ended up with a number of
methods that directly support the matches method. Changes to the Profile class
report erratum  •  discuss
The Profile Class and the SRP • 171


---
**Page 172**

are thus probable for a second reason: you’ll undoubtedly change the
sophistication of your matching algorithm over time.
The Profile class violates the Single Responsibility Principle (SRP) of object-
oriented class design, which says classes should have only one reason to change.
(The SRP is one of a set of class design principles—see the following sidebar.)
Focusing on the SRP decreases the risk of change. The more responsibilities a
class has, the easier it is to break other existing behaviors when changing code
within the class.
SOLID Class-Design Principles
In the mid-1990s, Robert C. Martin gathered five principles for object-oriented class
design, presenting them as the best guidelines for building a maintainable object-
oriented system. Michael Feathers attached the acronym SOLID to these principles
in the early 2000s.a
• Single Responsibility Principle (SRP). Classes should have one reason to change.
Keep your classes small and single-purposed.
• Open-Closed Principle (OCP). Design classes to be open for extension but closed
for modification. Minimize the need to make changes to existing classes.
• Liskov Substitution Principle (LSP). Subtypes should be substitutable for their
base types. Method overrides shouldn’t break a client’s expectations for behavior.
• Interface Segregation Principle (ISP). Clients shouldn’t have to depend on methods
they don’t use. Split a larger interface into a number of smaller interfaces.
• Dependency Inversion Principle (DIP). High-level modules should not depend on
low-level modules; both should depend on abstractions. Abstractions should not
depend on details; details should depend on abstractions.
a.
http://en.wikipedia.org/wiki/SOLID_(object-oriented_design)
Smaller, more focused classes more readily provide value in another context—
re-use! In contrast, a very large class with lots of responsibilities cannot
possibly be used in other contexts.
Underlying the SOLID principles are the concepts of cohesion and coupling.
Classes in your systems should exhibit high cohesion and low coupling. Such
systems make change easier, and they also make unit testing easier.
The concepts of SOLID, low coupling, and high cohesion are not new, but
they’re also not “outdated.” Despite some post-modern ideas about software
design, these principles remain valid. They’re not absolutes: all choices in
software systems represent tradeoffs. You must balance the principles with
Chapter 9. Refactoring Your Code’s Structure • 172
report erratum  •  discuss


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


---
**Page 181**

The score side effect causes another problem, which is that a client can’t sep-
arate one interest from the other. If a client wants (only) the score for a set
of criteria, it must first call the matches() method. This sort of temporal coupling
is not going to be immediately obvious to a developer and demands clear
documentation. The client would ignore the boolean value returned by matches
(awkward!) and then call the score accessor. Conversely, for a client interested
in determining whether a set of criteria matches, the call to matches ends up
altering the Profile’s score attribute.
A method that both returns a value and generates a side effect (changes the
state of the class or some other entity in the system) violates the principle
known as command-query separation (CQS): A method should either be a
command, creating a side effect, or a query that returns a value. It should
not be both.
Lack of CQS can create potential pain for client code. If a query method alters
the state of an object, it might not work to call that method again. You might
not get the same answer a second time, and it might cause trouble to trigger
the side effect a second time.
Lack of CQS also violates expectations for developers using the query method.
Without careful reading of the code and its tests, it’s possible for a developer
to completely overlook the side effect and thus create a problem.
Fixing the CQS Problem in Profile
A client of Profile should be free to call a method without having to know they
must first call another. Make clients happy by moving all the score-related
logic into the score accessor. It’s not much work, particularly since you’d moved
the bulk of the logic into Matcher.
utj3-refactor/22/src/main/java/iloveyouboss/Profile.java
public boolean matches(Criteria criteria) {
return new Matcher(criteria, answers).matches();
}
public int score(Criteria criteria) {
➤
return new Matcher(criteria, answers).score();
➤
}
Most significantly, the score method is no longer a raw accessor. It now takes
on a Criteria instance as an argument and then delegates to a new Matcher that
calculates and retrieves the score.
Don’t forget to delete the score field from Profile; it is no longer needed.
report erratum  •  discuss
Command-Query Separation • 181


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


---
**Page 188**

Now that you’ve learned to continually address your system’s micro and
macro-level design because your unit tests allow you to do so with high confi-
dence, it’s time to take a look at those tests themselves. Next up, you’ll see
how streamlining your tests lets them pay off even more as concise, clear,
and correct documentation on all the unit capabilities you’ve built into your
system.
Chapter 9. Refactoring Your Code’s Structure • 188
report erratum  •  discuss


---
**Page 189**

CHAPTER 10
Streamlining Your Tests
You’ve wrapped up a couple of chapters that teach you how to use tests to
keep your code clean. Now, it’s time to focus on the tests themselves.
Your tests represent a significant investment. They’ll pay off by minimizing
defects and allowing you to keep your production system clean through
refactoring. But, they also represent a continual cost. You need to continually
revisit your tests as your system changes. At times, you’ll want to make
sweeping changes and might end up having to fix numerous broken tests as
a result.
In this chapter, you’ll learn to refactor your tests, much like you would
refactor your production system, to maximize understanding and minimize
maintenance costs. You’ll accomplish this by learning to identify a series of
“smells” in your tests that make it harder to quickly understand them. You’ll
work through an example or two of how you can transform each smell into
de-odorized code.
The deodorization process is quick. In reading through the chapter, you might
think it would take a long time to clean a test similar to the example in the
chapter. In reality, it’s often well under fifteen minutes of real work once you
learn how to spot the problems.
Tests as Documentation
Your unit tests should provide lasting and trustworthy documentation of the
capabilities of the classes you build. Tests provide opportunities to explain
things that the code itself can’t do as easily. Well-designed tests can supplant
a lot of the comments you might otherwise feel compelled to write.
report erratum  •  discuss



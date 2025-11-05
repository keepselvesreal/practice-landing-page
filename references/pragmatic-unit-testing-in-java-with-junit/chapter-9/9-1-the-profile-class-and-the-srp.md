# 9.1 The Profile Class and the SRP (pp.170-173)

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



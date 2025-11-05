# 8.2 Finding Better Homes for Your Methods (pp.154-157)

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



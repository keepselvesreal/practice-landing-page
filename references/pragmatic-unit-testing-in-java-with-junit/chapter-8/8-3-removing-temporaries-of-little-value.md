# 8.3 Removing Temporaries of Little Value (pp.157-158)

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



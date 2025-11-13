# 8.4 Amplifying the Core Intent of Code (pp.158-162)

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



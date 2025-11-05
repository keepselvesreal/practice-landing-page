# 9.3 Command-Query Separation (pp.180-182)

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



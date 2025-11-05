# 8.7 Summary (pp.167-169)

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



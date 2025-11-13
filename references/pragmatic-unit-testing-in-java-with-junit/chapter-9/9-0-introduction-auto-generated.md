# 9.0 Introduction [auto-generated] (pp.169-170)

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



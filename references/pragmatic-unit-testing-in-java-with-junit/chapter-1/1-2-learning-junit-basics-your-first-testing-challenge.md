# 1.2 Learning JUnit Basics: Your First Testing Challenge (pp.4-8)

---
**Page 4**

and stops immediately to fix it. The problems she creates are a lot easier to
fix since she’s added only a few lines of code since she last saw all the tests
pass. She avoids piling lots of new code atop her mistakes before discovering
a problem.
Lucia’s tests are part of the system and included in the project’s GitHub
repository. They continue to pay off each time she or anyone else changes
code, alerting the team when someone breaks existing behavior.
Lucia’s tests also save Joe and everyone else on the team significant amounts
of comprehension time on their system. “How does the system handle the
case where the end date isn’t provided?” asks Madhu, the product owner.
Joe’s response, more often than not, is, “I don’t know; let me take a look at
the code.” Sometimes, Joe can answer the question in a minute or two, but
frequently, he ends up digging about for a half hour or more.
Lucia looks at her unit tests and finds one that matches Madhu’s case. She
has an answer within a minute or so.
You’ll follow in Lucia’s footsteps and learn how to write small, focused unit
tests. You’ll start by learning basic JUnit concepts.
Learning JUnit Basics: Your First Testing Challenge
For your first example, you’ll work with a small class named CreditHistory. Its
goal is to return the mean (average) for a number of credit rating objects.
In this book, you’ll probe the many reasons for choosing to write unit tests.
For now, you’ll start with a simple but critical reason: you want to continue
adding behaviors to CreditHistory and want to know the moment you break any
previously coded behaviors.
Initially, you will see screenshots to help guide you through getting started
with JUnit. After this chapter, you will see very few screenshots, and you
won’t need them.
The screenshots demonstrate using JUnit in IntelliJ IDEA. If you’re using
another integrated development environment (IDE), the good news is that
your JUnit test code will look the same whether you use IDEA, Eclipse,
VSCode, or something else. How you set up your project to use JUnit will
differ. The way the JUnit looks and feels will differ from IDE to IDE, though
it will, in general, operate the same and produce the same information.
Chapter 1. Building Your First JUnit Test • 4
report erratum  •  discuss


---
**Page 5**

Here’s the code you need to test:
utj3-credit-history/01/src/main/java/credit/CreditHistory.java
import java.time.LocalDate;
import java.time.Month;
import java.util.*;
public class CreditHistory {
private final List<CreditRating> ratings = new ArrayList<>();
public void add(CreditRating rating) {
ratings.add(rating);
}
public int arithmeticMean() {
var total = ratings.stream().mapToInt(CreditRating::rating).sum();
return total / ratings.size();
}
}
The CreditHistory class collects CreditRating objects through its add method. Its
current primary goal is to provide you with an average (arithmeticMean) of the
scores contained in the credit rating objects.
You implement CreditRating with a Java record declaring a single rating field.
utj3-credit-history/01/src/main/java/credit/CreditRating.java
public record CreditRating(int rating) {}
Your first exercise is small, and you could easily enter it from scratch. Typing
in the code yourself should help you grow your coding skills faster. Still, you
can also choose to download the source for this and all other exercises from
https://pragprog.com/titles/utj3/pragmatic-unit-testing-in-java-with-junit-third-edition/.
Where to Put the Tests
Your project is laid out per the Apache Software Foundation’s standard
directory layout:
1
utj3-credit-history
src/
main/
java/
credit/
CreditHistory.java
CreditRating.java
test/
java/
credit/
1.
https://maven.apache.org/guides/introduction/introduction-to-the-standard-directory-layout.html
report erratum  •  discuss
Learning JUnit Basics: Your First Testing Challenge • 5


---
**Page 6**

Your two production source files for this project are stored in the directory
src/main/java in the package named credit. (IntelliJ IDEA refers to the direc-
tory src/main/java as a Sources Root.)
You’re ready to write a test that describes the behavior in CreditHistory. You’ll
be putting the test in the same package as the production source—credit—but
in the Test Sources Root directory src/test/java.
Your IDE probably provides you with many ways to create a new test class.
In IDEA, you’ll create it by following these steps in the Project explorer:
1.
Select the package src/test/java/credit from the Project or Packages explorer.
2.
Right-click to bring up the context menu.
3.
Select New ▶ Java Class. You will see the New Java Class popup, which
defaults its selection to creating a new class.
4.
Type the classname ACreditHistory (“a credit history”); press enter. IDEA’s
inspections may be unhappy about your test naming convention. You
can reconfigure the inspection,
2 or you can go with the old-school name
CreditHistoryTest.
Running Tests: Testing Nothing at All
When you press enter from the New ▶Java Class menu item, IDEA provides you
with an empty class declaration for ACreditHistory. Your first job is to squeeze
a test method into it:
utj3-credit-history/01/src/test/java/credit/ACreditHistory.java
class ACreditHistory {
@org.junit.jupiter.api.Test
➤
void whatever() {
➤
}
➤
}
To be a bit more specific: Within the body of ACreditHistory, type in the three
lines that start with the @org.junit.jupiter.api.Test annotation.
Lines marked with arrows in code listings represent added lines,
changed lines, or otherwise interesting bits of code.
Type? Yes. It’s better to type code and tests in yourself while learning, rather
than copy/paste them, unless typing isn’t at all your thing. It’ll feel more like
2.
https://langrsoft.com/2024/04/28/your-new-test-naming-convention/
Chapter 1. Building Your First JUnit Test • 6
report erratum  •  discuss


---
**Page 7**

real development, which should help you learn more. It also won’t take as long
as you think. Your IDE offers numerous time-saving shortcuts, such as
intellisense, live templates, and context-sensitive “quick fix.”
Your test is an empty method annotated with the type @org.junit.jupiter.api.Test.
When you tell JUnit to run one or more tests, it will locate all methods
annotated with @Test and run them. It’ll ignore all other methods.
You can run your empty test, which, for now, you’ve given a placeholder name
of whatever. As usual, you have many options for executing tests. You’ll start
by being mousey. Click the little green arrow that appears to the left of the
class declaration, as shown in the following figure. (Chances are good your
IDE has a similar icon.)
Clicking the green arrow pops up a context menu where you can select the
option to run all tests in ACreditHistory, as shown in this figure:
Clicking Run 'ACreditHistory' runs the whatever test. It’s passing, as the figure on
page 8 reveals.
If your test isn’t getting executed, make sure it follows these three guidelines:
• it is annotated with @org.junit.jupiter.api.Test
• it has a void return
• it has no parameters
report erratum  •  discuss
Learning JUnit Basics: Your First Testing Challenge • 7


---
**Page 8**

The built-in JUnit test runner appears at the bottom of the IDE. Its left-hand
panel shows a summary of all the tests executed. Your summary shows that
you ran the whatever test within ACreditHistory, that it succeeded (because it has
a green check mark), and that it took 12 milliseconds to execute.
The test runner’s right-hand panel shows different information depending on
what’s selected in the left-hand panel. By default, it tells you how many tests
passed out of the number that were executed (yours: “1 of 1”). It also provides
you with information captured as part of the JUnit process execution. (In this
screenshot, the IDE is configured to use Gradle to execute the test via the
build task, which also executes the tests.)
You now know something fundamental about how JUnit behaves: an empty
test passes. More specifically and more usefully, a test whose method execu-
tion completes—without having encountered any failure points or throwing
any exceptions—is a passing test.
Writing a First Real Test
An empty test isn’t of much use. Let’s devise a good first test.
You could start with a meaty test that adds a few credit scores, asks for the
average, and then ascertains whether or not you got the right answer. This
happy path test case—in contrast with negative or error-based tests—is not
the only test you’d want to write, though. You have some other cases to con-
sider for verifying arithmeticMean:
Chapter 1. Building Your First JUnit Test • 8
report erratum  •  discuss



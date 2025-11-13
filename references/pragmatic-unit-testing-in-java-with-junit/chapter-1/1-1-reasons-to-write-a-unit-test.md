# 1.1 Reasons to Write a Unit Test (pp.3-4)

---
**Page 3**

CHAPTER 1
Building Your First JUnit Test
In this chapter, we’ll write a unit test by working through a small example.
You’ll set up your project, add a test class, and see what a test method looks
like. Most importantly, you’ll get JUnit to run your new, passing test.
Reasons to Write a Unit Test
Joe has just completed work on a small feature change, adding several dozen
lines to the system. He’s fairly confident in his change, but it’s been a while
since he’s tried things out in the deployed system. Joe runs the build script,
which packages and deploys the change to the local web server. He pulls up
the application in his browser, navigates to the appropriate screen, enters a
bit of data, clicks submit, and…stack trace!
Joe stares at the screen for a moment, then the code. Aha! Joe notes that he
forgot to initialize a field. He makes the fix, runs the build script again, cranks
up the application, enters data, clicks submit, and…hmm, that’s not the right
amount. Oops. This time, it takes a bit longer to decipher the problem. Joe
fires up his debugger and after a few minutes discovers an off-by-one error
in indexing an array. He once again repeats the cycle of fix, deploy, navigate
the GUI, enter data, and verify results.
Happily, Joe’s third fix attempt has been the charm. But he spent about fifteen
minutes working through the three cycles of code/manual test/fix.
Lucia works differently. Each time she writes a small bit of code, she adds a
unit test that verifies the small change she added to the system. She then
runs all her unit tests, including the new one just written. They run in sec-
onds, so she doesn’t wait long to find out whether or not she can move on.
Because Lucia runs her tests with each small change, she only moves on
when all the tests pass. If her tests fail, she knows she’s created a problem
report erratum  •  discuss


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



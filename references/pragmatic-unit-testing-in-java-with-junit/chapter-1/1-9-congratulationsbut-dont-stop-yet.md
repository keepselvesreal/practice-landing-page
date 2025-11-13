# 1.9 Congratulations!…But Don’t Stop Yet (pp.24-25)

---
**Page 24**

var result = creditHistory.arithmeticMean();
assertEquals(800, result);
}
}
Always consider writing a test for each of Zero, One, and Many
(ZOM) cases.
Covering Other Cases: Creating a Test List
Beyond the ZOM cases you’ve covered, you could brainstorm edge cases and
exception-based tests. You’ll explore doing that in later chapters.
As you write tests and continue to re-visit/re-read the code you’re testing,
you’ll think of additional tests you should write. In fact, as you write the code
yourself in the first place—before trying to write tests for it—think about and
note the cases you’ll need for that code.
Add the cases you think of to a test list to remember to write them. Cross
them off as you implement or obviate them. You can do this on paper, in a
notepad file, or even in the test class itself as a series of comments. (Perhaps
in the form of TODO comments, which IDEs like IntelliJ IDEA and Eclipse will
collect in a view as a set of reminders.) Things change, so don’t expend the
effort to code these tests just yet. You can read more on this highly useful
tool in Kent Beck’s seminal book on TDD [Bec02].
Congratulations!…But Don’t Stop Yet
In this chapter, you got past one of the more significant challenges: getting
a first test to pass using JUnit in your IDE. Congrats! Along with that
achievement, you also learned:
• What it takes to write a test that JUnit can accept and run
• How to tell JUnit to run your tests
• How to interpret the test results provided by JUnit
• How to use the ZOM mnemonic to figure out what the next test might be
• How to structure a test using AAA
You’ve been reading about “units” throughout this chapter. Next up, you’ll
learn what a unit is, and you’ll learn a number of tactics for testing some of
the common units that you’ll encounter.
Chapter 1. Building Your First JUnit Test • 24
report erratum  •  discuss


---
**Page 25**

CHAPTER 2
Testing the Building Blocks
In the previous chapter, you took a small piece of code and wrote a few JUnit
tests around it. In the process, you learned how to structure your tests, exe-
cute them, how to interpret results, and what test to write next.
You’ve only scratched the surface of what it means to write tests for code. In
this chapter, you’ll examine several common code constructs and learn how
to test them. These are the topics you’ll cover:
• Testing pure functions
• Testing code with side effects
• How different designs can impact unit tests
• Writing tests for code involving lists
• Writing tests for code that throws exceptions
• Covering boundary conditions with tests
First, however, let’s talk about the word unit in unit test.
Units
A software system is an organized collection of many units. A unit is the
smallest piece of code that accomplishes a specific behavioral goal—a concept.
Here are some examples of concepts:
• Capitalize the first letter of a word
• Move a passenger from the standby list to the boarding list
• Mark a passenger as upgraded
• Calculate the mean credit rating for an individual
• Throw an exception when a user is under 18 years old
report erratum  •  discuss



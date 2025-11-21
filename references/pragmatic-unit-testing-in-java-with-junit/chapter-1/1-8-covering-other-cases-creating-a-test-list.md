# 1.8 Covering Other Cases: Creating a Test List (pp.24-24)

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



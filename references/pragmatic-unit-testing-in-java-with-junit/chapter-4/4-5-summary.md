# 4.5 Summary (pp.95-99)

---
**Page 95**

Jqwik, a sophisticated and highly flexible tool, calls the property one thousand
times by default. And, beauty! The last property fails, and consistently so,
given those thousand inputs.
The array sort code represents a good fit for property testing. You might think
to write a handful of test cases (ZOM, certainly). But there are some cases
that can be hard to think of. Property testing can help uncover those cases.
Yes, there’s a defect in the insertion sort. The jqwik tool should identify the
problem. See if you can figure out and fix the defective code.
Summary
In this chapter, you rounded out your knowledge of core unit testing concepts
with a few (mostly unrelated) topics that look at bigger concerns surrounding
unit testing:
• Code coverage, a concept that can help you learn where your unit testing
is deficient
• Testing multithreaded code, a tricky and sophisticated challenge
• Integration tests, which verify code and its interaction with external
dependencies that might be out of your control
Now that you’ve worked through foundational concepts regarding unit testing,
you’ll take a deeper look into the preferred tool for Java unit testing, JUnit.
The next three chapters will explore JUnit in-depth, providing useful insights
and nuggets on how to best take advantage of its wealth of features.
report erratum  •  discuss
Summary • 95


---
**Page 97**

Part II
Mastering JUnit with “E”s
You can accomplish most of your unit testing needs
with a small fraction of JUnit’s robust capabilities.
In this part, you’ll learn to streamline your day-to-
day unit testing activities by delving into the three
"E"s of JUnit: Examining outcomes with assertions,
Establishing organization in your tests, and Execut-
ing your tests.


---
**Page 99**

CHAPTER 5
Examining Outcomes with Assertions
You’ve learned the most important features of JUnit in the prior four chapters
of this book, enough to survive but not thrive. Truly succeeding with your
unit testing journey will involve gaining proficiency with your primary tool,
JUnit. In this and the next couple of chapters, you’ll explore JUnit in signifi-
cant detail. First, you’ll focus on JUnit’s means of verification—its assertion
library.
Assertions (or asserts) in JUnit are static method calls that you drop into
your tests. Each assertion is an opportunity to verify that some condition
holds true. If an asserted condition does not hold true, the test stops executing
right there and JUnit reports a test failure.
To abort the test, JUnit throws an exception object of type AssertionFailedError.
If JUnit catches AssertionFailedError, it marks the test as failed. In fact, JUnit
marks any test as failed that throws an exception not caught in the test body.
In order to use the most appropriate assertion for your verification need, you’ll
want to learn about JUnit’s numerous assertion variants.
In examples to this point, you’ve used the two most prevalent assertion forms,
assertTrue and assertEquals. Since you’ll use them for the bulk of your tests, you’ll
first examine these assertion workhorses more deeply. You’ll then move on
to exploring the numerous alternative assertion choices that JUnit provides.
In some cases, the easiest way to assert something won’t be to compare to
an actual result but to instead verify an operation by inverting it. You’ll see
a brief example of how.
You’ll also get an overview of AssertJ, a third-party assertion library that
allows you to write “fluent” assertions. Such assertions can make your tests
considerably easier to read. They can also provide more precise explanations
about why a test is failing.
report erratum  •  discuss



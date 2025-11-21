# 7.4 Exploring More Features (pp.142-143)

---
**Page 142**

Gradle is a great way to build and run tests within a continuous build envi-
ronment. But don’t use Gradle for interactive unit testing unless you customize
its output to remind you of disabled tests. Have it fail the test run if any dis-
abled tests exist or show their count as the last line of output.
Disabled tests should not really exist other than on your own machine. Avoid
integrating disabled tests—they usually represent big questions about the
health of your system, such as these: Is the test really needed? Can we just
delete it? What do we currently understand about why we couldn’t immedi-
ately get this to pass?
Exploring More Features
JUnit has grown over its past 20-something years into a fairly large and
sophisticated tool. It’s likely that the features you’ve learned in this chapter
will be enough for your needs for years to come. However, it’s also possible
that one of JUnit’s other features
2 might be useful for your special circum-
stances. Here’s a quick summary:
Abort execution of a test if an assumption is not met (but
don’t count it as failed).
assumptions
Enable or disable tests conditionally. Conditions can ref-
erence the OS, architecture, Java version, value of a system
property/environment variable, or custom-coded predicates.
conditional test
execution
Rather than show the (typically) camel-cased test name
during a test run, show the contents of a string.
display names
Generate more human-readable test names by transform-
ing the test method names. For example, transform
underscores in test names into spaces.
display name
generators
Generate tests at runtime.
dynamic tests
Run tests concurrently to speed up their execution.
parallel execution
Run a test a specified number of times.
repeated tests
Programmatically declare a filtered collection of tests to
execute.
suites
Write a file-dependent test that executes in the context
of a temporary directory.
temp dir context
Fail a test (or lifecycle method) if its execution time
exceeds a specific duration.
timeouts
2.
https://junit.org/junit5/docs/current/user-guide/
Chapter 7. Executing JUnit Tests • 142
report erratum  •  discuss


---
**Page 143**

Summary
In this and the prior two chapters that dig into JUnit, you learned the bulk
of what you’ll need to know about writing assertions, organizing your tests,
and running your tests.
With this solid foundation for JUnit, you can move on to more important
concerns. In the next part of the book, you’ll focus on tests and their relation-
ship to your system’s design. You’ll refactor your code “in the small” because
you have tests that give you the confidence to do so. You’ll touch on larger
design concepts as well, and you’ll also learn how to design your tests to
increase the return on your investment in them.
report erratum  •  discuss
Summary • 143



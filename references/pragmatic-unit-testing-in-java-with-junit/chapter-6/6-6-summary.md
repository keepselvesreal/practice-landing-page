# 6.6 Summary (pp.134-135)

---
**Page 134**

Here’s a quick summary:
A single array of values. Useful only if your test takes one
parameter (which implies that the expected outcome is the
same for every source value)
@ValueSource
Iterates all the possible enum values, with some options for
inclusion/exclusion and regex matching
@EnumSource
Expects the name of a method, which must return all data
rows in a stream
@MethodSource
Mostly the same thing as @CsvSource, except that you specify
a filename containing the CSV rows
@CsvFileSource
Allows you to create a custom, reusable data source in a
class that extends an interface named ArgumentsProvider
@ArgumentsSource
While parameterized tests in JUnit are sophisticated and flexible beasts,
@CsvSource will suit most of your needs. I’ve never needed another data source
variant (though I don’t frequently use parameterized tests).
In summary, parameterized tests are great when you need to demonstrate
data (not behavioral) variants. These are a couple of pervasive needs:
• Code that conditionally executes if a parameter is null or an empty string.
A parameterized test with two inputs (null and "") lets you avoid test
duplication.
• Code around border conditions, particularly because such code often
breeds defects. For example, for code that conditionally executes if n <= 0,
use a parameterized test with the values n - 1 and n.
Otherwise, create a new @Test that describes a distinct behavior.
Summary
On most systems, you’ll end up with many hundreds or thousands of unit
tests. You’ll want to keep your maintenance costs low by taking advantage
of a few JUnit features, including lifecycle methods, nested classes, and param-
eterized tests. These features allow you to reduce redundant code and make
it easy to run a related set of tests.
Now that you’ve learned how to best organize your tests, in the next chapter,
you’ll dig into topics that relate to executing tests using JUnit. You’ll pick up
some good habits for deciding how many tests to run (and when to not run
tests). You’ll learn how to run subsets of tests as well as how to temporarily
disable tests.
Chapter 6. Establishing Organization in JUnit Tests • 134
report erratum  •  discuss


---
**Page 135**

CHAPTER 7
Executing JUnit Tests
You learned about assertions, test organization, and the JUnit lifecycle of
execution earlier in this part of the book.
Having all the tests in the world is useless if you never run them. You’ll want
to run tests often as you build software on your own machine like you’ve been
doing so far. But you’ll also want to run them as part of the process of vetting
integrated software before deploying it, perhaps as part of a continuous build
process.
In this chapter, you’ll learn “when,” “what,” and more of the “how” of running
tests:
• What set of unit tests you’ll want to run when executing JUnit
• Grouping tests using the JUnit @Tag annotation, which allows you to
execute arbitrary groups of tests
• Temporarily not running your tests using the @Disabled annotation
Testing Habits: What Tests to Run
Full-fledged Java IDEs (for example, IntelliJ IDEA or Eclipse) have built-in
support for JUnit. Out of the box, you can load a project, click on its test
directory, and execute tests without having to configure anything. You saw
in Chapter 1, Building Your First JUnit Test, on page 3 at least a couple of
ways to run JUnit tests from within IntelliJ IDEA. In the following sections,
you’ll see how the number of tests you run affects your results.
Run All the Tests
If your tests are fast (see Fast Tests, on page 66), it’s possible to run thousands
of unit tests within a few seconds. When you have fast tests, you can run all
report erratum  •  discuss



# 10.13 Summary (pp.207-211)

---
**Page 207**

Summary
You ended up with four sleek, refactored tests. A developer can understand
the goal of each test through its name, which provides a generalized summary
of behavior. They can see how that behavior plays out by reading the example
within the test. Arrange—Act—Assert (AAA) guides them immediately to the
act step so that they can see how the code being verified gets executed. They
can reconcile the asserts against the test name’s description of behavior.
Finally, if needed, they can review the arrange step to understand how it puts
the system in the proper state to be tested.
The tests are scannable. A developer can rapidly find and digest each test
element (name, arrange, act, and assert) they’re interested in. The needed
comprehension can happen in seconds rather than minutes. Remember also
that readily understood tests—descriptions of unit behavior—can save even
hours of time required to understand production code.
Seeking to understand your system through its tests motivates
you to keep them as clean as they should be.
It only takes minutes to clean up tests enough to save extensive future
amounts of comprehension time.
You now have a complete picture of what you must do in the name of design:
refactor your production code for clarity and conciseness, refactor your pro-
duction code to support more flexibility in design, design your system to
support mocking of dependency challenges, and refactor your tests to minimize
maintenance and maximize understanding.
You’re ready to move on to the final part of this book, a smorgasbord of
additional topics related to unit testing.
report erratum  •  discuss
Summary • 207


---
**Page 209**

Part IV
Bigger Topics Around Unit Testing
Writing tests is but a part of a larger experience.
Explore unit testing in various modern and relevant
contexts: test-driven development (TDD), project
teams, and AI-driven development.


---
**Page 211**

CHAPTER 11
Advancing with Test-Driven
Development (TDD)
You’re now armed with what you’ll need to know about straight-up unit
testing in Java. In this part, you’ll learn about three significant topics:
• Using TDD to flip the concept of unit testing from test-after to test-driven
• Considerations for unit testing within a project team
• Using AI tooling to drive development, assisted by unit tests
You’ll start with a meaty example of how to practice TDD.
It’s hard to write unit tests for some code. Such “difficult” code grows partly
from a lack of interest in unit testing. In contrast, the more you consider how
to unit test the code you write, the more you’ll end up with easier-to-test code.
(“Well, duh!” responds our reluctant unit tester Joe.)
With TDD, you think first about the outcome you expect for the code you’re
going to write. Rather than slap out some code and then figure out how to
test it (or even what it should do), you first capture the expected outcome in
a test. You then code the behavior needed to meet that outcome. This reversed
approach might seem bizarre or even impossible, but it’s the core element
in TDD.
With TDD, you wield unit tests as a tool to help you shape and control your
systems. Rather than a haphazard practice where you sometimes write unit
tests after you write code, and sometimes you don’t, describing outcomes and
verifying code through unit tests becomes your central focus.
You will probably find the practice of TDD dramatically different than
anything you’ve experienced in software development. The way you build
report erratum  •  discuss



# 2.7 Exploring Boundaries with CORRECT (pp.51-52)

---
**Page 51**

If you view the unit tests as a way of characterizing all your code units, collec-
tively they become the requirements in an odd but useful little “requirements
by example” manner. Your test names describe the behavioral needs. Each
test provides an example of one of those behaviors.
Such well-named requirements-by-example (tests) can quickly answer ques-
tions others (or even you) might ask: “hey, what does the system do when we
try to calculate the arithmetic mean and there are no credit ratings?” Everyone
is happy, you have an immediate answer, and you’re highly confident it’s
correct because all of your tests are passing.
One way to take control: invert your approach to unit testing—drive a
requirements change by first updating the tests that relate to the change.
After observing that the updated tests fail (because you’ve not yet updated
the system with the new requirement), you can make the necessary changes
and then run all tests to ensure you’re still happy.
Once you feel increased control by test-driving changes, your next thought
might be, “what if I drove in all new functionality this way?” You can, and
doing so is known as Test-Driven Development (TDD). See Chapter 11,
Advancing with Test-Driven Development (TDD), on page 211 for a rundown
of what TDD looks like and why it might help even more. Get a little excited
about it—because TDD is also a lot of fun—but for now, you should continue
your unit testing journey.
Testing that an exception is thrown when expected is as important as testing
any other code. You’ll also want to verify that other code responds properly
to the situation when an exception is thrown. Doing so is a slightly trickier
technique; visit Testing Exception Handling, on page 65 for details.
Exploring Boundaries with CORRECT
The zero, one, many, and exception-based tests will cover most of your typical
needs when testing code. But you’ll also want to consider adding tests for
cases that a happy path through the code might not hit. These boundary
conditions represent scenarios that involve the edges of the input domain.
You can employ the CORRECT acronym, devised by Andy Hunt and Dave
Thomas for the first edition of this book [HT03], to help you think about
potential boundary conditions. For each of these items, consider whether or
not similar conditions can exist in the method that you want to test and what
might happen if these conditions are violated:
report erratum  •  discuss
Exploring Boundaries with CORRECT • 51


---
**Page 52**

• Conformance—Does the value conform to an expected format, such as
an email address or filename? What does the method do when passed an
invalid format? Does a string parameter support upper or mixed case?
• Ordering—Is the set of values ordered or unordered as appropriate? What
happens if things happen out of chronological order, such as an HTTP
server that returns an OPTIONS response after a POST instead of before?
• Range—Is the value within reasonable minimum and maximum values?
Can any computations result in numeric overflow?  range
• Reference—Does the object need to be in a certain state? What happens
if it’s in an unexpected state? What if the code references something
external that’s not under its direct control?
• Existence—Does the value exist (is it non-null, nonzero, present in a set)?
What if you pass a method empty values (0, 0.0, "", null)?
• Cardinality—Are there exactly enough values? Have you covered all your
bases with ZOM? Can it handle large volumes? Is there a notion of too
many? What if there are duplicates in a list that shouldn’t allow them (for
example, a roster of classroom students)?
• Time (absolute and relative)—Is everything happening in order? At the
right time? In time?
Many of the defects you’ll code in your career will involve similar corner cases,
so you’ll positively want to cover them with tests.
Summary
You have worked through writing tests for a number of common unit
scenarios. Your own “real” code test will, of course, be different and often
more involved. Still, how you approach writing tests for your code will be
similar to the approaches you’ve learned here.
Much of the code you try to test will be dependent on other classes that are vol-
atile, slow, or even incomplete. In the next chapter, you’ll learn how to use
test doubles (colloquially referred to as mock objects or mocks) to break those
dependencies so that you can test.
Chapter 2. Testing the Building Blocks • 52
report erratum  •  discuss



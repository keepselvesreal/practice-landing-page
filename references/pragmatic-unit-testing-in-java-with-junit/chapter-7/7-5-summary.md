# 7.5 Summary (pp.143-147)

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


---
**Page 145**

Part III
Increasing ROI: Unit Testing and Design
Elevate your unit tests beyond mere logic validation.
In this part, learn how to use your tests to maintain
clean code—both "in the small" and "in the large"—
and document your system’s unit capabilities.


---
**Page 147**

CHAPTER 8
Refactoring to Cleaner Code
In Parts I and II, you dug deep into how to write unit tests and take advantage
of JUnit. In this part, you’ll learn to take advantage of unit tests to help shape
the design of your system, as well as document the numerous unit-level
behavioral choices you’ve made. Your ability to keep your system simpler and
your tests clearer can reduce your development costs considerably.
You’ll start by focusing on design “in the small,” addressing the lack of clarity
and excessive complexity that’s commonplace in most systems. You’ll
accomplish this by learning to refactor—making small, frequent edits to the
code you write. Your design improvements will help reduce the cost of change.
In a clear, well-designed system, it might take seconds to locate a point of
change and understand the surrounding code. In a more typically convoluted
system, the navigation and comprehension tasks often require minutes
instead. Once you’ve understood the code well enough to change it, a well-
designed system might accommodate your change readily. In the convoluted
system, weaving in your changes might take hours.
Convoluted systems can increase your maintenance costs by an
order of magnitude or more.
You can, with relative ease, create systems that embody clean code. In brief,
this describes clean code:
• Concise: It imparts the solution without unnecessary code.
• Clear: It can be directly understood.
report erratum  •  discuss



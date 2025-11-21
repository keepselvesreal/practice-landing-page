# 8.0 Introduction [auto-generated] (pp.147-148)

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


---
**Page 148**

• Cohesive: It groups related concepts together and apart from unrelated
concepts.
• Confirmable: It can be easily verified with tests.
Your unit tests provide you with that last facet of clean code.
A Little Bit o’ Refactor
Refactoring is a fancy way to indicate that you’re transforming the underlying
structure of your code—its implementation details—while retaining its existing
functional behavior. Since refactoring involves reshaping and moving code,
you must ensure your system still works after such manipulations. Unit tests
are the cheapest, fastest way to do so.
Refactoring is to coding as editing is to writing. Even the best (expository)
writers edit most sentences they write to make them immediately clear to
readers. Coding is no different. Once you capture a solution in an editor, your
code is often harder to follow than necessary.
Writers follow the mindset to write first for themselves and then for others.
To do so as a programmer, first, code your solution in a way that makes sense to
you. Then, consider your teammates who must revisit your code at some
point in the future. Rework your code to provide a clearer solution now while
it still makes sense to you.
Code in two steps: first, capture your thoughts in a correct solu-
tion. Second, clarify your solution for others.
Confidence is the key consideration when it comes to refactoring. Without
the confidence that good unit tests provide, you’d want to be extremely cau-
tious about “fixing” code that’s already working. In fact, without unit tests,
you might think, “it ain’t broke. Don’t fix it.” Your code would start its life
unedited—with deficiencies—and would get a little worse with each change.
If you’ve followed the recommendations in this book, however, you can make
changes willy-nilly. Did you think of a new name for a method, one that makes
more sense? Rename it (ten seconds in a good IDE; perhaps minutes other-
wise), run your tests, and know seconds later that nothing broke. Method too
long and hard to follow? Extract a chunk of it to a new method, and run your
tests. Method in the wrong place? Move it, run tests. You can make small
improvements to your codebase all day long, each making it incrementally
easier (cheaper) to work with.
Chapter 8. Refactoring to Cleaner Code • 148
report erratum  •  discuss



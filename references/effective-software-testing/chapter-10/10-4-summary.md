# 10.4 Summary (pp.275-276)

---
**Page 275**

275
Summary
A Make each test runner a specific sandbox.
B Use fresh fixtures in every test.
C Remove and isolate duplicated test code.
D Clean up the state during teardown.
Summary
Writing good test code is as challenging as writing good production code. We
should ensure that our test code is easy to maintain and evolve.
We desire many things in a test method. Tests should be fast, cohesive, and
repeatable; they should fail for a reason and contain strong assertions; they
should be easy to read, write, and evolve; and they should be loosely coupled
with the production code.
Many things can hinder the maintainability of test methods: too much duplica-
tion, too many bad assertions, bad handling of complex (external) resources, too
many general fixtures, too many sensitive assertions, and flakiness. You should
avoid these.


---
**Page 276**

276
Wrapping up the book
We are now at the end of this book. The book comprises a lot of my knowledge
about practical software testing, and I hope you now understand the testing tech-
niques that have supported me throughout the years. In this chapter, I will say some
final words about how I see effective testing in practice and reinforce points that I
feel should be uppermost in your mind.
11.1
Although the model looks linear, iterations 
are fundamental
Figure 11.1 (which you saw for the first time back in chapter 1) illustrates what I
call effective software testing. Although this figure and the order of the chapters in this
book may give you a sense of linearity (that is, you first do specification-based test-
ing and then move on to structural testing), this is not the case. You should not
view the proposed flow as a sort of testing waterfall.
 Software development is an iterative process. You may start with specification-
based testing, then go to structural testing, and then feel you need to go back to
specification-based testing. Or you may begin with structural testing because the
This chapter covers
Revisiting what was discussed in this book



# 1.4.4 When to use each test level (pp.23-23)

---
**Page 23**

23
The testing pyramid, and where we should focus
than usual (due to small variations we often do not control in real-life scenar-
ios). The test does not expect this and thus fails. The test is executed again, the
web app takes the usual time to respond, and the test passes. Many uncertain-
ties in a system test can lead to unexpected behavior. 
1.4.4
When to use each test level
With a clear understanding of the different test levels and their benefits, we have to
decide whether to invest more in unit testing or system testing and determine which
components should be tested via unit testing and which components should be tested
via system testing. A wrong decision may have a considerable impact on the system’s
quality: a wrong level may cost too many resources and may not find sufficient bugs.
As you may have guessed, the best answer here is, “It depends.”
 Some developers—including me—favor unit testing over other test levels. This
does not mean such developers do not do integration or system testing; but whenever
possible, they push testing toward the unit test level. A pyramid is often used to illus-
trate this idea, as shown in figure 1.8. The size of the slice in the pyramid represents
the relative number of tests to carry out at each test level.
Unit testing is at the bottom of the pyramid and has the largest area. This means
developers who follow this scheme favor unit testing (that is, write more unit tests).
Climbing up in the diagram, the next level is integration testing. The area is smaller,
indicating that, in practice, these developers write fewer integration tests than unit
tests. Given the extra effort that integration tests require, the developers write tests
only for the integrations they need. The diagram shows that these developers favor
system tests less than integration tests and have even fewer manual tests. 
1.4.5
Why do I favor unit tests?
As I said, I tend to favor unit testing. I appreciate the advantages that unit tests give
me. They are easy to write, they are fast, I can write them intertwined with production
code, and so on. I also believe that unit testing fits very well with the way software
Unit tests
Integration tests
System tests
Manual
More real
More complex
All business rules
should be tested here.
Exploratory tests
Complex integrations
with external services
Tests the main/risky
ﬂow of the app
Figure 1.8
My version of the testing pyramid. The closer a test is to the 
top, the more real and complex the test becomes. At the right part you see 
what I test at each test level.



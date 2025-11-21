# 11.5.3 Is there proof that unit testing helps? (pp.228-228)

---
**Page 228**

228
CHAPTER 11
Integrating unit testing into the organization
 In some places, QA engineers write code, and they can help write unit tests for the
application. That happens in conjunction with the work of the application developers
and not instead of it. Both developers and QA engineers can write unit tests.
11.5.3 Is there proof that unit testing helps?
There aren’t any specific studies on whether unit testing helps achieve better code
quality that I can point to. Most related studies talk about adopting specific agile
methods, with unit testing being just one of them. Some empirical evidence can be
gleaned from the web, of companies and colleagues having great results and never
wanting to go back to a codebase without tests. A few studies on TDD can be found at
The QA Lead here: http://mng.bz/dddo. 
11.5.4 Why is the QA department still finding bugs?
You may not have a QA department anymore, but this is still a very prevalent practice.
Either way, you’ll still be finding bugs. Please use tests at multiple levels, as described
in chapter 10, to gain confidence across many layers of your application. Unit tests
give you fast feedback and easy maintainability, but they leave some confidence
behind, which can only be gained through some levels of integration tests. 
11.5.5 We have lots of code without tests: Where do we start?
Studies conducted in the 1970s and 1980s showed that, typically, 80% of bugs are
found in 20% of the code. The trick is to find the code that has the most problems.
More often than not, any team can tell you which components are the most prob-
lematic. Start there. You can always add some metrics related to the number of bugs
per class.
Testing legacy code requires a different approach than when writing new code with
tests. See chapter 12 for more details.
Sources for the 80/20 figure
Studies that show 80% of the bugs are in 20% of the code include the following:
Albert Endres, “An analysis of errors and their causes in system programs,” IEEE
Transactions on Software Engineering 2 (June 1975), 140–49; Lee L. Gremillion,
“Determinants of program repair maintenance requirements,” Communications of the
ACM 27, no. 8 (August 1984), 826–32; Barry W. Boehm, “Industrial software metrics
top 10 list,” IEEE Software 4, no. 9 (September 1987), 84–85 (reprinted in an IEEE
newsletter and available online at http://mng.bz/rjjJ); and Shull and others, “What
we have learned about fighting defects,” Proceedings of the 8th International Sympo-
sium on Software Metrics (2002), 249–58.



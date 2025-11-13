# 11.5.5 We have lots of code without tests: Where do we start? (pp.228-229)

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


---
**Page 229**

229
Summary
11.5.6 What if we develop a combination of software and hardware?
You can use unit tests even if you develop a combination of software and hardware.
Look into the test layers mentioned in the previous chapter to make sure you cover
both software and hardware. Hardware testing usually requires the use of simulators
and emulators at various levels, but it is a common practice to have a suite of tests both
for low-level embedded and high-level code.
11.5.7 How can we know we don’t have bugs in our tests?
You need to make sure your tests fail when they should and pass when they should.
TDD is a great way to make sure you don’t forget to check those things. See chapter 1
for a short walk-through of TDD.
11.5.8 Why do I need tests if my debugger shows that my code works?
Debuggers don’t help much with multithreaded code. Also, you may be sure your
code works fine, but what about other people’s code? How do you know it works? How
do they know your code works and that they haven’t broken anything when they make
changes? Remember that coding is the first step in the life of the code. Most of its life,
the code will be in maintenance mode. You need to make sure it will tell people when
it breaks, using unit tests.
 A study held by Curtis, Krasner, and Iscoe (“A field study of the software design
process for large systems,” Communications of the ACM 31, no. 11 (November 1988),
1268–87) showed that most defects don’t come from the code itself but result from
miscommunication between people, requirements that keep changing, and a lack of
application domain knowledge. Even if you’re the world’s greatest coder, chances are
that if someone tells you to code the wrong thing, you’ll do it. When you need to
change it, you’ll be glad you have tests for everything else, to make sure you don’t
break it.
11.5.9 What about TDD?
TDD is a style choice. I personally see a lot of value in TDD, and many people find it
productive and beneficial, but others find that writing tests after the code is good
enough for them. You can make your own choice.
Summary
Implementing unit testing in their organization is something that many readers
of this book will have to face at one time or another.
Make sure that you don’t alienate the people who can help you. Recognize
champions and blockers inside the organization. Make both groups part of the
change process.



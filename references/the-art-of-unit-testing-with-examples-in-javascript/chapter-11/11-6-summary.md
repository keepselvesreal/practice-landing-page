# 11.6 Summary (pp.229-231)

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


---
**Page 230**

230
CHAPTER 11
Integrating unit testing into the organization
Identify possible starting points. Start with a small team or project with a limited
scope to get a quick win and minimize project duration risks.
Make the progress visible to everyone. Aim for specific goals, metrics, and KPIs.
Take note of potential causes of failure, such as the lack of a driving force and
lack of political or team support.
Be prepared to have good answers to the questions you’re likely to be asked. 


---
**Page 231**

231
Working with legacy code
I once consulted for a large development shop that produced billing software.
They had over 10,000 developers and mixed .NET, Java, and C++ in products, sub-
products, and intertwined projects. The software had existed in one form or
another for over five years, and most of the developers were tasked with maintain-
ing and building on top of existing functionality. 
 My job was to help several divisions (using all languages) learn TDD techniques.
For about 90% of the developers I worked with, this never became a reality for sev-
eral reasons, some of which were a result of legacy code:
It was difficult to write tests against existing code.
It was next to impossible to refactor the existing code (or there wasn’t
enough time to do it).
Some people didn’t want to change their designs.
Tooling (or a lack of tooling) was getting in the way.
It was difficult to determine where to begin.
This chapter covers
Examining common problems with legacy code
Deciding where to begin writing tests



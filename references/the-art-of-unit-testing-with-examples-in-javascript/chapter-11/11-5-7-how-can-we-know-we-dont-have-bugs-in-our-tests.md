# 11.5.7 How can we know we don’t have bugs in our tests? (pp.229-229)

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



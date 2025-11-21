# 11.6 What’s next? (pp.280-281)

---
**Page 280**

280
CHAPTER 11
Wrapping up the book
11.6
What’s next?
There is still much to learn about software testing! This book did not have space to
cover these important topics:
Non-functional testing—If you have non-functional requirements such as perfor-
mance, scalability, or security, you may want to write tests for them as well. A
2022 book by Gayathri Mohan, Full Stack Testing (https://learning.oreilly.com/
library/view/full-stack-testing/9781098108120) has good coverage of these
type of tests.
Testing for specific architectures and contexts—As you saw in chapter 9, different
technologies may require different testing patterns. If you are building an API,
it is wise to write API tests for it. If you are building a VueJS application, it is wise
to write VueJS tests. Manning has several interesting books on the topic, includ-
ing Testing Web APIs by Mark Winteringham (www.manning.com/books/testing
-web-apis); Exploring Testing Java Microservices, with chapters selected by Alex
Soto Bueno and Jason Porter (www.manning.com/books/exploring-testing
-java-microservices), and Testing Vue.js Applications by Edd Yerburgh (www.manning
.com/books/testing-vue-js-applications).
Design for testability principles for your programming language—I mostly discussed
principles that make sense for object-oriented languages in general. If you are
working with, for example, functional languages, the principles may be some-
what different. If we pick Clojure as an example, Phil Calçado has a nice blog
post on his experiences with TDD in that language (http://mng.bz/g40x), and
Manning’s book Clojure in Action (www.manning.com/books/clojure-in-action
-second-edition) by Amit Rathore and Francis Avila has an entire chapter dedi-
cated to TDD.
Static analysis tools—Tools such as SonarQube (www.sonarqube.org) and Spot-
Bugs (https://spotbugs.github.io/) are interesting ways to look for quality
issues in code bases. These tools mostly rely on static analysis and look for spe-
cific buggy code patterns. Their main advantage is that they are very fast and
can be executed in continuous integration. I strongly suggest that you become
familiar with these tools.
Software monitoring—I said you should invest in monitoring, which means you
also need to learn how to do proper monitoring. Techniques such as A/B test-
ing, blue-green deployment, and others will help you ensure that bugs have a
harder time getting to production even if they made it through your thor-
ough testing process. The blog post “QA in Production” by Rouan Wilsenach
is a good introduction to the subject (https://martinfowler.com/articles/qa-in
-production.html).
Have fun testing!


---
**Page 281**

281
appendix
Answers to exercises
Chapter 1
1.1 The goal of systematic testing, as its name says, is to engineer test cases in a
more systematic way, rather than simply following gut feelings. Systematic testing
gives engineers sound techniques to engineer test cases out of requirements,
boundaries, and source code.
1.2 The absence-of-errors fallacy. While the software does not have many bugs, it does
not give users what they want. In this case, the verification is good, but the develop-
ers need to work on the validation.
1.3 B. Exhaustive testing is impossible in most cases.
1.4 D. Test early is an important principle, but it is definitely not related to the
problem of only doing unit tests. All the other principles can help developers
understand that using different types of testing is important.
1.5 A. The pesticide paradox fits the discussion best. The development team has
high code coverage, but they need to apply different techniques.
1.6 A. The primary use of integration tests is to find mistakes in the communication
between a system and its external dependencies.
1.7 A.
1.8 A.
1.9 B.



# 11.5 Invest in monitoring (pp.279-280)

---
**Page 279**

279
Invest in monitoring
class LegacyClass {
  public void complexMethod() {
    // ...
    // lots of code here...
    // ...
    new BeautifullyDesignedClass().cleanMethod();  
    // ...
    // lots of code here...
    // ...
  }
}
class BeautifullyDesignedClass {
  public void cleanMethod() {  
    // ...
    // lots of code here...
    // ...
  }
}
You may, of course, need to do things differently for your specific case, but the idea
is the same. For more information on handling legacy systems, I suggest Feather’s
book (2004). I also suggest reading about the anti-corruption layer idea proposed by
Evans (2004). 
11.5
Invest in monitoring
You do your best to catch all the bugs before we deploy. But in practice, you know that
is impossible. What can you do? Make sure that you detect the bugs as soon as they
happen in production.
 Software monitoring is as important as testing. Be sure your team invests in decent
monitoring systems. This is more complicated than you may think. First, developers need
to know what to log. This may be a tricky decision, as you do not want to log too much (to
avoid overloading your infrastructure), and you do not want to log too little (because you
will not have enough information to debug the problem). Make sure your team has good
guidelines for what should be logged, what log level to use, and so on. If you are curious,
we wrote a paper showing that machine learning can recommend logs to developers
(Cândido et al., 2021). We hope to have more concrete tooling in the future.
 It is also difficult for developers to identify anomalies when the system logs mil-
lions or even billions of log lines each month. Sometimes exceptions happen, and the
software is resilient enough to know what to do with them. Developers log these
exceptions anyway, but often the exceptions are not important. Therefore, investing
in ways to identify exceptions that matter is a pragmatic challenge, and you and your
team should invest in it. 
Listing 11.1
Handling legacy code
In the legacy class, 
we call the behavior 
that is now in the 
new class.
This class is also 
complex, but it is 
testable.


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



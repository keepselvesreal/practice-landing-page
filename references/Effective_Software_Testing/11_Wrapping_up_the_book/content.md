Line 1: 
Line 2: --- 페이지 304 ---
Line 3: 276
Line 4: Wrapping up the book
Line 5: We are now at the end of this book. The book comprises a lot of my knowledge
Line 6: about practical software testing, and I hope you now understand the testing tech-
Line 7: niques that have supported me throughout the years. In this chapter, I will say some
Line 8: final words about how I see effective testing in practice and reinforce points that I
Line 9: feel should be uppermost in your mind.
Line 10: 11.1
Line 11: Although the model looks linear, iterations 
Line 12: are fundamental
Line 13: Figure 11.1 (which you saw for the first time back in chapter 1) illustrates what I
Line 14: call effective software testing. Although this figure and the order of the chapters in this
Line 15: book may give you a sense of linearity (that is, you first do specification-based test-
Line 16: ing and then move on to structural testing), this is not the case. You should not
Line 17: view the proposed flow as a sort of testing waterfall.
Line 18:  Software development is an iterative process. You may start with specification-
Line 19: based testing, then go to structural testing, and then feel you need to go back to
Line 20: specification-based testing. Or you may begin with structural testing because the
Line 21: This chapter covers
Line 22: Revisiting what was discussed in this book
Line 23: 
Line 24: --- 페이지 305 ---
Line 25: 277
Line 26: Bug-free software development: Reality or myth?
Line 27: tests that emerged from your TDD sessions are good enough. There is nothing wrong
Line 28: with customizing the process to specific cases.
Line 29:  As you become more experienced with testing, you will develop a feeling for the
Line 30: best order in which to apply the techniques. As long as you master them all and
Line 31: understand the goals and outputs of each, that will come naturally. 
Line 32: 11.2
Line 33: Bug-free software development: Reality or myth?
Line 34: The techniques explore the source code from many different perspectives. That may
Line 35: give you the impression that if you apply them all, no bugs will ever happen. Unfortu-
Line 36: nately, this is not the case.
Line 37:  The more you test your code from different angles, the greater the chances of
Line 38: revealing bugs you did not see previously. But the software systems we work with today
Line 39: are very complex, and bugs may happen in corner cases that involve dozens of differ-
Line 40: ent components working together. Domain knowledge may help you see such cases.
Line 41: So, deeply understanding the business behind the software systems you test is funda-
Line 42: mental in foreseeing complex interactions between systems that may lead to crashes
Line 43: or bugs.
Line 44: Developer
Line 45: Builds a
Line 46: feature
Line 47: T
Line 48: o guide
Line 49: e
Line 50: esting t
Line 51: d velopment
Line 52: Requirement
Line 53: analysis
Line 54: Test-driven
Line 55: development
Line 56: Design for
Line 57: testability
Line 58: Design by
Line 59: contracts
Line 60: Eﬀective and systematic testing
Line 61: Speciﬁcation
Line 62: testing
Line 63: Bound
Line 64: y
Line 65: ar
Line 66: testing
Line 67: Structural
Line 68: testing
Line 69: Intelligent testing
Line 70: Mutation
Line 71: testing
Line 72: Larger tests
Line 73: Integration
Line 74: testing
Line 75: System
Line 76: testing
Line 77: Unit w h d
Line 78: s
Line 79: it
Line 80: iﬀerent roles
Line 81: and
Line 82: iliti
Line 83: responsib
Line 84: es
Line 85: Unit testing
Line 86: Property-
Line 87: based testing
Line 88: Here, we discussed ideas
Line 89: that will help us in
Line 90: implementing the feature
Line 91: with conﬁdence and with
Line 92: testability in mind.
Line 93: Here, we discussed different techniques
Line 94: that will exercise our implementation
Line 95: from many different angles and help us
Line 96: to identify possible bugs in our code.
Line 97: Mocks,
Line 98: stubs, and
Line 99: fakes
Line 100: Automated test
Line 101: suite
Line 102: T
Line 103: ode
Line 104: est c
Line 105: quality
Line 106: Figure 11.1
Line 107: Flow of a developer who applies effective and systematic testing. The arrows indicate the 
Line 108: iterative nature of the process; we may go back and forth between techniques as we learn more about the 
Line 109: program under development and test.
Line 110: 
Line 111: --- 페이지 306 ---
Line 112: 278
Line 113: CHAPTER 11
Line 114: Wrapping up the book
Line 115:  I am betting all my chips on intelligent testing. I do not talk much about it in this
Line 116: book, although it appears in figure 11.1. Intelligent testing is all about having comput-
Line 117: ers explore software systems for us. In this book, we automated the process of test exe-
Line 118: cution. Test case engineering—that is, thinking of good tests—was a human activity.
Line 119: Intelligent testing systems propose test cases for us.
Line 120:  The idea is no longer novel among academics. There are many interesting intelli-
Line 121: gent testing techniques, some of which are mature enough to be deployed into pro-
Line 122: duction. Facebook, for example, has deployed Sapienz, a tool that uses search-based
Line 123: algorithms that automatically explore mobile apps, looking for crashes. And Google
Line 124: deploys fuzz testing (generating unexpected inputs to programs to see if they crash)
Line 125: on a large scale to identify bugs in open source systems. And the beauty of the
Line 126: research is that these tools are not randomly generating input data: they are getting
Line 127: smarter and smarter.
Line 128:  If you want to play with automated test case generation, try EvoSuite for Java
Line 129: (www.evosuite.org). EvoSuite receives a class as input and produces a set of JUnit tests
Line 130: that often achieve 100% branch coverage. It is awe-inspiring. I am hoping the big soft-
Line 131: ware development companies of this world will catch up with this idea and build more
Line 132: production-ready tools. 
Line 133: 11.3
Line 134: Involve your final user
Line 135: This book focuses on verification. Verification ensures that the code works as we
Line 136: expect. Another angle to consider is validation: whether the software does what the
Line 137: user wants or needs. Delivering software that brings the most value is as essential as
Line 138: delivering software that works. Be sure you have mechanisms to ensure that you are
Line 139: building the right software in your pipeline. 
Line 140: 11.4
Line 141: Unit testing is hard in practice
Line 142: I have a clear position regarding unit testing versus integration testing: you should do
Line 143: as much unit testing as possible and leave integration testing for the parts of the sys-
Line 144: tem that need it. For that to happen, you need code that is easily tested and designed
Line 145: with testability in mind. However, most readers of this book are not in such a situation.
Line 146: Software systems are rarely designed this way.
Line 147:  When you write new pieces of code that you have more control over, be sure you
Line 148: code in a unit-testable way. This means integrating the new code with hard-to-test
Line 149: legacy code. I have a very simple suggestion that works in most cases. Imagine that
Line 150: you need to add new behavior to a legacy class. Instead of coding the behavior in
Line 151: this class, create a new class, put the new behavior in it, and unit-test it. Then, in the
Line 152: legacy class, instantiate the new class and call the method. This way, you avoid the
Line 153: hassle of writing a test for a class that is impossible to test. The following listing
Line 154: shows an example.
Line 155:  
Line 156:  
Line 157: 
Line 158: --- 페이지 307 ---
Line 159: 279
Line 160: Invest in monitoring
Line 161: class LegacyClass {
Line 162:   public void complexMethod() {
Line 163:     // ...
Line 164:     // lots of code here...
Line 165:     // ...
Line 166:     new BeautifullyDesignedClass().cleanMethod();  
Line 167:     // ...
Line 168:     // lots of code here...
Line 169:     // ...
Line 170:   }
Line 171: }
Line 172: class BeautifullyDesignedClass {
Line 173:   public void cleanMethod() {  
Line 174:     // ...
Line 175:     // lots of code here...
Line 176:     // ...
Line 177:   }
Line 178: }
Line 179: You may, of course, need to do things differently for your specific case, but the idea
Line 180: is the same. For more information on handling legacy systems, I suggest Feather’s
Line 181: book (2004). I also suggest reading about the anti-corruption layer idea proposed by
Line 182: Evans (2004). 
Line 183: 11.5
Line 184: Invest in monitoring
Line 185: You do your best to catch all the bugs before we deploy. But in practice, you know that
Line 186: is impossible. What can you do? Make sure that you detect the bugs as soon as they
Line 187: happen in production.
Line 188:  Software monitoring is as important as testing. Be sure your team invests in decent
Line 189: monitoring systems. This is more complicated than you may think. First, developers need
Line 190: to know what to log. This may be a tricky decision, as you do not want to log too much (to
Line 191: avoid overloading your infrastructure), and you do not want to log too little (because you
Line 192: will not have enough information to debug the problem). Make sure your team has good
Line 193: guidelines for what should be logged, what log level to use, and so on. If you are curious,
Line 194: we wrote a paper showing that machine learning can recommend logs to developers
Line 195: (Cândido et al., 2021). We hope to have more concrete tooling in the future.
Line 196:  It is also difficult for developers to identify anomalies when the system logs mil-
Line 197: lions or even billions of log lines each month. Sometimes exceptions happen, and the
Line 198: software is resilient enough to know what to do with them. Developers log these
Line 199: exceptions anyway, but often the exceptions are not important. Therefore, investing
Line 200: in ways to identify exceptions that matter is a pragmatic challenge, and you and your
Line 201: team should invest in it. 
Line 202: Listing 11.1
Line 203: Handling legacy code
Line 204: In the legacy class, 
Line 205: we call the behavior 
Line 206: that is now in the 
Line 207: new class.
Line 208: This class is also 
Line 209: complex, but it is 
Line 210: testable.
Line 211: 
Line 212: --- 페이지 308 ---
Line 213: 280
Line 214: CHAPTER 11
Line 215: Wrapping up the book
Line 216: 11.6
Line 217: What’s next?
Line 218: There is still much to learn about software testing! This book did not have space to
Line 219: cover these important topics:
Line 220: Non-functional testing—If you have non-functional requirements such as perfor-
Line 221: mance, scalability, or security, you may want to write tests for them as well. A
Line 222: 2022 book by Gayathri Mohan, Full Stack Testing (https://learning.oreilly.com/
Line 223: library/view/full-stack-testing/9781098108120) has good coverage of these
Line 224: type of tests.
Line 225: Testing for specific architectures and contexts—As you saw in chapter 9, different
Line 226: technologies may require different testing patterns. If you are building an API,
Line 227: it is wise to write API tests for it. If you are building a VueJS application, it is wise
Line 228: to write VueJS tests. Manning has several interesting books on the topic, includ-
Line 229: ing Testing Web APIs by Mark Winteringham (www.manning.com/books/testing
Line 230: -web-apis); Exploring Testing Java Microservices, with chapters selected by Alex
Line 231: Soto Bueno and Jason Porter (www.manning.com/books/exploring-testing
Line 232: -java-microservices), and Testing Vue.js Applications by Edd Yerburgh (www.manning
Line 233: .com/books/testing-vue-js-applications).
Line 234: Design for testability principles for your programming language—I mostly discussed
Line 235: principles that make sense for object-oriented languages in general. If you are
Line 236: working with, for example, functional languages, the principles may be some-
Line 237: what different. If we pick Clojure as an example, Phil Calçado has a nice blog
Line 238: post on his experiences with TDD in that language (http://mng.bz/g40x), and
Line 239: Manning’s book Clojure in Action (www.manning.com/books/clojure-in-action
Line 240: -second-edition) by Amit Rathore and Francis Avila has an entire chapter dedi-
Line 241: cated to TDD.
Line 242: Static analysis tools—Tools such as SonarQube (www.sonarqube.org) and Spot-
Line 243: Bugs (https://spotbugs.github.io/) are interesting ways to look for quality
Line 244: issues in code bases. These tools mostly rely on static analysis and look for spe-
Line 245: cific buggy code patterns. Their main advantage is that they are very fast and
Line 246: can be executed in continuous integration. I strongly suggest that you become
Line 247: familiar with these tools.
Line 248: Software monitoring—I said you should invest in monitoring, which means you
Line 249: also need to learn how to do proper monitoring. Techniques such as A/B test-
Line 250: ing, blue-green deployment, and others will help you ensure that bugs have a
Line 251: harder time getting to production even if they made it through your thor-
Line 252: ough testing process. The blog post “QA in Production” by Rouan Wilsenach
Line 253: is a good introduction to the subject (https://martinfowler.com/articles/qa-in
Line 254: -production.html).
Line 255: Have fun testing!
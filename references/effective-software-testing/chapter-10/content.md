# Test code quality (pp.258-276)

---
**Page 258**

258
Test code quality
You have probably noticed that once test infected, the number of JUnit tests a soft-
ware development team writes and maintains can become significant. In practice,
test code bases grow quickly. Moreover, we have observed that Lehman’s law of evo-
lution, “Code tends to rot, unless one actively works against it” (1980), also applies
to test code. A 2018 literature review by Garousi and Küçük shows that our body of
knowledge about things that can go wrong with test code is already comprehensive.
 As with production code, we must put extra effort into writing high-quality test code
bases so they can be maintained and developed sustainably. In this chapter, I discuss two
opposite perspectives of writing test code. First, we examine what constitutes good
and maintainable test code, and best practices that can help you keep complexity
under control. Then we look at what constitutes problematic test code. We focus on
key test smells that hinder test code comprehension and evolution.
 I have discussed some of this material informally in previous chapters. This
chapter consolidates that knowledge.
This chapter covers
Principles and best practices of good and 
maintainable test code
Avoiding test smells that hinder the 
comprehension and evolution of test code


---
**Page 259**

259
Principles of maintainable test code
10.1
Principles of maintainable test code
What does good test code look like? There is a great deal of literature about test code
quality, which I rely on in this section. Much of what I say here can be found in the
works of Langr, Hunt, and Thomas (2015); Meszaros (2007); and Beck (2019)—as
always, with my own twist.
10.1.1
Tests should be fast
Tests are a developer’s safety net. Whenever we perform maintenance or evolution in
source code, we use the feedback from the test suite to understand whether the system
is working as expected. The faster we get feedback from the test code, the better.
Slower test suites force us to run the tests less often, making them less effective. There-
fore, good tests are fast. There is no hard line that separates slow from fast tests. You
should apply common sense.
 If you are facing a slow test, consider the following:
Using mocks or stubs to replace slower components that are part of the test
Redesigning the production code so slower pieces of code can be tested sepa-
rately from fast pieces of code
Moving slower tests to a different test suite that you can run less often
Sometimes you cannot avoid slow tests. Think of SQL tests: they are much slower than
unit tests, but there is not much you can do about it. I separate slow tests from fast
ones: this way, I can run my fast tests all the time and the slow tests when I modify the
production code that has a slow test tied to it. I also run the slow tests before commit-
ting my code and in continuous integration. 
10.1.2
Tests should be cohesive, independent, and isolated
Tests should be as cohesive, independent, and isolated as possible. Ideally, a single test
method should test a single functionality or behavior of the system. Fat tests (or, as the
test smells community calls them, eager tests) exercise multiple functionalities and are
often complex in terms of implementation. Complex test code reduces our ability to
understand what is being tested at a glance and makes future maintenance more diffi-
cult. If you face such a test, break it into multiple smaller tests. Simpler and shorter
tests are better.
 Moreover, tests should not depend on other tests to succeed. The test result should
be the same whether the test is executed in isolation or together with the rest of the
test suite. It is not uncommon to see cases where test B only works if test A is executed
first. This is often the case when test B relies on the work of test A to set up the envi-
ronment for it. Such tests become highly unreliable.
 If you have a test that is somewhat dependent on another test, refactor the test
suite so each test is responsible for setting up the whole environment it needs.
Another tip that helps make tests independent is to make sure your tests clean up
their messes: for example, by deleting any files they created on the disk and cleaning


---
**Page 260**

260
CHAPTER 10
Test code quality
up values they inserted into a database. This will force tests to set up things themselves
and not rely on data that was already there. 
10.1.3
Tests should have a reason to exist
You want tests that either help you find bugs or help you document behavior. You do
not want tests that, for example, increase code coverage. If a test does not have a good
reason to exist, it should not exist. Remember that you must maintain all your tests.
The perfect test suite is one that can detect all the bugs with the minimum number of
tests. While having such a perfect test suite is impossible, making sure you do not have
useless tests is a good start. 
10.1.4
Tests should be repeatable and not flaky
A repeatable test gives the same result no matter how many times it is executed. Devel-
opers lose their trust in tests that present flaky behavior (sometimes pass and some-
times fail, without any changes in the system or test code).
 Flaky tests hurt the productivity of software development teams. It is hard to know
whether a flaky test is failing because the behavior is buggy or because it is flaky. Little
by little, flaky tests can make us lose confidence in our test suites. Such lack of confi-
dence may lead us to deploy our systems even though the tests fail (they may be bro-
ken because of flakiness, not because the system is misbehaving).
 The prevalence and impact of flaky tests in the software development world have
increased over time (or, at least, we talk more about them now). Companies like
Google and Facebook have publicly talked about problems caused by flaky tests.
 A test can become flaky for many reasons:
Because it depends on external or shared resources—If a test depends on a database,
many things can cause flakiness. For example, the database may not be available
at the moment the test is executed, it may contain data that the test does not
expect, or two developers may be running the test suite at the same time and
sharing the same database, causing one to break the test of the other.
Due to improper time-outs—This is a common reason in web testing. Suppose a test
has to wait for something to happen in the system: for example, a request com-
ing back from a web service, which is then displayed in an HTML element. If
the web application is slower than normal, the test may fail because it did not
wait long enough.
Because of a hidden interaction between different test methods—Test A somehow influ-
ences the result of test B, possibly causing it to fail.
The work of Luo et al. (2014) also shed light on the causes of flaky tests. After analyz-
ing 201 flaky tests in open source systems, the authors noticed the following:
Async wait, concurrency, and test order dependency are the three most com-
mon causes of flakiness.
Most flaky tests are flaky from the time they are written.


---
**Page 261**

261
Principles of maintainable test code
Flaky tests are rarely due to the platform-specifics (they do not fail because of
different operating systems).
Flakiness is often due to dependencies on external resources and can be fixed
by cleaning the shared state between test runs.
Detecting the cause of a flaky test is challenging. Software engineering researchers
have proposed automated tools to detect flaky tests. If you are curious about such
tools and the current state of the art, I suggest that you read the following:
The work of Bell et al. (2018), who proposed DeFlaker, a tool that monitors the
coverage of the latest code changes and marks a test as flaky if any new failing
test did not exercise any of the changed code.
The work of Lam et al. (2019), who proposed iDFlakies, a tool that executes
tests in random order, looking for flakiness.
Because these tools are not fully ready, it is up to us to find the flaky tests and fix them.
Meszaros has made a decision table that may help you with that task. You can find it in
his book (2007) or on his website (http://xunitpatterns.com/Erratic%20Test.html). 
10.1.5
Tests should have strong assertions
Tests exist to assert that the exercised code behaved as expected. Writing good asser-
tions is therefore key to a good test. An extreme example of a test with bad assertions
is one with no assertions. This seems strange, but believe it or not, it happens—not
because we do not know what we are doing, but because writing a good assertion can
be tricky. In cases where observing the outcome of behavior is not easily achievable, I
suggest refactoring the class or method under test to increase its observability. Revisit
chapter 7 if you need tips for how to do so.
 Assertions should be as strong as possible. You want your tests to fully validate the
behavior and break if there is any slight change in the output. Imagine that a method
calculateFinalPrice() in a ShoppingCart class changes two properties: finalPrice
and the taxPaid. If your tests only ensure the value of the finalPrice property, a bug
may happen in the way taxPaid is set, and your tests will not notice it. Make sure you
are asserting everything that needs to be asserted. 
10.1.6
Tests should break if the behavior changes
Tests let you know that you broke the expected behavior. If you break the behavior
and the test suite is still green, something is wrong with your tests. That may hap-
pen because of weak assertions (which we have discussed) or because the method is
covered but not tested (this happens, as discussed in chapter 9). Also recall that I
mentioned the work of Vera-Pérez and colleagues (2019) and the existence of
pseudo-tested methods.
 Whenever you write a test, make sure it will break if the behavior changes. The
TDD cycle allows developers to always see the test breaking. That happens because
the behavior is not yet implemented, but I like the idea of “let’s see if the test breaks


---
**Page 262**

262
CHAPTER 10
Test code quality
if the behavior does not exist or is incorrect.” I am not afraid of purposefully intro-
ducing a bug in the code, running the tests, and seeing them red (and then revert-
ing the bug). 
10.1.7
Tests should have a single and clear reason to fail
We love tests that fail. They indicate problems in our code, usually long before the
code is deployed. But the test failure is the first step toward understanding and fixing
the bug. Your test code should help you understand what caused the bug.
 There are many ways you can do that. If your test follows the earlier principles, the
test is cohesive and exercises only one (hopefully small) behavior of the software sys-
tem. Give your test a name that indicates its intention and the behavior it exercises.
Make sure anyone can understand the input values passed to the method under test.
If the input values are complex, use good variable names that explain what they are
about and code comments in natural language. Finally, make sure the assertions are
clear, and explain why a value is expected. 
10.1.8
Tests should be easy to write
There should be no friction when it comes to writing tests. If it is hard to do so (per-
haps writing an integration test requires you to set up the database, create complex
objects one by one, and so on), it is too easy for you to give up and not do it.
 Writing unit tests tends to be easy most of the time, but it may get complicated
when the class under test requires too much setup or depends on too many other
classes. Integration and system tests also require each test to set up and tear down the
(external) infrastructure.
 Make sure tests are always easy to write. Give developers all the tools to do that. If
tests require a database to be set up, provide developers with an API that requires one
or two method calls and voilà—the database is ready for tests.
 Investing time in writing good test infrastructure is fundamental and pays off in
the long term. Remember the test base classes we created to facilitate SQL integra-
tion tests and all the POs we created to facilitate web testing in chapter 9? This is the
type of infrastructure I am talking about. After the test infrastructure was in place,
the rest was easy. 
10.1.9
Tests should be easy to read
I touched on this point when I said that tests should have a clear reason to fail. I will
reinforce it now. Your test code base will grow significantly. But you probably will not
read it until there is a bug or you add another test to the suite.
 It is well known that developers spend more time reading than writing code. There-
fore, saving reading time will make you more productive. All the things you know about
code readability and use in your production code apply to test code, as well. Do not be
afraid to invest some time in refactoring it. The next developer will thank you.


---
**Page 263**

263
Principles of maintainable test code
 I follow two practices when making my tests readable: make sure all the informa-
tion (especially the inputs and assertions) is clear enough, and use test data builders
whenever I build complex data structures.
 Let’s illustrate these two ideas with an example. The following listing shows an
Invoice class.
public class Invoice {
  private final double value;
  private final String country;
  private final CustomerType customerType;
  public Invoice(double value, String country, CustomerType customerType) {
    this.value = value;
    this.country = country;
    this.customerType = customerType;
  }
  public double calculate() { 
    double ratio = 0.1;
    // some business rule here to calculate the ratio
    // depending on the value, company/person, country ...
    return value * ratio;
  }
}
Not-very-clear test code for the calculate() method could look like the next listing.
@Test
void test1() {
  Invoice invoice = new Invoice(new BigDecimal("2500"), "NL",
  ➥ CustomerType.COMPANY);
  double v = invoice.calculate();
  assertThat(v).isEqualTo(250);
}
At first glance, it may be hard to understand what all the information in the code
means. It may require some extra effort to see what this invoice looks like. Imagine an
entity class from a real enterprise system: an Invoice class may have dozens of attri-
butes. The name of the test and the name of the cryptic variable v do not clearly
explain what they mean. It is also not clear if the choice of “NL” as a country or
“COMPANY” as a customer type makes any difference for the test or whether they are
random values.
Listing 10.1
Invoice class
Listing 10.2
A not-very-clear test for an invoice
The method we will soon test. 
Imagine business rule here.


---
**Page 264**

264
CHAPTER 10
Test code quality
 A better version of this test method could be as follows.
@Test
void taxesForCompanies() {
  Invoice invoice = new InvoiceBuilder()
      .asCompany()
      .withCountry("NL")
      .withAValueOf(2500.0)
      .build(); 
  double calculatedValue = invoice.calculate(); 
  assertThat(calculatedValue) 
    .isEqualTo(250.0); // 2500 * 0.1 = 250
}
First, the name of the test method—taxesForCompanies—clearly expresses what
behavior the method is exercising. This is a best practice: name your test method after
what it tests. Why? Because a good method name may save developers from having to
read the method’s body to understand what is being tested. In practice, it is common
to skim the test suite, looking for a specific test or learning more about that class.
Meaningful test names help. Some developers would argue for an even more detailed
method name, such as taxesForCompanyAreTaxRateMultipliedByAmount. A devel-
oper skimming the test suite can understand even the business rule.
 Many of the methods we tested in previous chapters, while complex, had a single
responsibility: for example, substringsBetween in chapter 2, or leftPad in chapter 3.
We even created single parameterized tests with a generic name. We did not need a set
of test methods with nice names, as the name of the method under test said it all. But
in enterprise systems, where we have business-like methods such as calculateTaxes
or calculateFinalPrice, each test method (or partition) covers a different business
rule. Those can be expressed in the name of that test method.
 Next, using InvoiceBuilder (the implementation of which I show shortly)
clearly expresses what this invoice is about: it is an invoice for a company (as clearly
stated by the asCompany() method), “NL” is the country of that invoice, and the
invoice has a value of 2500. The result of the behavior goes to a variable whose name
says it all (calculatedValue). The assertion contains a comment that explains
where the 250 comes from.
 InvoiceBuilder is an example of an implementation of a test data builder (as defined
by Pryce [2007]). The builder helps us create test scenarios by providing a clear and
expressive API. The use of fluent interfaces (such as asCompany().withAValueOf()…) is
also a common implementation choice. In terms of its implementation, Invoice-
Builder is a Java class. The trick that allows methods to be chained is to return the
class in the methods (methods return this), as shown in the following listing.
 
Listing 10.3
A more readable version of the test
The Invoice object is 
now built through a 
fluent builder.
The variable that holds the 
result has a better name.
The assertion has a comment to 
explain where the 250 comes from.


---
**Page 265**

265
Principles of maintainable test code
public class InvoiceBuilder {
  private String country = "NL"; 
  private CustomerType customerType = CustomerType.PERSON;
  private double value = 500;
  public InvoiceBuilder withCountry(String country) { 
    this.country = country;
    return this;
  }
  public InvoiceBuilder asCompany() {
    this.customerType = CustomerType.COMPANY;
    return this;
  }
  public InvoiceBuilder withAValueOf(double value) {
    this.value = value;
    return this;
  }
  public Invoice build() { 
    return new Invoice(value, country, customerType);
  }
}
You should feel free to customize your builders. A common trick is to make the builder
build a common version of the class without requiring the call to all the setup methods.
You can then, in one line, build a complex invoice, as you see in the next listing.
var invoice = new InvoiceBuilder().build();
In such a case, the build method (without any setup) will always build an invoice for a
person with a value of 500.0 and “NL” as the country (see the initialized values in
InvoiceBuilder).
 Other developers may write shortcut methods that build other common fixtures
for the class. In listing 10.6, the anyCompany() method returns an Invoice that belongs
to a company (and the default value for the other fields). The fromTheUS() method
builds an Invoice for someone in the U.S.
public Invoice anyCompany() {
  return new Invoice(value, country, CustomerType.COMPANY);
}
Listing 10.4
Invoice test data builder
Listing 10.5
Building an invoice with a single line
Listing 10.6
Other helper methods in the builder
The builder contains predefined values allowing 
the user to only set the values they need to 
customize for the current test.
The builder contains 
many methods that 
let the test change a 
specific value (such 
as the country).
Once the required Invoice 
is set up, the builder builds 
an instance of it.


---
**Page 266**

266
CHAPTER 10
Test code quality
public Invoice fromTheUS() {
  return new Invoice(value, "US", customerType);
}
Building complex test data is such a recurrent task that frameworks are available to
help, such as Java Faker (https://github.com/DiUS/java-faker) for the Java world and
factory_bot (https://github.com/thoughtbot/factory_bot) for Ruby. I am sure you
can find one for your programming language.
 Finally, you may have noticed the comment near the assertion: 2500 * 0.1 = 250.
Some developers would suggest that the need for this comment indicates the code
requires improvement. To remove the comment, we can introduce explanatory vari-
ables: in listing 10.7, we use the invoiceValue and tax variables in the assertion. It is
up to you and your team members to agree on the best approach for you.
@Test
void taxesForCompanyAreTaxRateMultipliedByAmount() {
  double invoiceValue = 2500.0; 
  double tax = 0.1;
  Invoice invoice = new InvoiceBuilder()
      .asCompany()
      .withCountry("NL")
      .withAValueOf(invoiceValue) 
      .build();
  double calculatedValue = invoice.calculate();
  assertThat(calculatedValue)
    .isEqualTo(invoiceValue * tax); 
}
To sum up, introducing test data builders, using variable names to explain the mean-
ing of information, having clear assertions, and adding comments where code is not
expressive enough will help developers better comprehend the test code. 
10.1.10 Tests should be easy to change and evolve
Although we like to think that we always design stable classes with single responsibili-
ties that are closed for modification but open for extension (see Martin [2014] for
more about the Open Closed Principle), in practice, that does not always happen.
Your production code will change, and that will force your tests to change as well.
 Therefore, your task when implementing test code is to ensure that changing it
will not be too painful. I do not think it is possible to make it completely painless, but
you can reduce the number of points that will require changes. For example, if you
see the same snippet of code in 10 different test methods, consider extracting it. If a
Listing 10.7
Making the test more readable via explanatory variables
Declares the 
invoiceValue and 
tax variables
Uses the variable instead 
of the hard-coded value
The assertion uses the 
explanatory variables instead 
of hard-coded numbers.


---
**Page 267**

267
Test smells
change happens and you are forced to change that code snippet, you now only have
to change it in 1 place rather than 10.
 Your tests are coupled to the production code in one way or another. That is a fact.
The more your tests know about how the production code works, the harder it is to
change them. As we discussed in chapter 6, a clear disadvantage of using mocks is the
significant coupling with the production code. Determining how much your tests
need to know about the production code to test it properly is a significant challenge. 
10.2
Test smells
In the previous sections, we discussed some best practices for writing good test code.
Now let’s discuss test smells. The term code smell indicates symptoms that may indicate
deeper problems in the system’s source code. Some well-known examples are Long
Method, Long Class, and God Class. Several research papers show that code smells hin-
der the comprehensibility and maintainability of software systems (such as the work by
Khomh and colleagues [2009]).
 While the term has long been applied to production code, our community has
been developing catalogs of smells that are specific to test code. Research has also
shown that test smells are prevalent in real life and, unsurprisingly, often hurt the
maintenance and comprehensibility of the test suite (Spadini et al., 2020).
 The following sections examine several well-known test smells. A more compre-
hensive list can be found in xUnit Test Patterns by Meszaros (2007). I also recommend
reading the foundational paper on test smells by Deursen and colleagues (2001).
10.2.1
Excessive duplication
It is not surprising that code duplication can happen in test code since it is widespread
in production code. Tests are often similar in structure, as you may have noticed in
several of the code examples in this book. We even used parameterized tests to reduce
duplication. A less attentive developer may end up writing duplicate code (copy-pasting
often happens in real life, as Treude, Zaidman, and I observed in an empirical study
[2021]) instead of putting some effort into implementing a better solution.
 Duplicated code can reduce the productivity of software developers. If we need to
change a duplicated piece of code, we must apply the same change in all the places
where the code is duplicated. In practice, it is easy to forget one of these places and end
up with problematic test code. Duplicating code may also hinder the ability to evolve the
test suite, as mentioned earlier. If the production code changes, you do not want to have
to change too much test code. Isolating duplicated code reduces this pain.
 I advise you to refactor your test code often. Extracting duplicate code to private
methods or external classes is often a good, quick, cheap solution to the problem. But
being pragmatic is key: a little duplication may not harm you, and you should use your
experience to judge when refactoring is needed. 


---
**Page 268**

268
CHAPTER 10
Test code quality
10.2.2
Unclear assertions
Assertions are the first thing a developer looks at when a test fails. A good assertion
clearly reveals its reason for failure, is legible, and is as specific as possible. The test smell
emerges when it is hard to understand the assertions or the reason for their failure.
 There are several reasons for this smell to happen. Some features or business rules are
so complex that they require a complex set of assertions to ensure their behavior. In
these situations, we end up writing complex assert instructions that are not easy to under-
stand. To help with such cases, I recommend writing customized assert instructions that
abstract away part of the complexity of the assertion code, and writing code comments
that explain quickly and in natural language what those assertions are about. The latter
mainly applies when the assertions are not self-explanatory. Do not be afraid to write a
comment in your code if it will help future developers understand what is going on.
 Interestingly, a common best practice in the test best practice literature is the “one
assertion per method” strategy. The idea is that a test with a single assertion can only
focus on a single behavior, and it is easier for developers to understand if the assertion
fails. I strongly disagree with this rule. If my test is cohesive enough and focuses on a
single feature, the assertions should ensure that the entire behavior is as expected.
This may mean asserting that many fields were updated and have a new value. It may
also mean asserting that the mock interacted with other dependencies properly.
There are many cases in which using multiple assertions in a single test is useful. Forc-
ing developers to have a single assertion per test method is extreme—but your tests
also should not have useless assertions.
 Frameworks often offer the possibility of doing soft assertions: assertions that do
not stop the test if they fail but are reported only at the very end of the test execu-
tion (which is still considered a failed test). For example, AssertJ offers this ability
(http://mng.bz/aDeo).
 Finally, even if you know what to assert for, picking the right assertion method pro-
vided by whatever test framework you are using can make a difference. Using the
wrong or not ideal assert instruction may lead to imprecise assertion error messages. I
strongly suggest using AssertJ and its extensive collection of assertions. 
10.2.3
Bad handling of complex or external resources
Understanding test code that uses external resources can be difficult. The test should
ensure that the resource is readily available and prepared for it. The test should also
clean up its mess afterward.
 A common smell is to be optimistic about the external resource. Resource optimism
happens when a test assumes that a necessary resource (such as a database) is readily
available at the start of its execution. The problem is that when the resource is not avail-
able, the test fails, often without a clear message that explains the reason. This can con-
fuse developers, who may think a new bug has been introduced in the system.
 To avoid such resource optimism, a test should not assume that the resource is
already in the correct state. The test should be responsible for setting up the state


---
**Page 269**

269
Test smells
itself. This can mean the test is responsible for populating a database, writing the
required files to the disk, or starting up a Tomcat server. This setup may require com-
plex code, and you should also make your best effort to abstract away such complexity
by, for example, moving such code to other classes (like DatabaseInitialization or
TomcatLoader) and allowing the test code to focus on the test cases.
 Another common test smell happens when the test assumes that the resource is
available all the time. Imagine a test method that interacts with a web service, which
may be down for reasons we do not control. To avoid this test smell, you have two
options: avoid depending on external resources by using stubs and mocks or, if the
test cannot avoid using the external dependency, make the test suite robust enough.
For example, make your test suite skip that test when the resource is unavailable, and
provide an alert explaining why that was the case. This may seem counterintuitive, but
remember that developers trust their test suites. Having a single test fail for the wrong
reasons can make you lose confidence in the entire test suite.
 From a readability perspective, it should be easy to understand all the (external)
resources required and used by the test. Imagine that a test requires a test file in some
directory. If the file is not there, the test fails. A first-time developer may have difficulty
understanding this prerequisite. Avoid having such mystery guests in your test suite.
The test code should be explicit about all its external dependencies.  
10.2.4
Fixtures that are too general
A fixture is the set of input values used to exercise the component under test. As you
may have noticed, fixtures are the stars of the test method, as they derive naturally
from the test cases we engineer using any of the techniques we have discussed.
 When testing more complex components, you may need to build several different
fixtures: one for each partition you want to exercise. These fixtures can then become
complex. And to make the situation worse, while tests are different from each other,
their fixtures may intersect. Given this possible intersection among the different fix-
tures, as well as the difficulty with building complex entities and fixtures, you may
decide to declare a large fixture that works for many different tests. Each test would
then use a small part of this large fixture.
 While this approach may work, and the tests may correctly implement the test
cases, they quickly become hard to maintain. Once a test fails, you will find yourself
with a large fixture that may not be completely relevant for that particular failing test.
You then must manually filter out parts of the fixture that are not exercised by the fail-
ing test. That is an unnecessary cost.
 Making sure the fixture of a test is as specific and cohesive as possible helps you com-
prehend the essence of a test (which is, again, highly relevant when the test starts to fail).
Build patterns (focusing on building test data) can help you avoid generic fixtures. More
specifically, the Test Data Builder pattern we discussed is often used in the test code of
enterprise applications. Such applications often deal with creating complex sets of inter-
related business entities, which can easily lead developers to write general fixtures. 


---
**Page 270**

270
CHAPTER 10
Test code quality
10.2.5
Sensitive assertions
Good assertions are fundamental in test cases. A bad assertion may result in a test not
failing when it should. However, a bad assertion may also cause a test to fail when it
should not. Engineering a good assertion statement is challenging—even more so when
components produce fragile outputs (outputs that change often). Test code should be
as resilient as possible to the implementation details of the component under test.
Assertions also should not be oversensitive to internal changes.
 In the tool we use to assess students’ submissions (https://github.com/cse1110/
andy), we have a class responsible for transforming the assessment results into a message
(string) that we show in our cloud-based IDE. The following listing shows the output for
one of our exercises.
--- Compilation 
Success
--- JUnit execution 
7/7 passed
--- JaCoCo coverage 
Line coverage: 13/13
Instruction coverage: 46/46
Branch coverage: 12/12 
--- Mutation testing     
10/10 killed
--- Code checks 
No code checks to be assessed
--- Meta tests 
13/13 passed
Meta test: always finds clumps (weight: 1) PASSED
Meta test: always returns zero (weight: 1) PASSED
Meta test: checks in pairs (weight: 1) PASSED
Meta test: does not support more than two per clump (weight: 1) PASSED
Meta test: does not support multiple clumps (weight: 1) PASSED
Meta test: no empty check (weight: 1) PASSED
Meta test: no null check (weight: 1) PASSED
Meta test: only checks first two elements (weight: 1) PASSED
Meta test: only checks last two elements (weight: 1) PASSED
Meta test: skips elements after clump (weight: 1) PASSED
Meta test: skips first element (weight: 1) PASSED
Meta test: skips last element (weight: 1) PASSED
Meta test: wrong result for one element (weight: 1) PASSED 
--- Assessment
Branch coverage: 12/12 (overall weight=0.10)
Mutation coverage: 10/10 (overall weight=0.10)
Listing 10.8
An example of the output of our tool
The result of the compilation
How many tests passed
Coverage information
Mutation testing 
information
Static code checks (in this 
case, none were executed)
The student’s final grade
The student’s 
final grade


---
**Page 271**

271
Test smells
Code checks: 0/0 (overall weight=0.00)
Meta tests: 13/13 (overall weight=0.80)
Final grade: 100/100
If we write tests without thinking too much, we end up writing lots of assertions that
check whether some string is in the output. And given that we will write many test
cases for many different outputs, our test suite will end up with lots of statements like
“assert output contains Final grade: 100/100”.
 Note how sensitive this assertion is. If we change the message slightly, the tests will all
break. Making assertions that are less sensitive to small changes is usually a good idea.
 In this situation, we have no other option than to assert that the string matches
what we have. To sort this out, we decided to create our own set of assertions for each
part of the message we need to assert. These assertions enable us to decouple our test
code from the strings themselves. And if the message changes in the future, all we will
need to do is change our assertion.
 In listing 10.9, the reportCompilationError test method ensures that we show the
proper message to the student when they submit a solution that does not compile. We
create a Result object (representing the final assessment of the student solution) with
a compilation error. We then call the method under test and get back the generated
string message.
@Test
void reportCompilationError() {
  Result result = new ResultTestDataBuilder()
    .withCompilationFail(
      new CompilationErrorInfo(
        ➥ "Library.java", 10, "some compilation error"),
      new CompilationErrorInfo(
        ➥ "Library.java", 11, "some other compilation error")
  ).build(); 
  writer.write(ctx, result); 
  String output = generatedResult();
  assertThat(output) 
    .has(noFinalGrade())
    .has(not(compilationSuccess()))
    .has(compilationFailure())
    .has(compilationErrorOnLine(10))
    .has(compilationErrorOnLine(11))
    .has(compilationErrorType("some compilation error"))
    .has(compilationErrorType("some other compilation error"));
}
Listing 10.9
A test that uses our own assertions
Creates a 
Result in 
which we tell 
the student 
that there is a 
compilation 
error in their 
solution
Calls the method 
under test and gets 
the generated message
Asserts that the message is as we expect. 
Note, however, our set of assertions: 
noFinalGrade, compilationSuccess, and 
so on. They decouple our test from the 
concrete string.


---
**Page 272**

272
CHAPTER 10
Test code quality
The trick happens in the assertions. Note the many assertions we created: noFinal-
Grade() ensures that the final grade is not displayed, compilationErrorOnLine(10)
ensures that we tell the student there is a compilation error on line 10, and so on. To
create these assertions, we use AssertJ’s extension capabilities. All we need to do is cre-
ate a method that returns AssertJ’s Condition<?> class. The generic type should be
the same as the type of the object on which we are performing the assertion. In this
case, the output variable is a string, so we need to create a Condition<String>.
 The implementation of the compilationErrorOnLine assertion is shown in listing
10.10. If a compilation error happens, we print "- line <number>: <error message>".
This assertion then looks for "- line <number>" in the string.
public static Condition<String> compilationErrorOnLine(int lineNumber) { 
  return new Condition<>() {
    @Override
    public boolean matches(String value) {
      return value.contains("- line " + lineNumber); 
    }
  };
}
Back to the big picture: make sure your assertions are not too sensitive, or your tests
may break for no good reason. 
Exercises
10.1
Jeanette hears that two tests are behaving strangely. Both of them pass when
executed in isolation, but they fail when executed together.
Which one of the following is not the cause of this problem?
A The tests depend on the same external resources.
B The execution order of the tests matters.
C Both tests are very slow.
D They do not perform a cleanup operation after execution.
10.2
Look at the following test code. What is the most likely test code smell that this
piece of code presents?
@Test
void test1() {
  // web service that communicates with the bank
  BankWebService bank = new BankWebService();
  User user = new User("d.bergkamp", "nl123");
  bank.authenticate(user);
  Thread.sleep(5000); // sleep for 5 seconds
  double balance = bank.getBalance();
  Thread.sleep(2000);
Listing 10.10
compilationErrorOnLine assertion
Makes the method
static, so we can
statically import it
in the test class
Checks whether value contains
the string we are looking for


---
**Page 273**

273
Exercises
  Payment bill = new Payment();
  bill.setOrigin(user);
  bill.setValue(150.0);
  bill.setDescription("Energy bill");
  bill.setCode("YHG45LT");
  bank.pay(bill);
  Thread.sleep(5000);
  double newBalance = bank.getBalance();
  Thread.sleep(2000);
  // new balance should be previous balance - 150
  Assertions.assertEquals(newBalance, balance - 150);
}
A Flaky test
B Test code duplication
C Obscure test
D Long method
10.3
RepoDriller is a project that extracts information from Git repositories. Its inte-
gration tests use a lot of real Git repositories (that are created solely for the
test), each with a different characteristic: one repository contains a merge com-
mit, another contains a revert operation, and so on.
Its tests look like this:
@Test
public void test01() {
  // arrange: specific repo
  String path = "test-repos/git-4";
  // act
  TestVisitor visitor = new TestVisitor();
  new RepositoryMining()
    .in(GitRepository.singleProject(path))
    .through(Commits.all())
    .process(visitor)
    .mine();
  // assert
  Assert.assertEquals(3, visitor.getVisitedHashes().size());
  Assert.assertTrue(visitor.getVisitedHashes().get(2).equals("b8c2"));
  Assert.assertTrue(visitor.getVisitedHashes().get(1).equals("375d"));
  Assert.assertTrue(visitor.getVisitedHashes().get(0).equals("a1b6"));
}
Which test smell might this piece of code suffer from?
A Condition logic in the test
B General fixture


---
**Page 274**

274
CHAPTER 10
Test code quality
C Flaky test
D Mystery guest
10.4
In the following code, we show an actual test from Apache Commons Lang, a
very popular open source Java library. This test focuses on the static random()
method, which is responsible for generating random characters. An interesting
detail in this test is the comment Will fail randomly about 1 in 1000 times.
/**
 * Test homogeneity of random strings generated --
 * i.e., test that characters show up with expected frequencies
 * in generated strings.  Will fail randomly about 1 in 1000 times.
 * Repeated failures indicate a problem.
 */
@Test
public void testRandomStringUtilsHomog() {
  final String set = "abc";
  final char[] chars = set.toCharArray();
  String gen = "";
  final int[] counts = {0, 0, 0};
  final int[] expected = {200, 200, 200};
  for (int i = 0; i < 100; i++) {
    gen = RandomStringUtils.random(6,chars);
    for (int j = 0; j < 6; j++) {
      switch (gen.charAt(j)) {
        case 'a': {counts[0]++; break;}
        case 'b': {counts[1]++; break;}
        case 'c': {counts[2]++; break;}
        default: {fail("generated character not in set");}
      }
    }
  }
  // Perform chi-square test with df = 3-1 = 2, testing at .001 level
  assertTrue("test homogeneity -- will fail about 1 in 1000 times",
    chiSquare(expected,counts) < 13.82);
}
Which one of the following statements is incorrect about the test?
A The test is flaky because of the randomness that exists in generating
characters.
B The test checks for invalidly generated characters and also checks that
characters are picked in the same proportion.
C The method being static has nothing to do with its flakiness.
D To avoid flakiness, a developer should have mocked the random() function.
10.5
A developer observes that two tests pass when executed in isolation but fail
when executed together.
Which of the following is the least likely fix for this problem (also known as
Test Run War)?


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



# 10.1.10 Tests should be easy to change and evolve (pp.266-267)

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



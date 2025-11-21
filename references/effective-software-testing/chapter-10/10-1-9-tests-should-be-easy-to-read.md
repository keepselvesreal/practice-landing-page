# 10.1.9 Tests should be easy to read (pp.262-266)

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



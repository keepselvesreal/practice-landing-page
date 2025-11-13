# 9.3.3 Patterns and best practices (pp.251-254)

---
**Page 251**

251
System tests
If you run the test again, it will fail. The list of owners will return four people instead
of two, as the test expects—we are running our entire web application, and data is per-
sisted in the database. We need to make sure we can reset the web application when-
ever we run a test, and we discuss that in the next section. 
9.3.3
Patterns and best practices
You probably noticed that the amount of code required to get our first system test
working was much greater than in previous chapters. In this section, I introduce some
patterns and best practices that will help you write maintainable web tests. These pat-
terns come from my own experience after writing many such tests. Together with
Guerra and Gerosa, I proposed some of these patterns at the PLoP conference in
2014.
PROVIDE A WAY TO SET THE SYSTEM TO THE STATE THAT THE WEB TEST REQUIRES
To ensure that the Find Owners journey worked properly, we needed some owners in
the database. We added them by repeatedly navigating to the Add Owner page, filling
in the form, and saving it. This strategy works fine in simple cases. However, imagine a
more complicated scenario where your test requires 10 different entities in the data-
base. Visiting 10 different web pages in a specific order is too much work (and also
slow, since the test would take a considerable amount of time to visit all the pages).
 In such cases, I suggest creating all the required data before running the test. But
how do you do that if the web application runs standalone and has its own database?
You can provide web services (say, REST web services) that are easily accessible by the
test. This way, whenever you need some data in the application, you can get it through
simple requests. Imagine that instead of visiting the pages, we call the API. From the
test side, we implement classes that abstract away all the complexity of calling a
remote web service. The following listing shows how the previous test would look if it
consumed a web service.
@Test
void findOwnersBasedOnTheirLastNames() {
  AddOwnerInfo owner1 = new AddOwnerInfo(
    ➥ "John", "Doe", "some address", "some city", "11111");
  AddOwnerInfo owner2 = new AddOwnerInfo(
    ➥ "Jane", "Doe", "some address", "some city", "11111");
  AddOwnerInfo owner3 = new AddOwnerInfo(
    ➥ "Sally", "Smith", "some address", "some city", "11111");
  OwnersAPI api = new OwnersAPI();  
  api.add(owner1);
  api.add(owner2);
  api.add(owner3);
  page.visit();
  ListOfOwnersPage listPage = page.findOwners("Doe");
  List<OwnerInfo> all = listPage.all();
Listing 9.32
Our test if we had a web service to add owners
Calls the API. We no longer need to visit 
the Add Owner page. The OwnersAPI 
class hides the complexity of calling 
a web service.


---
**Page 252**

252
CHAPTER 9
Writing larger tests
  assertThat(all).hasSize(2).
      containsExactlyInAnyOrder(owner1.toOwnerInfo(), owner2.toOwnerInfo());
}
Creating simple REST web services is easy today, given the full support of the web
frameworks. In Spring MVC (or Ruby, or Django, or Asp.Net Core), you can write one
in a couple of lines. The same thing happens from the client side. Calling a REST web
service is simple, and you don’t have to write much code.
 You may be thinking of security issues. What if you do not want the web services in
production? If they are only for testing purposes, your software should hide the API
when in production and allow the API only in the testing environment.
 Moreover, do not be afraid to write different functionalities for these APIs, if doing
so makes the testing process easier. If your web page needs a combination of Products,
Invoices, Baskets, and Items, perhaps you can devise a web service solely to help the
test build up complex data. 
MAKE SURE EACH TEST ALWAYS RUNS IN A CLEAN ENVIRONMENT
Similar to what we did earlier when testing SQL queries, we must make sure our tests
always run in a clean version of the web application. Otherwise, the test may fail for
reasons other than a bug. This means databases (and any other dependencies) must
only contain the bare minimum amount of data for the test to start.
 We can reset the web application the same way we provide data to it: via web ser-
vices. The application could provide an easy backdoor that resets it. It goes without
saying that such a web service should never be deployed in production.
 Resetting the web application often means resetting the database. You can imple-
ment that in many different ways, such as truncating all the tables or dropping and re-
creating them.
WARNING
Be very careful. The reset backdoor is nice for tests, but if it is
deployed into production, chaos may result. If you use this solution, make
sure it is only available in the test environment!
GIVE MEANINGFUL NAMES TO YOUR HTML ELEMENTS
Locating elements is a vital part of a web test, and we do that by, for example,
searching for their name, class, tag, or XPath. In one of our examples, we first
searched for the form the element was in and then found the element by its tag. But
user interfaces change frequently during the life of a website. That is why web test
suites are often highly unstable. We do not want a change in the presentation of a
web page (such as moving a button from the left menu to the right menu) to break
the test.
 Therefore, I suggest assigning proper (unique) names and IDs to elements that
will play a role in the test. Even if the element does not need an ID, giving it one will
simplify the test and make sure the test will not break if the presentation of the ele-
ment changes.


---
**Page 253**

253
System tests
 If for some reason an element has a very unstable ID (perhaps it is dynamically
generated), we need to create any specific property for the testing. HTML5 allows us
to create extra attributes on HTML tags, like the following example.
<input type="text"
id="customer_\${i}"
name="customer"
data-selenium="customer-name" />    
If you think this extra property may be a problem in the production environment,
remove it during deployment. There are many tools that manipulate HTML pages
before deploying them (minification is an example).
NOTE
Before applying this pattern to the project, you may want to talk to
your team’s frontend lead. 
VISIT EVERY STEP OF A JOURNEY ONLY WHEN THAT JOURNEY IS UNDER TEST
Unlike unit testing, building up scenarios on a system test can be complicated. We saw
that some journeys may require the test to navigate through many different pages
before getting to the page it wants to test.
 Imagine a specific page A that requires the test to visit pages B, C, D, E, and F
before it can finally get to A and test it. A test for that page is shown here.
@Test
void longest() {
  BPage b = new BPage();    
  b.action1(..);
  b.action2(..);
  CPage c = new CPage();   
  c.action1(..);
  DPage d = new DPage();   
  d.action1(..);
  d.action2(..);
  EPage e = new EPage();
  e.action1(..);
  FPage e = new FPage();
  f.action1(..);
  // finally!!
  APage a = new APage();
  a.action1();
  assertThat(a.confirmationAppears()).isTrue();
}
Listing 9.33
HTML element with a property that makes it easy to find
Listing 9.34
A very long test that calls many POs
It is easy to find the HTML element 
that has a data-selenium attribute 
with customer-name as its value.
Calls the 
first PO
Calls a 
second PO
Calls a third 
PO, and so on


---
**Page 254**

254
CHAPTER 9
Writing larger tests
Note how long and complex the test is. We discussed a similar problem, and our
solution was to provide a web service that enabled us to skip many of the page visits.
But if visiting all these pages is part of the journey under test, the test should visit
each one. If one or two of these steps are not part of the journey, you can use the
web services. 
ASSERTIONS SHOULD USE DATA THAT COMES FROM THE POS
In the Find Owners test, our assertions focused on checking whether all the owners
were on the list. In the code, the FindOwnersPage PO provided an all() method that
returned the owners. The test code was only responsible for the assertion. This is a
good practice. Whenever your tests require information from the page for the asser-
tion, the PO provides this information. Your JUnit test should not locate HTML ele-
ments by itself. However, the assertions stay in the JUnit test code. 
PASS IMPORTANT CONFIGURATIONS TO THE TEST SUITE
The example test suite has some hard-coded details, such as the local URL of the
application (right now, it is localhost:8080) and the browser to run the tests (currently
Safari). However, you may need to change these configurations dynamically. For
example, your continuous integration may need to run the web app on a different
port, or you may want to run your test suite on Chrome.
 There are many different ways to pass configuration to Java tests, but I usually opt
for the simplest approach: everything that is a configuration is provided by a method
in  my PageObject base class. For example, a String baseUrl() method returns the
base URL of the application, and a WebDriver browser() method returns the con-
crete instance of WebDriver. These methods then read from a configuration file or an
environment variable, as those are easy to pass via build scripts. 
RUN YOUR TESTS IN MULTIPLE BROWSERS
You should run your tests in multiple browsers to be sure everything works every-
where. But I don’t do this on my machine, because it takes too much time. Instead, my
continuous integration (CI) tool has a multiple-stage process that runs the web test
suite multiple times, each time passing a different browser. If configuring such a CI is
an issue, consider using a service such as SauceLabs (https://saucelabs.com), which
automates this process for you. 
9.4
Final notes on larger tests
I close this chapter with some points I have not yet mentioned regarding larger tests.
9.4.1
How do all the testing techniques fit?
In the early chapters of this book, our goal was to explore techniques that would help
you engineer test cases systematically. In this chapter, we discuss a more orthogonal
topic: how large should our tests be? I have shown you examples of larger component
tests, integration tests, and system tests. But regardless of the test level, engineering
good test cases should still be the focus.



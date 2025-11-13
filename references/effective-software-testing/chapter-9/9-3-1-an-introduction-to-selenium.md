# 9.3.1 An introduction to Selenium (pp.239-242)

---
**Page 239**

239
System tests
CONSIDER (OR DON’T) AN IN-MEMORY DATABASE
You should decide whether your tests will communicate with a real database (the same
type of database as in your production environment) or a simpler database (such as
an in-memory database). As always, both sides have advantages and disadvantages.
Using the same database as in production makes your tests more realistic: your tests
will exercise the same SQL engine that will be exercised in production. On the other
hand, running full-blown MySQL is much more expensive, computationally speaking,
than a simple in-memory database. All in all, I favor using real databases when I am
writing SQL integration tests. 
9.3
System tests
At some point, your classes, business rules, persistence layers, and so on are combined
to form, for example, a web application. Let’s think about how a web application tradi-
tionally works. Users visit a web page (that is, their browser makes a request to the
server, and the server processes the request and returns a response that the browser
shows) and interact with the elements on the page. These interactions often trigger
other requests and responses. Considering a pet clinic application: a user goes to the
web page that lists all the scheduled appointments for today, clicks the New Appoint-
ment button, fills out the name of their pet and its owner, and selects an available time
slot. The web page then takes the user back to the Appointments page, which now
shows the newly added appointment.
 If this pet clinic web application was developed using test-driven approaches and
everything we discussed in the previous chapters of this book, the developer already
wrote (systematic) unit tests for each unit in the software. For example, the Appointment
class already has unit tests of its own.
 In this section, we discuss what to test in a web application and what tools we can
use to automatically open the browser and interact with the web page. We also discuss
some best practices for writing system tests.
NOTE
Although I use a web application as an example of how to write a sys-
tem test, the ideas in this section apply to any other type of software system.
9.3.1
An introduction to Selenium
Before diving into the best practices, let’s get familiar with the mechanics of writing such
tests. For that, we will rely on Selenium. The Selenium framework (www.selenium.dev)
is a well-known tool that supports developers in testing web applications. Selenium
can connect to any browser and control it. Then, through the Selenium API, we can
give commands such as “open this URL,” “find this HTML element in the page and
get its inner text,” and “click that button.” We will use commands like these to test our
web applications.
 We use the Spring PetClinic web application (https://projects.spring.io/spring
-petclinic) as an example throughout this section. If you are a Java web developer,
you are probably familiar with Spring Boot. For those who are not, Spring Boot is


---
**Page 240**

240
CHAPTER 9
Writing larger tests
the state-of-the-art framework for web development in Java. Spring PetClinic is a sim-
ple web application that illustrates how powerful and easy to use Spring Boot is. Its
code base contains the two lines required for you to download (via Git) and run (via
Maven) the web application. Once you do, you should be able to visit your local-
host:8080 and see the web application, shown in figures 9.3 and 9.4.
Figure 9.3
First screenshot of the Spring PetClinic application
Figure 9.4
Second screenshot of the Spring PetClinic application


---
**Page 241**

241
System tests
Before discussing testing techniques and best practices, let’s get started with Sele-
nium. The Selenium API is intuitive and easy to use. The following listing shows our
first test.
public class FirstSeleniumTest {
  @Test
  void firstSeleniumTest() {
    WebDriver browser = new SafariDriver();   
    browser.get("http:/ /localhost:8080");   
    WebElement welcomeHeader = browser.findElement(By.tagName("h2"));   
    assertThat(welcomeHeader.getText())
      .isEqualTo("Welcome");  
    browser.close();   
  }
}
Let’s go line by line:
1
The first line, WebDriver browser = new SafariDriver(), instantiates a Safari
browser. WebDriver is the abstraction that all other browsers implement. If you
would like to try a different browser, you can use new FirefoxBrowser() or new
ChromeBrowser() instead. I am using Safari for two reasons:
a
I am a Mac user, and Safari is often my browser of choice.
b
Other browsers, such as Chrome, may require you to download an external
application that enables Safari to communicate with it. In the case of Chrome,
you need to download ChromeDriver (https://chromedriver.chromium.org/
downloads).
2
With an instantiated browser, we visit a URL by means of browser.get("url");.
Whatever URL we pass, the browser will visit. Remember that Selenium is not
simulating the browser: it is using the real browser.
3
The test visits the home page of the Spring PetClinic web app (figure 9.3). This
website is very simple and shows a brief message (“Welcome”) and a cute pic-
ture of a dog and a cat. To ensure that we can extract data from the page we are
visiting, let’s ensure that the “Welcome” message is on the screen. To do that,
we first must locate the element that contains the message. Knowledge of
HTML and DOM is required here.
If you inspect the HTML of the Spring PetClinic, you see that the message is
within an h2 tag. Later, we discuss the best ways to locate elements on the page;
but for now, we locate the only h2 element. To do so, we use Selenium’s find-
Element() function, which receives a strategy that Selenium will use to find the
Listing 9.24
Our first Selenium test
Selects a driver. The 
driver indicates which 
browser to use.
Visits a page at 
the given URL
Finds an HTML
element in the page
Asserts that the 
page contains 
what we want
Closes the browser and 
the selenium session


---
**Page 242**

242
CHAPTER 9
Writing larger tests
element. We can find elements by their names, IDs, CSS classes, and tag name.
By.tagName("h2") returns a WebElement, an abstraction representing an ele-
ment on the web page.
4
We extract some properties of this element: in particular, the text inside the h2
tag. For that, we call the getText() method. Because we expect it to return
“Welcome”, we write an assertion the same way we are used to. Remember, this
is an automated test. If the web element does not contain “Welcome”, the test
will fail.
5
We close the browser. This is an important step, as it disconnects Selenium
from the browser. It is always a good practice to close any resources you use in
your tests.
If you run the test, you should see Safari (or your browser of choice) open, be auto-
matically controlled by Selenium, and then close. This will get more exciting when we
start to fill out forms. 
9.3.2
Designing page objects
For web applications and system testing, we do not want to exercise just one unit of
the system but the entire system. We want to do what we called system testing in chap-
ter 1. What should we test in a web application, with all the components working
together and an infinite number of different paths to test?
 Following what we discussed in the testing pyramid, all the units of the web appli-
cation are at this point (we hope) already tested at the unit or integration level. The
entities in the Spring PetClinic, such as Owner or Pet, have been unit-tested, and all
the queries that may exist in DAOs have also been tested via integration tests similar to
what we just did.
 But if everything has already been tested, what is left for us to test? We can test the
different user journeys via web testing. Here is Fowler’s definition of a user journey test
(2003): “User-journey tests are a form of business-facing test, designed to simulate a
typical user’s journey through the system. Such a test will typically cover a user’s entire
interaction with the system to achieve some goal. They act as one path in a use case.”
 Think of possible user journeys in the Spring PetClinic application. One possible
journey is the user trying to find owners. Other possible journeys include the user
adding a new owner, adding a pet to the owner, or adding a log entry of the pet after
the pet visits the veterinarian.
 Let’s test one journey: the find owners journey. We will code this test using a Page
Object pattern. Page objects (POs) help us write more maintainable and readable web
tests. The idea of the Page Object pattern is to define a class that encapsulates all the
(Selenium) logic involved in manipulating one page.
 For example, if the application has a List of Owners page that shows all the owners,
we will create a ListOfOwnersPage class that will know how to handle it (such as
extracting the names of the owners from the HTML). If the application has an Add
Owner page, we will create an AddOwnerPage class that will know how to handle it



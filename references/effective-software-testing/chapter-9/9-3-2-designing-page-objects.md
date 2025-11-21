# 9.3.2 Designing page objects (pp.242-251)

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


---
**Page 243**

243
System tests
(such as filling out the form with the name of the new owner and clicking the button
that saves it). Later, we will put all these POs together in a JUnit test, simulate the
whole journey, and assert that it went as expected.
 When I write Selenium web tests, I prefer to start by designing my POs. Let’s begin
by modeling the first page of this journey: the Find Owners page. This page is shown
in figure 9.5, and the page can be accessed by clicking the Find Owners link in the menu.
This page primarily contains one interesting thing to be modeled: the “find owners”
functionality. For that to work, we need to fill in the Last Name input field and click
the Find Owners button. Let’s start with that.
public class FindOwnersPage extends PetClinicPageObject {
  public FindOwnersPage(WebDriver driver) {  
    super(driver);
  }
  public ListOfOwnersPage findOwners(String ownerLastName) {   
    driver.findElement(By.id("lastName")).sendKeys(ownerLastName);   
    WebElement findOwnerButton = driver
      .findElement(By.id("search-owner-form"))
      .findElement(By.tagName("button"));
    findOwnerButton.click();   
    ListOfOwnersPage listOfOwnersPage = new ListOfOwnersPage(driver);  
    listOfOwnersPage.isReady();   
    return listOfOwnersPage;
  }
}
Listing 9.25
FindOwners page object
We need to type the name of the owner in
this HTML ﬁeld and press the Find Owner
button for the search to happen.
Figure 9.5
The Find Owners page
The constructor of all our POs receives the Selenium 
driver. The PO needs it to manipulate the web page.
This method is
responsible for
finding an owner
on this page based
on their last name.
Finds the HTML element
whose ID is lastName and
types the last name of the
owner we are looking for.
Clicks the
Find Owner
button. We
find it on
the page by
its ID.
Takes us to another page.
To represent that, we
make the PO return the
new page, also as a PO.
Waits for the 
page to be 
ready before 
returning it


---
**Page 244**

244
CHAPTER 9
Writing larger tests
Let’s look at this code line by line:
1
The newly created class FindOwnersPage represents the Find Owners page. It
inherits from another class, PetClinicPageObject, which will serve as a com-
mon abstraction for our POs. I show its source code later.
2
Our POs always have a constructor that receives a WebDriver. Everything we do
with Selenium starts with the WebDriver class, which we will instantiate later
from a JUnit test method.
3
Methods in this PO represent actions we can take with the page we are model-
ing. The first action we modeled is findOwners(), which fills the Last Name
input with the value passed to the ownerLastName string parameter.
4
The implementation of the method is straightforward. We first locate the
HTML input element. By inspecting the Spring PetClinic web page, we see that
the field has an ID. Elements with IDs are usually easy to find, as IDs are unique
in the page. With the element in hand, we use the sendKeys() function to fill in
the input with ownerLastName. Selenium’s API is fluent, so we can chain the
method calls: findElement(…).sendKeys(…).
5
We search for the Find Owner button. When inspecting the page, we see that
this button does not have a specific ID. This means we need to find another way
to locate it on the HTML page. My first instinct is to see if this button’s HTML
form has an ID. It does: search-owner-form. We can locate the form and then
locate a button inside it (as this form has one button).
Note how we chain calls for the findElement method. Remember that
HTML elements may have other HTML elements inside them. Therefore, the
first findElement() returns the form, and the second findElement searches
only the elements inside the element returned by the first findElement. With
the button available to us, we call the click() method, which clicks the button.
The form is now submitted.
6
The website takes us to another page that shows the list of owners with the
searched last name. This is no longer the Find Owners page, so we should now
use another PO to represent the current page. That is why we make the find-
Owners() method return a ListOfOwnersPage: one page takes you to another
page.
7
Before we return the newly instantiated ListOfOwnersPage, we call an isReady()
method. This method waits for the Owners page to be ready. Remember that
this is a web application, so requests and responses may take some time. If we
try to look for an element from the page, but the element is not there yet, the
test will fail. Selenium has a set of APIs that enable us to wait for such things,
which we will see soon.
We still have more POs to model before writing the test for the entire journey. Let’s
model the Owners page, shown in figure 9.6. This page contains a table in which each
row represents one owner.


---
**Page 245**

245
System tests
Our ListOfOwnersPage PO models a single action that will be very important for our
test later: getting the list of owners in this table. The following listing shows the source
code.
public class ListOfOwnersPage extends PetClinicPageObject {
  public ListOfOwnersPage(WebDriver driver) {    
    super(driver);
  }
  @Override
  public void isReady() {   
    WebDriverWait wait = new WebDriverWait (driver, Duration.ofSeconds(3));
    wait.until(
      ExpectedConditions.visibilityOfElementLocated(
      By.id("owners")));    
  }
  public List<OwnerInfo> all() {
    List<OwnerInfo> owners = new ArrayList<>();    
    WebElement table = driver.findElement(By.id("owners"));   
    List<WebElement> rows = table.findElement(By.tagName(
      ➥ "tbody")).findElements(By.tagName("tr"));
    for (WebElement row : rows) {    
      List<WebElement> columns = row.findElements(By.tagName("td"));  
      String name = columns.get(0).getText().trim();   
      String address = columns.get(1).getText().trim();
      String city = columns.get(2).getText().trim();
      String telephone = columns.get(3).getText().trim();
      String pets = columns.get(4).getText().trim();
Listing 9.26
ListOfOwners PO
We need to get the list of
owners from this HTML table.
Figure 9.6
The Owners page
As we know, all POs receive the 
WebDriver in the constructor.
The isReady method lets us know whether the 
page is ready in the browser so we can start 
manipulating it. This is important, as some 
pages take more time than others to load.
The Owners page is considered ready when the list of 
owners is loaded. We find the table with owners by its 
ID. We wait up to three seconds for that to happen.
Creates
a list to
hold all the
owners. For
that, we
create an
OwnerInfo
class.
Gets the HTML table 
and all its rows. The 
table’s ID is owners, 
which makes it easy 
to find.
For each row in 
the table …
… gets the 
HTML row
Gets the value of each 
HTML cell. The first 
column contains the 
name, the second the 
address, and so on.


---
**Page 246**

246
CHAPTER 9
Writing larger tests
      OwnerInfo ownerInfo = new OwnerInfo(
        ➥ name, address, city, telephone, pets);    
      owners.add(ownerInfo);
    }
    return owners;   
  }
}
Let’s walk through this code:
1
Our class is a PO, so it extends from PetClinicPageObject, which forces the
class to have a constructor that receives a WebDriver. We still have not seen the
PetClinicPageObject code, but we will soon.
2
The isReady() method (which you can see by the @Override annotation is also
defined in the base class) knows when this page is loaded. How do we do this?
The simplest way is to wait a few seconds for a specific element to appear on the
page. In this case, we wait for the element with ID “owners” (the table with all
the owners) to be on the page. We tell WebDriverWait to wait up to three sec-
onds for the owners element to be visible. If the element is not there after three
seconds, the method throws an exception. Why three seconds? That was a
guess; in practice, you have to find the number that best fits your test.
3
We return to our main action: the all() method. The objective is to extract the
names of all the owners. Because this is an HTML table, we know that each row
is in a tr element. The table has a header, which we want to ignore. So, we
locate #owners > tbody > tr or, in other words, all trs inside tbody that are
inside the owners element. We do this using nested findElement() and find-
Elements() calls. Note the difference between the two methods: one returns a
single element, the other multiple elements (useful in this case, as we know
there are many trs to be returned).
4
With the list of rows ready, we iterate over each element. We know that trs are
composed of tds. We find all tds inside the current tr and extract the text
inside each td, one by one. We know the first cell contains the name, the sec-
ond cell contains the address, and so on. We then build an object to hold this
information: the OwnerInfo class. This is a simple class with getters only. We also
trim() the string to get rid of any whitespaces in the HTML.
5
We return the list of owners in the table.
Now, searching for an owner with their surname takes us to the next page, where we
can extract the list of owners. Figure 9.7 illustrates the two POs we have implemented
so far and which pages of the web application they model.
 We are only missing two things. First and foremost, to search for an owner, the
owner must be in the application. How do we add a new owner? We use the Add
Owner page. So, we need to model one more PO. Second we need a way to visit these
pages for the first time.
Once all the information 
is collected from the 
HTML, we build an 
OwnerInfo class.
Returns a list of 
OwnerInfos. This object 
knows nothing about 
the HTML page.


---
**Page 247**

247
System tests
NOTE
Much more work is required to write a test for a single journey than we
are used to when doing unit tests. System tests are naturally more expensive
to create. But I also want you to recognize that adding a new test becomes eas-
ier once you have an initial structure with POs. The high cost comes now,
when building this initial infrastructure.
Let’s start with adding an owner. The next listing shows the AddOwnerPage PO.
public class AddOwnerPage extends PetClinicPageObject {
  public AddOwnerPage(WebDriver driver) {   
    super(driver);
  }
  @Override
  public void isReady() {
    WebDriverWait wait = new WebDriverWait (driver, Duration.ofSeconds(3));
    wait.until(
      ExpectedConditions.visibilityOfElementLocated(
      By.id("add-owner-form")));     
  }
  public OwnerInformationPage add(AddOwnerInfo ownerToBeAdded) {
    driver.findElement(By.id("firstName"))
      .sendKeys(ownerToBeAdded.getFirstName());   
    driver.findElement(By.id("lastName"))
      .sendKeys(ownerToBeAdded.getLastName());
    driver.findElement(By.id("address"))
      .sendKeys(ownerToBeAdded.getAddress());
    driver.findElement(By.id("city"))
      .sendKeys(ownerToBeAdded.getCity());
    driver.findElement(By.id("telephone"))
      .sendKeys(ownerToBeAdded.getTelephone());
Listing 9.27
.AddOwnerPage page object
/findOwners
owners?lastName=x
FindOwnersPage
(Java object)
ow er
n
s()
…
ListOfOwnersPage
(Java object)
all()
…
Web pages
Page objects
Each page object represents one web page. It contains elegant
methods that know how to manipulate the page. Test methods
use these page objects to test the web application.
Figure 9.7
An illustration 
of web pages and their 
respective POs
Again, the PO 
receives the 
WebDriver.
The HTML page is 
ready when the 
form appears on 
the screen.
Fills out all the HTML form 
elements with the data 
provided in AddOwnerInfo, 
a class created for that 
purpose. We find the form 
elements by their IDs.


---
**Page 248**

248
CHAPTER 9
Writing larger tests
    driver.findElement(By.id("add-owner-form"))
        .findElement(By.tagName("button"))
        .click();     
    OwnerInformationPage ownerInformationPage =
      new OwnerInformationPage(driver);  
    ownerInformationPage.isReady();
    return ownerInformationPage;
  }
}
The implementation should not be a surprise. The isReady() method waits for the
form to be ready. The add() method, which is the relevant method here, finds the
input elements (which all have specific IDs, making our lives much easier), fills them
in, finds the Add Owner button, and returns the PO that represents the page we go to
after adding an owner: OwnerInformationPage. I do not show its code, to save space,
but it is a PO much like the others we have seen.
 Finally, all we need is a way to visit the pages. I usually have a visit() method in
my POs to take me directly to that page. Let’s add a visit() method to the POs we
need to visit: the Find Owner page and the Add Owner page.
// FindOwnersPage
public void visit() {
  visit("/owners/find");
}
// AddOwnersPage
public void visit() {
  visit("/owners/new");
}
Note that these visit() methods call another visit method in the superclass.
 Now it is time to show the PO base class. This is where we put common behavior
that all our POs have. Base classes like these support and simplify the development of
our tests.
public abstract class PetClinicPageObject {
  protected final WebDriver driver;   
  public PetClinicPageObject(WebDriver driver) {
    this.driver = driver;
  }
  public void visit() {     
    throw new RuntimeException("This page does not have a visit link");
  }
Listing 9.28
Adding visit() methods to all the POs
Listing 9.29
Initial code of the PO base class
Clicks the 
Add button
When an owner is added, the web 
application redirects us to the Owner 
Information page. The method then 
returns the PO of the class we are 
redirected to.
The base class keeps 
the reference to the 
WebDriver.
The visit method 
should be overridden 
by the child classes.


---
**Page 249**

249
System tests
  protected void visit(String url) {       
    driver.get("http:/ /localhost:8080" + url);  
    isReady();
  }
  public abstract void isReady();    
}
You can make this PO base class as complex as you need. In more involved apps, the
base class is more complex and full of helper methods. For now, we have a constructor
that receives WebDriver (forcing all POs to have the same constructor), a visit()
method that can be overridden by child POs, a helper visit() method that com-
pletes the URL with the localhost URL, and an abstract isReady() method that forces
all POs to implement this functionality.
 We now have enough POs to model our first journey. The following listing shows a
JUnit test.
public class FindOwnersFlowTest {
  protected static WebDriver driver = new SafariDriver();   
  private FindOwnersPage page = new FindOwnersPage(driver);   
  @AfterAll
  static void close() {   
    driver.close();
  }
  @Test
  void findOwnersBasedOnTheirLastNames() {
    AddOwnerInfo owner1 = new AddOwnerInfo(
      ➥ "John", "Doe", "some address", "some city", "11111");   
    AddOwnerInfo owner2 = new AddOwnerInfo(
      ➥ "Jane", "Doe", "some address", "some city", "11111");
    AddOwnerInfo owner3 = new AddOwnerInfo(
      ➥ "Sally", "Smith", "some address", "some city", "11111");
    addOwners(owner1, owner2, owner3);
    page.visit();   
    ListOfOwnersPage listPage = page.findOwners("Doe");  
    List<OwnerInfo> all = listPage.all();
    assertThat(all).hasSize(2).
        containsExactlyInAnyOrder(
        owner1.toOwnerInfo(), owner2.toOwnerInfo());  
  }
Listing 9.30
Our first journey: find owners
Provides a helper 
method for the base 
classes to help them 
visit the page
The hard-coded URL can come 
from a configuration file.
All POs are forced to implement an isReady 
method. Making methods abstract is a nice 
way to force all POs to implement their 
minimum required behavior.
Creates a concrete WebDriver, the SafariDriver.
Later, we will make this more flexible so our
tests can run in multiple browsers.
Creates the 
FindOwners PO, 
where the test 
should start
When the test suite is done, we 
close the Selenium driver. This 
method is also a good candidate 
to move to a base class.
Creates a bunch of owners to
be added. We need owners
before testing the listing page.
Visits the Find 
Owners page
Looks for all 
owners with Doe 
as their surname
Asserts that we find 
John and Jane from 
the Doe family


---
**Page 250**

250
CHAPTER 9
Writing larger tests
  private void addOwners(AddOwnerInfo... owners) {   
    AddOwnerPage addOwnerPage = new AddOwnerPage(driver);
    for (AddOwnerInfo owner : owners) {
      addOwnerPage.visit();
      addOwnerPage.add(owner);
    }
  }
}
Let’s walk through this code:
1
At the top of the class, we create a static instance of SafariDriver, which we
enclose in the @AfterAll method. To save some time (opening and closing the
browser for every test), we only need one instance of WebDriver for all the tests
in this class. For now, this means our test has the Safari browser hard-coded.
Later we will discuss how to make it more flexible so you can run your test suite
in multiple browsers.
2
The findOwnersBasedOnTheirLastNames() method contains our journey. We
create two fake AddOwnerInfos: two owners that will be added to the applica-
tion. For each owner, we visit the Add Owner page, fill in the information, and
save. (I created an addOwners() private helper method to increase the readabil-
ity of the main test method.)
3
We visit the Owners page and get all the owners in the list. We expect both
newly added owners to be there, so we assert that the list contains two items and
they are the two owners we created.
4
AddOwnerInfo, the data structure used by AddOwnerPage, is different from Owner-
Info, the data structure returned by the ListOfOwnersPage page. In one, a
name is the first name and last name together, and in the other, the first name
and last name are separate. We could use a single data structure for both or
design them separately. I chose to design them separately, so I needed to con-
vert from one to another. So, I implemented toOwnerInfo() in the AddOwner-
Info class. It is a simple method, as you see in the next listing.
public OwnerInfo toOwnerInfo() {
  return new OwnerInfo(firstName + " " + lastName, address, city, telephone, "");
}
Now, when we run the test, it looks almost like magic: the browser opens, the names of
the owners are typed in the page, buttons are clicked, pages change, the browser
closes, and JUnit shows us that the test passed. We are finished with our first web Sele-
nium test.
NOTE
A good exercise for you is to write tests for other application journeys.
This will require the development of more POs!
Listing 9.31
toOwnerInfo converter method
The addOwners 
helper method 
adds an owner 
via the Add 
Owner page.


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



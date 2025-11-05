# Using Test Doubles (pp.53-71)

---
**Page 53**

CHAPTER 3
Using Test Doubles
You can test a lot of your system using the information you’ve learned over
the prior two chapters. But not all units are going to be similarly easy to test.
It’s a safe bet you find your own system hard to test. Perhaps you think the first
two chapters made it look too easy. “It must be nice to have a system that sup-
ports writing unit tests out of the box, but it doesn’t match my reality,” says Joe.
In this chapter, you’ll learn how to employ test doubles to break dependencies
on pain-inducing collaborators. A test double is a stand-in (think “stunt
double”) for the dependencies that make your code hard to test. You’re prob-
ably already familiar with the name of one kind of test double—a mock object.
With test doubles, you gain a tool that will help you get past the ever-present
unit testing hurdle of troublesome dependencies.
A Testing Challenge
You’re testing an AddressRetriever. Given a latitude and longitude, its retrieve
method returns an appropriately populated Address object.
utj3-mock-objects/01/src/main/java/com/langrsoft/domain/AddressRetriever.java
import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.DeserializationFeature;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.langrsoft.util.HttpImpl;
public class AddressRetriever {
private static final String SERVER =
"https://nominatim.openstreetmap.org";
public Address retrieve(double latitude, double longitude) {
var locationParams =
"lon=%.6f&lat=%.6f".formatted(latitude, longitude);
var url =
"%s/reverse?%s&format=json".formatted(SERVER, locationParams);
report erratum  •  discuss


---
**Page 54**

var jsonResponse = new HttpImpl().get(url);
➤
var response = parseResponse(jsonResponse);
var address = response.address();
var country = address.country_code();
if (!country.equals("us"))
throw new UnsupportedOperationException(
"intl addresses unsupported");
return address;
}
private Response parseResponse(String jsonResponse) {
var mapper = new ObjectMapper().configure(
DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
try {
return mapper.readValue(jsonResponse, Response.class);
} catch (JsonProcessingException e) {
throw new RuntimeException(e);
}
}
}
At first glance, testing retrieve appears straightforward—it’s only about ten lines
long with one conditional and a short helper method. Then you notice code that
appears to make a live HTTP get request (highlighted in AddressRetriever). Hmm.
Sure enough, the HttpImpl class interacts with Apache’s HttpComponents client to
execute a REST call:
utj3-mock-objects/01/src/main/java/com/langrsoft/util/HttpImpl.java
import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse.BodyHandlers;
public class HttpImpl implements Http {
@Override
public String get(String url) {
try (var client = HttpClient.newHttpClient()) {
var request = HttpRequest.newBuilder().uri(URI.create(url)).build();
try {
var httpResponse = client.send(request, BodyHandlers.ofString());
return httpResponse.body();
} catch (IOException | InterruptedException e) {
throw new RuntimeException(e);
}
}
}
}
Chapter 3. Using Test Doubles • 54
report erratum  •  discuss


---
**Page 55**

The HttpImpl class implements the HTTP interface:
utj3-mock-objects/01/src/main/java/com/langrsoft/util/Http.java
public interface Http {
String get(String url);
}
You trust HttpImpl because you find an integration test for it in ./src/test/java/com
/langrsoft/util. But you also know that HttpImpl’s code interacts with an external
service over HTTP—a recipe for unit testing trouble. Any tests you write for
retrieve in AddressRetriever will ultimately trigger a live HTTP call. That carries at
least two big implications:
• The tests against the live call will be slow compared to the bulk of your
other fast tests.
• You can’t guarantee that the Nominatim HTTP API will be available or
return consistent results. It’s out of your control.
A test version of the API would give you control over availability. Your builds
and local dev environments would need to start/restart the service as
appropriate. It would also be slow in comparison (see Fast Tests, on page 66).
You want a way to focus on unit testing the rest of the logic in retrieve—the
code that preps the HTTP call and the code that handles the response—
isolated from the HTTP dependency.
Replacing Troublesome Behavior with Stubs
The challenge for testing is the code in HttpImpl that calls a real endpoint. To
fix the problem, your test can supplant HttpImpl’s live call with logic that instead
returns mocked-up data. You’ll create an implementation of HttpImpl known
as a stub: It will stub out the real code with a simplified version.
A stub is a test double that supplants real behavior with a method
that returns a hardcoded value.
HTTP is a functional interface: It contains exactly one abstract method decla-
ration (for get). As a result, you can dynamically and concisely declare an
implementation of HTTP using a lambda:
utj3-mock-objects/02/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Http http = url ->
"""
{"address":{
"house_number":"324",
report erratum  •  discuss
Replacing Troublesome Behavior with Stubs • 55


---
**Page 56**

"road":"Main St",
"city":"Anywhere",
"state":"Colorado",
"postcode":"81234",
"country_code":"us"}}
""";
The stub returns a hardcoded JSON string, backward engineered from the
parsing code in retrieve. Consider it an alternate implementation of the HTTP
interface, suitable for use only by a test.
Injecting Dependencies into Production Code
The HTTP stub gets you halfway toward being able to write your test. You
must also tell AddressRetriever to use your stub instead of a “real” HttpImpl object.
You do so using dependency injection, a fancy term for passing the stub to
an AddressRetriever instance. You can inject a stub in a few ways; here, you’ll
inject it via the constructor:
utj3-mock-objects/02/src/main/java/com/langrsoft/domain/AddressRetriever.java
public class AddressRetriever {
private static final String SERVER =
"https://nominatim.openstreetmap.org";
private final Http http;
➤
public AddressRetriever(Http http) {
➤
this.http = http;
➤
}
➤
public Address retrieve(double latitude, double longitude) {
var locationParams =
"lon=%.6f&lat=%.6f".formatted(latitude, longitude);
var url =
"%s/reverse?%s&format=json".formatted(SERVER, locationParams);
var jsonResponse = http.get(url);
➤
var response = parseResponse(jsonResponse);
// ...
}
// ...
The call to http.get(url) in retrieve (highlighted) no longer creates a private instance
of HTTP. It now dereferences the http field, which points to the stub when
executed in the context of the test you can now write.
utj3-mock-objects/02/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
import com.langrsoft.util.*;
import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;
Chapter 3. Using Test Doubles • 56
report erratum  •  discuss


---
**Page 57**

class AnAddressRetriever {
@Test
void answersAppropriateAddressForValidCoordinates() {
Http http = url ->
"""
{"address":{
"house_number":"324",
"road":"Main St",
"city":"Anywhere",
"state":"Colorado",
"postcode":"81234",
"country_code":"us"}}
""";
var retriever = new AddressRetriever(http);
var address = retriever.retrieve(38, -104);
assertEquals("324", address.house_number());
assertEquals("Main St", address.road());
assertEquals("Anywhere", address.city());
assertEquals("Colorado", address.state());
assertEquals("81234", address.postcode());
}
}
When the test runs:
• It creates an AddressRetriever, passing it the HTTP stub instance.
• When executed, the retrieve method formats a URL using parameters passed
to the method. It then calls the get method on http.
• The stub returns the JSON string you hardcoded in the test.
• The rest of the retrieve method parses the hardcoded JSON string and
populates an Address object accordingly.
• The test verifies elements of the returned Address object.
The retrieve method is oblivious to whether http references a stub or the real
implementation. In this example, the stub represents a “single use test case”
for purposes of one test. Add another test that creates a completely different
stub:
utj3-mock-objects/02/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
@Test
void throwsWhenNotUSCountryCode() {
Http http = url -> """
{"address":{ "country_code":"not us"}}""";
var retriever = new AddressRetriever(http);
report erratum  •  discuss
Replacing Troublesome Behavior with Stubs • 57


---
**Page 58**

assertThrows(UnsupportedOperationException.class,
() -> retriever.retrieve(1.0, -1.0));
}
This second test takes advantage of the fact that AddressRetriever code looks
only at country_code, throwing an exception when it is anything but the lowercase
string "us".
Changing Your Design to Support Testing
You changed the design of AddressRetriever. Before, it created an HttpImpl instance
in retrieve as a private detail. Now, a client using AddressRetriever must pass an
HTTP-derived object to its constructor (or use a dependency injection tool):
var retriever = new AddressRetriever(new HttpImpl());
Changing design to simplify testing might seem odd, but doing so lets you
write the tests that increase your confidence to ship.
You’re not limited to constructor injection; you can inject stubs in many
other ways. Some ways require no changes to the interface of your class. You
can use setters instead of constructors, you can override factory methods,
you can introduce abstract factories, and you can even use tools such as
Google Guice or Spring that do the injection somewhat magically.
Adding Smarts to Your Stub: Verifying Parameters
Your HTTP stub always returns the same hardcoded JSON string, regardless
of the latitude/longitude passed to get. That’s a small hole in testing. If the
AddressRetriever doesn’t pass the parameters properly, you have a defect.
You are not exercising the real behavior of HttpImpl (which already has
tests). You’re exercising the rest of retrieve’s code based on a return value that
HttpImpl might cough up. The only thing left to cover is verifying that retrieve
correctly interacts with HttpImpl.
As a quick stab at a solution, add a guard clause to the stub that verifies the
URL passed to the HTTP method get. If it doesn’t contain the expected
parameter string, explicitly fail the test at that point:
utj3-mock-objects/03/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
@Test
void answersAppropriateAddressForValidCoordinates() {
Http http = url -> {
if (!url.contains("lat=38") ||
➤
!url.contains("lon=-104"))
➤
fail("url " + url + " does not contain correct params");
➤
Chapter 3. Using Test Doubles • 58
report erratum  •  discuss


---
**Page 59**

return """
{"address":{
"house_number":"324",
"road":"Main St",
"city":"Anywhere",
"state":"Colorado",
"postcode":"81234",
"country_code":"us"}}
""";
};
var retriever = new AddressRetriever(http);
var address = retriever.retrieve(38, -104);
// ...
The stub has a little bit of smarts now…meaning it’s no longer a stub. It’s
closer to being a mock. A mock, like a stub, lets you provide test-specific
behavior. It can also self-verify, as in this example, by ensuring that expected
interactions with collaborators (an HTTP implementation here) occur.
The “smart stub” pays off—your test now fails. Did you spot the defect earlier?
utj3-mock-objects/03/src/main/java/com/langrsoft/domain/AddressRetriever.java
public Address retrieve(double latitude, double longitude) {
var locationParams = "lon=%.6f&lat=%.6f".formatted(latitude, longitude);
var url = "%s/reverse?%s&format=json".formatted(SERVER, locationParams);
var jsonResponse = http.get(url);
// ...
}
Fixing the problem involves swapping the two query parameter names:
utj3-mock-objects/04/src/main/java/com/langrsoft/domain/AddressRetriever.java
var locationParams = "lat=%.6f&lon=%.6f".formatted(latitude, longitude);
Using a mock, your test can verify that a method was called and
with the right arguments.
Simplifying Testing Using a Mock Tool
Hand-grown smart stubs are kind of a bad idea. A stub is a simple test con-
struct that returns a hard-coded value. Adding logic in the middle of it is a
recipe for wasted time when you get the logic wrong (you eventually will)—
which turns it into a smart-ahh…never mind.
report erratum  •  discuss
Simplifying Testing Using a Mock Tool • 59


---
**Page 60**

You’ll instead represent your stub using Mockito,
1 the de facto standard
“mock” library for Java. Using the tool will keep your tests safer and simpler
when you need test doubles. It handles the smarts, so you don’t have to.
Here’s the test updated to use Mockito:
utj3-mock-objects/05/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
// ...
import static org.mockito.ArgumentMatchers.contains;
➤
import static org.mockito.Mockito.mock;
➤
import static org.mockito.Mockito.when;
➤
class AnAddressRetriever {
Http http = mock(Http.class);
➤
@Test
void answersAppropriateAddressForValidCoordinates() {
when(http.get(contains("lat=38.000000&lon=-104.000000"))).thenReturn(
➤
"""
{"address":{
"house_number":"324",
"road":"Main St",
"city":"Anywhere",
"state":"Colorado",
"postcode":"81234",
"country_code":"us"}}
""");
var retriever = new AddressRetriever(http);
var address = retriever.retrieve(38, -104);
// ...
}
// ...
}
The field http is initialized with a call to Mockito’s static mock method, which
synthesizes an object that implements the HTTP interface. This mock object
tracks when methods are called and with what arguments.
The first statement in the test (in its arrange step) sets up an expectation on
the mock. It tells the mock object to expect that the get method might be called.
If the method is indeed called (at any point later during test execution), and
with an argument containing the substring "lat=38.000000&lon=-104.000000", the
mock object will return the specified hard-coded JSON string.
If the get method is not called, or if it’s called but doesn’t contain the expected
lat-long string, the mock object returns null. The contains method is what
1.
https://site.mockito.org
Chapter 3. Using Test Doubles • 60
report erratum  •  discuss


---
**Page 61**

Mockito refers to as matcher. More typically, you wouldn’t use a matcher like
contains, but would instead specify the exact argument expected.
The second statement in the test, as before, injects the Mockito mock into
the AddressRetriever via its constructor. Replacing your stub with Mockito doesn’t
require changing any production code.
When the retrieve method is called during the “act” step of the test, its code
interacts with the Mockito mock. If the Mockito mock’s expectations are
met—if the production code calls http.get(url) as expected, the mock returns
the hardcoded JSON string, and the test passes. If not, the test fails.
It would be better if your mock didn’t have to know the exact encoding order
of the latitude and longitude query params. Mockito lets you supply two dis-
tinct matchers using the and matcher:
utj3-mock-objects/06/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
import static org.mockito.AdditionalMatchers.and;
// ...
@Test
void answersAppropriateAddressForValidCoordinates() {
when(http.get(
and(contains("lat=38.000000"), contains("lon=-104.000000"))))
➤
.thenReturn(
// ...
}
Both contains matchers have to hold true for the test to pass.
With the happy path test for retrieve out of the way, you can update the not-
as-happy-path test, throwsWhenNotUSCountryCode, to use Mockito:
utj3-mock-objects/05/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
@Test
void throwsWhenNotUSCountryCode() {
when(http.get(anyString())).thenReturn("""
➤
{"address":{ "country_code":"not us"}}""");
➤
var retriever = new AddressRetriever(http);
assertThrows(UnsupportedOperationException.class,
() -> retriever.retrieve(1.0, -1.0));
}
Your happy path test, answersAppropriateAddressForValidCoordinates, demonstrated that
retrieve correctly formats its arguments into a query parameter string. Accord-
ingly, you don’t need to similarly worry about doing so in this second test. You
can use the Mockito matcher method anyString() to indicate that the test should
pass as long as a string object is passed to the get method.
report erratum  •  discuss
Simplifying Testing Using a Mock Tool • 61


---
**Page 62**

The when(...).thenReturn(...) pattern is one of a number of ways to set up mocks
using Mockito, but it’s probably the simplest to understand and code. It distills
the effort of setting up a mock into what’s essentially a one-liner that imme-
diately makes sense to someone reading the code.
Injecting Mocks with Mockito
Using constructor injection may require you to change your class’s interface.
A dependency injection (DI) tool like Spring DI, Google Guice, or PicoContainer
can eliminate the need for that change. You can also use Mockito, which
provides nominal built-in DI capabilities. It’s not as sophisticated as the
other two tools, but it might be all you need. To use Mockito’s DI:
• Annotate the test class with @ExtendWith(MockitoExtension.class).
• Annotate the http field with @Mock. Mockito initializes it as a mock object.
• Annotate the retriever field with @InjectMocks. Mockito creates an instance of
retriever and injects any @Mock fields into it.
utj3-mock-objects/07/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
// ...
import org.junit.jupiter.api.extension.ExtendWith;
➤
import org.mockito.Mock;
➤
import org.mockito.InjectMocks;
➤
import org.mockito.junit.jupiter.MockitoExtension;
➤
@ExtendWith(MockitoExtension.class)
➤
class AnAddressRetriever {
@InjectMocks
➤
AddressRetriever retriever;
➤
@Mock
➤
Http http;
➤
@Test
void answersAppropriateAddressForValidCoordinates() {
when(http.get(and(contains("lat=38.000000"),
contains("lon=-104.000000"))))
// ...
}
// ...
}
When injecting mock objects, Mockito first seeks an appropriate constructor—
in this case, one that takes on an HTTP instance. If it finds none, it seeks an
appropriate setter method, and then finally, a field with the matching type.
To try this feature, eliminate AddressRetriever’s constructor and initialize an http
field:
Chapter 3. Using Test Doubles • 62
report erratum  •  discuss


---
**Page 63**

utj3-mock-objects/07/src/main/java/com/langrsoft/domain/AddressRetriever.java
public class AddressRetriever {
private static final String SERVER =
"https://nominatim.openstreetmap.org";
private Http http = new HttpImpl(); // this cannot be final
➤
// look ma, no constructor!
➤
public Address retrieve(double latitude, double longitude) {
// ...
}
// ...
}
From the test, Mockito magically finds your http field and injects the mock
instance into it (overwriting what was already there)!
Production clients no longer need to pass a value for http into the AddressRetriever
since it’s initialized to the appropriate production object.
Downsides: mucking with privates violates many folks’ design sensibilities.
Also, Mockito injection is slow, adding almost a full second to the test run on
my machine. Ensure its inclusion doesn’t pig out the overall execution time
of your test suite.
Verifying a Method Was Called…or Not
As an alternative to when(...).thenReturn(...), you might want to verify that a certain
method was called with the proper arguments as part of processing. The
typical case for this need is when you’re invoking a consumer—a method that
has side effects but returns nothing. Mockito helps you verify that such a
method was called with its verify functionality.
Update the AddressRetriever to tell an Auditor instance to add audit information
when the country code returned is a non-U.S. country code:
utj3-mock-objects/08/src/main/java/com/langrsoft/domain/AddressRetriever.java
public class AddressRetriever {
private Auditor auditor = new ApplicationAuditor();
➤
// ...
public Address retrieve(double latitude, double longitude) {
// ...
var country = address.country_code();
if (!country.equals("us")) {
auditor.audit("request for country code: %s".formatted(country));
➤
throw new UnsupportedOperationException(
"intl addresses unsupported");
}
report erratum  •  discuss
Verifying a Method Was Called…or Not • 63


---
**Page 64**

return address;
}
// ...
}
For now, the audit method in ApplicationAuditor does nothing; some other team
member is coding it. You need only the interface declaration in order to write
your test:
utj3-mock-objects/08/src/main/java/com/langrsoft/domain/Auditor.java
public interface Auditor {
void audit(String message);
}
Add a test that proves audit is called for a non-U.S. country code. Use Mockito’s
verify method, which acts as an assertion. If the audit method is called with
exactly the same String argument, the test passes.
utj3-mock-objects/08/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
import static org.mockito.Mockito.verify;
➤
// ...
@Test
void auditsWhenNonUSAddressRetrieved() {
when(http.get(anyString())).thenReturn("""
{"address":{ "country_code":"not us"}}""");
assertThrows(UnsupportedOperationException.class,
() -> retriever.retrieve(1.0, -1.0));
verify(auditor).audit("request for country code: not us");
➤
}
// ...
}
Note the difference regarding parentheses placement between verify and when:
verify(someObject).method();
when(someObject.method()).thenReturn(...);
Add a second test to verify that audit is not called when the country code is
“us”. You can add a second argument to verify that represents the number of
times you expect verify to be invoked. In this case, you can specify that you
expect it never to be called. Provide an any() matcher as the argument to the
audit method, indicating that the method will never be called with anything.
utj3-mock-objects/08/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
import static org.mockito.Mockito.never;
➤
import static org.mockito.ArgumentMatchers.any;
➤
// ...
@Test
void doesNotOccurWhenUSAddressRetrieved() {
Chapter 3. Using Test Doubles • 64
report erratum  •  discuss


---
**Page 65**

when(http.get(anyString())).thenReturn("""
{"address":{ "country_code":"us"}}""");
retriever.retrieve(1.0, -1.0);
verify(auditor, never()).audit(any());
➤
}
Both verify and when contain numerous nuances and options. Make sure you
peruse the Mockito docs
2 for more on these and other features.
Testing Exception Handling
Exception handling is often an afterthought. The happy path is the first thing
in the mind of most developers; that’s human nature. After they get a solution
working, a developer revisits the code and thinks about what might go wrong.
They add exception-handling logic to all the places (hopefully) it looks like it
needs it.
Currently, AddressRetriever doesn’t handle errors thrown by the HTTP get method,
which could occur for a number of reasons. You’ve decided that retrieve
shouldn’t propagate the exception but should instead return null.
Mockito will help you set up a test to emulate get throwing an exception.
Rather than returning a value when an expectation is met, as you’ve been
doing throughout this chapter, you tell Mockito to throw an exception:
utj3-mock-objects/09/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
@Test
void returnsNullWhenHttpGetThrows() {
when(http.get(anyString())).thenThrow(RuntimeException.class);
➤
var address = retriever.retrieve(38, -104);
assertNull(address);
}
Your implementation requires a try/catch block to trap the potential exception
emanating from get. The unsightliness of the construct—six, count ‘em, six
vertical lines of code—is worth isolating by extracting to a separate method:
utj3-mock-objects/09/src/main/java/com/langrsoft/domain/AddressRetriever.java
public class AddressRetriever {
private Auditor auditor = new ApplicationAuditor();
private static final String SERVER =
"https://nominatim.openstreetmap.org";
private Http http = new HttpImpl(); // this cannot be final
2.
https://site.mockito.org/javadoc/current/org/mockito/Mockito.html
report erratum  •  discuss
Testing Exception Handling • 65


---
**Page 66**

public Address retrieve(double latitude, double longitude) {
// ...
var jsonResponse = get(url);
➤
if (jsonResponse == null) return null;
// ...
}
private String get(String url) {
➤
try {
➤
return http.get(url);
➤
}
➤
catch (Exception e) {
➤
return null;
➤
}
➤
}
➤
// ...
}
Mockito’s thenThrow stub helps your tests describe how the system deals with
errors. Also important: writing tests to describe how and when code propa-
gates errors. You’ll learn about that in Expecting Exceptions, on page 112.
Fast Tests
Mock objects are essential for creating unit tests that aren’t beholden to
volatile external dependencies, such as the Nominatim API. An added bonus
of employing mock objects: you gain tremendously faster tests.
Tremendously? There’s no unit testing standard for what fast and slow mean.
Perhaps it’s personal: if you’re unwilling to wait for tests to complete and
instead, forego or defer running them, they’re too slow.
Here’s another way to characterize a test’s speed: if it runs code that ultimately
interacts with external dependencies—databases, files, and network calls—it’s
slow. If the test otherwise executes Java code that interacts only with more
Java code and no external dependencies, it’s usually fast.
Slow tests take many dozens, hundreds, or thousands of milliseconds to
execute. Fast tests each take, at most, a few milliseconds to execute.
Milliseconds add up. Consider a suite of 2500 unit tests. If the average exe-
cution time of each test is 200ms, running them all takes over eight minutes.
If, instead, each test takes 5ms, running them all takes less than 15 seconds.
You might run an eight-plus-minute test suite two or three times a day. You
can run a 15-second suite many times per hour.
Chapter 3. Using Test Doubles • 66
report erratum  •  discuss


---
**Page 67**

With an eight-minute suite, you might also concede and run a small subset
after making changes. But you’ll start unwittingly breaking code elsewhere,
not finding out until much later.
Keep your tests fast! Minimize dependencies on code that executes slowly. If
all your tests interact with code that makes one or more database calls,
directly or indirectly, all your tests will be slow.
Fast tests support the most effective way to build software: incrementally.
Testing as you go verifies that each new behavior works and doesn’t break
other code, letting you frequently and confidently integrate code changes.
Fast tests empower continual, confident software development.
A Mélange of Important Test Double Tips
• A good mock-based test is three lines: a one-line arrange step with a
highly readable smart stub declaration, followed by one-line act and assert
steps. That’s a test anyone can quickly read, understand, and trust.
• In answersAppropriateAddressForValidCoordinates, the expected parameter string
of "lat=38.000000&lon=-104.000000" correlates clearly with the act arguments of
38.0 and -104.0. Creating correlation between arrange and assert isn’t easy
sometimes, but it saves developers from digging about for understanding.
Without such correlation, tests using mocks can be hard to follow.
• Mocks supplant real behavior. Ask yourself if you’re using them safely.
Does your mock really emulate the way the production code works? Does
the production code return other formats you’re not thinking of? Does it
throw exceptions? Does it return null? You’ll want a different test for each
of these conditions.
• Does your test really trigger use of a mock, or does it run real production
code? Try turning off the mock and letting your code interact with the
production class to see what happens (it might be as subtle as a slightly
slower test run). Step-debug if needed.
• Try temporarily throwing a runtime exception from the production code.
If your test bombs as a result, you know you’re hitting the production
code. (Don’t forget and accidentally push that throw into production!)
report erratum  •  discuss
A Mélange of Important Test Double Tips • 67


---
**Page 68**

• Use test data that you know is not what a production call would return.
Your test passed neat, whole numbers for latitude and longitude. You
also know Anywhere is not a real city in Colorado. If you were using the
real HttpImpl class, your test expectations would fail.
• The code you’re mocking is getting replaced with a test double and is not
getting tested. A mock represents gaps in test coverage. Make sure you
have an appropriate higher-level test (perhaps an integration test) that
demonstrates end-to-end use of the real class.
• Using DI frameworks can slow down your test runs considerably. Consider
injecting your dependencies by hand—it turns out to be fairly easy to do.
• When using DI frameworks, prefer injecting via a real, exposed interface
point—typically the constructor. Cleverness creates complexity and culti-
vates contempt.
A mock creates a hole in unit testing coverage. Write integration
tests to cover these gaps.
Possibly the most important when it comes to test doubles: avoid using them,
or at least minimize their pervasiveness. If a large number of tests require
test doubles, you’re allowing your troublesome dependencies to proliferate
too much. Reconsider the design.
A couple of avoidance policies:
• Rather than have a class depend on the persistence layer, push the
responsibility out. Have a client retrieve the relevant data, then inject that.
• If collaborator classes don’t have troublesome dependencies, let your tests
interact with their real code rather than mock them.
Mocks are great tools, but they can also create great headaches. Take care.
Summary
In this chapter, you learned the important technique of introducing stubs
and mocks to emulate the behavior of dependent objects. Your tests don’t
have to interact with live services, files, databases, and other troublesome
dependencies! You also learned how to use Mockito to simplify your effort in
creating and injecting mocks.
Chapter 3. Using Test Doubles • 68
report erratum  •  discuss


---
**Page 69**

You also learned Mockito’s core features, but it can do much more:
• Verify that methods were called in order
• Capture and assert against an argument passed to a mock method
• Spy on a method, which results in the real method getting called
Now that you’re empowered with enough unit testing fundamentals to survive,
it’s time to explore some bigger-picture unit testing topics: code coverage,
integration testing, and tests for multithreaded code.
report erratum  •  discuss
Summary • 69


---
**Page 71**

CHAPTER 4
Expanding Your Testing Horizons
At this point, you’ve worked through the core topics in unit testing, including
JUnit and unit testing fundamentals, how to test various scenarios, and how
to use test doubles to deal with dependencies.
In this chapter, you’ll review a few topics that begin to move outside the sphere
of “doing unit testing”:
• Code coverage and how it can help (or hurt)
• Challenges with writing tests for multithreaded code
• Writing integration tests
Improving Unit Testing Skills Using Code Coverage
Code coverage metrics measure the percentage of code that your unit tests
execute (exercise) when run. Ostensibly, code that is covered is working, and
code that is not covered represents the risk of breakage.
From a high level, tests that exhaust all relevant pieces of code provide 100
percent coverage. Code with no tests whatsoever has 0 percent coverage. Most
code lies somewhere in between.
Many tools exist that will calculate coverage metrics for Java code, including
JaCoCo, OpenClover, SonarQube, and Cobertura. IntelliJ IDEA ships with a
coverage tool built into the IDE.
Numerous coverage metrics exist to measure various code aspects. Function
coverage, for example, measures the percentage of functions (methods) exer-
cised by tests. Some of the other metrics include line, statement, branch,
condition, and path coverage.
report erratum  •  discuss



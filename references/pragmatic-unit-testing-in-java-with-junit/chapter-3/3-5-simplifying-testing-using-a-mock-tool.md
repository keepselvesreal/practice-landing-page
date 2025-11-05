# 3.5 Simplifying Testing Using a Mock Tool (pp.59-62)

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



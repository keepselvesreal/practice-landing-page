# 3.2 Replacing Troublesome Behavior with Stubs (pp.55-58)

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



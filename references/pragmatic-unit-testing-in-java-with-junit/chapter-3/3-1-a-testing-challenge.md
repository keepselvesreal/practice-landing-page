# 3.1 A Testing Challenge (pp.53-55)

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



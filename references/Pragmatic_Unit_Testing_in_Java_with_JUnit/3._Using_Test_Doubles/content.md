Line 1: 
Line 2: --- 페이지 74 ---
Line 3: CHAPTER 3
Line 4: Using Test Doubles
Line 5: You can test a lot of your system using the information you’ve learned over
Line 6: the prior two chapters. But not all units are going to be similarly easy to test.
Line 7: It’s a safe bet you find your own system hard to test. Perhaps you think the first
Line 8: two chapters made it look too easy. “It must be nice to have a system that sup-
Line 9: ports writing unit tests out of the box, but it doesn’t match my reality,” says Joe.
Line 10: In this chapter, you’ll learn how to employ test doubles to break dependencies
Line 11: on pain-inducing collaborators. A test double is a stand-in (think “stunt
Line 12: double”) for the dependencies that make your code hard to test. You’re prob-
Line 13: ably already familiar with the name of one kind of test double—a mock object.
Line 14: With test doubles, you gain a tool that will help you get past the ever-present
Line 15: unit testing hurdle of troublesome dependencies.
Line 16: A Testing Challenge
Line 17: You’re testing an AddressRetriever. Given a latitude and longitude, its retrieve
Line 18: method returns an appropriately populated Address object.
Line 19: utj3-mock-objects/01/src/main/java/com/langrsoft/domain/AddressRetriever.java
Line 20: import com.fasterxml.jackson.core.JsonProcessingException;
Line 21: import com.fasterxml.jackson.databind.DeserializationFeature;
Line 22: import com.fasterxml.jackson.databind.ObjectMapper;
Line 23: import com.langrsoft.util.HttpImpl;
Line 24: public class AddressRetriever {
Line 25: private static final String SERVER =
Line 26: "https://nominatim.openstreetmap.org";
Line 27: public Address retrieve(double latitude, double longitude) {
Line 28: var locationParams =
Line 29: "lon=%.6f&lat=%.6f".formatted(latitude, longitude);
Line 30: var url =
Line 31: "%s/reverse?%s&format=json".formatted(SERVER, locationParams);
Line 32: report erratum  •  discuss
Line 33: 
Line 34: --- 페이지 75 ---
Line 35: var jsonResponse = new HttpImpl().get(url);
Line 36: ➤
Line 37: var response = parseResponse(jsonResponse);
Line 38: var address = response.address();
Line 39: var country = address.country_code();
Line 40: if (!country.equals("us"))
Line 41: throw new UnsupportedOperationException(
Line 42: "intl addresses unsupported");
Line 43: return address;
Line 44: }
Line 45: private Response parseResponse(String jsonResponse) {
Line 46: var mapper = new ObjectMapper().configure(
Line 47: DeserializationFeature.FAIL_ON_UNKNOWN_PROPERTIES, false);
Line 48: try {
Line 49: return mapper.readValue(jsonResponse, Response.class);
Line 50: } catch (JsonProcessingException e) {
Line 51: throw new RuntimeException(e);
Line 52: }
Line 53: }
Line 54: }
Line 55: At first glance, testing retrieve appears straightforward—it’s only about ten lines
Line 56: long with one conditional and a short helper method. Then you notice code that
Line 57: appears to make a live HTTP get request (highlighted in AddressRetriever). Hmm.
Line 58: Sure enough, the HttpImpl class interacts with Apache’s HttpComponents client to
Line 59: execute a REST call:
Line 60: utj3-mock-objects/01/src/main/java/com/langrsoft/util/HttpImpl.java
Line 61: import java.io.IOException;
Line 62: import java.net.URI;
Line 63: import java.net.http.HttpClient;
Line 64: import java.net.http.HttpRequest;
Line 65: import java.net.http.HttpResponse.BodyHandlers;
Line 66: public class HttpImpl implements Http {
Line 67: @Override
Line 68: public String get(String url) {
Line 69: try (var client = HttpClient.newHttpClient()) {
Line 70: var request = HttpRequest.newBuilder().uri(URI.create(url)).build();
Line 71: try {
Line 72: var httpResponse = client.send(request, BodyHandlers.ofString());
Line 73: return httpResponse.body();
Line 74: } catch (IOException | InterruptedException e) {
Line 75: throw new RuntimeException(e);
Line 76: }
Line 77: }
Line 78: }
Line 79: }
Line 80: Chapter 3. Using Test Doubles • 54
Line 81: report erratum  •  discuss
Line 82: 
Line 83: --- 페이지 76 ---
Line 84: The HttpImpl class implements the HTTP interface:
Line 85: utj3-mock-objects/01/src/main/java/com/langrsoft/util/Http.java
Line 86: public interface Http {
Line 87: String get(String url);
Line 88: }
Line 89: You trust HttpImpl because you find an integration test for it in ./src/test/java/com
Line 90: /langrsoft/util. But you also know that HttpImpl’s code interacts with an external
Line 91: service over HTTP—a recipe for unit testing trouble. Any tests you write for
Line 92: retrieve in AddressRetriever will ultimately trigger a live HTTP call. That carries at
Line 93: least two big implications:
Line 94: • The tests against the live call will be slow compared to the bulk of your
Line 95: other fast tests.
Line 96: • You can’t guarantee that the Nominatim HTTP API will be available or
Line 97: return consistent results. It’s out of your control.
Line 98: A test version of the API would give you control over availability. Your builds
Line 99: and local dev environments would need to start/restart the service as
Line 100: appropriate. It would also be slow in comparison (see Fast Tests, on page 66).
Line 101: You want a way to focus on unit testing the rest of the logic in retrieve—the
Line 102: code that preps the HTTP call and the code that handles the response—
Line 103: isolated from the HTTP dependency.
Line 104: Replacing Troublesome Behavior with Stubs
Line 105: The challenge for testing is the code in HttpImpl that calls a real endpoint. To
Line 106: fix the problem, your test can supplant HttpImpl’s live call with logic that instead
Line 107: returns mocked-up data. You’ll create an implementation of HttpImpl known
Line 108: as a stub: It will stub out the real code with a simplified version.
Line 109: A stub is a test double that supplants real behavior with a method
Line 110: that returns a hardcoded value.
Line 111: HTTP is a functional interface: It contains exactly one abstract method decla-
Line 112: ration (for get). As a result, you can dynamically and concisely declare an
Line 113: implementation of HTTP using a lambda:
Line 114: utj3-mock-objects/02/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 115: Http http = url ->
Line 116: """
Line 117: {"address":{
Line 118: "house_number":"324",
Line 119: report erratum  •  discuss
Line 120: Replacing Troublesome Behavior with Stubs • 55
Line 121: 
Line 122: --- 페이지 77 ---
Line 123: "road":"Main St",
Line 124: "city":"Anywhere",
Line 125: "state":"Colorado",
Line 126: "postcode":"81234",
Line 127: "country_code":"us"}}
Line 128: """;
Line 129: The stub returns a hardcoded JSON string, backward engineered from the
Line 130: parsing code in retrieve. Consider it an alternate implementation of the HTTP
Line 131: interface, suitable for use only by a test.
Line 132: Injecting Dependencies into Production Code
Line 133: The HTTP stub gets you halfway toward being able to write your test. You
Line 134: must also tell AddressRetriever to use your stub instead of a “real” HttpImpl object.
Line 135: You do so using dependency injection, a fancy term for passing the stub to
Line 136: an AddressRetriever instance. You can inject a stub in a few ways; here, you’ll
Line 137: inject it via the constructor:
Line 138: utj3-mock-objects/02/src/main/java/com/langrsoft/domain/AddressRetriever.java
Line 139: public class AddressRetriever {
Line 140: private static final String SERVER =
Line 141: "https://nominatim.openstreetmap.org";
Line 142: private final Http http;
Line 143: ➤
Line 144: public AddressRetriever(Http http) {
Line 145: ➤
Line 146: this.http = http;
Line 147: ➤
Line 148: }
Line 149: ➤
Line 150: public Address retrieve(double latitude, double longitude) {
Line 151: var locationParams =
Line 152: "lon=%.6f&lat=%.6f".formatted(latitude, longitude);
Line 153: var url =
Line 154: "%s/reverse?%s&format=json".formatted(SERVER, locationParams);
Line 155: var jsonResponse = http.get(url);
Line 156: ➤
Line 157: var response = parseResponse(jsonResponse);
Line 158: // ...
Line 159: }
Line 160: // ...
Line 161: The call to http.get(url) in retrieve (highlighted) no longer creates a private instance
Line 162: of HTTP. It now dereferences the http field, which points to the stub when
Line 163: executed in the context of the test you can now write.
Line 164: utj3-mock-objects/02/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 165: import com.langrsoft.util.*;
Line 166: import org.junit.jupiter.api.Test;
Line 167: import static org.junit.jupiter.api.Assertions.assertEquals;
Line 168: import static org.junit.jupiter.api.Assertions.assertThrows;
Line 169: Chapter 3. Using Test Doubles • 56
Line 170: report erratum  •  discuss
Line 171: 
Line 172: --- 페이지 78 ---
Line 173: class AnAddressRetriever {
Line 174: @Test
Line 175: void answersAppropriateAddressForValidCoordinates() {
Line 176: Http http = url ->
Line 177: """
Line 178: {"address":{
Line 179: "house_number":"324",
Line 180: "road":"Main St",
Line 181: "city":"Anywhere",
Line 182: "state":"Colorado",
Line 183: "postcode":"81234",
Line 184: "country_code":"us"}}
Line 185: """;
Line 186: var retriever = new AddressRetriever(http);
Line 187: var address = retriever.retrieve(38, -104);
Line 188: assertEquals("324", address.house_number());
Line 189: assertEquals("Main St", address.road());
Line 190: assertEquals("Anywhere", address.city());
Line 191: assertEquals("Colorado", address.state());
Line 192: assertEquals("81234", address.postcode());
Line 193: }
Line 194: }
Line 195: When the test runs:
Line 196: • It creates an AddressRetriever, passing it the HTTP stub instance.
Line 197: • When executed, the retrieve method formats a URL using parameters passed
Line 198: to the method. It then calls the get method on http.
Line 199: • The stub returns the JSON string you hardcoded in the test.
Line 200: • The rest of the retrieve method parses the hardcoded JSON string and
Line 201: populates an Address object accordingly.
Line 202: • The test verifies elements of the returned Address object.
Line 203: The retrieve method is oblivious to whether http references a stub or the real
Line 204: implementation. In this example, the stub represents a “single use test case”
Line 205: for purposes of one test. Add another test that creates a completely different
Line 206: stub:
Line 207: utj3-mock-objects/02/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 208: @Test
Line 209: void throwsWhenNotUSCountryCode() {
Line 210: Http http = url -> """
Line 211: {"address":{ "country_code":"not us"}}""";
Line 212: var retriever = new AddressRetriever(http);
Line 213: report erratum  •  discuss
Line 214: Replacing Troublesome Behavior with Stubs • 57
Line 215: 
Line 216: --- 페이지 79 ---
Line 217: assertThrows(UnsupportedOperationException.class,
Line 218: () -> retriever.retrieve(1.0, -1.0));
Line 219: }
Line 220: This second test takes advantage of the fact that AddressRetriever code looks
Line 221: only at country_code, throwing an exception when it is anything but the lowercase
Line 222: string "us".
Line 223: Changing Your Design to Support Testing
Line 224: You changed the design of AddressRetriever. Before, it created an HttpImpl instance
Line 225: in retrieve as a private detail. Now, a client using AddressRetriever must pass an
Line 226: HTTP-derived object to its constructor (or use a dependency injection tool):
Line 227: var retriever = new AddressRetriever(new HttpImpl());
Line 228: Changing design to simplify testing might seem odd, but doing so lets you
Line 229: write the tests that increase your confidence to ship.
Line 230: You’re not limited to constructor injection; you can inject stubs in many
Line 231: other ways. Some ways require no changes to the interface of your class. You
Line 232: can use setters instead of constructors, you can override factory methods,
Line 233: you can introduce abstract factories, and you can even use tools such as
Line 234: Google Guice or Spring that do the injection somewhat magically.
Line 235: Adding Smarts to Your Stub: Verifying Parameters
Line 236: Your HTTP stub always returns the same hardcoded JSON string, regardless
Line 237: of the latitude/longitude passed to get. That’s a small hole in testing. If the
Line 238: AddressRetriever doesn’t pass the parameters properly, you have a defect.
Line 239: You are not exercising the real behavior of HttpImpl (which already has
Line 240: tests). You’re exercising the rest of retrieve’s code based on a return value that
Line 241: HttpImpl might cough up. The only thing left to cover is verifying that retrieve
Line 242: correctly interacts with HttpImpl.
Line 243: As a quick stab at a solution, add a guard clause to the stub that verifies the
Line 244: URL passed to the HTTP method get. If it doesn’t contain the expected
Line 245: parameter string, explicitly fail the test at that point:
Line 246: utj3-mock-objects/03/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 247: @Test
Line 248: void answersAppropriateAddressForValidCoordinates() {
Line 249: Http http = url -> {
Line 250: if (!url.contains("lat=38") ||
Line 251: ➤
Line 252: !url.contains("lon=-104"))
Line 253: ➤
Line 254: fail("url " + url + " does not contain correct params");
Line 255: ➤
Line 256: Chapter 3. Using Test Doubles • 58
Line 257: report erratum  •  discuss
Line 258: 
Line 259: --- 페이지 80 ---
Line 260: return """
Line 261: {"address":{
Line 262: "house_number":"324",
Line 263: "road":"Main St",
Line 264: "city":"Anywhere",
Line 265: "state":"Colorado",
Line 266: "postcode":"81234",
Line 267: "country_code":"us"}}
Line 268: """;
Line 269: };
Line 270: var retriever = new AddressRetriever(http);
Line 271: var address = retriever.retrieve(38, -104);
Line 272: // ...
Line 273: The stub has a little bit of smarts now…meaning it’s no longer a stub. It’s
Line 274: closer to being a mock. A mock, like a stub, lets you provide test-specific
Line 275: behavior. It can also self-verify, as in this example, by ensuring that expected
Line 276: interactions with collaborators (an HTTP implementation here) occur.
Line 277: The “smart stub” pays off—your test now fails. Did you spot the defect earlier?
Line 278: utj3-mock-objects/03/src/main/java/com/langrsoft/domain/AddressRetriever.java
Line 279: public Address retrieve(double latitude, double longitude) {
Line 280: var locationParams = "lon=%.6f&lat=%.6f".formatted(latitude, longitude);
Line 281: var url = "%s/reverse?%s&format=json".formatted(SERVER, locationParams);
Line 282: var jsonResponse = http.get(url);
Line 283: // ...
Line 284: }
Line 285: Fixing the problem involves swapping the two query parameter names:
Line 286: utj3-mock-objects/04/src/main/java/com/langrsoft/domain/AddressRetriever.java
Line 287: var locationParams = "lat=%.6f&lon=%.6f".formatted(latitude, longitude);
Line 288: Using a mock, your test can verify that a method was called and
Line 289: with the right arguments.
Line 290: Simplifying Testing Using a Mock Tool
Line 291: Hand-grown smart stubs are kind of a bad idea. A stub is a simple test con-
Line 292: struct that returns a hard-coded value. Adding logic in the middle of it is a
Line 293: recipe for wasted time when you get the logic wrong (you eventually will)—
Line 294: which turns it into a smart-ahh…never mind.
Line 295: report erratum  •  discuss
Line 296: Simplifying Testing Using a Mock Tool • 59
Line 297: 
Line 298: --- 페이지 81 ---
Line 299: You’ll instead represent your stub using Mockito,
Line 300: 1 the de facto standard
Line 301: “mock” library for Java. Using the tool will keep your tests safer and simpler
Line 302: when you need test doubles. It handles the smarts, so you don’t have to.
Line 303: Here’s the test updated to use Mockito:
Line 304: utj3-mock-objects/05/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 305: // ...
Line 306: import static org.mockito.ArgumentMatchers.contains;
Line 307: ➤
Line 308: import static org.mockito.Mockito.mock;
Line 309: ➤
Line 310: import static org.mockito.Mockito.when;
Line 311: ➤
Line 312: class AnAddressRetriever {
Line 313: Http http = mock(Http.class);
Line 314: ➤
Line 315: @Test
Line 316: void answersAppropriateAddressForValidCoordinates() {
Line 317: when(http.get(contains("lat=38.000000&lon=-104.000000"))).thenReturn(
Line 318: ➤
Line 319: """
Line 320: {"address":{
Line 321: "house_number":"324",
Line 322: "road":"Main St",
Line 323: "city":"Anywhere",
Line 324: "state":"Colorado",
Line 325: "postcode":"81234",
Line 326: "country_code":"us"}}
Line 327: """);
Line 328: var retriever = new AddressRetriever(http);
Line 329: var address = retriever.retrieve(38, -104);
Line 330: // ...
Line 331: }
Line 332: // ...
Line 333: }
Line 334: The field http is initialized with a call to Mockito’s static mock method, which
Line 335: synthesizes an object that implements the HTTP interface. This mock object
Line 336: tracks when methods are called and with what arguments.
Line 337: The first statement in the test (in its arrange step) sets up an expectation on
Line 338: the mock. It tells the mock object to expect that the get method might be called.
Line 339: If the method is indeed called (at any point later during test execution), and
Line 340: with an argument containing the substring "lat=38.000000&lon=-104.000000", the
Line 341: mock object will return the specified hard-coded JSON string.
Line 342: If the get method is not called, or if it’s called but doesn’t contain the expected
Line 343: lat-long string, the mock object returns null. The contains method is what
Line 344: 1.
Line 345: https://site.mockito.org
Line 346: Chapter 3. Using Test Doubles • 60
Line 347: report erratum  •  discuss
Line 348: 
Line 349: --- 페이지 82 ---
Line 350: Mockito refers to as matcher. More typically, you wouldn’t use a matcher like
Line 351: contains, but would instead specify the exact argument expected.
Line 352: The second statement in the test, as before, injects the Mockito mock into
Line 353: the AddressRetriever via its constructor. Replacing your stub with Mockito doesn’t
Line 354: require changing any production code.
Line 355: When the retrieve method is called during the “act” step of the test, its code
Line 356: interacts with the Mockito mock. If the Mockito mock’s expectations are
Line 357: met—if the production code calls http.get(url) as expected, the mock returns
Line 358: the hardcoded JSON string, and the test passes. If not, the test fails.
Line 359: It would be better if your mock didn’t have to know the exact encoding order
Line 360: of the latitude and longitude query params. Mockito lets you supply two dis-
Line 361: tinct matchers using the and matcher:
Line 362: utj3-mock-objects/06/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 363: import static org.mockito.AdditionalMatchers.and;
Line 364: // ...
Line 365: @Test
Line 366: void answersAppropriateAddressForValidCoordinates() {
Line 367: when(http.get(
Line 368: and(contains("lat=38.000000"), contains("lon=-104.000000"))))
Line 369: ➤
Line 370: .thenReturn(
Line 371: // ...
Line 372: }
Line 373: Both contains matchers have to hold true for the test to pass.
Line 374: With the happy path test for retrieve out of the way, you can update the not-
Line 375: as-happy-path test, throwsWhenNotUSCountryCode, to use Mockito:
Line 376: utj3-mock-objects/05/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 377: @Test
Line 378: void throwsWhenNotUSCountryCode() {
Line 379: when(http.get(anyString())).thenReturn("""
Line 380: ➤
Line 381: {"address":{ "country_code":"not us"}}""");
Line 382: ➤
Line 383: var retriever = new AddressRetriever(http);
Line 384: assertThrows(UnsupportedOperationException.class,
Line 385: () -> retriever.retrieve(1.0, -1.0));
Line 386: }
Line 387: Your happy path test, answersAppropriateAddressForValidCoordinates, demonstrated that
Line 388: retrieve correctly formats its arguments into a query parameter string. Accord-
Line 389: ingly, you don’t need to similarly worry about doing so in this second test. You
Line 390: can use the Mockito matcher method anyString() to indicate that the test should
Line 391: pass as long as a string object is passed to the get method.
Line 392: report erratum  •  discuss
Line 393: Simplifying Testing Using a Mock Tool • 61
Line 394: 
Line 395: --- 페이지 83 ---
Line 396: The when(...).thenReturn(...) pattern is one of a number of ways to set up mocks
Line 397: using Mockito, but it’s probably the simplest to understand and code. It distills
Line 398: the effort of setting up a mock into what’s essentially a one-liner that imme-
Line 399: diately makes sense to someone reading the code.
Line 400: Injecting Mocks with Mockito
Line 401: Using constructor injection may require you to change your class’s interface.
Line 402: A dependency injection (DI) tool like Spring DI, Google Guice, or PicoContainer
Line 403: can eliminate the need for that change. You can also use Mockito, which
Line 404: provides nominal built-in DI capabilities. It’s not as sophisticated as the
Line 405: other two tools, but it might be all you need. To use Mockito’s DI:
Line 406: • Annotate the test class with @ExtendWith(MockitoExtension.class).
Line 407: • Annotate the http field with @Mock. Mockito initializes it as a mock object.
Line 408: • Annotate the retriever field with @InjectMocks. Mockito creates an instance of
Line 409: retriever and injects any @Mock fields into it.
Line 410: utj3-mock-objects/07/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 411: // ...
Line 412: import org.junit.jupiter.api.extension.ExtendWith;
Line 413: ➤
Line 414: import org.mockito.Mock;
Line 415: ➤
Line 416: import org.mockito.InjectMocks;
Line 417: ➤
Line 418: import org.mockito.junit.jupiter.MockitoExtension;
Line 419: ➤
Line 420: @ExtendWith(MockitoExtension.class)
Line 421: ➤
Line 422: class AnAddressRetriever {
Line 423: @InjectMocks
Line 424: ➤
Line 425: AddressRetriever retriever;
Line 426: ➤
Line 427: @Mock
Line 428: ➤
Line 429: Http http;
Line 430: ➤
Line 431: @Test
Line 432: void answersAppropriateAddressForValidCoordinates() {
Line 433: when(http.get(and(contains("lat=38.000000"),
Line 434: contains("lon=-104.000000"))))
Line 435: // ...
Line 436: }
Line 437: // ...
Line 438: }
Line 439: When injecting mock objects, Mockito first seeks an appropriate constructor—
Line 440: in this case, one that takes on an HTTP instance. If it finds none, it seeks an
Line 441: appropriate setter method, and then finally, a field with the matching type.
Line 442: To try this feature, eliminate AddressRetriever’s constructor and initialize an http
Line 443: field:
Line 444: Chapter 3. Using Test Doubles • 62
Line 445: report erratum  •  discuss
Line 446: 
Line 447: --- 페이지 84 ---
Line 448: utj3-mock-objects/07/src/main/java/com/langrsoft/domain/AddressRetriever.java
Line 449: public class AddressRetriever {
Line 450: private static final String SERVER =
Line 451: "https://nominatim.openstreetmap.org";
Line 452: private Http http = new HttpImpl(); // this cannot be final
Line 453: ➤
Line 454: // look ma, no constructor!
Line 455: ➤
Line 456: public Address retrieve(double latitude, double longitude) {
Line 457: // ...
Line 458: }
Line 459: // ...
Line 460: }
Line 461: From the test, Mockito magically finds your http field and injects the mock
Line 462: instance into it (overwriting what was already there)!
Line 463: Production clients no longer need to pass a value for http into the AddressRetriever
Line 464: since it’s initialized to the appropriate production object.
Line 465: Downsides: mucking with privates violates many folks’ design sensibilities.
Line 466: Also, Mockito injection is slow, adding almost a full second to the test run on
Line 467: my machine. Ensure its inclusion doesn’t pig out the overall execution time
Line 468: of your test suite.
Line 469: Verifying a Method Was Called…or Not
Line 470: As an alternative to when(...).thenReturn(...), you might want to verify that a certain
Line 471: method was called with the proper arguments as part of processing. The
Line 472: typical case for this need is when you’re invoking a consumer—a method that
Line 473: has side effects but returns nothing. Mockito helps you verify that such a
Line 474: method was called with its verify functionality.
Line 475: Update the AddressRetriever to tell an Auditor instance to add audit information
Line 476: when the country code returned is a non-U.S. country code:
Line 477: utj3-mock-objects/08/src/main/java/com/langrsoft/domain/AddressRetriever.java
Line 478: public class AddressRetriever {
Line 479: private Auditor auditor = new ApplicationAuditor();
Line 480: ➤
Line 481: // ...
Line 482: public Address retrieve(double latitude, double longitude) {
Line 483: // ...
Line 484: var country = address.country_code();
Line 485: if (!country.equals("us")) {
Line 486: auditor.audit("request for country code: %s".formatted(country));
Line 487: ➤
Line 488: throw new UnsupportedOperationException(
Line 489: "intl addresses unsupported");
Line 490: }
Line 491: report erratum  •  discuss
Line 492: Verifying a Method Was Called…or Not • 63
Line 493: 
Line 494: --- 페이지 85 ---
Line 495: return address;
Line 496: }
Line 497: // ...
Line 498: }
Line 499: For now, the audit method in ApplicationAuditor does nothing; some other team
Line 500: member is coding it. You need only the interface declaration in order to write
Line 501: your test:
Line 502: utj3-mock-objects/08/src/main/java/com/langrsoft/domain/Auditor.java
Line 503: public interface Auditor {
Line 504: void audit(String message);
Line 505: }
Line 506: Add a test that proves audit is called for a non-U.S. country code. Use Mockito’s
Line 507: verify method, which acts as an assertion. If the audit method is called with
Line 508: exactly the same String argument, the test passes.
Line 509: utj3-mock-objects/08/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 510: import static org.mockito.Mockito.verify;
Line 511: ➤
Line 512: // ...
Line 513: @Test
Line 514: void auditsWhenNonUSAddressRetrieved() {
Line 515: when(http.get(anyString())).thenReturn("""
Line 516: {"address":{ "country_code":"not us"}}""");
Line 517: assertThrows(UnsupportedOperationException.class,
Line 518: () -> retriever.retrieve(1.0, -1.0));
Line 519: verify(auditor).audit("request for country code: not us");
Line 520: ➤
Line 521: }
Line 522: // ...
Line 523: }
Line 524: Note the difference regarding parentheses placement between verify and when:
Line 525: verify(someObject).method();
Line 526: when(someObject.method()).thenReturn(...);
Line 527: Add a second test to verify that audit is not called when the country code is
Line 528: “us”. You can add a second argument to verify that represents the number of
Line 529: times you expect verify to be invoked. In this case, you can specify that you
Line 530: expect it never to be called. Provide an any() matcher as the argument to the
Line 531: audit method, indicating that the method will never be called with anything.
Line 532: utj3-mock-objects/08/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 533: import static org.mockito.Mockito.never;
Line 534: ➤
Line 535: import static org.mockito.ArgumentMatchers.any;
Line 536: ➤
Line 537: // ...
Line 538: @Test
Line 539: void doesNotOccurWhenUSAddressRetrieved() {
Line 540: Chapter 3. Using Test Doubles • 64
Line 541: report erratum  •  discuss
Line 542: 
Line 543: --- 페이지 86 ---
Line 544: when(http.get(anyString())).thenReturn("""
Line 545: {"address":{ "country_code":"us"}}""");
Line 546: retriever.retrieve(1.0, -1.0);
Line 547: verify(auditor, never()).audit(any());
Line 548: ➤
Line 549: }
Line 550: Both verify and when contain numerous nuances and options. Make sure you
Line 551: peruse the Mockito docs
Line 552: 2 for more on these and other features.
Line 553: Testing Exception Handling
Line 554: Exception handling is often an afterthought. The happy path is the first thing
Line 555: in the mind of most developers; that’s human nature. After they get a solution
Line 556: working, a developer revisits the code and thinks about what might go wrong.
Line 557: They add exception-handling logic to all the places (hopefully) it looks like it
Line 558: needs it.
Line 559: Currently, AddressRetriever doesn’t handle errors thrown by the HTTP get method,
Line 560: which could occur for a number of reasons. You’ve decided that retrieve
Line 561: shouldn’t propagate the exception but should instead return null.
Line 562: Mockito will help you set up a test to emulate get throwing an exception.
Line 563: Rather than returning a value when an expectation is met, as you’ve been
Line 564: doing throughout this chapter, you tell Mockito to throw an exception:
Line 565: utj3-mock-objects/09/src/test/java/com/langrsoft/domain/AnAddressRetriever.java
Line 566: @Test
Line 567: void returnsNullWhenHttpGetThrows() {
Line 568: when(http.get(anyString())).thenThrow(RuntimeException.class);
Line 569: ➤
Line 570: var address = retriever.retrieve(38, -104);
Line 571: assertNull(address);
Line 572: }
Line 573: Your implementation requires a try/catch block to trap the potential exception
Line 574: emanating from get. The unsightliness of the construct—six, count ‘em, six
Line 575: vertical lines of code—is worth isolating by extracting to a separate method:
Line 576: utj3-mock-objects/09/src/main/java/com/langrsoft/domain/AddressRetriever.java
Line 577: public class AddressRetriever {
Line 578: private Auditor auditor = new ApplicationAuditor();
Line 579: private static final String SERVER =
Line 580: "https://nominatim.openstreetmap.org";
Line 581: private Http http = new HttpImpl(); // this cannot be final
Line 582: 2.
Line 583: https://site.mockito.org/javadoc/current/org/mockito/Mockito.html
Line 584: report erratum  •  discuss
Line 585: Testing Exception Handling • 65
Line 586: 
Line 587: --- 페이지 87 ---
Line 588: public Address retrieve(double latitude, double longitude) {
Line 589: // ...
Line 590: var jsonResponse = get(url);
Line 591: ➤
Line 592: if (jsonResponse == null) return null;
Line 593: // ...
Line 594: }
Line 595: private String get(String url) {
Line 596: ➤
Line 597: try {
Line 598: ➤
Line 599: return http.get(url);
Line 600: ➤
Line 601: }
Line 602: ➤
Line 603: catch (Exception e) {
Line 604: ➤
Line 605: return null;
Line 606: ➤
Line 607: }
Line 608: ➤
Line 609: }
Line 610: ➤
Line 611: // ...
Line 612: }
Line 613: Mockito’s thenThrow stub helps your tests describe how the system deals with
Line 614: errors. Also important: writing tests to describe how and when code propa-
Line 615: gates errors. You’ll learn about that in Expecting Exceptions, on page 112.
Line 616: Fast Tests
Line 617: Mock objects are essential for creating unit tests that aren’t beholden to
Line 618: volatile external dependencies, such as the Nominatim API. An added bonus
Line 619: of employing mock objects: you gain tremendously faster tests.
Line 620: Tremendously? There’s no unit testing standard for what fast and slow mean.
Line 621: Perhaps it’s personal: if you’re unwilling to wait for tests to complete and
Line 622: instead, forego or defer running them, they’re too slow.
Line 623: Here’s another way to characterize a test’s speed: if it runs code that ultimately
Line 624: interacts with external dependencies—databases, files, and network calls—it’s
Line 625: slow. If the test otherwise executes Java code that interacts only with more
Line 626: Java code and no external dependencies, it’s usually fast.
Line 627: Slow tests take many dozens, hundreds, or thousands of milliseconds to
Line 628: execute. Fast tests each take, at most, a few milliseconds to execute.
Line 629: Milliseconds add up. Consider a suite of 2500 unit tests. If the average exe-
Line 630: cution time of each test is 200ms, running them all takes over eight minutes.
Line 631: If, instead, each test takes 5ms, running them all takes less than 15 seconds.
Line 632: You might run an eight-plus-minute test suite two or three times a day. You
Line 633: can run a 15-second suite many times per hour.
Line 634: Chapter 3. Using Test Doubles • 66
Line 635: report erratum  •  discuss
Line 636: 
Line 637: --- 페이지 88 ---
Line 638: With an eight-minute suite, you might also concede and run a small subset
Line 639: after making changes. But you’ll start unwittingly breaking code elsewhere,
Line 640: not finding out until much later.
Line 641: Keep your tests fast! Minimize dependencies on code that executes slowly. If
Line 642: all your tests interact with code that makes one or more database calls,
Line 643: directly or indirectly, all your tests will be slow.
Line 644: Fast tests support the most effective way to build software: incrementally.
Line 645: Testing as you go verifies that each new behavior works and doesn’t break
Line 646: other code, letting you frequently and confidently integrate code changes.
Line 647: Fast tests empower continual, confident software development.
Line 648: A Mélange of Important Test Double Tips
Line 649: • A good mock-based test is three lines: a one-line arrange step with a
Line 650: highly readable smart stub declaration, followed by one-line act and assert
Line 651: steps. That’s a test anyone can quickly read, understand, and trust.
Line 652: • In answersAppropriateAddressForValidCoordinates, the expected parameter string
Line 653: of "lat=38.000000&lon=-104.000000" correlates clearly with the act arguments of
Line 654: 38.0 and -104.0. Creating correlation between arrange and assert isn’t easy
Line 655: sometimes, but it saves developers from digging about for understanding.
Line 656: Without such correlation, tests using mocks can be hard to follow.
Line 657: • Mocks supplant real behavior. Ask yourself if you’re using them safely.
Line 658: Does your mock really emulate the way the production code works? Does
Line 659: the production code return other formats you’re not thinking of? Does it
Line 660: throw exceptions? Does it return null? You’ll want a different test for each
Line 661: of these conditions.
Line 662: • Does your test really trigger use of a mock, or does it run real production
Line 663: code? Try turning off the mock and letting your code interact with the
Line 664: production class to see what happens (it might be as subtle as a slightly
Line 665: slower test run). Step-debug if needed.
Line 666: • Try temporarily throwing a runtime exception from the production code.
Line 667: If your test bombs as a result, you know you’re hitting the production
Line 668: code. (Don’t forget and accidentally push that throw into production!)
Line 669: report erratum  •  discuss
Line 670: A Mélange of Important Test Double Tips • 67
Line 671: 
Line 672: --- 페이지 89 ---
Line 673: • Use test data that you know is not what a production call would return.
Line 674: Your test passed neat, whole numbers for latitude and longitude. You
Line 675: also know Anywhere is not a real city in Colorado. If you were using the
Line 676: real HttpImpl class, your test expectations would fail.
Line 677: • The code you’re mocking is getting replaced with a test double and is not
Line 678: getting tested. A mock represents gaps in test coverage. Make sure you
Line 679: have an appropriate higher-level test (perhaps an integration test) that
Line 680: demonstrates end-to-end use of the real class.
Line 681: • Using DI frameworks can slow down your test runs considerably. Consider
Line 682: injecting your dependencies by hand—it turns out to be fairly easy to do.
Line 683: • When using DI frameworks, prefer injecting via a real, exposed interface
Line 684: point—typically the constructor. Cleverness creates complexity and culti-
Line 685: vates contempt.
Line 686: A mock creates a hole in unit testing coverage. Write integration
Line 687: tests to cover these gaps.
Line 688: Possibly the most important when it comes to test doubles: avoid using them,
Line 689: or at least minimize their pervasiveness. If a large number of tests require
Line 690: test doubles, you’re allowing your troublesome dependencies to proliferate
Line 691: too much. Reconsider the design.
Line 692: A couple of avoidance policies:
Line 693: • Rather than have a class depend on the persistence layer, push the
Line 694: responsibility out. Have a client retrieve the relevant data, then inject that.
Line 695: • If collaborator classes don’t have troublesome dependencies, let your tests
Line 696: interact with their real code rather than mock them.
Line 697: Mocks are great tools, but they can also create great headaches. Take care.
Line 698: Summary
Line 699: In this chapter, you learned the important technique of introducing stubs
Line 700: and mocks to emulate the behavior of dependent objects. Your tests don’t
Line 701: have to interact with live services, files, databases, and other troublesome
Line 702: dependencies! You also learned how to use Mockito to simplify your effort in
Line 703: creating and injecting mocks.
Line 704: Chapter 3. Using Test Doubles • 68
Line 705: report erratum  •  discuss
Line 706: 
Line 707: --- 페이지 90 ---
Line 708: You also learned Mockito’s core features, but it can do much more:
Line 709: • Verify that methods were called in order
Line 710: • Capture and assert against an argument passed to a mock method
Line 711: • Spy on a method, which results in the real method getting called
Line 712: Now that you’re empowered with enough unit testing fundamentals to survive,
Line 713: it’s time to explore some bigger-picture unit testing topics: code coverage,
Line 714: integration testing, and tests for multithreaded code.
Line 715: report erratum  •  discuss
Line 716: Summary • 69
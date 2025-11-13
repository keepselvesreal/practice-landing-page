# 3.3 Changing Your Design to Support Testing (pp.58-58)

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



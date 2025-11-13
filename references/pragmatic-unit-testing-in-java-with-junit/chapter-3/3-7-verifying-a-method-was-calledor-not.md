# 3.7 Verifying a Method Was Called…or Not (pp.63-65)

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



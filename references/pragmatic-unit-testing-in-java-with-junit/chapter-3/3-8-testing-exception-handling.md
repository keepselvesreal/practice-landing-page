# 3.8 Testing Exception Handling (pp.65-66)

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



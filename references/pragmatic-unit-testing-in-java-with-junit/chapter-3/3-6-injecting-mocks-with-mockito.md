# 3.6 Injecting Mocks with Mockito (pp.62-63)

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



# 2.8 Summary (pp.52-53)

---
**Page 52**

• Conformance—Does the value conform to an expected format, such as
an email address or filename? What does the method do when passed an
invalid format? Does a string parameter support upper or mixed case?
• Ordering—Is the set of values ordered or unordered as appropriate? What
happens if things happen out of chronological order, such as an HTTP
server that returns an OPTIONS response after a POST instead of before?
• Range—Is the value within reasonable minimum and maximum values?
Can any computations result in numeric overflow?  range
• Reference—Does the object need to be in a certain state? What happens
if it’s in an unexpected state? What if the code references something
external that’s not under its direct control?
• Existence—Does the value exist (is it non-null, nonzero, present in a set)?
What if you pass a method empty values (0, 0.0, "", null)?
• Cardinality—Are there exactly enough values? Have you covered all your
bases with ZOM? Can it handle large volumes? Is there a notion of too
many? What if there are duplicates in a list that shouldn’t allow them (for
example, a roster of classroom students)?
• Time (absolute and relative)—Is everything happening in order? At the
right time? In time?
Many of the defects you’ll code in your career will involve similar corner cases,
so you’ll positively want to cover them with tests.
Summary
You have worked through writing tests for a number of common unit
scenarios. Your own “real” code test will, of course, be different and often
more involved. Still, how you approach writing tests for your code will be
similar to the approaches you’ve learned here.
Much of the code you try to test will be dependent on other classes that are vol-
atile, slow, or even incomplete. In the next chapter, you’ll learn how to use
test doubles (colloquially referred to as mock objects or mocks) to break those
dependencies so that you can test.
Chapter 2. Testing the Building Blocks • 52
report erratum  •  discuss


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



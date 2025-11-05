# 3.9 Fast Tests (pp.66-67)

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



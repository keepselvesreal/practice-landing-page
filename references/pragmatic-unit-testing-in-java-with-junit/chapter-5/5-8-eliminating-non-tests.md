# 5.8 Eliminating Non-Tests (pp.121-122)

---
**Page 121**

this(new Segment(origin, destination, distance), dateTime);
}
boolean includes(String airport) {
return segment.includes(airport);
}
}
The following AssertJ assertion compares against a list of Flight objects stored
in the variable flights:
utj3-junit/01/src/test/java/scratch/SomeAssertJExamples.java
@Test
void filterAndExtract() {
// ...
assertThat(flights)
.filteredOn(flight -> flight.includes("DEN"))
.extracting("segment.distance", Integer.class)
.allMatch(distance -> distance < 1700);
}
The call to filteredOn returns a subset of flights involving the flight code "DEN".
The call to extracting applies an AssertJ property reference ("segment.distance") to
each "DEN" flight. The reference tells AssertJ to first retrieve the segment object
from a flight, then retrieve the distance value from that segment as an Integer.
Yes, you could manually code an equivalent to the AssertJ solution, but the
resulting code would lose the declarative nature that AssertJ can provide.
Your test would require more effort to both write and read. In contrast,
AssertJ’s support for method chaining creates a fluent sentence that you can
read as a single concept.
Regardless of whether you choose to adopt AssertJ or another third-party
assertions library, streamline your tests so they read as concise documenta-
tion. A well-designed assertion step minimizes stepwise reading.
Eliminating Non-Tests
Assertions are what make a test an automated test. Omitting assertions from
your tests would render them pointless. And yet, some developers do exactly
that in order to meet code coverage mandates easily. Another common ruse
is to write tests that exercise a large amount of code, then assert something
simple—for example, that a method’s return value is not null.
Such non-tests provide almost zero value at a significant cost in time and
effort. Worse, they carry an increasingly negative return on investment: you
must expend time on non-tests when they fail or error, when they appear in
report erratum  •  discuss
Eliminating Non-Tests • 121


---
**Page 122**

search results (“is that a real test we need to update or do we not need to
worry about it?”), and when you must update them to keep them running
(for example, when a method signature gets changed).
Eliminate tests that verify nothing.
Summary
You’ve learned numerous assertion forms in this chapter. You also learned
about AssertJ, an alternate assertions library.
Initially, you’ll survive if you predominantly use assertEquals for most assertions,
along with an occasional assertTrue or assertFalse. You’ll want to move to the next
level quickly, however, and learn to use the most concise and expressive
assertion for the situation at hand.
Armed with a solid understanding of how to write assertions, you’ll next dig
into the organization of test classes so that you can most effectively run and
maintain related groups of tests.
Chapter 5. Examining Outcomes with Assertions • 122
report erratum  •  discuss



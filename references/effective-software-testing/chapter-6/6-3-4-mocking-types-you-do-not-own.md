# 6.3.4 Mocking types you do not own (pp.166-168)

---
**Page 166**

166
CHAPTER 6
Test doubles and mocks
public class ChristmasDiscountTest {
  private final Clock clock = mock(Clock.class);    
  private final ChristmasDiscount cd = new ChristmasDiscount(clock);
  @Test
  public void christmas() {
    LocalDate christmas = LocalDate.of(2015, Month.DECEMBER, 25);
    when(clock.now()).thenReturn(christmas);   
    double finalValue = cd.applyDiscount(100.0);
    assertThat(finalValue).isCloseTo(85.0, offset(0.001));
  }
  @Test
  public void notChristmas() {
    LocalDate notChristmas = LocalDate.of(2015, Month.DECEMBER, 26);
    when(clock.now()).thenReturn(notChristmas);     
    double finalValue = cd.applyDiscount(100.0);
    assertThat(finalValue).isCloseTo(100.0, offset(0.001));
  }
}
As I said, creating an abstraction on top of date and time operations is common. The
idea is that having a class that encapsulates these operations will facilitate the testing
of the other classes in the system, because they are no longer handling date and time
operations. And because these classes now receive this clock abstraction as a depen-
dency, it can be easily stubbed. Martin Fowler’s wiki even has an entry called Clock-
Wrapper, which explains the same thing.
 Is it a problem to use Mockito’s ability to mock static methods? As always, there are
no right and wrong answers. If your system does not have complex date and time
operations, stubbing them using Mockito’s mockStatic() API should be fine. Pragma-
tism always makes sense. 
6.3.4
Mocking types you do not own
Mocking frameworks are powerful. They even allow you to mock classes you do not
own. For example, we could stub the LocalDate class if we wanted to. We can mock
any classes from any library our software system uses. The question is, do we want to?
 When mocking, it is a best practice to avoid mocking types you do not own. Imag-
ine that your software system uses a library. This library is costly, so you decide to mock
it 100% of the time. In the long run, you may face the following complications:
If this library ever changes (for example, a method stops doing what it was sup-
posed to do), you will not have a breaking test. The entire behavior of that
library was mocked. You will only notice it in production. Remember that you
want your tests to break whenever something goes wrong.
Listing 6.20
Testing the new ChristmasDiscount
Clock is a stub.
Stubs the now() 
method to return 
the Christmas date
Stubs the now() 
method. It now 
returns a date that 
is not Christmas.


---
**Page 167**

167
Mocks in the real world
It may be difficult to mock external libraries. Think about the library you use to
access a database such as Hibernate. Mocking all the API calls to Hibernate is
too complex. Your tests will quickly become difficult to maintain.
What is the solution? When you need to mock a type you do not own, you create an
abstraction on top of it that encapsulates all the interactions with that type of library.
In a way, the Clock class we discussed is an example. We do not own the Time API, so
we created an abstraction that encapsulates it. These abstractions will let you hide all
the complexity of that type, offering a much simpler API to the rest of your software
system (which is good for the production code). At the same time, we can easily stub
these abstractions.
 If the behavior of your class changes, you do not have any failing tests anyway, as
your classes depend on the abstraction, not on the real thing. This is not a problem if
you apply the right test levels. In all the classes of the system that depend on this
abstraction, you can mock or stub the dependency. At this point, a change in the type
you do not own will not be caught by the test suite. The abstraction depends on the
contracts of the type before it changed. However, the abstraction itself needs to be
tested using integration tests. These integration tests will break if the type changes.
 Suppose you encapsulate all the behavior of a specific XML parser in an Xml-
Writer class. The abstraction offers a single method: write(Invoice). All the classes
of the system that depend on XmlWriter have write mocked in their unit tests. The
XmlWriter class, which calls the XML parser, will not mock the library. Rather, it will
make calls to the real library and see how it reacts. It will make sure the XML is written
as expected. If the library changes, this one test will break. It will then be up to the
developer to understand what to do, given the new behavior of the type. See figure 6.2
for an illustration.
In practice, unit tests are fast and easy to write and do not depend on external librar-
ies. Integration tests ensure that the interaction with the library happens as expected,
and they capture any changes in the behavior.
Mocks XmlWriter
XmlWriter
(External)
library
A
B
C
ATest
(unit test)
BTest
(unit test)
CTest
(unit test)
XmlWriter
(mock)
XmlWriterTest
(integration test)
Figure 6.2
XmlWriter is 
mocked when the developer 
is testing classes that use it 
(A, B, and C, in the example). 
XmlWriter is then tested 
via integration tests, 
exercising the library.


---
**Page 168**

168
CHAPTER 6
Test doubles and mocks
 Creating abstractions on top of dependencies that you do not own, as a way to gain
more control, is a common technique among developers. (The idea of only mocking
types you own was suggested by Freeman et al. in the paper that introduced the con-
cept of mock objects [2004] and by Mockito.) Doing so increases the overall complex-
ity of the system and requires maintaining another abstraction. But does the ease in
testing the system that we get from adding the abstraction compensate for the cost of
the increased complexity? Often, the answer is yes: it does pay off. 
6.3.5
What do others say about mocking?
As I said, some developers favor mocking, and others do not. Software Engineering at Goo-
gle, edited by Winters, Manshreck, and Wright (2020), has an entire chapter dedicated
to test doubles. Here’s what I understood from it, along with my own point of view:
Using test doubles requires the system to be designed for testability. Indeed, as we saw, if
you use mocks, you need to make sure the class under test can receive the mock.
Building test doubles faithful to the real implementation is challenging. Test doubles must
be as faithful as possible. If your mocks do not offer the same contracts and expec-
tations of the production class, your tests may all pass, but the software system
will fail in production. Whenever you are mocking, make sure your mocks faith-
fully represent the class you are mocking.
Prefer realism over isolation. When possible, opt for the real implementation instead of
fakes, stubs, or mocks. I fully agree with this. Although I did my best to convince
you about the usefulness of mocking (that was the point of this chapter), real-
ism always wins over isolation. I am pragmatic about it, though. If it is getting
too hard to test with the real dependency, I mock it.
The following are trade-offs to consider when deciding whether to use a test
double:
– The execution time of the real implementation—I also take the execution time of
the dependency into account when deciding to mock or not. I usually mock
slow dependencies.
– How much non-determinism we would get from using the real implementation—
While I did not discuss non-deterministic behavior, dependencies that pres-
ent such behavior may be good candidates for mocking.
When using the real implementation is not possible or too costly, prefer fakes over mocks. I
do not fully agree with this recommendation. In my opinion, you either use the
real implementation or mock it. A fake implementation may end up having the
same problems as a mock. How do you ensure that the fake implementation has
the same behavior as the real implementation? I rarely use fakes.
Excessive mocking can be dangerous, as tests become unclear (hard to comprehend), brittle
(may break too often), and less effective (reduced ability to detect faults). I agree. If you
are mocking too much or the class under test forces you to mock too much,
that may be a sign that the production class is poorly designed.



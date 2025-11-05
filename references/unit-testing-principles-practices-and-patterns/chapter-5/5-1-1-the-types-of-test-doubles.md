# 5.1.1 The types of test doubles (pp.93-94)

---
**Page 93**

93
Differentiating mocks from stubs
 This chapter draws heavily on the discussion about the London versus classical
schools of unit testing from chapter 2. In short, the disagreement between the schools
stems from their views on the test isolation issue. The London school advocates isolat-
ing pieces of code under test from each other and using test doubles for all but
immutable dependencies to perform such isolation.
 The classical school stands for isolating unit tests themselves so that they can be
run in parallel. This school uses test doubles only for dependencies that are shared
between tests.
 There’s a deep and almost inevitable connection between mocks and test fragility.
In the next several sections, I will gradually lay down the foundation for you to see why
that connection exists. You will also learn how to use mocks so that they don’t compro-
mise a test’s resistance to refactoring.
5.1
Differentiating mocks from stubs
In chapter 2, I briefly mentioned that a mock is a test double that allows you to exam-
ine interactions between the system under test (SUT) and its collaborators. There’s
another type of test double: a stub. Let’s take a closer look at what a mock is and how it
is different from a stub.
5.1.1
The types of test doubles
A test double is an overarching term that describes all kinds of non-production-ready,
fake dependencies in tests. The term comes from the notion of a stunt double in a
movie. The major use of test doubles is to facilitate testing; they are passed to the
system under test instead of real dependencies, which could be hard to set up or
maintain.
 According to Gerard Meszaros, there are five variations of test doubles: dummy,
stub, spy, mock, and fake.1 Such a variety can look intimidating, but in reality, they can all
be grouped together into just two types: mocks and stubs (figure 5.1).
1 See xUnit Test Patterns: Refactoring Test Code (Addison-Wesley, 2007).
Test double
Mock
(mock, spy)
Stub
(stub, dummy, fake)
Figure 5.1
All variations of test 
doubles can be categorized into 
two types: mocks and stubs.


---
**Page 94**

94
CHAPTER 5
Mocks and test fragility
The difference between these two types boils down to the following:
Mocks help to emulate and examine outcoming interactions. These interactions
are calls the SUT makes to its dependencies to change their state.
Stubs help to emulate incoming interactions. These interactions are calls the
SUT makes to its dependencies to get input data (figure 5.2).
All other differences between the five variations are insignificant implementation
details. For example, spies serve the same role as mocks. The distinction is that spies
are written manually, whereas mocks are created with the help of a mocking frame-
work. Sometimes people refer to spies as handwritten mocks.
 On the other hand, the difference between a stub, a dummy, and a fake is in how
intelligent they are. A dummy is a simple, hardcoded value such as a null value or a
made-up string. It’s used to satisfy the SUT’s method signature and doesn’t partici-
pate in producing the final outcome. A stub is more sophisticated. It’s a fully fledged
dependency that you configure to return different values for different scenarios.
Finally, a fake is the same as a stub for most purposes. The difference is in the ratio-
nale for its creation: a fake is usually implemented to replace a dependency that
doesn’t yet exist.
 Notice the difference between mocks and stubs (aside from outcoming versus
incoming interactions). Mocks help to emulate and examine interactions between the
SUT and its dependencies, while stubs only help to emulate those interactions. This is
an important distinction. You will see why shortly. 
5.1.2
Mock (the tool) vs. mock (the test double)
The term mock is overloaded and can mean different things in different circum-
stances. I mentioned in chapter 2 that people often use this term to mean any test
double, whereas mocks are only a subset of test doubles. But there’s another meaning
System under test
SMTP server
Send an email
Retrieve data
Database
Stub
Mock
Figure 5.2
Sending an email is 
an outcoming interaction: an inter-
action that results in a side effect 
in the SMTP server. A test double 
emulating such an interaction is 
a mock. Retrieving data from the 
database is an incoming inter-
action; it doesn’t result in a 
side effect. The corresponding 
test double is a stub.



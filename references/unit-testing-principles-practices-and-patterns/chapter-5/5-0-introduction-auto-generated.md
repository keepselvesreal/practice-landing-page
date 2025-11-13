# 5.0 Introduction [auto-generated] (pp.92-93)

---
**Page 92**

92
Mocks and test fragility
Chapter 4 introduced a frame of reference that you can use to analyze specific tests
and unit testing approaches. In this chapter, you’ll see that frame of reference in
action; we’ll use it to dissect the topic of mocks.
 The use of mocks in tests is a controversial subject. Some people argue that
mocks are a great tool and apply them in most of their tests. Others claim that mocks
lead to test fragility and try not to use them at all. As the saying goes, the truth lies
somewhere in between. In this chapter, I’ll show that, indeed, mocks often result in
fragile tests—tests that lack the metric of resistance to refactoring. But there are still
cases where mocking is applicable and even preferable.
This chapter covers
Differentiating mocks from stubs
Defining observable behavior and implementation 
details
Understanding the relationship between mocks 
and test fragility
Using mocks without compromising resistance 
to refactoring


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



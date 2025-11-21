# 5.5 Summary (pp.116-119)

---
**Page 116**

116
CHAPTER 5
Mocks and test fragility
systems. That’s because you can’t change those external systems simultaneously with
your application; they may follow a different deployment cycle, or you might simply
not have control over them.
 But when your application acts as a proxy to an external system, and no client can
access it directly, the backward-compatibility requirement vanishes. Now you can deploy
your application together with this external system, and it won’t affect the clients. The
communication pattern with such a system becomes an implementation detail.
 A good example here is an application database: a database that is used only by
your application. No external system has access to this database. Therefore, you can
modify the communication pattern between your system and the application database
in any way you like, as long as it doesn’t break existing functionality. Because that data-
base is completely hidden from the eyes of the clients, you can even replace it with an
entirely different storage mechanism, and no one will notice.
 The use of mocks for out-of-process dependencies that you have a full control over
also leads to brittle tests. You don’t want your tests to turn red every time you split a
table in the database or modify the type of one of the parameters in a stored proce-
dure. The database and your application must be treated as one system.
 This obviously poses an issue. How would you test the work with such a depen-
dency without compromising the feedback speed, the third attribute of a good unit
test? You’ll see this subject covered in depth in the following two chapters. 
5.4.2
Using mocks to verify behavior
Mocks are often said to verify behavior. In the vast majority of cases, they don’t. The
way each individual class interacts with neighboring classes in order to achieve some
goal has nothing to do with observable behavior; it’s an implementation detail.
 Verifying communications between classes is akin to trying to derive a person’s
behavior by measuring the signals that neurons in the brain pass among each other.
Such a level of detail is too granular. What matters is the behavior that can be traced
back to the client goals. The client doesn’t care what neurons in your brain light up
when they ask you to help. The only thing that matters is the help itself—provided by
you in a reliable and professional fashion, of course. Mocks have something to do with
behavior only when they verify interactions that cross the application boundary and
only when the side effects of those interactions are visible to the external world. 
Summary
Test double is an overarching term that describes all kinds of non-production-
ready, fake dependencies in tests. There are five variations of test doubles—
dummy, stub, spy, mock, and fake—that can be grouped in just two types: mocks
and stubs. Spies are functionally the same as mocks; dummies and fakes serve
the same role as stubs.
Mocks help emulate and examine outcoming interactions: calls from the SUT to
its dependencies that change the state of those dependencies. Stubs help


---
**Page 117**

117
Summary
emulate incoming interactions: calls the SUT makes to its dependencies to get
input data.
A mock (the tool) is a class from a mocking library that you can use to create a
mock (the test double) or a stub.
Asserting interactions with stubs leads to fragile tests. Such an interaction doesn’t
correspond to the end result; it’s an intermediate step on the way to that result,
an implementation detail.
The command query separation (CQS) principle states that every method
should be either a command or a query but not both. Test doubles that substi-
tute commands are mocks. Test doubles that substitute queries are stubs.
All production code can be categorized along two dimensions: public API ver-
sus private API, and observable behavior versus implementation details. Code
publicity is controlled by access modifiers, such as private, public, and
internal keywords. Code is part of observable behavior when it meets one of
the following requirements (any other code is an implementation detail):
– It exposes an operation that helps the client achieve one of its goals. An oper-
ation is a method that performs a calculation or incurs a side effect.
– It exposes a state that helps the client achieve one of its goals. State is the cur-
rent condition of the system.
Well-designed code is code whose observable behavior coincides with the public
API and whose implementation details are hidden behind the private API. A
code leaks implementation details when its public API extends beyond the
observable behavior.
Encapsulation is the act of protecting your code against invariant violations.
Exposing implementation details often entails a breach in encapsulation
because clients can use implementation details to bypass the code’s invariants.
Hexagonal architecture is a set of interacting applications represented as hexa-
gons. Each hexagon consists of two layers: domain and application services.
Hexagonal architecture emphasizes three important aspects:
– Separation of concerns between the domain and application services layers.
The domain layer should be responsible for the business logic, while the
application services should orchestrate the work between the domain layer
and external applications.
– A one-way flow of dependencies from the application services layer to the
domain layer. Classes inside the domain layer should only depend on each
other; they should not depend on classes from the application services layer.
– External applications connect to your application through a common inter-
face maintained by the application services layer. No one has a direct access
to the domain layer.
Each layer in a hexagon exhibits observable behavior and contains its own set of
implementation details.


---
**Page 118**

118
CHAPTER 5
Mocks and test fragility
There are two types of communications in an application: intra-system and
inter-system. Intra-system communications are communications between classes
inside the application. Inter-system communication is when the application talks
to external applications.
Intra-system communications are implementation details. Inter-system commu-
nications are part of observable behavior, with the exception of external systems
that are accessible only through your application. Interactions with such sys-
tems are implementation details too, because the resulting side effects are not
observed externally.
Using mocks to assert intra-system communications leads to fragile tests. Mock-
ing is legitimate only when it’s used for inter-system communications—commu-
nications that cross the application boundary—and only when the side effects
of those communications are visible to the external world.


---
**Page 119**

119
Styles of unit testing
Chapter 4 introduced the four attributes of a good unit test: protection against
regressions, resistance to refactoring, fast feedback, and maintainability. These attri-
butes form a frame of reference that you can use to analyze specific tests and unit
testing approaches. We analyzed one such approach in chapter 5: the use of mocks.
 In this chapter, I apply the same frame of reference to the topic of unit testing
styles. There are three such styles: output-based, state-based, and communication-
based testing. Among the three, the output-based style produces tests of the highest
quality, state-based testing is the second-best choice, and communication-based
testing should be used only occasionally.
 Unfortunately, you can’t use the output-based testing style everywhere. It’s only
applicable to code written in a purely functional way. But don’t worry; there are
techniques that can help you transform more of your tests into the output-based
style. For that, you’ll need to use functional programming principles to restructure
the underlying code toward a functional architecture.
This chapter covers
Comparing styles of unit testing
The relationship between functional and 
hexagonal architectures
Transitioning to output-based testing



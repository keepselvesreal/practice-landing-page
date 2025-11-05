# 7.5.1 The cohesion of the class under test (pp.192-193)

---
**Page 192**

192
CHAPTER 7
Designing for testability
2
It invokes the method under test. It can be as simple as a.method() or as com-
plicated as a.precall1(); a.precall2(); a.method(param1, param2, …);. If a
method has pre-conditions before being invoked and/or receiving parameters,
the test should also be responsible for those.
3
It asserts that the method behaves as expected. It can be as simple as assert-
That(return).isEqualTo(42); or as complicated as dozens of lines to
observe what has happened in the system. Again, your test code is responsible
for all the assertions.
You should constantly monitor how hard it is to perform each of these steps. Is it dif-
ficult to instantiate the class under test? Maybe there is a way to design it with fewer
dependencies. Is it hard to invoke the method under test? Maybe there is a way to
design it so its pre-conditions are easier to handle. Is it difficult to assert the out-
come of the method? Maybe there is a way to design it so it is easier to observe what
the method does.
 Next, I will describe some things I pay attention to when writing tests. They give me
feedback about the design and testability of the class I am testing.
7.5.1
The cohesion of the class under test
Cohesion is about a module, a class, a method, or any element in your architecture
having only a single responsibility. Classes with multiple responsibilities are naturally
more complex and harder to comprehend than classes with fewer responsibilities. So,
strive for classes and methods that do one thing. Defining what a single responsibility
means is tricky and highly context-dependent. Nevertheless, sometimes it can be easy
to detect multiple responsibilities in a single element, such as a method that calculates
a specific tax and updates the values of all its invoices.
 Let’s give you some ideas about what you can observe in a test. Note that these tips
are symptoms or indications that something may be wrong with the production code.
It is up to you to make the final decision. Also, note that these tips are solely based on
my experience as a developer and are not scientifically validated:
Non-cohesive classes have very large test suites. They contain a lot of behavior that
needs to be tested. Pay attention to the number of tests you write for a single
class and/or method. If the number of tests grows beyond what you consider
reasonable, maybe it is time to re-evaluate the responsibilities of that class or
method. A common refactoring strategy is to break the class in two.
Non-cohesive classes have test suites that never stop growing. You expect the class to
reach a more stable status at some point. However, if you notice that you are
always going back to the same test class and adding new tests, this may be a bad
design. It is usually related to the lack of a decent abstraction.
– A class that never stops growing breaks both the Single Responsibility (SRP)
and the Open Closed (OCP) principles from the SOLID guidelines. A com-
mon refactoring strategy is to create an abstraction to represent the different


---
**Page 193**

193
Designing for testability in the real world
roles and move each calculation rule to its own class. Google the Strategy
design pattern to see code examples. 
7.5.2
The coupling of the class under test
In a world of cohesive classes, we combine different classes to build large behaviors.
But doing so may lead to a highly coupled design. Excessive coupling may harm evolu-
tion, as changes in one class may propagate to other classes in ways that are not clear.
Therefore, we should strive for classes that are coupled as little as possible.
 Your test code can help you detect highly coupled classes:
If the production class requires you to instantiate many dependencies in your
test code, this may be a sign. Consider redesigning the class. There are different
refactoring strategies you can employ. Maybe the large behavior that the class
implements can be broken into two steps.
– Sometimes coupling is unavoidable, and the best we can do is manage it bet-
ter. Breaking a class enables developers to test it more easily. I will give more
concrete examples of such cases in the following chapters.
Another sign is if you observe a test failing in class ATest (supposedly testing the
behavior of class A), but when you debug it, you find the problem in class B. This
is a clear issue with dependencies: a problem in class B somehow leaked to class A.
It is time to re-evaluate how these classes are coupled and how they interact and
see if such leakages can be prevented in future versions of the system. 
7.5.3
Complex conditions and testability
We have seen in previous chapters that very complex conditions (such as an if state-
ment composed of multiple boolean operations) require considerable effort from tes-
ters. For example, we may devise too many tests after applying boundary testing or
condition + branch coverage criteria. Reducing the complexity of such conditions by,
for example, breaking them into multiple smaller conditions will not reduce the over-
all complexity of the problem but will at least spread it out. 
7.5.4
Private methods and testability
A common question among developers is whether to test private methods. In princi-
ple, testers should test private methods only through their public methods. However,
testers often feel the urge to test a particular private method in isolation.
 A common reason for this feeling is the lack of cohesion or the complexity of the
private method. In other words, this method does something so different from the
public method, and/or its task is so complicated, that it must be tested separately. This
is a good example of the test speaking to us. In terms of design, this may mean the pri-
vate method does not belong in its current place. A common refactoring is to extract
the method, perhaps to a brand new class. There, the former private method, now a
public method, can be tested normally. The original class, where the private method
used to be, should now depend on this new class. 



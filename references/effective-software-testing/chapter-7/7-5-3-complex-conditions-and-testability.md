# 7.5.3 Complex conditions and testability (pp.193-193)

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



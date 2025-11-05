# 4.7 Summary (pp.116-117)

---
**Page 116**

116
CHAPTER 4
Designing contracts
4.6
A method M belongs to a class C and has a pre-condition P and a post-condition
Q. Suppose that a developer creates a class C' that extends C and creates a method
M' that overrides M.
Which one of the following statements correctly explains the relative strength
of the pre- (P') and post-conditions (Q') of the overridden method M'?
A
P' should be equal to or weaker than P, and Q' should be equal to or
stronger than Q.
B
P' should be equal to or stronger than P, and Q' should be equal to or
stronger than Q.
C
P' should be equal to or weaker than P, and Q' should be equal to or
weaker than Q.
D
P' should be equal to or stronger than P, and Q' should be equal to or
weaker than Q.
Summary
Contracts ensure that classes can safely communicate with each other without
surprises.
In practice, designing contracts boils down to explicitly defining the pre-
conditions, post-conditions, and invariants of our classes and methods.
Deciding to go for a weaker or a stronger contract is a contextual decision. Both
have advantages and disadvantages.
Design-by-contract does not remove the need for validation. Validation and con-
tract checking are different things with different objectives. Both should be done.
Whenever changing a contract, we need to reflect on the impact of the change.
Some contract changes might be breaking changes.


---
**Page 117**

117
Property-based testing
So far, we have been doing example-based testing. We judiciously divide the input
space of a program (into partitions), pick one concrete example from all the possi-
ble ones, and write the test case. What if we did not have to pick one concrete
example out of many? What if we could express the property we are trying to exercise
and let the test framework choose several concrete examples for us? Our tests
would be less dependent on a concrete example, and the test framework would be
able to call the method under test multiple times with different input parameters—
usually with zero effort from us.
 This is what property-based testing is about. We do not pick a concrete example;
rather, we define a property (or a set of properties) that the program should
adhere to, and the test framework tries to find a counterexample that causes the
program to break with these properties.
 I have learned that the best way to teach how to write property-based tests is with
multiple examples. So, this chapter presents five different examples with varying
levels of complexity. I want you to focus on my way of thinking and notice how
much creativity is required to write such tests.
This chapter covers
Writing property-based tests
Understanding when to write property-based tests 
or example-based tests



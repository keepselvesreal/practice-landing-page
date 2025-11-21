# 8.2.2 Keep tests DRY (pp.175-175)

---
**Page 175**

175
8.2
Refactoring to increase maintainability
specific role in the system. You can then test that class separately. Michael Feathers’
Working Effectively with Legacy Code (Pearson, 2004) has some good examples of this
technique, and Clean Code by Robert Martin (Pearson, 2008) can help you figure out
when this is a good idea.
MAKING STATELESS PRIVATE METHODS PUBLIC AND STATIC
If your method is completely stateless, some people choose to refactor the method by
making it static (in languages that support this feature). That makes it much more
testable but also states that the method is a sort of utility method that has a known
public contract specified by its name.
8.2.2
Keep tests DRY
Duplication in your unit tests can hurt you, as a developer, just as much as, if not more
than, duplication in production code. That’s because any change in a piece of code
that has duplicates will force you to change all the duplicates as well. When you’re
dealing with tests, there’s more risk of the developer just avoiding this trouble and
deleting or ignoring tests instead of fixing them.
 The DRY (don’t repeat yourself) principle should be in effect in test code just as in
production code. Duplicated code means there’s more code to change when one
aspect you test against changes. Changing a constructor or changing the semantics of
using a class can have a major effect on tests that have a lot of duplicated code.
 As we’ve seen in previous examples in this chapter, using helper functions can help
to reduce duplication in tests. 
WARNING
Removing duplication can also go too far and hurt readability.
We’ll talk about that in the next chapter, on readability.
8.2.3
Avoid setup methods
I’m not a fan of the beforeEach function (also called a setup function) that happens
once before each test and is often used to remove duplication. I much prefer using
helper functions. Setup functions are too easy to abuse. Developers tend to use them
for things they weren’t meant for, and tests become less readable and less maintain-
able as a result. 
 Many developers abuse setup methods in several ways:
Initializing objects in the setup method that are used in only some tests in the file
Having setup code that’s lengthy and hard to understand
Setting up mocks and fake objects within the setup method
Also, setup methods have limitations, which you can get around by using simple
helper methods:
Setup methods can only help when you need to initialize things.
Setup methods aren’t always the best candidates for duplication removal.
Removing duplication isn’t always about creating and initializing new instances



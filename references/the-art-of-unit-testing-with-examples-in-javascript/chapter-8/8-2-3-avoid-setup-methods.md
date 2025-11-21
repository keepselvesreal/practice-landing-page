# 8.2.3 Avoid setup methods (pp.175-176)

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


---
**Page 176**

176
CHAPTER 8
Maintainability
of objects. Sometimes it’s about removing duplication in assertion logic or call-
ing out code in a specific way.
Setup methods can’t have parameters or return values.
Setup methods can’t be used as factory methods that return values. They’re run
before the test executes, so they must be more generic in the way they work.
Tests sometimes need to request specific things or call shared code with a
parameter for the specific test (for example, retrieving an object and setting its
property to a specific value).
Setup methods should only contain code that applies to all the tests in the cur-
rent test class, or the method will be harder to read and understand.
I’ve almost entirely stopped using setup methods for the tests I write. Test code should
be nice and clean, just like production code, but if your production code looks horri-
ble, please don’t use that as a crutch to write unreadable tests. Use factory and helper
methods, and make the world a better place for the generation of developers that will
have to maintain your code in 5 or 10 years.
NOTE
We looked at an example of moving from using beforeEach to helper
functions in section 8.2.3 (listing 8.9) and also in chapter 2.
8.2.4
Use parameterized tests to remove duplication
Another great option for replacing setup methods, if all your tests look the same, is
to use parameterized tests. Different test frameworks in different languages support
parameterized tests—if you’re using Jest, you can use the built-in test.each or it.each
functions. 
 Parameterization helps move the setup logic that would otherwise remain dupli-
cated or would reside in the beforeEach block to the test’s arrange section. It also
helps avoid duplication of the assertion logic, as shown in the following listing.
const sum = numbers => {
    if (numbers.length > 0) {
        return parseInt(numbers);
    }
    return 0;
};
describe('sum with regular tests', () => {
    test('sum number 1', () => {
        const result = sum('1');    
        expect(result).toBe(1);     
    });
    test('sum number 2', () => {
        const result = sum('2');    
        expect(result).toBe(2);     
    });
});
Listing 8.10
Parameterized tests with Jest
Duplicated setup 
and assertion logic



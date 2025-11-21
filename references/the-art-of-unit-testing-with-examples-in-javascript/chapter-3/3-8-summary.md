# 3.8 Summary (pp.81-83)

---
**Page 81**

81
Summary
    verify(input: string):string[] {
        const isWeekend = [SUNDAY, SATURDAY]
            .filter(x => x === this._timeProvider.getDay())
            .length>0;
        if (isWeekend) {
            throw new Error("It's the weekend!")
        }
        return [];
    }
}
class FakeTimeProvider implements TimeProviderInterface{
    fakeDay: number;
    getDay(): number {
        return this.fakeDay;
    }
}
describe('password verifier with interfaces', () => {
    test('on weekends, throws exceptions', () => {
        const stubTimeProvider = new FakeTimeProvider();
        stubTimeProvider.fakeDay = SUNDAY;
        const verifier = new PasswordVerifier([], stubTimeProvider);
        expect(() => verifier.verify('anything'))
            .toThrow("It's the weekend!");
    });
});
We’ve now made a full transition from a purely functional design into a strongly
typed, object-oriented design. Which is best for your team and your project? There’s
no single answer. I’ll talk more about design in chapter 8. Here, I mainly wanted to
show that whatever design you end up choosing, the pattern of injection remains
largely the same. It is just enabled with different vocabulary or language features.
 It’s the ability to inject that enables us to simulate things that would be practically
impossible to test in real life. That’s where the idea of stubs shines the most. We can
tell our stubs to return fake values or even to simulate exceptions in our code, to see
how it handles errors arising from dependencies. Injection makes this possible. Injec-
tion has also made our tests more repeatable, consistent, and trustworthy, and I’ll talk
about trustworthiness in the third part of this book. In the next chapter, we’ll look at
mock objects and see how they differ from stubs.
Summary
Test double is an overarching term that describes all kinds of non-production-
ready, fake dependencies in tests. There are five variations on test doubles that
can be grouped into just two types: mocks and stubs. 
Mocks help emulate and examine outgoing dependencies: dependencies that repre-
sent an exit point of our unit of work. The system under test (SUT) calls outgoing


---
**Page 82**

82
CHAPTER 3
Breaking dependencies with stubs
dependencies to change the state of those dependencies. Stubs help emulate
incoming dependencies: the SUT makes calls to such dependencies to get input data.
Stubs help replace an unreliable dependency with a fake, reliable one and thus
avoid test flakiness.
There are multiple ways to inject a stub into a unit of work:
– Function as parameter—Injecting a function instead of a plain value.
– Partial application (currying) and factory functions—Creating a function that
returns another function with some of the context baked in. This context
may include the dependency you replaced with a stub.
– Module injection—Replacing a module with a fake one with the same API.
This approach is fragile. You may need a lot of refactoring if the module you
are faking changes its API in the future.
– Constructor function—This is mostly the same as partial application.
– Class constructor injection—This is a common object-oriented technique where
you inject a dependency via a constructor.
– Object as parameter (aka duck typing)—In JavaScript, you can inject any depen-
dency in place of the required one as long as that dependency implements
the same functions.
– Common interface as parameter—This is the same as object as parameter, but it
involves a check during compile time. For this approach, you need a strongly
typed language like TypeScript.


---
**Page 83**

83
Interaction testing
using mock objects
In the previous chapter, we solved the problem of testing code that depends on
other objects to run correctly. We used stubs to make sure that the code under
test received all the inputs it needed so that we could test the unit of work in
isolation.
 So far, you’ve only written tests that work against the first two of the three types
of exit points a unit of work can have: returning a value and changing the state of the
system (you can read more about these types in chapter 1). In this chapter, we’ll
look at how you can test the third type of exit point—a call to a third-party func-
tion, module, or object. This is important, because often we’ll have code that
depends on things we can’t control. Knowing how to check that type of code is an
important skill in the world of unit testing. Basically, we’ll find ways to prove that
This chapter covers
Defining interaction testing 
Reasons to use mock objects
Injecting and using mocks
Dealing with complicated interfaces
Partial mocks



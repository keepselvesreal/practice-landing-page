# 3.7.3 Extracting a common interface (pp.79-81)

---
**Page 79**

79
3.7
Object-oriented injection techniques
This code works because JavaScript, by default, is a very permissive language. Much
like Ruby or Python, you can get away with duck typing things. Duck typing refers to the
idea that if it walks like a duck and it talks like a duck, we’ll treat it like a duck. In this
case, the real object and fake object both implement the same function, even though
they are completely different objects. We can simply send one in place of the other,
and the production code should be OK with this.
 Of course, we’ll only know that this is OK and that we didn’t make any mistakes or
miss anything regarding the function signatures at run time. If we want a bit more
confidence, we can try it in a more type-safe manner.
3.7.3
Extracting a common interface
We can take things one step further, and, if we’re using TypeScript or a strongly typed
language such as Java or C#, start using interfaces to denote the roles that our depen-
dencies play. We can create a contract of sorts that both real objects and fake objects
will have to abide by at the compiler level.
 First, we’ll define our new interface (notice that this is now TypeScript code):
export interface TimeProviderInterface {
    getDay(): number;
}
Second, we’ll define a real time provider that implements our interface in our pro-
duction code like this:
import * as moment from "moment";
import {TimeProviderInterface} from "./time-provider-interface";
export class RealTimeProvider implements TimeProviderInterface {
    getDay(): number {
        return moment().day();
    }
}
Third, we’ll update the constructor of our PasswordVerifier to take a dependency of
our new TimeProviderInterface type, instead of having a parameter type of Real-
TimeProvider. We’re abstracting away the role of a time provider and declaring that
we don’t care what object is being passed, as long as it answers to this role’s interface:
export class PasswordVerifier {
    private _timeProvider: TimeProviderInterface;
    constructor(rules: any[], timeProvider: TimeProviderInterface) {
        this._timeProvider = timeProvider;
    }
    verify(input: string):string[] {
        const isWeekened = [SUNDAY, SATURDAY]
            .filter(x => x === this._timeProvider.getDay())
            .length > 0;


---
**Page 80**

80
CHAPTER 3
Breaking dependencies with stubs
        if (isWeekened) {
            throw new Error("It's the weekend!")
        }
         // more logic goes here
        return [];
    }
}
Now that we have an interface that defines what a “duck” looks like, we can implement
a duck of our own in our tests. It’s going to look a lot like the previous test’s code, but
it will have one strong difference: it will be compiler checked to ensure the correct-
ness of the method signatures.
 Here’s what our fake time provider looks like in our test file:
class FakeTimeProvider implements TimeProviderInterface {
    fakeDay: number;
    getDay(): number {
        return this.fakeDay;
    }
}
And here’s our test:
describe('password verifier with interfaces', () => {
    test('on weekends, throws exceptions', () => {
        const stubTimeProvider = new FakeTimeProvider();
        stubTimeProvider.fakeDay = SUNDAY;
        const verifier = new PasswordVerifier([], stubTimeProvider);
        expect(() => verifier.verify('anything'))
            .toThrow("It's the weekend!");
    });
});
The following listing shows all the code together.
export interface TimeProviderInterface {  getDay(): number;  }
 
export class RealTimeProvider implements TimeProviderInterface {
    getDay(): number {
        return moment().day();
    }
}
export class PasswordVerifier {
    private _timeProvider: TimeProviderInterface;
    constructor(rules: any[], timeProvider: TimeProviderInterface) {
        this._timeProvider = timeProvider;
    }
Listing 3.14
Extracting a common interface in production code


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



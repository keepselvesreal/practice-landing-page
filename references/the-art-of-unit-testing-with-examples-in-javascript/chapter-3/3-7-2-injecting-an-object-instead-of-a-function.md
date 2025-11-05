# 3.7.2 Injecting an object instead of a function (pp.76-79)

---
**Page 76**

76
CHAPTER 3
Breaking dependencies with stubs
test maintainability, and it can work with object-oriented and functional production
code because it hides how the function or object is being created or configured. It’s
an abstraction layer in our tests, so we can push the dependency on how a function or
object is created or configured into a single place in our tests.
3.7.2
Injecting an object instead of a function
Right now, our class constructor takes in a function as the second parameter:
constructor(rules, dayOfWeekFn) {
    this.rules = rules;
    this.dayOfWeek = dayOfWeekFn;
}
Let’s go one step up in our object-oriented design and use an object instead of a func-
tion as our parameter. This requires us to do a bit of legwork: refactor the code.
 First, we’ll create a new file called time-provider.js, which will contain our real
object that has a dependency on moment.js. The object will be designed to have a sin-
gle function called getDay():
import moment from "moment";
const RealTimeProvider = () =>  {
    this.getDay = () => moment().day()
};
Next, we’ll change the parameter usage to use an object with a function:
const SUNDAY = 0, MONDAY = 1, SATURDAY = 6;
class PasswordVerifier {
    constructor(rules, timeProvider) {
        this.rules = rules;
        this.timeProvider = timeProvider;
    }
    verify(input) {
        if ([SATURDAY, SUNDAY].includes(this.timeProvider.getDay())) {
            throw new Error("It's the weekend!");
        }
    ...
}
Finally, let’s give whoever needs an instance of our PasswordVerifier the ability to
get it preconfigured with the real time provider by default. We’ll do this with a new
passwordVerifierFactory function that any production code that needs a verifier
instance will need to use:
const passwordVerifierFactory = (rules) => {
    return new PasswordVerifier(new RealTimeProvider())
};


---
**Page 77**

77
3.7
Object-oriented injection techniques
The following listing shows the entire piece of new code.
import moment from "moment";
const RealTimeProvider = () =>  {
    this.getDay = () => moment().day()
};
const SUNDAY = 0, MONDAY=1, SATURDAY = 6;
class PasswordVerifier {
    constructor(rules, timeProvider) {
        this.rules = rules;
        this.timeProvider = timeProvider;
    }
    verify(input) {
        if ([SATURDAY, SUNDAY].includes(this.timeProvider.getDay())) {
            throw new Error("It's the weekend!");
        }
        const errors = [];
        //more code goes here..
        return errors;
    };
}
const passwordVerifierFactory = (rules) => {
    return new PasswordVerifier(new RealTimeProvider())
};
IoC containers and dependency injection
There are many other ways to glue PasswordVerifier and TimeProvider together.
I’ve just chosen manual injection to keep things simple. Many frameworks today are
able to configure the injection of dependencies into objects under test, so that we
can define how an object is to be constructed. Angular is one such framework. 
If you’re using libraries like Spring in Java or Autofac or StructureMap in C#, you can
easily configure the construction of objects with constructor injection without needing
to create specialized functions. Commonly, these features are called Inversion of
Control (IoC) containers or Dependency Injection (DI) containers. I’m not using them
in this book to avoid unneeded details. You don’t need them to create great tests. 
In fact, I don’t normally use IoC containers in tests. I’ll almost always use custom
factory functions to inject dependencies. I find that makes my tests easier to read
and reason about. 
Even for tests covering Angular code, we don’t have to go through Angular’s DI frame-
work to inject a dependency into an object in memory; we can call that object’s con-
structor directly and send in fake stuff. As long as we do that in a factory function,
we’re not sacrificing maintainability, and we’re also not adding extra code to tests
unless it’s essential to the tests.
Listing 3.12
Injecting an object


---
**Page 78**

78
CHAPTER 3
Breaking dependencies with stubs
How can we handle this type of design in our tests, where we need to inject a fake
object, instead of a fake function? We’ll do this manually at first, so you can see that
it’s not a big deal. Later, we’ll let frameworks help us, but you’ll see that sometimes
hand-coding fake objects can actually make your test more readable than using a
framework, such as Jasmine, Jest, or Sinon (we’ll cover those in chapter 5).
 First, in our test file, we’ll create a new fake object that has the same function sig-
nature as our real time provider, but it will be controllable by our tests. In this case,
we’ll just use a constructor pattern:
function FakeTimeProvider(fakeDay) {
    this.getDay = function () {
        return fakeDay;
    }
}
NOTE
If you are working in a more object-oriented style, you might choose to
create a simple class that inherits from a common interface. We’ll cover that a
bit later in the chapter.
Next, we’ll construct the FakeTimeProvider in our tests and inject it into the verifier
under test:
describe('verifier', () => {
    test('on weekends, throws exception', () => {
        const verifier = 
             new PasswordVerifier([], new FakeTimeProvider(SUNDAY));
        expect(()=> verifier.verify('anything'))
            .toThrow("It's the weekend!");
    });
Here’s what the full test file looks like.
function FakeTimeProvider(fakeDay) {
    this.getDay = function () {
        return fakeDay;
    }
}
describe('verifier', () => {
    test('class constructor: on weekends, throws exception', () => {
        const verifier = 
            new PasswordVerifier([], new FakeTimeProvider(SUNDAY));
        expect(() => verifier.verify('anything'))
            .toThrow("It's the weekend!");
    });
}); 
Listing 3.13
Creating a handwritten stub object


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



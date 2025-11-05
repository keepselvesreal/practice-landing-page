# 3.7.1 Constructor injection (pp.74-76)

---
**Page 74**

74
CHAPTER 3
Breaking dependencies with stubs
const {Verifier} = require("./password-verifier-time01");
test('constructor function: on weekends, throws exception', () => {
    const alwaysSunday = () => SUNDAY;
    const verifier = new Verifier([], alwaysSunday);
    expect(() => verifier.verify('anything'))
        .toThrow("It's the weekend!");
});
You might look at this and ask, “Why move toward objects?” The answer really depends
on the context of your current project, its stack, your team’s knowledge of functional
programming and object-oriented background, and many other non-technical fac-
tors. It’s good to have this tool in your toolbox so you can use it when it makes sense to
you. Keep this in the back of your mind as you read the next few sections.
3.7
Object-oriented injection techniques
If a more object-oriented style is what you’re leaning toward, or if you’re working in
an object-oriented language such as C# or Java, here are a few common patterns that
are widely used in the object-oriented world for dependency injection.
3.7.1
Constructor injection
Constructor injection is how I would describe a design in which we can inject dependen-
cies through the constructor of a class. In the JavaScript world, Angular is the best-
known web frontend framework that uses this design for injecting “services,” which is
just a code word for “dependencies” in Angular-speak. This is a viable design in many
other situations. 
 Having a stateful class is not without benefits. It can remove repetition from clients
that only need to configure our class once and can then reuse the configured class
multiple times. 
 If we had chosen to create a stateful version of Password Verifier, and we wanted
to inject the date function through constructor injection, it might look like the fol-
lowing design. 
class PasswordVerifier {
    constructor(rules, dayOfWeekFn) {
        this.rules = rules;
        this.dayOfWeek = dayOfWeekFn;
    }
    verify(input) {
        if ([SATURDAY, SUNDAY].includes(this.dayOfWeek())) {
            throw new Error("It's the weekend!");
        }
        const errors = [];
        //more code goes here..
Listing 3.10
Constructor injection design


---
**Page 75**

75
3.7
Object-oriented injection techniques
        return errors;
    };
}
test('class constructor: on weekends, throws exception', () => {
    const alwaysSunday = () => SUNDAY;
    const verifier = new PasswordVerifier([], alwaysSunday);
    expect(() => verifier.verify('anything'))
        .toThrow("It's the weekend!");
});
This looks and feels a lot like the constructor function design in section 3.6. This is a
more class-oriented design that many people will feel more comfortable with, coming
from an object-oriented background. It also is more verbose. You’ll see that we get
more and more verbose the more object-oriented we make things. It’s part of the
object-oriented game. This is partly why people are choosing functional styles more
and more—they are much more concise.
 Let’s talk a bit about the maintainability of the tests. If I wrote a second test with
this class, I’d extract the creation of the class via the constructor to a nice little factory
function that returns an instance of the class under test, so that if (i.e., “when”) the
constructor signature changes and breaks many tests at once, I only have to fix a single
place to get all the tests working again, as you can see in the following listing.
describe('refactored with constructor', () => {
    const makeVerifier = (rules, dayFn) => {
        return new PasswordVerifier(rules, dayFn);
    };
    test('class constructor: on weekends, throws exceptions', () => {
        const alwaysSunday = () => SUNDAY;
        const verifier = makeVerifier([],alwaysSunday);
        expect(() => verifier.verify('anything'))
            .toThrow("It's the weekend!");
    });
    test('class constructor: on weekdays, with no rules, passes', () => { 
        const alwaysMonday = () => MONDAY;
        const verifier = makeVerifier([],alwaysMonday);
        const result = verifier.verify('anything');
        expect(result.length).toBe(0);
    });
});
Notice that this is not the same as the factory function design in section 3.4.2. This fac-
tory function resides in our tests; the other was in our production code. This one is for
Listing 3.11
Adding a helper factory function to our tests


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



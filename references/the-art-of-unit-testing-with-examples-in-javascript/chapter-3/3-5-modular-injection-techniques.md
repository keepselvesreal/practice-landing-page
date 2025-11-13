# 3.5 Modular injection techniques (pp.70-73)

---
**Page 70**

70
CHAPTER 3
Breaking dependencies with stubs
There’s very little difference from the previous test, but using a function as a parame-
ter is a valid way to do injection. In other scenarios, it’s also a great way to enable spe-
cial behavior, such as simulating special cases or exceptions in your code under test.
3.4.2
Dependency injection via partial application
Factory functions or methods (a subcategory of “higher-order functions”) are func-
tions that return other functions, preconfigured with some context. In our case, the
context can be the list of rules and the current day function. We then get back a new
function that we can trigger with only a string input, and it will use the rules and get-
Day() function configured in its creation. 
 The code in the following listing essentially turns the factory function into the
arrange part of the test, and calls the returned function into the act part. Quite lovely.
const SUNDAY = 0, . . . FRIDAY=5, SATURDAY = 6;
const makeVerifier = (rules, dayOfWeekFn) => {
    return function (input) {
        if ([SATURDAY, SUNDAY].includes(dayOfWeekFn())) {
            throw new Error("It's the weekend!");
        }
        //more code goes here..
    };
};
describe('verifier', () => {
    test('factory method: on weekends, throws exceptions', () => {
        const alwaysSunday = () => SUNDAY;
        const verifyPassword = makeVerifier([], alwaysSunday);
        expect(() => verifyPassword('anything'))
            .toThrow("It's the weekend!");
    });
3.5
Modular injection techniques
JavaScript also allows for the idea of modules, which we import or require. How can we
handle the idea of dependency injection when faced with a direct import of a depen-
dency in our code under test, such as in the code from listing 3.1, shown again here?
const moment = require('moment');
const SUNDAY = 0; const SATURDAY = 6;
const verifyPassword = (input, rules) => {
    const dayOfWeek = moment().day();
    if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
        throw Error("It's the weekend!");
    }
Listing 3.6
Using a higher-order factory function


---
**Page 71**

71
3.5
Modular injection techniques
    // more code goes here...
    // return list of errors found..
    return [];
};
How can we overcome this direct dependency that’s happening? The answer is, we
can’t. We’ll have to write the code differently to allow for the replacement of that
dependency later on. We’ll have to create a seam through which we can replace our
dependencies. Here’s one such example.
const originalDependencies = {    
    moment: require(‘moment’),    
};                                
let dependencies = { ...originalDependencies };     
const inject = (fakes) => {          
    Object.assign(dependencies, fakes);
    return function reset() {                    
        dependencies = { ...originalDependencies };
    }
};
const SUNDAY = 0; const SATURDAY = 6;
const verifyPassword = (input, rules) => {
    const dayOfWeek = dependencies.moment().day();
    if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
        throw Error("It's the weekend!");
    }
    // more code goes here...
    // return list of errors found..
    return [];
};
module.exports = {
    SATURDAY,
    verifyPassword,
    inject
};
What’s going on here? Three new things have been introduced:
First, we have replaced our direct dependency on moment.js with an object:
originalDependencies. It contains that module import as part of its
implementation. 
Next, we have added yet another object into the mix: dependencies. This
object, by default, takes on all of the real dependencies that the original-
Dependencies object contains. 
Listing 3.7
Abstracting the required dependencies
Wrapping moment.js 
with an intermediary 
object
The object containing 
the current dependency, 
either real or fake
A function that replaces the real 
dependency with a fake one
A function that resets 
the dependency back 
to the real one


---
**Page 72**

72
CHAPTER 3
Breaking dependencies with stubs
Finally, the inject function, which we’re also exposing as part of our own mod-
ule, allows whoever is importing our module (both production code and tests)
to override our real dependencies with custom dependencies (fakes). 
When you invoke inject, it returns a reset function that reapplies the origi-
nal dependencies onto the current dependencies variable, thus resetting any
fakes currently being used. 
Here’s how you can use the inject and reset functions in a test.
const { inject, verifyPassword, SATURDAY } = require('./password-verifier-
time00-modular');
const injectDate = (newDay) => {  
    const reset = inject({       
        moment: function () {
            //we're faking the moment.js module's API here.
            return {
                day: () => newDay
            }
        }
    });
    return reset;
};
describe('verifyPassword', () => {
    describe('when its the weekend', () => {
        it('throws an error', () => {
            const reset = injectDate(SATURDAY);   
            expect(() => verifyPassword('any input'))
                .toThrow("It's the weekend!");
            reset();   
        });
    });
});
Let’s break down what’s going on here:
1
The injectDate function is just a helper function meant to reduce the boiler-
plate code in our test. It always builds the fake structure of the moment.js API,
and it sets its getDay function to return the newDay parameter.
2
The injectDate function calls inject with the new fake moment.js API. This
applies the fake dependency in our unit of work to the one we have sent in as a
parameter. 
3
Our test calls the inject function with a custom, fake day.
4
At the end of the test, we call the reset function, which resets the unit of work’s
module dependencies to the original ones. 
Listing 3.8
Injecting a fake module with inject()
A helper function
Injecting a fake API 
instead of moment.js
Providing a 
fake day
Resetting the 
dependency


---
**Page 73**

73
3.6
Moving toward objects with constructor functions
Once you’ve done this a couple of times, it starts making sense. But it has some caveats
as well. On the pro side, it definitely takes care of the dependency issue in our tests,
and it’s relatively easy to use. As for the cons, there is one huge downside as far as I can
see. Using this method to fake our modular dependencies forces our tests to be
closely tied to the API signature of the dependencies we are faking. If these are third-
party dependencies, such as moment.js, loggers, or anything else that we do not fully
control, our tests will become very brittle when the time comes (as it always does) to
upgrade or replace the dependencies with something that has a different API. This
doesn’t hurt much if it’s just a test or two, but we’ll usually have hundreds or thou-
sands of tests that have to fake several common dependencies, and that sometimes
means changing and fixing hundreds of files when replacing a logger with a breaking
API change, for example. 
 I have two possible ways to prevent such a situation:
Never import a third-party dependency that you don’t control directly in your
code. Always use an interim abstraction that you do control. The Ports and
Adapters architecture is a good example of such an idea (other names for this
architecture are Hexagonal architecture and Onion architecture). With such
an architecture, faking these internal APIs should present less risk, because
we can control their rate of change, thus making our tests less brittle. (We can
refactor them internally without our tests caring, even if the outside world
changes.)
Avoid using module injection, and instead use one of the other ways mentioned
in this book for dependency injection: function parameters, currying, and, as
mentioned in the next section, constructors and interfaces. Between these, you
should have plenty of choices instead of importing things directly. 
3.6
Moving toward objects with constructor functions
Constructor functions are a slightly more object-oriented JavaScript-ish way of achiev-
ing the same result as a factory function, but they return something akin to an object
with methods we can trigger. We then use the keyword new to call this function and get
back that special object. 
 Here’s what the same code and tests look like with this design choice.
const Verifier = function(rules, dayOfWeekFn)
{
    this.verify = function (input) {
        if ([SATURDAY, SUNDAY].includes(dayOfWeekFn())) {
            throw new Error("It's the weekend!");
        }
        //more code goes here..
    };
};
Listing 3.9
Using a constructor function



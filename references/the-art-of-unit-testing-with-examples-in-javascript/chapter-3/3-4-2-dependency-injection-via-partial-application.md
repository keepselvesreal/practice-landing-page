# 3.4.2 Dependency injection via partial application (pp.70-70)

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



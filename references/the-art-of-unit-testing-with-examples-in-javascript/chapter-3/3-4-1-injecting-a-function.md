# 3.4.1 Injecting a function (pp.69-70)

---
**Page 69**

69
3.4
Functional injection techniques
Seams in production code play an important role in the maintainability and readabil-
ity of unit tests. The easier it is to change and inject behavior or custom data into the
code under test, the easier it will be to write, read, and later on maintain the test as
the production code changes. I’ll talk more about some patterns and antipatterns
related to designing code in chapter 8.
3.4
Functional injection techniques
At this point, we might not be happy with our design choice. Adding a parameter did
solve the dependency issue at the function level, but now every caller will need to
know how to handle dates in some way. It feels a bit too chatty. 
 JavaScript enables two major styles of programming—functional and object-
oriented—so I’ll show approaches in both styles when it makes sense, and you can
pick and choose what works best in your situation.
 There isn’t a single way to design something. Functional programming proponents
will argue for the simplicity, clarity, and provability of the functional style, but it does
come with a learning curve. For that reason alone, it is wise to learn both approaches
so that you can apply whichever works best for the team you’re working with. Some
teams will lean more toward object-oriented designs because they feel more comfort-
able with that. Others will lean towards functional designs. I’d argue that the patterns
remain largely the same; we just translate them to different styles. 
3.4.1
Injecting a function
The following listing shows a different refactoring for the same problem: instead of a
data object, we’re expecting a function as the parameter. That function returns the
date object.
const verifyPassword3 = (input, rules, getDayFn) => {
    const dayOfWeek = getDayFn();
    if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
        throw Error("It's the weekend!");
    }
    //more code goes here...
    //return list of errors found..
    return [];
};
The associated test is shown in the following listing.
describe('verifier3 - dummy function', () => {
    test('on weekends, throws exceptions', () => {
        const alwaysSunday = () => SUNDAY;
        expect(()=> verifyPassword3('anything',[], alwaysSunday))
            .toThrow("It's the weekend!");
    });
Listing 3.4
Dependency injection with a function
Listing 3.5
Testing with function injection


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



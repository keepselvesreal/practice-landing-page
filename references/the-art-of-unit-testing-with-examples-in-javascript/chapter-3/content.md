# Breaking dependencies with stubs (pp.61-83)

---
**Page 61**

61
Breaking dependencies
with stubs
In the previous chapter, you wrote your first unit test using Jest, and we looked
more at the maintainability of the test itself. The scenario was pretty simple, and
more importantly, it was completely self-contained. The Password Verifier had no
reliance on outside modules, and we could focus on its functionality without worry-
ing about other things that might interfere with it. 
 In that chapter, we used the first two types of exit points for our examples:
return value exit points and state-based exit points. In this chapter, we’ll talk about
the final type—calling a third party. This chapter will also present a new require-
ment—having your code rely on time. We’ll look at two different approaches to
handling it—refactoring our code and monkey-patching it without refactoring.
 The reliance on outside modules or functions can and will make it harder to
write a test and to make the test repeatable, and it can also cause tests to be flaky.
This chapter covers
Types of dependencies—mocks, stubs, and more
Reasons to use stubs
Functional injection techniques
Modular injection techniques
Object-oriented injection techniques


---
**Page 62**

62
CHAPTER 3
Breaking dependencies with stubs
We call the external things that we rely on in our code dependencies. I’ll define them
more thoroughly later in the chapter. These dependencies could include things like
time, async execution, using the filesystem, or using the network, or they could simply
involve using something that is very difficult to configure or that may be time consum-
ing to execute.
3.1
Types of dependencies
In my experience, there are two main types of dependencies that our unit of work
can use:
Outgoing dependencies—Dependencies that represent an exit point of our unit of
work, such as calling a logger, saving something to a database, sending an email,
notifying an API or a webhook that something has happened, etc. Notice these
are all verbs: “calling,” “sending,” and “notifying.” They are flowing outward from
the unit of work in a sort of fire-and-forget scenario. Each represents an exit
point, or the end of a specific logical flow in a unit of work.
Incoming dependencies—Dependencies that are not exit points. These do not rep-
resent a requirement on the eventual behavior of the unit of work. They are
merely there to provide test-specific specialized data or behavior to the unit of
work, such as a database query’s result, the contents of a file on the filesystem, a
network response, etc. Notice that these are all passive pieces of data that flow
inward to the unit of work as the result of a previous operation. 
Figure 3.1 shows these side by side.
Test
Entry point
Exit point
Data
or behavior
Dependency
Unit
of
work
Test
Entry point
Exit point
Dependency
Unit
of
work
Outgoing dependency
Incoming dependency
Figure 3.1
On the left, an exit point is implemented as invoking a dependency. On the right, the dependency 
provides indirect input or behavior and is not an exit point.


---
**Page 63**

63
3.1
Types of dependencies
Some dependencies can be both incoming and outgoing—in some tests they will rep-
resent exit points, and in other tests they will be used to simulate data coming into the
application. These shouldn’t be very common, but they do exist, such as an external
API that returns a success/fail response for an outgoing message.
 With these types of dependencies in mind, let’s look at how the book xUnit Test Pat-
terns defines the various patterns for things that look like other things in tests.
Table 3.1 lists my thoughts about some patterns from the book’s website at http://
mng.bz/n1WK.
Here’s another way to think about this for the rest of this book:
Stubs break incoming dependencies (indirect inputs). Stubs are fake modules,
objects, or functions that provide fake behavior or data into the code under test.
We do not assert against them. We can have many stubs in a single test.
Mocks break outgoing dependencies (indirect outputs or exit points). Mocks
are fake modules, objects, or functions that we assert were called in our tests. A
mock represents an exit point in a unit test. Because of this, it is recommended
that you have no more than a single mock per test.
Unfortunately, in many shops you’ll hear the word “mock” thrown around as a catch-
all term for both stubs and mocks. Phrases like “we’ll mock this out” or “we have a
mock database” can really create confusion. There is a huge difference between stubs
Table 3.1
Clarifying terminology around stubs and mocks
Category
Pattern
Purpose
Uses
Test double
Generic name for stubs and 
mocks
I also use the term fake.
Stub
Dummy object
Used to specify the values to 
be used in tests when the only 
usage is as irrelevant argu-
ments of SUT method calls
Send as a parameter to the 
entry point or as the arrange 
part of the AAA pattern.
Test stub
Used to verify logic inde-
pendently when it depends on 
indirect inputs from other soft-
ware components
Inject as a dependency, and 
configure it to return specific 
values or behavior into the SUT.
Mock
Test spy
Used to verify logic inde-
pendently when it has indirect 
outputs to other software com-
ponents
Override a single function on a 
real object, and verify that the 
fake function was called as 
expected.
Mock object
Used to verify logic inde-
pendently when it depends on 
indirect outputs to other soft-
ware components
Inject the fake as a depen-
dency into the SUT, and verify 
that the fake was called as 
expected.


---
**Page 64**

64
CHAPTER 3
Breaking dependencies with stubs
and mocks (one should really only be used once in a test), and we should use the right
terms to ensure it’s clear what the other person is referring to. 
 When in doubt, use the term “test double” or “fake.” Often, a single fake depen-
dency can be used as a stub in one test, and it can be used as a mock in another test.
We’ll see an example of this later on. 
This might seem like a whole lot of information at once. I’ll dive deep into these defi-
nitions throughout this chapter. Let’s take a small bite and start with stubs.
3.2
Reasons to use stubs
What if we’re faced with the task of testing a piece of code like the following?
const moment = require('moment');
const SUNDAY = 0, SATURDAY = 6;
const verifyPassword = (input, rules) => {
    const dayOfWeek = moment().day();
    if ([SATURDAY, SUNDAY].includes(dayOfWeek)) {
        throw Error("It's the weekend!");
    }
    //more code goes here...
    //return list of errors found..
    return [];
};
Our password verifier has a new dependency: it can’t work on weekends. Go figure. Spe-
cifically, the module has a direct dependency on moment.js, which is a very common
date/time wrapper for JavaScript. Working with dates directly in JavaScript is not a pleas-
ant experience, so we can assume many shops out there have something like this. 
XUnit test patterns and naming things
xUnit Test Patterns: Refactoring Test Code by Gerard Meszaros (Addison-Wesley,
2007) is a classic pattern reference book for unit testing. It defines patterns for
things you fake in your tests in at least five ways. Once you’ve gotten a feel for the
three types I mention here, I encourage you to take a look at the extra details that
book provides. 
Note that xUnit Test Patterns has a definition for the word “fake”: “Replace a compo-
nent that the system under test (SUT) depends on with a much lighter-weight imple-
mentation.” For example, you might use an in-memory database instead of a full-
fledged production instance. 
I still consider this type of test double a “stub,” and I use the word “fake” to call out
anything that isn’t real, much like the term “test double,” but “fake” is shorter and
easier on the tongue.
Listing 3.1
verifyPassword using time


---
**Page 65**

65
3.2
Reasons to use stubs
 How does this direct use of a time-related library affect our unit tests? The unfor-
tunate issue here is that this direct dependency forces our tests, given no direct way
to affect date and time inside our application under test, to take into account the
correct date and time. The following listing shows an unfortunate test that only runs
on weekends.
const moment = require('moment');
const {verifyPassword} = require("./password-verifier-time00");
const SUNDAY = 0, SATURDAY = 6, MONDAY = 2;
describe('verifier', () => {
    const TODAY = moment().day();
    //test is always executed, but might not do anything
    test('on weekends, throws exceptions', () => {
        if ([SATURDAY, SUNDAY].includes(TODAY)) {    
            expect(()=> verifyPassword('anything',[]))
                .toThrow("It's the weekend!");
        }
    });
    //test is not even executed on week days
    if ([SATURDAY, SUNDAY].includes(TODAY)) {       
        test('on a weekend, throws an error', () => {
            expect(()=> verifyPassword('anything', []))
                .toThrow("It's the weekend!");
        });
    }
});
The preceding listing includes two variations on the same test. One checks for the cur-
rent date inside the test, and the other has the check outside the test, which means the
test never even executes unless it’s the weekend. This is bad. 
 Let’s revisit one of the good test qualities mentioned in chapter 1, consistency:
Every time I run a test, it is the same exact test that I ran before. The values being used
do not change. The asserts do not change. If no code has changed (in test or produc-
tion code), then the test should provide the exact same result as previous runs.
 The second test sometimes doesn’t even run. That’s a good enough reason to use a
fake to break the dependency right there. Furthermore, we can’t simulate a weekend
or a weekday, which gives us more than enough incentive to redesign the code under
test so it’s a bit more injectable for dependencies.
 But wait, there’s more. Tests that use time can often be flaky. They only fail
sometimes, without anything but the time changing. This test is a prime candidate
for this behavior, because we’ll only get feedback on one of its two states when we
run it locally. If you want to know how it behaves on a weekend, just wait a couple of
days. Ugh.
Listing 3.2
Initial unit tests for verifyPassword
Checking the 
date inside 
the test
Checking the 
date outside 
the test


---
**Page 66**

66
CHAPTER 3
Breaking dependencies with stubs
 Tests might become flaky due to edge cases that affect variables that are not under
our control in the test. Common examples are network issues during end-to-end testing,
database connectivity issues, or various server issues. When this happens, it’s easy to
dismiss the test failure by saying “just run it again” or “It’s OK. It’s just [insert variabil-
ity issue here].”
3.3
Generally accepted design approaches to stubbing
In the next few sections, we’ll discuss several common forms of injecting stubs into
our units of work. First, we’ll discuss basic parameterization as a first step, then we’ll
jump into the following approaches:
Functional approaches
– Function as parameter
– Partial application (currying)
– Factory functions 
– Constructor functions 
Modular approach
– Module injection
Object-oriented approaches
– Class constructor injection
– Object as parameter (aka duck typing)
– Common interface as parameter (for this we’ll use TypeScript)
We’ll tackle each of these by starting with the simple case of controlling time in our
tests.
3.3.1
Stubbing out time with parameter injection
I can think of at least two good reasons to control time based on what we’ve covered
so far:
To remove the variability from our tests
To easily simulate any time-related scenario we’d like to test our code with
Here’s the simplest refactoring I can think of that makes things a bit more repeatable.
Let’s add a currentDay parameter to our function to specify the current date. This will
remove the need to use the moment.js module in our function, and it will put that
responsibility on the caller of the function. That way, in our tests, we can determine
the time in a hardcoded manner and make the test and the function repeatable and
consistent. The following listing shows an example of such a refactoring.
const verifyPassword2 = (input, rules, currentDay) => {
    if ([SATURDAY, SUNDAY].includes(currentDay)) {
        throw Error("It's the weekend!");
Listing 3.3
verifyPassword with a currentDay parameter


---
**Page 67**

67
3.3
Generally accepted design approaches to stubbing
    }
    //more code goes here...
    //return list of errors found..
    return [];
};
const SUNDAY = 0, SATURDAY = 6, MONDAY = 1;
describe('verifier2 - dummy object', () => {
    test('on weekends, throws exceptions', () => {
        expect(() => verifyPassword2('anything',[],SUNDAY ))
            .toThrow("It's the weekend!");
    });
});
By adding the currentDay parameter, we’re essentially giving control over time to the
caller of the function (our test). What we’re injecting is formally called a “dummy”—
it’s just a piece of data with no behavior—but we can call it a “stub” from now on. 
 This is approach is a form of Dependency Inversion. It seems the term “Inversion of
Control” first came up in Johnson and Foote’s paper “Designing Reusable Classes,”
published by the Journal of Object-Oriented Programming in 1988. The term “Dependency
Inversion” is also one of the SOLID patterns described by Robert C. Martin in 2000, in
his “Design Principles and Design Patterns” paper. I’ll talk more about higher-level
design considerations in chapter 8. 
 Adding this parameter is a simple refactoring, but it’s quite effective. It provides a
couple of nice benefits other than consistency in the test:
We can now easily simulate any day we want.
The code under test is not responsible for managing time imports, so it has one
less reason to change if we ever use a different time library.
We’re doing “dependency injection” of time into our unit of work. We’ve changed the
design of the entry point to use a day value as a parameter. The function is now “pure”
by functional programming standards in that it has no side effects. Pure functions
have built-in injections of all of their dependencies, which is one of the reasons you’ll
find functional programming designs are typically much easier to test.
 It might feel weird to call the currentDay parameter a stub if it’s just a day integer
value, but based on the definitions from xUnit Test Patterns, we can say that this is a
“dummy” value, and as far as I’m concerned, it falls into the “stub” category. It does
not have to be complex in order to be a stub. It just has to be under our control. It’s a
stub because we are using it to simulate some input or behavior being passed into the
unit under test. Figure 3.2 shows this visually.


---
**Page 68**

68
CHAPTER 3
Breaking dependencies with stubs
3.3.2
Dependencies, injections, and control
Table 3.2 recaps some important terms we’ve discussed and are about to use through-
out the rest of the chapter.
Table 3.2
Terminology used in this chapter
Dependencies
The things that make our testing lives and code maintainability difficult, since we can-
not control them from our tests. Examples include time, the filesystem, the network, 
random values, and more.
Control
The ability to instruct a dependency how to behave. Whoever is creating the dependen-
cies is said to be in control of them, since they have the ability to configure them 
before they are used in the code under test. 
In listing 3.1, our test does not have control over time because the module under test 
has control over it. The module has chosen to always use the current date and time. This 
forces the test to do the exact same thing, and thus we lose consistency in our tests. 
In listing 3.3, we have gained access to the dependency by inverting the control over it 
via the currentDay parameter. Now the test has control over the time and can decide 
to use a hardcoded time. The module under test has to use the time provided, which 
makes things much easier for our test.
Inversion of 
control
Designing the code to remove the responsibility of creating the dependency internally, 
and externalizing it instead. Listing 3.3 shows one way of doing this with parameter 
injection.
Dependency 
injection
The act of sending a dependency through the design interface to be used internally by a 
piece of code. The place where you inject the dependency is the injection point. In our 
case, we are using a parameter injection point. Another word for this place where we 
can inject things is a seam.
Seam
Pronounced “s-ee-m,” and coined by Michael Feathers in his book Working Effectively 
with Legacy Code (Pearson, 2004).
Seams are where two pieces of software meet and something else can be injected. 
They are a place where you can alter behavior in your program without editing in that 
place. Examples include parameters, functions, module loaders, function rewriting, 
and, in the object-oriented world, class interfaces, public virtual methods, and more.
verify(input, rules, dayStub)
Return value
Test
Stub
Time
Figure 3.2
Injecting a stub 
for a time dependency


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



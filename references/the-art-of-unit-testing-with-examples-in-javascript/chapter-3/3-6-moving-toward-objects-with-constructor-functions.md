# 3.6 Moving toward objects with constructor functions (pp.73-74)

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



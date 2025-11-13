# 3.3.2 Dependencies, injections, and control (pp.68-69)

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



# 1.3 Entry points and exit points (pp.6-11)

---
**Page 6**

6
CHAPTER 1
The basics of unit testing
is often an entire interface, such as a class, or an individual method (https://en
.wikipedia.org/wiki/Unit_testing).
The thing you’ll write tests for is the subject, system, or suite under test (SUT).
DEFINITION
SUT stands for subject, system, or suite under test, and some people
like to use CUT (component, class, or code under test). When you test something,
you refer to the thing you’re testing as the SUT.
Let’s talk about the word “unit” in unit testing. To me, unit stands for a “unit of work”
or a “use case” inside the system. A unit of work has a beginning and an end, which I
call an entry point and an exit point. A simple example of a unit of work is a function
that calculates something and returns a value. However, a function could also use
other functions, other modules, and other components in the calculation process,
which means the unit of work (from entry point to exit point), could span more than
just a function.
1.3
Entry points and exit points
A unit of work always has an entry point and one or
more exit points. Figure 1.1 shows a simple diagram
of a unit of work.
 A unit of work can be a single function, multiple
functions, or even multiple modules or components.
But it always has an entry point that we can trigger
from the outside (via tests or other production code),
and it always ends up doing something useful. If it
doesn’t do anything useful, we might as well remove it
from our codebase. 
 What’s useful? Something publicly noticeable that
happens in the code: a return value, a state change,
or calling an external party, as shown in figure 1.2.
Those noticeable behaviors are what I call exit points. 
Unit of work
A unit of work is all the actions that take place between the invocation of an entry
point up until a noticeable end result through one or more exit points. The entry point
is the thing we trigger. Given a publicly visible function, for example
The function’s body is all or part of the unit of work. 
The function’s declaration and signature are the entry point into the body. 
The resulting outputs or behaviors of the function are its exit points.
Entry point
Exit point
Unit
of
work
Exit point
Exit point
Figure 1.1
A unit of work has 
entry points and exit points.


---
**Page 7**

7
1.3
Entry points and exit points
The following listing shows a quick code example of a simple unit of work. 
const sum = (numbers) => {
  const [a, b] = numbers.split(',');
  const result = parseInt(a) + parseInt(b);
  return result;
};
Why “exit point”?
Why use the term “exit point” and not something like “behavior”? My thinking is that
behaviors can be purely internal, whereas we’re looking for externally visible behav-
iors from the caller. That difference might be difficult to distinguish at a glance. Also,
“exit point” nicely suggests we are leaving the context of a unit of work and going
back to the test context, though behaviors might be a bit more fluid than that. There’s
an extensive discussion about types of behavior, including observable behavior, in
Unit Testing Principles, Practices, and Patterns by Vladimir Khorikov (Manning, 2020).
Refer to that book to learn more about this topic.
Listing 1.1
A simple function that we’d like to test
About the JavaScript version used in this book
I’ve chosen to use Node.js 12.8 with plain ES6 JavaScript along with JSDoc-style com-
ments. The module system I’ll use is CommonJS, to keep things simple. Perhaps in a
future edition I’ll start using ES modules (.mjs files), but for now, and for the rest of this
book, CommonJS will do. It doesn’t really matter for the patterns in this book anyway. 
You should be able to easily extrapolate the techniques used here for whatever
JavaScript stack you’re currently working with, whether you’re using TypeScript, Plain
JS, ES modules, backend or frontend, Angular, or React. It shouldn’t matter. 
someFunction()
Return value
or error
Unit
of
work
Calling third-party
dependency
Noticeable
state change
Figure 1.2
Types of exit points


---
**Page 8**

8
CHAPTER 1
The basics of unit testing
This unit of work is completely encompassed in a
single function. The function is the entry point,
and because its end result returns a value, it also
acts as the exit point. We get the end result in the
same place we trigger the unit of work, so the entry
point is also the exit point.
 If we drew this function as a unit of work, it
would look something like figure 1.3. I used
sum(numbers) as the entry point, not numbers,
because the entry point is the function signature.
The parameters are the context or input given
through the entry point.
 The following listing shows a variation on this
idea. 
let total = 0;
const totalSoFar = () => {
  return total;
};
const sum = (numbers) => {
  const [a, b] = numbers.split(',');
  const result = parseInt(a) + parseInt(b);
  total += result;    
  return result;
};
This new version of sum has two exit points. It does two things: 
It returns a value.
It introduces new functionality: a running total of all the sums. It sets the state
of the module in a way that is noticeable (via totalSoFar) from the caller of the
entry point.
Getting the code for this chapter
You can download all the code samples shown in this book from GitHub. You can find
the repository at https://github.com/royosherove/aout3-samples. Make sure you
have Node 12.8 or higher installed, and run npm install followed by npm run
ch[chapter number]. For this chapter, you would run npm run ch1. This will run all
the tests for this chapter so you can see their outputs.
Listing 1.2
A unit of work with entry points and exit points
sum(numbers)
Return value
Unit
of
work
Figure 1.3
A function that has the 
same entry point as exit point
New functionality: 
calculating a 
running total


---
**Page 9**

9
1.3
Entry points and exit points
Figure 1.4 shows how I would draw this unit of
work. You can think of these two exit points as
two different paths, or requirements, from the
same unit of work, because they indeed are two
different useful things the code is expected to
do. This also means I’d be very likely to write
two different unit tests here: one for each exit
point. Very soon we’ll do exactly that.
 What about totalSoFar? Is this also an
entry point? Yes, it could be, in a separate test. I
could write a test that proves that calling
totalSoFar without triggering prior to that
call returns 0. That would make it its own little
unit of work, which would be perfectly fine.
Often one unit of work (such as sum) can be
composed of smaller units. 
 As you can see, the scope of our tests can change and mutate, but we can still
define them with entry points and exit points. Entry points are always where the test
triggers the unit of work. You can have multiple entry points into a unit of work, each
used by a different set of tests. 
A note on design
There are two main types of actions: “query” actions and “command” actions. Query
actions don’t change stuff; they just return values. Command actions change stuff
but don’t return values. 
We often combine the two, but there are many cases where separating them might
be a better design choice. This book isn’t primarily about design, but I urge you to
read more about the concept of command query separation over on Martin Fowler’s
website: https://martinfowler.com/bliki/CommandQuerySeparation.html.
Exit points signifying requirements and new tests, and vice versa
Exit points are end results of a unit of work. For unit tests, I usually write at least one
test, with its own readable name, for each exit point. I may then add more tests with
variations on the inputs, all using the same entry point, to gain more confidence. 
Integration tests, which we’ll discuss later in this chapter and in the book, usually
include multiple end results, since it can be impossible to separate code paths at
those levels. That’s also one of the reasons integration tests are harder to debug,
get up and running, and maintain: they do much more than unit tests, as you’ll
soon see. 
sum(numbers)
Return value
Unit
of
work
State change
totalSoFar()
Figure 1.4
A unit of work with two exit 
points


---
**Page 10**

10
CHAPTER 1
The basics of unit testing
A third version of our example function is shown in the following listing.
let total = 0;
const totalSoFar = () => {
  return total;
};
const logger = makeLogger();
const sum = (numbers) => {
  const [a, b] = numbers.split(',');
  logger.info(                               
    'this is a very important log output',   
    { firstNumWas: a, secondNumWas: b });    
  const result = parseInt(a) + parseInt(b);
  total += result;
  return result;
};
You can see that there’s a new exit point (or requirement, or end result) in the func-
tion. It logs something to an external entity—perhaps to a file, or the console, or a
database. We don’t know, and we don’t care. This is the third type of exit point: calling
a third party. I also like to refer to it as “calling a dependency.” 
DEFINITION
A dependency is something we don’t have full control over during
a unit test. Or it can be something that trying to control in a test would
make our lives miserable. Some examples would include loggers that write
to files, things that talk to the network, code that’s controlled by other teams,
components that take a long time (calculations, threads, database access),
and more. The rule of thumb is that if we can fully and easily control what
it’s doing, and it runs in memory, and it’s fast, then it’s not a dependency.
There are always exceptions to the rule, but this should get you through
80% of the cases, at least.
Figure 1.5 shows how I’d draw this unit of work with all three exit points. At this point
we’re still discussing a function-sized unit of work. The entry point is the function call,
but now we have three possible paths, or exit points, that do something useful and
that the caller can verify publicly.
 Here’s where it gets interesting: it’s a good idea to have a separate test for each exit
point. This will make the tests more readable and simpler to debug or change without
affecting other outcomes.
 
 
 
Listing 1.3
Adding a logger call to the function
A new exit 
point


---
**Page 11**

11
1.4
Exit point types
1.4
Exit point types
We’ve seen that we have three different types of end results:
The invoked function returns a useful value (not undefined). If this was in a stati-
cally typed language such as Java or C#, we’d say it is a public, non-void function.
There’s a noticeable change to the state or behavior of the system before and
after invocation that can be determined without interrogating private state.
There’s a callout to a third-party system over which the test has no control. That
third-party system doesn’t return any value, or that value is ignored. (Example:
the code calls a third-party logging system that was not written by you, and you
don’t control its source code.)
Let’s see how the idea of entry and exit points affects the definition of a unit test: A
unit test is a piece of code that invokes a unit of work and checks one specific exit point
as an end result of that unit of work. If the assumptions about the end result turn out
to be wrong, the unit test has failed. A unit test’s scope can span as little as a function
or as much as multiple modules or components, depending on how many functions
and modules are used between the entry point and the exit point. 
XUnit Test Patterns’ definition of entry and exit points
Gerard Meszaros’ book XUnit Test Patterns (Addison-Wesley Professional, 2007) dis-
cusses the notion of direct inputs and outputs, and indirect inputs and outputs. Direct
inputs are what I like to call entry points. Meszaros refers to it as “using the front
door” of a component. Indirect outputs in that book are the other two types of exit
points I mentioned (state change and calling a third party). 
Both versions of these ideas have evolved in parallel, but the idea of a “unit of work”
only appears in this book. A unit of work, coupled with entry and exit points, makes
much more sense to me than direct and indirect inputs and outputs, but you can con-
sider this a stylistic choice about how to teach the concept of test scopes. You can
find more about XUnit Test Patterns at xunitpatterns.com. 
sum(numbers)
Return value
Unit
of
work
Call third-party
logger
State change
totalSoFar()
Figure 1.5
Showing three exit 
points from a function



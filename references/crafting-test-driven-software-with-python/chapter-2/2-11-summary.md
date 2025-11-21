# 2.11 Summary (pp.66-67)

---
**Page 66**

Test Doubles with a Chat Application
Chapter 2
[ 66 ]
If we were to make a ChatClient with the proto_inject, we would now see that each
client has its own Connection object:
>>> cli = proto_injector.provide(ChatClient)
<ChatClient object at 0x7fadab060e50> GOT <Connection object at
0x7fadab013910>
>>> cli2 = proto_injector.provide(ChatClient)
<ChatClient object at 0x7fadab060f10> GOT <Connection object at
0x7fadab013850>
So, dependency injection frameworks can solve many needs for you. Whether you need to
use one or not depends mostly on how complex the network of dependencies in your
software is, but having one around can usually give you a quick way to break dependencies
between your components when you need to.
Summary
Dependencies between the components that you have to test can make your life hard as a
developer. To test anything more complex than a simple utility function, you might end up
having to cope with tens of dependencies and their state.
This is why the idea of being able to provide doubles for testing in place of the real
components was quickly born once the idea of automated tests became reality. Being able
to replace the components the unit you are testing depends on with fakes, dummies, stubs,
and mocks can make your life a lot easier and keep your test suite fast and easy to maintain.
The fact that any software is, in reality, a complex network of dependencies is the reason
why many people advocate that integration tests are the most realistic and reliable form of
testing, but managing that complex network can be hard and that's where dependency
injection and dependency injection frameworks can make your life far easier.
Now that we know how to write automatic test suites and we know how to use test
doubles to verify our components in isolation and spy their state and behavior, we have all
the tools that we need to dive into test-driven development in the next chapter and see how
to write software in the TDD way.


---
**Page 67**

3
Test-Driven Development while
Creating a TODO List
No programmer ever releases a software without having tested it – even for the most basic
proof of concept and rough hack, the developer will run it once to see that it at least starts
and resembles what they had in mind.
But to test, as a verb, usually ends up meaning clicking buttons here and there to get a
vague sense of confidence that the software does what we intended. This is different from
test as a noun, which means a set of written-out checks that our software must pass to
confirm it does what we wanted.
Apart from being more reliable, written-out checks force us to think about what the code
must do. They force us to get into the details and think beforehand about what we want to
build. Otherwise, we would just jump to building without thinking about what we are
building. And trying to ensure that what gets built is, in every single detail, the right thing
through a written specification is quickly going to turn into writing the software itself, just
in plain English.
The problem is that the more hurried, stressed, and overwhelmed developers are, the less
they test. Tests are the first thing that get skipped when things go wrong, and by doing so
things suddenly get even worse, as tests are what avoid errors and failures, and more errors
and failures mean more stress and rushing through the code to fix them, making the whole
process a loop that gets worse and worse.
Test-Driven Development (TDD) tries to solve this problem by engendering a set of
practices where tests become a fundamental step of your daily routine. To write more code
you must write tests, and as you get used to TDD and it becomes natural, you will quickly
notice that it gets hard to even think about how to get started if not by writing a test.
That's why in this chapter, we will cover how TDD can fit into the software development
routine and how to leverage it to keep problems under control at times of high stress.



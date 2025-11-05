# 3.0 Introduction [auto-generated] (pp.61-62)

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



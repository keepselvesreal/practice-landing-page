# 4.0 Introduction [auto-generated] (pp.83-84)

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


---
**Page 84**

84
CHAPTER 4
Interaction testing using mock objects
our unit of work ends up calling a function that we don’t control and identify what val-
ues were sent as arguments. 
 The approaches we’ve looked at so far won’t do here, because third-party func-
tions usually don’t have specialized APIs that allow us to check if they were called
correctly. Instead, they internalize their operations for clarity and maintainability.
So, how can you test that your unit of work interacts with third-party functions cor-
rectly? You use mocks.
4.1
Interaction testing, mocks, and stubs
Interaction testing is checking how a unit of work interacts with and sends messages
(i.e., calls functions) to a dependency beyond its control. Mock functions or objects
are used to assert that a call was made correctly to an external dependency.
 Let’s recall the differences between mocks and stubs as we covered them in chap-
ter 3. The main difference is in the flow of information: 
Mock—Used to break outgoing dependencies. Mocks are fake modules, objects,
or functions that we assert were called in our tests. A mock represents an exit
point in a unit test. If we don’t assert on it, it’s not used as a mock. 
It is normal to have no more than a single mock per test, for maintainability
and readability reasons. (We’ll discuss this more in part 3 of this book about
writing maintainable tests.)
Stub—Used to break incoming dependencies. Stubs are fake modules, objects,
or functions that provide fake behavior or data to the code under test. We do
not assert against them, and we can have many stubs in a single test. 
Stubs represent waypoints, not exit points, because the data or behavior
flows into the unit of work. They are points of interaction, but they do not repre-
sent an ultimate outcome of the unit of work. Instead, they are an interaction
on the way to achieving the end result we care about, so we don’t treat them as
exit points.
Figure 4.1 shows these two side by side.
 Let’s look at a simple example of an exit point to a dependency that we do not con-
trol: calling a logger.
 
 
 
 
 
 
 



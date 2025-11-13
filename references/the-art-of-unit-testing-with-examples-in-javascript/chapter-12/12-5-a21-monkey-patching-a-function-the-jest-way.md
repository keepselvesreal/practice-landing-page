# 12.5 A.2.1 Monkey-patching a function the Jest way (pp.241-241)

---
**Page 241**

241
A.2
Monkey-patching functions, globals, and possible issues
when I factor seams into the design of the code under test instead of around it in an
implicit manner, such as what we just did.
 Especially when considering that more and more frameworks might start to copy
Jest’s features and run tests in parallel, global fakes become more and more dangerous.
A.2.1
Monkey-patching a function the Jest way
To make the picture more complete, Jest also supports the idea of monkey-patching
through the use of two functions that work in tandem: spyOn and mockImplementation.
Here’s spyOn:
Date.now = jest.spyOn(Date, 'now')
spyOn takes as parameters the scope and the function that requires tracking. Note that
we need to use a string as a parameter here, which is not really refactoring-friendly—
it’s easy to miss if we rename that function. 
A.2.2
Jest spies
The word “spy” has a slightly more interesting shade of grey to it than the terms we’ve
encountered so far in this book, which is why I don’t like to use it too much (or at all)
if I can help it. Unfortunately, this word is a major part of Jest’s API, so let’s make sure
we understand it. 
 xUnit Test Patterns (Addison-Wesley, 2007), by Gerard Meszaros, says this in its dis-
cussion of spies: “Use a Test Double to capture the indirect output calls made to
another component by the system under test (SUT) for later verification by the test.”
The only difference between a spy and a fake or test double is that a spy is calling the
real implementation of the function underneath, and it only tracks the inputs to and
outputs from that function, which we can later verify through the test. Fakes and test
doubles don’t use the real implementation of a function.
 My refined definition of a spy is pretty close: The act of wrapping a unit of work
with an invisible tracking layer on the entry points and exit points without changing
the underlying functionality, for the purpose of tracking its inputs and outputs
during testing.
A.2.3
spyOn with mockImplementation()
This “tracking without changing functionality” behavior that is inherent to spies also
explains why just using spyOn won’t be enough for us to fake Date.now. It’s only meant
for tracking, not faking. 
 To actually fake the Date.now function and turn it into a stub, we’ll use the confus-
ingly named mockImplementation to replace the underlying unit of work’s functionality:
jest.spyOn(Date, 'now').mockImplementation(() => /*return stub time*/);



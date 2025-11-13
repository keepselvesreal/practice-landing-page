# 9.2.4 Only mock types that you own (pp.227-227)

---
**Page 227**

227
Summary
9.2.4
Only mock types that you own
The last guideline I’d like to talk about is mocking only types that you own. It was first
introduced by Steve Freeman and Nat Pryce.1 The guideline states that you should
always write your own adapters on top of third-party libraries and mock those adapters
instead of the underlying types. A few of their arguments are as follows:
You often don’t have a deep understanding of how the third-party code works.
Even if that code already provides built-in interfaces, it’s risky to mock those
interfaces, because you have to be sure the behavior you mock matches what
the external library actually does.
Adapters abstract non-essential technical details of the third-party code and
define the relationship with the library in your application’s terms.
I fully agree with this analysis. Adapters, in effect, act as an anti-corruption layer
between your code and the external world.2 These help you to
Abstract the underlying library’s complexity
Only expose features you need from the library
Do that using your project’s domain language
The IBus interface in our sample CRM project serves exactly that purpose. Even if the
underlying message bus’s library provides as nice and clean an interface as IBus, you
are still better off introducing your own wrapper on top of it. You never know how the
third-party code will change when you upgrade the library. Such an upgrade could
cause a ripple effect across the whole code base! The additional abstraction layer
restricts that ripple effect to just one class: the adapter itself.
 Note that the “mock your own types” guideline doesn’t apply to in-process depen-
dencies. As I explained previously, mocks are for unmanaged dependencies only.
Thus, there’s no need to abstract in-memory or managed dependencies. For instance,
if a library provides a date and time API, you can use that API as-is, because it doesn’t
reach out to unmanaged dependencies. Similarly, there’s no need to abstract an ORM
as long as it’s used for accessing a database that isn’t visible to external applications.
Of course, you can introduce your own wrapper on top of any library, but it’s rarely
worth the effort for anything other than unmanaged dependencies. 
Summary
Verify interactions with an unmanaged dependency at the very edges of your
system. Mock the last type in the chain of types between the controller and the
unmanaged dependency. This helps you increase both protection against
regressions (due to more code being validated by the integration test) and
1 See page 69 in Growing Object-Oriented Software, Guided by Tests by Steve Freeman and Nat Pryce (Addison-Wesley
Professional, 2009).
2 See Domain-Driven Design: Tackling Complexity in the Heart of Software by Eric Evans (Addison-Wesley, 2003).



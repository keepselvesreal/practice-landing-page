Line 1: 
Line 2: --- 페이지 94 ---
Line 3: Chapter 8
Line 4: Building on Third-Party Code
Line 5: Programming today is all about doing science on the parts you have
Line 6: to work with.
Line 7: —Gerald Jay Sussman
Line 8: Introduction
Line 9: We’ve shown how we pull a system’s design into existence: discovering what our
Line 10: objects need and writing interfaces and further objects to meet those needs. This
Line 11: process works well for new functionality. At some point, however, our design
Line 12: will come up against a need that is best met by third-party code: standard APIs,
Line 13: open source libraries, or vendor products. The critical point about third-party
Line 14: code is that we don’t control it, so we cannot use our process to guide its design.
Line 15: Instead, we must focus on the integration between our design and the
Line 16: external code.
Line 17: In integration, we have an abstraction to implement, discovered while we de-
Line 18: veloped the rest of the feature. With the third-party API pushing back at our
Line 19: design, we must ﬁnd the best balance between elegance and practical use of
Line 20: someone else’s ideas. We must check that we are using the third-party API cor-
Line 21: rectly, and adjust our abstraction to ﬁt if we ﬁnd that our assumptions are
Line 22: incorrect.
Line 23: Only Mock Types That You Own
Line 24: Don’t Mock Types You Can’t Change
Line 25: When we use third-party code we often do not have a deep understanding of
Line 26: how it works. Even if we have the source available, we rarely have time to read
Line 27: it thoroughly enough to explore all its quirks. We can read its documentation,
Line 28: which is often incomplete or incorrect. The software may also have bugs that we
Line 29: will need to work around. So, although we know how we want our abstraction
Line 30: to behave, we don’t know if it really does so until we test it in combination with
Line 31: the third-party code.
Line 32: We also prefer not to change third-party code, even when we have the sources.
Line 33: It’s usually too much trouble to apply private patches every time there’s a new
Line 34: version. If we can’t change an API, then we can’t respond to any design feedback
Line 35: we get from writing unit tests that touch it. Whatever alarm bells the unit tests
Line 36: 69
Line 37: 
Line 38: --- 페이지 95 ---
Line 39: might be ringing about the awkwardness of an external API, we have to live with
Line 40: it as it stands.
Line 41: This means that providing mock implementations of third-party types is of
Line 42: limited use when unit-testing the objects that call them. We ﬁnd that tests that
Line 43: mock external libraries often need to be complex to get the code into the right
Line 44: state for the functionality we need to exercise. The mess in such tests is telling
Line 45: us that the design isn’t right but, instead of ﬁxing the problem by improving the
Line 46: code, we have to carry the extra complexity in both code and test.
Line 47: A second risk is that we have to be sure that the behavior we stub or mock
Line 48: matches what the external library will actually do. How difﬁcult this is depends
Line 49: on the quality of the library—whether it’s speciﬁed (and implemented) well
Line 50: enough for us to be certain that our unit tests are valid. Even if we get it right
Line 51: once, we have to make sure that the tests remain valid when we upgrade the
Line 52: libraries.
Line 53: Write an Adapter Layer
Line 54: If we don’t want to mock an external API, how can we test the code that drives
Line 55: it? We will have used TDD to design interfaces for the services our objects
Line 56: need—which will be deﬁned in terms of our objects’ domain, not the external
Line 57: library.
Line 58: We write a layer of adapter objects (as described in [Gamma94]) that uses the
Line 59: third-party API to implement these interfaces, as in Figure 8.1. We keep this
Line 60: layer as thin as possible, to minimize the amount of potentially brittle and hard-
Line 61: to-test code. We test these adapters with focused integration tests to conﬁrm our
Line 62: understanding of how the third-party API works. There will be relatively few
Line 63: integration tests compared to the number of unit tests, so they should not get in
Line 64: the way of the build even if they’re not as fast as the in-memory unit tests.
Line 65: Figure 8.1
Line 66: Mockable adapters to third-party objects
Line 67: Following this approach consistently produces a set of interfaces that deﬁne
Line 68: the relationship between our application and the rest of the world in our
Line 69: application’s terms and discourages low-level technical concepts from leaking
Line 70: Chapter 8
Line 71: Building on Third-Party Code
Line 72: 70
Line 73: 
Line 74: --- 페이지 96 ---
Line 75: into the application domain model. In Chapter 25, we discuss a common example
Line 76: where abstractions in the application’s domain model are implemented using a
Line 77: persistence API.
Line 78: There are some exceptions where mocking third-party libraries can be helpful.
Line 79: We might use mocks to simulate behavior that is hard to trigger with the real
Line 80: library, such as throwing exceptions. Similarly, we might use mocks to test a se-
Line 81: quence of calls, for example making sure that a transaction is rolled back if there’s
Line 82: a failure. There should not be many tests like this in a test suite.
Line 83: This pattern does not apply to value types because, of course, we don’t need
Line 84: to mock them. We still, however, have to make design decisions about how
Line 85: much to use third-party value types in our code. They might be so fundamental
Line 86: that we just use them directly. Often, however, we want to follow the same
Line 87: principles of isolation as for third-party services, and translate between value
Line 88: types appropriate to the application domain and to the external domain.
Line 89: Mock Application Objects in Integration Tests
Line 90: As described above, adapter objects are passive, reacting to calls from our code.
Line 91: Sometimes, adapter objects must call back to objects from the application. Event-
Line 92: based libraries, for example, usually expect the client to provide a callback object
Line 93: to be notiﬁed when an event happens. In this case, the application code will give
Line 94: the adapter its own event callback (deﬁned in terms of the application domain).
Line 95: The adapter will then pass an adapter callback to the external library to receive
Line 96: external events and translate them for the application callback.
Line 97: In these cases, we do use mock objects when testing objects that integrate with
Line 98: third-party code—but only to mock the callback interfaces deﬁned in the appli-
Line 99: cation, to verify that the adapter translates events between domains correctly
Line 100: (Figure 8.2).
Line 101: Multithreading adds more complication to integration tests. For example,
Line 102: third-party libraries may start background threads to deliver events to the appli-
Line 103: cation code, so synchronization is a vital aspect of the design effort of adapter
Line 104: layers; we discuss this further in Chapter 26.
Line 105: Figure 8.2
Line 106: Using mock objects in integration tests
Line 107: 71
Line 108: Mock Application Objects in Integration Tests
Line 109: 
Line 110: --- 페이지 97 ---
Line 111: This page intentionally left blank 
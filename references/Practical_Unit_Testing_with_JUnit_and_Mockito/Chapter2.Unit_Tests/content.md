Line 1: 
Line 2: --- 페이지 28 ---
Line 3: Chapter 2. Unit Tests
Line 4: After the introductory sections devoted to developers’ testing in general we now move on to the
Line 5: central topic of the book: unit testing.
Line 6: 2.1. What is a Unit Test?
Line 7: The idea behind unit tests is simple: it is to make sure the class you are working on right now
Line 8: works correctly – to make sure it does its job. This concerns whether, given certain input data,
Line 9: it will respond with a certain expected output, or whether, fed with nonsense data, it will throw
Line 10: an appropriate exception, and so on. The idea, then, is to write tests that will verify this expected
Line 11: behaviour.
Line 12: But that is not enough. You should test your classes in isolation, and test them to verify that they
Line 13: work in any environment. When writing unit tests it is important to test a single class and nothing
Line 14: more. Concentrate on the logic of your class. Once you are sure your code works fine, then test its
Line 15: integration with other components. But first conduct unit tests!
Line 16: Unfortunately, even now many confuse unit tests with other kinds of test (e.g. you can read
Line 17: about "unit testing of your database"), or use this term to describe just any kind of test
Line 18: developers write. Many people claim that every test they write is of the unit variety, just
Line 19: on the basis that it is executed by some unit testing framework! Others claim that they are
Line 20: doing unit testing and have chosen three layers of software as the unit they are going to
Line 21: test… This is, of course, wrong: it sows confusion and makes discussion difficult. Do not
Line 22: do that! You know what unit tests really are.
Line 23: Unit tests have some properties which distinguish them from other developers' tests. They are focused
Line 24: on single classes and they strictly control the context in which an SUT is executed. They also run
Line 25: extremely fast and are able to pinpoint bugs with great accuracy, often leading the developer straight
Line 26: to the guilty method, if not to the guilty line of code itself! By giving such precise and immediate
Line 27: feedback on the quality of our work they help us to fix the bugs quickly before they spread through
Line 28: the whole system (see Section 1.4).
Line 29: The existence of a comprehensive and rigorous set of unit tests allows us to refactor code without any
Line 30: fear of breaking something: once all your classes are covered by unit tests, there are no areas of code
Line 31: left that "no one dares to touch"!
Line 32: Another benefit of writing unit tests is that they serve as a live (that is, always up-to-date)
Line 33: documentation of our code. They are much more reliable than Javadocs or any other kind of textual
Line 34: description that might be developed in parallel to the creation of the code itself.
Line 35: Last but not least, a skilful developer can turn the process of creating unit tests into a design activity.
Line 36: This, quite surprisingly, might be the most important of all the benefits conferred by unit tests!
Line 37: And remember one more thing: unit tests have been brought into this world by developers,
Line 38: and they are our responsibility, our tool and something we take pride in – or, if not done
Line 39: properly, something for us to be ashamed of.
Line 40: 13
Line 41: 
Line 42: --- 페이지 29 ---
Line 43: Chapter 2. Unit Tests
Line 44: 2.2. Interactions in Unit Tests
Line 45: To understand what should be tested by unit tests, and how, we need to take a closer look at the
Line 46: interactions between the test class and the SUT, and the SUT and its DOCs1.
Line 47:    First, some theory in the form of a diagram. Figure 2.1 shows possible interactions between an SUT
Line 48: and other entities.
Line 49: Figure 2.1. Types of collaboration with an SUT
Line 50: Two interactions are direct, and involve the SUT and its client (a test class, in this case). These
Line 51: two are very easy to act upon - they are directly "available" from within the test code. Two other
Line 52: interactions are indirect: they involve the SUT and DOCs. In this case, the client (a test class) has no
Line 53: way of directly controlling the interactions.
Line 54: Another possible classification divides up interactions into inputs (the SUT receiving some message)
Line 55: and outputs (the SUT sending a message). When testing, we will use direct and indirect inputs to
Line 56: set the SUT in a required state and to invoke its methods. The direct and indirect outputs of the SUT
Line 57: are expressions of the SUT’s behaviour; this means we shall use them to verify whether the SUT is
Line 58: working properly.
Line 59: Table 2.1 summarizes the types of possible collaboration between an SUT and DOCs. The first
Line 60: column – "type of interaction" – describes the type of collaboration from the SUT’s point of view. A
Line 61: test class acts as a client (someone who uses the SUT); hence its appearance in the "involved parties"
Line 62: column.
Line 63: Table 2.1. Types of collaboration with an SUT within test code
Line 64: type of
Line 65: interaction
Line 66: involved parties
Line 67: description
Line 68: direct input
Line 69: Test class & SUT
Line 70: Calls to the methods of the SUT’s API.
Line 71: direct output
Line 72: Test class & SUT
Line 73: Values returned by the SUT to the test class after
Line 74: calling some SUT method.
Line 75: indirect output
Line 76: SUT & DOCs
Line 77: Arguments passed by the SUT to a method of one
Line 78: of its collaborators.
Line 79: indirect input
Line 80: SUT & DOCs
Line 81: Value returned (or an exception thrown) to the
Line 82: SUT by collaborators, after it called some of their
Line 83: methods.
Line 84: 1An SUT is a thing being tested; DOCs are its collaborators. Both terms are introduced in Section 1.2.
Line 85: 14
Line 86: 
Line 87: --- 페이지 30 ---
Line 88: Chapter 2. Unit Tests
Line 89: A code example will make all of this clear. Let’s imagine some financial service (FinancialService
Line 90: class) which, based on the last client payment and its type (whatever that would be), calculates some
Line 91: "bonus".
Line 92: Listing 2.1. Example class to present various types of interaction in unit tests
Line 93: public class FinancialService {
Line 94:     .... // definition of fields and other methods omitted
Line 95:     public BigDecimal calculateBonus(long clientId, BigDecimal payment) {
Line 96:         Short clientType = clientDAO.getClientType(clientId);
Line 97:         BigDecimal bonus = calculator.calculateBonus(clientType, payment);
Line 98:         clientDAO.saveBonusHistory(clientId, bonus);
Line 99:         return bonus;
Line 100:     }
Line 101: }
Line 102: As you can see the SUT’s calculateBonus() method takes two parameters (clientId and
Line 103: payment) and interacts with two collaborators (clientDAO and calculator). In order to test the
Line 104: calculateBonus() method thoroughly, we need to control both the input parameters (direct inputs)
Line 105: and the messages returned from its collaborators (indirect inputs). Then we will be able to see if
Line 106: returned value (direct output) is correct.
Line 107: Table 2.2 summarizes the types of interaction that happen within the calculateBonus() method, and
Line 108: that are important from the test point of view.
Line 109: Table 2.2. Collaborations within the calculateBonus() method
Line 110: type of
Line 111: interaction
Line 112: involved parties
Line 113: description
Line 114: direct input
Line 115: Test class & SUT
Line 116: Direct call of the calculateBonus() method of the SUT
Line 117: with clientId and payment arguments
Line 118: direct output
Line 119: Test class & SUT
Line 120: bonus value returned by the SUT to the test class after it
Line 121: called the calculateBonus() method
Line 122: indirect output
Line 123: SUT & DOCs
Line 124: • clientId and bonus passed by the SUT to the
Line 125: saveBonusHistory() method of clientDAO
Line 126: • clientType and payment passed by the SUT to the
Line 127: calculateBonus() method of calculator
Line 128: indirect input
Line 129: SUT & DOCs
Line 130: clientType returned by clientDAO, and bonus returned by
Line 131: calculator to the SUT
Line 132: 2.2.1. State vs. Interaction Testing
Line 133: Let us now recall the simple abstraction of an OO system.
Line 134: 15
Line 135: 
Line 136: --- 페이지 31 ---
Line 137: Chapter 2. Unit Tests
Line 138: Figure 2.2. An OO system abstraction
Line 139: It shows how two kinds of classes - workers and managers - cooperate together in order to fulfill
Line 140: a request issued by a client. The book describes unit testing of both kind of classes. First we shall
Line 141: dive into the world of workers, because we want to make sure that the computations they do, and the
Line 142: values they return, are correct. This part of unit testing – called state testing – is really simple, and
Line 143: has been fully recognized for many years. This kind of test uses direct inputs and outputs. We will
Line 144: discuss state testing in Chapter 3, Unit Tests with no Collaborators.
Line 145: Then we will move into the more demanding topics connected with interactions testing. We will
Line 146: concentrate on the work of managers, and we will concentrate on how messages are passed between
Line 147: collaborators. This is a far trickier and less intuitive kind of testing. Every so often, new ideas and
Line 148: tools emerge, and there are still lively discussions going on about how to properly test interactions.
Line 149: What is really scary is that interaction tests can sometimes do more harm than good, so we will
Line 150: concentrate not only on how but also on whether questions. This kind of test concentrates on indirect
Line 151: outputs. We will discuss interactions testing in Chapter 5, Mocks, Stubs, and Dummies.
Line 152: Testing of direct outputs is also called "state verification", while testing of indirect outputs
Line 153: is called "behaviour verification" (see [fowler2007]).
Line 154: 2.2.2. Why Worry about Indirect Interactions?
Line 155: An object-oriented zealot could, at this point, start yelling at me: "Ever heard of encapsulation and
Line 156: information hiding? So why on earth should we worry about what methods were called by the SUT on
Line 157: its collaborators? Why not leave it as an implementation detail of the SUT? If this is a private part of
Line 158: the SUT implementation, then we should not touch it at all."
Line 159: This sounds reasonable, doesn’t it? If only we could test our classes thoroughly, just using their API!
Line 160: Unfortunately, this is not possible.
Line 161: Consider a simple example of retrieving objects from a cache.
Line 162: 16
Line 163: 
Line 164: --- 페이지 32 ---
Line 165: Chapter 2. Unit Tests
Line 166: Let us remember what the general idea of a cache is. There are two storage locations, the "real one",
Line 167: with vast capacity and average access time, and the "cache", which has much smaller capacity but
Line 168: much faster access time2. Let us now define a few requirements for a system with a cache. This will
Line 169: not be a fully-fledged cache mechanism, but will be sufficient to illustrate the problem we encounter.
Line 170: When asked for an object with key X, our system with its cache should act according to the following
Line 171: simple rules:
Line 172: 1. if the object with key X exists in the cache storage, then it will be returned from this storage, and
Line 173: the main storage location won’t be searched,
Line 174: 2. if the object with key X doesn’t exist in the cache storage, then it will be returned from the main
Line 175: storage,
Line 176: 3. if the object with key X is not in any storage location, the system will return null.
Line 177: The point is, of course, to have a smart caching strategy that will increase the cache hit ratio3 – but
Line 178: this is not really relevant to our discussion. What we are concerned with are the outputs (returned
Line 179: values) and the interactions between the SUT and its collaborators.
Line 180: If you consider the requirements listed above, you will notice that with state testing we can only test
Line 181: the last one. This is because state testing respects objects’ privacy. It does not allow one to see what
Line 182: the object is doing internally – something which, in our case, means that it cannot verify from which
Line 183: storage area the requested object has been retrieved. Thus, requirements 1 and 2 cannot be verified
Line 184: using state testing.
Line 185: This is illustrated in the picture below. Our SUT, which consists of two storage locations (a fast cache
Line 186: storage and a slower real storage), is accessible via a single get() method. The client, who sends
Line 187: requests to the SUT, knows nothing about its internal complexity.
Line 188: Figure 2.3. Is this storage working correctly or not?
Line 189: Ideally, when a request comes first the cache storage is searched and then, in case the cache storage
Line 190: does not have an entry with the given key (X in this example), the main storage is searched. However,
Line 191: if the SUT is not implemented correctly then it can first look into the main storage without checking
Line 192: 2In fact, it would be more correct to say that access to one storage area is cheaper than to the other one. Usually, the unit of cost is
Line 193: time-relative, so we will make such a simplification here.
Line 194: 3Which basically means that most of the items will be in the cache when requested, and the number of queries to the real storage
Line 195: will be minimized.
Line 196: 17
Line 197: 
Line 198: --- 페이지 33 ---
Line 199: Chapter 2. Unit Tests
Line 200: the faster storage first. The client who waits for an object with the given key can not distinguish
Line 201: between these two situations. All he knows is that he requested an object with key X and that he got it.
Line 202: In order to really verify whether our system is working as it is supposed to or not, interaction testing
Line 203: must by applied. The order of calls to collaborators – cache and real storage – must be checked.
Line 204: Without this, we cannot say whether the system is working or not.
Line 205: This simple example proves that verification of the observable behaviour of the SUT (its direct
Line 206: outputs) is not enough. Similar issues arise when testing managers (see Section 1.1), which
Line 207: coordinate the efforts of others. As mentioned previously, such coordinating classes are quite popular
Line 208: in OO systems. This is why we will be spending a great deal of time discussing techniques, tools and
Line 209: issues related to indirect outputs testing.
Line 210: But to begin with let’s concentrate on the simpler case. In the next section we will learn how to test
Line 211: simple objects that do not have any collaborators.
Line 212: 18
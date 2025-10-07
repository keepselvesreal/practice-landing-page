Line 1: 
Line 2: --- 페이지 64 ---
Line 3: Chapter 5
Line 4: Maintaining the Test-Driven
Line 5: Cycle
Line 6: Every day you may make progress. Every step may be fruitful. Yet there
Line 7: will stretch out before you an ever-lengthening, ever-ascending,
Line 8: ever-improving path. You know you will never get to the end of the
Line 9: journey. But this, so far from discouraging, only adds to the joy and
Line 10: glory of the climb.
Line 11: —Winston Churchill
Line 12: Introduction
Line 13: Once we’ve kick-started the TDD process, we need to keep it running smoothly.
Line 14: In this chapter we’ll show how a TDD process runs once started. The rest of the
Line 15: book explores in some detail how we ensure it runs smoothly—how we write
Line 16: tests as we build the system, how we use tests to get early feedback on internal
Line 17: and external quality issues, and how we ensure that the tests continue to support
Line 18: change and do not become an obstacle to further development.
Line 19: Start Each Feature with an Acceptance Test
Line 20: As we described in Chapter 1, we start work on a new feature by writing failing
Line 21: acceptance tests that demonstrate that the system does not yet have the feature
Line 22: we’re about to write and track our progress towards completion of the
Line 23: feature (Figure 5.1).
Line 24: We write the acceptance test using only terminology from the application’s
Line 25: domain, not from the underlying technologies (such as databases or web servers).
Line 26: This helps us understand what the system should do, without tying us to any of
Line 27: our initial assumptions about the implementation or complicating the test with
Line 28: technological details. This also shields our acceptance test suite from changes to
Line 29: the system’s technical infrastructure. For example, if a third-party organization
Line 30: changes the protocol used by their services from FTP and binary ﬁles to web
Line 31: services and XML, we should not have to rework the tests for the system’s
Line 32: application logic.
Line 33: We ﬁnd that writing such a test before coding makes us clarify what we want
Line 34: to achieve. The precision of expressing requirements in a form that can be auto-
Line 35: matically checked helps us uncover implicit assumptions. The failing tests keep
Line 36: 39
Line 37: 
Line 38: --- 페이지 65 ---
Line 39: Figure 5.1
Line 40: Each TDD cycle starts with a failing acceptance test
Line 41: us focused on implementing the limited set of features they describe, improving
Line 42: our chances of delivering them. More subtly, starting with tests makes us look
Line 43: at the system from the users’ point of view, understanding what they need it to
Line 44: do rather than speculating about features from the implementers’ point of view.
Line 45: Unit tests, on the other hand, exercise objects, or small clusters of objects, in
Line 46: isolation. They’re important to help us design classes and give us conﬁdence that
Line 47: they work, but they don’t say anything about whether they work together with
Line 48: the rest of the system. Acceptance tests both test the integration of unit-tested
Line 49: objects and push the project forwards.
Line 50: Separate Tests That Measure Progress from Those That
Line 51: Catch Regressions
Line 52: When we write acceptance tests to describe a new feature, we expect them to fail
Line 53: until that feature has been implemented; new acceptance tests describe work yet
Line 54: to be done. The activity of turning acceptance tests from red to green gives the
Line 55: team a measure of the progress it’s making. A regular cycle of passing acceptance
Line 56: tests is the engine that drives the nested project feedback loops we described in
Line 57: “Feedback Is the Fundamental Tool” (page 4). Once passing, the acceptance tests
Line 58: now represent completed features and should not fail again. A failure means that
Line 59: there’s been a regression, that we’ve broken our existing code.
Line 60: We organize our test suites to reﬂect the different roles that the tests fulﬁll.
Line 61: Unit and integration tests support the development team, should run quickly,
Line 62: and should always pass. Acceptance tests for completed features catch
Line 63: regressions and should always pass, although they might take longer to run.
Line 64: New acceptance tests represent work in progress and will not pass until a feature
Line 65: is ready.
Line 66: If requirements change, we must move any affected acceptance tests out of the
Line 67: regression suite back into the in-progress suite, edit them to reﬂect the new
Line 68: requirements, and change the system to make them pass again.
Line 69: Chapter 5
Line 70: Maintaining the Test-Driven Cycle
Line 71: 40
Line 72: 
Line 73: --- 페이지 66 ---
Line 74: Start Testing with the Simplest Success Case
Line 75: Where do we start when we have to write a new class or feature? It’s tempting
Line 76: to start with degenerate or failure cases because they’re often easier. That’s a
Line 77: common interpretation of the XP maxim to do “the simplest thing that could
Line 78: possibly work” [Beck02], but simple should not be interpreted as simplistic.
Line 79: Degenerate cases don’t add much to the value of the system and, more important-
Line 80: ly, don’t give us enough feedback about the validity of our ideas. Incidentally,
Line 81: we also ﬁnd that focusing on the failure cases at the beginning of a feature is bad
Line 82: for morale—if we only work on error handling it feels like we’re not achieving
Line 83: anything.
Line 84: We prefer to start by testing the simplest success case. Once that’s working,
Line 85: we’ll have a better idea of the real structure of the solution and can prioritize
Line 86: between handling any possible failures we noticed along the way and further
Line 87: success cases. Of course, a feature isn’t complete until it’s robust. This isn’t an
Line 88: excuse not to bother with failure handling—but we can choose when we want
Line 89: to implement ﬁrst.
Line 90: We ﬁnd it useful to keep a notepad or index cards by the keyboard to jot down
Line 91: failure cases, refactorings, and other technical tasks that need to be addressed.
Line 92: This allows us to stay focused on the task at hand without dropping detail. The
Line 93: feature is ﬁnished only when we’ve crossed off everything on the list—either
Line 94: we’ve done each task or decided that we don’t need to.
Line 95: Iterations in Space
Line 96: We’re writing this material around the fortieth anniversary of the ﬁrst Moon landing.
Line 97: The Moon program was an excellent example of an incremental approach (although
Line 98: with much larger stakes than we’re used to). In 1967, they proposed a series of
Line 99: seven missions, each of which would be a step on the way to a landing:
Line 100: 1.
Line 101: Unmanned Command/Service Module (CSM) test
Line 102: 2.
Line 103: Unmanned Lunar Module (LM) test
Line 104: 3.
Line 105: Manned CSM in low Earth orbit
Line 106: 4.
Line 107: Manned CSM and LM in low Earth orbit
Line 108: 5.
Line 109: Manned CSM and LM in an elliptical Earth orbit with an apogee of 4600 mi
Line 110: (7400 km)
Line 111: 6.
Line 112: Manned CSM and LM in lunar orbit
Line 113: 7.
Line 114: Manned lunar landing
Line 115: At least in software, we can develop incrementally without building a new rocket
Line 116: each time.
Line 117: 41
Line 118: Start Testing with the Simplest Success Case
Line 119: 
Line 120: --- 페이지 67 ---
Line 121: Write the Test That You’d Want to Read
Line 122: We want each test to be as clear as possible an expression of the behavior to be
Line 123: performed by the system or object. While writing the test, we ignore the fact that
Line 124: the test won’t run, or even compile, and just concentrate on its text; we act as
Line 125: if the supporting code to let us run the test already exists.
Line 126: When the test reads well, we then build up the infrastructure to support the
Line 127: test. We know we’ve implemented enough of the supporting code when the test
Line 128: fails in the way we’d expect, with a clear error message describing what needs
Line 129: to be done. Only then do we start writing the code to make the test pass. We
Line 130: look further at making tests readable in Chapter 21.
Line 131: Watch the Test Fail
Line 132: We always watch the test fail before writing the code to make it pass, and check
Line 133: the diagnostic message. If the test fails in a way we didn’t expect, we know we’ve
Line 134: misunderstood something or the code is incomplete, so we ﬁx that. When we get
Line 135: the “right” failure, we check that the diagnostics are helpful. If the failure descrip-
Line 136: tion isn’t clear, someone (probably us) will have to struggle when the code breaks
Line 137: in a few weeks’ time. We adjust the test code and rerun the tests until the error
Line 138: messages guide us to the problem with the code (Figure 5.2).
Line 139: Figure 5.2
Line 140: Improving the diagnostics as part of the TDD cycle
Line 141: As we write the production code, we keep running the test to see our progress
Line 142: and to check the error diagnostics as the system is built up behind the test. Where
Line 143: necessary, we extend or modify the support code to ensure the error messages
Line 144: are always clear and relevant.
Line 145: There’s more than one reason for insisting on checking the error messages.
Line 146: First, it checks our assumptions about the code we’re working on—sometimes
Line 147: Chapter 5
Line 148: Maintaining the Test-Driven Cycle
Line 149: 42
Line 150: 
Line 151: --- 페이지 68 ---
Line 152: we’re wrong. Second, more subtly, we ﬁnd that our emphasis on (or, perhaps,
Line 153: mania for) expressing our intentions is fundamental for developing reliable,
Line 154: maintainable systems—and for us that includes tests and failure messages. Taking
Line 155: the trouble to generate a useful diagnostic helps us clarify what the test, and
Line 156: therefore the code, is supposed to do. We look at error diagnostics and how to
Line 157: improve them in Chapter 23.
Line 158: Develop from the Inputs to the Outputs
Line 159: We start developing a feature by considering the events coming into the system
Line 160: that will trigger the new behavior. The end-to-end tests for the feature will simu-
Line 161: late these events arriving. At the boundaries of our system, we will need to write
Line 162: one or more objects to handle these events. As we do so, we discover that these
Line 163: objects need supporting services from the rest of the system to perform their re-
Line 164: sponsibilities. We write more objects to implement these services, and discover
Line 165: what services these new objects need in turn.
Line 166: In this way, we work our way through the system: from the objects that receive
Line 167: external events, through the intermediate layers, to the central domain model,
Line 168: and then on to other boundary objects that generate an externally visible response.
Line 169: That might mean accepting some text and a mouse click and looking for a record
Line 170: in a database, or receiving a message in a queue and looking for a ﬁle on a server.
Line 171: It’s tempting to start by unit-testing new domain model objects and then trying
Line 172: to hook them into the rest of the application. It seems easier at the start—we feel
Line 173: we’re making rapid progress working on the domain model when we don’t have
Line 174: to make it ﬁt into anything—but we’re more likely to get bitten by integration
Line 175: problems later. We’ll have wasted time building unnecessary or incorrect func-
Line 176: tionality, because we weren’t receiving the right kind of feedback when we were
Line 177: working on it.
Line 178: Unit-Test Behavior, Not Methods
Line 179: We’ve learned the hard way that just writing lots of tests, even when it produces
Line 180: high test coverage, does not guarantee a codebase that’s easy to work with. Many
Line 181: developers who adopt TDD ﬁnd their early tests hard to understand when they
Line 182: revisit them later, and one common mistake is thinking about testing methods.
Line 183: A test called testBidAccepted() tells us what it does, but not what it’s for.
Line 184: We do better when we focus on the features that the object under test should
Line 185: provide, each of which may require collaboration with its neighbors and calling
Line 186: more than one of its methods. We need to know how to use the class to achieve
Line 187: a goal, not how to exercise all the paths through its code.
Line 188: 43
Line 189: Unit-Test Behavior, Not Methods
Line 190: 
Line 191: --- 페이지 69 ---
Line 192: The Importance of Describing Behavior, Not API Features
Line 193: Nat used to run a company that produced online advertising and branded content
Line 194: for clients sponsoring sports teams. One of his clients sponsored a Formula One
Line 195: racing team. Nat wrote a fun little game that simulated Formula One race strategies
Line 196: for the client to put on the team’s website. It took him two weeks to write, from
Line 197: initial idea to ﬁnal deliverable, and once he handed it over to the client he forgot
Line 198: all about it.
Line 199: It turned out, however, that the throw-away game was by far the most popular
Line 200: content on the team’s website. For the next F1 season, the client wanted to capi-
Line 201: talize on its success. They wanted the game to model the track of each Grand
Line 202: Prix, to accommodate the latest F1 rules, to have a better model of car physics,
Line 203: to simulate dynamic weather, overtaking, spin-outs, and more.
Line 204: Nat had written the original version test-ﬁrst, so he expected it to be easy to
Line 205: change. However, going back to the code, he found the tests very hard to under-
Line 206: stand. He had written a test for each method of each object but couldn’t understand
Line 207: from those tests how each object was meant to behave—what the responsibilities
Line 208: of the object were and how the different methods of the object worked together.
Line 209: It helps to choose test names that describe how the object behaves in the
Line 210: scenario being tested. We look at this in more detail in “Test Names Describe
Line 211: Features” (page 248).
Line 212: Listen to the Tests
Line 213: When writing unit and integration tests, we stay alert for areas of the code that
Line 214: are difﬁcult to test. When we ﬁnd a feature that’s difﬁcult to test, we don’t just
Line 215: ask ourselves how to test it, but also why is it difﬁcult to test.
Line 216: Our experience is that, when code is difﬁcult to test, the most likely cause is
Line 217: that our design needs improving. The same structure that makes the code difﬁcult
Line 218: to test now will make it difﬁcult to change in the future. By the time that future
Line 219: comes around, a change will be more difﬁcult still because we’ll have forgotten
Line 220: what we were thinking when we wrote the code. For a successful system, it might
Line 221: even be a completely different team that will have to live with the consequences
Line 222: of our decisions.
Line 223: Our response is to regard the process of writing tests as a valuable early
Line 224: warning of potential maintenance problems and to use those hints to ﬁx a problem
Line 225: while it’s still fresh. As Figure 5.3 shows, if we’re ﬁnding it hard to write the next
Line 226: failing test, we look again at the design of the production code and often refactor
Line 227: it before moving on.
Line 228: Chapter 5
Line 229: Maintaining the Test-Driven Cycle
Line 230: 44
Line 231: 
Line 232: --- 페이지 70 ---
Line 233: Figure 5.3
Line 234: Difﬁculties writing tests may suggest a need to ﬁx
Line 235: production code
Line 236: This is an example of how our maxim—“Expect Unexpected Changes”—guides
Line 237: development. If we keep up the quality of the system by refactoring when we see
Line 238: a weakness in the design, we will be able to make it respond to whatever changes
Line 239: turn up. The alternative is the usual “software rot” where the code decays until
Line 240: the team just cannot respond to the needs of its customers. We’ll return to this
Line 241: topic in Chapter 20.
Line 242: Tuning the Cycle
Line 243: There’s a balance between exhaustively testing execution paths and testing inte-
Line 244: gration. If we test at too large a grain, the combinatorial explosion of trying all
Line 245: the possible paths through the code will bring development to a halt. Worse,
Line 246: some of those paths, such as throwing obscure exceptions, will be impractical to
Line 247: test from that level. On the other hand, if we test at too ﬁne a grain—just at the
Line 248: class level, for example—the testing will be easier but we’ll miss problems that
Line 249: arise from objects not working together.
Line 250: How much unit testing should we do, using mock objects to break external
Line 251: dependencies, and how much integration testing? We don’t think there’s a single
Line 252: answer to this question. It depends too much on the context of the team and its
Line 253: environment. The best we can get from the testing part of TDD (which is a lot)
Line 254: is the conﬁdence that we can change the code without breaking it: Fear kills
Line 255: progress. The trick is to make sure that the conﬁdence is justiﬁed.
Line 256: So, we regularly reﬂect on how well TDD is working for us, identify any
Line 257: weaknesses, and adapt our testing strategy. Fiddly bits of logic might need more
Line 258: unit testing (or, alternatively, simpliﬁcation); unhandled exceptions might need
Line 259: more integration-level testing; and, unexpected system failures will need more
Line 260: investigation and, possibly, more testing throughout.
Line 261: 45
Line 262: Tuning the Cycle
Line 263: 
Line 264: --- 페이지 71 ---
Line 265: This page intentionally left blank 
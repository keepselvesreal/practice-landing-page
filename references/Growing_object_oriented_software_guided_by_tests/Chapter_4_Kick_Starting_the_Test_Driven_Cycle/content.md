Line 1: 
Line 2: --- 페이지 56 ---
Line 3: Chapter 4
Line 4: Kick-Starting the Test-Driven
Line 5: Cycle
Line 6: We should be taught not to wait for inspiration to start a thing. Action
Line 7: always generates inspiration. Inspiration seldom generates action.
Line 8: —Frank Tibolt
Line 9: Introduction
Line 10: The TDD process we described in Chapter 1 assumes that we can grow the system
Line 11: by just slotting the tests for new features into an existing infrastructure. But what
Line 12: about the very ﬁrst feature, before we have this infrastructure? As an acceptance
Line 13: test, it must run end-to-end to give us the feedback we need about the system’s
Line 14: external interfaces, which means we must have implemented a whole automated
Line 15: build, deploy, and test cycle. This is a lot of work to do before we can even see
Line 16: our ﬁrst test fail.
Line 17: Deploying and testing right from the start of a project forces the team to un-
Line 18: derstand how their system ﬁts into the world. It ﬂushes out the “unknown
Line 19: unknown” technical and organizational risks so they can be addressed while
Line 20: there’s still time. Attempting to deploy also helps the team understand who they
Line 21: need to liaise with, such as system administrators or external vendors, and start
Line 22: to build those relationships.
Line 23: Starting with “build, deploy, and test” on a nonexistent system sounds odd,
Line 24: but we think it’s essential. The risks of leaving it to later are just too high. We
Line 25: have seen projects canceled after months of development because they could not
Line 26: reliably deploy their system. We have seen systems discarded because new features
Line 27: required months of manual regression testing and even then the error rates were
Line 28: too high. As always, we view feedback as a fundamental tool, and we want to
Line 29: know as early as possible whether we’re moving in the right direction. Then,
Line 30: once we have our ﬁrst test in place, subsequent tests will be much quicker to write.
Line 31: 31
Line 32: 
Line 33: --- 페이지 57 ---
Line 34: First, Test a Walking Skeleton
Line 35: The quandary in writing and passing the ﬁrst acceptance test is that it’s hard to
Line 36: build both the tooling and the feature it’s testing at the same time. Changes in
Line 37: one disrupt any progress made with the other, and tracking down failures is
Line 38: tricky when the architecture, the tests, and the production code are all moving.
Line 39: One of the symptoms of an unstable development environment is that there’s no
Line 40: obvious ﬁrst place to look when something fails.
Line 41: We can cut through this “ﬁrst-feature paradox” by splitting it into two smaller
Line 42: problems. First, work out how to build, deploy, and test a “walking skeleton,”
Line 43: then use that infrastructure to write the acceptance tests for the ﬁrst meaningful
Line 44: feature. After that, everything will be in place for test-driven development of the
Line 45: rest of the system.
Line 46: A “walking skeleton” is an implementation of the thinnest possible slice of
Line 47: real functionality that we can automatically build, deploy, and test end-to-end
Line 48: [Cockburn04]. It should include just enough of the automation, the major com-
Line 49: ponents, and communication mechanisms to allow us to start working on the
Line 50: ﬁrst feature. We keep the skeleton’s application functionality so simple that it’s
Line 51: obvious and uninteresting, leaving us free to concentrate on the infrastructure.
Line 52: For example, for a database-backed web application, a skeleton would show a
Line 53: ﬂat web page with ﬁelds from the database. In Chapter 10, we’ll show an example
Line 54: that displays a single value in the user interface and sends just a handshake
Line 55: message to the server.
Line 56: It’s also important to realize that the “end” in “end-to-end” refers to the pro-
Line 57: cess, as well as the system. We want our test to start from scratch, build a deploy-
Line 58: able system, deploy it into a production-like environment, and then run the tests
Line 59: through the deployed system. Including the deployment step in the testing process
Line 60: is critical for two reasons. First, this is the sort of error-prone activity that should
Line 61: not be done by hand, so we want our scripts to have been thoroughly exercised
Line 62: by the time we have to deploy for real. One lesson that we’ve learned repeatedly
Line 63: is that nothing forces us to understand a process better than trying to automate
Line 64: it. Second, this is often the moment where the development team bumps into the
Line 65: rest of the organization and has to learn how it operates. If it’s going to take six
Line 66: weeks and four signatures to set up a database, we want to know now, not
Line 67: two weeks before delivery.
Line 68: In practice, of course, real end-to-end testing may be so hard to achieve that
Line 69: we have to start with infrastructure that implements our current understanding
Line 70: of what the real system will do and what its environment is. We keep in mind,
Line 71: however, that this is a stop-gap, a temporary patch until we can ﬁnish the job,
Line 72: and that unknown risks remain until our tests really run end-to-end. One of the
Line 73: weaknesses of our Auction Sniper example (Part III) is that the tests run against
Line 74: Chapter 4
Line 75: Kick-Starting the Test-Driven Cycle
Line 76: 32
Line 77: 
Line 78: --- 페이지 58 ---
Line 79: a dummy server, not the real site. At some point before going live, we would
Line 80: have had to test against Southabee’s On-Line; the earlier we can do that, the
Line 81: easier it will be for us to respond to any surprises that turn up.
Line 82: Whilst building the “walking skeleton,” we concentrate on the structure and
Line 83: don’t worry too much about cleaning up the test to be beautifully expressive.
Line 84: The walking skeleton and its supporting infrastructure are there to help us work
Line 85: out how to start test-driven development. It’s only the ﬁrst step toward a complete
Line 86: end-to-end acceptance-testing solution. When we write the test for the ﬁrst feature,
Line 87: then we need to “write the test you want to read” (page 42) to make sure that
Line 88: it’s a clear expression of the behavior of the system.
Line 89: The Importance of Early End-to-End Testing
Line 90: We joined a project that had been running for a couple of years but had never
Line 91: tested their entire system end-to-end. There were frequent production outages
Line 92: and deployments often failed. The system was large and complex, reﬂecting the
Line 93: complicated business transactions it managed.The effort of building an automated,
Line 94: end-to-end test suite was so large that an entire new team had to be formed to
Line 95: perform the work. It took them months to build an end-to-end test environment,
Line 96: and they never managed to get the entire system covered by an end-to-end
Line 97: test suite.
Line 98: Because the need for end-to-end testing had not inﬂuenced its design, the system
Line 99: was difﬁcult to test. For example, the system’s components used internal timers
Line 100: to schedule activities, some of them days or weeks into the future. This made it
Line 101: very difﬁcult to write end-to-end tests: It was impractical to run the tests in real-
Line 102: time but the scheduling could not be inﬂuenced from outside the system. The
Line 103: developers had to redesign the system itself so that periodic activities were trig-
Line 104: gered by messages sent from a remote scheduler which could be replaced in the
Line 105: test environment; see “Externalize Event Sources” (page 326).This was a signiﬁ-
Line 106: cant architectural change—and it was very risky because it had to be performed
Line 107: without end-to-end test coverage.
Line 108: Deciding the Shape of the Walking Skeleton
Line 109: The development of a “walking skeleton” is the moment when we start to make
Line 110: choices about the high-level structure of our application. We can’t automate the
Line 111: build, deploy, and test cycle without some idea of the overall structure. We don’t
Line 112: need much detail yet, just a broad-brush picture of what major system components
Line 113: will be needed to support the ﬁrst planned release and how they will communicate.
Line 114: Our rule of thumb is that we should be able to draw the design for the “walking
Line 115: skeleton” in a few minutes on a whiteboard.
Line 116: 33
Line 117: Deciding the Shape of the Walking Skeleton
Line 118: 
Line 119: --- 페이지 59 ---
Line 120: Mappa Mundi
Line 121: We ﬁnd that maintaining a public drawing of the structure of the system, for example
Line 122: on the wall in the team’s work area as in Figure 4.1, helps the team stay oriented
Line 123: when working on the code.
Line 124: Figure 4.1
Line 125: A broad-brush architecture diagram drawn on the
Line 126: wall of a team’s work area
Line 127: To design this initial structure, we have to have some understanding of the
Line 128: purpose of the system, otherwise the whole exercise risks being meaningless. We
Line 129: need a high-level view of the client’s requirements, both functional and non-
Line 130: functional, to guide our choices. This preparatory work is part of the chartering
Line 131: of the project, which we must leave as outside the scope of this book.
Line 132: The point of the “walking skeleton” is to use the writing of the ﬁrst test to
Line 133: draw out the context of the project, to help the team map out the landscape of
Line 134: their solution—the essential decisions that they must take before they can write
Line 135: any code; Figure 4.2 shows how the TDD process we drew in Figure 1.2 ﬁts into
Line 136: this context.
Line 137: Chapter 4
Line 138: Kick-Starting the Test-Driven Cycle
Line 139: 34
Line 140: 
Line 141: --- 페이지 60 ---
Line 142: Figure 4.2
Line 143: The context of the ﬁrst test
Line 144: Please don’t confuse this with doing “Big Design Up Front” (BDUF) which
Line 145: has such a bad reputation in the Agile Development community. We’re not trying
Line 146: to elaborate the whole design down to classes and algorithms before we start
Line 147: coding. Any ideas we have now are likely to be wrong, so we prefer to discover
Line 148: those details as we grow the system. We’re making the smallest number of
Line 149: decisions we can to kick-start the TDD cycle, to allow us to start learning and
Line 150: improving from real feedback.
Line 151: Build Sources of Feedback
Line 152: We have no guarantees that the decisions we’ve taken about the design of our
Line 153: application, or the assumptions on which they’re based, are right. We do the best
Line 154: we can, but the only thing we can rely on is validating them as soon as possible
Line 155: by building feedback into our process. The tools we build to implement the
Line 156: “walking skeleton” are there to support this learning process. Of course, these
Line 157: tools too will not be perfect, and we expect we will improve them incrementally
Line 158: as we learn how well they support the team.
Line 159: Our ideal situation is where the team releases regularly to a real production
Line 160: system, as in Figure 4.3. This allows the system’s stakeholders to respond to how
Line 161: well the system meets their needs, at the same time allowing us to judge its
Line 162: implementation.
Line 163: Figure 4.3
Line 164: Requirements feedback
Line 165: 35
Line 166: Build Sources of Feedback
Line 167: 
Line 168: --- 페이지 61 ---
Line 169: We use the automation of building and testing to give us feedback on qualities
Line 170: of the system, such as how easily we can cut a version and deploy, how well the
Line 171: design works, and how good the code is. The automated deployment helps us
Line 172: release frequently to real users, which gives us feedback on how well we have
Line 173: understood the domain and whether seeing the system in practice has changed
Line 174: our customer’s priorities.
Line 175: The great beneﬁt is that we will be able to make changes in response to what-
Line 176: ever we learn, because writing everything test-ﬁrst means that we will have a
Line 177: thorough set of regression tests. No tests are perfect, of course, but in practice
Line 178: we’ve found that a substantial test suite allows us to make major changes safely.
Line 179: Expose Uncertainty Early
Line 180: All this effort means that teams are frequently surprised by the time it takes to
Line 181: get a “walking skeleton” working, considering that it does hardly anything.
Line 182: That’s because this ﬁrst step involves establishing a lot of infrastructure and
Line 183: asking (and answering) many awkward questions. The time to implement the
Line 184: ﬁrst few features will be unpredictable as the team discovers more about its re-
Line 185: quirements and target environment. For a new team, this will be compounded
Line 186: by the social stresses of learning how to work together.
Line 187: Fred Tingey, a colleague, once observed that incremental development can be
Line 188: disconcerting for teams and management who aren’t used to it because it front-
Line 189: loads the stress in a project. Projects with late integration start calmly but gener-
Line 190: ally turn difﬁcult towards the end as the team tries to pull the system together
Line 191: for the ﬁrst time. Late integration is unpredictable because the team has to
Line 192: assemble a great many moving parts with limited time and budget to ﬁx any
Line 193: failures. The result is that experienced stakeholders react badly to the instability
Line 194: at the start of an incremental project because they expect that the end of the
Line 195: project will be much worse.
Line 196: Our experience is that a well-run incremental development runs in the opposite
Line 197: direction. It starts unsettled but then, after a few features have been implemented
Line 198: and the project automation has been built up, settles in to a routine. As a project
Line 199: approaches delivery, the end-game should be a steady production of functionality,
Line 200: perhaps with a burst of activity before the ﬁrst release. All the mundane but
Line 201: brittle tasks, such as deployment and upgrades, will have been automated so that
Line 202: they “just work.” The contrast looks rather like Figure 4.4.
Line 203: This aspect of test-driven development, like others, may appear counter-
Line 204: intuitive, but we’ve always found it worth taking enough time to structure and
Line 205: automate the basics of the system—or at least a ﬁrst cut. Of course, we don’t
Line 206: want to spend the whole project setting up a perfect “walking skeleton,” so we
Line 207: limit ourselves to whiteboard-level decisions and reserve the right to change our
Line 208: mind when we have to. But the most important thing is to have a sense of direction
Line 209: and a concrete implementation to test our assumptions.
Line 210: Chapter 4
Line 211: Kick-Starting the Test-Driven Cycle
Line 212: 36
Line 213: 
Line 214: --- 페이지 62 ---
Line 215: Figure 4.4
Line 216: Visible uncertainty in test-ﬁrst and test-later projects
Line 217: A “walking skeleton” will ﬂush out issues early in the project when there’s
Line 218: still time, budget, and goodwill to address them.
Line 219: Brownﬁeld Development
Line 220: We don’t always have the luxury of building a new system from the ground up.
Line 221: Many of our projects have started with an existing system that must be extended,
Line 222: adapted, or replaced. In such cases, we can’t start by building a “walking skeleton”;
Line 223: we have to work with what already exists, no matter how hostile its structure.
Line 224: That said, the process of kick-starting TDD of an existing system is not fundamen-
Line 225: tally different from applying it to a new system—although it may be orders of
Line 226: magnitude more difﬁcult because of the technical baggage the system already
Line 227: carries. Michael Feathers has written a whole book on the topic, [Feathers04].
Line 228: It is risky to start reworking a system when there are no tests to detect regressions.
Line 229: The safest way to start the TDD process is to automate the build and deploy pro-
Line 230: cess, and then add end-to-end tests that cover the areas of the code we need to
Line 231: change. With that protection, we can start to address internal quality issues with
Line 232: more conﬁdence, refactoring the code and introducing unit tests as we add func-
Line 233: tionality.
Line 234: The easiest way to start building an end-to-end test infrastructure is with the sim-
Line 235: plest path through the system that we can ﬁnd. Like a “walking skeleton,” this lets
Line 236: us build up some supporting infrastructure before we tackle the harder problems
Line 237: of testing more complicated functionality.
Line 238: 37
Line 239: Expose Uncertainty Early
Line 240: 
Line 241: --- 페이지 63 ---
Line 242: This page intentionally left blank 
Line 1: 
Line 2: --- 페이지 28 ---
Line 3: Chapter 1
Line 4: What Is the Point of
Line 5: Test-Driven Development?
Line 6: One must learn by doing the thing; for though you think you know it,
Line 7: you have no certainty, until you try.
Line 8: —Sophocles
Line 9: Software Development as a Learning Process
Line 10: Almost all software projects are attempting something that nobody has done
Line 11: before (or at least that nobody in the organization has done before). That some-
Line 12: thing may refer to the people involved, the application domain, the technology
Line 13: being used, or (most likely) a combination of these. In spite of the best efforts of
Line 14: our discipline, all but the most routine projects have elements of surprise. Inter-
Line 15: esting projects—those likely to provide the most beneﬁt—usually have a lot
Line 16: of surprises.
Line 17: Developers often don’t completely understand the technologies they’re using.
Line 18: They have to learn how the components work whilst completing the project.
Line 19: Even if they have a good understanding of the technologies, new applications
Line 20: can force them into unfamiliar corners. A system that combines many signiﬁcant
Line 21: components (which means most of what a professional programmer works on)
Line 22: will be too complex for any individual to understand all of its possibilities.
Line 23: For customers and end users, the experience is worse. The process of building
Line 24: a system forces them to look at their organization more closely than they have
Line 25: before. They’re often left to negotiate and codify processes that, until now,
Line 26: have been based on convention and experience.
Line 27: Everyone involved in a software project has to learn as it progresses. For the
Line 28: project to succeed, the people involved have to work together just to understand
Line 29: what they’re supposed to achieve, and to identify and resolve misunderstandings
Line 30: along the way. They all know there will be changes, they just don’t know what
Line 31: changes. They need a process that will help them cope with uncertainty as their
Line 32: experience grows—to anticipate unanticipated changes.
Line 33: 3
Line 34: 
Line 35: --- 페이지 29 ---
Line 36: Feedback Is the Fundamental Tool
Line 37: We think that the best approach a team can take is to use empirical feedback to
Line 38: learn about the system and its use, and then apply that learning back to the system.
Line 39: A team needs repeated cycles of activity. In each cycle it adds new features and
Line 40: gets feedback about the quantity and quality of the work already done. The team
Line 41: members split the work into time boxes, within which they analyze, design,
Line 42: implement, and deploy as many features as they can.
Line 43: Deploying completed work to some kind of environment at each cycle is critical.
Line 44: Every time a team deploys, its members have an opportunity to check their as-
Line 45: sumptions against reality. They can measure how much progress they’re really
Line 46: making, detect and correct any errors, and adapt the current plan in response to
Line 47: what they’ve learned. Without deployment, the feedback is not complete.
Line 48: In our work, we apply feedback cycles at every level of development, organizing
Line 49: projects as a system of nested loops ranging from seconds to months, such as:
Line 50: pair programming, unit tests, acceptance tests, daily meetings, iterations, releases,
Line 51: and so on. Each loop exposes the team’s output to empirical feedback so that
Line 52: the team can discover and correct any errors or misconceptions. The nested
Line 53: feedback loops reinforce each other; if a discrepancy slips through an inner loop,
Line 54: there is a good chance an outer loop will catch it.
Line 55: Each feedback loop addresses different aspects of the system and development
Line 56: process. The inner loops are more focused on the technical detail: what a unit of
Line 57: code does, whether it integrates with the rest of the system. The outer loops are
Line 58: more focused on the organization and the team: whether the application serves
Line 59: its users’ needs, whether the team is as effective as it could be.
Line 60: The sooner we can get feedback about any aspect of the project, the better.
Line 61: Many teams in large organizations can release every few weeks. Some teams re-
Line 62: lease every few days, or even hours, which gives them an order of magnitude
Line 63: increase in opportunities to receive and respond to feedback from real users.
Line 64: Incremental and Iterative Development
Line 65: In a project organized as a set of nested feedback loops, development is
Line 66: incremental and iterative.
Line 67: Incremental development builds a system feature by feature, instead of building
Line 68: all the layers and components and integrating them at the end. Each feature is
Line 69: implemented as an end-to-end “slice” through all the relevant parts of the system.
Line 70: The system is always integrated and ready for deployment.
Line 71: Iterative development progressively reﬁnes the implementation of features in
Line 72: response to feedback until they are good enough.
Line 73: Chapter 1
Line 74: What Is the Point of Test-Driven Development?
Line 75: 4
Line 76: 
Line 77: --- 페이지 30 ---
Line 78: Practices That Support Change
Line 79: We’ve found that we need two technical foundations if we want to grow a system
Line 80: reliably and to cope with the unanticipated changes that always happen. First,
Line 81: we need constant testing to catch regression errors, so we can add new features
Line 82: without breaking existing ones. For systems of any interesting size, frequent
Line 83: manual testing is just impractical, so we must automate testing as much as we
Line 84: can to reduce the costs of building, deploying, and modifying versions of the
Line 85: system.
Line 86: Second, we need to keep the code as simple as possible, so it’s easier to under-
Line 87: stand and modify. Developers spend far more time reading code than writing it,
Line 88: so that’s what we should optimize for.1 Simplicity takes effort, so we constantly
Line 89: refactor [Fowler99] our code as we work with it—to improve and simplify its
Line 90: design, to remove duplication, and to ensure that it clearly expresses what it does.
Line 91: The test suites in the feedback loops protect us against our own mistakes as we
Line 92: improve (and therefore change) the code.
Line 93: The catch is that few developers enjoy testing their code. In many development
Line 94: groups, writing automated tests is seen as not “real” work compared to adding
Line 95: features, and boring as well. Most people do not do as well as they should at
Line 96: work they ﬁnd uninspiring.
Line 97: Test-Driven Development (TDD) turns this situation on its head. We write
Line 98: our tests before we write the code. Instead of just using testing to verify our work
Line 99: after it’s done, TDD turns testing into a design activity. We use the tests to clarify
Line 100: our ideas about what we want the code to do. As Kent Beck described it to us,
Line 101: “I was ﬁnally able to separate logical from physical design. I’d always been told
Line 102: to do that but no one ever explained how.” We ﬁnd that the effort of writing a
Line 103: test ﬁrst also gives us rapid feedback about the quality of our design ideas—that
Line 104: making code accessible for testing often drives it towards being cleaner and more
Line 105: modular.
Line 106: If we write tests all the way through the development process, we can build
Line 107: up a safety net of automated regression tests that give us the conﬁdence to make
Line 108: changes.
Line 109: “… you have nothing to lose but your bugs”
Line 110: We cannot emphasize strongly enough how liberating it is to work on test-driven
Line 111: code that has thorough test coverage.We ﬁnd that we can concentrate on the task
Line 112: in hand, conﬁdent that we’re doing the right work and that it’s actually quite hard
Line 113: to break the system—as long as we follow the practices.
Line 114: 1. Begel and Simon [Begel08] showed that new graduates at Microsoft spend most of
Line 115: their ﬁrst year just reading code.
Line 116: 5
Line 117: Practices That Support Change
Line 118: 
Line 119: --- 페이지 31 ---
Line 120: Test-Driven Development in a Nutshell
Line 121: The cycle at the heart of TDD is: write a test; write some code to get it working;
Line 122: refactor the code to be as simple an implementation of the tested features as
Line 123: possible. Repeat.
Line 124: Figure 1.1
Line 125: The fundamental TDD cycle
Line 126: As we develop the system, we use TDD to give us feedback on the quality of
Line 127: both its implementation (“Does it work?”) and design (“Is it well structured?”).
Line 128: Developing test-ﬁrst, we ﬁnd we beneﬁt twice from the effort. Writing tests:
Line 129: •
Line 130: makes us clarify the acceptance criteria for the next piece of work—we
Line 131: have to ask ourselves how we can tell when we’re done (design);
Line 132: •
Line 133: encourages us to write loosely coupled components, so they can easily be
Line 134: tested in isolation and, at higher levels, combined together (design);
Line 135: •
Line 136: adds an executable description of what the code does (design); and,
Line 137: •
Line 138: adds to a complete regression suite (implementation);
Line 139: whereas running tests:
Line 140: •
Line 141: detects errors while the context is fresh in our mind (implementation); and,
Line 142: •
Line 143: lets us know when we’ve done enough, discouraging “gold plating” and
Line 144: unnecessary features (design).
Line 145: This feedback cycle can be summed up by the Golden Rule of TDD:
Line 146: The Golden Rule of Test-Driven Development
Line 147: Never write new functionality without a failing test.
Line 148: Chapter 1
Line 149: What Is the Point of Test-Driven Development?
Line 150: 6
Line 151: 
Line 152: --- 페이지 32 ---
Line 153: Refactoring.Think Local, Act Local
Line 154: Refactoring means changing the internal structure of an existing body of code
Line 155: without changing its behavior.The point is to improve the code so that it’s a better
Line 156: representation of the features it implements, making it more maintainable.
Line 157: Refactoring is a disciplined technique where the programmer applies a series of
Line 158: transformations (or “refactorings”) that do not change the code’s behavior. Each
Line 159: refactoring is small enough to be easy to understand and “safe”; for example, a
Line 160: programmer might pull a block of code into a helper method to make the original
Line 161: method shorter and easier to understand. The programmer makes sure that the
Line 162: system is still working after each refactoring step, minimizing the risk of getting
Line 163: stranded by a change; in test-driven code, we can do that by running the tests.
Line 164: Refactoring is a “microtechnique” that is driven by ﬁnding small-scale im-
Line 165: provements. Our experience is that, applied rigorously and consistently, its many
Line 166: small steps can lead to signiﬁcant structural improvements. Refactoring is not the
Line 167: same activity as redesign, where the programmers take a conscious decision to
Line 168: change a large-scale structure. That said, having taken a redesign decision, a
Line 169: team can use refactoring techniques to get to the new design incrementally
Line 170: and safely.
Line 171: You’ll see quite a lot of refactoring in our example in Part III. The standard text on
Line 172: the concept is Fowler’s [Fowler99].
Line 173: The Bigger Picture
Line 174: It is tempting to start the TDD process by writing unit tests for classes in the
Line 175: application. This is better than having no tests at all and can catch those basic
Line 176: programming errors that we all know but ﬁnd so hard to avoid: fencepost errors,
Line 177: incorrect boolean expressions, and the like. But a project with only unit tests is
Line 178: missing out on critical beneﬁts of the TDD process. We’ve seen projects with
Line 179: high-quality, well unit-tested code that turned out not to be called from anywhere,
Line 180: or that could not be integrated with the rest of the system and had to be rewritten.
Line 181: How do we know where to start writing code? More importantly, how do we
Line 182: know when to stop writing code? The golden rule tells us what we need to do:
Line 183: Write a failing test.
Line 184: When we’re implementing a feature, we start by writing an acceptance test,
Line 185: which exercises the functionality we want to build. While it’s failing, an acceptance
Line 186: test demonstrates that the system does not yet implement that feature; when it
Line 187: passes, we’re done. When working on a feature, we use its acceptance test to
Line 188: guide us as to whether we actually need the code we’re about to write—we only
Line 189: write code that’s directly relevant. Underneath the acceptance test, we follow the
Line 190: unit level test/implement/refactor cycle to develop the feature; the whole cycle
Line 191: looks like Figure 1.2.
Line 192: 7
Line 193: The Bigger Picture
Line 194: 
Line 195: --- 페이지 33 ---
Line 196: Figure 1.2
Line 197: Inner and outer feedback loops in TDD
Line 198: The outer test loop is a measure of demonstrable progress, and the growing
Line 199: suite of tests protects us against regression failures when we change the system.
Line 200: Acceptance tests often take a while to make pass, certainly more than one check-in
Line 201: episode, so we usually distinguish between acceptance tests we’re working on
Line 202: (which are not yet included in the build) and acceptance tests for the features
Line 203: that have been ﬁnished (which are included in the build and must always pass).
Line 204: The inner loop supports the developers. The unit tests help us maintain the
Line 205: quality of the code and should pass soon after they’ve been written. Failing unit
Line 206: tests should never be committed to the source repository.
Line 207: Testing End-to-End
Line 208: Wherever possible, an acceptance test should exercise the system end-to-end
Line 209: without directly calling its internal code. An end-to-end test interacts with the
Line 210: system only from the outside: through its user interface, by sending messages as
Line 211: if from third-party systems, by invoking its web services, by parsing reports, and
Line 212: so on. As we discuss in Chapter 10, the whole behavior of the system includes
Line 213: its interaction with its external environment. This is often the riskiest and most
Line 214: difﬁcult aspect; we ignore it at our peril. We try to avoid acceptance tests that
Line 215: just exercise the internal objects of the system, unless we really need the speed-up
Line 216: and already have a stable set of end-to-end tests to provide cover.
Line 217: The Importance of End-to-End Testing: A Horror Story
Line 218: Nat was once brought onto a project that had been using TDD since its inception.
Line 219: The team had been writing acceptance tests to capture requirements and show
Line 220: progress to their customer representatives. They had been writing unit tests for
Line 221: the classes of the system, and the internals were clean and easy to change.They
Line 222: had been making great progress, and the customer representatives had signed
Line 223: off all the implemented features on the basis of the passing acceptance tests.
Line 224: Chapter 1
Line 225: What Is the Point of Test-Driven Development?
Line 226: 8
Line 227: 
Line 228: --- 페이지 34 ---
Line 229: But the acceptance tests did not run end-to-end—they instantiated the system’s
Line 230: internal objects and directly invoked their methods. The application actually did
Line 231: nothing at all. Its entry point contained only a single comment:
Line 232: // TODO implement this
Line 233: Additional feedback loops, such as regular show-and-tell sessions, should have
Line 234: been in place and would have caught this problem.
Line 235: For us, “end-to-end” means more than just interacting with the system from
Line 236: the outside—that might be better called “edge-to-edge” testing. We prefer to
Line 237: have the end-to-end tests exercise both the system and the process by which it’s
Line 238: built and deployed. An automated build, usually triggered by someone checking
Line 239: code into the source repository, will: check out the latest version; compile and
Line 240: unit-test the code; integrate and package the system; perform a production-like
Line 241: deployment into a realistic environment; and, ﬁnally, exercise the system through
Line 242: its external access points. This sounds like a lot of effort (it is), but has to be
Line 243: done anyway repeatedly during the software’s lifetime. Many of the steps might
Line 244: be ﬁddly and error-prone, so the end-to-end build cycle is an ideal candidate for
Line 245: automation. You’ll see in Chapter 10 how early in a project we get this working.
Line 246: A system is deployable when the acceptance tests all pass, because they should
Line 247: give us enough conﬁdence that everything works. There’s still, however, a ﬁnal
Line 248: step of deploying to production. In many organizations, especially large or
Line 249: heavily regulated ones, building a deployable system is only the start of a release
Line 250: process. The rest, before the new features are ﬁnally available to the end users,
Line 251: might involve different kinds of testing, handing over to operations and data
Line 252: groups, and coordinating with other teams’ releases. There may also be additional,
Line 253: nontechnical costs involved with a release, such as training, marketing, or an
Line 254: impact on service agreements for downtime. The result is a more difﬁcult release
Line 255: cycle than we would like, so we have to understand our whole technical and
Line 256: organizational environment.
Line 257: Levels of Testing
Line 258: We build a hierarchy of tests that correspond to some of the nested feedback
Line 259: loops we described above:
Line 260: Acceptance:  Does the whole system work?
Line 261: Integration:  Does our code work against code we can't change?
Line 262: Unit:  Do our objects do the right thing, are they convenient to work with?
Line 263: 9
Line 264: Levels of Testing
Line 265: 
Line 266: --- 페이지 35 ---
Line 267: There’s been a lot of discussion in the TDD world over the terminology for
Line 268: what we’re calling acceptance tests: “functional tests,” “customer tests,” “system
Line 269: tests.” Worse, our deﬁnitions are often not the same as those used by professional
Line 270: software testers. The important thing is to be clear about our intentions. We use
Line 271: “acceptance tests” to help us, with the domain experts, understand and agree on
Line 272: what we are going to build next. We also use them to make sure that we haven’t
Line 273: broken any existing features as we continue developing.
Line 274: Our preferred implementation of the “role” of acceptance testing is to write
Line 275: end-to-end tests which, as we just noted, should be as end-to-end as possible;
Line 276: our bias often leads us to use these terms interchangeably although, in some
Line 277: cases, acceptance tests might not be end-to-end.
Line 278: We use the term integration tests to refer to the tests that check how some of
Line 279: our code works with code from outside the team that we can’t change. It might
Line 280: be a public framework, such as a persistence mapper, or a library from another
Line 281: team within our organization. The distinction is that integration tests make sure
Line 282: that any abstractions we build over third-party code work as we expect. In a
Line 283: small system, such as the one we develop in Part III, acceptance tests might be
Line 284: enough. In most professional development, however, we’ll want integration tests
Line 285: to help tease out conﬁguration issues with the external packages, and to give
Line 286: quicker feedback than the (inevitably) slower acceptance tests.
Line 287: We won’t write much more about techniques for acceptance and integration
Line 288: testing, since both depend on the technologies involved and even the culture of
Line 289: the organization. You’ll see some examples in Part III which we hope give a sense
Line 290: of the motivation for acceptance tests and show how they ﬁt in the development
Line 291: cycle. Unit testing techniques, however, are speciﬁc to a style of programming,
Line 292: and so are common across all systems that take that approach—in our case, are
Line 293: object-oriented.
Line 294: External and Internal Quality
Line 295: There’s another way of looking at what the tests can tell us about a system. We
Line 296: can make a distinction between external and internal quality: External quality
Line 297: is how well the system meets the needs of its customers and users (is it functional,
Line 298: reliable, available, responsive, etc.), and internal quality is how well it meets the
Line 299: needs of its developers and administrators (is it easy to understand, easy to change,
Line 300: etc.). Everyone can understand the point of external quality; it’s usually part of
Line 301: the contract to build. The case for internal quality is equally important but is
Line 302: often harder to make. Internal quality is what lets us cope with continual and
Line 303: unanticipated change which, as we saw at the beginning of this chapter, is a fact
Line 304: of working with software. The point of maintaining internal quality is to allow
Line 305: us to modify the system’s behavior safely and predictably, because it minimizes
Line 306: the risk that a change will force major rework.
Line 307: Chapter 1
Line 308: What Is the Point of Test-Driven Development?
Line 309: 10
Line 310: 
Line 311: --- 페이지 36 ---
Line 312: Running end-to-end tests tells us about the external quality of our system, and
Line 313: writing them tells us something about how well we (the whole team) understand
Line 314: the domain, but end-to-end tests don’t tell us how well we’ve written the code.
Line 315: Writing unit tests gives us a lot of feedback about the quality of our code, and
Line 316: running them tells us that we haven’t broken any classes—but, again, unit tests
Line 317: don’t give us enough conﬁdence that the system as a whole works. Integration
Line 318: tests fall somewhere in the middle, as in Figure 1.3.
Line 319: Figure 1.3
Line 320: Feedback from tests
Line 321: Thorough unit testing helps us improve the internal quality because, to be
Line 322: tested, a unit has to be structured to run outside the system in a test ﬁxture. A
Line 323: unit test for an object needs to create the object, provide its dependencies, interact
Line 324: with it, and check that it behaved as expected. So, for a class to be easy to unit-
Line 325: test, the class must have explicit dependencies that can easily be substituted and
Line 326: clear responsibilities that can easily be invoked and veriﬁed. In software engineer-
Line 327: ing terms, that means that the code must be loosely coupled and highly
Line 328: cohesive—in other words, well-designed.
Line 329: When we’ve got this wrong—when a class, for example, is tightly coupled to
Line 330: distant parts of the system, has implicit dependencies, or has too many or unclear
Line 331: responsibilities—we ﬁnd unit tests difﬁcult to write or understand, so writing a
Line 332: test ﬁrst gives us valuable, immediate feedback about our design. Like everyone,
Line 333: we’re tempted not to write tests when our code makes it difﬁcult, but we try to
Line 334: resist. We use such difﬁculties as an opportunity to investigate why the test is
Line 335: hard to write and refactor the code to improve its structure. We call this “listening
Line 336: to the tests,” and we’ll work through some common patterns in Chapter 20.
Line 337: 11
Line 338: External and Internal Quality
Line 339: 
Line 340: --- 페이지 37 ---
Line 341: Coupling and Cohesion
Line 342: Coupling and cohesion are metrics that (roughly) describe how easy it will be to
Line 343: change the behavior of some code.They were described by Larry Constantine in
Line 344: [Yourdon79].
Line 345: Elements are coupled if a change in one forces a change in the other. For example,
Line 346: if two classes inherit from a common parent, then a change in one class might
Line 347: require a change in the other. Think of a combo audio system: It’s tightly coupled
Line 348: because if we want to change from analog to digital radio, we must rebuild the
Line 349: whole system. If we assemble a system from separates, it would have low coupling
Line 350: and we could just swap out the receiver. “Loosely” coupled features (i.e., those
Line 351: with low coupling) are easier to maintain.
Line 352: An element’s cohesion is a measure of whether its responsibilities form a mean-
Line 353: ingful unit. For example, a class that parses both dates and URLs is not coherent,
Line 354: because they’re unrelated concepts.Think of a machine that washes both clothes
Line 355: and dishes—it’s unlikely to do both well.2 At the other extreme, a class that parses
Line 356: only the punctuation in a URL is unlikely to be coherent, because it doesn’t repre-
Line 357: sent a whole concept. To get anything done, the programmer will have to ﬁnd
Line 358: other parsers for protocol, host, resource, and so on. Features with “high”
Line 359: coherence are easier to maintain.
Line 360: 2. Actually, there was a combined clothes and dishwasher.The “Thor Automagic” was
Line 361: manufactured in the 1940s, but the idea hasn’t survived.
Line 362: Chapter 1
Line 363: What Is the Point of Test-Driven Development?
Line 364: 12
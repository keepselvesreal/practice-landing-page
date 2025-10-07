Line 1: 
Line 2: --- 페이지 248 ---
Line 3: CHAPTER 12
Line 4: Adopting Team Practices
Line 5: You last learned about TDD, a concept you can employ on your own. When you
Line 6: work in a team environment, shifting to TDD represents an effective way to
Line 7: take your unit testing practice to the next, more disciplined level. In this
Line 8: chapter, you’ll learn a few other considerations for doing unit testing within
Line 9: a team environment.
Line 10: If you’re like most of us, you’re working on a project with other team members.
Line 11: You want to be on the same page with them when it comes to unit testing.
Line 12: In this chapter, you’ll learn about working agreements that your team must
Line 13: hash out to avoid wasting time on endless debates and code thrashing. Topics
Line 14: include test standards, code/test review, and continuous integration.
Line 15: Coming up to Speed
Line 16: Incorporating a new practice like unit testing requires continual vigilance.
Line 17: Even if you enjoy writing unit tests and are good about covering the new code
Line 18: you write, you’ll sometimes face an uphill battle within your team. They might
Line 19: not be as vigilant, and they’re probably producing code at a rate that far
Line 20: outpaces your ability to test it. You might also face a team that insists on
Line 21: tossing all safeguards, tests included, in order to meet a critical deadline.
Line 22: “Unit testing isn’t free,” says Joe, “We’ve gotta deliver in two weeks. We’re way
Line 23: behind and just need to slam out code.”
Line 24: Lucia responds to Joe, “The worst possible time to throw away unit tests is
Line 25: while in crunch mode. Squeezing lots of coding into a short time will guarantee
Line 26: a mess. It’ll take longer to know if everything still works and to fix the defects
Line 27: that arise…and there’ll be a lot more of those. One way or another, we’ll pay
Line 28: dearly if we dispense with quality for short-term gains.
Line 29: report erratum  •  discuss
Line 30: 
Line 31: --- 페이지 249 ---
Line 32: “Slapping out code with no tests only speeds us up for a very short period of
Line 33: time—maybe a couple of days or so. Invariably, we’ll hit ugly defects requiring
Line 34: long debugging sessions. Maybe the worst of it is that we’ll create chunks of
Line 35: legacy code that’ll cost us forever. Sorry Joe, tossing unit tests isn’t worth it.”
Line 36: Not much will allow you to escape last-minute crunches unscathed, no matter
Line 37: how good you are at development. Once you’re there, all you can do is nego-
Line 38: tiate or work excessive hours. But if you insist on quality controls from day
Line 39: one, it won’t happen nearly as often.
Line 40: Unit testing is a part of those quality controls. Let’s look at how to ensure
Line 41: that it becomes a habit within your team.
Line 42: Getting on the Same Page with Your Team
Line 43: Approaches to unit testing can vary dramatically from developer to developer.
Line 44: Some insist on TDD. Others resist unit testing at all costs, producing only
Line 45: tests they feel forced to write. Some prefer lumping multiple cases into a
Line 46: single test method. Some favor slower integration tests. Some will disagree
Line 47: with other recommendations you’ve learned from this book.
Line 48: Your team must get on the same page, whether it’s regarding unit testing
Line 49: standards or how you review code in the first place. Long debates or continual
Line 50: back-and-forth without resolution are wastes of everyone’s time. You’ll never
Line 51: agree on everything, but you can quickly discover what you do agree on and
Line 52: increase consensus over time.
Line 53: Your team can establish initial working agreements as part of team char-
Line 54: tering activities. Liftoff [LN17] is a great guide for facilitating effective
Line 55: chartering sessions.
Line 56: Establishing Standards
Line 57: You’ll want to derive some standards around unit testing. Start minimally.
Line 58: Answer two questions:
Line 59: • What code (and test) related elements are wasting our time?
Line 60: • What simple standards can we quickly agree on?
Line 61: Run a sub-hour discussion that results in a short list of standards, or better,
Line 62: in a code example that clearly embodies the standards. Over time, ensure
Line 63: that standards stay relevant and followed. Reference them when violated,
Line 64: review them when disagreement arises, and revise them as needed.
Line 65: Chapter 12. Adopting Team Practices • 236
Line 66: report erratum  •  discuss
Line 67: 
Line 68: --- 페이지 250 ---
Line 69: Here’s a short, incomplete list of unit test practices to standardize on:
Line 70: • Which tests developers should run prior to check-in
Line 71: • How to name test classes and test methods
Line 72: • Whether to use JUnit’s assertions or an assertion library like AssertJ
Line 73: • Whether to use AAA or not
Line 74: • Which mock tool to prefer
Line 75: • Whether to prohibit console output on test runs (please do)
Line 76: • How to identify and discourage slow tests in the unit test suite
Line 77: Your team should quickly adopt and adhere to most of these standards. Some
Line 78: will require continual vigilance, such as eliminating all console output from
Line 79: a test run. You might be able to automate solutions to ensure people comply;
Line 80: otherwise, you might find yourself continually pestering folks. You might also
Line 81: find that some standards just aren’t worth the effort.
Line 82: Increasing Quality with Post Facto Reviews
Line 83: To ensure everyone adheres to standards, your team must exert collective
Line 84: peer pressure through some form of code review. Your team’s investment in
Line 85: code and unit tests is too expensive to allow individuals to do anything they
Line 86: want to the codebase.
Line 87: Many teams require pull requests (PRs)—a feature most closely associated
Line 88: with GitHub. A developer submits a pull request for a chunk of work deemed
Line 89: ready for integration into the main branch. GitHub notifies the rest of the
Line 90: team, who reviews and comments on changes made. Reviewers approve a
Line 91: request by pulling (merging) it into the main branch.
Line 92: The PR process has become a preferred standard in many organizations.
Line 93: While it appears efficient, the PR process is the least effective of the review
Line 94: mechanisms. That’s because it is the least agile—it attempts to streamline
Line 95: reviews by minimizing face-to-face human interaction.
Line 96: 1
Line 97: You might initiate review sessions where unit test producers solicit feedback
Line 98: from others on the team. Such post facto reviews can range from informal
Line 99: code walkthroughs to fairly formal processes like Fagan inspections, which
Line 100: are designed to streamline and standardize the review.
Line 101: 2
Line 102: When using Fagan inspections, the person creating the document—the thing
Line 103: to be reviewed (usually code)—is responsible for soliciting reviewers, much
Line 104: as when doing PRs. A meeting is typically held a couple of days later, which
Line 105: 1.
Line 106: https://medium.com/pragmatic-programmers/prs-shift-left-please-part-one-b0f8bb79ef2b
Line 107: 2.
Line 108: http://en.wikipedia.org/wiki/Fagan_inspection
Line 109: report erratum  •  discuss
Line 110: Getting on the Same Page with Your Team • 237
Line 111: 
Line 112: --- 페이지 251 ---
Line 113: allows time for reviewers to take a look at the changes. Prior to the meeting,
Line 114: reviewers make note of defects and categorize them based on severity.
Line 115: The inspection meeting is designed to go fast. Only the most severe problems
Line 116: are described, and discussions are constrained to clarifications only.
Line 117: Expressly prohibited during the meeting is “solutioning” any problem.
Line 118: The document producer takes away the list of all problems (including ones
Line 119: that aren’t severe) and fixes them as appropriate. A follow-up meeting to dis-
Line 120: cuss the resolution can be held if needed.
Line 121: Fagan inspections seem similar to PRs in that both are designed to be
Line 122: streamlined. But they also involve face-to-face communication, which can
Line 123: help eliminate misunderstandings. The opportunity to interact also helps a
Line 124: team refine what’s truly important to focus on when doing reviews.
Line 125: The PR process, Fagan inspections, and things like code walkthroughs are
Line 126: all post facto—they occur after the code in question was produced. For that
Line 127: reason, they all suffer from a few challenges.
Line 128: First, reviewers aren’t usually familiar with the intimate details of the code
Line 129: product being reviewed. The best reviews—the ones that find problems before
Line 130: you ship them—come from people with a deep understanding of the code.
Line 131: The reality in most shops prevents this sort of time investment on the part
Line 132: of the reviewers—they’re too busy working on their own thing.
Line 133: As a result, post facto reviews find fewer defects than we’d like. Reviewers can
Line 134: discover many surface-level defects and style violations. But they often miss
Line 135: deeper-seated defects related to things you might only think of when you
Line 136: are deeply immersed in the challenge at hand. Such problems are often
Line 137: harder to fix after the fact, as they can be deeply intertwined with the existing
Line 138: solution.
Line 139: Second, if there are serious problems, after-the-fact reviews come too late.
Line 140: Once the code is built and seemingly ready, teams are usually under too
Line 141: much pressure to ship it—by their peers, managers, and even themselves.
Line 142: They’re not about to step back and significantly rework code that’s purport-
Line 143: edly already working. As a result, the team takes on problematic software
Line 144: that will cost them even more to maintain down the road.
Line 145: In short, post facto reviews are too late and probably barely worth the time
Line 146: investment they require. Put another way, doing the work, reviewing it,
Line 147: reworking it, and re-reviewing it is an inefficient process.
Line 148: Chapter 12. Adopting Team Practices • 238
Line 149: report erratum  •  discuss
Line 150: 
Line 151: --- 페이지 252 ---
Line 152: Active Review via Pair Programming
Line 153: A good review process would let a team review and reject a poor design before
Line 154: anyone tries to implement it. In the 1990s, much of software development
Line 155: was driven with design-up-front processes. A team typically invested 30 per-
Line 156: cent or more of a project producing speculative designs. Development work
Line 157: did not start until these designs were complete. The designs, based on
Line 158: exhaustively detailed requirements, were captured as heavy documents with
Line 159: copious diagrams and models. It worked…for a small number of situations.
Line 160: Heavy up-front design doesn’t work for most of us because it holds up poorly
Line 161: to that ever-present thing called change. Also, no matter the amount of up-
Line 162: front investment, speculative designs are often inadequate or flat-out wrong.
Line 163: The intent of pair programming, or pairing, is to increase quality. To pair, two
Line 164: programmers work together side-by-side (or face-to-face remotely) to develop
Line 165: a two-heads-are-better-than-one solution. Pairing is an active form of
Line 166: review—its participants review each other’s ideas and code as they code and
Line 167: fix any problems before moving on. Pair members help each other adhere to
Line 168: standards and practices like unit testing.
Line 169: Few practices have drawn as much controversy in the software development
Line 170: world, however. The thought of working with other developers closely
Line 171: throughout the day sends many screaming for the exits. Even when practiced
Line 172: well, pairing incurs a number of overhead costs. It’s also still possible for a
Line 173: pair to produce a solution that the rest of the team finds problematic.
Line 174: Don’t dismiss pairing out of hand, however. When done well, even active resisters
Line 175: can become converts, perhaps due to the increase in quality. Some find its
Line 176: highly interactive, collaborative aspect gratifying. The PragPub article “Pair
Line 177: Programming Benefits”
Line 178: 3 describes some potentials for its ROI. Another article,
Line 179: “Pair Programming in a Flash,”
Line 180: 4 lays out ground rules for successful pairing
Line 181: and points out a few pitfalls to avoid.
Line 182: Pair swapping can be valuable. Before a task is considered complete, a new
Line 183: person replaces one of the starting pair’s developers. This third party provides
Line 184: the perspective of someone not intimately involved in creating the current
Line 185: solution. They can help correct clarity and other issues not seen by the original
Line 186: pair. Recognize that to some extent, though, the process has reverted to work-
Line 187: review-rework—the new party is identifying and helping fix problems that
Line 188: might not have existed had they arrived sooner.
Line 189: 3.
Line 190: https://langrsoft.com/ftp/pragpub-2011-07.pdf
Line 191: 4.
Line 192: https://langrsoft.com/ftp/pragpub-2011-06.pdf
Line 193: report erratum  •  discuss
Line 194: Getting on the Same Page with Your Team • 239
Line 195: 
Line 196: --- 페이지 253 ---
Line 197: Active Review via Mob Programming
Line 198: Maybe the answer is to have the whole team actively review everything related
Line 199: to delivering a feature—the design, tests, code, and anything else required—as
Line 200: that same team builds it all. This is the idea behind the nearly 15-year-old
Line 201: practice known as mob programming or ensemble programming.
Line 202: While its name might suggest chaos, proper mob programming requires the
Line 203: team to work together in a structured manner in the same virtual or physical
Line 204: space. It’s not “throw everyone in a room and see what happens.”
Line 205: When mob programming, one person acts as a driver whose job is to listen
Line 206: to the rest of the mob—the navigators—and translate their direction into code.
Line 207: Physically and in person, this means that the driver is the only one typing at
Line 208: a keyboard; the rest of the mob watches on a shared monitor.
Line 209: After a short period of time— maybe a handful of minutes—the driver yields
Line 210: control to another mob member. A driver with a brilliant idea must relinquish
Line 211: their seat to step the next driver through their thinking.
Line 212: These two simple rules maximize engagement and minimize domination and
Line 213: fear. Without structure, a mob usually devolves. A senior team member speeds
Line 214: off to their desired solution while the rest of the team watches confused and
Line 215: helpless from the back seat. But with short rotations and a driver who must
Line 216: follow direction, it becomes difficult for anyone to dominate.
Line 217: The driver role is a short-lived experience, which can make it less intimidating,
Line 218: as can the fact that they’re not responsible for knowing what to do. A good
Line 219: driver ramps up their listening and translating skills. They might start
Line 220: knowing nothing about a language, requiring detailed direction on its syntax
Line 221: (“type public static void main, then parentheses, then String[])”). It’s rough at first,
Line 222: but most drivers quickly improve to the point where they can readily translate
Line 223: higher-level instruction (“write a method that filters the customer list down
Line 224: to active customers only”) into code.
Line 225: Mob programming seems to send fewer folks screaming for the exits than
Line 226: pairing. That’s possibly because pairing demands continual attention and
Line 227: forces considerable intimacy between you and each of your teammates. Some
Line 228: pairs will just never click. In a mob, you’re not “on point” for the entire
Line 229: development session, unlike when you’re working in a pair.
Line 230: Mob sessions can be highly effective. Mob programming eliminates a lot of
Line 231: the cost of splitting the work amongst sub-teams, whether they are pairs or
Line 232: individuals. Not only can you eliminate review sessions (everyone’s there!),
Line 233: but ceremonies like standup meetings, iteration planning, and pull requests
Line 234: Chapter 12. Adopting Team Practices • 240
Line 235: report erratum  •  discuss
Line 236: 
Line 237: --- 페이지 254 ---
Line 238: disappear or are greatly simplified. Since everyone is in the room, you find
Line 239: the problems sooner, you derive a better design that everyone can live with,
Line 240: you converge on a team coding standard, you have all the expertise available
Line 241: to use right now, and you write all the tests you need to write.
Line 242: Most importantly (to me at least), mob sessions are usually a lot of fun, and
Line 243: I often feel like we got a lot more done.
Line 244: If you choose to practice either mob or pair programming, you’ll still end up
Line 245: with some individual work product. Make sure you use a post facto review
Line 246: process for this work.
Line 247: Practicing Continuous Integration
Line 248: “It works on my machine!” cries Joe. “Must be something wrong on yours,”
Line 249: he says to Lucia.
Line 250: Hearken to the call of the wild developer, heard ofttimes in olde shops that
Line 251: weren’t practicing continuous integration (CI). With CI, all developers frequently
Line 252: integrate their changes with the centralized repository (commonly in GitHub).
Line 253: A tool known as a CI server monitors the repository. When the repository is
Line 254: updated, the CI server triggers a new build and runs one or more sets of tests
Line 255: prior to completion. The first of those test suites to execute is typically your
Line 256: team’s unit tests.
Line 257: CI demands a solid suite of fast unit tests.
Line 258: CI servers can be hosted internally or available in the cloud. The most common
Line 259: tools are Jenkins, GitHub Actions, and GitLab CI. Some alternative solutions
Line 260: include Azure DevOps, CircleCI, and TeamCity.
Line 261: 5 Some of the tools are free,
Line 262: some are licensed, and some are software as a service (SaaS).
Line 263: The CI build’s tests verify that the integrated codebase works as expected. If
Line 264: a developer pushes and any CI tests fail, the build fails and the team is notified
Line 265: of the problem. The unit tests running in CI thus establish a centralized,
Line 266: authoritative standard.
Line 267: Broken CI tests indicate a system that cannot be deployed. Resolve
Line 268: them before doing anything else.
Line 269: 5.
Line 270: https://blog.jetbrains.com/teamcity/2023/07/best-ci-tools/
Line 271: report erratum  •  discuss
Line 272: Practicing Continuous Integration • 241
Line 273: 
Line 274: --- 페이지 255 ---
Line 275: Tools like Git can be configured to abort commit/push attempts
Line 276: when unit tests fail locally.
Line 277: CI is a foundation for practicing continuous deployment (CD), wherein each
Line 278: successful build triggers a deployment to production. Amazon
Line 279: 6 and Netflix
Line 280: 7
Line 281: are companies that deploy to production thousands of times daily using CD.
Line 282: Conflicts and Merges
Line 283: If two or more separate developers separately make changes to the same
Line 284: codebase, it’s possible for their combined changes to break the system (even
Line 285: though the individual contributions worked prior to integration). In order for
Line 286: CI to work, each developer wishing to push must first pull the latest code
Line 287: from the central repository. They run their fantastic unit test suite to ensure
Line 288: nothing is broken and then push up what now becomes the latest version of
Line 289: the system. If they don’t have a fantastic unit test suite, they must carefully
Line 290: review the combined code first. (Corollary: folks without a fantastic unit test
Line 291: suite or some other comprehensive test suite are not usually practicing CI.)
Line 292: A healthy team that’s created a trustworthy test suite integrates frequently.
Line 293: Some teams who practice TDD push up every TDD cycle, in other words, as often
Line 294: as every few minutes. Once they get a new behavior working and clean up the
Line 295: code, they integrate that new increment. This “continuous” aspect of CI helps
Line 296: make it work and be successful. Feedback comes sooner and in smaller incre-
Line 297: ments. It’s easier and faster to find and fix problems in such small increments.
Line 298: In contrast, developers on less advanced teams defer integrating their changes
Line 299: until a feature is complete. They typically make their changes on code
Line 300: branches across the course of a day, a few days, and sometimes a few weeks.
Line 301: The amount of new code that must subsequently be integrated can be consid-
Line 302: erable, thus significantly likely to conflict with existing code.
Line 303: Developers can spend hours, even days, managing a meticulous manual
Line 304: merge process to integrate a long-lived branch. The correct technical term for
Line 305: such a nightmare is “merge hell.” The duration of the nightmare often
Line 306: increases proportionally with the age of the branch.
Line 307: Better communication and division of labor can help minimize code conflicts
Line 308: and merge hell. But consider also mob programming (see Active Review via
Line 309: Mob Programming, on page 240).
Line 310: 6.
Line 311: https://www.zdnet.com/article/how-amazon-handles-a-new-software-deployment-every-second/
Line 312: 7.
Line 313: https://www.theserverside.com/feature/How-Netflix-built-tooling-for-multi-cloud-deployment
Line 314: Chapter 12. Adopting Team Practices • 242
Line 315: report erratum  •  discuss
Line 316: 
Line 317: --- 페이지 256 ---
Line 318: An Integration Process Checklist
Line 319: Here’s a summary of your steps as a developer for practicing continuous
Line 320: integration:
Line 321: 1.
Line 322: Pull from your central repo to get your local codebase up to date.
Line 323: 2.
Line 324: Change the code, running unit tests as you go.
Line 325: 3.
Line 326: Pull from the repo to integrate any new changes from teammates.
Line 327: 4.
Line 328: Manually review the incoming changes as appropriate.
Line 329: 5.
Line 330: Run your tests to ensure that the integrated code works.
Line 331: 6.
Line 332: Push your changes to the central repository.
Line 333: Don’t advance to the next step if any of your tests are failing.
Line 334: A CI process fosters healthy peer pressure against costly code. Developers
Line 335: quickly habituate themselves to running their unit tests before check-in so
Line 336: as not to waste their teammates’ time by causing the CI build process to fail.
Line 337: A CI server is a minimum for building a modern development team.
Line 338: Summary
Line 339: You and your team must be on the same page when it comes to unit testing.
Line 340: If it’s new to your team, it’ll take time to adopt and ingrain as a beneficial
Line 341: habit. If it’s an existing practice, your team practices might need improvement.
Line 342: In this chapter, you learned about establishing team-level standards for unit
Line 343: testing from both implementation and process perspectives. You also learned
Line 344: about the active review mechanisms that help ensure test quality—specifically,
Line 345: mob and pair programming. Finally, you discovered the key role that CI plays
Line 346: in unit testing.
Line 347: Last up: times are changing rapidly. AI has dramatically made its way into
Line 348: the software development arena. Unlike previous attempts (anyone remember
Line 349: Prolog and 4GLs?), AI has made a ubiquitous impact not just in software
Line 350: development but in day-to-day life for many of us. AI’s improvements are
Line 351: accelerating and there’s little chance of its disappearance.
Line 352: Yes, unit testing is quite relevant in the age of AI. Read on to discover how.
Line 353: report erratum  •  discuss
Line 354: Summary • 243
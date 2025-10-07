Line 1: 
Line 2: --- 페이지 241 ---
Line 3: 213
Line 4: Integrating unit testing
Line 5: into the organization
Line 6: As a consultant, I’ve helped several companies, big and small, integrate continuous
Line 7: delivery processes and various engineering practices, such as test-driven develop-
Line 8: ment and unit testing, into their organizational culture. Sometimes this has failed,
Line 9: but those companies that succeeded had several things in common. In any type of
Line 10: organization, changing people’s habits is more psychological than technical. Peo-
Line 11: ple don’t like change, and change is usually accompanied with plenty of FUD (fear,
Line 12: uncertainty, and doubt) to go around. It won’t be a walk in the park for most peo-
Line 13: ple, as you’ll see in this chapter.
Line 14: 11.1
Line 15: Steps to becoming an agent of change
Line 16: If you’re going to be the agent of change in your organization, you should first
Line 17: accept that role. People will view you as the person responsible (and sometimes
Line 18: This chapter covers
Line 19: Becoming an agent of change
Line 20: Implementing change from the top down or from 
Line 21: the bottom up
Line 22: Preparing to answer the tough questions about 
Line 23: unit testing
Line 24: 
Line 25: --- 페이지 242 ---
Line 26: 214
Line 27: CHAPTER 11
Line 28: Integrating unit testing into the organization
Line 29: accountable) for what’s happening, whether or not you want them to, and there’s no
Line 30: use in hiding. In fact, hiding can cause things to go terribly wrong.
Line 31:  As you start to implement or push for changes, people will start asking tough ques-
Line 32: tions related to what they care about. How much time will this “waste”? What does this
Line 33: mean for me as a QA engineer? How do we know it works? Be prepared to answer. The
Line 34: answers to the most common questions are discussed in section 11.5. You’ll find that
Line 35: convincing others inside the organization before you start making changes will help
Line 36: you immensely when you need to make tough decisions and answer those questions.
Line 37:  Finally, someone will have to stay at the helm, making sure the changes don’t die
Line 38: for lack of momentum. That’s you. There are ways to keep things alive, as you’ll see in
Line 39: the next sections.
Line 40: 11.1.1 Be prepared for the tough questions
Line 41: Do your research. Read the questions and answers at the end of this chapter, and look
Line 42: at the related resources. Read forums, mailing lists, and blogs, and consult with your
Line 43: peers. If you can answer your own tough questions, there’s a good chance you can
Line 44: answer someone else’s.
Line 45: 11.1.2 Convince insiders: Champions and blockers
Line 46: Few things make you feel as lonely in an organization as the decision to go against the
Line 47: current. If you’re the only one who thinks what you’re doing is a good idea, there’s lit-
Line 48: tle reason for anyone to make an effort to implement what you’re advocating. Con-
Line 49: sider who can help and hurt your efforts: the champions and blockers.
Line 50: CHAMPIONS
Line 51: As you start pushing for change, identify the people you think are most likely to help
Line 52: in your quest. They’ll be your champions. They’re usually early adopters, or people who
Line 53: are open minded enough to try the things you’re advocating. They may already be
Line 54: half convinced but are looking for an impetus to start the change. They may have even
Line 55: tried it and failed on their own.
Line 56:  Approach them before anyone else and ask for their opinions on what you’re
Line 57: about to do. They may tell you some things that you hadn’t considered, including 
Line 58: Teams that might be good candidates to start with 
Line 59: Places where people are more accepting of such changes 
Line 60: What (and who) to watch out for in your quest
Line 61: By approaching them, you’re helping to ensure that they’re part of the process. Peo-
Line 62: ple who feel part of the process usually try to help make it work. Make them your
Line 63: champions: ask them if they can help you and be the ones people can come to with
Line 64: questions. Prepare them for such events.
Line 65: BLOCKERS
Line 66: Next, identify the blockers. These are the people in the organization who are most
Line 67: likely to resist the changes you’re making. For example, a manager might object to
Line 68: 
Line 69: --- 페이지 243 ---
Line 70: 215
Line 71: 11.1
Line 72: Steps to becoming an agent of change
Line 73: adding unit tests, claiming that they’ll add too much time to the development effort
Line 74: and increase the amount of code that needs to be maintained. Make them part of the
Line 75: process instead of resisters of it by giving them (at least those who are willing and
Line 76: able) an active role in the process.
Line 77:  The reasons why people might resist changes vary. Answers to some of the possible
Line 78: objections are covered in section 11.4 on influence forces. Some will be worried about
Line 79: job security, and some will just feel too comfortable with the way things currently are.
Line 80: Approaching potential blockers and detailing all the things they could have done bet-
Line 81: ter is often not constructive, as I’ve found out the hard way. People don’t like to be
Line 82: told that their baby is ugly. 
Line 83:  Instead, ask blockers to help you in the process by being in charge of defining cod-
Line 84: ing standards for unit tests, for example, or by doing code and test reviews with peers
Line 85: every other day. Or make them part of the team that chooses the course materials or
Line 86: outside consultants. You’ll give them a new responsibility that will help them feel
Line 87: relied on and relevant in the organization. They need to be part of the change or
Line 88: they’ll almost certainly undermine it.
Line 89: 11.1.3 Identify possible starting points
Line 90: Identify where in the organization you can start implementing changes. Most success-
Line 91: ful implementations take a steady route. Start with a pilot project in a small team, and
Line 92: see what happens. If all goes well, move on to other teams and other projects.
Line 93:  Here are some tips that will help you along the way:
Line 94: Choose smaller teams.
Line 95: Create subteams.
Line 96: Consider project feasibility.
Line 97: Use code and test reviews as teaching tools.
Line 98: These tips can take you a long way in a mostly hostile environment.
Line 99: CHOOSE SMALLER TEAMS
Line 100: Identifying possible teams to start with is usually easy. You’ll generally want a small
Line 101: team working on a low-profile project with low risks. If the risk is minimal, it’s easier to
Line 102: convince people to try your proposed changes. 
Line 103:  One caveat is that the team needs to have members who are open to changing the
Line 104: way they work and to learning new skills. Ironically, the people with less experience on
Line 105: a team are usually most likely to be open to change, and people with more experience
Line 106: tend to be more entrenched in their way of doing things. If you can find a team with
Line 107: an experienced leader who’s open to change, but that also includes less-experienced
Line 108: developers, it’s likely that team will offer little resistance. Go to the team and ask their
Line 109: opinion on holding a pilot project. They’ll tell you if this is (or is not) the right place
Line 110: to start.
Line 111: 
Line 112: --- 페이지 244 ---
Line 113: 216
Line 114: CHAPTER 11
Line 115: Integrating unit testing into the organization
Line 116: CREATE SUBTEAMS
Line 117: Another possible candidate for a pilot test is to form a subteam within an existing
Line 118: team. Almost every team will have a “black hole” component that needs to be main-
Line 119: tained, and while it does many things right, it also has many bugs. Adding features for
Line 120: such a component is a tough task, and this kind of pain can drive people to experi-
Line 121: ment with a pilot project. 
Line 122: CONSIDER PROJECT FEASIBILITY
Line 123: For a pilot project, make sure you’re not biting off more than you can chew. It takes
Line 124: more experience to run more difficult projects, so you might want to have at least
Line 125: two options—a complicated project and an easier project—so that you can choose
Line 126: between them.
Line 127: USE CODE AND TEST REVIEWS AS TEACHING TOOLS
Line 128: If you’re the technical lead on a small team (up to eight people), one of the best ways
Line 129: of teaching is instituting code reviews that also include test reviews. The idea is that as
Line 130: you review other people’s code and tests, you teach them what you look for in the tests
Line 131: and your way of thinking about writing tests or approaching TDD. Here are some tips:
Line 132: Do the reviews in person, not through remote software. The personal connec-
Line 133: tion lets much more information pass between you in nonverbal ways, so learn-
Line 134: ing happens better and faster.
Line 135: In the first couple of weeks, review every line of code that gets checked in. This
Line 136: will help you avoid the “we didn’t think this code needs reviewing” problem. 
Line 137: Add a third person to your code reviews—one who will sit on the side and learn
Line 138: how you review the code. This will allow them to later do code reviews them-
Line 139: selves and teach others, so that you won’t become a bottleneck for the team as
Line 140: the only person capable of doing reviews. The idea is to develop others’ ability
Line 141: to do code reviews and accept more responsibility.
Line 142: If you want to learn more about this technique, I wrote about it in my blog for techni-
Line 143: cal leaders: “What Should a Good Code Review Look and Feel Like?” at https://5whys
Line 144: .com/blog/what-should-a-good-code-review-look-and-feel-like.html.
Line 145: 11.2
Line 146: Ways to succeed
Line 147: There are two main ways an organization or team can start changing a process: from
Line 148: the bottom-up or the top-down (and sometimes both). The two ways are very differ-
Line 149: ent, as you’ll see, and either could be the right approach for your team or company.
Line 150: There’s no one right way.
Line 151:  As you proceed, you’ll need to learn how to convince management that your efforts
Line 152: should also be their efforts, or when it would be wise to bring in someone from outside
Line 153: to help. Making progress visible is important, as is setting clear goals that can be mea-
Line 154: sured. Identifying and avoiding obstacles should also be high on your list. There are
Line 155: many battles that can be fought, and you need to choose the right ones.
Line 156: 
Line 157: --- 페이지 245 ---
Line 158: 217
Line 159: 11.2
Line 160: Ways to succeed
Line 161: 11.2.1 Guerrilla implementation (bottom-up)
Line 162: Guerrilla-style implementation is all about starting out with a team, getting results,
Line 163: and only then convincing other people that the practices are worthwhile. Usually the
Line 164: driver for guerrilla implementation is a team who’s tired of doing things the pre-
Line 165: scribed way. They set out to do things differently; they study on their own and make
Line 166: changes happen. When the team shows results, other people in the organization may
Line 167: decide to start implementing similar changes in their own teams.
Line 168:  In some cases, guerrilla-style implementation is a process adopted first by develop-
Line 169: ers and then by management. At other times, it’s a process advocated for first by devel-
Line 170: opers and then by management. The difference is that you can accomplish the first
Line 171: covertly, without the higher powers knowing about it. The latter is done in conjunc-
Line 172: tion with management. It’s up to you to figure out which approach will work better.
Line 173: Sometimes the only way to change things is by covert operations. Avoid this if you can,
Line 174: but if there’s no other way, and you’re sure the change is needed, you can just do it.
Line 175:  Don’t take this as a recommendation to make a career-limiting move. Developers
Line 176: do things without permission all the time: debugging code, reading email, writing
Line 177: code comments, creating flow diagrams, and so on. These are all tasks that developers
Line 178: do as a regular part of the job. The same goes for unit testing. Most developers already
Line 179: write tests of some sort (automated or not). The idea is to redirect the time spent on
Line 180: tests into something that will provide benefits in the long term.
Line 181: 11.2.2 Convincing management (top-down)
Line 182: The top-down move usually starts in one of two ways. A manager or a developer will
Line 183: initiate the process and start the rest of the organization moving in that direction,
Line 184: piece by piece. Or a mid-level manager may see a presentation, read a book (such as
Line 185: this one), or talk to a colleague about the benefits of specific changes to the way they
Line 186: work. Such a manager will usually initiate the process by giving a presentation to peo-
Line 187: ple in other teams or even using their authority to make the change happen.
Line 188: 11.2.3 Experiments as door openers
Line 189: Here’s a powerful way to get started with unit testing in a large organization (it could
Line 190: also fit other types of transformation or new skills). Declare an experiment that will
Line 191: last two to three months. It will apply to only one pre-picked team and relate to only
Line 192: one or two components in a real application. Make sure it’s not too risky. If it fails, the
Line 193: company won’t go under or lose a major client. It also shouldn’t be useless: the exper-
Line 194: iment must provide real value and not just serve as a playground. It has to be some-
Line 195: thing you’ll end up pushing into your codebase and use in production eventually; it
Line 196: shouldn’t be a write-and-forget piece of code.
Line 197:  The word “experiment” conveys that the change is temporary, and if it doesn’t
Line 198: work out, the team can go back to the way they were before. Also, the effort is time-
Line 199: boxed, so we know when the experiment is finished.
Line 200: 
Line 201: --- 페이지 246 ---
Line 202: 218
Line 203: CHAPTER 11
Line 204: Integrating unit testing into the organization
Line 205:  Such an approach helps people feel more at ease with big changes, because it
Line 206: reduces the risk to the organization, the number of people affected (and thus the
Line 207: number of people objecting), and the number of objections relating to fear of chang-
Line 208: ing things “forever.” 
Line 209:  Here’s another hint: when faced with multiple options for an experiment, or if you
Line 210: get objections pushing for another way of working, ask, “Which idea do we want to
Line 211: experiment with first?”
Line 212: WALK THE WALK
Line 213: Be prepared that your idea might not be selected from among all the options for an
Line 214: experiment. When push comes to shove, you have to hold experiments based on what
Line 215: the consensus of leadership decides, whether you like it or not.
Line 216:  The nice thing about going with other people’s experiments is that, like with
Line 217: yours, they are time-boxed and temporary! The best outcome might be that another
Line 218: approach fixes what you were trying to fix, and you might want to keep someone else’s
Line 219: experiment going. However, if you hate the experiment, just remember that it’s tem-
Line 220: porary, and you can push for the next experiment.
Line 221: METRICS AND EXPERIMENTS
Line 222: Be sure to record a baseline set of metrics before and after the experiment. These
Line 223: metrics should be related to things you’re trying to change, such as eliminating wait-
Line 224: ing times for a build, reducing the lead time for a product to go out the door, or
Line 225: reducing the number of bugs found in production.
Line 226:  To dive deeper into the various metrics you might use, take a look at my talk “Lies,
Line 227: Damned Lies, and Metrics,” which you can find in my blog at https://pipelinedriven
Line 228: .org/article/video-lies-damned-lies-and-metrics. 
Line 229: 11.2.4 Get an outside champion
Line 230: I highly recommend getting an outside person to help with the change. An outside
Line 231: consultant coming in to help with unit testing and related matters has advantages over
Line 232: someone who works in the company: 
Line 233: Freedom to speak—A consultant can say things that people inside the company
Line 234: may not be willing to hear from someone who works there (“The code integrity
Line 235: is bad,” “Your tests are unreadable,” and so on). 
Line 236: Experience—A consultant will have more experience dealing with resistance
Line 237: from the inside, coming up with good answers to tough questions, and knowing
Line 238: which buttons to push to get things going. 
Line 239: Dedicated time—For a consultant, this is their job. Unlike other employees in the
Line 240: company who have better things to do than push for change (like writing soft-
Line 241: ware), the consultant does this full time and is dedicated to this purpose. 
Line 242: I’ve often seen a change break down because an overworked champion doesn’t have
Line 243: the time to dedicate to the process.
Line 244: 
Line 245: --- 페이지 247 ---
Line 246: 219
Line 247: 11.2
Line 248: Ways to succeed
Line 249: 11.2.5 Make progress visible
Line 250: It’s important to keep the progress and status of the change visible. Hang white-
Line 251: boards or posters on walls in corridors or in the food-related areas where people
Line 252: congregate. The data displayed should be related to the goals you’re trying to achieve.
Line 253: For example:
Line 254: Show the number of passing or failing tests in the last nightly build. 
Line 255: Keep a chart showing which teams are already running an automated build
Line 256: process. 
Line 257: Put up a Scrum burndown chart of iteration progress or a test-code-coverage
Line 258: report (as shown in figure 11.1) if that’s what you have your goals set to. (You
Line 259: can learn more about Scrum at www.controlchaos.com.) 
Line 260: Put up contact details for yourself and all the champions, so someone can
Line 261: answer any questions that arise. 
Line 262: Figure 11.1
Line 263: An example of a test-code-coverage report in TeamCity with NCover
Line 264: 
Line 265: --- 페이지 248 ---
Line 266: 220
Line 267: CHAPTER 11
Line 268: Integrating unit testing into the organization
Line 269: Set up a big-screen display that’s always showing, in big bold graphics, the status
Line 270: of the builds, what’s currently running, and what’s failing. Put that in a visible
Line 271: place where all developers can see—in a well-trafficked corridor, for example,
Line 272: or at the top of the team room’s main wall.
Line 273: Your aim in using these charts is to connect with two groups: 
Line 274: The group undergoing the change—People in this group will gain a greater feeling
Line 275: of accomplishment and pride as the charts (which are open to everyone) are
Line 276: updated, and they’ll feel more compelled to complete the process because it’s
Line 277: visible to others. They’ll also be able to keep track of how they’re doing com-
Line 278: pared to other groups. They may push harder, knowing that another group
Line 279: implemented specific practices more quickly.
Line 280: Those in the organization who aren’t part of the process—You’re raising interest and
Line 281: curiosity among these people, triggering conversations and buzz, and creating a
Line 282: current that they can join if they choose.
Line 283: 11.2.6 Aim for specific goals, metrics, and KPIs
Line 284: Without goals, the change will be hard to measure and to communicate to others. It
Line 285: will be a vague “something” that can easily be shut down at the first sign of trouble.
Line 286: LAGGING INDICATORS
Line 287: At the organizational level, unit tests are generally part of a bigger set of goals, usually
Line 288: related to continuous delivery. If that’s the case for you, I highly recommend using the
Line 289: four common DevOps metrics:
Line 290: Deployment frequency—How often an organization successfully releases to pro-
Line 291: duction.
Line 292: Lead time for changes—The time it takes a feature request to get into production.
Line 293: Note that many places incorrectly publish this as the amount of time it takes a
Line 294: commit to get into production, which is only a part of the journey that a feature
Line 295: goes through, from an organizational standpoint. If you’re measuring from
Line 296: commit time, you’re closer to measuring the “cycle time” of a feature from com-
Line 297: mit up to a specific point. Lead time is made up of multiple cycle times. 
Line 298: Escaped bugs/change failure rate—The number of failures found in production
Line 299: per some unit, usually release, deployment, or time. You can also use the per-
Line 300: centage of deployments causing a failure in production.
Line 301: Time to restore service—How long it takes an organization to recover from a fail-
Line 302: ure in production.
Line 303: These four are what we’d call lagging indicators, and they’re very hard to fake (although
Line 304: they’re pretty easy to measure in most places). They are great in making sure we do
Line 305: not lie to ourselves about the results of experiments.
Line 306: 
Line 307: --- 페이지 249 ---
Line 308: 221
Line 309: 11.2
Line 310: Ways to succeed
Line 311: LEADING INDICATORS
Line 312: Often we’d like faster feedback to ensure that we’re going the right way. That’s where
Line 313: leading indicators come in. Leading indicators are things we can control on a day-to-day
Line 314: basis—code coverage, number of tests, build run time, and more. They are easier to
Line 315: fake, but combined with lagging indicators, they can often provide us with early signs
Line 316: that we might be going the right way.
Line 317:  Figure 11.2 shows a sample structure and ideas for lagging and leading indicators
Line 318: you can use in your organization. You can find a high-resolution image with color at
Line 319: https://pipelinedriven.org/article/a-metrics-framework-for-continuous-delivery.
Line 320: INDICATOR CATEGORIES AND GROUPS
Line 321: I usually break up leading indicators into two groups:
Line 322: Team level—Metrics that an individual team can control
Line 323: Engineering management level—Metrics that require cross-team collaboration or
Line 324: aggregate metrics across multiple teams
Line 325: I also like to categorize them based on what they will be used to solve:
Line 326: Progress—Used to solve visibility and decision making on the plan
Line 327: Bottlenecks and feedback—As the name implies
Line 328: Quality—Escaped bugs in production
Line 329: Figure 11.2
Line 330: An example of a metrics framework for use in continuous delivery
Line 331: 
Line 332: --- 페이지 250 ---
Line 333: 222
Line 334: CHAPTER 11
Line 335: Integrating unit testing into the organization
Line 336: Skills—Track that we are slowly removing knowledge barriers inside teams or
Line 337: across teams
Line 338: Learning—Acting like we’re a learning organization
Line 339: QUALITATIVE METRICS
Line 340: The metrics are mostly quantitative (i.e., they are numbers that can be measured), but
Line 341: a few are qualitative, in that you ask people how they feel or think about something.
Line 342: The ones I use are
Line 343: How confident you are that the tests can and will find bugs in the code if they
Line 344: arise (from 1 to 5)? Take the average of the responses from the team members
Line 345: or across multiple teams.
Line 346: Does the code do what it is supposed to do (from 1 to 5)?
Line 347: These are surveys you can ask at each retrospective meeting, and they take five min-
Line 348: utes to answer. 
Line 349: TREND LINES ARE YOUR FRIEND
Line 350: For all leading and lagging indicators, you want to see trend lines, not just snapshots of
Line 351: numbers. Lines over time is how you see if you’re getting better or worse. 
Line 352:  Don’t fall into the trap of having a nice dashboard with large numbers on it. Num-
Line 353: bers without context are not good or bad. Trend lines tell you if you’re better this
Line 354: week than you were last week. 
Line 355: 11.2.7 Realize that there will be hurdles
Line 356: There are always hurdles. Most will come from within the organizational structure,
Line 357: and some will be technical. The technical ones are easier to fix, because it’s a matter
Line 358: of finding the right solution. The organizational ones need care and attention and a
Line 359: psychological approach.
Line 360:  It’s important not to surrender to a feeling of temporary failure when an iteration
Line 361: goes bad, tests go slower than expected, and so on. It’s sometimes hard to get going,
Line 362: and you’ll need to persist for at least a couple of months to start feeling comfortable
Line 363: with the new process and to iron out all the kinks. Have management commit to con-
Line 364: tinuing for at least three months even if things don’t go as planned. It’s important to
Line 365: get their agreement up front. You don’t want to be running around trying to convince
Line 366: people in the middle of a stressful first month.
Line 367:  Also, absorb this short realization, shared by Tim Ottinger on Twitter (@Tottinge):
Line 368: “If your tests don’t catch all defects, they still make it easier to fix the defects they
Line 369: didn’t catch. It is a profound truth.”
Line 370:  Now that we’ve looked at ways of ensuring things go right, let’s look at some things
Line 371: that can lead to failure.
Line 372: 11.3
Line 373: Ways to fail
Line 374: In the preface to this book, I talked about one project I was involved with that failed,
Line 375: partly because unit testing wasn’t implemented correctly. That’s one way a project can
Line 376: 
Line 377: --- 페이지 251 ---
Line 378: 223
Line 379: 11.3
Line 380: Ways to fail
Line 381: fail. I’ll discuss several others here, along with one that cost me that project, and some
Line 382: things that can be done about them.
Line 383: 11.3.1 Lack of a driving force
Line 384: In the places where I’ve seen change fail, the lack of a driving force was the most pow-
Line 385: erful factor in play. Being a consistent driving force of change has its price. It will take
Line 386: time away from your normal job to teach others, help them, and wage internal politi-
Line 387: cal wars for change. You need to be willing to surrender time for these tasks, or the
Line 388: change won’t happen. Bringing in an outside person, as mentioned in section 11.2.4,
Line 389: will help you in your quest for a consistent driving force.
Line 390: 11.3.2 Lack of political support
Line 391: If your boss explicitly tells you not to make the change, there isn’t a whole lot you can
Line 392: do, besides trying to convince management to see what you see. But sometimes the
Line 393: lack of support is much more subtle than that, and the trick is to realize that you’re
Line 394: facing opposition. 
Line 395:  For example, you may be told, “Sure, go ahead and implement those tests. We’re
Line 396: adding 10% to your time to do this.” Anything below 30% isn’t realistic for beginning
Line 397: a unit testing effort. This is one way a manager may try to stop a trend—by choking it
Line 398: out of existence. 
Line 399:  You need to recognize that you’re facing opposition, but once you know what to
Line 400: look for, it’s easy to identify. When you tell them that their limitations aren’t realistic,
Line 401: you’ll be told, “So don’t do it.”
Line 402: 11.3.3 Ad hoc implementations and first impressions
Line 403: If you’re planning to implement unit testing without prior knowledge of how to write
Line 404: good unit tests, do yourself one big favor: involve someone who has experience and
Line 405: follow good practices (such as those outlined in this book). 
Line 406:  I’ve seen developers jump into the deep water without a proper understanding of
Line 407: what to do or where to start, and that’s not a good place to be. Not only will it take a
Line 408: huge amount of time to learn how to make changes that are acceptable for your situa-
Line 409: tion, but you’ll also lose a lot of credibility along the way for starting out with a bad
Line 410: implementation. This can lead to the pilot project being shut down.
Line 411:  If you read this book’s preface, you’ll know that this happened to me. You have
Line 412: only a couple of months to get things up to speed and convince the higher-ups that
Line 413: you’re achieving results with experiments. Make that time count, and remove any risks
Line 414: that you can. If you don’t know how to write good tests, read a book or get a consul-
Line 415: tant. If you don’t know how to make your code testable, do the same. Don’t waste time
Line 416: reinventing testing methods.
Line 417: 
Line 418: --- 페이지 252 ---
Line 419: 224
Line 420: CHAPTER 11
Line 421: Integrating unit testing into the organization
Line 422: 11.3.4 Lack of team support
Line 423: If your team doesn’t support your efforts, it will be nearly impossible to succeed,
Line 424: because you’ll have a hard time consolidating your extra work on the new process with
Line 425: your regular work. You should strive to have your team be part of the new process or at
Line 426: least not interfere with it. 
Line 427:  Talk to your team members about the changes. Getting their support one by one is
Line 428: sometimes a good way to start, but talking to them as a group about your efforts—and
Line 429: answering their hard questions—can also prove valuable. Whatever you do, don’t take
Line 430: the team’s support for granted. Make sure you know what you’re getting into; these
Line 431: are the people you have to work with on a daily basis.
Line 432: 11.4
Line 433: Influence factors
Line 434: I’ve written and covered influencing behaviors as a full chapter in my book Elastic
Line 435: Leadership (Manning, 2016). If you find this topic interesting, I recommend picking
Line 436: that one up, or reading more about it at 5whys.com. 
Line 437:  One of the things I find even more fascinating than unit tests is people and why
Line 438: they behave the way they do. It can be very frustrating to try to get someone to start
Line 439: doing something (like TDD, for example), and regardless of your best efforts, they
Line 440: just won’t do it. You may have already tried reasoning with them, but you see they
Line 441: don’t do anything in response to your little talk. 
Line 442:  In the book Influencer: The Power to Change Anything (McGraw-Hill, 2007) by Kerry
Line 443: Patterson, Joseph Grenny, David Maxfield, Ron McMillan, and Al Switzler, you’ll find
Line 444: the following mantra (paraphrased):
Line 445: For every behavior that you see, the world is perfectly designed for that behavior to
Line 446: happen. That means that there are other factors besides the person wanting to do
Line 447: something or being able to do it that influence their behavior. Yet we rarely look beyond
Line 448: those two factors.
Line 449: The book exposes us to six influence factors:
Line 450: Personal ability—Does the person have all the skills or knowledge to perform
Line 451: what is required? 
Line 452: Personal motivation—Does the person take satisfaction from the right behavior
Line 453: or dislike the wrong behavior? Do they have the self-control to engage in the
Line 454: behavior when it’s hardest to do so?
Line 455: Social ability—Do you or others provide the help, information, and resources
Line 456: required by that person, particularly at critical times?
Line 457: Social motivation—Are the people around them actively encouraging the right
Line 458: behavior and discouraging the wrong behavior? Are you or others modeling the
Line 459: right behavior in an effective way?
Line 460: Structural (environmental) ability—Are there aspects in the environment (build-
Line 461: ing, budget, and so on) that make the behavior convenient, easy, and safe? Are
Line 462: there enough cues and reminders to stay on course?
Line 463: 
Line 464: --- 페이지 253 ---
Line 465: 225
Line 466: 11.4
Line 467: Influence factors
Line 468: Structural motivation—Are there clear and meaningful rewards (such as pay,
Line 469: bonuses, or incentives) when you or others behave the right or wrong way? Do
Line 470: short-term rewards match the desired long-term results and behaviors you want
Line 471: to reinforce or want to avoid?
Line 472: Consider this a short checklist for starting to understand why things aren’t going your
Line 473: way. Then consider another important fact: there might be more than one factor in
Line 474: play. For the behavior to change, you should change all the factors in play. If you
Line 475: change just one, the behavior won’t change.
Line 476:  Table 11.1 is an example of an imaginary checklist about someone not performing
Line 477: TDD. (Keep in mind that this will differ for each person in each organization.)
Line 478: I put asterisks next to the items in the right column that require work. Here I’ve iden-
Line 479: tified two issues that need to be resolved. Solving only the build machine budget prob-
Line 480: lem won’t change the behavior. They have to get a build machine and deter their
Line 481: managers from giving a bonus on shipping crappy stuff quickly.
Line 482: Table 11.1
Line 483: Influence factors checklist
Line 484: Influence factor
Line 485: Question to ask
Line 486: Example answer 
Line 487: Personal ability
Line 488: Does the person have all the skills or knowl-
Line 489: edge to perform what is required? 
Line 490: Yes. They went through a 
Line 491: three-day TDD course with 
Line 492: Roy Osherove.
Line 493: Personal motivation
Line 494: Does the person take satisfaction from the 
Line 495: right behavior or dislike the wrong behavior? 
Line 496: Do they have the self-control to engage in 
Line 497: the behavior when it’s hardest to do so?
Line 498: I spoke with them, and they 
Line 499: like doing TDD.
Line 500: Social ability
Line 501: Do you or others provide the help, informa-
Line 502: tion, and resources required by that person, 
Line 503: particularly at critical times?
Line 504: Yes.
Line 505: Social motivation
Line 506: Are the people around them actively encour-
Line 507: aging the right behavior and discouraging 
Line 508: the wrong behavior?
Line 509: Are you or others modeling the right behav-
Line 510: ior in an effective way?
Line 511: As much as possible.
Line 512: Structural (environmen-
Line 513: tal) ability
Line 514: Are there aspects in the environment (build-
Line 515: ing, budget, and so on) that make the behav-
Line 516: ior convenient, easy, and safe?
Line 517: Are there enough cues and reminders to 
Line 518: stay on course?
Line 519: They don’t have a budget for 
Line 520: a build machine.*
Line 521: Structural motivation
Line 522: Are there clear and meaningful rewards 
Line 523: (such as pay, bonuses, or incentives) when 
Line 524: you or others behave the right or wrong way?
Line 525: Do short-term rewards match the desired 
Line 526: long-term results and behaviors you want to 
Line 527: reinforce or want to avoid?
Line 528: When they try to spend time 
Line 529: unit testing, their managers 
Line 530: tell them they’re wasting 
Line 531: time. If they ship early and 
Line 532: crappy, they get a bonus.*
Line 533: 
Line 534: --- 페이지 254 ---
Line 535: 226
Line 536: CHAPTER 11
Line 537: Integrating unit testing into the organization
Line 538:  I write much more on this in Notes to a Software Team Leader (Team Agile Publishing,
Line 539: 2014), a book about running a technical team. You can find it at 5whys.com.
Line 540: 11.5
Line 541: Tough questions and answers
Line 542: This section covers some questions I’ve come across in various places. They usually arise
Line 543: from the premise that implementing unit testing can hurt someone personally—a man-
Line 544: ager concerned about their deadlines or a QA employee concerned about their rele-
Line 545: vance. Once you understand where a question is coming from, it’s important to address
Line 546: the issue, directly or indirectly. Otherwise, there will always be subtle resistance.
Line 547: 11.5.1 How much time will unit testing add to the current process?
Line 548: Team leaders, project managers, and clients are the ones who usually ask how much
Line 549: time unit testing will add to the process. They’re the people at the front lines in terms
Line 550: of timing. 
Line 551:  Let’s begin with some facts. Studies have shown that raising the overall code quality
Line 552: in a project can increase productivity and shorten schedules. How does this match up
Line 553: with the fact that writing tests makes coding slower? Through maintainability and the
Line 554: ease of fixing bugs, mostly.
Line 555: NOTE
Line 556: For studies on code quality and productivity, see Programming Productiv-
Line 557: ity (McGraw-Hill College, 1986) and Software Assessments, Benchmarks, and Best
Line 558: Practices (Addison-Wesley Professional, 2000), both by Capers Jones.
Line 559: When asking about time, team leaders may really be asking, “What should I tell my
Line 560: project manager when we go way past our due date?” They may actually think the pro-
Line 561: cess is useful but be looking for ammunition for the upcoming battle. They may also
Line 562: be asking the question not in terms of the whole product but in terms of specific fea-
Line 563: ture sets or functionality. A project manager or customer who asks about timing, on
Line 564: the other hand, will usually be talking in terms of full product releases.
Line 565:  Because different people care about different scopes, your answers may vary. For
Line 566: example, unit testing can double the time it takes to implement a specific feature, but
Line 567: the overall release date for the product may actually be reduced. To understand this,
Line 568: let’s look at a real example I was involved with.
Line 569: A TALE OF TWO FEATURES
Line 570: A large company I consulted with wanted to implement unit testing in their process,
Line 571: beginning with a pilot project. The pilot consisted of a group of developers adding a
Line 572: new feature to a large existing application. The company’s main livelihood was in cre-
Line 573: ating this large billing application and customizing parts of it for various clients. The
Line 574: company had thousands of developers around the world.
Line 575:  The following measures were taken to test the pilot’s success:
Line 576: The time the team spent on each of the development stages 
Line 577: The overall time for the project to be released to the client
Line 578: The number of bugs found by the client after the release
Line 579: 
Line 580: --- 페이지 255 ---
Line 581: 227
Line 582: 11.5
Line 583: Tough questions and answers
Line 584: The same statistics were collected for a similar feature created by a different team for
Line 585: a different client. The two features were nearly the same size, and the teams were
Line 586: roughly at the same skill and experience level. Both tasks were customization efforts—
Line 587: one with unit tests, the other without. Table 11.2 shows the differences in time.
Line 588: Overall, the time it took to release with tests was less than without tests. Still, the man-
Line 589: agers on the team with unit tests didn’t initially believe the pilot would be a success,
Line 590: because they only looked at the implementation (coding) statistic (the first row in
Line 591: table 11.2) as the criteria for success, instead of the bottom line. It took twice the
Line 592: amount of time to code the feature (because unit tests require you to write more
Line 593: code). Despite this, the extra time was more than compensated for when the QA team
Line 594: found fewer bugs to deal with.
Line 595:  That’s why it’s important to emphasize that although unit testing can increase the
Line 596: amount of time it takes to implement a feature, the overall time requirements balance
Line 597: out over the product’s release cycle because of increased quality and maintainability.
Line 598: 11.5.2 Will my QA job be at risk because of unit testing?
Line 599: Unit testing doesn’t eliminate QA-related jobs. QA engineers will receive the applica-
Line 600: tion with full unit test suites, which means they can make sure all the unit tests pass
Line 601: before they start their own testing process. Having unit tests in place will actually make
Line 602: their job more interesting. Instead of doing UI debugging (where every second but-
Line 603: ton click results in an exception of some sort), they’ll be able to focus on finding more
Line 604: logical (applicative) bugs in real-world scenarios. Unit tests provide the first layer of
Line 605: defense against bugs, and QA work provides the second layer—the user acceptance
Line 606: layer. As with security, the application always needs to have more than one layer of
Line 607: protection. Allowing the QA process to focus on the larger issues can produce better
Line 608: applications.
Line 609: Table 11.2
Line 610: Team progress and output measured with and without tests 
Line 611: Stage
Line 612: Team without tests
Line 613: Team with tests
Line 614: Implementation (coding)
Line 615: 7 days
Line 616: 14 days
Line 617: Integration
Line 618: 7 days
Line 619: 2 days
Line 620: Testing and bug fixing
Line 621: Testing, 3 days 
Line 622: Fixing, 3 days 
Line 623: Testing, 3 days 
Line 624: Fixing, 2 days 
Line 625: Testing, 1 day
Line 626: Total: 12 days
Line 627: Testing, 3 days 
Line 628: Fixing, 1 day
Line 629: Testing, 1 day
Line 630: Fixing, 1 day
Line 631: Testing, 1 day
Line 632: Total: 7 days
Line 633: Overall release time
Line 634: 26 days
Line 635: 23 days
Line 636: Bugs found in production
Line 637: 71
Line 638: 11
Line 639: 
Line 640: --- 페이지 256 ---
Line 641: 228
Line 642: CHAPTER 11
Line 643: Integrating unit testing into the organization
Line 644:  In some places, QA engineers write code, and they can help write unit tests for the
Line 645: application. That happens in conjunction with the work of the application developers
Line 646: and not instead of it. Both developers and QA engineers can write unit tests.
Line 647: 11.5.3 Is there proof that unit testing helps?
Line 648: There aren’t any specific studies on whether unit testing helps achieve better code
Line 649: quality that I can point to. Most related studies talk about adopting specific agile
Line 650: methods, with unit testing being just one of them. Some empirical evidence can be
Line 651: gleaned from the web, of companies and colleagues having great results and never
Line 652: wanting to go back to a codebase without tests. A few studies on TDD can be found at
Line 653: The QA Lead here: http://mng.bz/dddo. 
Line 654: 11.5.4 Why is the QA department still finding bugs?
Line 655: You may not have a QA department anymore, but this is still a very prevalent practice.
Line 656: Either way, you’ll still be finding bugs. Please use tests at multiple levels, as described
Line 657: in chapter 10, to gain confidence across many layers of your application. Unit tests
Line 658: give you fast feedback and easy maintainability, but they leave some confidence
Line 659: behind, which can only be gained through some levels of integration tests. 
Line 660: 11.5.5 We have lots of code without tests: Where do we start?
Line 661: Studies conducted in the 1970s and 1980s showed that, typically, 80% of bugs are
Line 662: found in 20% of the code. The trick is to find the code that has the most problems.
Line 663: More often than not, any team can tell you which components are the most prob-
Line 664: lematic. Start there. You can always add some metrics related to the number of bugs
Line 665: per class.
Line 666: Testing legacy code requires a different approach than when writing new code with
Line 667: tests. See chapter 12 for more details.
Line 668: Sources for the 80/20 figure
Line 669: Studies that show 80% of the bugs are in 20% of the code include the following:
Line 670: Albert Endres, “An analysis of errors and their causes in system programs,” IEEE
Line 671: Transactions on Software Engineering 2 (June 1975), 140–49; Lee L. Gremillion,
Line 672: “Determinants of program repair maintenance requirements,” Communications of the
Line 673: ACM 27, no. 8 (August 1984), 826–32; Barry W. Boehm, “Industrial software metrics
Line 674: top 10 list,” IEEE Software 4, no. 9 (September 1987), 84–85 (reprinted in an IEEE
Line 675: newsletter and available online at http://mng.bz/rjjJ); and Shull and others, “What
Line 676: we have learned about fighting defects,” Proceedings of the 8th International Sympo-
Line 677: sium on Software Metrics (2002), 249–58.
Line 678: 
Line 679: --- 페이지 257 ---
Line 680: 229
Line 681: Summary
Line 682: 11.5.6 What if we develop a combination of software and hardware?
Line 683: You can use unit tests even if you develop a combination of software and hardware.
Line 684: Look into the test layers mentioned in the previous chapter to make sure you cover
Line 685: both software and hardware. Hardware testing usually requires the use of simulators
Line 686: and emulators at various levels, but it is a common practice to have a suite of tests both
Line 687: for low-level embedded and high-level code.
Line 688: 11.5.7 How can we know we don’t have bugs in our tests?
Line 689: You need to make sure your tests fail when they should and pass when they should.
Line 690: TDD is a great way to make sure you don’t forget to check those things. See chapter 1
Line 691: for a short walk-through of TDD.
Line 692: 11.5.8 Why do I need tests if my debugger shows that my code works?
Line 693: Debuggers don’t help much with multithreaded code. Also, you may be sure your
Line 694: code works fine, but what about other people’s code? How do you know it works? How
Line 695: do they know your code works and that they haven’t broken anything when they make
Line 696: changes? Remember that coding is the first step in the life of the code. Most of its life,
Line 697: the code will be in maintenance mode. You need to make sure it will tell people when
Line 698: it breaks, using unit tests.
Line 699:  A study held by Curtis, Krasner, and Iscoe (“A field study of the software design
Line 700: process for large systems,” Communications of the ACM 31, no. 11 (November 1988),
Line 701: 1268–87) showed that most defects don’t come from the code itself but result from
Line 702: miscommunication between people, requirements that keep changing, and a lack of
Line 703: application domain knowledge. Even if you’re the world’s greatest coder, chances are
Line 704: that if someone tells you to code the wrong thing, you’ll do it. When you need to
Line 705: change it, you’ll be glad you have tests for everything else, to make sure you don’t
Line 706: break it.
Line 707: 11.5.9 What about TDD?
Line 708: TDD is a style choice. I personally see a lot of value in TDD, and many people find it
Line 709: productive and beneficial, but others find that writing tests after the code is good
Line 710: enough for them. You can make your own choice.
Line 711: Summary
Line 712: Implementing unit testing in their organization is something that many readers
Line 713: of this book will have to face at one time or another.
Line 714: Make sure that you don’t alienate the people who can help you. Recognize
Line 715: champions and blockers inside the organization. Make both groups part of the
Line 716: change process.
Line 717: 
Line 718: --- 페이지 258 ---
Line 719: 230
Line 720: CHAPTER 11
Line 721: Integrating unit testing into the organization
Line 722: Identify possible starting points. Start with a small team or project with a limited
Line 723: scope to get a quick win and minimize project duration risks.
Line 724: Make the progress visible to everyone. Aim for specific goals, metrics, and KPIs.
Line 725: Take note of potential causes of failure, such as the lack of a driving force and
Line 726: lack of political or team support.
Line 727: Be prepared to have good answers to the questions you’re likely to be asked. 

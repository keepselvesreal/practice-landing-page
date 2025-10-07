Line 1: 
Line 2: --- 페이지 258 ---
Line 3: 227
Line 4: Chapter 20
Line 5: Monitoring the Iteration Plan
Line 6: “Facts are better than dreams.”
Line 7: —Winston Churchill
Line 8: In addition to tracking progress toward the high-level goal of a release, it is al-
Line 9: ways helpful to track the development team’s progress toward completing the
Line 10: work of a single iteration. In this chapter, we’ll look at the two tools for iteration
Line 11: tracking: the task board and iteration burndown charts. 
Line 12: The Task Board
Line 13: A task board serves the dual purpose of giving a team a convenient mechanism
Line 14: for organizing their work and a way of seeing at a glance how much work is left.
Line 15: It is important that the task board (or something equivalent to it) allow the team
Line 16: a great deal of flexibility in how they organize their work. Individuals on an agile
Line 17: team do not sign up for (or get assigned) work until they are ready to work on it.
Line 18: This means that except for the last day or two of an iteration, there typically are
Line 19: many tasks that no one has yet signed up for. A task board makes these tasks
Line 20: highly visible so that everyone can see which tasks are being worked on and
Line 21: which are available to sign up for. An example task board is shown in
Line 22: Figure 20.1.
Line 23: The task board is often a large whiteboard or, even better, a corkboard. Taped
Line 24: or pinned to the task board are the story cards as well as the task cards that were
Line 25: written during iteration planning. The task board includes one row for each
Line 26: 
Line 27: --- 페이지 259 ---
Line 28: 228 |
Line 29: Chapter 20
Line 30: Monitoring the Iteration Plan
Line 31: story or feature that will be worked on during the iteration. In Figure 20.1, the
Line 32: first row contains information about the five-point story. The first column of the
Line 33: task board holds the story card. Because the story card shows the point estimate
Line 34: assigned to the story, anyone looking at the task board can quickly determine the
Line 35: number of story points for each story included in the iteration.
Line 36: Figure 20.1 A task board in use during an iteration.
Line 37: The second column holds all of the task cards that the team identified as
Line 38: necessary to implement the story or feature. Each of these cards shows the esti-
Line 39: mate of the work remaining to complete the task. 
Line 40: The third column indicates whether the acceptance tests are ready for the
Line 41: story. I am a big fan of test-driven development (Beck 2002), both at the code
Line 42: level, where I encourage developers to write a failing unit test before writing
Line 43: code, and at the feature level, where I encourage teams to design high-level ac-
Line 44: ceptance tests before they begin coding. If the conditions of satisfaction for each
Line 45: story were identified as part of iteration planning (as advised in Chapter 14, “It-
Line 46: eration Planning”), this is easy, as the conditions of satisfactions are essentially a
Line 47: user story’s high-level acceptance tests. This type of specification by example is
Line 48: 5
Line 49: As a user, I 
Line 50: can...
Line 51: Tests
Line 52: Ready
Line 53: MC
Line 54: 4
Line 55: Code the...
Line 56: In Process
Line 57: DC
Line 58: 4
Line 59: Code the...
Line 60: SC
Line 61: 6
Line 62: Code the...
Line 63: To Verify
Line 64: LC
Line 65: 4
Line 66: Code the...
Line 67: Hours
Line 68: 33
Line 69: 13
Line 70: 8
Line 71: Code the...
Line 72: 5
Line 73: Code the...
Line 74: 6
Line 75: Test the...
Line 76: To Do
Line 77: 5
Line 78: Code the...
Line 79: 8
Line 80: Code the...
Line 81: 6
Line 82: Code the...
Line 83: 3
Line 84: Code the...
Line 85: Story
Line 86: 2
Line 87: As a user, I 
Line 88: can...
Line 89: 3
Line 90: As a user, I 
Line 91: can...
Line 92: 13
Line 93: √
Line 94: √
Line 95: 
Line 96: --- 페이지 260 ---
Line 97: The Task Board 
Line 98: |
Line 99: 229
Line 100: very beneficial for the programmers, as they can refer to specific examples of
Line 101: how each function and business rule is expected to work.
Line 102: I have teams put a big checkmark in the Tests Ready column when they have
Line 103: specified the high-level tests for a story. Further, I encourage teams not to move
Line 104: many cards to the fourth column, In Process, unless the tests are specified. You
Line 105: may not need a Tests Specified column, but it’s a useful, visible reminder to a
Line 106: team that is trying to become accustomed to specifying acceptance tests before
Line 107: coding a feature.
Line 108: The In Process column holds cards that developers have signed up for. Typi-
Line 109: cally, a developer takes a card from the To Do column, puts her initials on it, and
Line 110: moves it to the In Process column. This happens throughout the day as develop-
Line 111: ers are finishing work and selecting what they’ll work on next. No one should
Line 112: sign up for more than one or two cards at a time. This helps maintain a consis-
Line 113: tent flow of work through the process and reduces the cost of context switching
Line 114: among multiple tasks. As a constant reminder of this, when I have a team set up
Line 115: their task board I have them make the In Process column the width of one card.
Line 116: The To Do column is typically wider (and wider than shown in Figure 20.1) be-
Line 117: cause cards are often taped four across there.
Line 118: The To Verify column is another that you may or may not need but that I
Line 119: find useful, especially when working with a team that is learning how to become
Line 120: agile. Ideally, each test activity is thought of and a task card written during iter-
Line 121: ation planning. If so, when a programming task card (“Code the boojum user in-
Line 122: terface”) is finished, it is removed from the task board (or moved to a final colum
Line 123: called Done). At that time, someone can sign up for the associated test card
Line 124: (“Test the boojum user interface”). However, I find there are times when a devel-
Line 125: oper considers a task card done but would like a fresh pair of eyes to take a quick,
Line 126: verifying look. In those cases, and when there is no associated test task, the task
Line 127: card is placed in the To Verify column.
Line 128: The developers are encouraged to change the estimate on any task card on
Line 129: the board at any time. For example, if I start working on a card and realize that
Line 130: the estimate of two hours on it is wrong, I will go over to the task board, cross
Line 131: out the two, and replace it with perhaps a six. If I believe the estimate is even fur-
Line 132: ther off, I may rip up that task card and replace it with two or three task cards,
Line 133: each with its own estimate. The final colum on the task board is simply a sum of
Line 134: the hours of work remaining on the feature or story. I usually sum the hours for
Line 135: each row every morning. I use these totals to draw an iteration burndown chart,
Line 136: which is the second tool for tracking the progress of an iteration.
Line 137: 
Line 138: --- 페이지 261 ---
Line 139: 230 |
Line 140: Chapter 20
Line 141: Monitoring the Iteration Plan
Line 142: Iteration Burndown Charts
Line 143: Drawing a release burndown chart is a great way to see whether a project is go-
Line 144: ing astray or not. Depending on the length of your iterations, it can be useful to
Line 145: create an iteration burndown chart. If you’re using one-week iterations, it prob-
Line 146: ably isn’t necessary. By the time a trend is visible on an iteration burndown
Line 147: chart, a one-week iteration will be over. However, I’ve found iteration burndown
Line 148: charts to be extremely useful with iteration lengths of two weeks or longer. An
Line 149: iteration burndown chart plots hours remaining by day, as shown in Figure 20.2.
Line 150: To create an iteration burndown chart, simply sum all of the hours on your
Line 151: task board once per day and plot that on the chart. If the team’s task board is
Line 152: drawn on a whiteboard, I usually draw the iteration burndown by hand on one
Line 153: side of the task board. If the task board is on a corkboard, I tack a large piece of
Line 154: paper to the corkboard and draw the burndown chart on it.
Line 155: Tracking Bugs on a Task Board
Line 156: Many teams, when they begin the transition to an agile development
Line 157: process, are faced with a large number of legacy bugs. Not only is there
Line 158: usually a large backlog of bugs to be fixed “someday,” but also bugs con-
Line 159: tinue to come in at a rapid rate. A common challenge for teams moving
Line 160: to an agile process is how to deal with these bugs. The task board pro-
Line 161: vides a convenient mechanism for starting to correct this problem.
Line 162: As an example of how the task board can help, suppose the product
Line 163: owner includes “Fix ten ‘high’ bugs” in the new iteration. The product
Line 164: owner selects the ten bugs, and the developers write a task card (with an
Line 165: estimate) for each. The cards are taped in the To Do column of a row on
Line 166: the task board. As the iteration progresses, the developers work on the
Line 167: ten bugs in the same way they work on other task cards. Now suppose a
Line 168: user finds a new bug halfway through the iteration. If the new bug is
Line 169: considered a higher priority than one or more bug remaining in the To
Line 170: Do column, the product owner can swap out an equivalent amount of
Line 171: bug fixing work in favor of fixing the new bug.
Line 172: This approach allows a team to correct legacy defects at whatever rate
Line 173: the product owner chooses. The team could allocate 40 hours to bug fix-
Line 174: ing, or they could allocate 100 hours. The product owner selects how
Line 175: much of an iteration should be directed toward bug fixing rather than
Line 176: new feature development. The product owner and team then collobora-
Line 177: tively select which bugs fit within that amount of time.
Line 178: 
Line 179: --- 페이지 262 ---
Line 180: Tracking Effort Expended 
Line 181: |
Line 182: 231
Line 183: Figure 20.2 An iteration burndown chart.
Line 184: Tracking Effort Expended
Line 185: In the previous chapter, the analogy of a project as a sailboat was introduced to
Line 186: make the point that a sailboat’s progress is not always easily measured. A sailboat
Line 187: that sailed for eight hours yesterday and then anchored may or may not be eight
Line 188: hours closer to its destination. Wind and current may have pushed the sailboat
Line 189: off what was believed to be its course. The boat may be closer to or farther from
Line 190: its destination. When this is the case, the most useful thing the crew can do is
Line 191: assess where they are relative to the destination. Measuring the distance traveled
Line 192: or time spent traveling are not helpful if we’re not sure all progress was in the
Line 193: right direction. 
Line 194: On a project, it is far more useful to know how much remains to be done
Line 195: rather than how much has been done. Further, tracking effort expended and
Line 196: comparing it with estimated effort can lead to “evaluation apprehension” (Sand-
Line 197: ers 1984). When estimators are apprehensive about providing an estimate, the
Line 198: familiar “fight or flight” instinct kicks in, and estimators rely more on instinct
Line 199: than on analytical thought (Jørgensen 2004).
Line 200: Tracking effort expended in an effort to improve estimate accuracy is a very
Line 201: fine line. It can work (Lederer and Prasad 1998; Weinberg and Schulman 1974).
Line 202: However, the project manager or whoever is doing the tracking must be very
Line 203: 50
Line 204: 100
Line 205: 150
Line 206: 200
Line 207: 250
Line 208: Hours
Line 209: Days
Line 210: 
Line 211: --- 페이지 263 ---
Line 212: 232 |
Line 213: Chapter 20
Line 214: Monitoring the Iteration Plan
Line 215: careful to avoid putting significant evaluation pressure on the estimators, as do-
Line 216: ing so could result in estimates that are worse rather than better.
Line 217: Additionally, keep in mind that variability is a part of every estimate. No mat-
Line 218: ter how much effort is put into improving estimates, a team will never be able to
Line 219: estimate perfectly. Evidence of this is no further away than your morning com-
Line 220: mute to work. There is an inherent amount of variability in your commute re-
Line 221: gardless of how you travel, how far you must go, and where you live. If you drive
Line 222: to work, no amount of driving skill will eliminate this variability.
Line 223: Individual Velocity
Line 224: Some teams refer to individual velocity as the number of story points or ideal
Line 225: days completed by an individual team member. Do not track individual velocity.
Line 226: Tracking individual velocity leads to behavior that works against the success of
Line 227: the project. Suppose it has been announced that individual velocity will be mea-
Line 228: sured and tracked from iteration to iteration. How do you think individuals will
Line 229: respond? If I am forced to choose between finishing a story on my own and help-
Line 230: ing someone else, what incentive does measuring individual velocity give me?
Line 231: Individuals should be given every incentive possible to work as a team. If the
Line 232: team’s throughput is increased by my helping someone else, that’s what I should
Line 233: do. Team velocity matters; individual velocity doesn’t. It’s not even a metric of
Line 234: passing interest. 
Line 235: As a further argument against measuring individual velocity, you shouldn’t
Line 236: even be able to calculate it. Most user stories should be written such that they
Line 237: need to be worked on by more than one person, such as a user interface designer,
Line 238: programmer, database engineer, and a tester. If most of your stories can be com-
Line 239: pleted by a single person, you should reconsider how your stories are written.
Line 240: Normally, this means they need to be written at a higher level so that work from
Line 241: multiple individuals is included with each.
Line 242: Summary
Line 243: A task board—which is often a whiteboard, corkboard, or just a designated space
Line 244: on a wall—helps a team organize and visualize their work. The columns of a task
Line 245: board are labeled, and team members move task cards through the columns as
Line 246: work progresses.
Line 247: An iteration burndown chart is similar to a release burndown chart but is
Line 248: used to track only the work of the current iteration. It graphs the number of
Line 249: 
Line 250: --- 페이지 264 ---
Line 251: Discussion Questions 
Line 252: |
Line 253: 233
Line 254: hours remaining on the vertical axis and the days of the iteration on the horizon-
Line 255: tal axis.
Line 256: Teams should be reluctant to track the actual hours expended on tasks to get
Line 257: better at estimating. The risks and the effort to do so usually outweigh the
Line 258: benefits.
Line 259: Teams should not calculate or track individual velocity.
Line 260: Discussion Questions
Line 261: 1. In your organization, would the benefits of tracking the actual effort ex-
Line 262: pended on tasks and comparing these with the estimates outweigh the risks
Line 263: and costs of doing so?
Line 264: 2. If your current project team is not collocated, what can you do to achieve
Line 265: some of the same benefits that collocated teams experience when using a
Line 266: task board?
Line 267: 
Line 268: --- 페이지 265 ---
Line 269: This page intentionally left blank 
Line 1: 
Line 2: --- 페이지 176 ---
Line 3: 145
Line 4: Chapter 14
Line 5: Iteration Planning
Line 6: “It is a capital mistake to theorize
Line 7: before one has data.”
Line 8: —Sherlock Holmes, Scandal in Bohemia
Line 9: A release plan is an excellent high-level view of how a team intends to deliver the
Line 10: most valuable product they can. However, a release plan provides only the high-
Line 11: level view of the product being built. It does not provide the short-term, more
Line 12: detailed view that teams use to drive the work that occurs within an iteration.
Line 13: With an iteration plan, a team takes a more focused, detailed look at what will be
Line 14: necessary to implement completely only those user stories selected for the new
Line 15: iteration. 
Line 16: An iteration plan is created in an iteration planning meeting. This meeting
Line 17: should be attended by the product owner, analysts, programmers, testers, data-
Line 18: base engineers, user interaction designers, and so on. Anyone involved in taking
Line 19: a raw idea and turning it into a functioning product should be present.
Line 20: Tangibly, an iteration plan can be as simple as a spreadsheet or a set of note
Line 21: cards with one task handwritten on each card. In either case, tasks and stories
Line 22: should be organized so that it’s possible to tell which tasks go with which stories.
Line 23: For example, see Table 14.1, which shows an iteration plan in a spreadsheet.
Line 24: Tasks are shown one per row and are indented beneath the story to which they
Line 25: apply.
Line 26: As an alternative to a spreadsheet, see Figure 14.1, which illustrates using
Line 27: note cards for iteration planning. The cards can be arranged as in that figure on
Line 28: 
Line 29: --- 페이지 177 ---
Line 30: 146 |
Line 31: Chapter 14
Line 32: Iteration Planning
Line 33: a table or floor, or by taping or pinning them to a wall. For collocated teams, my
Line 34: preference is to do iteration planning with note cards. The team may walk out of
Line 35: an iteration planning meeting and immediately type the cards into a software
Line 36: system, if they desire, but there are very real benefits to using cards during the
Line 37: meeting.
Line 38: One of the most significant advantages to using note cards during iteration
Line 39: planning is that it allows everyone to participate in the process. If tasks are being
Line 40: typed into a system during the iteration planning meeting, someone has his or
Line 41: her fingers on a keyboard. There is tremendous power to having control over the
Line 42: keyboard. All conversations had better involve the typist, or nothing will get en-
Line 43: tered into the release plan. Worse, whoever has the keyboard can change what
Line 44: gets entered into the release plan. 
Line 45: Two examples attest to this power. In the first case, the team discussed a par-
Line 46: ticular item and decided it should be estimated at twelve hours. The keyboard
Line 47: was in the control of a combination project manager/technical lead. He entered
Line 48: an estimate of eight into the system because “there’s no way it will take that
Line 49: long,” even though he was extremely unlikely to be the one who would do the
Line 50: task.
Line 51: Table 14.1 An Iteration Plan Shown as a Simple Spreadsheet
Line 52: Row
Line 53: User Story / Task
Line 54: Hours
Line 55: 1
Line 56: As a coach, I can assign swimmers to events for a meet.
Line 57: 2
Line 58: Determine rules about who can swim in which events.
Line 59: 6
Line 60: 3
Line 61: Specify acceptance tests to show how this should work.
Line 62: 8
Line 63: 4
Line 64: Design user interface.
Line 65: 16
Line 66: 5
Line 67: Code user interface.
Line 68: 8
Line 69: 6
Line 70: Add tables and stored procedures to database.
Line 71: 6
Line 72: 7
Line 73: Automate tests.
Line 74: 6
Line 75: 8
Line 76: As a swimmer, I can update my demographics.
Line 77: 9
Line 78: Specify acceptance tests.
Line 79: 5
Line 80: 10
Line 81: Change view-only demographics page to allow edits.
Line 82: 6
Line 83: 11
Line 84: …
Line 85: 
Line 86: --- 페이지 178 ---
Line 87: Tasks Are Not Allocated During Iteration Planning 
Line 88: |
Line 89: 147
Line 90: Figure 14.1 Iteration planning can be done with note cards on a table or wall.
Line 91: In the second case, the team I was coaching discussed how a new feature
Line 92: would be implemented—would it be server-side Java code or a stored procedure
Line 93: in the database? Everyone but the team lead, who had the keyboard, agreed it
Line 94: would be implemented through stored procedures. He was asked to create a task
Line 95: of “add stored procedures” on their spreadsheet. Instead, he typed “Write data
Line 96: storage code.” His message was clear: This issue has not been resolved.
Line 97: Compare these two situations to an iteration planning meeting in which
Line 98: anyone can grab a card and write a task at any time. Using cards is a much more
Line 99: democratic and collaborative approach and is likely to lead to better results
Line 100: throughout the iteration and the project, not just during that meeting.
Line 101: Tasks Are Not Allocated During Iteration Planning
Line 102: Before looking at the things that are done during iteration planning, it’s impor-
Line 103: tant to clarify one thing that is not done. While planning an iteration, tasks are
Line 104: not allocated to specific individuals. At the start of the iteration, it may appear
Line 105: obvious who will work on a specific task; however, based on the progress of the
Line 106: whole team against the entire set of tasks, what is obvious at the start may not be
Line 107: Determine rules 
Line 108: about who can 
Line 109: swim in which 
Line 110: events.
Line 111: 6
Line 112: As a coach, I can
Line 113: assign swimmers 
Line 114: to events for a 
Line 115: meet.
Line 116: Specify acceptance
Line 117: tests to show how
Line 118: this should work. 
Line 119: 8
Line 120: Design user 
Line 121: interface.
Line 122: 16
Line 123: Code user 
Line 124: interface.
Line 125: 8
Line 126: Specify 
Line 127: acceptance tests.
Line 128: 5
Line 129: As a swimmer, I
Line 130: can update my 
Line 131: demographics.
Line 132: -only 
Line 133: Change view
Line 134: demographics 
Line 135: page to allow edits.
Line 136: 6
Line 137: Tasks
Line 138: Story
Line 139: 
Line 140: --- 페이지 179 ---
Line 141: 148 |
Line 142: Chapter 14
Line 143: Iteration Planning
Line 144: what happens during the iteration. For example, when planning an iteration we
Line 145: may assume that our database administrator will complete the “tune the ad-
Line 146: vanced search query” task because she has the best SQL skills on the team. How-
Line 147: ever, if she’s unable to get to this task, someone else may step forward and do it.
Line 148: Individuals do not sign up for tasks until the iteration begins and generally
Line 149: sign up for only one or two related tasks at a time. New tasks are not begun until
Line 150: previously selected ones are completed.
Line 151: There’s nothing to gain and quite a bit to lose by assigning individuals to
Line 152: specific tasks during iteration planning. Projects do best when they foster a
Line 153: “we’re all in this together” attitude—when team members pick up slack for each
Line 154: other knowing that the favor will be returned. When individuals sign up for spe-
Line 155: cific tasks at the beginning of the iteration, it works against fostering a unified
Line 156: commitment to achieving the goals of the iteration.
Line 157: How Iteration and Release Planning Differ
Line 158: The release plan looks forward through the release of the product, usually three
Line 159: to six months out at the start of a new project. In contrast, the iteration plan
Line 160: looks ahead only the length of one iteration, usually two to four weeks. The user
Line 161: stories of the release plan are decomposed into tasks on the iteration plan.
Line 162: Where the user stories of a release plan are estimated in story points or ideal
Line 163: days, the tasks on the iteration plan are estimated in ideal hours.
Line 164: Why are the tasks of an iteration plan estimated in hours but the stories of a
Line 165: release plan are estimated in story points or ideal days? Primarily because it is
Line 166: possible to do so. The work of an iteration is no more than a few weeks off, and
Line 167: the team should have a reasonable level of insight into the work, especially after
Line 168: discussing during the iteration planning meeting. This allows them to credibly
Line 169: estimate the tasks of an iteration in hours. The user stories that comprise a re-
Line 170: lease each represent multiple tasks, are more vague, and less understood so they
Line 171: must be estimated in more abstract units such as story points or ideal days.
Line 172: These primary differences between a release plan and an iteration plan are
Line 173: summarized in Table 14.2.
Line 174: The primary purpose of iteration planning is to refine suppositions made in
Line 175: the more coarse-grained release plan. The release plan is usually intentionally
Line 176: vague about the specific order in which user stories will be worked on. Addition-
Line 177: ally, at the time of iteration planning the team knows more than when the re-
Line 178: lease plan was last updated. Planning the iteration as it begins allows the team to
Line 179: make use of their recently acquired knowledge. In this way, agile planning
Line 180: 
Line 181: --- 페이지 180 ---
Line 182: Velocity-Driven Iteration Planning 
Line 183: |
Line 184: 149
Line 185: becomes a two-stage process. The first stage is the release plan, with its rough
Line 186: edges and general uncertainties. The second stage is the iteration plan. An itera-
Line 187: tion plan still has some rough edges and continues to be uncertain. However, be-
Line 188: cause it is created concurrent with the start of a new iteration, an iteration plan
Line 189: is more detailed than a release plan.
Line 190: Creating the iteration plan leads a team into discussions about both product
Line 191: design and software design. Product design discussions, for example, may be
Line 192: around topics such as the best combination of stories for optimizing value, inter-
Line 193: pretation of feedback from showing working software to customers, or the extent
Line 194: to which a desired feature should be implemented (that is, will 20% of the fea-
Line 195: ture and effort deliver 80% of the value?). Software design discussions may, for
Line 196: example, involve the appropriate architectural tier in which to implement a new
Line 197: feature, which technologies should be used, whether existing code can be re-
Line 198: used, and so on. As a result of these discussions the team comes to a better un-
Line 199: derstanding of what should and will be built, and they also create a list of the
Line 200: tasks needed to achieve their goal for the iteration.
Line 201: Velocity-Driven Iteration Planning
Line 202: At a broad level, there are two ways of planning an iteration, which I refer to as
Line 203: velocity-driven and commitment-driven. Different teams use different ap-
Line 204: proaches, and each can be successful. Additionally, the two general approaches
Line 205: can be combined to varying degrees. In this section, we’ll consider velocity-
Line 206: driven iteration planning; in the next, we’ll focus on commitment-driven itera-
Line 207: tion planning.
Line 208: The steps involved in velocity-driven iteration planning are shown in
Line 209: Figure 14.2. First, the team collaboratively adjusts priorities. They may have
Line 210: learned something in the preceding iteration that alters their priorities. Next,
Line 211: they identify the target velocity for the coming iteration. The team then selects
Line 212: an iteration goal, which is a general description of what they wish to accomplish
Line 213: during the coming iteration. After selecting an iteration goal, the team selects
Line 214: Table 14.2 The Primary Differences between a Release and an Iteration Plan
Line 215: Release Plan
Line 216: Iteration Plan
Line 217: Planning horizon
Line 218: 3–9 months
Line 219: 1–4 weeks
Line 220: Items in plan
Line 221: User stories
Line 222: Tasks
Line 223: Estimated in
Line 224: Story points or ideal days
Line 225: Ideal hours
Line 226: 
Line 227: --- 페이지 181 ---
Line 228: 150 |
Line 229: Chapter 14
Line 230: Iteration Planning
Line 231: the top-priority user stories that support that goal. As many stories are selected
Line 232: as necessary for the sum of their ideal-day or story-point estimates to equal the
Line 233: target velocity. Finally, each selected story is split into tasks, and each task is es-
Line 234: timated. These steps are described in more detail throughout the rest of this
Line 235: chapter.
Line 236: Figure 14.2 The sequence of steps in velocity-driven iteration planning.
Line 237: Adjust Priorities
Line 238: Imagine all of the user stories either physically stacked up or sorted within a
Line 239: spreadsheet such that the most valuable story is at the top and the least valuable
Line 240: is at the bottom. The project could progress by always taking stories from the top
Line 241: of this prioritized list to start each iteration. However, business and project con-
Line 242: ditions change quickly, so it is always worth a quick reconsideration of priorities. 
Line 243: One source of changes to priorities is the iteration review meeting, which is
Line 244: held after an iteration is finished. During the iteration review, the new function-
Line 245: ality and capabilities that were added during the iteration are demonstrated to
Line 246: stakeholders, the extended project community, and anyone else who is inter-
Line 247: ested. Valuable feedback is often received during these iteration reviews. The
Line 248: product owner herself should generally not come up with new ideas or changes
Line 249: during the iteration review, because she’s been involved daily throughout the it-
Line 250: eration. However, many others (including potential customers and users) may
Line 251: be seeing the results of the iteration for the first time. They will often have good
Line 252: new ideas that could preempt previously high-priority items. 
Line 253: As described in Chapter 9, “Prioritizing Themes,” user stories and themes
Line 254: are prioritized based on their financial value to the product, their cost, the
Line 255: amount and signficance of what the team will learn, and the amount of risk re-
Line 256: duced. Ideally, a team should wait until after the iteration review meeting before
Line 257: Identify an
Line 258: iteration
Line 259: goal
Line 260: Select user
Line 261: stories
Line 262: Estimate
Line 263: tasks
Line 264: Adjust
Line 265: priorities
Line 266: Determine
Line 267: target
Line 268: velocity
Line 269: Do in any
Line 270: sequence
Line 271: Split user
Line 272: stories into
Line 273: tasks
Line 274: 
Line 275: --- 페이지 182 ---
Line 276: Identify an Iteration Goal 
Line 277: |
Line 278: 151
Line 279: discussing priorities for the coming iteration. After all, what they hear during
Line 280: the iteration review may influence them, and it’s hard to prioritize next itera-
Line 281: tion’s work if you are not entirely sure of what will be completed in this iteration.
Line 282: However, in many organizations I’ve found it useful to hold a prioritization
Line 283: meeting a few days before the start of a new iteration. I do this to fit the iteration
Line 284: review and the iteration planning meetings into the same day more easily.
Line 285: An iteration review will typically take thirty to sixty minutes. For a large
Line 286: product with multiple teams, it’s quite feasible that the product owner and other
Line 287: key stakeholders necessary for prioritization discussions could spend half a day
Line 288: in iteration reviews. Add another four hours to plan an iteration, and there may
Line 289: not be time to discuss priorities on the same day. 
Line 290: I usually schedule the prioritization meeting for two days before the end of
Line 291: the iteration. By that time, it’s normally clear if there will be unfinished work
Line 292: from the current iteration. This allows the product owner to decide whether fin-
Line 293: ishing that work will be a priority for the coming iteration. The product owner
Line 294: conducts the prioritization meeting and involves anyone she thinks can contrib-
Line 295: ute to a discussion of the project’s priorities. After having this meeting, the prod-
Line 296: uct owner can usually quickly and on the fly adjust priorities based on anything
Line 297: that happens during the iteration review.
Line 298: Determine Target Velocity
Line 299: The next step in velocity-driven iteration planning is to determine the team’s
Line 300: target velocity. The default assumption by most teams is that their velocity in the
Line 301: next iteration will equal the velocity of the most recent iteration. Beck and
Line 302: Fowler (2000) call this yesterday’s weather, because our best guess of today's
Line 303: weather is that it will be like yesterday's weather. Other teams prefer to use a
Line 304: moving average over perhaps the last three iterations. 
Line 305: If a team has not worked together before or is new to their agile process,
Line 306: they will have to forecast velocity. Techniques for doing so are described in
Line 307: Chapter 16, “Estimating Velocity.”
Line 308: Identify an Iteration Goal
Line 309: With their priorities and target velocity in mind, the team identifies a goal they
Line 310: would like to achieve during the iteration. The goal succinctly describes what
Line 311: they would like to accomplish during that period. As an example, the SwimStats
Line 312: team may select “All demographics features are finished” as an iteration goal.
Line 313: Other example iteration goals for SwimStats could include the following:
Line 314: 
Line 315: --- 페이지 183 ---
Line 316: 152 |
Line 317: Chapter 14
Line 318: Iteration Planning
Line 319: ◆Make progress on reports.
Line 320: ◆Finish all event time reports.
Line 321: ◆Get security working.
Line 322: The iteration goal is a unifying statement about what will be accomplished
Line 323: during the iteration. It does not have to be very specific. For example, “Make
Line 324: progress on reports” is a good iteration goal. It does not have to be made more
Line 325: specific, as in “Finish 15 reports” or “Do the meet results reports.” If “Make
Line 326: progress on reports” is the best description of what will be worked on in the
Line 327: coming iteration, it is a good statement of that goal.
Line 328: Select User Stories
Line 329: Next, the product owner and team select stories that combine to meet the itera-
Line 330: tion goal. If the SwimStats team selected an iteration goal of “All demographics
Line 331: features are finished,” they would work on any demographics-related stories that
Line 332: were not yet finished. This might include
Line 333: ◆As a swimmer, I can update my demographics.
Line 334: ◆As a coach, I can enter demographic data on each of my swimmers.
Line 335: ◆As a coach, I can import a file of all demographic data.
Line 336: ◆As a coach, I can export a file of all demographic data.
Line 337: In selecting the stories to work on, the product owner and team consider the
Line 338: priority of each story. For example, if exporting a file of demographic data is near
Line 339: the bottom of the prioritized requirements list for the product, it may not be in-
Line 340: cluded in the iteration. In that case, the iteration goal could have been better
Line 341: stated as “The most important demographics features are finished.”
Line 342: Split User Stories into Tasks
Line 343: Once the appropriate set of user stories has been selected, each is decomposed
Line 344: into the set of tasks necessary to deliver the new functionality. Suppose the high-
Line 345: est-priority user story is “As a coach, I can assign swimmers to events for an up-
Line 346: coming meet.” This user story will be turned into a list of tasks, such as:
Line 347: ◆Determine rules that affect who can be assigned to which events.
Line 348: ◆Write acceptance test cases that show how this should work.
Line 349: ◆Design the user interface.
Line 350: 
Line 351: --- 페이지 184 ---
Line 352: Split User Stories into Tasks 
Line 353: |
Line 354: 153
Line 355: ◆Get user interface feedback from coaches.
Line 356: ◆Code the user interface.
Line 357: ◆Code the middle tier.
Line 358: ◆Add new tables to database.
Line 359: ◆Automate the acceptance tests.
Line 360: A common question around iteration planning is what should be included.
Line 361: All tasks necessary to go from a user story to a functioning, finished product
Line 362: should be identified. If there are analysis, design, user interaction design, or
Line 363: other tasks necessary, they need to be identified and estimated. Because the goal
Line 364: of each iteration is to produce a potentially shippable product, take care to in-
Line 365: clude tasks for testing and documenting the product. Including test tasks is im-
Line 366: portant because the team needs to think right at the start of the iteration about
Line 367: how a user story will be tested. This helps engage testers right from the start of
Line 368: the iteration, which improves the cross-functional behavior of the team.
Line 369: Include Only Work That Adds Value to This Project
Line 370: The iteration plan should identify only those tasks that add immediate value to
Line 371: the current project. Obviously, that includes tasks that may be considered analy-
Line 372: sis, design, coding, testing, user interface design, and so on. Don’t include the
Line 373: hour in the morning when you answer email. Yes, some of those email messages
Line 374: are project-related, but tasks like “answer email, 1 hour” should not be included
Line 375: in an iteration plan. 
Line 376: Similarly, suppose you need to meet with the company’s director of person-
Line 377: nel about a new annual review process. That should not be included in the itera-
Line 378: tion plan. Even though project team members will be reviewed using the new
Line 379: process, the meeting to discuss it (and any follow-on work you need to do) is not
Line 380: directly related to developing the product. So no tasks associated with it become
Line 381: part of the iteration plan.
Line 382: Be Specific Until It’s a Habit
Line 383: New agile teams are often not familiar with or skilled at writing automated unit
Line 384: tests. However, this is a skill they work to cultivate during the first few itera-
Line 385: tions. During that period, I encourage programmers to identify and estimate
Line 386: unit testing tasks explicitly. A programmer may, for example, identify that cod-
Line 387: ing a new feature will take eight hours and that writing its unit tests will take
Line 388: five hours. Later, once unit testing has become a habit for the programmers, the
Line 389: programmer would write only one card saying to code the new feature and
Line 390: 
Line 391: --- 페이지 185 ---
Line 392: 154 |
Line 393: Chapter 14
Line 394: Iteration Planning
Line 395: would give it an estimate that included time to automate the unit tests. Once
Line 396: something like unit testing becomes a habit, it can be included within another
Line 397: task. Until then, however, making it explicit helps keep awareness of the task
Line 398: high.
Line 399: Meetings Count (A Lot)
Line 400: You should identify, estimate, and include tasks for meetings related to the
Line 401: project. When estimating the meeting, be sure to include the time for all partic-
Line 402: ipants, as well as any time spent preparing for the meeting. Suppose the team
Line 403: schedules a meeting to discuss feedback from users. All seven team members
Line 404: plan to attend the one-hour meeting, and the analyst plans to spend two hours
Line 405: preparing for the meeting. The estimate for this task is nine hours. I usually en-
Line 406: ter this into the iteration plan as a single nine-hour task, rather than as a sepa-
Line 407: rate task for each team member.
Line 408: Bugs
Line 409: An agile team has the goal of fixing all bugs in the iteration in which they are dis-
Line 410: covered. They become able to achieve this as they become more proficient in
Line 411: working in short iterations, especially through relying on automated testing.
Line 412: When a programmer gives an estimate for coding something, that estimate in-
Line 413: cludes time for fixing any bugs found in the implementation, or a separate task
Line 414: (“Correct bugs”) is identified and estimated. My preference is for identifying a
Line 415: single task but not considering it complete until all of its tests pass. 
Line 416: A defect found later (or not fixed during the iteration in which it was discov-
Line 417: ered) is treated the same way as a user story. Fixing the defect will need to be pri-
Line 418: oritized into a subsequent iteration in the same way that any other user story
Line 419: would be. Outside an iteration, the whole idea of a defect starts to go away. Fix-
Line 420: ing a bug and adding a feature become two ways of describing the same thing. 
Line 421: Handling Dependencies
Line 422: Often, developing one user story will depend upon the previous implementation
Line 423: of another. In most cases, these dependencies are not a significant issue. There is
Line 424: usually what I consider a natural order to implementing user stories—that is,
Line 425: there is a sequence that makes sense to both developers and the product owner.
Line 426: It is not a problem when there are dependencies among stories that lead to
Line 427: developing them in their natural order. The natural order is usually the order
Line 428: the team assumed when they estimated the stories. For example, the SwimStats
Line 429: team would probably assume that swimmers can be added to the system before
Line 430: they can be deleted. When stories are worked on in a sequence other than what
Line 431: 
Line 432: --- 페이지 186 ---
Line 433: Split User Stories into Tasks 
Line 434: |
Line 435: 155
Line 436: was assumed when estimating, during iteration planning the team will often
Line 437: have to include additional tasks that make it possible to work on stories in the
Line 438: new order.
Line 439: As an example, the natural order for the SwimStats website would be to
Line 440: complete the features that let a user add new swimmers to the system and then
Line 441: the features that let a user view an individual swimmer’s fastest times in each
Line 442: event. It’s a little unusual to think about seeing a swimmer’s fastest times before
Line 443: having the screens through which swimmers are added to the system. However,
Line 444: it could be done if the product owner and team wanted to develop the features in
Line 445: that order. To do so, they would, of course, need to design enough of the database
Line 446: to hold swimmers and their times. They would also have to put at least one
Line 447: swimmer and her times into the database. Because this is part of the feature they
Line 448: don’t want to do first, they would add the swimmer (and her times) to the data-
Line 449: base directly rather than through any user interface and software they devel-
Line 450: oped. 
Line 451: For the SwimStats team to do this, during iteration planning they will need
Line 452: to identify a few tasks that would not have been identified if these two stories had
Line 453: been worked on in their natural order. For example, if the ability to add swim-
Line 454: mers existed already, the team would not need to include a task of “Design data-
Line 455: base tables for information about individual swimmers.” However, because the
Line 456: stories are being worked on out of their natural order, they will need to include
Line 457: this task.
Line 458: Does that mean that working out of the natural order will cause the project
Line 459: to take longer? Two answers: Probably not, and it doesn’t matter.
Line 460: First, the project will probably not take longer; all we’ve done is shift some
Line 461: tasks from one user story to another. Designing the swimmer tables in this ex-
Line 462: ample would have happened sooner or later. When the time comes to work on
Line 463: the story about adding new swimmers to the system, that story will be done
Line 464: more quickly because part of its work is already complete.
Line 465: You may be worried about the impact this task shifting has on the estimates
Line 466: given to the two stories. We may, for example, have shifted a point or an ideal day
Line 467: of work from one story to the other. In most cases, this isn’t a big deal, and the
Line 468: differences will wash out over the course of the project. If anything, I’ve observed
Line 469: this to be a pessimistic shift, in that a five-point story becomes a six-point story.
Line 470: But because the team gives itself credit for only five points when they’re finished,
Line 471: they slightly understate their velocity. Because the impact is small with a slightly
Line 472: pessimistic bias, I usually don’t worry about it. However, if you’re concerned
Line 473: about these impacts or if the task shifting is much more significant, re-estimate
Line 474: 
Line 475: --- 페이지 187 ---
Line 476: 156 |
Line 477: Chapter 14
Line 478: Iteration Planning
Line 479: the stories involved as soon as you decide to work on them in other than the nat-
Line 480: ural order.
Line 481: Second, even if working on the stories in this order does cause the project to
Line 482: take longer, it doesn’t matter, because there presumably was some good reason
Line 483: for working on them out of their natural order. The team may want to work on
Line 484: stories in a particular order so that they can address a technical risk earlier. Or a
Line 485: product owner may want earlier user feedback on a story that would more natu-
Line 486: rally have been developed later. By developing the stories out of their natural or-
Line 487: der, the team is able to get early feedback and potentially save a month or two of
Line 488: rework near the end of the project (when the schedule is least likely to be able to
Line 489: accommodate such a change).
Line 490: Work That Is Difficult to Split
Line 491: Some features are especially difficult to split into tasks. For example, I was re-
Line 492: cently in a planning meeting discussing a small change to a legacy feature. No
Line 493: one was comfortable in his or her ability to think through all of the possible im-
Line 494: pacts of the change. We were certain that some sections of the code would be af-
Line 495: fected but were not sure whether other sections would be. The changes were
Line 496: small in the sections we were sure about; we estimated them at a total of four
Line 497: hours. If the other sections were affected, we thought the estimate could go
Line 498: much higher, possibly as high as twenty hours. We couldn’t be sure without
Line 499: looking at the code, and we didn’t want to stop a planning meeting for that. In-
Line 500: stead, we wrote these two tasks:
Line 501: ◆Determine what’s affected—two hours.
Line 502: ◆Make the changes—ten hours.
Line 503: This first task is called a spike. A spike is a task included in an iteration plan
Line 504: that is being undertaken specifically to gain knowledge or answer a question. In
Line 505: this case, the team did not have a good guess at something, so they created two
Line 506: tasks: one a spike and one a placeholder with a guess at the duration. The spike
Line 507: would help the team learn how they’d approach the other task, which would al-
Line 508: low them to estimate it.
Line 509: Estimate Tasks
Line 510: The next step in velocity-driven iteration planning is to estimate each task. Some
Line 511: teams prefer to estimate tasks after all have been identified; other teams prefer to
Line 512: estimate tasks as each is identified. Task estimates are expressed in ideal time. So
Line 513: 
Line 514: --- 페이지 188 ---
Line 515: Estimate Tasks 
Line 516: |
Line 517: 157
Line 518: if I think that a task will take me six hours of working time, I give it an estimate
Line 519: of six hours. I do this even if six hours of time on the task will take me an entire
Line 520: eight-hour day.
Line 521: Although I agree with accepted advice that the best estimates come from
Line 522: those who will do the work (Lederer and Prasad 1992), I believe that task esti-
Line 523: mating on an agile project should be a group endeavor. There are four reasons
Line 524: for this.
Line 525: First, because tasks are not allocated to specific individuals during iteration
Line 526: planning, it is impossible to ask the specific person who will do the work. 
Line 527: Second, even though we expect a specific individual will be the one to do a
Line 528: task, and even though he may know the most about that task, it does not mean
Line 529: that others have nothing to contribute. Suppose during an iteration planning
Line 530: meeting, James says, “It will take me about two hours to program that—it’s triv-
Line 531: ial!” However, you remember that just last month James worked on a similar
Line 532: task and made a similar comment, and that it took him closer to sixteen hours.
Line 533: This time, when James says that a similar task is going to take only two hours,
Line 534: you might add, “But James, the last time you worked on a similar task, you
Line 535: thought it would be two hours, and it took you sixteen.” Most likely, James will
Line 536: respond with a legitimate reason why this case truly is different, or he’ll agree
Line 537: that there is some difficulty or extra work in this type of task that he has been
Line 538: systematically forgetting. 
Line 539: Third, hearing how long something is expected to take often helps teams
Line 540: identify misunderstandings about a user story or task. Upon hearing an unex-
Line 541: pectedly high estimate, a product owner or analyst may discover that the team is
Line 542: heading toward a more detailed solution than necessary. Because the estimate is
Line 543: discussed among the team, this can be corrected before any unneeded effort is
Line 544: expended.
Line 545: Finally, when the person who will do the work provides the estimate, the
Line 546: person’s pride and ego may make him reluctant to admit later that an estimate
Line 547: was incorrect. When an estimate is made collaboratively, this reluctance to ad-
Line 548: mit an estimate is wrong goes away.
Line 549: Some Design Is OK
Line 550: Naturally, it’s necessary for there to be some amount of design discussion while
Line 551: creating this list of tasks and estimates. We can’t create a list of tasks if we don’t
Line 552: have some idea of how we’re going to do the work. Fortunately, though, when
Line 553: planning an iteration, it isn’t necessary to go very far into the design of a feature.
Line 554: The product owner, analysts, and user interface designers may discuss
Line 555: product design, how much of a feature should be implemented, and how it will
Line 556: 
Line 557: --- 페이지 189 ---
Line 558: 158 |
Line 559: Chapter 14
Line 560: Iteration Planning
Line 561: appear to users. The developers may discuss options of how they will implement
Line 562: what is needed. Both types of design discussion are needed and appropriate.
Line 563: However, I’ve never been in an iteration planning meeting where it’s become
Line 564: necessary to draw a class diagram or similar model. A desire to do so is probably
Line 565: the best warning sign of taking the design too far during iteration planning. Save
Line 566: those discussions for outside iteration planning
Line 567: It’s not necessary to go so far as drawing a design, because all that’s neces-
Line 568: sary at this point are guesses about the work that will be needed to complete the
Line 569: features. If you get into the iteration and discover the tasks are wrong, get rid of
Line 570: the initial tasks and create new ones. If an estimate is wrong, cross it out and
Line 571: write a new value. Writing tasks and estimates on note cards is a great approach
Line 572: because each card carries with it a subtle reminder of impermanence.
Line 573: The Right Size for a Task
Line 574: The tasks you create should be of an approximate size so that each developer is
Line 575: able to finish an average of one per day. This size works well for allowing work to
Line 576: flow smoothly through your agile development process. Larger tasks tend to get
Line 577: bottled up with a developer or two, and the rest of the team can be left waiting
Line 578: for them to complete the task. Additionally, if the team is holding short daily
Line 579: meetings (Schwaber and Beedle 2002; Rising 2002), having tasks of this size al-
Line 580: lows each developer to report the completion of at least one task on most days.
Line 581: Naturally, there will often be tasks that are larger than this. But larger tasks
Line 582: should be generally understood to be placeholders for one or more additional
Line 583: tasks that will be added as soon as they are understood. If you need to create a
Line 584: sixteen-hour task during iteration planning, do so. However, once the task is
Line 585: more adequately understood, augment or replace it. This may mean replacing
Line 586: the initial card with more or less than the initially estimated sixteen hours. 
Line 587: Commitment-Driven Iteration Planning
Line 588: A commitment-driven approach is an alternative way to plan an iteration. Com-
Line 589: mitment-driven iteration planning involves many of the same steps as velocity-
Line 590: driven iteration planning. However, rather than creating an iteration plan that
Line 591: uses the yesterday’s weather idea to determine how many story points or ideal
Line 592: days should be planned into the current iteration, the team is asked to add
Line 593: stories to the iteration one by one until they can commit to completing no more.
Line 594: The overall commitment-driven approach is shown in Figure 14.3.
Line 595: 
Line 596: --- 페이지 190 ---
Line 597: Ask for a Team Commitment 
Line 598: |
Line 599: 159
Line 600: Figure 14.3 The activities of commitment-driven iteration planning.
Line 601: The first steps—adjusting priorities and identifying an iteration goal—are
Line 602: the same as in the velocity-driven approach. The next step, selecting a story to
Line 603: add to the iteration, is different. The product owner and team still select the
Line 604: highest-priority story that supports the iteration goal. However, in commit-
Line 605: ment-driven iteration planning, stories are selected and decomposed into tasks,
Line 606: and the tasks estimated one story at a time. This is different from the velocity-
Line 607: driven approach, in which a set of stories whose estimates equaled the estimated
Line 608: velocity were selected.
Line 609: Stories are selected one at a time because after each story is split into tasks
Line 610: and the tasks estimated, the team decides whether or not they can commit to de-
Line 611: livering that story during the iteration. 
Line 612: Ask for a Team Commitment
Line 613: In their study of what makes teams successful, Larson and LaFasto (1989) deter-
Line 614: mined that a unified commitment made by all team members is one of the key
Line 615: factors contributing to team success. During an iteration planning meeting, I
Line 616: ask the team, “Can you commit to delivering the features we’ve discussed?” No-
Line 617: tice that the question I ask is not “Can you commit to delivering the tasks we’ve
Line 618: identified?” That is a very different question and a far weaker commitment, be-
Line 619: cause it is a commitment to complete a set of tasks rather than a commitment to
Line 620: deliver new functionality.
Line 621: If new tasks are discovered during the iteration (and they almost certainly
Line 622: will be), a team that is committed to delivering the functionality described by a
Line 623: user story will try to complete the new tasks as well. A team that committed to
Line 624: Iteration
Line 625: planning
Line 626: is done 
Line 627: Ask for
Line 628: team
Line 629: commitment
Line 630: Remove a 
Line 631: user story 
Line 632: Select a 
Line 633: story to add
Line 634: Expand the
Line 635: story into 
Line 636: tasks
Line 637: Estimate
Line 638: tasks
Line 639: Adjust
Line 640: priorites
Line 641: Identify an
Line 642: iteration
Line 643: goal
Line 644: Can commit;
Line 645: not full
Line 646: Can commit;
Line 647: but full
Line 648: Cannot
Line 649: commit
Line 650: 
Line 651: --- 페이지 191 ---
Line 652: 160 |
Line 653: Chapter 14
Line 654: Iteration Planning
Line 655: only an identified list of tasks may not. In either case, it is possible that the newly
Line 656: discovered tasks will take long enough that they cannot be completed during the
Line 657: iteration. In that case, the team will need to discuss the situation with the prod-
Line 658: uct owner and see if there is still a way to meet the iteration goal; they may need
Line 659: to reduce the functionality of a story or drop one entirely.
Line 660: I ask a team if they can commit after each user story is split into tasks and
Line 661: the tasks are estimated. For the first user story, the question often seems silly.
Line 662: There may be seven people on the team, planning to work a two-week iteration.
Line 663: Perhaps they’ve identified only thirty-four hours of work so far, and I ask if they
Line 664: can commit to it. Their answer (either verbal or through the confused looks on
Line 665: their faces) is “Of course we can commit to this. There are seven of us for two
Line 666: weeks, and this is only thirty-four hours of work.” However, as the meeting
Line 667: progresses and as more user stories are brought into the iteration, the answer to
Line 668: my question, “Can you commit?” begins to require some thought. Eventually,
Line 669: we reach a point where the team cannot commit any further. If they cannot, they
Line 670: may choose to drop a story and replace it with a smaller one before finishing.
Line 671: Summing the Estimates
Line 672: The best way I’ve found for a team to determine whether they can commit to a
Line 673: set of user stories is to sum up the estimates given to the tasks and see if the sum
Line 674: represents a reasonable amount of work. There may very well be a large amount
Line 675: of uncertainty on some tasks, because the work hasn’t been designed and re-
Line 676: quirements are vague. However, summing the estimates still gives some indica-
Line 677: tion of the overall size of the work.
Line 678: Suppose a team of seven is working in two-week iterations. They have 560
Line 679: hours available each iteration (
Line 680: ). We know
Line 681: that some amount of time will be spent on activities that are not shown on task
Line 682: cards—answering email, participating in meetings, and so on. Similarly, we
Line 683: know the estimates are wrong; they are, after all, estimates, not guarantees. For
Line 684: these reasons, we cannot expect this team to sign up for 560 hours of tasks. In
Line 685: fact, most teams are successful when their planned work (the sum of their task
Line 686: cards) represents between four and six hours per day. For our team of seven peo-
Line 687: ple, working two-week iterations means they can probably plan between 280 and
Line 688: 420 hours. Where a given team will end up within this range is influenced by
Line 689: how well they identify the tasks for a given user story, how accurately those tasks
Line 690: are estimated, the amount of outside commitments by team members, and the
Line 691: amount of general corporate overhead for the team. After as few as a couple of
Line 692: iterations, most teams begin to get a feel for approximately how many hours
Line 693: they should plan for an iteration.
Line 694: 7 people
Line 695: 10 days
Line 696: u
Line 697: 8 hours per day
Line 698: u
Line 699: 
Line 700: --- 페이지 192 ---
Line 701: Ask for a Team Commitment 
Line 702: |
Line 703: 161
Line 704: Before committing to the work of an iteration, the team needs to look at the
Line 705: tasks and get a feel for whether they represent an appropriate distribution of
Line 706: work based on the various skills within the team. Is the Java programmer likely
Line 707: to be overloaded, while the HTML programmer has nothing to do this iteration?
Line 708: Are the selected user stories easy to program but time-consuming or difficult to
Line 709: test, thereby overloading the tester? Do the stories selected each need analysis
Line 710: and user interaction design before coding can begin?
Line 711: A team in a situation like this should first try to find ways to better share
Line 712: work. Can the HTML programmer in this example help the tester? Can someone
Line 713: other than the user interaction designer do that work? If not, can we leave out of
Line 714: this iteration some stories that need user interaction design, and can we bring in
Line 715: some other stories that do not? The key is that everyone on the team is account-
Line 716: able for contributing whatever is within their capabilities, regardless of whether
Line 717: it is their specialty.
Line 718: Maintenance and the Commitment
Line 719: In addition to making progress on a project, many teams are responsible for sup-
Line 720: port and maintenance of another system. It may be a prior version of the product
Line 721: they are working on, or it may be an unrelated system. When a team makes a
Line 722: commitment to complete a set of stories during an iteration, they need to do so
Line 723: with their maintenance and support load in mind. I am not referring to general
Line 724: bug fixes that can be prioritized in advance. Those should go through the regular
Line 725: iteration planning prioritization process. By maintenance and support activities,
Line 726: I mean those unpredictable but required parts of many teams’ lives—supporting
Line 727: a production website or database, taking support calls from key customers or
Line 728: first-tier technical support, and so on.
Line 729: Individual Commitments
Line 730: When assessing the ability to commit to completing a set of new func-
Line 731: tionality, some teams prefer to allocate each task to a specific person and
Line 732: then assess whether each individual is able to commit to that amount of
Line 733: work. This approach works well, and I’ve recommended it in the past
Line 734: (Cohn 2004). However, I’ve found that by not allocating tasks while plan-
Line 735: ning the iteration and not doing the personal math needed to make in-
Line 736: dividual commitments, the team benefits from the creation of a “we’re
Line 737: all in this together” mindset.
Line 738: If you do find a need to allocate tasks to individuals while planning an
Line 739: iteration, the allocations should be considered temporary and subject to
Line 740: change once the iteration is under way.
Line 741: 
Line 742: --- 페이지 193 ---
Line 743: 162 |
Line 744: Chapter 14
Line 745: Iteration Planning
Line 746: I think of an iteration as an empty glass. The first things poured into the
Line 747: glass are the team’s unchangeable commitments, such as support and mainte-
Line 748: nance of other products. Whatever room remains in the glass is available for the
Line 749: team when they commit to the work of an iteration. This is shown in
Line 750: Figure 14.4. Clearly, a team whose glass is 10% full with support work will have
Line 751: time to commit to more other work than will a team whose glass starts 90% full.
Line 752: Figure 14.4 Other commitments determine how much a team can commit to during 
Line 753: an iteration.
Line 754: In most situations, the team will not be able to predict their upcoming sup-
Line 755: port load very accurately. They should know a long-term average, but averaging
Line 756: twenty hours of support per week is not the same as having twenty hours every
Line 757: week. If the support and maintenance load exceeds expectations during an itera-
Line 758: tion, they may not be able to meet their commitment. They need to counter this
Line 759: by trying to exceed their commitment when the support and maintenance load
Line 760: is less than expected in some iterations. This variability is inescapable on teams
Line 761: with significant support and maintenance obligations.
Line 762: My Recommendation
Line 763: Both velocity-driven and commitment-driven iteration planning are viable ap-
Line 764: proaches; however, my preference is for the commitment-driven approach. Al-
Line 765: though velocity plays a critical role in release planning, I do not think it should
Line 766: play an equivalent role in iteration planning. There are two reasons for this.
Line 767: First, because velocity is a measure of coarse-grained estimates (story points
Line 768: or ideal days), it is not accurate enough for planning the work of short iterations.
Line 769: We can use these coarse-grained estimates for estimating the overall amount of
Line 770: The commitment to work
Line 771: for the iteration is based
Line 772: on how much room is left.
Line 773: Support, maintenance,
Line 774: and other commitments
Line 775: 
Line 776: --- 페이지 194 ---
Line 777: Relating Task Estimates to Story Points 
Line 778: |
Line 779: 163
Line 780: work a team will complete during an iteration. We cannot, however, use them in
Line 781: the same way for planning the shorter-term work of a single iteration.
Line 782: Second, a team would need to complete twenty to thirty user stories per it-
Line 783: eration for errors in the story-point or ideal-day estimates to average out. Very
Line 784: few teams complete this many stories in an iteration.
Line 785: To see the result of these problems, suppose a team has had a velocity of
Line 786: thirty in each of the past five iterations. That’s about as consistent as it gets, and
Line 787: it’s likely they’ll complete thirty points again in the coming iteration. However,
Line 788: we know that not all five-point stories are the same. If we were to sort through a
Line 789: large collection of five-point stories, we know we could identify six five-point
Line 790: stories that all looked slightly easier than five points. We might be wrong on
Line 791: some, but if this was the first time we tried this, we’d probably succeed. We
Line 792: might increase our velocity from thirty to forty. On the other hand, we could in-
Line 793: stead select only the five-point stories that seem slightly harder. We still think
Line 794: they should be estimated at five points, but they are slightly harder than the
Line 795: other five-point stories. 
Line 796: On a project, we’re not going to dig through our collection of user stories
Line 797: and try to find the “easy fives” or the “hard fives.” However, most teams plan be-
Line 798: tween three and a dozen stories into each iteration. When pulling that few
Line 799: stories into an iteration, a team will certainly get lucky and select all slightly
Line 800: easy ones or unlucky and select all slightly harder ones occasionally.
Line 801: Because too few stories are completed in a single iteration for these to aver-
Line 802: age out, I prefer not to use velocity when planning an iteration. However, be-
Line 803: cause these differences do average out over the course of a release, velocity
Line 804: works extremely well for release planning.
Line 805: Relating Task Estimates to Story Points
Line 806: I’m often asked to explain the relationship between task estimates used during
Line 807: iteration planning and the story points or ideal days used for longer-range re-
Line 808: lease planning. I see teams go astray when they start to believe there is a strong
Line 809: relationship between a story point and an exact number of hours. For example, I
Line 810: helped a team recently that had tracked their actual number of productive hours
Line 811: per iteration and their velocity per iteration. From this, they calculated that each
Line 812: story point took approximately twelve hours of work. Their view became the mis-
Line 813: taken certainty that each story point always equaled twelve hours of work. How-
Line 814: ever, the real case was something closer to that shown in Figure 14.5.
Line 815: 
Line 816: --- 페이지 195 ---
Line 817: 164 |
Line 818: Chapter 14
Line 819: Iteration Planning
Line 820: Figure 14.5 shows that on average, it will take twelve hours to complete a
Line 821: one-point user story. However, it also shows that some one-point stories will take
Line 822: less, and some will take more. Until the team estimates a story’s underlying
Line 823: tasks, it is hard to know where a particular story lies on a curve such as this.
Line 824: Figure 14.5 Distribution of the time needed to complete a one-point user story.
Line 825: Although Figure 14.5 shows the distribution of hours for a one-point user
Line 826: story, Figure 14.6 shows the hypothetical distributions for one-, two-, and three-
Line 827: point stories. In this figure, each story point is still equivalent to twelve hours on
Line 828: average. However, it is possible that some one-point stories will take longer than
Line 829: some two-point stories. 
Line 830: Figure 14.6 Distribution of times to complete one-, two-, and three-point stories.
Line 831: Hours
Line 832: 12
Line 833: Probability of completion
Line 834: Hours
Line 835: 12
Line 836: 24
Line 837: 36
Line 838: 1-point story
Line 839: 2-point story
Line 840: 3-point story
Line 841: Probability of completion
Line 842: 
Line 843: --- 페이지 196 ---
Line 844: Summary 
Line 845: |
Line 846: 165
Line 847: That some two-point stories will take less time to develop than some one-
Line 848: point stories is entirely reasonable and to be expected. It is not a problem as long
Line 849: as there are sufficient stories in the release for these outliers to average out, and
Line 850: as long as everyone on the project remembers that some stories will take longer
Line 851: than others, even though their initial, high-level estimates were the same.
Line 852: Summary
Line 853: Unlike a release plan, an iteration plan looks in more detail at the specific work
Line 854: of a single iteration. Rather than the three-to-nine month horizon of a typical re-
Line 855: lease plan, the iteration plan looks out no further than a single iteration. The
Line 856: fairly large user stories of a release plan are decomposed into tasks on the itera-
Line 857: tion plan. Each task is estimated in terms of the number of ideal hours the task
Line 858: will take to complete.
Line 859: Days of the Week
Line 860: When I started managing agile projects, my teams routinely started their
Line 861: iterations on a Monday and ended them on a Friday. We’d do this
Line 862: whether the specific team was using two-, three-, or four-week itera-
Line 863: tions. Mondays seemed like a natural day to begin an iteration, and Fri-
Line 864: days were an obvious day to end on. I changed my mind about this after
Line 865: I began coaching a team that was developing a website that was busy
Line 866: during the week and barely used on the weekend. 
Line 867: The most logical night for this team to deploy new web updates was
Line 868: Friday evening. If something went wrong, they could fix it over the
Line 869: weekend, and the impact would be minimal because the site was very
Line 870: lightly used during that time. To accommodate this, this team decided to
Line 871: run two-week iterations that would start on a Friday and end on a Thurs-
Line 872: day. This worked wonderfully. Fridays were spent doing an iteration re-
Line 873: view and in planning the next iteration. This took until midafternoon
Line 874: most Fridays, after which the team would either get started on the work
Line 875: of the new iteration or occasionally head out for drinks or bowling. The
Line 876: iteration would start in earnest the following Monday. This was great be-
Line 877: cause there was no dread of a Monday filled with meetings, as there was
Line 878: when Monday was review and planning day.
Line 879: The team also benefited by occasionally using Friday morning to wrap
Line 880: up any last-minute work they’d been unable to finish on Thursday. They
Line 881: didn’t make a habit of this, and it happened only a few times; however,
Line 882: spending a few hours on a Friday morning wrapping things up was pref-
Line 883: erable to coming in over the weekend (as they would have done with a
Line 884: Monday iteration start).
Line 885: 
Line 886: --- 페이지 197 ---
Line 887: 166 |
Line 888: Chapter 14
Line 889: Iteration Planning
Line 890: There are two general approaches to planning an iteration: velocity-driven
Line 891: and commitment-driven. The two approaches share many steps and often result
Line 892: in the creation of the same iteration plan. 
Line 893: Discussion Questions
Line 894: 1. Which approach to iteration planning do you prefer: velocity-driven or com-
Line 895: mitment-driven? Why?
Line 896: 2. What do you think of not having team members sign up for specific tasks
Line 897: during iteration planning?
Line 1: 
Line 2: --- 페이지 246 ---
Line 3: 215
Line 4: Chapter 19
Line 5: Monitoring the Release Plan
Line 6: “The stars might lie, but the numbers never do.”
Line 7: —Mary Chapin Carpenter, “I Feel Lucky”
Line 8: Ancient sailors had two problems. First, they had to know their latitude—that is,
Line 9: their north-south position on a map. Second, they had to know their longitude,
Line 10: or east-west position. Determining latitude by observing the North Star was rel-
Line 11: atively easy and had been done as early as 300 BC. Longitude presented a more
Line 12: difficult problem because it relied on the use of a relatively accurate clock, or
Line 13: chronometer. Unfortunately, there were no sufficiently accurate chronometers
Line 14: (especially that would fit and work aboard a ship) until the early eighteenth
Line 15: century. 
Line 16: Before the invention of the chronometer, a sailor could only guess at his lon-
Line 17: gitude. To make these guesses, sailors applied a series of guesses and adjust-
Line 18: ments known as dead reckoning, which is generally considered to be short for
Line 19: deduced reckoning. Dead reckoning involved guessing how far east or west a
Line 20: ship had sailed and then adjusting that guess by guesses at the impact of the
Line 21: wind and the drift of the sea. Suppose that the speedometer on your yacht says
Line 22: you are traveling eight miles per hour. However, if you are heading into waves,
Line 23: wind, and current you may be making only five miles per hour of progress. Your
Line 24: dead reckoning guesses would need to reflect all of this, or you would incorrectly
Line 25: estimate your longitude.
Line 26: Tracking the progress of a software team is very similar to charting a ship’s
Line 27: position, especially by dead reckoning. We would like to sail our software
Line 28: 
Line 29: --- 페이지 247 ---
Line 30: 216 |
Line 31: Chapter 19
Line 32: Monitoring the Release Plan
Line 33: development project in a straight line from Point A to Point B. This rarely hap-
Line 34: pens, though, because requirements change or are refined, our rate of progress
Line 35: isn’t always what we expect, and we sometimes make mistakes in how we mea-
Line 36: sure our position. The sections of this chapter describe techniques for tracking
Line 37: progress that are designed to minimize the effect of these and similar problems.
Line 38: Tracking the Release
Line 39: At the start of a release, we establish a plan that says something like “Over the
Line 40: next four months and eight two-week iterations we will complete approximately
Line 41: 240 story points [or ideal days] of work.” As we learn more about our users’ true
Line 42: needs and about the size of the project, this estimate may change. However, at
Line 43: any point we would like to be able to assess where we are relative to the goal of
Line 44: completing a certain amount of work in a given amount of time.
Line 45: In doing so, there are many forces at work, and each needs to be considered.
Line 46: First, and ideally most significant, is the amount of progress made by the team.
Line 47: Second, however, is any change in the scope of the project. The product owner
Line 48: may have added or removed requirements. If the product owner adds forty story
Line 49: points and the team completes thirty, the team has more work to complete than
Line 50: when they started the prior iteration. The target has shifted, and it will be useful
Line 51: to know how far away the team is from the new target. Similarly, the developers
Line 52: may have learned things during the iteration that make them want to revise the
Line 53: story-point estimates assigned to some of the work coming later in the release
Line 54: plan. 
Line 55: These forces (completed work, changed requirements, and revised esti-
Line 56: mates) can be thought of as being similar to the forces of the wind (called lee-
Line 57: way) and the forces of the sea (called drift) on a boat. Consider Figure 19.1,
Line 58: which shows the forces at work on a boat. The boat shown in this diagram will
Line 59: travel less distance than would be inferred from its speedometer. Similarly, even
Line 60: though the boat’s compass pointed due east for its entire voyage, the wind will
Line 61: have caused it to make leeway to the south. Without course adjustments, this
Line 62: boat will take longer to get somewhere not quite its original destination. Men-
Line 63: tally relabel the arrows of Figure 19.1 so that drift and leeway become require-
Line 64: ments changes (adding or removing functionality) and changes to estimates.
Line 65: Figure 19.1 then reflects the challenges of tracking the progress of a software
Line 66: project against its schedule.
Line 67: 
Line 68: --- 페이지 248 ---
Line 69: Velocity 
Line 70: |
Line 71: 217
Line 72: Figure 19.1 The forces at work on a boat.
Line 73: Velocity
Line 74: A boat measures its rate of progress in knots; an agile team measures its rate of
Line 75: progress with velocity. Velocity is expressed as the number of story points (or
Line 76: ideal days) completed per iteration. For a team that finished twelve stories worth
Line 77: a total of thirty story points in their last iteration, we say that their velocity is
Line 78: “thirty” or “thirty points per iteration.” Assuming that the scope of the project
Line 79: hasn’t changed, the team has that much less work to complete. 
Line 80: Because velocity is the primary measure of a team’s progress, it is important
Line 81: to establish some ground rules for how it is calculated. The most important rule
Line 82: is that a team counts points toward velocity only for stories or features that are
Line 83: complete at the end of the iteration. Complete doesn’t mean something like “The
Line 84: coding is done, but it hasn’t been tested” or “It’s coded but needs to be inte-
Line 85: grated.” Complete means code that is well written, well factored, checked-in, and
Line 86: clean; complies with coding standards; and passes all tests. To know how much
Line 87: progress has been made, we count only the points for work that is complete.
Line 88: Opening the door to counting partially finished work, perhaps giving partial
Line 89: credit, makes it impossible to know exactly where we are. 
Line 90: There are three main problems with counting unfinished work. First, it is
Line 91: extremely hard to measure unfinished or incomplete work. Which is further
Line 92: along: A user story that has been programmed but has had no tests run against it
Line 93: or a story that has been partially programmed and partially tested? How far
Line 94: along is a programmer who has designed a solution for a story but hasn’t started
Line 95: coding it? We’re good at knowing when something hasn’t been started, and we’re
Line 96: Wind (leeway)
Line 97: Progress
Line 98: Current (drift)
Line 99: 
Line 100: --- 페이지 249 ---
Line 101: 218 |
Line 102: Chapter 19
Line 103: Monitoring the Release Plan
Line 104: fairly good at knowing when it’s done. We should assess work to be in one of
Line 105: those two states and leave it at that.
Line 106: Second, incomplete stories break down the trust between the developer
Line 107: team and the customer team on the project. If a story cannot be completed as
Line 108: planned during an iteration, the developers and the customer team need to col-
Line 109: laboratively resolve the issue as soon as it’s discovered. Usually, this means the
Line 110: story will be moved out of the iteration or split and parts of it moved out. The
Line 111: product owner and customer team can make these decisions in real time during
Line 112: the iteration and may choose to reprioritize based on the new knowledge about
Line 113: the cost of the story. Alternatively, the customer team may decide to alter the ac-
Line 114: ceptance criteria for the story, accepting it under lessened criteria. They
Line 115: wouldn’t go so far as to accept a buggy or untested version of the story, but they
Line 116: may reduce performance requirements, handling of special cases, and so on. 
Line 117: Third, and most important, unfinished work leads to a buildup of work in
Line 118: process in the development process. The more work in process a team allows to
Line 119: build up, the longer it will take new features to be transformed from raw ideas
Line 120: into functioning software. Over time, this will decrease the throughput of the
Line 121: whole team. Similarly, with large amounts of work in process, it takes longer for
Line 122: the team to get feedback on what they’re developing. This means that learning is
Line 123: also delayed.
Line 124: If a team has unfinished stories at the end of an iteration, they are working
Line 125: with features or stories that are too large. Small stories lead to a steady flow
Line 126: through the development process. If stories are left unfinished, they need to be
Line 127: split into smaller stories. Ideally, this should happen prior to the start of the iter-
Line 128: ation. However, if during an iteration a story is found to be larger than expected,
Line 129: it needs to be brought to the attention of the product owner. The product owner,
Line 130: in collaboration with the team, finds a way to split the story or reduce its scope
Line 131: such that a portion can ideally still be completed within the iteration, with the
Line 132: remainder moved to a future iteration.
Line 133: So how should a team count a partially finished story when determining ve-
Line 134: locity? How they count such a story is less important than that they determine
Line 135: why it happened and how they can prevent it from happening again. It may have
Line 136: happened because it was underestimated. If so, the team should think about
Line 137: what type of work was underestimated or forgotten and try to remember to take
Line 138: care when estimating that type of work in the future. Or the story may have been
Line 139: unfinished because too many stories were pulled into the current iteration. If
Line 140: that was the cause, care should be taken to plan iterations more carefully.
Line 141: 
Line 142: --- 페이지 250 ---
Line 143: Release Burndown Charts 
Line 144: |
Line 145: 219
Line 146: Release Burndown Charts
Line 147: Figure 19.2 shows a release burndown chart (Schwaber and Beedle 2002). The
Line 148: vertical axis shows the number of story points remaining in the project. (It could
Line 149: just as easily show the number of ideal days remaining.) Iterations are shown
Line 150: across the horizontal axis. A release burndown chart shows the amount of work
Line 151: remaining at the start of each iteration. This becomes a powerful visual indicator
Line 152: of how quickly a team is moving toward its goal. Figure 19.2 shows a hypotheti-
Line 153: cal burndown for a project with 240 story points delivered in equal amounts over
Line 154: eight iterations.
Line 155: .
Line 156: Figure 19.2 A 240-point project completed in eight iterations.
Line 157: Of course, it’s unlikely that a team that expects to have a velocity of thirty
Line 158: will have that exact velocity in each iteration. A more likely burndown chart of
Line 159: the 240-point release might appear as in Figure 19.3.
Line 160: Figure 19.3 shows a team’s progress after three iterations. Their progress
Line 161: has been inconsistent. During the first iteration they completed what appears to
Line 162: be about the planned thirty points of work. But at the end of the second iteration
Line 163: they actually had more work left to do than when they’d started that iteration.
Line 164: This could happen if, for example, the team realized that developing the user in-
Line 165: terface would be much more involved than they’d initially estimated and in-
Line 166: creased their estimates for all remaining user interface stories. 
Line 167: 50
Line 168: 100
Line 169: 150
Line 170: 200
Line 171: 250
Line 172: 0
Line 173: Iterations
Line 174: Points
Line 175: 1
Line 176: 2
Line 177: 3
Line 178: 4
Line 179: 5
Line 180: 6
Line 181: 7
Line 182: 8
Line 183: 
Line 184: --- 페이지 251 ---
Line 185: 220 |
Line 186: Chapter 19
Line 187: Monitoring the Release Plan
Line 188: Figure 19.3 A more realistic burndown on a 240-point project after the third 
Line 189: iteration.
Line 190: Alternatively, the burndown chart may show a burnup because work has
Line 191: been added to the release. Think of this as equivalent to a sailboat making 8
Line 192: miles per hour of progress but sailing directly into a current running 12 miles
Line 193: per hour in the opposite direction. In the sailboat’s case, it ends up farther away
Line 194: from its initial target. However, in the case of the software project, the added
Line 195: work may be the result of the team’s having learned something that directs them
Line 196: toward a more valuable release.
Line 197: To see how this works, suppose that in the second iteration the team again
Line 198: completed the planned thirty points of work but that the product owner identi-
Line 199: fied another forty points of work that is needed in the release. In this case, the
Line 200: net result is that there is more work to do at the end of the iteration than there
Line 201: was when it began. Because a burndown chart reflects the team’s net progress,
Line 202: the chart is drawn to reflect this increase.
Line 203: You may wonder why we’d draw the chart this way. We draw it this way be-
Line 204: cause it allows a single burndown chart to show clearly and simply the two most
Line 205: important numbers we can use to see if a project is on track: how much work is
Line 206: remaining and the team’s rate of progress net of all changes to the scope of the
Line 207: project. Imagine that you are on the team whose progress is shown in
Line 208: Figure 19.3. At the end of the third iteration, you are asked if the release will be
Line 209: 50
Line 210: 100
Line 211: 150
Line 212: 200
Line 213: 250
Line 214: 0
Line 215: Iterations
Line 216: Points
Line 217: 1
Line 218: 2
Line 219: 3
Line 220: 4
Line 221: 5
Line 222: 6
Line 223: 7
Line 224: 8
Line 225: 
Line 226: --- 페이지 252 ---
Line 227: A Release Burndown Bar Chart 
Line 228: |
Line 229: 221
Line 230: finished within the planned eight iterations. And if it won’t be, you are asked to
Line 231: provide a better estimate of when it will be finished. You can answer this ques-
Line 232: tion just by looking at the burndown chart in Figure 19.3. Simply line up a
Line 233: straight edge between the 240 points on the vertical axis and the number of
Line 234: points currently remaining in the project. Where the straight edge intersects the
Line 235: horizontal axis is when you can expect the project to finish. A casual look at
Line 236: Figure 19.3 tells you enough to know it won’t finish in the planned eight itera-
Line 237: tions.
Line 238: A Release Burndown Bar Chart
Line 239: At one level, the release burndown chart of Figure 19.3 is great. It’s easy to un-
Line 240: derstand and can be explained quickly to anyone in the organization. A release
Line 241: burndown chart like this is very informative and tells us when the project is
Line 242: likely to finish if all factors affecting the project remain unchanged. However,
Line 243: sometimes it’s useful to draw the release burndown chart so that you can easily
Line 244: see the team’s velocity and the scope changes separately. To do this, draw a re-
Line 245: lease burndown bar chart like the one shown in Figure 19.4.
Line 246: Figure 19.4 Separating the impact of velocity and scope changes.
Line 247: Each bar in Figure 19.4 shows the amount of work in a release as of the start
Line 248: of an iteration. This type of burndown chart uses bars rather than lines to help
Line 249: 0
Line 250: Iterations
Line 251: 50
Line 252: 100
Line 253: 150
Line 254: 200
Line 255: 250
Line 256: Points
Line 257: -50
Line 258: 
Line 259: --- 페이지 253 ---
Line 260: 222 |
Line 261: Chapter 19
Line 262: Monitoring the Release Plan
Line 263: distinguish the regions above and below the horizontal axis at 0. The bottom of
Line 264: the bar is lowered whenever work is added to the project. The bottom is moved
Line 265: up whenever work is removed from an iteration. If the bottom is below the hori-
Line 266: zontal axis at 0, it means that overall work has been added to the release.
Line 267: An example is the best way to see how this works. In Figure 19.4, a release is
Line 268: planned to include 240 points of work. At the start of the first iteration the burn-
Line 269: down chart is drawn with a single bar extending from 0 to 240. As before, the
Line 270: team expects an average velocity of thirty and expects to be done after eight iter-
Line 271: ations. During the first iteration, the team achieves the expected velocity, and
Line 272: the top of the second bar is drawn at 210. However, the product owner has real-
Line 273: ized that the release needs more features than originally thought. An additional
Line 274: fifty story points of work is identified that will be needed in this release. This
Line 275: causes the bar for the second iteration to extend below the 0 line. The second bar
Line 276: is drawn ranging from –50 to 210. In other words, the release now needs 260
Line 277: points of work, which is more than when it was begun. By the end of the second
Line 278: iteration Figure 19.4 reveals three interesting facts.
Line 279: 1. The velocity of the team is as expected. This can be seen from the burndown
Line 280: across the top of the first two bars.
Line 281: 2. A great deal of work has been added. You can see this from the drop at the
Line 282: bottom of the second bar. Presumably, work has been added because it will
Line 283: lead to a more valuable release. However, it may be worth paying attention
Line 284: to the rate of scope change on this project—so far, more has been added
Line 285: than has been completed. This may not be something to worry about; it will
Line 286: depend on whether the trend is likely to continue and how important the
Line 287: initial target release date is.
Line 288: 3. The total amount of work remaining in the release is greater than when the
Line 289: project started. This is evident because the overall height of the second bar is
Line 290: greater than the first. 
Line 291: Clearly, there is a great deal more expressive power in drawing a burndown
Line 292: chart in this way. The drawback to it is that the meaning of the chart is not as
Line 293: immediately clear. 
Line 294: Let’s look at the second and third iterations of the project in Figure 19.4.
Line 295: During the second iteration the team again achieves their target velocity. The
Line 296: product owner has again added work, but at least less was added than during the
Line 297: previous iteration.
Line 298: But what happened during the third iteration? During this iteration, veloc-
Line 299: ity has slowed to only twenty. This may be the result of underestimating some
Line 300: 
Line 301: --- 페이지 254 ---
Line 302: A Release Burndown Bar Chart 
Line 303: |
Line 304: 223
Line 305: stories done in that iteration, a team member’s being sick or on vacation, or the
Line 306: re-estimation of some of the remaining work. The team may have completed
Line 307: their planned thirty points of work but may have increased estimates on some
Line 308: remaining stories such that net progress is twenty rather than thirty. 
Line 309: What is most interesting, however, about the third iteration is shown at the
Line 310: bottom of the the fourth bar. During this iteration, the product owner removed
Line 311: features from the release. When it’s released, this project will still involve more
Line 312: story points than initially planned. We can tell this because the bar still extends
Line 313: below the x-axis at 0. However, at this point the project contains fewer planned
Line 314: points than it did at the start of the previous iteration. It’s not important
Line 315: whether the features removed were ones in the original release plan or ones the
Line 316: product owner added in previous iterations. Prioritzation of work is still up to
Line 317: the product owner, who can add or remove functionality as desired. The net ef-
Line 318: fect is shown at the bottom of the burndown bar.
Line 319: There are four simple rules to keep in mind when drawing this type of burn-
Line 320: down chart.
Line 321: ◆Any time work is completed, the top is lowered.
Line 322: ◆When work is re-estimated, the top moves up or down.
Line 323: ◆When new work is added, the bottom is lowered.
Line 324: ◆When work is removed, the bottom is raised.
Line 325: Let’s take a look at a release burndown bar chart from a real project, as
Line 326: shown in Figure 19.5. What we see here is that the team made good progress
Line 327: during the first two iterations. The product owner added a small amount of work
Line 328: prior to the start of the second iteration, which is a fairly common occurrence
Line 329: on many teams. During the third iteration, the team discovered that some of
Line 330: their user stories were underestimated, and they re-estimated some of the re-
Line 331: maining work. This led to the increase at the top of the fourth bar in Figure 19.5.
Line 332: Prior to the start of the fourth iteration, the product owner removed work from
Line 333: the release plan. This resulted in the bottom moving upward, even above the 0
Line 334: line. During that iteration, the team made good progress. From that point on,
Line 335: the release plan stayed the same, and consistent progress was made until the
Line 336: end.
Line 337: 
Line 338: --- 페이지 255 ---
Line 339: 224 |
Line 340: Chapter 19
Line 341: Monitoring the Release Plan
Line 342: Figure 19.5 Removing work from a release.
Line 343: A Parking-Lot Chart
Line 344: Jeff DeLuca (2002) has suggested another useful way of visualizing how a team is
Line 345: doing at completing the planned functionality of a release. Figure 19.6 shows a
Line 346: variation of what DeLuca calls a parking-lot chart. A parking-lot chart contains
Line 347: a large rectangular box for each theme (or grouping of user stories) in a release.
Line 348: Each box is annotated with the name of the them, the number of stories in that
Line 349: theme, the number of story points or ideal days for those stories, and the per-
Line 350: centage of the story points that are complete.
Line 351: A Caveat on Using the Release Burndown Bar Chart
Line 352: Although I find the release burndown bar chart more expressive (and,
Line 353: therefore, often more useful) than the traditional burndown chart, I do
Line 354: have a couple of caveats on its use. First, the burndown bar chart is
Line 355: harder to understand, so I almost always start a new team with the sim-
Line 356: pler burndown line chart. Second, the burndown bar chart is for use only
Line 357: in organizations mature enough not to argue about whether something
Line 358: belongs above the line or below the line. At the first sign of an argument
Line 359: of this nature, I tell everyone involved that we can’t use the burndown
Line 360: bar chart and we’re reverting to the line chart.
Line 361: 25
Line 362: 50
Line 363: 75
Line 364: 100
Line 365: 125
Line 366: 0
Line 367: Iterations
Line 368: –25
Line 369: Points
Line 370: 
Line 371: --- 페이지 256 ---
Line 372: Summary 
Line 373: |
Line 374: 225
Line 375: Figure 19.6 A parking-lot chart shows how much of each theme has been 
Line 376: completed.
Line 377: In the Swimmer Demographics box of Figure 19.6 you can see that this
Line 378: theme comprises eight stories, which are estimated at an aggregate of thirty-six
Line 379: story points. Eighteen of these story points are done, because we know that 50%
Line 380: of the feature is complete. We cannot tell how many of the specific user stories
Line 381: are done. The individual boxes on a parking lot chart may even be colored to in-
Line 382: dicate whether a theme is done or on schedule, needs attention or is significantly
Line 383: behind schedule.
Line 384: A parking-lot chart is a powerful method for compressing a great deal of in-
Line 385: formation into a small space. In many cases, all of a release’s themes can be sum-
Line 386: marized on one page using a parking-lot diagram.
Line 387: Summary
Line 388: Velocity measures the amount of work completed by a team each iteration. Ve-
Line 389: locity should be calculated using an all-or-nothing rule. If a story is finished, the
Line 390: team counts its full estimate when counting velocity. If a story is partially com-
Line 391: pleted during an iteration, it is not counted at all when determining velocity.
Line 392: A release burndown chart shows the number of story points or ideal days re-
Line 393: maining in the project as of the start of each iteration. A team’s burndown is
Line 394: never perfectly smooth. It will vary because of inaccurate estimates, changed es-
Line 395: timates, and changes in scope, for example. A burndown chart may even show a
Line 396: burnup during an iteration. This means that even though the team probably
Line 397: completed some work, they either realized that the remaining work was under-
Line 398: estimated or increased the scope of the project. A key to interpreting a release
Line 399: burndown chart is understanding that it shows the team’s net progress—that is,
Line 400: their progress minus any work added to the release.
Line 401: Swimmer
Line 402: Demographics
Line 403: 8 stories
Line 404: 36 story points
Line 405: 50%
Line 406: Reporting
Line 407: 12 stories
Line 408: 41 story points
Line 409: 100%
Line 410: Security
Line 411: 4 stories
Line 412: 18 story points
Line 413: 33%
Line 414: 
Line 415: --- 페이지 257 ---
Line 416: 226 |
Line 417: Chapter 19
Line 418: Monitoring the Release Plan
Line 419: A release burndown bar chart offers a sometimes-useful variation on the
Line 420: standard release burndown chart. It does so by separating a team’s progress
Line 421: against planned work and changes to the scope of the release. Scope changes are
Line 422: shown by dropping the bar below the horizontal axis. This type of chart is more
Line 423: expressive than a standard burndown chart but must be used with care, as it may
Line 424: cause arguments in some organizations about whether a change affects the top
Line 425: or the bottom of a bar in the chart.
Line 426: A parking-lot chart is useful for presenting a high-level view of a team’s
Line 427: progress toward implementing the various themes planned in a project.
Line 428: Discussion Questions
Line 429: 1. If you are not using a release burndown chart on your current project, what
Line 430: would be the result of producing one at the end of each iteration?
Line 431: 2. Which of the progress monitoring and reporting techniques described in
Line 432: this chapter would be most beneficial to your current project?
Line 433: 3. Which stakeholders on your project are not receiving information about the
Line 434: project that they would find useful?
Line 1: 
Line 2: --- 페이지 80 ---
Line 3: 49
Line 4: Chapter 6
Line 5: Techniques for Estimating
Line 6: “Prediction is very difficult,
Line 7: especially about the future.”
Line 8: —Niels Bohr, Danish physicist
Line 9: The more effort we put into something, the better the result. Right? Perhaps, but
Line 10: we often need to expend just a fraction of that effort to get adequate results. For
Line 11: example, my car is dirty, and I need to wash it. If I wash it myself, I’ll spend about
Line 12: an hour on it, which will be enough to wash the exterior, vacuum the interior,
Line 13: and clean the windows. For a one-hour investment, I’ll have a fairly clean car.
Line 14: On the other hand, I could call a car-detailing service and have them wash
Line 15: my car. They’ll spend four hours on it. They do everything I do but much more
Line 16: thoroughly. They’ll also wax the car, shine the dashboard, and so on. I watched
Line 17: one time, and they used tiny cotton swabs to clean out the little places too small
Line 18: to reach with a rag. That’s a lot of effort for slightly better results. For me, the
Line 19: law of diminishing returns kicks in well before I’ll use a cotton swab on my car. 
Line 20: We want to remain aware, too, of the diminishing return on time spent esti-
Line 21: mating. We can often spend a little time thinking about an estimate and come up
Line 22: with a number that is nearly as good as if we had spent a lot of time thinking
Line 23: about it. The relationship between estimate accuracy and effort is shown in
Line 24: Figure 6.1. The curve in this graph is placed according to my experience, corrob-
Line 25: orated in discussions with others. It is not based on empirical measurement.
Line 26: 
Line 27: --- 페이지 81 ---
Line 28: 50
Line 29: |
Line 30: Chapter 6
Line 31: Techniques for Estimating
Line 32: Figure 6.1 Additional estimation effort yields very little value beyond a certain point.
Line 33: To understand this relationship better, suppose you decide to estimate how
Line 34: many cookies I’ve eaten in the past year. You could put no effort into the esti-
Line 35: mate and just take a random guess. Mapping this onto Figure 6.1, you’d be com-
Line 36: pletely to the left on the effort axis, and your estimate would be unlikely to be
Line 37: accurate. You could move to the right on the effort axis by spending a half-hour
Line 38: or so researching national averages for cookie consumption. This would improve
Line 39: your accuracy over the pure guess. If you felt the need to be more accurate, you
Line 40: could do some research—call my friends and family, subpoena my past cookie
Line 41: orders from the Girl Scouts, and so on. You could even follow me around for a
Line 42: day—or, better yet, a month—and then extrapolate your observations into how
Line 43: many cookies you think I eat in a year.
Line 44: Vary the effort you put into estimating according to purpose of the estimate.
Line 45: If you are trying to decide whether or not to send me a box of cookies as a gift,
Line 46: you do not need a very accurate estimate. If the estimate will be used to make a
Line 47: software build versus buy decision, it is likely enough to determine that the
Line 48: project will take six to twelve months. It may be unnecessary to refine that to the
Line 49: point where you can say it will take seven or eight months.
Line 50: Look carefully at Figure 6.1, and notice a couple of things. First, no matter
Line 51: how much effort is invested, the estimate is never at the top of the accuracy axis.
Line 52: No matter how much effort you put into an estimate, an estimate is still an esti-
Line 53: mate. No amount of additional effort will make an estimate perfect. Next, notice
Line 54: how little effort is required to move the accuracy up dramatically from the base-
Line 55: line. As drawn in Figure 6.1, about 10% of the effort gets 50% of the potential ac-
Line 56: curacy. Finally, notice that eventually, the accuracy of the estimate declines. It is
Line 57: 50
Line 58: Accuracy
Line 59: 100
Line 60: Effort
Line 61: 
Line 62: --- 페이지 82 ---
Line 63: Estimates Are Shared 
Line 64: |
Line 65: 51
Line 66: possible to put too much effort into estimating, with the result being a less accu-
Line 67: rate estimate.
Line 68: When starting to plan a project, it is useful to think about where on the
Line 69: curve of Figure 6.1 we wish to be. Many projects try to be very high up the accu-
Line 70: racy axis, forcing teams far out on the effort axis even though the benefits dimin-
Line 71: ish rapidly. Often, this is the result of the simplistic view that we can lock down
Line 72: budgets, schedules, and scope and that project success equates to on-time, on-
Line 73: budget delivery of an up-front, precisely planned set of features. This type of
Line 74: thinking leads to a desire for extensive signed requirements documents, lots of
Line 75: up-front analysis work, and detailed project plans that show every task a team
Line 76: can think of. Then, even after all this additional up-front work, the estimates still
Line 77: aren’t perfect.
Line 78: Agile teams, however, choose to be closer to the left in a figure like
Line 79: Figure 6.1. They acknowledge that we cannot eliminate uncertainty from esti-
Line 80: mates, but they embrace the idea that small efforts are rewarded with big gains.
Line 81: Even though they are less far up the accuracy/effort scale, agile teams can pro-
Line 82: duce more reliable plans because they frequently deliver small increments of
Line 83: fully working, tested, integrated code.
Line 84: Estimates Are Shared
Line 85: Estimates are not created by a single individual on the team. Agile teams do not
Line 86: rely on a single expert to estimate. Despite well-known evidence that estimates
Line 87: prepared by those who will do the work are better than estimates prepared by
Line 88: anyone else (Lederer and Prasad 1992), estimates are best derived collaboratively
Line 89: by the team, which includes those who will do the work. There are two reasons
Line 90: for this.
Line 91: First, on an agile project we tend not to know specifically who will perform a
Line 92: given task. Yes, we may all suspect that the team’s database guru will be the one
Line 93: to do the complex stored procedure task that has been identified. However,
Line 94: there’s no guarantee that this will be the case. She may be busy when the time
Line 95: comes, and someone else will work on it. So because anyone may work on any-
Line 96: thing, it is important that everyone have input into the estimate.
Line 97: Second, even though we may expect the database guru to do the work, oth-
Line 98: ers may have something to say about her estimate. Suppose that the team’s data-
Line 99: base guru, Kristy, estimates a particular user story as three ideal days. Someone
Line 100: else on the project may not know enough to program the feature himself, but he
Line 101: may know enough to say, “Kristy, you’re nuts; the last time you worked on a fea-
Line 102: ture like that, it took a lot longer. I think you’re forgetting how hard it was last
Line 103: 
Line 104: --- 페이지 83 ---
Line 105: 52
Line 106: |
Line 107: Chapter 6
Line 108: Techniques for Estimating
Line 109: time.” At that point Kristy may offer a good explanation of why it’s different this
Line 110: time. However, more often than not in my experience, she will acknowledge that
Line 111: she was indeed underestimating the feature.
Line 112: The Estimation Scale
Line 113: Studies have shown that we are best at estimating things that fall within one or-
Line 114: der of magnitude (Miranda 2001; Saaty 1996). Within your town, you should be
Line 115: able to estimate reasonably well the relative distances to things like the nearest
Line 116: grocery store, the nearest restaurant, and the nearest library. The library may be
Line 117: twice as far as the restaurant, for example. Your estimates will be far less accu-
Line 118: rate if you are asked also to estimate the relative distance to the moon or a
Line 119: neighboring country’s capital. Because we are best within a single order of mag-
Line 120: nitude, we would like to have most of our estimates in such a range. 
Line 121: Two estimation scales I’ve had good success with are
Line 122: ◆1, 2, 3, 5, and 8
Line 123: ◆1, 2, 4, and 8
Line 124: There’s a logic behind each of these sequences. The first is the Fibonacci se-
Line 125: quence.1 I’ve found this to be a very useful estimation sequence because the gaps
Line 126: in the sequence become appropriately larger as the numbers increase. A one-
Line 127: point gap from 1 to 2 and from 2 to 3 seems appropriate, just as the gaps from 3
Line 128: to 5 and from 5 to 8 do. The second sequence is spaced such that each number is
Line 129: twice the number that precedes it. These nonlinear sequences work well because
Line 130: they reflect the greater uncertainty associated with estimates for larger units of
Line 131: work. Either sequence works well, although my slight personal preference is for
Line 132: the first. 
Line 133: Each of these numbers should be thought of as a bucket into which items of
Line 134: the appropriate size are poured. Rather than thinking of work as water being
Line 135: poured into the buckets, think of the work as sand. If you are estimating using 1,
Line 136: 2, 3, 5, and 8, and have a story that you think is just the slightest bit bigger than
Line 137: the other five-point stories you’ve estimated, it would be OK to put it into the
Line 138: five-point bucket. A story you think is a 7, however, clearly would not fit in the
Line 139: five-point bucket.
Line 140: 1.
Line 141: A number in the Fibonacci sequence is generated by taking the sum of the previous
Line 142: two numbers.
Line 143: 
Line 144: --- 페이지 84 ---
Line 145: User Stories, Epics, and Themes 
Line 146: |
Line 147: 53
Line 148: You may want to consider including 0 as a valid number within your estima-
Line 149: tion range. Although it’s unlikely that a team will encounter many user stories
Line 150: or features that truly take no work, including 0 is often useful. There are two rea-
Line 151: sons for this. First, if we want to keep all features within a 10x range, assigning
Line 152: nonzero values to tiny features will limit the size of largest features. Second, if
Line 153: the work truly is closer to 0 than 1, the team may not want the completion of the
Line 154: feature to contribute to its velocity calculations. If the team earns one point in
Line 155: this iteration for something truly trivial, in the next iteration their velocity will
Line 156: either drop by one or they’ll have to earn that point by doing work that may not
Line 157: be as trivial. 
Line 158: If the team does elect to include 0 in their estimation scale, everyone in-
Line 159: volved in the project (especially the product owner) needs to understand that
Line 160: . I’ve never had the slightest problem explaining this to product own-
Line 161: ers, who realize that a 0-point story is the equivalent of a free lunch. However,
Line 162: they also realize there’s a limit to the number of free lunches they can get in a
Line 163: single iteration. An alternative to using 0 is to group very small stories and esti-
Line 164: mate them as a single unit. 
Line 165: Some teams prefer to work with larger numbers, such as 10, 20, 30, 50, and
Line 166: 100. This is fine, because these are also within a single order of magnitude. How-
Line 167: ever, if you go with larger numbers, such as 10 to 100, I still recommend that
Line 168: you pre-identify the numbers you will use within that range. Do not, for exam-
Line 169: ple, allow one story to be estimated at 66 story points or ideal days and another
Line 170: story to be estimated at 67. That is a false level of precision, and we cannot dis-
Line 171: cern a 1.5% difference in size. It’s acceptable to have one-point differences be-
Line 172: tween values such as 1, 2, and 3. As percentages, those differences are much
Line 173: larger than between 66 and 67.
Line 174: User Stories, Epics, and Themes
Line 175: Although in general, we want to estimate user stories whose sizes are within one
Line 176: order of magnitude, this cannot always be the case. If we are to estimate every-
Line 177: thing within one order of magnitude, it would mean writing all stories at a fairly
Line 178: fine-grained level. For features that we’re not sure we want (a preliminary cost
Line 179: estimate is desired before too much investment is put into them) or for features
Line 180: that may not happen in the near future, it is often desirable to write one much
Line 181: larger user story. A large user story is sometimes called an epic.
Line 182: Additionally, a set of related user stories may be combined (usually by a pa-
Line 183: per clip if working with note cards) and treated as a single entity for either
Line 184: 13
Line 185: 0
Line 186: u
Line 187: 0
Line 188: z
Line 189: 
Line 190: --- 페이지 85 ---
Line 191: 54
Line 192: |
Line 193: Chapter 6
Line 194: Techniques for Estimating
Line 195: estimating or release planning. Such a set of user stories is referred to as a
Line 196: theme. An epic, by its very size alone, is often a theme on its own. 
Line 197: By aggregating some stories into themes and writing some stories as epics, a
Line 198: team is able to reduce the effort they’ll spend on estimating. However, it’s impor-
Line 199: tant that they realize that estimates of themes and epics will be more uncertain
Line 200: than estimates of the more specific, smaller user stories.
Line 201: User stories that will be worked on in the near future (the next few itera-
Line 202: tions) need to be small enough that they can be completed in a single iteration.
Line 203: These items should be estimated within one order of magnitude. I use the se-
Line 204: quence 1, 2, 3, 5, and 8 for this.
Line 205: User stories or other items that are likely to be more distant than a few iter-
Line 206: ations can be left as epics or themes. These items can be estimated in units be-
Line 207: yond the 1 to 8 range I recommend. To accommodate estimating these larger
Line 208: items I add 13, 20, 40, and 100 to my preferred sequence of 1, 2, 3, 5, and 8.
Line 209: Deriving an Estimate
Line 210: The three most common techniques for estimating are
Line 211: ◆Expert opinion
Line 212: ◆Analogy
Line 213: ◆Disaggregation
Line 214: Each of these techniques may be used on its own, but the techniques should
Line 215: be combined for best results.
Line 216: Expert Opinion
Line 217: If you want to know how long something is likely to take, ask an expert. At least,
Line 218: that’s one approach. In an expert opinion-based approach to estimating, an ex-
Line 219: pert is asked how long something will take or how big it will be. The expert relies
Line 220: on her intuition or gut feel and provides an estimate. 
Line 221: This approach is less useful on agile projects than on traditional projects. On
Line 222: an agile project, estimates are assigned to user stories or other user-valued func-
Line 223: tionality. Developing this functionality is likely to require a variety of skills nor-
Line 224: mally performed by more than one person. This makes it difficult to find suitable
Line 225: experts who can assess the effort across all disciplines. On a traditional project
Line 226: 
Line 227: --- 페이지 86 ---
Line 228: Disaggregation 
Line 229: |
Line 230: 55
Line 231: for which estimates are associated with tasks, this is not as significant of a prob-
Line 232: lem, because each task is likely performed by one person. 
Line 233: A nice benefit of estimating by expert opinion is that it usually doesn’t take
Line 234: very long. Typically, a developer reads a user story, perhaps asks a clarifying
Line 235: question or two, and then provides an estimate based on her intuition. There is
Line 236: even evidence that says this type of estimating is more accurate than other, more
Line 237: analytical approaches (Johnson et al. 2000).
Line 238: Analogy
Line 239: An alternative to expert opinion comes in the form of estimating by analogy,
Line 240: which is what we’re doing when we say, “This story is a little bigger than that
Line 241: story.” When estimating by analogy, the estimator compares the story being esti-
Line 242: mated with one or more other stories. If the story is twice the size, it is given an
Line 243: estimate twice as large. There is evidence that we are better at estimating rela-
Line 244: tive size than we are at estimating absolute size (Lederer and Prasad 1998; Vici-
Line 245: nanza et al. 1991).
Line 246: When estimating this way, you do not compare all stories against a single
Line 247: baseline or universal reference. Instead, you want to estimate each new story
Line 248: against an assortment of those that have already been estimated. This is referred
Line 249: to as triangulation. To triangulate, compare the story being estimated against a
Line 250: couple of other stories. To decide if a story should be estimated at five story
Line 251: points, see if it seems a little bigger than a story you estimated at three and a lit-
Line 252: tle smaller than a story you estimated at eight. 
Line 253: Disaggregation
Line 254: Disaggregation refers to splitting a story or feature into smaller, easier-to-esti-
Line 255: mate pieces. If most of the user stories to be included in a project are in the
Line 256: range of two to five days to develop, it will be very difficult to estimate a single
Line 257: story that may be 100 days. Not only are large things notoriously more difficult
Line 258: to estimate, but also in this case there will be very few similar stories to compare.
Line 259: Asking “Is this story fifty times as hard as that story” is a very different question
Line 260: from “Is this story about one-and-a-half times that one?”
Line 261: The solution to this, of course, is to break the large story or feature into
Line 262: multiple smaller items and estimate those. However, you need to be careful not
Line 263: to go too far with this approach. The easiest way to illustrate the problem is with
Line 264: a nonsoftware example. Let’s use disaggregation to estimate my golf score this
Line 265: weekend. Assume the course I am playing has eighteen holes each with a par of
Line 266: four. (If you’re unfamiliar with golf scoring, the par score is the number of shots
Line 267: 
Line 268: --- 페이지 87 ---
Line 269: 56
Line 270: |
Line 271: Chapter 6
Line 272: Techniques for Estimating
Line 273: it should take a decent player to shoot his ball into the cup at the end of the
Line 274: hole.)
Line 275: To estimate by disaggregation, we need to estimate my score for each hole.
Line 276: There’s the first hole, and that’s pretty easy, so let’s give me a three on that. But
Line 277: then I usually hit into the lake on the next hole, so that’s a seven. Then there’s
Line 278: the hole with the sandtraps; let’s say a five. And so on. However, if I’m mentally
Line 279: re-creating an entire golf course it is very likely I’ll forget one of the holes. Of
Line 280: course, in this case I have an easy check for that, as I know there must be eigh-
Line 281: teen individual estimates. But when disaggregating a story, there is no such
Line 282: safety check. 
Line 283: Not only does the likelihood of forgetting a task increase if we disaggregate
Line 284: too far, but summing estimates of lots of small tasks also leads to problems. For
Line 285: example, for each of the 18 holes, I may estimate my score for that hole to be in
Line 286: the range 3 to 8. Multiplying those by 18 gives me a full round range of 54 to
Line 287: 144. There’s no chance that I’ll do that well or that poorly. If asked for an esti-
Line 288: mate of my overall score for a full round, I’m likely to say anywhere from 80 to
Line 289: 120, which is a much smaller range and a much more useful estimate.
Line 290: Specific advice on splitting user stories is provided in Chapter 12, “Splitting
Line 291: User Stories.”
Line 292: Planning Poker
Line 293: The best way I’ve found for agile teams to estimate is by playing planning poker
Line 294: (Grenning 2002). Planning poker combines expert opinion, analogy, and disag-
Line 295: gregation into an enjoyable approach to estimating that results in quick but re-
Line 296: liable estimates. 
Line 297: Participants in planning poker include all of the developers on the team. Re-
Line 298: member that developers refers to all programmers, testers, database engineers,
Line 299: analysts, user interaction designers, and so on. On an agile project, this will typ-
Line 300: ically not exceed ten people. If it does, it is usually best to split into two teams.
Line 301: Each team can then estimate independently, which will keep the size down. The
Line 302: product owner participates in planning poker but does not estimate.
Line 303: At the start of planning poker, each estimator is given a deck of cards. Each
Line 304: card has written on it one of the valid estimates. Each estimator may, for exam-
Line 305: ple, be given a deck of cards that reads 0, 1, 2, 3, 5, 8, 13, 20, 40, and 100. The
Line 306: cards should be prepared prior to the planning poker meeting, and the numbers
Line 307: should be large enough to see across a table. Cards can be saved and used for the
Line 308: next planning poker session.
Line 309: 
Line 310: --- 페이지 88 ---
Line 311: Planning Poker 
Line 312: |
Line 313: 57
Line 314: For each user story or theme to be estimated, a moderator reads the descrip-
Line 315: tion. The moderator is usually the product owner or an analyst. However, the
Line 316: moderator can be anyone, as there is no special privilege associated with the
Line 317: role. The product owner answers any questions that the estimators have. How-
Line 318: ever, everyone is asked to remain aware of the effort/accuracy curve (Figure 6.1).
Line 319: The goal in planning poker is not to derive an estimate that will withstand all fu-
Line 320: ture scrutiny. Rather, the goal is to be somewhere well on the left of the effort
Line 321: line, where a valuable estimate can be arrived at cheaply.
Line 322: After all questions are answered, each estimator privately selects a card rep-
Line 323: resenting his or her estimate. Cards are not shown until each estimator has
Line 324: made a selection. At that time, all cards are simultaneously turned over and
Line 325: shown so that all participants can see each estimate.
Line 326: It is very likely at this point that the estimates will differ significantly. This is
Line 327: actually good news. If estimates differ, the high and low estimators explain their
Line 328: estimates. It’s important that this does not come across as attacking those esti-
Line 329: mators. Instead, you want to learn what they were thinking about.
Line 330: As an example, the high estimator may say, “Well, to test this story, we need
Line 331: to create a mock database object. That might take us a day. Also, I’m not sure if
Line 332: our standard compression algorithm will work, and we may need to write one
Line 333: that is more memory efficient.” The low estimator may respond, “I was thinking
Line 334: we’d store that information in an XML file—that would be easier than a database
Line 335: for us. Also, I didn’t think about having more data—maybe that will be a
Line 336: problem.”
Line 337: The group can discuss the story and their estimates for a few more minutes.
Line 338: The moderator can take any notes she thinks will be helpful when this story is
Line 339: being programmed and tested. After the discussion, each estimator re-estimates
Line 340: by selecting a card. Cards are once again kept private until everyone has esti-
Line 341: mated, at which point they are turned over at the same time.
Line 342: In many cases, the estimates will already converge by the second round. But
Line 343: if they have not, continue to repeat the process. The goal is for the estimators to
Line 344: converge on a single estimate that can be used for the story. It rarely takes more
Line 345: than three rounds, but continue the process as long as estimates are moving
Line 346: closer together. It isn’t necessary that everyone in the room turns over a card
Line 347: with exactly the same estimate written down. If I’m moderating an estimation
Line 348: meeting, and on the second round four estimators tell me 5, 5, 5, and 3, I will ask
Line 349: the low estimator if she is OK with an estimate of 5. Again, the point is not abso-
Line 350: lute precision but reasonableness.
Line 351: 
Line 352: --- 페이지 89 ---
Line 353: 58
Line 354: |
Line 355: Chapter 6
Line 356: Techniques for Estimating
Line 357: Smaller Sessions
Line 358: It is possible to play planning poker with a subset of the team, rather than in-
Line 359: volving everyone. This isn’t ideal but may be a reasonable option, especially if
Line 360: there are many, many items to be estimated, as can happen at the start of a new
Line 361: project.
Line 362: The best way to do this is to split the larger team into two or three smaller
Line 363: teams, each of which must have at least three estimators. It is important that
Line 364: each of the teams estimates consistently. What your team calls three story points
Line 365: or ideal days had better be consistent with what my team calls the same. To
Line 366: achieve this, start all teams together in a joint planning poker session for an
Line 367: hour or so. Have them estimate ten to twenty stories. Then make sure each team
Line 368: has a copy of these stories and their estimates and that they use them as base-
Line 369: lines for estimating the stories they are given to estimate.
Line 370: When to Play Planning Poker
Line 371: Teams will need to play planning poker at two different times. First, there will
Line 372: usually be an effort to estimate a large number of items before the project offi-
Line 373: cially begins or during its first iterations. Estimating an initial set of user stories
Line 374: may take a team two or three meetings of from one to three hours each. Natu-
Line 375: rally, this will depend on how many items there are to estimate, the size of the
Line 376: team, and the product owner’s ability to clarify the requirements succinctly.
Line 377: Second, teams will need to put forth some ongoing effort to estimate any
Line 378: new stories that are identified during an iteration. One way to do this is to plan
Line 379: The Right Amount of Discussion
Line 380: Some amount of preliminary design discussion is necessary and appropri-
Line 381: ate when estimating. However, spending too much time on design dis-
Line 382: cussions sends a team too far up the effort/accuracy curve of Figure 6.1.
Line 383: Here’s an effective way to encourage some amount of discussion but
Line 384: make sure that it doesn’t go on too long.
Line 385: Buy a two-minute sand timer, and place it in the middle of the table
Line 386: where planning poker is being played. Anyone in the meeting can turn
Line 387: the timer over at any time. When the sand runs out (in two minutes), the
Line 388: next round of cards is played. If agreement isn’t reached, the discussion
Line 389: can continue. But someone can immediately turn the timer over, again
Line 390: limiting the discussion to two minutes. The timer rarely needs to be
Line 391: turned over more than twice. Over time this helps teams learn to esti-
Line 392: mate more rapidly.
Line 393: 
Line 394: --- 페이지 90 ---
Line 395: Why Planning Poker Works 
Line 396: |
Line 397: 59
Line 398: to hold a very short estimation meeting near the end of each iteration. Normally,
Line 399: this is quite sufficient for estimating any work that came in during the iteration,
Line 400: and it allows new work to be considered in the prioritization of the coming iter-
Line 401: ation.
Line 402: Alternatively, Kent Beck suggests hanging an envelope on the wall with all
Line 403: new stories placed in the envelope. As individuals have a few spare minutes, they
Line 404: will grab a story or two from the envelope and estimate them. Teams will estab-
Line 405: lish a rule for themselves, typically that all stories must be estimated by the end
Line 406: of the day or by the end of the iteration. I like the idea of hanging an envelope on
Line 407: the wall to contain unestimated stories. However, I’d prefer that when someone
Line 408: has a few spare minutes to devote to estimating, he find at least one other person
Line 409: and that they estimate jointly.
Line 410: Why Planning Poker Works
Line 411: Now that I’ve described planning poker, it’s worth spending a moment on some
Line 412: of the reasons why it works so well. 
Line 413: First, planning poker brings together multiple expert opinions to do the es-
Line 414: timating. Because these experts form a cross-functional team from all disci-
Line 415: plines on a software project, they are better suited to the estimation task than
Line 416: anyone else. After completing a thorough review of the literature on software es-
Line 417: timation, Jørgensen (2004) concluded that “the people most competent in solv-
Line 418: ing the task should estimate it.” 
Line 419: Second, a lively dialogue ensues during planning poker, and estimators are
Line 420: called upon by their peers to justify their estimates. This has been found to im-
Line 421: prove the accuracy of the estimate, especially on items with large amounts of un-
Line 422: certainty (Hagafors and Brehmer 1983). Being asked to justify estimates has also
Line 423: been shown to result in estimates that better compensate for missing informa-
Line 424: tion (Brenner et al. 1996). This is important on an agile project because the user
Line 425: stories being estimated are often intentionally vague.
Line 426: Third, studies have shown that averaging individual estimates leads to better
Line 427: results (Hoest and Wohlin 1998) as do group discussions of estimates (Jørgensen
Line 428: and Moløkken 2002). Group discussion is the basis of planning poker, and those
Line 429: discussions lead to an averaging of sorts of the individual estimates. 
Line 430: Finally, planning poker works because it’s fun.
Line 431: 
Line 432: --- 페이지 91 ---
Line 433: 60
Line 434: |
Line 435: Chapter 6
Line 436: Techniques for Estimating
Line 437: Summary
Line 438: Expending more time and effort to arrive at an estimate does not necessarily in-
Line 439: crease the accuracy of the estimate. The amount of effort put into an estimate
Line 440: should be determined by the purpose of that estimate. Although it is well known
Line 441: that the best estimates are given by those who will do the work, on an agile team
Line 442: we do not know in advance who will do the work. Therefore, estimating should
Line 443: be a collaborative activity for the team.
Line 444: Estimates should be on a predefined scale. Features that will be worked on
Line 445: in the near future and that need fairly reliable estimates should be made small
Line 446: enough that they can be estimated on a nonlinear scale from 1 to 10 such as 1, 2,
Line 447: 3, 5, and 8 or 1, 2, 4, and 8. Larger features that will most likely not be imple-
Line 448: mented in the next few iterations can be left larger and estimated in units such
Line 449: as 13, 20, 40, and 100. Some teams choose to include 0 in their estimation scale. 
Line 450: To arrive at an estimate, we rely on expert opinion, analogy, and disaggrega-
Line 451: tion. A fun and effective way of combining these is planning poker. In planning
Line 452: poker, each estimator is given a deck of cards with a valid estimate shown on
Line 453: each card. A feature is discussed, and each estimator selects the card that repre-
Line 454: sents his or her estimate. All cards are shown at the same time. The estimates are
Line 455: discussed and the process repeated until agreement on the estimate is reached.
Line 456: Discussion Questions
Line 457: 1. How good are your estimates today? Which techniques do you primarily rely
Line 458: on: expert opinion, analogy, or disaggregation?
Line 459: 2. Which estimation scale do you prefer? Why?
Line 460: 3. Who should participate in planning poker on your project?
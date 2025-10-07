Line 1: 
Line 2: --- 페이지 234 ---
Line 3: 203
Line 4: Chapter 18
Line 5: Planning the Multiple-Team 
Line 6: Project
Line 7: “Do the planning, but throw out the plans.”
Line 8: —Mary Poppendieck
Line 9: Agile teams are often described as having no more than seven to ten developers.
Line 10: Teams of this size can accomplish quite a bit, especially with an agile process
Line 11: that allows and encourages them to become more productive. However, there
Line 12: are some projects in which we’d like to bring a larger team to bear on the
Line 13: project. Rather than establishing a single 100-person team, the agile approach is
Line 14: to create multiple smaller teams. An agile project may have a dozen smaller
Line 15: teams instead of a single 100-person team.
Line 16: In this chapter, we will take what we’ve learned in previous chapters and ap-
Line 17: ply it to the challenge of planning a project comprising multiple teams. Planning
Line 18: a large, multiple team project may require
Line 19: 1. Establishing a common basis for estimates.
Line 20: 2. Adding detail to their user stories sooner.
Line 21: 3. Performing lookahead planning.
Line 22: 4. Incorporating feeding buffers into the plan.
Line 23: A project may require some or all of these techniques, depending on how
Line 24: many subteams are involved, as well as how often and intensely they need to co-
Line 25: ordinate. In general, I advise teams to incorporate only as many of these
Line 26: 
Line 27: --- 페이지 235 ---
Line 28: 204 |
Line 29: Chapter 18
Line 30: Planning the Multiple-Team Project
Line 31: additional techniques as necessary, starting with establishing a common basis
Line 32: and working in order toward introducing feeding buffers.
Line 33: Establishing a Common Basis for Estimates
Line 34: Although it would be nice to let each individual subteam choose whether to esti-
Line 35: mate in story points or ideal days, most projects with multiple teams will benefit
Line 36: from estimating in a common unit and establishing a baseline meaning for that
Line 37: unit. Imagine the difficulty of predicting how much longer is needed to complete
Line 38: a set of user stories if some of them are estimated in ideal days and some are es-
Line 39: timated in story points. Worse, imagine how much harder it would be if one
Line 40: team estimated a set of stories as 20 points but another team estimated the same
Line 41: work as 100 story points. 
Line 42: At the start of a project, the teams should meet and choose between story
Line 43: points and ideal days. They should then establish a common baseline for their es-
Line 44: timates so that an estimate by one team will be similar to that of another team if
Line 45: the other team had estimated the work instead. Each user story needs to be esti-
Line 46: mated by only one team, but the estimates should be equivalent regardless of
Line 47: which team estimated the work. 
Line 48: There are two good ways to establish a common baseline. The first approach
Line 49: works only if the teams have worked together on a past project. In that case, they
Line 50: can select some user stories from the past project and agree on the estimates for
Line 51: them. Suppose they are estimating in ideal days; they should find two or three
Line 52: stories they consider as one ideal-day each. Then they should find a few they con-
Line 53: sider to be two ideal-day stories, and so on. They may identify twenty or so old
Line 54: stories, agreeing upon a new estimate for each, knowing what they now know
Line 55: about the stories. Once these baseline stories are agreed upon, the teams may
Line 56: separately estimate stories by comparing them with the baseline stories (that is,
Line 57: estimating them by analogy).
Line 58: The second approach is similar but involves collaboratively estimating an as-
Line 59: sortment of new user stories. A variety of stories planned for the new release are
Line 60: selected. The stories should span a variety of sizes and should be in areas of the
Line 61: system that most of the estimators can relate to. Either the entire large team—
Line 62: or representatives of each subteam, if the entire team is too big—meet and agree
Line 63: upon an estimate for these stories. As with the first approach, these estimates are
Line 64: then used as baselines against which future estimates are compared.
Line 65: The only time separate teams should consider estimating in different units
Line 66: without a common baseline is when the products being built are truly separate
Line 67: and there is absolutely no opportunity for developers from one team to move
Line 68: 
Line 69: --- 페이지 236 ---
Line 70: Adding Detail to User Stories Sooner 
Line 71: |
Line 72: 205
Line 73: onto another. Even then, my recommendation is to establish a common base-
Line 74: line, as it facilitates communicating about the project.
Line 75: Adding Detail to User Stories Sooner
Line 76: Ideally, an agile team begins an iteration with vaguely defined requirements and
Line 77: turns those vague requirements into functioning, tested software by the end of
Line 78: the iteration. Going from vague requirement to working software in one itera-
Line 79: tion is usually easier on a single-team project than it is when there are multiple
Line 80: teams. On a multiple-team project, it is often appropriate and necessary to put
Line 81: more thought into the user stories before the start of the iteration. The addi-
Line 82: tional detail allows multiple teams to coordinate work. 
Line 83: To achieve this, larger teams often include dedicated analysts, user interac-
Line 84: tion designers, and others who spend a portion of their time during a given iter-
Line 85: ation preparing the work of the next iteration. In general, I do not advise having
Line 86: analysts, interaction designers, and others work a full iteration ahead. Rather,
Line 87: their primary responsibility should remain the work of the current iteration, but
Line 88: in planning the current iteration, they should include some tasks related to pre-
Line 89: paring for the next iteration. 
Line 90: What I’ve found to be the most useful outcome of work done in advance of
Line 91: the iteration is the identification of the product owner’s conditions of satisfac-
Line 92: tion for the user stories that are likely to be developed during the iteration. A
Line 93: product owner’s conditions of satisfaction for a user story are the high-level ac-
Line 94: ceptance tests that she would like to see applied to the story before considering
Line 95: it finished. A user story is finished when it can be demonstrated to meet all of the
Line 96: conditions of satisfaction identified by the product owner.
Line 97: Although it is extremely helpful to know the conditions of satisfaction for a
Line 98: user story before an iteration begins, it is unlikely (and unnecessary) that a team
Line 99: identify them for all user stories in advance of the iteration. Realistically, the ex-
Line 100: act set of stories that will be undertaken in the next iteration are not known until
Line 101: the end of the iteration planning meeting that kicks off the iteration. In most
Line 102: cases, however, the product owner and team can make a reasonable guess at the
Line 103: stories that will most likely be prioritized into the next iteration. Conditions of
Line 104: satisfaction can be identified for these stories in advance of the iteration.
Line 105: 
Line 106: --- 페이지 237 ---
Line 107: 206 |
Line 108: Chapter 18
Line 109: Planning the Multiple-Team Project
Line 110: Lookahead Planning
Line 111: Most teams with either moderately complex or frequent interdependencies will
Line 112: benefit from maintaining a rolling lookahead window during release and itera-
Line 113: tion planning. Suppose two teams are working on the SwimStats application.
Line 114: Part of SwimStats involves displaying static information such as practice times,
Line 115: the addresses of and directions to pools, and so on. However, SwimStats must
Line 116: also provide database-driven dynamic information, including results from all
Line 117: meets over the past fifteen years and personal records for all swimmers in all
Line 118: events.
Line 119: National and age-group records are stored in a database at the remote facil-
Line 120: ity of the national swimming association. Accessing the database isn’t as simple
Line 121: as the teams would like, and the national association is planning to change data-
Line 122: base vendors in the next year or two. For these reasons, the product owner and
Line 123: development teams agree that they want to develop an API (application pro-
Line 124: gramming interface) for accessing the database. This will make a later change to
Line 125: a different database vendor much simpler. The initial user stories and the esti-
Line 126: mates for each are shown in Table 18.1.
Line 127: Velocity is estimated to be twenty points per iteration for each team. Because
Line 128: there are 110 points of work, this means the teams should be able to deliver all
Line 129: functionality in three iterations. However, thirty of the points are for developing
Line 130: Table 18.1 The Initial User Stories and Estimates for SwimStats
Line 131: User Story
Line 132: Story Points
Line 133: As SwimStats, we want to be able to change our database 
Line 134: vendor easily.
Line 135: 30
Line 136: As any site visitor, I need to be authenticated before being 
Line 137: given access to sensitive parts of the site.
Line 138: 20
Line 139: As a swimmer, I want to see when practices are scheduled.
Line 140: 10
Line 141: As a swimmer or parent, I want to know where league pools 
Line 142: are located.
Line 143: 10
Line 144: As any site visitor, I want to see the national records by age 
Line 145: group and event.
Line 146: 10
Line 147: As any site visitor, I would like to see the results of any meet.
Line 148: 10
Line 149: As any site visitor, I would like to see the personal records of 
Line 150: any swimmer.
Line 151: 20
Line 152: 
Line 153: --- 페이지 238 ---
Line 154: Lookahead Planning 
Line 155: |
Line 156: 207
Line 157: the API, and another forty (the last three stories in Table 18.1) can be done only
Line 158: after the API. To finish these seventy points in three iterations, both teams will
Line 159: need to use the API. This leads them to an allocation of work as shown in
Line 160: Figure 18.1, which shows the team interdependency as an arrow between the
Line 161: API work of the first team and the personal records work done by the second.
Line 162: Figure 18.1 Coordinating the work of two teams.
Line 163: You may recall that in Chapter 13, “Release Planning Essentials,” I advised
Line 164: that the release plan show detail only for the next couple of iterations. This is be-
Line 165: cause that is often enough to support the interdependencies encountered by
Line 166: many teams. When multiple teams need to coordinate work, the release plan
Line 167: should be updated to show and coordinate the work of the next two or three iter-
Line 168: ations. The exact number of iterations will, of course, depend on the frequency
Line 169: and significance of the dependencies among teams. As iterations are completed,
Line 170: details about them are dropped from the plan. The release plan then becomes a
Line 171: rolling lookahead plan that always outlines expectations about the new few iter-
Line 172: ations. Laufer (1996) refers to this as “peering forward.”
Line 173: Figure 18.1 shows the situation in which a handoff between teams occurs
Line 174: between iterations. This is safer than planning on a handoff occuring during an
Line 175: iteration. At the start of each iteration, each team identifies the work they can
Line 176: complete and commits to finishing it. In the case of Figure 18.1, at the start of
Line 177: the third iteration, Team 2 was able to make a meaningful commitment to com-
Line 178: pleting the personal records user story because they knew that the API was fin-
Line 179: ished. Suppose instead that when Team 2 planned its third iteration the API was
Line 180: not done but was expected to be finished in a few days. Even if Team 2 could fin-
Line 181: ish the personal-records story without having the API on the first day, it is a
Line 182: much more tenuous commitment, and the overall schedule is at greater risk.
Line 183: Teams will often need to make commitments based on miditeration deliverables.
Line 184: However, to the extent possible, they should limit commitments to work com-
Line 185: pleted before the start of the iteration.
Line 186: Authentication
Line 187: Personal records
Line 188: Practice and pool 
Line 189: info
Line 190: Meet
Line 191: results
Line 192: Unused
Line 193: API
Line 194: Team 1
Line 195: Team 2
Line 196: API
Line 197: National
Line 198: records
Line 199: 
Line 200: --- 페이지 239 ---
Line 201: 208 |
Line 202: Chapter 18
Line 203: Planning the Multiple-Team Project
Line 204: Incorporating Feeding Buffers into the Plan
Line 205: For most teams in most situations, a rolling lookahead plan is adequate. There
Line 206: are situations, however, in which the interdependencies between teams are so
Line 207: complex or frequent that the simple rolling lookahead planning of the preceding
Line 208: section is not enough. In these cases, your first recourse should be to try to find
Line 209: a way to reduce the number of interdependencies so that a rolling lookahead
Line 210: plan is adequate. If that cannot be done, consider including a feeding buffer in
Line 211: iterations that deliver capabilities needed by other teams. A feeding buffer, like
Line 212: the schedule buffer of the previous chapter, protects the on-time delivery of a set
Line 213: of new capabilities. This is a somewhat complicated way of saying that if your
Line 214: team needs something from my team tomorrow at 8:00 a.m., my team shouldn’t
Line 215: plan on finishing it at 7:59. That is, we’d like a plan that looks like Figure 18.2.
Line 216: Figure 18.2 Adding a feeding buffer.
Line 217: In Figure 18.2, a feeding buffer has been inserted between Team 1’s comple-
Line 218: tion of the API and the beginning of Team 2’s work using the API on the personal
Line 219: records user story. The feeding buffer protects the start date on the personal-
Line 220: records story against delays in the completion of the API. 
Line 221: To include a feeding buffer in a release plan, all you need to do is plan tem-
Line 222: porarily for a lower velocity for the team that is delivering a capability to another
Line 223: team. In the case of Figure 18.2, Team 1’s effort is evenly split between finishing
Line 224: the API and a feeding buffer so that we can be sure Team 2 is able to start on the
Line 225: personal records at the beginning of the third iteration. This does not mean that
Line 226: Team 1 gets to take it easy during the second iteraton. In fact, the expectation is
Line 227: that they will complete ten points on the API, need only a portion of the buffer,
Line 228: and begin work on the national-records user story during the second iteration.
Line 229: What Gets Buffered?
Line 230: In the case shown in Figure 18.2, adding a feeding buffer did not extend the
Line 231: length of the overall project, because Team 1’s third iteration was not already
Line 232: Authentication
Line 233: Personal records
Line 234: Practice and pool 
Line 235: info
Line 236: National
Line 237: records
Line 238: Meet
Line 239: results
Line 240: API
Line 241: Team 1
Line 242: Team 2
Line 243: API
Line 244: Feeding
Line 245: buffer
Line 246: 
Line 247: --- 페이지 240 ---
Line 248: Sizing a Feeding Buffer 
Line 249: |
Line 250: 209
Line 251: full. In many cases, however, adding feeding buffers will extend the expected du-
Line 252: ration of a project. But it usually does so in a way that represents a realistic ex-
Line 253: pectation of the likely schedule, not in a “let’s pad the schedule so we don’t have
Line 254: to work hard” way. Because feeding buffers can prolong a schedule, you want to
Line 255: add them only when necessary. 
Line 256: To determine where feeding buffers are necessary, first allocate user stories
Line 257: among teams and iterations. Then look for critical dependencies between itera-
Line 258: tions and teams. Finally, add a feeding buffer only between these critical depen-
Line 259: dencies. That is, add a feeding buffer only if a team will be unable to do planned,
Line 260: high-priority work without the deliverables of another team. Even so, if the team
Line 261: can easily swap in other highly valuable work, a feeding buffer is unnecessary.
Line 262: Similarly, do not add a feeding buffer if the second team will be able to start mak-
Line 263: ing progress with a partial deliverable from the first team. If your team can start
Line 264: its work even if my team delivers only half of the planned functionality, a feeding
Line 265: buffer is not needed. 
Line 266: Sizing a Feeding Buffer
Line 267: To size the feeding buffer, you can use the guidelines provided in Chapter 17,
Line 268: “Buffering Plans for Uncertainty.” Fortunately, however, most interteam depen-
Line 269: dencies are based on no more than a handful of stories or features at a time. Be-
Line 270: cause of this, you usually won’t have enough stories to use the square root of the
Line 271: sum of the squares approach described in that chapter effectively. In these cases,
Line 272: set the size of the feeding buffer as a percentage of the stories creating the inter-
Line 273: dependency. You can use 50% as a default buffer size, but this should be adjusted
Line 274: based on team judgment.
Line 275: It is possible to have a feeding buffer that is longer than a full iteration.
Line 276: However, it is rarely advisable to use a feeding buffer that long. A feeding buffer
Line 277: that is longer than an iteration is usually the result of planning to pass a large
Line 278: chunk of functionality on to another team. There are two reasons why a project
Line 279: probably doesn’t need a large feeding buffer in these cases. First, the handoff
Line 280: from one team to another should almost certainly be divided so that the func-
Line 281: tionality is delivered incrementally. This will allow the second team to get
Line 282: started as soon as they receive the initial set of functionality from the first team.
Line 283: Second, rather than consume an extremely large feeding buffer, the teams would
Line 284: probably find ways of splitting the work or of making other adjustments between
Line 285: iterations as soon as they noticed one team slipping behind. Having the receiv-
Line 286: ing team act as a product owner or customer of the delivering team will usually
Line 287: allow the two teams to work out an incremental delivery sequence that works for
Line 288: both teams.
Line 289: 
Line 290: --- 페이지 241 ---
Line 291: 210 |
Line 292: Chapter 18
Line 293: Planning the Multiple-Team Project
Line 294: I’ve never had to use a feeding buffer that was larger than a full iteration and
Line 295: have rarely used one longer than half an iteration. Whenever I encounter the
Line 296: possible need to do so, I question my assumptions and review the plan to see
Line 297: what I can do to shorten the chain of deliverables being passed from one team to
Line 298: another.
Line 299: But This Is So Much Work
Line 300: Well, yes, but so is a large, multiple-team project. Keep in mind that you don’t
Line 301: need to do any of this if you’ve got a single team. You probably don’t even need to
Line 302: do this if you have just three or four approximately seven-person teams as long
Line 303: as those teams communicate often.
Line 304: However, many large projects need to announce and commit to deadlines
Line 305: many months in advance, and many large projects do have interteam dependen-
Line 306: cies like those shown in this chapter. When faced with a project like that, it is
Line 307: useful to spend a few more hours planning the project. Doing so will allow you to
Line 308: more confidently and accurately estimate a target completion date at the outset
Line 309: and will also provide some protection against easily avoided schedule delays.
Line 310: Summary
Line 311: Agile projects tend to avoid large teams instead using teams of teams to develop
Line 312: large projects. When multiple teams are working on one project, they need to
Line 313: coordinate their work. This chapter described four techniques that are useful in
Line 314: helping multiple teams work on the same project.
Line 315: First, teams should establish a common basis for their estimates. All teams
Line 316: should agree to estimate in the same unit: story points or ideal days. They should
Line 317: further agree on the meaning of those units by agreeing upon the estimates for
Line 318: a small set of stories.
Line 319: Second, when multiple teams need to work together, it is often useful to add
Line 320: detail to their user stories sooner. The best way to do this is to identify the prod-
Line 321: uct owner’s conditions of satisfaction for a story. These are the things that can be
Line 322: demonstrated as true about a story once it is fully implemented.
Line 323: Third, multiple teams benefit from incorporating a rolling lookahead plan
Line 324: into their release planning process. A rolling lookahead plan simply looks for-
Line 325: ward a small number of iterations (typically, only two or three) and allows teams
Line 326: to coordinate work by sharing information about what each will be working on
Line 327: in the near future.
Line 328: 
Line 329: --- 페이지 242 ---
Line 330: Discussion Questions 
Line 331: |
Line 332: 211
Line 333: Fourth, on highly complex projects with many interteam dependencies, it
Line 334: can be helpful to incorporate feeding buffers into the plan. A feeding buffer is an
Line 335: amount of time that prevents the late delivery by one team causing the late start
Line 336: of another.
Line 337: These techniques are generally introduced to a project in the order de-
Line 338: scribed. They can, however, be introduced in any order desired.
Line 339: Discussion Questions
Line 340: 1. How would you choose to establish a common baseline for your estimates
Line 341: on a project with multiple teams?
Line 342: 2. How significant are team interdependencies on your project? Which of the
Line 343: techniques introduced in this chapter would be most beneficial?
Line 344: 
Line 345: --- 페이지 243 ---
Line 346: This page intentionally left blank 
Line 1: 
Line 2: --- 페이지 34 ---
Line 3: 3
Line 4: Chapter 1
Line 5: The Purpose of Planning
Line 6: “Planning is everything. Plans are nothing.”
Line 7: —Field Marshal Helmuth Graf von Moltke
Line 8: Estimating and planning are critical to the success of any software development
Line 9: project of any size or consequence. Plans guide our investment decisions: We
Line 10: might initiate a specific project if we estimate it to take six months and ¤1 mil-
Line 11: lion1 but would reject the same project if we thought it would take two years and
Line 12: ¤4 million. Plans help us know who needs to be available to work on a project
Line 13: during a given period. Plans help us know if a project is on track to deliver the
Line 14: functionality that users need and expect. Without plans we open our projects to
Line 15: any number of problems.
Line 16: Yet planning is difficult, and plans are often wrong. Teams often respond to
Line 17: this by going to one of two extremes: They either do no planning at all, or they
Line 18: put so much effort into their plans that they become convinced that the plans
Line 19: must be right. The team that does no planning cannot answer the most basic
Line 20: questions, such as “When will you be done?” and “Can we schedule the product
Line 21: release for June?” The team that overplans deludes themselves into thinking that
Line 22: any plan can be “right.” Their plan may be more thorough, but that does not
Line 23: necessarily mean it will be more accurate or useful.
Line 24: That estimating and planning are difficult is not news. We’ve known it for a
Line 25: long time. In 1981, Barry Boehm drew the first version of what Steve McConnell
Line 26: 1. Remember that ¤ is the universal, generic currency symbol. 
Line 27: 
Line 28: --- 페이지 35 ---
Line 29: 4
Line 30: |
Line 31: Chapter 1
Line 32: The Purpose of Planning
Line 33: (1998) later called the “cone of uncertainty.” Figure 1.1 shows Boehm’s initial
Line 34: ranges of uncertainty at different points in a sequential development (“water-
Line 35: fall”) process. The cone of uncertainty shows that during the feasibility phase of
Line 36: a project a schedule estimate is typically as far off as 60% to 160%. That is, a
Line 37: project expected to take 20 weeks could take anywhere from 12 to 32 weeks. Af-
Line 38: ter the requirements are written, the estimate might still be off +/- 15% in either
Line 39: direction. So an estimate of 20 weeks means work that takes 17 to 23 weeks.
Line 40: Figure 1.1 The cone of uncertainty narrows as the project progresses.
Line 41: The Project Management Institute (PMI) presents a similar view on the pro-
Line 42: gressive accuracy of estimates. However, rather than viewing the cone of uncer-
Line 43: tainty as symmetric, PMI views it as asymmetric. PMI suggests the creation of an
Line 44: initial order of magnitude estimate, which ranges from +75% to –25%. The next
Line 45: estimate to be created is the budgetary estimate, with a range of +25% to –10%,
Line 46: followed by the final definitive estimate, with a range of +10% to –5%.
Line 47: Project 
Line 48: Schedule
Line 49: Approved
Line 50: Product
Line 51: Definition
Line 52: Requirements
Line 53: Specification
Line 54: Initial
Line 55: Product
Line 56: Definition
Line 57: Detailed
Line 58: Design
Line 59: Specification
Line 60: Accepted
Line 61: Software
Line 62: 1.6x
Line 63: 1.25x
Line 64: 1.15x
Line 65: Product
Line 66: Design
Line 67: Specification
Line 68: 1.1x
Line 69: x
Line 70: 0.9x
Line 71: 0.85x
Line 72: 0.8x
Line 73: 0.6x
Line 74: 
Line 75: --- 페이지 36 ---
Line 76: Reducing Risk 
Line 77: |
Line 78: 5
Line 79: Why Do It?
Line 80: If estimating and planning are difficult, and if it’s impossible to get an accurate
Line 81: estimate until so late in a project, why do it at all? Clearly, there is the obvious
Line 82: reason that the organizations in which we work often demand that we provide
Line 83: estimates. Plans and schedules may be needed for a variety of legitimate reasons,
Line 84: such as planning marketing campaigns, scheduling product release activities,
Line 85: training internal users, and so on. These are important needs, and the difficulty
Line 86: of estimating a project does not excuse us from providing a plan or schedule that
Line 87: the organization can use for these purposes. However, beyond these perfunctory
Line 88: needs, there is a much more fundamental reason to take on the hard work of es-
Line 89: timating and planning.
Line 90: Estimating and planning are not just about determining an appropriate
Line 91: deadline or schedule. Planning—especially an ongoing iterative approach to
Line 92: planning—is a quest for value. Planning is an attempt to find an optimal solu-
Line 93: tion to the overall product development question: What should we build? To an-
Line 94: swer this question, the team considers features, resources, and schedule. The
Line 95: question cannot be answered all at once. It must be answered iteratively and in-
Line 96: crementally. At the start of a project we may decide that a product should con-
Line 97: tain a specific set of features and be released on August 31. But in June we may
Line 98: decide that a slightly later date with slightly more features will be better. Or we
Line 99: may decide that slightly sooner with slightly fewer features will be better. 
Line 100: A good planning process supports this by
Line 101: ◆Reducing risk
Line 102: ◆Reducing uncertainty
Line 103: ◆Supporting better decision making
Line 104: ◆Establishing trust
Line 105: ◆Conveying information
Line 106: Reducing Risk
Line 107: Planning increases the likelihood of project success by providing insights into
Line 108: the project’s risks. Some projects are so risky that we may choose not to start
Line 109: once we’ve learned about the risks. Other projects may contain features whose
Line 110: risks can be contained by early attention.
Line 111: The discussions that occur while estimating raise questions that expose po-
Line 112: tential dark corners of a project. Suppose you are asked to estimate how long it
Line 113: will take to integrate the new project with an existing mainframe legacy system
Line 114: 
Line 115: --- 페이지 37 ---
Line 116: 6
Line 117: |
Line 118: Chapter 1
Line 119: The Purpose of Planning
Line 120: that you know nothing about. This will expose the integration features as a po-
Line 121: tential risk. The project team can opt to eliminate the risk right then by spend-
Line 122: ing time learning about the legacy system. Or the risk can be noted and the
Line 123: estimate for the work either made larger or expressed as a range to account for
Line 124: the greater uncertainty and risk.
Line 125: Reducing Uncertainty
Line 126: Throughout a project, the team is generating new capabilities in the product.
Line 127: They are also generating new knowledge—about the product, the technologies
Line 128: in use, and themselves as a team. It is critical that this new knowledge be ac-
Line 129: knowledged and factored into an iterative planning process that is designed to
Line 130: help a team refine their vision of the product. The most critical risk facing most
Line 131: projects is the risk of developing the wrong product. Yet this risk is entirely ig-
Line 132: nored on most projects. An agile approach to planning can dramatically reduce
Line 133: (and ideally eliminate) this risk. 
Line 134: The often-cited CHAOS studies (Standish 2001) define a successful project
Line 135: as on time, on budget, and with all features as initially specified. This is a danger-
Line 136: ous definition because it fails to acknowledge that a feature that looked good
Line 137: when the project was started may not be worth its development cost once the
Line 138: team begins on the project. If I were to define a failed project, one of my criteria
Line 139: would certainly be “a project on which no one came up with any better ideas
Line 140: than what was on the initial list of requirements.” We want to encourage
Line 141: projects on which investment, schedule, and feature decisions are periodically
Line 142: reassessed. A project that delivers all features on the initial plan is not necessar-
Line 143: ily a success. The product’s users and customer would probably not be satisfied if
Line 144: wonderful new feature ideas had been rejected in favor of mediocre ones simply
Line 145: because the mediocre features were in the initial plan.
Line 146: Supporting Better Decision Making
Line 147: Estimates and plans help us make decisions. How does an organization decide
Line 148: whether a particular project is worth doing if it does not have estimates of the
Line 149: value and the cost of the project? Beyond decisions about whether or not to start
Line 150: a project, estimates help us make sure we are working on the most valuable
Line 151: projects possible. Suppose an organization is considering two projects; one is es-
Line 152: timated to make ¤1 million, and the second is estimated to make ¤2 million.
Line 153: First, the organization needs schedule and cost estimates to determine whether
Line 154: these projects are worth pursuing. Will the projects take so long that they miss a
Line 155: market window? Will the projects cost more than they’ll make? Second, the
Line 156: 
Line 157: --- 페이지 38 ---
Line 158: Establishing Trust 
Line 159: |
Line 160: 7
Line 161: organization needs estimates and a plan so that it can decide which to pursue.
Line 162: The organization may be able to pursue one project, both projects, or neither if
Line 163: the costs are too high.
Line 164: Organizations need estimates in order to make decisions beyond whether or
Line 165: not to start a project. Sometimes the staffing profile of a project can be more im-
Line 166: portant than its schedule. For example, a project may not be worth starting if it
Line 167: will involve the time of the organization’s chief architect, who is already fully
Line 168: committed on another project. However, if a plan can be developed that shows
Line 169: how to complete the new project without the involvement of this architect, the
Line 170: project may be worth starting.
Line 171: Many of the decisions made while planning a project are tradeoff decisions.
Line 172: For example, on every project we make tradeoff decisions between development
Line 173: time and cost. Often the cheapest way to develop a system would be to hire one
Line 174: good programmer and allow her ten or twenty years to write the system, allow-
Line 175: ing her years of detouring to perhaps master the domain, become an expert in
Line 176: database administration, and so on. Obviously, though, we can rarely wait twenty
Line 177: years for a system, and so we engage teams. A team of thirty may spend a year
Line 178: (thirty person-years) developing what a lone programmer could have done in
Line 179: twenty. The development cost goes up, but the value of having the application
Line 180: nineteen years earlier justifies the increased cost.
Line 181: We are constantly making similar tradeoff decisions between functionality
Line 182: and effort, cost, and time. Is a particular feature worth delaying the release?
Line 183: Should we hire one more developer so that a particular feature can be included
Line 184: in the upcoming release? Should we release in June or hold off until August and
Line 185: have more features? Should we buy this development tool? To make these deci-
Line 186: sions we need estimates of both the costs and benefits.
Line 187: Establishing Trust
Line 188: Frequent reliable delivery of promised features builds trust between the develop-
Line 189: ers of a product and the customers of that product. Reliable estimates enable re-
Line 190: liable delivery. A customer needs estimates to make important prioritization and
Line 191: tradeoff decisions. Estimates also help a customer decide how much of a feature
Line 192: to develop. Rather than investing twenty days and getting everything, perhaps
Line 193: investing ten days of effort will yield 80% of the benefit. Customers are reluctant
Line 194: to make these types of tradeoff decisions early in a project unless the developers’
Line 195: estimates have proved trustworthy.
Line 196: Reliable estimates benefit developers by allowing them to work at a sustain-
Line 197: able pace. This leads to higher-quality code and fewer bugs. These, in turn, lead
Line 198: 
Line 199: --- 페이지 39 ---
Line 200: 8
Line 201: |
Line 202: Chapter 1
Line 203: The Purpose of Planning
Line 204: back to more reliable estimates because less time is spent on highly unpredict-
Line 205: able work such as bug fixing. 
Line 206: Conveying Information
Line 207: A plan conveys expectations and describes one possibility of what may come to
Line 208: pass over the course of a project. A plan does not guarantee an exact set of fea-
Line 209: tures on an exact date at a specified cost. A plan does, however, communicate
Line 210: and establish a set of baseline expectations. Far too often a plan is reduced to a
Line 211: single date, and all of the assumptions and expectations that led to that date are
Line 212: forgotten.
Line 213: Suppose you ask me when a project will be done. I tell you seven months but
Line 214: provide no explanation of how I arrived at that duration. You should be skeptical
Line 215: of my estimate. Without additional information you have no way of determining
Line 216: whether I’ve thought about the question sufficiently or whether my estimate is
Line 217: realistic. 
Line 218: Suppose, instead, that I provide you a plan that estimates completion in
Line 219: seven to nine months, shows what work will be completed in the first one or two
Line 220: months, documents key assumptions, and establishes an approach for how we’ll
Line 221: collaboratively measure progress. In this case you can look at my plan and draw
Line 222: conclusions about the confidence you should have in it. 
Line 223: What Makes a Good Plan?
Line 224: A good plan is one that stakeholders find sufficiently reliable that they can use it
Line 225: as the basis for making decisions. Early in a project, this may mean that the plan
Line 226: says that the product can be released in the third quarter, rather than the sec-
Line 227: ond, and that it will contain approximately a described set of features. Later in
Line 228: the project, to remain useful for decision making, this plan will need to be more
Line 229: precise.
Line 230: Suppose you are estimating and planning a new release of the company’s
Line 231: flagship product. You determine that the new version will be ready for release in
Line 232: six months. You create a plan that describes a set of features that are certain to
Line 233: be in the new version and another set of features that may or may not be in-
Line 234: cluded, depending on how well things progress. 
Line 235: Others in the company can use this plan to make decisions. They can pre-
Line 236: pare marketing materials, schedule an advertising campaign, allocate resources
Line 237: to assist with upgrading key customers, and so on. This plan is useful—as long
Line 238: 
Line 239: --- 페이지 40 ---
Line 240: What Makes Planning Agile? 
Line 241: |
Line 242: 9
Line 243: as it is somewhat predictive of what actually happens on the project. If develop-
Line 244: ment takes twelve months instead of the planned six, this was not a good plan. 
Line 245: However, if the project takes seven months instead of six, the plan was prob-
Line 246: ably still useful. Yes, the plan was incorrect, and yes, it may have led to some
Line 247: slightly mistimed decisions. But a seven-month delivery of an estimated six-
Line 248: month project is generally not the end of the world and is certainly within the
Line 249: PMI’s margin of error for a budgetary estimate. The plan, although inaccurate,
Line 250: was even more likely useful if we consider that it should have been updated reg-
Line 251: ularly throughout the course of the project. In that case, the one-month late de-
Line 252: livery should not have been a last-minute surprise to anyone. 
Line 253: What Makes Planning Agile?
Line 254: This book is about agile planning, not agile plans. Plans are documents or fig-
Line 255: ures; they are snapshots of how we believe a project might unfold over an uncer-
Line 256: tain future. Planning is an activity. Agile planning shifts the emphasis from the
Line 257: plan to the planning. 
Line 258: Agile planning balances the effort and investment in planning with the
Line 259: knowledge that we will revise the plan through the course of the project. An
Line 260: agile plan is one that we are not only willing, but also eager to change. We don’t
Line 261: want to change the plan just for the sake of changing, but we want to change be-
Line 262: cause change means we’ve learned something or that we’ve avoided a mistake.
Line 263: We may have learned that users want more of this feature or that they want less
Line 264: of that feature or that usability is more important than we’d believed or that pro-
Line 265: gramming in this new language takes longer than we’d expected. The financial
Line 266: impact of each of these changes can be assessed and, if worthy, can alter the plan
Line 267: and schedule.
Line 268: As we discover these things, they affect our plans. This means we need plans
Line 269: that are easily changed. This is why the planning becomes more important than
Line 270: the plan. The knowledge and insight we gain from planning persists long after
Line 271: one plan is torn up and a revised one put in its place. So an agile plan is one that
Line 272: is easy to change. 
Line 273: Just because we’re changing the plan does not mean we change the dates.
Line 274: We may or may not do that. But if we learn we were wrong about some aspect of
Line 275: the target product and need to do something about it, the plan needs to change.
Line 276: There are many ways we can change the plan without changing the date. We can
Line 277: drop a feature, we can reduce the scope of a feature, we can possibly add people
Line 278: to the project, and so on.
Line 279: 
Line 280: --- 페이지 41 ---
Line 281: 10
Line 282: |
Line 283: Chapter 1
Line 284: The Purpose of Planning
Line 285: Because we acknowledge that we cannot totally define a project at its outset,
Line 286: it is important that we do not perform all of a project’s planning at the outset.
Line 287: Agile planning is spread more or less evenly across the duration of a project. Re-
Line 288: lease planning sets the stage and is followed by a number of rounds of iteration
Line 289: planning, after which the entire process is repeated perhaps a handful of times
Line 290: on a project.
Line 291: So in defining agile planning we find that it
Line 292: ◆Is focused more on the planning than on the plan
Line 293: ◆Encourages change
Line 294: ◆Results in plans that are easily changed
Line 295: ◆Is spread throughout the project
Line 296: Summary
Line 297: Estimating and planning are critical, yet are difficult and error prone. We cannot
Line 298: excuse ourselves from these activities just because they are hard. Estimates
Line 299: given early in a project are far less accurate than those given later. This progres-
Line 300: sive refinement is shown in the cone of uncertainty. 
Line 301: The purpose of planning is to find an optimal answer to the overall product
Line 302: development question of what to build. The answer incorporates features, re-
Line 303: sources, and schedule. Answering this question is supported by a planning pro-
Line 304: cess that reduces risk, reduces uncertainty, supports reliable decision making,
Line 305: establishes trust, and conveys information.
Line 306: A good plan is one that is sufficiently reliable that it can be used as the basis
Line 307: for making decisions about the product and the project. Agile planning is fo-
Line 308: cused more on the planning than on the creation of a plan, encourages change,
Line 309: results in plans that are easily changed, and is spread throughout the project.
Line 310: Discussion Questions
Line 311: 1. This chapter started by making the claim that overplanning and doing no
Line 312: planning are equally dangerous. What is the right amount of planning on
Line 313: your current project?
Line 314: 2. What other reasons can you think of for planning?
Line 315: 3. Think of one or two of the most successful projects in which you have been
Line 316: involved. What role did planning play in those projects?
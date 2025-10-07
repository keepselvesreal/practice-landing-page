Line 1: 
Line 2: --- 페이지 42 ---
Line 3: 11
Line 4: Chapter 2
Line 5: Why Planning Fails
Line 6: “No plan survives contact with the enemy.”
Line 7: —Field Marshal Helmuth Graf von Moltke
Line 8: The previous chapter made the argument that the purpose of planning is to ar-
Line 9: rive iteratively at an optimized answer to the ultimate new product development
Line 10: question of what should be developed. That is, what capabilities should the prod-
Line 11: uct exhibit, in what timeframe, and with which and how many resources? We
Line 12: learned that planning supports this by reducing risk, by reducing uncertainty
Line 13: about what the product should be, by supporting better decision making, by es-
Line 14: tablishing trust, and by conveying information. 
Line 15: Unfortunately, the traditional ways in which we plan projects often let us
Line 16: down. In answering the combined scope/schedule/resources question for a new
Line 17: product, our traditional planning processes do not always lead to very satisfac-
Line 18: tory answers and products. As support of this, consider that:
Line 19: ◆Nearly two-thirds of projects significantly overrun their cost estimates (Led-
Line 20: erer and Prasad 1992)
Line 21: ◆Sixty-four percent of the features included in products are rarely or never
Line 22: used (Johnson 2002)
Line 23: ◆The average project exceeds its schedule by 100% (Standish 2001)
Line 24: In this chapter, we look at five causes of planning failure.
Line 25: 
Line 26: --- 페이지 43 ---
Line 27: 12
Line 28: |
Line 29: Chapter 2
Line 30: Why Planning Fails
Line 31: Planning Is by Activity Rather Than Feature
Line 32: A critical problem with traditional approaches to planning is that they focus on
Line 33: the completion of activities rather than on the delivery of features. A tradition-
Line 34: ally managed project’s Gantt chart or work breakdown structure identifies the
Line 35: activities that will be performed. This becomes how we measure the progress of
Line 36: the team. A first problem with activity-based planning is that customers get no
Line 37: value from the completion of activities. Features are the unit of customer value.
Line 38: Planning should, therefore, be at the level of features, not activities.
Line 39: A second problem occurs after a traditional schedule has been created and is
Line 40: being reviewed. When we review a schedule showing activities, we do so looking
Line 41: for forgotten activities rather than for missing features.
Line 42: Further problems occur because activity-based plans often lead to projects
Line 43: that overrun their schedules. When faced with overrunning a schedule, some
Line 44: teams attempt to save time by inappropriately reducing quality. Other teams in-
Line 45: stitute change-control policies designed to constrain product changes, even
Line 46: highly valuable changes. Some of the reasons why activity-based planning leads
Line 47: to schedule overruns include
Line 48: ◆Activities don’t finish early.
Line 49: ◆Lateness is passed down the schedule.
Line 50: ◆Activities are not independent.
Line 51: Each of these problems is described in the following sections.
Line 52: Activities Don’t Finish Early
Line 53: A few years ago I had two main projects that needed my time. I was program-
Line 54: ming some interesting new features for a product. I also needed to prepare doc-
Line 55: umentation for an ISO 9001 compliance audit. The programming was fun.
Line 56: Writing documents for the compliance audit wasn’t. Not surprisingly, I managed
Line 57: to expand the scope of the programming work so that it filled almost all my time
Line 58: and left me the bare minimum of time to prepare for the audit.
Line 59: I’m not the only one who does this. In fact, this behavior is so common that
Line 60: it has a name, Parkinson’s Law (1993), which states:
Line 61: Work expands so as to fill the time available for its completion.
Line 62: Parkinson is saying that we take as much time to complete an activity as we
Line 63: think we’ll be allowed. If there’s a Gantt chart hanging on the wall that says an
Line 64: activity is expected to take five days, the programmer assigned to that activity
Line 65: 
Line 66: --- 페이지 44 ---
Line 67: Lateness Is Passed Down the Schedule 
Line 68: |
Line 69: 13
Line 70: will generally make sure the activity takes the full five days. She may do this by
Line 71: adding a few bells and whistles if it looks like she’ll finish early (a practice known
Line 72: as gold-plating). Or she may split time between the activity and researching
Line 73: some hot new technology she thinks may be useful. What she will not do very of-
Line 74: ten is finish the activity early. In many organizations, if she finishes early, her
Line 75: boss may accuse her of having given a padded estimate. Or her boss may expect
Line 76: her to finish more activities early. Why risk either of these scenarios when a little
Line 77: web surfing can make the activity come in on schedule instead?
Line 78: When a Gantt chart shows that an activity is expected to take five days, it
Line 79: gives implicit permission to the developer to take up to that long to complete. It
Line 80: is human nature when ahead of that schedule to fill the extra time with other
Line 81: work that we, but perhaps not others, value.
Line 82: Lateness Is Passed Down the Schedule
Line 83: Because traditional plans are activity based, in large measure they focus on the
Line 84: dependencies between activities. Consider the Gantt chart shown in Figure 2.1,
Line 85: which shows four activities and their dependencies. An early start for testing re-
Line 86: quires the fortuitous confluence of these events:
Line 87: ◆Coding of the middle tier finishes early, which is influenced by when adding
Line 88: tables to the database is finished.
Line 89: ◆Coding of the user interface finishes early.
Line 90: ◆The tester is available early.
Line 91: Figure 2.1 Testing will start late if anything goes worse than planned; it will start 
Line 92: early only if everything goes better than planned.
Line 93: Add tables to database
Line 94: Code middle tier
Line 95: Test
Line 96: Code the user interface
Line 97: 
Line 98: --- 페이지 45 ---
Line 99: 14
Line 100: |
Line 101: Chapter 2
Line 102: Why Planning Fails
Line 103: The key here is that even in this simple case there are three things that all
Line 104: must occur for an early start on testing. Although multiple things must occur
Line 105: for testing to start early, any one of the following can cause testing to start late:
Line 106: ◆Coding the user interface finishes late.
Line 107: ◆Coding the middle tier takes longer than planned to complete and finishes
Line 108: late.
Line 109: ◆Coding the middle tier takes the time planned but starts late because adding
Line 110: tables to the database finishes late.
Line 111: ◆The tester is unavailable.
Line 112: In other words, an early start requires a combination of things to go well; a
Line 113: late start can be caused by one thing going wrong.
Line 114: The problem is compounded because we’ve already established that activi-
Line 115: ties will rarely finish early. This means that activities will start late and that the
Line 116: lateness will get passed down the schedule. Because early completion is rare, it is
Line 117: even more rare that an activity such as testing in Figure 2.1 gets to start early. 
Line 118: Activities Are Not Independent
Line 119: Activities are said to be independent if the duration of one activity does not influ-
Line 120: ence the duration of another activity. In building a house, the amount of time it
Line 121: takes to excavate the basement is independent of the amount of time it will take
Line 122: to paint the walls. When activities are independent, a late finish on one activity
Line 123: can be offset by an early finish on another. Flipping a coin multiple times is an-
Line 124: other example of independent activities. A coin that lands on heads on the first
Line 125: flip is no more or less likely to land on heads on the second flip. 
Line 126: Are software development activities independent? Will the variations in
Line 127: completion times tend to balance out? Unfortunately, no. Many software activi-
Line 128: ties are not independent of one another. For example, if I’m writing the client
Line 129: portion of an application and the first screen takes 50% longer than scheduled,
Line 130: there is a good chance that each of the remaining screens is also going to take
Line 131: longer than planned. If the activities of a development effort are not indepen-
Line 132: dent, variations in completion time will not balance out.
Line 133: Many activities in a typical project plan are not independent, yet we contin-
Line 134: ually forget this. When someone is late on the first of a handful of similar items
Line 135: we’ve all heard or given the answer, “Yes, I was late this time, but I’ll make it up
Line 136: on the rest.” This stems from the belief that the knowledge gained from complet-
Line 137: ing the first activity will allow the remaining similar activities to be completed
Line 138: 
Line 139: --- 페이지 46 ---
Line 140: Multitasking Causes Further Delays 
Line 141: |
Line 142: 15
Line 143: more quickly than called for in the plan. The real knowledge we should gain in a
Line 144: situation like this is that when an activity takes longer than planned, all similar
Line 145: activities are also likely to take longer than planned. 
Line 146: Multitasking Causes Further Delays
Line 147: A second reason why traditional approaches to planning often fail is multitask-
Line 148: ing, which is defined as simultaneously working on multiple tasks. Multitasking
Line 149: exacts a horrible toll on productivity. Clark and Wheelwright (1993) studied the
Line 150: effects of multitasking and found that the time an individual spends on value-
Line 151: adding work drops rapidly when the individual is working on more than two
Line 152: tasks. This is illustrated in Figure 2.2, which is based on their results.
Line 153: Figure 2.2 Effect of multitasking on productivity.
Line 154: Logically, it makes sense that multitasking helps when you have two things
Line 155: to work on; if you become blocked on one, you can switch to the other. It is also
Line 156: logical that Figure 2.2 shows a rapid decline in time spent on value-adding tasks
Line 157: after a second task. We’re rarely blocked on more than one task at a time; and if
Line 158: we’re working on three or more concurrent tasks, the time spent switching
Line 159: among them becomes a much more tangible cost and burden.
Line 160: Multitasking often becomes an issue once a project starts to have some ac-
Line 161: tivities finish late. At that point dependencies between activities become critical.
Line 162: 90
Line 163: 80
Line 164: 70
Line 165: 60
Line 166: 50
Line 167: 40
Line 168: 30
Line 169: 20
Line 170: 10
Line 171: 0
Line 172: 1
Line 173: 2
Line 174: 3
Line 175: 4
Line 176: 5
Line 177: Number of Concurrent Assigned Tasks
Line 178: Percent of Time on Tasks
Line 179: 
Line 180: --- 페이지 47 ---
Line 181: 16
Line 182: |
Line 183: Chapter 2
Line 184: Why Planning Fails
Line 185: A developer waiting on the work of another developer will ask that developer to
Line 186: deliver just a subset of work so that he may continue. Suppose I am to spend ten
Line 187: days working on some database changes, then ten days implementing an applica-
Line 188: tion programming interface (API) for accessing the database, and then ten days
Line 189: developing a user interface. This is illustrated in the top half of Figure 2.3. Your
Line 190: work is held up until you get the API from me. You ask me to do just enough of
Line 191: the API work so that you can get started. Similarly, the tester asks me to do just
Line 192: enough of the user interface so that she can begin automating tests. I agree, and
Line 193: my schedule becomes as shown in the bottom of Figure 2.3.
Line 194: Figure 2.3 Multitasking extends the completion date of work and leaves work in 
Line 195: process longer.
Line 196: This often gives the illusion of speed; but as shown in Figure 2.3, my data-
Line 197: base and API work finish later than originally planned. This is almost certain to
Line 198: ripple through and affect further activities in the plan. Additionally, in this ex-
Line 199: ample, each of the desired units of work remains in process for twenty days
Line 200: rather than ten, as was the case when the work was done serially. 
Line 201: To make matters worse, Figure 2.3 assumes that I am not slowed by switch-
Line 202: ing among these activities more frequently. The Clark and Wheelwright study
Line 203: indicates that a loss in productivity will occur.
Line 204: Multitasking becomes a problem on a traditionally planned project for two
Line 205: primary reasons. First, work is typically assigned well in advance of when the
Line 206: work will begin, and it is impossible to allocate work efficiently in advance. As-
Line 207: signing work to individuals rather than to groups exacerbates the problem. Sec-
Line 208: ond, it encourages focusing on achieving a high level of utilization of all
Line 209: individuals on the project rather than on maintaining sufficient slack to cope
Line 210: with the inherent variability in typical project tasks. Loading everyone to 100%
Line 211: of capacity has the same effect as loading a highway to 100% of capacity: No one
Line 212: can make any progress. 
Line 213: Database
Line 214: 10
Line 215: DB
Line 216: API
Line 217: API
Line 218: 10
Line 219: UI
Line 220: DB
Line 221: User Interface
Line 222: 10
Line 223: API
Line 224: UI
Line 225: 20
Line 226: 20
Line 227: 20
Line 228: 
Line 229: --- 페이지 48 ---
Line 230: We Ignore Uncertainty 
Line 231: |
Line 232: 17
Line 233: Features Are Not Developed by Priority
Line 234: A third reason why traditional planning fails to lead consistently to high-value
Line 235: products is because the work described by the plan is not prioritized by its value
Line 236: to the users and customer. Many traditional plans are created with the assump-
Line 237: tion that all identified activities will be completed. This means that work is typi-
Line 238: cally prioritized and sequenced for the convenience of the development team.
Line 239: Traditional thinking says that if all work will be completed, project custom-
Line 240: ers have no preference about the sequence in which that work is done. This leads
Line 241: to the development team’s working on features in what appears to the customer
Line 242: to be a relatively haphazard order. Then, with the end of the project approaching,
Line 243: the team scrambles to meet the schedule by dropping features. Because there
Line 244: was no attempt to work on features in order of priority, some of the features
Line 245: dropped are of greater value than those that are delivered.
Line 246: We Ignore Uncertainty
Line 247: A fourth shortcoming with traditional approaches to planning is the failure to
Line 248: acknowledge uncertainty. We ignore uncertainty about the product and assume
Line 249: that the initial requirements analysis led to a complete and perfect specification
Line 250: of the product. We assume that users will not change their minds, refine their
Line 251: opinions, or come up with new needs during the period covered by the plan. 
Line 252: Similarly, we ignore uncertainty about how we will build the product and
Line 253: pretend we can assign precise estimates (“two weeks”) to imprecise work. We
Line 254: cannot hope to identify every activity that will be needed in the course of a
Line 255: project. Yet we often fail to acknowledge this in the plans we create. 
Line 256: Even with all this uncertainty, schedules are often expressed as a single, un-
Line 257: qualified date: “We will ship on June 30,” for example. During the earliest part of
Line 258: a project we are the most uncertain. The estimates we give should reflect our un-
Line 259: certainty. One way of doing this is by expressing the end date as a range: “We’ll
Line 260: ship sometime between June and August,” for example. As the project progresses
Line 261: and as uncertainty and risk are removed from the project, estimates can be re-
Line 262: fined and made more precise. This was the point of the cone of uncertainty in
Line 263: Chapter 1, “The Purpose of Planning.”
Line 264: The best way of dealing with uncertainty is to iterate. To reduce uncertainty
Line 265: about what the product should be, work in short iterations, and show (or, ideally,
Line 266: give) working software to users every few weeks. Uncertainty about how to de-
Line 267: velop the product is similarly reduced by iterating. For example, missing tasks
Line 268: 
Line 269: --- 페이지 49 ---
Line 270: 18
Line 271: |
Line 272: Chapter 2
Line 273: Why Planning Fails
Line 274: can be added to plans, bad estimates can be corrected, and so on. In this way, the
Line 275: focus shifts from the plan to the planning.
Line 276: Estimates Become Commitments
Line 277: Embedded within every estimate is a probability that the work will be completed
Line 278: in the estimated time. Suppose your team has been asked to develop a new high-
Line 279: end word processor. The probability of finishing this by the end of the week is
Line 280: 0%. The probability of finishing it in ten years is 100%. If I ask you for an esti-
Line 281: mate, and you tell me the end of the week, that estimate comes with a probability
Line 282: of 0%. If the estimate you give me is ten years, that estimate comes with a prob-
Line 283: ability of 100%. Each estimate between the end of the week and ten years from
Line 284: now comes with its own probability between 0% and 100% (Armour 2002). 
Line 285: A problem with traditional planning can arise if the project team or its stake-
Line 286: holders equate estimating with committing. As Phillip Armour (2002) points
Line 287: out, an estimate is a probability, and a commitment cannot be made to a proba-
Line 288: bility. Commitments are made to dates. Normally the date that a team is asked
Line 289: (or told) to commit to is one to which they would assign a less-than-100% prob-
Line 290: ability. Before making such a commitment, the team needs to assess a variety of
Line 291: business factors and risks. It is important that they be given this opportunity,
Line 292: and that every estimate does not become an implicit commitment.
Line 293: Summary
Line 294: After looking through this list of problems with traditional approaches to plan-
Line 295: ning, it’s no wonder so many projects are disappointing. Activity-based planning
Line 296: distracts our attention from features, which are the true unit of customer value.
Line 297: A variety of problems then leads to the likelihood of delivering late against a
Line 298: schedule derived from an activity-based plan. With good intentions, project par-
Line 299: ticipants view multitasking as a possible cure but are eventually forced even fur-
Line 300: ther behind schedule because of the hidden costs of multitasking. When the
Line 301: project schedule runs out of time, features are inevitably dropped. Because fea-
Line 302: tures are developed in the order deemed most efficient by the developers, the
Line 303: dropped features are not necessarily those with the lowest value to users.
Line 304: Ignoring uncertainty about exactly what users will eventually want can lead
Line 305: to completing a project on schedule but without including important capabilties
Line 306: that were identified after the plan was created. Also ignoring uncertainty about
Line 307: how the product will be developed leads to missed activities in the project plan.
Line 308: 
Line 309: --- 페이지 50 ---
Line 310: Discussion Questions 
Line 311: |
Line 312: 19
Line 313: This in turn increases the likelihood that the project will be late, that features
Line 314: will be dropped at the end, or that inappropriate quality tradeoffs may be made.
Line 315: Many organizations confuse estimates with commitments. As soon as a team
Line 316: expresses an estimate, they are forced to commit to it. 
Line 317: Discussion Questions
Line 318: 1. What problems result from plans being based on activities rather than deliv-
Line 319: erable features?
Line 320: 2. In your current environment, is an estimate the same as a commitment?
Line 321: What problems does this cause? What could you do to change this misper-
Line 322: ception?
Line 323: 3. In what ways does multitasking affect your current project? How could you
Line 324: reduce that impact?
Line 325: 
Line 326: --- 페이지 51 ---
Line 327: This page intentionally left blank 
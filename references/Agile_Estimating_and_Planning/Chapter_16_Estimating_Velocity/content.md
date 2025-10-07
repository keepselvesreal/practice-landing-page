Line 1: 
Line 2: --- 페이지 208 ---
Line 3: 177
Line 4: Chapter 16
Line 5: Estimating Velocity
Line 6: “It is better to be roughly right
Line 7: than precisely wrong.”
Line 8: —John Maynard Keynes
Line 9: One of the challenges of planning a release is estimating the velocity of the team.
Line 10: You have the following three options:
Line 11: ◆Use historical values.
Line 12: ◆Run an iteration.
Line 13: ◆Make a forecast.
Line 14: There are occasions when each of these approaches is appropriate. However,
Line 15: regardless of which approach you are using, if you need to estimate velocity you
Line 16: should consider expressing the estimate as a range. Suppose you estimate that
Line 17: velocity for a given team on a given project will be 20 ideal days per iteration.
Line 18: You have a very limited chance of being correct. Velocity may be 21, or 19, or
Line 19: maybe even 20.0001. So instead of saying velocity will be 20, give your estimate
Line 20: as a range, saying perhaps instead that you estimate velocity will be between 15
Line 21: and 24. 
Line 22: In the following sections, I’ll describe each of the three general ap-
Line 23: proaches—using historicals, running an iteration, and making a forecast—and
Line 24: for each, I’ll also offer advice on selecting an appropriate range.
Line 25: 
Line 26: --- 페이지 209 ---
Line 27: 178 |
Line 28: Chapter 16
Line 29: Estimating Velocity
Line 30: Use Historical Values
Line 31: Historical values are great—if you have them. The problem with historical val-
Line 32: ues is that they’re of the greatest value when very little has changed between the
Line 33: old project and team and the new project and team. Any personnel or significant
Line 34: technology changes will reduce the usefulness of historical measures of velocity.
Line 35: Before using them, ask yourself questions like these:
Line 36: ◆Is the technology the same?
Line 37: ◆Is the domain the same?
Line 38: ◆Is the team the same?
Line 39: ◆Is the product owner the same?
Line 40: ◆Are the tools the same?
Line 41: ◆Is the working environment the same?
Line 42: ◆Were the estimates made by the same people?
Line 43: The answer to each question is often yes when the team is moving onto a
Line 44: new release of a product they just worked on. In that case, using the team’s his-
Line 45: torical values is entirely appropriate. Even though velocity in a situation like this
Line 46: is relatively stable, you should still consider expressing it as a range. You could
Line 47: create a range by simply adding and subtracting a few points to the average or by
Line 48: looking at the team’s best and worst iterations over the past two or three
Line 49: months.
Line 50: However, if the answer to any of the preceding questions is no, you may want
Line 51: to think twice about using historical velocities. Or you may want to use histori-
Line 52: cal velocities but put a larger range around them to reflect the inherent uncer-
Line 53: tainty in the estimate. To do this, start by calculating the team’s average velocity
Line 54: over the course of the preceding release. If they completed 150 story points of
Line 55: work during 10 iterations, their average (mean) velocity was 15 points.
Line 56: Before showing how to convert this to a range, take a look at Figure 16.1.
Line 57: This figure shows the cone of uncertainty that was introduced back in Chapter 1,
Line 58: “The Purpose of Planning.” The cone of uncertainty says that the actual duration
Line 59: of a project will be between 60% and 160% of what we think it is. So to turn our
Line 60: single-point, average velocity into a range, I multiply it by 60% and 160%.1 So if
Line 61: 1. Technically, I should divide it by 0.60 and 1.6. However, because 0.60 and 1.60 are
Line 62: meant to be reciprocals (
Line 63: ), you get approximately the same values
Line 64: by multiplying. 
Line 65: 0.6
Line 66: 1.6
Line 67: u
Line 68: 0.96
Line 69: 1
Line 70: #
Line 71: =
Line 72: 
Line 73: --- 페이지 210 ---
Line 74: Run an Iteration 
Line 75: |
Line 76: 179
Line 77: our average historical velocity is 15, I would estimate velocity to be in the range
Line 78: of 9 to 24.
Line 79: Figure 16.1 The cone of uncertainty around schedule estimates.
Line 80: This range may feel large, but given the uncertainty at this point, it is prob-
Line 81: ably appropriate. Constructing a range in this way helps the project team heed
Line 82: the advice offered in the quote at the start of this chapter that it is better to be
Line 83: roughly right than precisely wrong. A large range around the expected velocity
Line 84: will allow the team to be roughly right about it.
Line 85: Run an Iteration
Line 86: An ideal way to forecast velocity is to run an iteration (or two or three) and then
Line 87: estimate velocity from the observed velocity during the one to three iterations.
Line 88: Because the best way to predict velocity is to observe velocity, this should always
Line 89: be your default approach. Many traditional projects get under way with the
Line 90: Project 
Line 91: Schedule
Line 92: Approved
Line 93: Product
Line 94: Definition
Line 95: Requirements
Line 96: Specification
Line 97: Initial
Line 98: Product
Line 99: Definition
Line 100: Detailed
Line 101: Design
Line 102: Specification
Line 103: Accepted
Line 104: Software
Line 105: 1.6x
Line 106: 1.25x
Line 107: 1.15x
Line 108: Product
Line 109: Design
Line 110: Specification
Line 111: 1.1x
Line 112: x
Line 113: 0.9x
Line 114: 0.85x
Line 115: 0.8x
Line 116: 0.6x
Line 117: 
Line 118: --- 페이지 211 ---
Line 119: 180 |
Line 120: Chapter 16
Line 121: Estimating Velocity
Line 122: developers working on the “obvious” requirements or infrastructure, the ana-
Line 123: lysts “finalizing” the requirements, and the project manager putting together a
Line 124: comprehensive list of tasks that becomes the project plan. All of this takes
Line 125: time—often, as long as a few iterations on an agile project. 
Line 126: I was with a development director recently who said that deadlines are not
Line 127: set on traditional projects in his company until about two months into a year-
Line 128: long project. It takes them that long to get the requirements “locked down” and
Line 129: a plan created. He told me that even after that much effort, their project plans
Line 130: were always off at least 50% and often more. We agreed that instead, he would
Line 131: use this up-front time to turn the team loose on the project, observe their veloc-
Line 132: ity over two or three iterations, and then use that to plan a release date. 
Line 133: For similar reasons, as was the case with this development director, most
Line 134: project managers can hold off giving an estimate for at least one iteration. If
Line 135: that’s your case, use the time to run an iteration and measure the velocity. Then
Line 136: create a range around that one data point, using the cone of uncertainty. So if
Line 137: you ran one iteration and had a velocity of 15, turn it into a range by multiplying
Line 138: by 0.60 and 1.6, giving a range of 9 to 24.
Line 139: If a team can run three or more iterations before being giving an estimate of
Line 140: velocity, they have a couple of additional options for determining a range. First
Line 141: and easiest, they can simply use the range of observed values. Suppose the team
Line 142: has completed three iterations and had velocities of 12, 15, and 16. They could
Line 143: express velocity as likely to be within the range 12 to 16.
Line 144: Alternatively, they could again use the cone of uncertainty. Although there’s
Line 145: no solid empirical basis for the approach I’m about to describe, it does work, and
Line 146: it makes sense. Here’s the approach: Calculate the average velocity for the itera-
Line 147: tions you’ve run. Then, for each iteration completed, move one step to the right
Line 148: on the cone of uncertainty. So for a team that has run one iteration, use the
Line 149: range for the “initial product definition” milestone. If the team has run two iter-
Line 150: ations, use the range for the “approved product definition” milestone (80% to
Line 151: 120%), and so on. For convenience, these numbers are shown in Table 16.1.
Line 152: Table 16.1 Multipliers for Estimating Velocity Based on Number of Iterations Completed
Line 153: Iterations Completed
Line 154: Low Multiplier
Line 155: High Multiplier
Line 156: 1
Line 157: 0.6
Line 158: 1.60
Line 159: 2
Line 160: 0.8
Line 161: 1.25
Line 162: 3
Line 163: 0.85
Line 164: 1.15
Line 165: 4 or more
Line 166: 0.90
Line 167: 1.10
Line 168: 
Line 169: --- 페이지 212 ---
Line 170: Make a Forecast 
Line 171: |
Line 172: 181
Line 173: Suppose that a team has run three iterations with an average velocity of
Line 174: twenty during that period. For three iterations the appropriate range is 85% to
Line 175: 115%. This means that if the team’s average velocity is twenty after three itera-
Line 176: tions, their actual true velocity by the end of the project will probably be in the
Line 177: range seventeen to twenty-three.
Line 178: I normally don’t extend this analysis past three or four iterations. I don’t use
Line 179: the cone of uncertainty, for example, to pretend that after six iterations, the team
Line 180: precisely knows their velocity, and it won’t waver through the end of the project. 
Line 181: Some organizations will resist starting a project without having a more spe-
Line 182: cific idea how long it will take. In such cases, stress that the need to run a few
Line 183: iterations first stems not from a desire to avoid making an estimate, but to avoid
Line 184: giving an estimate without adequate foundation. You’ll want to stress that the
Line 185: purpose of these initial iterations is to assess the dark corners of the system, bet-
Line 186: ter understand the technologies involved, refine the understanding of the re-
Line 187: quirements, and measure how quickly the team can make progress.
Line 188: Make a Forecast
Line 189: There are times when we don’t have historicals, and it is just not feasible to run
Line 190: a few iterations to observe velocity. Suppose the estimate is for a project that
Line 191: won’t start for twelve months. Or suppose the project may start soon, but only
Line 192: once a client signs a contract for the work. There are two key differences in cases
Line 193: like this. First, you want to minimize the expenditure on the project so you
Line 194: won’t actually start running iterations on a project that may not happen or that
Line 195: is too far in the future. Second, any estimate of velocity on these projects must
Line 196: reflect a high degree of uncertainty. 
Line 197: In cases like these, we need to forecast velocity. Forecasting velocity is rarely
Line 198: your first option, but it’s an important option and one you should have in your
Line 199: bag of tricks. The best way to forecast velocity involves expanding user stories
Line 200: into their constituent tasks, estimating those tasks (as we do when planning an
Line 201: iteration), seeing how much work fits into an iteration, and then calculating the
Line 202: velocity that would be achieved if that work were finished in an iteration. This
Line 203: involves the following steps:
Line 204: 1. Estimate the number of hours that each person will be available to work on
Line 205: the project each day.
Line 206: 2. Determine the total number of hours that will be spent on the project dur-
Line 207: ing the iteration.
Line 208: 
Line 209: --- 페이지 213 ---
Line 210: 182 |
Line 211: Chapter 16
Line 212: Estimating Velocity
Line 213: 3. Arbitrarily and somewhat randomly select stories, and expand them into
Line 214: their constituent tasks. Repeat until you have identified enough tasks to fill
Line 215: the number of hours in the iteration.
Line 216: 4. Convert the velocity determined in the preceding step into a range.
Line 217: Let’s see how this works through an example.
Line 218: Estimate the Hours Available
Line 219: Almost everyone has some responsibilities outside of the specific project that is
Line 220: their primary responsibility. There are emails to be answered, phone calls to be
Line 221: returned, company meetings to attend, and so on. The amount of time this takes
Line 222: differs from person to person and organization to organization. What it amounts
Line 223: to, though, is that project participants generally do not spend 100% of their time
Line 224: working on the project.
Line 225: From observation and discussion with colleagues, my opinion is that most
Line 226: individuals who are assigned full time to a project spend between four and six
Line 227: hours per day on that project. This fits with reports that individuals spend 55%
Line 228: (Ganssle 2004) to 70% (Boehm 1981) of their time on project activities. At the
Line 229: high end, Kennedy (2003) reports that engineers in Toyota—with its highly effi-
Line 230: cient, lean process—are able to spend 80% of their time on their designated
Line 231: projects.
Line 232: Use these numbers as parameters in estimating the amount of time individ-
Line 233: uals on your project team will be able to dedicate each day to the project. If you
Line 234: are part of a large bureaucracy, you will most likely be at the low end of the scale.
Line 235: If you are part of a three-person start-up in a garage, you’ll probably be at the
Line 236: high end. For the purposes of this example, let’s assume that the SwimStats
Line 237: team estimates they will each be able to dedicate six hours per day to the project.
Line 238: Estimate the Time Available in an Iteration
Line 239: This step is simple: Multiply the number of hours available each day by the num-
Line 240: ber of people on the team and the number of days in each iteration. Suppose the
Line 241: SwimStats team includes one analyst, one programmer, one database engineer,
Line 242: and one tester. Four people each working six hours per day is twenty-four hours
Line 243: each day. In a ten-day iteration they put about 240 hours toward the project.
Line 244: When I introduce this approach to some teams, they want to factor in addi-
Line 245: tional adjustments for vacations, sick time, and other such interruptions. Don’t
Line 246: bother; it’s not worth the extra effort, and it’s unlikely to be more accurate
Line 247: 
Line 248: --- 페이지 214 ---
Line 249: Expand Stories and See What Fits 
Line 250: |
Line 251: 183
Line 252: anyway. These events are part of the reason why we don’t plan on a team’s being
Line 253: 100% available in the first place.
Line 254: Expand Stories and See What Fits
Line 255: The next step is to expand stories into tasks, estimate the tasks, and keep going
Line 256: until we’ve filled the estimated number of available hours (240, in this case). It is
Line 257: not necessary that stories be expanded in priority order. What you really want is
Line 258: a fairly random assortment of stories. Do not, for example, expand all the one-
Line 259: and two-point stories and none of the three- and five-point stories. Similarly, do
Line 260: not expand only stories that involve mostly the user interface or the database.
Line 261: Try to find a representative set of stories.
Line 262: Continue selecting stories and breaking them into tasks as long as the tasks
Line 263: selected do not exceed the capacity of the individuals on the team. For the Swim-
Line 264: Stats team, for example, we need to be careful that we don’t assume the pro-
Line 265: grammer and analyst are also fully proficient database engineers. Select stories
Line 266: until one skill set on the team can’t handle any more work. Add up the story
Line 267: points or ideal days for the work selected, and that is the team’s possible velocity.
Line 268: Suppose we get the planned team together (or a proxy for them if the project
Line 269: will not start for a year), and we expand some stories as shown in Table 16.2. If
Line 270: we felt that the four-person SwimStats team could commit to this but probably
Line 271: no more, we’d stop here. This 221 hours of work seems like a reasonable fit
Line 272: within their 240 hours of available time. Our point estimate of velocity is then
Line 273: twenty-five.
Line 274: Getting More Time on Your Project
Line 275: Regardless of how many hours team members are able to put toward a
Line 276: project each day, you’d probably like to increase that number. The best
Line 277: technique I’ve found for doing so was invented by Francesco Cirillo of
Line 278: XPLabs. Cirillo coaches teams to work in highly focused thirty-minute in-
Line 279: crements (Cirillo 2005). Each thirty-minute increment consists of two
Line 280: parts: twenty-five minutes of intense work followed by a five-minute
Line 281: break. These thirty-minute increments are called “pomodori,” Italian for
Line 282: tomatoes and deriving from the use of tomato-shaped timers that ring
Line 283: when the twenty-five-minute period is complete.
Line 284: Cirillo introduced this technique to Piergiuliano Bossi, who has docu-
Line 285: mented its success with multiple teams (Bossi 2003; Bossi and Cirillo
Line 286: 2001). These teams would plan on completing ten pomodori (five hours)
Line 287: per day. If you find yourself with less productive time per day than you’d
Line 288: like, you may want to consider this approach.
Line 289: 
Line 290: --- 페이지 215 ---
Line 291: 184 |
Line 292: Chapter 16
Line 293: Estimating Velocity
Line 294: Put a Range Around It
Line 295: Use whatever technique you’d like to turn the point estimate of velocity into a
Line 296: range. As before, I like to multiply by 60% and 160%. For the SwimStats team,
Line 297: this means our estimate of twenty-five story points per iteration becomes an es-
Line 298: timate of fifteen to forty.
Line 299: A Variation for Some Teams
Line 300: Some teams—especially those with a significant number or part-time mem-
Line 301: bers—should not plan with a single number of hours that everyone is available.
Line 302: These teams may have members who are allocated for dramatically smaller por-
Line 303: tions of their time. In these cases, it can be useful to create a table like the one
Line 304: shown in Table 16.3.
Line 305: For the SwimStats team, as shown in Table 16.3, Yury and Sasha are dedi-
Line 306: cated full time to the project. SwimStats is Sergey’s only project, but he has
Line 307: Table 16.2 Hours and Points for Some SwimStats Stories
Line 308: Story
Line 309: Story 
Line 310: Points
Line 311: Hours for 
Line 312: Tasks
Line 313: As a coach, I can enter the names and demographic information 
Line 314: of all swimmers on my team.
Line 315: 3
Line 316: 24
Line 317: As a coach, I can define practice sessions.
Line 318: 5
Line 319: 45
Line 320: As a swimmer, I can see all of my times for a specific event.
Line 321: 2
Line 322: 18
Line 323: As a swimmer, I can update my demographics information.
Line 324: 1
Line 325: 14
Line 326: As a swimmer, I can see a line chart of my times for a particular 
Line 327: event.
Line 328: 2
Line 329: 14
Line 330: As a coach, I can see a line chart showing the progress over the 
Line 331: season of all of my swimmers in a particular event.
Line 332: 3
Line 333: 30
Line 334: As a swimmer, I can see a pie chart showing how many first, sec-
Line 335: ond, third, and lower places I’ve finished in.
Line 336: 2
Line 337: 12
Line 338: As a coach, I can see a text report showing each swimmer’s best 
Line 339: time in each event.
Line 340: 2
Line 341: 14
Line 342: As a coach, I can upload meet results from a file exported from 
Line 343: the timing system used at the meet.
Line 344: 5
Line 345: 50
Line 346: Total
Line 347: 25
Line 348: 221
Line 349: 
Line 350: --- 페이지 216 ---
Line 351: Which Approach Should I Use? 
Line 352: |
Line 353: 185
Line 354: some other managerial and corporate responsibilities that take up some of his
Line 355: time. Carina is split between SwimStats and another project. She has very few
Line 356: responsibilities beyond the two projects, and so she could put close to six hours
Line 357: per day on them. However, she needs to move back and forth between the two
Line 358: projects many times each day, and this multitasking affects her productivity, so
Line 359: she is shown as having only two productive hours on SwimStats per day.
Line 360: Which Approach Should I Use?
Line 361: Determining which approach to use is often simpler than this variety of choices
Line 362: may make it appear. Circumstances often guide you and constrain your options.
Line 363: In descending order of desirability, follow these guidelines to estimate velocity:
Line 364: ◆If you can run one or more iterations before giving an estimate of velocity,
Line 365: always do so. There’s no estimate like an actual, and seeing the team’s actual
Line 366: velocity is always your best choice.
Line 367: ◆Use the actual velocity from a related project by this team. 
Line 368: Table 16.3 Calculating Availability on a Team with Part-Time Members
Line 369: Person
Line 370: Available Hours
Line 371: per Day
Line 372: Available Hours
Line 373: per Iteration
Line 374: Sergey
Line 375: 4
Line 376: 40
Line 377: Yury
Line 378: 6
Line 379: 60
Line 380: Carina
Line 381: 2
Line 382: 20
Line 383: Sasha
Line 384: 6
Line 385: 60
Line 386: Total
Line 387: 180
Line 388: Remember Why We’re Doing This
Line 389: Keep in mind that the reason we’re forecasting velocity in this way is that
Line 390: it is either impossible or impractical for the team to run an iteration, and
Line 391: they do not yet have any historical observations. This may be the case be-
Line 392: cause the team doesn’t yet exist, and you are tasked with planning a
Line 393: project that starts a few months from now.
Line 394: If, for example, you are in an environment where you are doing stra-
Line 395: tegic planning and budgeting well in advance of initiating a project,
Line 396: forecasting velocity in this way can be your best approach.
Line 397: 
Line 398: --- 페이지 217 ---
Line 399: 186 |
Line 400: Chapter 16
Line 401: Estimating Velocity
Line 402: ◆Estimate velocity by seeing what fits.
Line 403: Regardless of which approach you use, switch to using actual, observed val-
Line 404: ues for velocity as soon as possible. Suppose that you choose to estimate velocity
Line 405: by seeing what fits in an iteration because the project is not set to begin for six
Line 406: months and the organization needs only a rough guess of how long the project
Line 407: will take. Once the project begins and you are able to measure actual velocity, be-
Line 408: gin using those actuals when discussing the project and its likely range of com-
Line 409: pletion dates.
Line 410: Summary
Line 411: There are three ways of estimating velocity. First, you can use historical averages
Line 412: if you have them. However, before using historical averages, you should consider
Line 413: whether there have been signficant changes in the team, the nature of the
Line 414: project, the technology, and so on. Second, you can defer estimating velocity un-
Line 415: til you’ve run a few iterations. This is usually the best option. Third, you can
Line 416: forecast velocity by breaking a few stories into tasks and seeing how much will fit
Line 417: into an iteration. This process is very similar to iteration planning.
Line 418: Regardless of which approach you use, estimates of velocity should be given
Line 419: in a range that reflects the uncertainty inherent in the estimate. The cone of un-
Line 420: certainty offers advice about the size of the range to use.
Line 421: Discussion Questions
Line 422: 1. In Table 16.2, stories that were estimated to have the same number of story
Line 423: points did not have the same number of task hours. Why? (If you need a re-
Line 424: fresher, see the section “Relating Task Estimates to Story Points” in
Line 425: Chapter 14, “Iteration Planning.”
Line 426: 2. Complete a table like Table 16.3 for your current project. What might you
Line 427: try to increase the amount of time each person is able to devote to the
Line 428: project?
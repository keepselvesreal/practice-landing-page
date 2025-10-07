Line 1: 
Line 2: --- 페이지 92 ---
Line 3: 61
Line 4: Chapter 7
Line 5: Re-Estimating
Line 6: “There’s no sense in being precise
Line 7: when you don’t even know what you’re talking about.”
Line 8: —John von Neumann
Line 9: One of the most common questions about estimating with story points or ideal
Line 10: days is “When do we re-estimate?” To arrive at an answer it is critical to remem-
Line 11: ber that story points and ideal days are estimates of the overall size and complex-
Line 12: ity of the feature being implemented. Story points in particular are not an
Line 13: estimate of the amount of time it takes to implement a feature, even though we
Line 14: often fall into the trap of thinking of them as such. The amount of time that im-
Line 15: plementing a feature will take is a function of its size (estimated in either ideal
Line 16: days or story points) and the team’s rate of progress (as reflected by its velocity).
Line 17: If we keep in mind that story points and ideal time estimate size, it’s easier to
Line 18: see that we should re-estimate only when we believe a story’s relative size has
Line 19: changed. When working with story points or ideal time, we do not re-estimate
Line 20: solely because a story took longer to implement than we thought. The best way
Line 21: to see this is through some examples.
Line 22: Introducing the SwimStats Website
Line 23: Throughout the rest of this chapter and some of the upcoming chapters, we will
Line 24: be working on SwimStats, a hypothetical website for swimmers and swim
Line 25: coaches. SwimStats will be sold as a service to competitive age-group, school,
Line 26: 
Line 27: --- 페이지 93 ---
Line 28: 62
Line 29: |
Line 30: Chapter 7
Line 31: Re-Estimating
Line 32: and college swim teams. Coaches will use it to keep track of their roster of swim-
Line 33: mers, organize workouts, and prepare for meets; swimmers will use the site to
Line 34: see meet results, check their personal records, and track improvements over
Line 35: time. Officials at swim meets will enter results into the system. A sample screen
Line 36: from SwimStats is shown in Figure 7.1.
Line 37: Figure 7.1 One screen from the SwimStats website.
Line 38: When Not to Re-Estimate
Line 39: Using SwimStats as an example, let’s first look briefly at a case when we should
Line 40: not re-estimate. Suppose we have the stories shown in Table 7.1. At the conclu-
Line 41: sion of the first iteration, the first two stories are complete. The team doesn’t feel
Line 42: good about this because they thought they would complete twice as many points
Line 43: (twelve rather than six) per iteration. They decide that each of those stories was
Line 44: twice as big or complex as initially thought, which is why they took twice as long
Line 45: as expected to complete. The team decides to double the number of story points
Line 46: associated with each. This means that their velocity was twelve (two six-point
Line 47: stories), which they feel better about.
Line 48: However, before the project started, the team considered all four stories of
Line 49: Table 7.1 to be of equivalent size and complexity, so each was estimated at three
Line 50: 
Line 51: --- 페이지 94 ---
Line 52: Velocity Is the Great Equalizer 
Line 53: |
Line 54: 63
Line 55: story points. Because they still believe these stories are equivalent, the estimates
Line 56: for Stories 3 and 4 must now also be doubled. The team has given themselves
Line 57: more points for the stories they completed, which doubled their velocity. But,
Line 58: because they also doubled the amount of work remaining in the project, their
Line 59: situation is the same as if they’d left all the estimates at three and velocity at six. 
Line 60: Velocity Is the Great Equalizer
Line 61: What’s happened here is that velocity is the great equalizer. Because the estimate
Line 62: for each feature is made relative to the estimates for other features, it does not
Line 63: matter if our estimates are correct, a little incorrect, or a lot incorrect. What
Line 64: matters is that they are consistent. We cannot simply roll a die and assign that
Line 65: number as the estimate to a feature. However, as long as we are consistent with
Line 66: our estimates, measuring velocity over the first few iterations will allow us to
Line 67: hone in on a reliable schedule.
Line 68: Let’s look at another example. Suppose a project consists of fifty user stories,
Line 69: each of which is estimated as one story point. For simplicity, suppose that I am
Line 70: the only person working on this project and that I expect I can complete one
Line 71: story point per work day. So on a two-week iteration, I expect to finish ten stories
Line 72: and have a velocity of ten. Further, I expect to finish the project in five iterations
Line 73: (ten weeks). However, after the first iteration, rather than having completed ten
Line 74: stories, I’ve completed only five. If I let velocity take care of correcting my mis-
Line 75: perceptions, I will realize that the project will take ten iterations, because my ve-
Line 76: locity is half of what I’d planned. 
Line 77: What happens, though, if I re-estimate? Suppose I re-estimate the five com-
Line 78: pleted stories, assigning each an estimate of two. My velocity is now ten (five
Line 79: completed stories, each re-estimated at two), and forty-five points of work re-
Line 80: main. With a velocity of ten and with forty-five points remaining, I expect to fin-
Line 81: ish the project in 4.5 iterations. The problem with this is that I am mixing
Line 82: Table 7.1 Some Stories and Estimates for the SwimStats Website
Line 83: Story ID
Line 84: Story
Line 85: Estimate
Line 86: 1
Line 87: As a coach, I can enter the names and demographic informa-
Line 88: tion for all swimmers on my team.
Line 89: 3
Line 90: 2
Line 91: As a coach, I can define practice sessions.
Line 92: 3
Line 93: 3
Line 94: As a swimmer, I can see all of my times for a specific event.
Line 95: 3
Line 96: 4
Line 97: As a swimmer, I can update my demographics information.
Line 98: 3
Line 99: 
Line 100: --- 페이지 95 ---
Line 101: 64
Line 102: |
Line 103: Chapter 7
Line 104: Re-Estimating
Line 105: revised and original estimates. Using hindsight, I have re-estimated the com-
Line 106: pleted stories at two points each. Unfortunately, when still looking forward at the
Line 107: remaining forty-five stories, I cannot predict which of those one-point stories I
Line 108: will want to say were worth two points in hindsight. 
Line 109: When to Re-Estimate
Line 110: Let’s continue working on the SwimStats website, this time with the user stories
Line 111: and estimates shown in Table 7.2.
Line 112: The first three of these stories each has to do with displaying a chart for the
Line 113: user. Suppose the team has planned the first iteration to include Stories 1, 2, and
Line 114: 6 from Table 7.2. Their planned velocity is thirteen. However, at the end of the
Line 115: iteration they have finished only Stories 1 and 6. They say they got less done
Line 116: than expected because Story 1 was much harder than expected and that it should
Line 117: have been “at least a six.” Suppose that rather than one difficult story, the team
Line 118: has completely underestimated the general difficulty of displaying charts. In that
Line 119: case, if Story 1 turned out to be twice as big as expected, we can expect the same
Line 120: of Stories 2 and 3. 
Line 121: Let’s see how this plays out across three scenarios.
Line 122: Table 7.2 Initial Estimates for Some SwimStats Stories
Line 123: Story ID
Line 124: Story
Line 125: Estimate
Line 126: 1
Line 127: As a swimmer, I can see a line chart of my times for a particular 
Line 128: event.
Line 129: 3
Line 130: 2
Line 131: As a coach, I can see a line chart showing the progress over the 
Line 132: season of all of my swimmers in a particular event.
Line 133: 5
Line 134: 3
Line 135: As a swimmer, I can see a pie chart showing how many first, 
Line 136: second, third, and lower places I’ve finished in.
Line 137: 3
Line 138: 4
Line 139: As a coach, I can see a text report showing each swimmer’s 
Line 140: best time in each event.
Line 141: 3
Line 142: 5
Line 143: As a coach, I can upload meet results from a file exported from 
Line 144: the timing system used at the meet.
Line 145: 3
Line 146: 6
Line 147: As a coach, I can have the system recommend who should 
Line 148: swim in each event subject to restrictions about how many 
Line 149: events a swimmer can participate in.
Line 150: 5
Line 151: 
Line 152: --- 페이지 96 ---
Line 153: Scenario 3: Re-Estimating When Relative Size Changes 
Line 154: |
Line 155: 65
Line 156: Scenario 1: No Re-Estimating
Line 157: In this scenario, we will leave all estimates alone. The team achieved a velocity of
Line 158: eight points in the last iteration. That leads us to the expectation that they’ll av-
Line 159: erage eight points in the upcoming iterations. However, the team knows they
Line 160: cannot complete Stories 2 and 3 in a single iteration, even though they represent
Line 161: only eight points. Because each of those stories involves charting, and because
Line 162: the team expects each charting story to be twice as big as its current estimate
Line 163: (just like Story 1 was), the team concludes that they cannot do Stories 2 and 3 in
Line 164: one iteration. It’s eight points, but it’s too much.
Line 165: Scenario 2: Re-Estimating the Finished Story
Line 166: In this scenario, let’s see if adjusting only the estimate of Story 1 fixes this prob-
Line 167: lem. After finishing the iteration, the team felt that Story 1 was twice as big as
Line 168: had been expected. So they decide to re-estimate it at six instead of three. That
Line 169: means that velocity for the prior iteration was eleven—six points for Story 1 and
Line 170: five points for Story 6.
Line 171: Because no other stories are re-estimated, the team plans its next iteration
Line 172: to comprise Stories 2, 3, and 4. These stories are worth eleven points, the same
Line 173: amount of work completed in the prior iteration. However, they run into the
Line 174: same problem as in the first scenario: Stories 2 and 3 will probably take twice as
Line 175: long as expected, and the team will not be able to average eleven points per iter-
Line 176: ation, as expected.
Line 177: Scenario 3: Re-Estimating When Relative Size 
Line 178: Changes
Line 179: In this scenario, the team re-estimates each of the charting stories. The esti-
Line 180: mates for Stories 1, 2, and 3 are double what is shown in Table 7.2. As in the sec-
Line 181: ond scenario, velocity for the first iteration is eleven—six points for Story 1 and
Line 182: five points for Story 6. Because velocity was eleven in the first iteration, the team
Line 183: expects approximately that velocity in the next iteration. However, when they
Line 184: plan their next iteration, only Story 2 will be selected. This story, initially esti-
Line 185: mated as five, was doubled to ten and is so big there is no room for an additional
Line 186: story.
Line 187: Re-estimating was helpful only in this third scenario. This means that you
Line 188: should re-estimate a story only when its relative size has changed.
Line 189: 
Line 190: --- 페이지 97 ---
Line 191: 66
Line 192: |
Line 193: Chapter 7
Line 194: Re-Estimating
Line 195: Re-Estimating Partially Completed Stories
Line 196: You may also wish to re-estimate when the team finishes only a portion of a story
Line 197: during an iteration. Suppose the team has been working on a story that says, “As
Line 198: a coach, I can have the system recommend who should swim in each event.” This
Line 199: story is initially estimated as five points, but it is deceptively complex.
Line 200: Teams in a swim meet receive points based on the finishing places of the
Line 201: swimmers. However, planning for a swim meet is not as easy as putting the
Line 202: team’s fastest swimmer for each event into that event. Each swimmer is limited
Line 203: in the number of events he or she can swim. This means we may not elect to
Line 204: have Savannah swim the 100-meter backstroke because we need her more in the
Line 205: 100-meter breaststroke. So suppose the team reaches the end of the iteration,
Line 206: and the system can optimize the assignment of swimmers to individual events.
Line 207: However, the team has not begun to think about how to assign swimmers to re-
Line 208: lay events. How many points should the team count toward the velocity of the
Line 209: current iteration? How many points should they assign to the remaining work?
Line 210: First, let me point out that I’m generally in favor of an all-or-nothing stance
Line 211: toward counting velocity: if a story is done (coded, tested, and accepted by the
Line 212: product owner), the team earns all the points, but if anything on the story isn’t
Line 213: done, they earn nothing. At the end of an iteration, this is the easiest case to as-
Line 214: sess: If everything is done, they get all the points; if anything is missing, they get
Line 215: no points. If the team is likely to take on the remaining portion of the story in
Line 216: the next iteration, this works well. Their velocity in the first iteration is a bit
Line 217: lower than expected because they got no credit for partially completing a story.
Line 218: In the second iteration, however, their velocity will be higher than expected be-
Line 219: cause they’ll get all of the points, even though some work had been completed
Line 220: prior to the start of the iteration. This works well as long as everyone remembers
Line 221: that we’re mostly interested in the team’s average velocity over time, not in
Line 222: whether velocity jumped up or down in a given iteration.
Line 223: However, in some cases the unfinished portion of a story may not be done in
Line 224: the next iteration. In these cases it can be appropriate to allow the team to take
Line 225: partial credit for the completed portion of the story. The remaining story (which
Line 226: is a subset of the initial story) is re-estimated based on the team’s current knowl-
Line 227: edge. In this case, the original story was estimated at five points. If the team feels
Line 228: that the subset they completed (scheduling individual events) is equivalent to
Line 229: three points or ideal days, they will give themselves that much credit. The unfin-
Line 230: ished portion of the original story in this case could be rewritten to be “As a
Line 231: coach, I can have the system recommend who should swim in each relay.” The
Line 232: team could then estimate that smaller story relative to all other stories. The
Line 233: combined estimates would not need to equal the original estimate of five.
Line 234: 
Line 235: --- 페이지 98 ---
Line 236: Discussion Questions 
Line 237: |
Line 238: 67
Line 239: However, the two best solutions to allocating points for incomplete stories
Line 240: are not to have any incomplete stories and to use sufficiently small stories that
Line 241: partial credit isn’t an issue.
Line 242: The Purpose of Re-Estimating
Line 243: Do not become overly concerned with the need to re-estimate. Whenever the
Line 244: team feels one or more stories are misestimated relative to other stories, re-esti-
Line 245: mate as few stories as possible to bring the relative estimates back in line. Use re-
Line 246: estimating as a learning experience for estimating future user stories. As Tom
Line 247: Poppendieck has taught me, “Failure to learn is the only true failure.” Learn
Line 248: from each re-estimated story, and turn the experience into a success.
Line 249: Summary
Line 250: Remembering that story points and ideal days are estimates of the size of a fea-
Line 251: ture helps you know when to re-estimate. You should re-estimate only when
Line 252: your opinion of the relative size of one or more stories has changed. Do not re-
Line 253: estimate solely because progress is not coming as rapidly as you’d expected. Let
Line 254: velocity, the great equalizer, take care of most estimation inaccuracies.
Line 255: At the end of an iteration, I do not recommend giving partial credit for par-
Line 256: tially finished user stories. My preference is for a team to count the entire esti-
Line 257: mate toward their velocity (if they completely finished and the feature has been
Line 258: accepted by the product owner) or for them to count nothing toward their story
Line 259: otherwise. However, the team may choose to re-estimate partially complete user
Line 260: stories. Typically, this will mean estimating a user story representing the work
Line 261: that was completed during the iteration and one or more user stories that de-
Line 262: scribe the remaining work. The sum of these estimates does not need to equal
Line 263: the initial estimate. 
Line 264: Discussion Questions
Line 265: 1. How does velocity correct bad estimates?
Line 266: 2. Why should you re-estimate only when the relative size has changed? Iden-
Line 267: tify some examples on a current or recent project when the relative size of
Line 268: one or more features changed.
Line 269: 
Line 270: --- 페이지 99 ---
Line 271: This page intentionally left blank 
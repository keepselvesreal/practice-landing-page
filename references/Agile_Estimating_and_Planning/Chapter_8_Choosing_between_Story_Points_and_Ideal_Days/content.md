Line 1: 
Line 2: --- 페이지 100 ---
Line 3: 69
Line 4: Chapter 8
Line 5: Choosing between Story 
Line 6: Points and Ideal Days
Line 7: “If you tell people where to go,
Line 8: but not how to get there,
Line 9: you’ll be amazed at the results.”
Line 10: —General George S. Patton
Line 11: As measures of size, story points and ideal days each have their advantages. To
Line 12: help you decide which one to use, this chapter outlines the key considerations in
Line 13: favor of each approach. 
Line 14: Considerations Favoring Story Points
Line 15: This section outlines the key points in favor of estimating in story points. These
Line 16: include
Line 17: ◆Story points help drive cross-functional behavior.
Line 18: ◆Story-point estimates do not decay.
Line 19: ◆Story points are a pure measure of size.
Line 20: ◆Estimating in story points typically is faster.
Line 21: ◆My ideal days are not your ideal days.
Line 22: 
Line 23: --- 페이지 101 ---
Line 24: 70
Line 25: |
Line 26: Chapter 8
Line 27: Choosing between Story Points and Ideal Days
Line 28: Story Points Help Drive Cross-Functional Behavior
Line 29: One of the reasons why agile teams are successful is that the teams are cross-
Line 30: functional. That is, agile teams include members from all disciplines necessary
Line 31: to build the product, including programmers, testers, product managers, usabil-
Line 32: ity designers, analysts, database engineers, and so on. Often, when we first as-
Line 33: semble a cross-functional team, some members have a hard time letting go of
Line 34: their departmental identity. The product will benefit to the extent that the
Line 35: project participants view themselves as team members first and as specialist con-
Line 36: tributors second—that is, “I am on the Napa project and am a tester” rather than
Line 37: “I am a tester assigned to the Napa project.” The distinction may be subtle, but
Line 38: the change in mindset is not.
Line 39: Estimating in story points can help teams learn to work cross-functionally.
Line 40: Because a story-point estimate needs to be a single number that represents all of
Line 41: the work for the whole team, estimating story points initiates high-level discus-
Line 42: sions about everything that will be involved. Estimating ideal days, on the other
Line 43: hand, often involves specialty groups estimating how long “their part” of a story
Line 44: will take and then summing these subestimates. For example, the programmers
Line 45: may conclude that they need three ideal days, the database engineer needs one,
Line 46: and the tester needs two. An estimate of six ideal days is then assigned to the
Line 47: story. 
Line 48: This small difference in how the earliest discussions about a story occur has
Line 49: an ongoing impact on how the story is developed.
Line 50: Story-Point Estimates Do Not Decay
Line 51: An estimate expressed in story points has a longer shelf life than an estimate in
Line 52: ideal days. An estimate in ideal days can change based on the team’s experience
Line 53: with the technology, the domain, and themselves, among other factors. To see
Line 54: why, suppose a programmer is learning a new language and is asked how long it
Line 55: will take to program a small application. His answer may be five days. Now jump
Line 56: forward a few months and ask the same programmer how long it will take to de-
Line 57: velop an application that is exactly the same size and complexity. His answer may
Line 58: be one day because he has become more skilled in the language. We have a prob-
Line 59: lem now, because the two applications are exactly the same size, yet they have
Line 60: been estimated differently.
Line 61: We would like to think that measuring velocity over time would correct or
Line 62: account for this problem. It won’t. Instead, we’ll see a consistent velocity even
Line 63: though more work is being done. Suppose that this programmer is the only per-
Line 64: son on the team and that he is working in one-week iterations. The first time he
Line 65: 
Line 66: --- 페이지 102 ---
Line 67: Estimating in Story Points Typically Is Faster 
Line 68: |
Line 69: 71
Line 70: develops the application, he has estimated it will take five ideal days. Let’s sup-
Line 71: pose he’s in an environment where a calendar day equals an ideal day. He starts
Line 72: this application on the first day of the iteration and finishes it on the fifth. He has
Line 73: a velocity of five for that iteration. Then, a few months later, because he esti-
Line 74: mates a similar application as one ideal day, he will complete five of them in an
Line 75: iteration. His velocity is again five, even though he did five times as much work
Line 76: as before. For some projects, especially those adopting new technologies or on
Line 77: which the team is new to the domain, this can be significant.
Line 78: Note that both story-point and ideal-day estimates will need to be updated if
Line 79: the size of an effort changes based on the development of a framework, for exam-
Line 80: ple. However, only ideal-day estimates need to change when the team becomes
Line 81: better at something. 
Line 82: Story Points Are a Pure Measure of Size
Line 83: As described in the introduction to this part, an important first step in estimat-
Line 84: ing how long something will take is estimating how big it is or how much of it
Line 85: there is to do. Story points are a pure measure of size. Ideal days are not. Ideal
Line 86: days may be used as a measure of size, but with some deficiencies. As noted in
Line 87: the preceding section, an estimate in ideal days will change as a developer’s pro-
Line 88: ficiency changes. This does not happen with story points—the size is what it is
Line 89: and doesn’t change. That is a desirable attribute of any measure of size.
Line 90: That story points are a pure measure of size has a couple of advantages.
Line 91: First, this means that we can estimate story points by analogy only. There is
Line 92: credible evidence that we are better at estimating “this is like that” than we are
Line 93: at estimating the absolute size of things (Lederer and Prasad 1998; Vicinanza et
Line 94: al. 1991). When we estimate in ideal days, on the other hand, we can still esti-
Line 95: mate by analogy. But when estimating in ideal days, we also tend to think of the
Line 96: calendar and how long a story will take to develop. 
Line 97: Second, because story points are a pure measure of size and are entirely ab-
Line 98: stract, there can be no temptation to compare them with reality. Teams that es-
Line 99: timate in ideal days almost inevitably have their ideal days compared with actual
Line 100: days. They then find themselves justifying why they completed “only” eight ideal
Line 101: days of work in a ten-day iteration.
Line 102: Estimating in Story Points Typically Is Faster
Line 103: Teams that estimate in story points seem to do so more quickly than teams that
Line 104: estimate in ideal days. To estimate many stories, it is necessary to have a very
Line 105: high-level design discussion about the story: Would we implement this in the
Line 106: 
Line 107: --- 페이지 103 ---
Line 108: 72
Line 109: |
Line 110: Chapter 8
Line 111: Choosing between Story Points and Ideal Days
Line 112: database? Can we reuse the user interface? How will this affect the middle tier?
Line 113: All these questions come up at one time or another.
Line 114: My experience is that teams estimating in ideal days have a tendency to take
Line 115: these discussions a little deeper than do teams estimating in story points. The
Line 116: difference is presumably because when estimating in ideal days, it is more
Line 117: tempting to think about the individual tasks necessary to develop a story than to
Line 118: think in terms of the size of the story relative to other stories. 
Line 119: My Ideal Days Are Not Your Ideal Days
Line 120: Suppose two runners, one fast and one slow, are standing at the start of a trail.
Line 121: Each can see the whole course of the trail, and they can agree that it is one kilo-
Line 122: meter. They can compare it with another trail they’ve each run and agree that it
Line 123: is about half the length of that other trail. Their discussions of trail size (really
Line 124: distance, in this case) are meaningful.
Line 125: Suppose instead of discussing the length of the trails, these two runners dis-
Line 126: cussed the time it took to run the trails. The fast runner might say, “This is a
Line 127: five-minute trail,” to which the slow runner would respond, “No, it’s at least a
Line 128: eight-minute trail.” Each would be right, of course, but they would have no way
Line 129: of settling their differences other than agreeing always to discuss trails in terms
Line 130: of how long one of them (or some other runner) would take to run the trail. 
Line 131: This same problem exists with ideal days. You may think you can completely
Line 132: develop a particular user story in three ideal days. I think I can do it in five days.
Line 133: We’re probably both right. How can we come to an agreement? We might choose
Line 134: to put your estimate on it because we think you’ll be the one to do the work. But
Line 135: that might be a mistake, because by the time we actually do the work, you may
Line 136: be too busy and I have to do it. And I’ll be late, because it’s estimated at three
Line 137: days for you, but will take me five. 
Line 138: What most teams do is ignore this issue. This is acceptable if all developers
Line 139: are of approximately the same skill or if programmers always work in pairs,
Line 140: which helps balance out extreme differences in productivity.
Line 141: Considerations Favoring Ideal Days
Line 142: This section outlines the key points in favor of estimating in ideal days. These in-
Line 143: clude the following:
Line 144: ◆Ideal days are easier to explain outside the team.
Line 145: 
Line 146: --- 페이지 104 ---
Line 147: Recommendation 
Line 148: |
Line 149: 73
Line 150: ◆Ideal days are easier to estimate at first.
Line 151: Ideal Days Are Easier to Explain Outside the Team
Line 152: There is a very intuitive feel to ideal days—“This is the amount of time it would
Line 153: take me if it’s all that I worked on.” Because of this intuitive feel, ideal days are
Line 154: easy to understand, which makes them easy to explain to others outside the
Line 155: project team. Everyone understands that not every minute of the work day is
Line 156: spent programming, testing, designing, or otherwise making progress toward
Line 157: new features.
Line 158: It is usually necessary to explain to outsiders (and the team, at first) the con-
Line 159: cept of a story point as a measure of size. However, you can often use the need to
Line 160: explain story points as an opportunity to describe the overall approach to esti-
Line 161: mating and planning your project will take. This is an excellent opportunity to
Line 162: accustom outside stakeholders to ideas such as the cone of uncertainty, the pro-
Line 163: gressive refinement of plan accuracy, and how observing velocity over a number
Line 164: of periods will lead to greater reliability in the plans you produce.
Line 165: Ideal Days Are Easier to Estimate at First
Line 166: In addition to being easier to explain to others, it is often easier for the team it-
Line 167: self to get started with ideal days. When a team chooses to estimate in story
Line 168: points, the first handful of stories they estimate can be difficult to estimate or
Line 169: have an unsettling feeling. Without a baseline such as a nine-to-five day or some
Line 170: previously estimated stories, the team that uses story points has to find its own
Line 171: baseline by estimating a few stories. 
Line 172: Fortunately, most teams get through this initial phase of story-point esti-
Line 173: mating very, very quickly. Usually within an hour, many teams estimate in story
Line 174: points as naturally as if they’d been doing it for years. However, those first few
Line 175: stories can feel uncomfortable.
Line 176: Recommendation
Line 177: My preference is for story points. I find that the benefits they offer as pure mea-
Line 178: sure of size are compelling. That story points help promote cross-functional
Line 179: team behavior is a huge advantage. Shifting a team’s thinking from “my part will
Line 180: take three ideal days, and your part will take two ideal days, so the total is five
Line 181: ideal days” is very different from “overall, this story seems about the same size as
Line 182: that one, so let’s call it five story points also.” That a story point to me can be the
Line 183: 
Line 184: --- 페이지 105 ---
Line 185: 74
Line 186: |
Line 187: Chapter 8
Line 188: Choosing between Story Points and Ideal Days
Line 189: same as a story point to you, while the same may not be true of an ideal day, is
Line 190: another big benefit. Two developers of different skill or experience can agree on
Line 191: the size of something while disagreeing about how long it will take to do. 
Line 192: The shortcomings of story points are indeed short. Yes, it’s easier to get
Line 193: started with ideal days. However, the discomfort of working with nebulous story
Line 194: points is short-lived. Ideal days are definitely easier to explain to those outside
Line 195: the team, but we probably shouldn’t choose based on how hard it will be to ex-
Line 196: plain to outsiders. That ideal days are so easily understandable causes problems
Line 197: as well. In some organizations there will be pressure to make an actual day
Line 198: closer to an ideal day. Pressure for more focus and concentration on our work is
Line 199: fine. But organizational pressure for each actual day to be close to an ideal day
Line 200: will also have the effect of causing us to estimate in actual time while calling it
Line 201: an ideal day. That is, an ideal day will become redefined as “a day where I make
Line 202: six hours of progress and do other things for two hours.”
Line 203: I occasionally start a team estimating in ideal days. I usually do this only
Line 204: with a team that cannot accept that it is beneficial to separate estimates of size
Line 205: and duration. Some individuals are so used to being asked for estimates and re-
Line 206: sponding immediately with a date that the jump to story points is difficult.
Line 207: In these cases, I have the team start estimating in ideal days, but as quickly
Line 208: as possible, I start to ask questions like “How big is this one compared with the
Line 209: one we estimated five minutes ago?” Or I’ll ask, “So this one is a little smaller
Line 210: than the story we just estimated?” The purpose of these questions is to shift the
Line 211: conversation to be more abstract and about the relative size of the stories than
Line 212: about how long it will take to design a screen, code a stored procedure, and write
Line 213: some HTML. In this way, a team can start with estimating in ideal days but grad-
Line 214: ually separate their estimates from a number of days. 
Line 215: Summary
Line 216: A team can choose to estimate in either story points or ideal days. Each is a via-
Line 217: ble choice with advantages to recommend it.
Line 218: Story points have the advantage of helping promote cross-functional team
Line 219: behavior. Additionally, because story points are a more pure measure of size,
Line 220: they do not need to be re-estimated if the team improves in a technology or the
Line 221: domain. Estimating in story points is often faster than estimating ideal days. Fi-
Line 222: nally, unlike ideal days, story points can be compared among team members. If
Line 223: one team member thinks something will take her four ideal days, and another
Line 224: team member thinks it will take him one ideal day, they may each be right, yet
Line 225: they have no basis on which to argue and establish a single estimate. 
Line 226: 
Line 227: --- 페이지 106 ---
Line 228: Discussion Questions 
Line 229: |
Line 230: 75
Line 231: Ideal days have the advantages of being more easily explained to those out-
Line 232: side the team and of being easier to get started with.
Line 233: My preference is for story points. The advantages of estimating in story
Line 234: points are more compelling. If a team is struggling with the concept of estimat-
Line 235: ing pure size, I will start them estimating in ideal days but will then convert
Line 236: them to story points. I do this by asking more questions such as “How big is this
Line 237: compared with the other stories we’ve estimated?” rather than “How many ideal
Line 238: days will this take?” Most teams hardly notice the gradual switch, and by the
Line 239: time they do, they are thinking about points rather than ideal days. 
Line 240: Discussion Questions
Line 241: 1. Which approach do you prefer—story points or ideal days? Why?
Line 242: 2. How might you introduce this to your organization? What obstacles do you
Line 243: anticipate, and how could you address them?
Line 244: 
Line 245: --- 페이지 107 ---
Line 246: This page intentionally left blank 
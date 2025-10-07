Line 1: 
Line 2: --- 페이지 66 ---
Line 3: 35
Line 4: Chapter 4
Line 5: Estimating Size with Story 
Line 6: Points
Line 7: “In a good shoe, I wear a size six,
Line 8: but a seven feels so good, I buy a size eight.”
Line 9: —Dolly Parton in Steel Magnolias
Line 10: Suppose a new restaurant opens nearby, and you decide to try it. For the first
Line 11: course, you can have either a cup or a bowl of soup. You can have the entrée as
Line 12: either a full or half portion. And you can have either a small or a large soda.
Line 13: You’ve probably been to many restaurants like this and can quite easily order
Line 14: about the right amount of food without asking how many ounces are in the cups
Line 15: and bowls of soup and exactly how big the entrée portions are. At most, you may
Line 16: ask the server something like “How big is the salad?” The server will likely re-
Line 17: spond by holding his hands apart to illustrate the size. In cases such as these,
Line 18: you are ordering by relative rather than measured size. You’re saying, “Give me
Line 19: the large portion” or “I’d like the small serving.” You are not ordering by exact
Line 20: size, such as “I’d like fourteen ounces of soda, six ounces of lasagna, and three
Line 21: ounces of bread.”
Line 22: It’s possible to estimate an agile project’s user stories or features in the same
Line 23: way. When I’m at an unfamiliar restaurant and order a large soda, I don’t really
Line 24: know how many ounces I’ll get. About all I do know is that a large soda is larger
Line 25: than a small or medium soda and that it’s smaller than an extra-large one. I also
Line 26: know from experience that when I’m about as thirsty as I am now, a large soda at
Line 27: other restaurants has been the right size. Fortunately, this is all the knowledge I
Line 28: need. And on software projects it’s even easier: All I need to know is whether a
Line 29: particular story or feature is larger or smaller than other stories and features.
Line 30: 
Line 31: --- 페이지 67 ---
Line 32: 36
Line 33: |
Line 34: Chapter 4
Line 35: Estimating Size with Story Points
Line 36: Story Points Are Relative
Line 37: Story points are a unit of measure for expressing the overall size of a user story,
Line 38: feature, or other piece of work. When we estimate with story points, we assign a
Line 39: point value to each item. The raw values we assign are unimportant. What mat-
Line 40: ters are the relative values. A story that is assigned a two should be twice as
Line 41: much as a story that is assigned a one. It should also be two-thirds of a story that
Line 42: is estimated as three story points.
Line 43: The number of story points associated with a story represents the overall
Line 44: size of the story. There is no set formula for defining the size of a story. Rather, a
Line 45: story-point estimate is an amalgamation of the amount of effort involved in de-
Line 46: veloping the feature, the complexity of developing it, the risk inherent in it, and
Line 47: so on. 
Line 48: There are two common ways to get started. The first approach is to select a
Line 49: story that you expect to be one of the smallest stories you’ll work with and say
Line 50: that story is estimated at one story point. The second approach is instead to se-
Line 51: lect a story that seems somewhat medium and give it a number somewhere in
Line 52: the middle of the range you expect to use. Personally, I prefer most of my stories
Line 53: to be in the range of one to ten. (I’ll explain why in Chapter 6, “Techniques for
Line 54: Estimating.”) This means I’ll look for a medium-size story and call it five story
Line 55: points. Once you’ve fairly arbitrarily assigned a story-point value to the first
Line 56: story, each additional story is estimated by comparing it with the first story or
Line 57: with any others that have been estimated.
Line 58: The best way to see how this works is to try it. Instead of story points, let’s
Line 59: estimate dog points for a moment. Let’s define a dog point as representing the
Line 60: height of the dog at the shoulder. With that in mind, assign dog points to each of
Line 61: these breeds:
Line 62: ◆Labrador retriever
Line 63: ◆Terrier
Line 64: ◆Great Dane
Line 65: ◆Poodle
Line 66: ◆Dachshund
Line 67: ◆German shepherd
Line 68: ◆Saint Bernard
Line 69: ◆Bulldog
Line 70: 
Line 71: --- 페이지 68 ---
Line 72: Story Points Are Relative 
Line 73: |
Line 74: 37
Line 75: Before reading on, really spend a moment thinking about how many dog
Line 76: points you would assign to each breed. The discussion that follows will be much
Line 77: more clear if you do.
Line 78: My estimates are shown in Table 4.1. I determined these values by starting
Line 79: with Labrador retriever. This breed seems medium-size to me, so I gave it a five.
Line 80: Great Danes seem about twice as tall, so I gave them a ten. Saint Bernards seem
Line 81: a little less than twice as tall, so I gave them a nine. A dachshund seems about as
Line 82: short as a dog gets and so got a one. Bulldogs are short, so I gave them a three.
Line 83: However, if I had been estimating dog points based on weight, I would have given
Line 84: bulldogs a higher number.
Line 85: On an agile project it is not uncommon to begin an iteration with incom-
Line 86: pletely specified requirements, the details of which will be discovered during the
Line 87: iteration. However, we need to associate an estimate with each story, even those
Line 88: that are incompletely defined. You’ve already seen how to do this if you assigned
Line 89: dog points to poodle and terrier. Without more detail, it should have been diffi-
Line 90: cult to assign dog points to poodle and terrier. There are toy, miniature, and
Line 91: standard poodles, each of a different height. Similarly, terrier is a group of more
Line 92: than twenty breeds. Some terriers (West Highland, Norwich, Norfolk) are less
Line 93: than a foot tall; others (Airedale) are nearly two feet tall.
Line 94: When you’re given a loosely defined user story (or dog), you make some as-
Line 95: sumptions, take a guess, and move on. In Table 4.1, I took a guess for terrier and
Line 96: poodle, and assigned each three dog points. I reasoned that even the largest are
Line 97: Table 4.1 One Possible Assignment of Dog Points
Line 98: Breed
Line 99: Dog Points
Line 100: Labrador retriever
Line 101: 5
Line 102: Terrier
Line 103: 3
Line 104: Great Dane
Line 105: 10
Line 106: Poodle
Line 107: 3
Line 108: Dachshund
Line 109: 1
Line 110: German shepherd
Line 111: 5
Line 112: Saint Bernard
Line 113: 9
Line 114: Bulldog
Line 115: 3
Line 116: 
Line 117: --- 페이지 69 ---
Line 118: 38
Line 119: |
Line 120: Chapter 4
Line 121: Estimating Size with Story Points
Line 122: smaller than Labrador retrievers and that the small terriers and poodles would
Line 123: be one- or two-point dogs, so on average a three seemed reasonable. 
Line 124: Velocity
Line 125: To understand how estimating in unitless story points can possibly work, it is
Line 126: necessary to introduce a new concept: velocity. Velocity is a measure of a team’s
Line 127: rate of progress. It is calculated by summing the number of story points assigned
Line 128: to each user story that the team completed during the iteration.1 If the team
Line 129: completes three stories each estimated at five story points, their velocity is fif-
Line 130: teen. If the team completes two five-point stories, their velocity is ten. 
Line 131: If a team completed ten story points of work last iteration, our best guess is
Line 132: that they will complete ten story points this iteration. Because story points are
Line 133: estimates of relative size, this will be true whether they work on two five-point
Line 134: stories or five two-point stories.
Line 135: In the introduction to this part of the book, the model in Figure 4.1 was
Line 136: used to show how an estimate of size could be turned into an estimate of dura-
Line 137: tion and a schedule. It should be possible now to see how story points and veloc-
Line 138: ity fit into this model.
Line 139: Figure 4.1 Estimating the duration of a project begins with estimating its size.
Line 140: If we sum the story-point estimates for all desired features we come up with
Line 141: a total size estimate for the project. If we know the team’s velocity we can divide
Line 142: 1. This definition will suffice for now. The next chapter will introduce the idea of estimat-
Line 143: ing in ideal time as an alternative to story points. A team that estimates in ideal time will
Line 144: calculate velocity as the sum of the ideal time estimates of the stories completed.
Line 145: Estimate size
Line 146: Derive
Line 147: duration
Line 148: Desired
Line 149: features
Line 150: Schedule
Line 151: 
Line 152: --- 페이지 70 ---
Line 153: Velocity Corrects Estimation Errors 
Line 154: |
Line 155: 39
Line 156: size by velocity to arrive at an estimated number of iterations. We can turn this
Line 157: duration into a schedule by mapping it onto a calendar. 
Line 158: A key tenet of agile estimating and planning is that we estimate size but de-
Line 159: rive duration. Suppose all of the user stories are estimated and the sum of those
Line 160: estimates is 100 story points. This is the estimated size of the system. Suppose
Line 161: further that we know from past experience that the team’s velocity has been ten
Line 162: points per two-week iteration, and that they will continue at the same velocity
Line 163: for this project. From our estimate of size and our known velocity value, we can
Line 164: derive a duration of ten iterations or twenty weeks. We can count forward twenty
Line 165: weeks on the calendar, and that becomes our schedule.
Line 166: This very simplistic explanation of release planning works for now. It will be
Line 167: extended in Part IV, “Scheduling.” Additionally, this example was made very sim-
Line 168: ple because we used the team’s past velocity. That is not always the case; velocity
Line 169: must sometimes be estimated instead. This can be difficult, but there are ways of
Line 170: doing it, which will be covered in Chapter 16, “Estimating Velocity.”
Line 171: Velocity Corrects Estimation Errors
Line 172: Fortunately, as a team begins making progress through the user stories of a
Line 173: project, their velocity becomes apparent over the first few iterations. The beauty
Line 174: of a points-based approach to estimating is that planning errors are self-correct-
Line 175: ing because of the application of velocity. Suppose a team estimates a project to
Line 176: include 200 points of work. They initially believe they will be able to complete
Line 177: twenty-five points per iteration, which means they will finish in eight iterations.
Line 178: However, once the project begins, their observed velocity is only twenty. Without
Line 179: re-estimating any work they will have correctly identified that the project will
Line 180: take ten iterations rather than eight. 
Line 181: To see how this works, suppose you are hired to paint an unfamiliar house.
Line 182: You are shown the floor plan in Figure 4.2 and are told that all materials will be
Line 183: provided, including a brush, roller, and paint. For your own purposes, you want
Line 184: to know how long this job will take you, so you estimate it. Because all you have
Line 185: is the floor plan, and you cannot see the actual house yet, you estimate based on
Line 186: what you can infer from the floor plan. Suppose that you estimate the effort to
Line 187: paint each of the smaller bedrooms to be five points. The five doesn’t mean any-
Line 188: thing. It does indicate, however, that the effort will be about the same for each
Line 189: bedroom. Because the master bedroom is about twice the size of the other bed-
Line 190: rooms, you estimate it as ten points.
Line 191: However, look more closely at Figure 4.2 and notice that there are no di-
Line 192: mensions given. Are the two bedrooms 8' x 10' or 16' x 20'? It’s impossible to tell
Line 193: 
Line 194: --- 페이지 71 ---
Line 195: 40
Line 196: |
Line 197: Chapter 4
Line 198: Estimating Size with Story Points
Line 199: from the floor plan. Are the estimates you’ve given completely worthless at this
Line 200: point? No. In fact, your estimates remain useful because they are estimates of
Line 201: the relative effort of painting each room. If you find that the bedrooms are twice
Line 202: the size you thought, the master bedroom is also twice the size you thought. The
Line 203: estimates remain the same, but because the rooms have four times the area you
Line 204: expected, your rate of progress through them will be slower.
Line 205: The beauty of this is that estimating in story points completely separates the
Line 206: estimation of effort from the estimation of duration. Of course, effort and sched-
Line 207: ule are related, but separating them allows each to be estimated independently.
Line 208: In fact, you are no longer even estimating the duration of a project; you are com-
Line 209: puting it or deriving it. The distinction is subtle but important.
Line 210: Figure 4.2 How long will it take to paint this house?
Line 211: Summary
Line 212: Story points are a relative measure of the size of a user story. A user story esti-
Line 213: mated as ten story points is twice as big, complex, or risky as a story estimated as
Line 214: five story points. A ten-point story is similarly half as big, complex, or risky as a
Line 215: twenty-point story. What matters are the relative values assigned to different
Line 216: stories.
Line 217: Bedroom
Line 218: Bath
Line 219: Office
Line 220: Kitchen
Line 221: Garage
Line 222: Living
Line 223: Dining
Line 224: Master
Line 225: Bath
Line 226: Foyer
Line 227: Bedroom
Line 228: 
Line 229: --- 페이지 72 ---
Line 230: Discussion Questions 
Line 231: |
Line 232: 41
Line 233: Velocity is a measure of a team’s rate of progress per iteration. At the end of
Line 234: each iteration, a team can look at the stories they have completed and calculate
Line 235: their velocity by summing the story-point estimates for each completed story. 
Line 236: Story points are purely an estimate of the size of the work to be performed.
Line 237: The duration of a project is not estimated as much as it is derived by taking the
Line 238: total number of story points and dividing it by the velocity of the team. 
Line 239: Discussion Questions
Line 240: 1. What story-point values would you put on some features of your current
Line 241: project?
Line 242: 2. After having assigned dog points to the dogs in this chapter, what estimate
Line 243: would you assign to an elephant if, as your project customer, I told you I
Line 244: misspoke and meant to give you a list of mammals not dogs?
Line 245: 3. It’s fairly easy to estimate that two things of very similar size are the same.
Line 246: Over what range (from the smallest item to the largest) do you think you can
Line 247: reliably estimate? Five times the smallest item? Ten times? A hundred times?
Line 248: A thousand times?
Line 249: 
Line 250: --- 페이지 73 ---
Line 251: This page intentionally left blank 
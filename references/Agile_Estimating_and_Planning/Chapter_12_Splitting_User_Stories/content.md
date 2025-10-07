Line 1: 
Line 2: --- 페이지 152 ---
Line 3: 121
Line 4: Chapter 12
Line 5: Splitting User Stories
Line 6: “These days we do not program software module by module;
Line 7: we program software feature by feature.”
Line 8: —Mary Poppendieck
Line 9: As user stories rise to the top of the release plan, meaning that they will be im-
Line 10: plemented soon, they often need to be split. After all, if implementing a particu-
Line 11: lar user story will take longer than the length of the iteration, there’s no choice
Line 12: but to split the story into two or more stories. Learning how to see ways to split
Line 13: stories is not a particularly difficult skill to acquire, but it does take practice and
Line 14: experience. The more different user stories you’ve split in the past, the easier it
Line 15: becomes. With that in mind, this chapter offers advice on splitting stories by
Line 16: providing a number of examples. From these examples, a number of guidelines
Line 17: are distilled that can be used for splitting other stories.
Line 18: The advice in this chapter can be used any time a story needs to be split.
Line 19: However, the guidelines are specifically targeted at the user stories or features
Line 20: that seem difficult to split.
Line 21: When to Split a User Story
Line 22: There are times when it may be necessary to split a user story into multiple,
Line 23: smaller parts. First, a user story should be split when it is too large to fit within
Line 24: a single iteration. Sometimes a user story won’t fit in an iteration because it is
Line 25: bigger than a full iteration. Clearly, a story in this situation needs to be split.
Line 26: 
Line 27: --- 페이지 153 ---
Line 28: 122 |
Line 29: Chapter 12
Line 30: Splitting User Stories
Line 31: Alternatively, a story may be small enough to fit within an iteration, but it won’t
Line 32: fit within the iteration being planned because there isn’t enough room left. The
Line 33: team may feel they will have time to develop a portion of a story in the iteration
Line 34: but not the entire story. 
Line 35: Second, it can be useful to split a large user story (an epic) if a more accurate
Line 36: estimate is necessary. For example, one of my clients was contemplating new
Line 37: features that would provide enhanced access into their system to customer ser-
Line 38: vice representatives (CSRs) who worked at other companies. The first question
Line 39: the product owner had to answer was whether these features were worth pursu-
Line 40: ing. Rather than writing a bunch of individual user stories, she wrote one large
Line 41: story and described the vision behind that story to the team. They estimated it as
Line 42: seventy story points. That was good enough for her to know she wanted to add
Line 43: these features. She knew there was a great deal of uncertainty in the estimate,
Line 44: but even if the estimate were off by 100% these features were still worth doing. If
Line 45: seventy story points had put her on the border of whether or not to include the
Line 46: CSR features in the release, she could have chosen to split the large story and
Line 47: have the team estimate the multiple smaller stories. 
Line 48: Splitting across Data Boundaries
Line 49: One of the best ways to split a large user story is by the data that will be sup-
Line 50: ported. For example, on a recent project the team was developing a product to
Line 51: collect financial information. They started with one epic user story: “As a user, I
Line 52: can enter my balance sheet information.” A balance sheet in this case could in-
Line 53: clude a great many fields. At the highest level, it includes assets and liabilities.
Line 54: Assets included such items as cash, securities, real estate, automobiles, loans,
Line 55: and so on. The system was such that the user could interact with this balance
Line 56: sheet at various levels of detail. A user could enter a single value representing all
Line 57: of his assets. Or he could enter slightly more detailed information (a total value
Line 58: of all loans, for example) or much more detailed information (an itemization of
Line 59: all loans). Considering the number of fields on the screen and the interactions
Line 60: among them, this was far more than the team felt they could complete in a sin-
Line 61: gle two-week iteration.
Line 62: The team split this story by the type of data that the user could enter. Their
Line 63: first story was “As a user, I can enter summary balance sheet data.” This story
Line 64: was very small (almost too small), as it covered only creating the basic form and
Line 65: two fields: one for assets and one for liabilities. Their next story was “As a user, I
Line 66: can enter categorized balance sheet data.” This story covered the next level of de-
Line 67: tail (such as cash, securities, real estate, loans, and so on). When this story was
Line 68: 
Line 69: --- 페이지 154 ---
Line 70: Splitting across Data Boundaries 
Line 71: |
Line 72: 123
Line 73: implemented, there would be two dozen input fields on the screen. Their next
Line 74: story covered data validation, “As a user, I want the values I enter to be validated
Line 75: so that I don’t make any mistakes.” They discussed what this meant and agreed
Line 76: that positive and negative amounts would be allowed, that decimals could be en-
Line 77: tered but that amounts would be automatically rounded to the nearest dollar,
Line 78: and so on.
Line 79: Their next user story was “As a user, I can enter detailed loan information.”
Line 80: This story would allow a user to enter up to 100 loans (this number was dis-
Line 81: cussed, agreed to, and noted as a condition of satisfaction on the story card). This
Line 82: story was larger than it sounds because it addressed a number of user interface
Line 83: issues, such as how new rows of loan data would be displayed on the screen. The
Line 84: story was much larger than the others that had been split out from the original
Line 85: story. However, even this story was much smaller than the original story because
Line 86: this one called for supporting detailed data only for loans. The loan story was
Line 87: used as a pattern for many other user stories that were split from the original,
Line 88: such as “As a user, I can enter detailed information about my real estate hold-
Line 89: ings” and “As a user, I can enter detailed information about my cash holdings, in-
Line 90: cluding checking and savings accounts.”
Line 91: By splitting the initial story in this way, the team created about a dozen user
Line 92: stories from the initial one. Each of the new stories was now well within the size
Line 93: they could complete in a two-week iteration. This leads to our first guideline:
Line 94: Splitting a user story along data boundaries is a very useful approach and
Line 95: one you should definitely have in your bag of tricks. As another example, a few
Line 96: years ago I was working with a team developing an automated fax subsystem.
Line 97: The team was faced with some large user stories about how the system could be
Line 98: configured. The stories were made much smaller by splitting support for U.S.
Line 99: and international phone numbers.
Line 100: In some cases a large story can be made much smaller by removing the han-
Line 101: dling of exceptional or error conditions from the main story. Suppose you are
Line 102: working on a system to process loan repayments and have this user story: “As a
Line 103: borrower, I want to pay off my loan.” When the team discusses this story, the
Line 104: product owner points out that if the borrower inadvertently sends a check for
Line 105: more than the outstanding loan amount, a refund check has to be printed and
Line 106: Split large stories along the boundaries of the data supported by
Line 107: the story.
Line 108: 
Line 109: --- 페이지 155 ---
Line 110: 124 |
Line 111: Chapter 12
Line 112: Splitting User Stories
Line 113: mailed back to the borrower. She adds that this applies only for amounts over ¤2.
Line 114: This story could be split by writing the following stories:
Line 115: ◆As a borrower, I want to pay off my loan. Note: Allow overpayments.
Line 116: ◆As a borrower, if I accidentally repay too much, I get a refund if it’s over ¤2.
Line 117: Splitting on Operational Boundaries
Line 118: I worked with a team recently that was tasked with developing a very complex
Line 119: search screen. There were dozens of fields on the top half of the screen, a middle-
Line 120: tier query builder that assembled formulated database queries based on what had
Line 121: been entered, and then a complex data display grid on the bottom of the screen.
Line 122: All of this work was initally described by a single user story. I had the team split
Line 123: the work into three pieces that were spread across three iterations. 
Line 124: In the first iteration they laid out the basic user interface, including about
Line 125: half of the search criteria fields that were on the top of the screen. They also
Line 126: wrote the portions of the query builder that worked with those fields. The bot-
Line 127: tom part of the screen was to hold the complex data display grid. This was too
Line 128: much to do in one two-week iteration. So at the end of the first iteration, that
Line 129: portion of the screen displayed a simple message such as “This search found 312
Line 130: matches.” This certainly wasn’t very useful for a user who wanted to know what
Line 131: those 312 matches contained. However, it represented significant progress and
Line 132: made that progress visible to all project stakeholders. 
Line 133: The second iteration on this project added the data display grid, and the
Line 134: third iteration added the remaining search criteria fields to the top of the screen.
Line 135: These iterations were prioritized this way because there was a lot of uncertainty
Line 136: about how long it would take to develop the data display grid. Removing that un-
Line 137: certainty in the second iteration was deemed better than leaving it until the
Line 138: third. Because the team had already achieved a solid understanding of what was
Line 139: necessary to create the query builder, they considered that work to be low risk.
Line 140: This leads to our next guideline:
Line 141: A common approach to doing this is to split a story along the boundaries of
Line 142: the common CRUD operations—Create, Read, Update, and Delete. To see how
Line 143: Split large stories based on the operations that are performed
Line 144: within the story.
Line 145: 
Line 146: --- 페이지 156 ---
Line 147: Removing Cross-Cutting Concerns 
Line 148: |
Line 149: 125
Line 150: this works, suppose you are working on the SwimStats system, and the team is
Line 151: ready to develop this story: “As a coach, I can manage the swimmers on my
Line 152: team.” The team talks to the coaches/users and finds out that this means the
Line 153: coach wants to add new swimmers, edit existing data for swimmers, and delete
Line 154: swimmers who have left the team. This initial story can easily be split into three
Line 155: stories:
Line 156: ◆As a coach, I can add new swimmers to my team.
Line 157: ◆As a coach, I can edit information about swimmers already on my team.
Line 158: ◆As a coach, I can delete swimmers who are no longer on my team.
Line 159: These stories very closely correspond to the Create, Update, and Delete por-
Line 160: tions of CRUD. Splitting a large story into these three stories is a very common
Line 161: pattern and leads to our next guideline:
Line 162: Removing Cross-Cutting Concerns
Line 163: There are many orthogonal or cross-cutting features in a typical application. Se-
Line 164: curity, error-handling, and logging, for example, each cut across all of the other
Line 165: features of an application. A story that is too big to fit in an iteration can often be
Line 166: reduced by isolating it from one or more of these cross-cutting concerns.
Line 167: For example, many applications contain screens that behave differently de-
Line 168: pending on the privileges of the current user. If that is too much to develop in a
Line 169: single iteration, develop the screens in one iteration and add support for user-
Line 170: specific privileges in a later iteration.
Line 171: On a recent project a client needed to split a story that involved searching
Line 172: for data and displaying the results. Each search would span the entire database,
Line 173: but only those results the user had privileges to see were to be displayed. The
Line 174: team’s solution was to ignore this security restriction, and in the first iteration
Line 175: on this feature, users could see the entire result set. 
Line 176: As another example, suppose the team plans to work on a story that says “As
Line 177: a user, I am required to log in with a username and password before using the
Line 178: system.” The team discusses the story and comes up with a list of constraints on
Line 179: the password: It must be at least eight characters, must include at least one digit,
Line 180: Split large stories into separate CRUD operations.
Line 181: 
Line 182: --- 페이지 157 ---
Line 183: 126 |
Line 184: Chapter 12
Line 185: Splitting User Stories
Line 186: must not include any characters repeated three or more times, must be en-
Line 187: crypted when transmitted and stored, and so on.
Line 188: None of this may be particularly time-consuming, but in aggregate it may
Line 189: make the story a little too big to fit in an iteration. This can be resolved by re-
Line 190: moving the security precautions from the login story and creating nonsecure
Line 191: and secure versions of the story. The second story could list the planned security
Line 192: precautions, such as password length, character restrictions, and so on. You
Line 193: probably would not choose to release the product with only the first, nonsecure
Line 194: story developed, but there could be value in splittng the initial, large story in this
Line 195: way.
Line 196: This leads to our next guideline:
Line 197: Don’t Meet Performance Constraints
Line 198: In software development we often forget (or ignore) Kernighan and Plauger’s
Line 199: (1974) advice to “Make it work, then make it faster.” A few years ago I was on a
Line 200: project to display charts of stock market prices. Web users would request a chart
Line 201: by the stock’s ticker symbol. Our code would then retrieve the price history of
Line 202: that stock (over any of a variety of time periods from the current day to the last
Line 203: five years) and display a line chart of the stock. Among the conditions of satisfac-
Line 204: tion associated with that feature were ones covering the accuracy of the line, the
Line 205: handling of missing data, and the performance. To meet the performance target,
Line 206: we would need to cache the most frequently requested charts, regenerating each
Line 207: once per minute. Because caching would be a significant part of the effort to de-
Line 208: liver this new feature, we separated it into a new user story and scheduled it into
Line 209: the next iteration. More generally, this same approach can be applied to any non-
Line 210: functional requirement, which leads to our next guideline:
Line 211: Consider removing cross-cutting concerns (such as security, logging,
Line 212: error handling, and so on) and creating two versions of the story:
Line 213: one with and one without support for the cross-cutting concern.
Line 214: Consider splitting a large story by separating the functional and
Line 215: nonfunctional aspects into separate stories.
Line 216: 
Line 217: --- 페이지 158 ---
Line 218: Don’t Split a Story into Tasks 
Line 219: |
Line 220: 127
Line 221: For example, this approach can be applied if a new feature must consume
Line 222: less than a defined amount of memory, be drawn with fewer than a number of
Line 223: shapes, or use a critical resource for less than a defined amount of time.
Line 224: Split Stories of Mixed Priority
Line 225: Occasionally, one story comprises multiple smaller substories that are of differ-
Line 226: ent priority. Suppose a project includes a typical login story: “As a user, I am re-
Line 227: quired to log into the system.” The product owner expresses her conditions of
Line 228: satisfaction for this story, and they include the following:
Line 229: ◆If the user enters a valid username and password, she is granted access.
Line 230: ◆If the user enters an invalid password three times in a row, she is denied ac-
Line 231: cess until she calls customer service.
Line 232: ◆If the user is denied access, she is sent an email stating that an attempt was
Line 233: made to use her account.
Line 234: This story is too big to fit in one iteration, so it must be split. The story can
Line 235: be split by looking for low-priority elements. In this case the product owner
Line 236: would not ship the product if it did not support the the core login functionality.
Line 237: She might, however, be willing to release the product without a retry time-out
Line 238: mechanism or without sending an email about the access attempt. This leads to
Line 239: another guideline about splitting stories:
Line 240: Don’t Split a Story into Tasks
Line 241: Sometimes, we come across a feature that is difficult to split. In these cases, it is
Line 242: tempting to split the feature into its constituent tasks. For most software devel-
Line 243: opers, considering a feature and decomposing it into its constituent tasks is such
Line 244: a habit that we often do it without even being aware of it. Do not, for example,
Line 245: split a story into the following:
Line 246: ◆Code the user interface.
Line 247: ◆Write the middle tier.
Line 248: Separate a large story into smaller stories if the smaller stories have
Line 249: different priorities.
Line 250: 
Line 251: --- 페이지 159 ---
Line 252: 128 |
Line 253: Chapter 12
Line 254: Splitting User Stories
Line 255: The best way to avoid this temptation is to follow Hunt and Thomas’ advice
Line 256: (1999) to fire a tracer bullet through the system. A tracer bullet travels through
Line 257: all layers of a feature. That may mean delivering a partial user interface, a partial
Line 258: middle tier, and a partial database. Delivering a cohesive subset of all layers of a
Line 259: feature is almost always better than delivering all of one layer. This leads to an-
Line 260: other guideline:
Line 261: Avoid the Temptation of Related Changes
Line 262: Once you’ve split a story and have it at an appropriate size, don’t make things
Line 263: worse by adding work to the story. Often, this comes in the form of the tempta-
Line 264: tion of related changes. We tell ourselves, “While I’m in that code, I might as
Line 265: well take care of these other lingering changes.” It can very possibly be appropri-
Line 266: ate to fix a bug or address an old issue while working on a separate issue in the
Line 267: same part of the code. However, the prioritiy of doing so needs to be considered
Line 268: in the same manner in which priorities were considered for other features. In
Line 269: other words, which is higher priority: spending half a day fixing a year-old bug or
Line 270: spending the same amount of time on something else? The answer is clearly en-
Line 271: tirely contextual and becomes this chapter’s final guideline:
Line 272: Combining Stories
Line 273: With all of this advice about splitting stories, it may be tempting to think that ev-
Line 274: ery user story about to be worked on should be made as small as possible. That’s
Line 275: not the case. For teams working in two-week iterations, splitting features such
Line 276: that each can be done in two to five days or so is appropriate. (Stories may still be
Line 277: estimated in story points, but by the time a team needs to split stories they will
Line 278: know approximately how many story points or ideal days equate to around two
Line 279: to five days.) Stories will need to be a little smaller for one-week iterations and
Line 280: Don’t split a large story into tasks. Instead, try to find a way to fire
Line 281: a tracer bullet through the story.
Line 282: Avoid making things worse by adding related changes to an appro-
Line 283: priately sized feature unless the related changes are of equivalent
Line 284: priority.
Line 285: 
Line 286: --- 페이지 160 ---
Line 287: Discussion Questions 
Line 288: |
Line 289: 129
Line 290: can, but don’t need to, be a little larger for longer iterations. Stories of these ap-
Line 291: proximate sizes flow best through the short iterations of an agile project.
Line 292: Just as we may need to split large stories, we may need to combine multiple
Line 293: tiny stories. The combined stories are estimated as a whole rather than individu-
Line 294: ally. When possible, try to combine related stories as that will make it easier to
Line 295: prioritize them. It is very common to combine multiple bug reports and treat
Line 296: them as one item.
Line 297: Summary
Line 298: It can be useful to split a story that does not fit in an iteration, either because it’s
Line 299: too large for any iteration or it’s too big to fit in the time remaining in an itera-
Line 300: tion being planned. It is also useful to split a large story if you need to provide a
Line 301: more accurate estimate than can be made of the one large story.
Line 302: A story may be split by the type of data it will support. A story may also be
Line 303: split based on the operations inherent in the story. Splitting stories across the
Line 304: common CRUD operations (Create, Read, Update, Delete) is common. A story
Line 305: may be made smaller by segmenting out any cross-cutting concerns, such as se-
Line 306: cuity, logging, error handling, and so on. A story may also be made smaller by ig-
Line 307: noring performance targets during the iteration in which the story is made
Line 308: functional. The performance target can be made its own story and satisfied in a
Line 309: later iteration. Many stories describe two or more needs. If these needs are of dif-
Line 310: ferent priority, split the stories that way. 
Line 311: Avoid splitting a story into the development tasks that will be necessary to
Line 312: implement the feature. Splitting work into its necessary tasks is such a habit for
Line 313: us that it is easy for us to begin splitting user stories that way. Avoid the tempta-
Line 314: tion of making a large story any larger by including related changes that are not
Line 315: necessary for the delivery of the user story.
Line 316: Finally, remember that sometimes it is appropriate to combine user stories,
Line 317: especially in the case of bug fixes, which may be too small on their own.
Line 318: Discussion Questions
Line 319: 1. What are some user stories on a current or recent project that you found dif-
Line 320: ficult to split? How might you split them now?
Line 321: 2. What problems do you think are caused by splitting a story into tasks and
Line 322: then treating the tasks as user stories?
Line 323: 
Line 324: --- 페이지 161 ---
Line 325: This page intentionally left blank 
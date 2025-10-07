Line 1: 
Line 2: --- 페이지 70 ---
Line 3: Chapter 6 
Line 4: The User Story Technique 
Line 5: “It is better to take many small steps in the right direction than to make a 
Line 6: great leap forward only to stumble backward.”
Line 7: Chinese Proverb 
Line 8: The triad (Cathy, Debbie, and Tom) meets to develop stories from a feature. 
Line 9: Debbie explains roles in stories, their attributes, and their personas. She intro-
Line 10: duces a story card template. Tom shows how acceptance criteria can determine 
Line 11: story size. The Independent, Negotiable, Valuable, Estimable, Small, and Test-
Line 12: able (INVEST) criteria for stories is listed. 
Line 13: Stories
Line 14: The features need to be broken down into smaller pieces, the next step shown in 
Line 15: Figure 6.1. It is easier to devise speciﬁc acceptance tests for smaller pieces than 
Line 16: for an entire feature. The focus of each story is narrower than the feature. One 
Line 17: or two features are broken down into stories—just enough to ﬁll the team’s time 
Line 18: until the next feature decomposition session. 
Line 19: Charter 
Line 20: Scenario 
Line 21: Test
Line 22: Story
Line 23: Feature
Line 24: Focus
Line 25: Figure 6.1 After High-Level Requirement, Create Stories 
Line 26: 47
Line 27: 
Line 28: --- 페이지 71 ---
Line 29: Chapter 6 The User Story Technique
Line 30: 48
Line 31: The team gets together again, this time without Sam. As the sponsor, he has 
Line 32: agreed to and is happy with the features that are going to be implemented. He 
Line 33: will come back as they are developed to see how things are going. Cathy will 
Line 34: lead the effort to develop the stories, getting suggestions from the users (Cary, 
Line 35: Mary, and Harry) along the way. Cathy has the necessary business and domain 
Line 36: knowledge to create the stories. Debbie and Tom can work with Cathy to help 
Line 37: her create the stories and to get a ﬁrsthand understanding of what the stories 
Line 38: are all about. 
Line 39: The team is going to break down the ﬁrst few features into stories. A  require-
Line 40: ment story is a small portion of a feature. Many of the requirement stories are 
Line 41: called user stories because they involve something that a user wants to do with 
Line 42: the system. Sometime a requirement story is just a constraint on the system, such 
Line 43: as using open-source software to avoid license fees or writing the program in 
Line 44: Java because that’s the corporate standard. This type of story is often called a 
Line 45: constraint story. The acceptance criteria for a constraint story are usually speci-
Line 46: ﬁed by the constraint. 
Line 47: Features into Stories 
Line 48: Debbie starts off, “Let’s break down the features into stories. The features we 
Line 49: are going to start with are” 
Line 50: •  Check out and check in CDs. 
Line 51: •  Enable credit card charging to eliminate cash. 
Line 52: “Tom and I use a story format that comes from Extreme Programming
Line 53: [Cohn02]. The form is” 
Line 54: As a < role>, I want to < do something> so that < reason>.
Line 55: “The <role> represents the user, the  <do something> is what the user is try-
Line 56: ing to accomplish, and the <reason> is why the user is doing it. The  <role> and 
Line 57: <do something> are the critical parts. The  <reason> is often helpful, but it’s not 
Line 58: required. An example of this form is” 
Line 59: As the clerk, I want to check out a CD for a customer so that I can keep 
Line 60: track of who has rented it. 
Line 61: 
Line 62: --- 페이지 72 ---
Line 63: Stories 
Line 64: 49
Line 65: Roles
Line 66: Debbie continues, “Before we start on the user stories, we need to come up 
Line 67: with some roles that are going to be involved in the stories. These roles are not 
Line 68: necessarily speciﬁc people, but the ‘hats’ that people wear in the rental process 
Line 69: and are important to uncover. When we gather the details for a story, we want 
Line 70: to ensure that someone who plays that role is available for collaboration. When 
Line 71: we do usability testing or exploratory testing, we take on a role to see how the 
Line 72: system functions from that perspective.” 
Line 73: “We use the same method that we did in coming up with features. Everybody 
Line 74: brainstorms by themselves and writes down potential roles. We then put the 
Line 75: cards on the table, match them up, and group them.” 
Line 76: After thinking, writing, and grouping, Cathy, with the help of the rest of 
Line 77: the team, came up with the following roles. Each role is clariﬁed by listing its 
Line 78: responsibilities.
Line 79:   1 . There are other roles to consider, such as system administration, operations, and 
Line 80: help desk. 
Line 81: Roles
Line 82: Clerk—Checks out CD and checks them in 
Line 83: Inventory maintainer—Keeps track of overall CD inventory 
Line 84: Finance manager—Manages all monetary transactions, such as rental pay-
Line 85: ments and late rental fees 
Line 86: Renter—Pays for CDs with cash or, in the future, with a credit card 
Line 87: Tom notes, “Cathy plays two of these roles: inventory maintainer and ﬁnance 
Line 88: manager. The roles are separate because they have different interests and points 
Line 89: of view, even though they are played by one person.” 1
Line 90: Role Attributes 
Line 91: Debbie continues, “Now that we have the roles, it’s useful to come up with at-
Line 92: tributes for them. These attributes give a better idea of how to design the system 
Line 93: and how to test it for usability. For each role, you determine” 
Line 94: •  Frequency of use— This is how often someone uses the system. 
Line 95: •  Domain expertise— This is in the area that the system is designed for. 
Line 96: 
Line 97: --- 페이지 73 ---
Line 98: Chapter 6 The User Story Technique
Line 99: 50
Line 100: •  Computer expertise— This is experience and comfort in using a computer. 
Line 101: •  General goals— These are goals you desire, such as convenience and speed. 
Line 102: “Let’s take the role of clerk. Is there anyone else other than Cary who works 
Line 103: as a clerk? What are their backgrounds?,” Debbie asks. 
Line 104: Cathy replies, “Harry and Mary. Cary works there every day and is a com-
Line 105: puter whiz. His dad Harry is a retired English professor who ﬁlls in every now 
Line 106: and then. He gets all his information from the books in the stacks at the library 
Line 107: rather than from the Internet. Mary still works as a French professor. Her com-
Line 108: puter skills are probably more in line with Harry’s than with Cary’s.” 
Line 109: Debbie goes on, “To avoid giving them names loaded with connotations, let’s 
Line 110: call the two types full-time and part-time clerks.” 
Line 111: Cathy replies, “Based on what I know about the three of them, I think the 
Line 112: attributes look like this.” 
Line 113: Role Attributes 
Line 114: Full-Time Clerk 
Line 115: • Frequency of use— Every day 
Line 116: • Domain expertise— Excellent
Line 117: • Computer expertise— Excellent
Line 118: • General goals— Speed (as few keystrokes as possible) 
Line 119: Part-Time Clerk 
Line 120: • Frequency of use— One day a week 
Line 121: • Domain expertise— Understands the general area 
Line 122: • Computer expertise— Low
Line 123: • General goals— Lots of helpful reminders 
Line 124: Persona
Line 125: Debbie continues, “We could create a persona for each of these sets of attributes. 
Line 126: A persona is an imaginary person described with lots of details [Cooper01]. It 
Line 127: helps me and Tom to envision an actual user, rather than just a dull set of at-
Line 128: tributes. It puts a human face on the user. Let’s do one for the part-time clerk. 
Line 129: We’ll use a different name for the persona to keep it less related to a particular 
Line 130: part-time clerk.” 
Line 131: 
Line 132: --- 페이지 74 ---
Line 133: Stories 
Line 134: 51
Line 135: Here’s what the triad came up with: 
Line 136: Persona
Line 137: Larry listens to classical music on CDs all the time. He comes in one day a 
Line 138: week to help check in and check out CDs. He prides himself in doing that 
Line 139: without making mistakes. He’s not up to date with all current technology. 
Line 140: He’s not graphically oriented, so icons don’t have much meaning for him. 
Line 141: He wonders if the new system is going to be too complicated and whether 
Line 142: he’ll be able to use it without problems. 
Line 143: Debbie comments, “This persona gives me a good picture to keep in mind 
Line 144: for which I’ll be developing the user interface. Now let’s start on the stories 
Line 145: themselves.”
Line 146: Stories for Roles 
Line 147: Over the next few hours, Cathy takes the lead in developing the stories from the 
Line 148: features. She winds up with the following on the whiteboard: 2
Line 149: Stories
Line 150: • As the clerk, I want to check out a CD for a customer. 
Line 151: • As the clerk, I want to check in a CD for a customer. 
Line 152: • As the inventory maintainer, I want to know where every CD is—in 
Line 153: the store or rented. 
Line 154: • As the ﬁnance manager, I want to know how many CDs are turned 
Line 155: in late and what late charges apply. 
Line 156: • As the ﬁnance manager, I want to submit a credit card charge every 
Line 157: time a CD is rented so that the store does not have to handle cash. 
Line 158: • As the ﬁnance manager, I want to know how much is being charged 
Line 159: every day so that I can check the charges against bank deposits. 
Line 160: 2. Some teams create stories for malicious roles. For example, “As a cheapskate renter, 
Line 161: I want to check out a CD without paying for it.” The system needs to prevent this 
Line 162: story from occurring. 
Line 163: 
Line 164: --- 페이지 75 ---
Line 165: Chapter 6 The User Story Technique
Line 166: 52
Line 167: Story Acceptance Criteria 
Line 168: “As we create each story, we need to list its acceptance criteria. 3 The criteria will 
Line 169: be expanded into speciﬁc acceptance tests just before the story is developed.” 
Line 170: The team comes up with the following tests. The titles are a short reference to 
Line 171: the stories listed previously. 
Line 172:   3 . There is a risk that each story is individually correct, but together, they do not fully 
Line 173: deliver the feature. Once the acceptance criteria for individual stories are created, the 
Line 174: acceptance criteria for the feature may be updated. Those criteria can then be turned 
Line 175: into speciﬁc acceptance tests. These tests may be harder to specify, but there will be 
Line 176: fewer of them. 
Line 177: Story Acceptance Criteria 
Line 178: Check Out CD 
Line 179: •  Check out a CD. Check to see that it is recorded as rented. 
Line 180: Check In CD 
Line 181: •  Check in a CD. Check to see that it is recorded as returned. 
Line 182: •  Check in a CD that is late. Check to see that it is noted as late. 
Line 183: Report Inventory 
Line 184: •  Check out a few CDs. See if the report shows them as rented. 
Line 185: •  Check in a few CDs. See if the report shows them as in the store. 
Line 186: Charge Rental 
Line 187: • Check in a CD. See if the rental charge is correct. See if the credit 
Line 188: charge matches the rental charge. See if the charge is made to the 
Line 189: credit card company. Check that the bank account receives money 
Line 190: from the charge. 
Line 191: The team can record these stories using any appropriate technology, from 
Line 192: cards on the wall to entries in a software system. In any case, at this point, the 
Line 193: stories should be short—just a brief description. The details are gathered just 
Line 194: prior to or during the story’s implementation. 
Line 195: 
Line 196: --- 페이지 76 ---
Line 197: Stories 
Line 198: 53
Line 199: Acceptance Tests Determine Size 
Line 200: “That last story, Charge Rental, seems too big from the acceptance criteria,” 
Line 201: Tom suggested. “There are tests associated with the rental and tests associated 
Line 202: with the credit card company. If we recognize that a story is too big at this point, 
Line 203: we should break it down into smaller stories. Smaller stories are easier to devel-
Line 204: op and test. If we discover the number of speciﬁc acceptance tests is large when 
Line 205: we detail the story, we may want to break it into two stories at that point.” 
Line 206: “The Charge Rental story feels like it could be broken into at least two sto-
Line 207: ries. One might be Compute Rental Charge and the other Submit Charge. The 
Line 208: tests underneath each of these stories would be” 
Line 209: Story Estimates 
Line 210: Two estimates are often made for every story. These are the business value 
Line 211: and the effort. The business value represents the relative worth of a story 
Line 212: to the business. The effort estimate (often done in story points) includes all 
Line 213: the work required to deliver the story, including implementing the code, 
Line 214: testing it, and any other work involved. One way to estimate business 
Line 215: value and effort is shown in Appendix B, “Estimating Business Value.” 
Line 216: Tracking the cumulative business value of delivered stories gives an idea 
Line 217: of the project’s progress. This keeps the entire team focused on delivering 
Line 218: business value. 
Line 219: If a team uses iteration scheduling, the effort estimate can determine 
Line 220: whether a story can ﬁt into an iteration. If the team uses a work queue, 
Line 221: the estimate indicates whether the items in the work queue are roughly the 
Line 222: same size. 
Line 223: A rough return on investment can be calculated by dividing the business 
Line 224: value by the effort. This can help the customer unit determine whether or 
Line 225: when a particular story should be included in the project. 
Line 226: Compute Rental Charge 
Line 227: •  Check in the CD. See if the rental charge is correct. See if the credit 
Line 228: charge matches the rental charge. 
Line 229: Submit Charge 
Line 230: •  Submit the charge to the credit card company. Check that the bank 
Line 231: account receives money from the charge. 
Line 232: 
Line 233: --- 페이지 77 ---
Line 234: Chapter 6 The User Story Technique
Line 235: 54
Line 236: Tom continued, “In this case, Cathy, you may come up with acceptance tests 
Line 237: for both of these stories because they are both business related. These two sto-
Line 238: ries are related to Charge Rental. If you were estimating the business value [see 
Line 239: Appendix B], these two stories may not have value because you can only submit 
Line 240: a charge when both are complete. Charge Rental has a business value, and we 
Line 241: get business value credit for it when it is complete.” 4
Line 242: “When we get to the details, Debbie and I may ﬁnd we need to break up 
Line 243: stories into smaller ones that are technical. These stories are called developer
Line 244: stories. Debbie and I sometimes create them to cut down the size of the stories. 
Line 245: Also, if we had multiple teams, we could break up one story into several stories 
Line 246: that each team could work on in order to spread the work. It is the responsibil-
Line 247: ity of the developer unit to create acceptance tests for developer stories” [see 
Line 248: Chapter 16, “Developer Acceptance Tests”]. 
Line 249: “Anytime stories are broken up, it’s good to have the triad participate. Ques-
Line 250: tions may arise in the breakup process that can yield answers which may lead to 
Line 251: more understanding on everyone’s part.” 
Line 252: Customer Terms 
Line 253: Debbie announces, “Now we need to agree on common terminology. It seems 
Line 254: that we are using the term charge in several ways. For example,  charge can refer 
Line 255: to both what you charge for a rental and a charge made on a credit card. This 
Line 256: language duplication can be confusing later on. Cathy, we need to state the 
Line 257: terms in business language, not computer language. So we can all agree on the 
Line 258: terms, let’s write a glossary. You’re the lead on this, Cathy” [Evans01]. 
Line 259: Cathy replies, “For what we’ve been talking about so far, here are the terms 
Line 260: that Sam and I use.” 
Line 261: 4. Some teams credit business value to these smaller stories. It is either a separate esti-
Line 262: mate or a breakdown of the business value of the higher-level story. 
Line 263: Rental Fee—Amount due for a rental at check out 
Line 264: Late Fee—Amount due if the rental is late when it’s checked in 
Line 265: Card Charge—Amount charged to a customer’s credit card for any reason 
Line 266: “Now that we have the terms, we should use them consistently. So let’s 
Line 267: re-write the stories to use these words,” Debbie said. “We’ll take these two 
Line 268: stories as an example.” 
Line 269: 
Line 270: --- 페이지 78 ---
Line 271: INVEST Criteria 
Line 272: 55
Line 273: INVEST Criteria 
Line 274: The INVEST criteria for requirement stories was developed by Bill Wake 
Line 275: [Wake02]. Stories should be compared to the criteria of independent, negoti-
Line 276: able, valuable, estimable, small, and testable. 
Line 277: Independent means that each story can be completed by itself, without 
Line 278: dependencies on other stories. Often a sequence of stories exists, such as the 
Line 279: check-out and check-in stories. Some people term this sequence a saga. Although 
Line 280: there is a relationship between the stories, check-out can be completed by itself, 
Line 281: and later the check-in story can be done. But it could be harder to do the stories 
Line 282: in reverse (check-in ﬁrst and then check-out.) 
Line 283: Negotiable means that the triad has not made a hard and fast determination 
Line 284: of exactly what is in the story. They will collaborate on that when they start 
Line 285: working on the story. 
Line 286: Valuable means that the story has a business value to the customer. That’s 
Line 287: one reason the customer should put a business value on each story [see Appen-
Line 288: dix B]. If a story cannot be ascribed a business value, perhaps it should not be 
Line 289: done. Any developer story that is created should relate to some story to which 
Line 290: there is an assigned business value. 
Line 291: Estimable implies that the developer and tester can come up with some sort 
Line 292: of rough estimate as to how long it will take to complete the story. If they lacked 
Line 293: knowledge about the business domain or were implementing the story in some 
Line 294: completely new technology, they might not be able to give an estimate. If the 
Line 295: customer needed a rough estimate to justify spending money on the story, the 
Line 296: developer would spend some time investigating the domain or the technology. 
Line 297: Small stories can be completed in a single iteration or in a reasonable cycle 
Line 298: time. If a story cannot be completed in a single iteration, it’s hard to track 
Line 299: progress, and chances are it is too big a story to comprehend easily. Preferably, 
Line 300: big stories (which some people call epics) are broken into smaller stories, each 
Line 301: of which the customer can understand. Otherwise, the triad may need to break 
Line 302: down the stories into developer stories to facilitate coding. For example, Charge 
Line 303: Compute Rental Fee 
Line 304: Check in the CD. See if the rental fee is correct. Verify that the card 
Line 305: charge matches the rental fee. 
Line 306: Process Card Charge 
Line 307: See if the card charge is made to the credit card company. Check that 
Line 308: the bank account receives money from the card charge. 
Line 309: 
Line 310: --- 페이지 79 ---
Line 311: Chapter 6 The User Story Technique
Line 312: 56
Line 313: Rental was broken into Compute Rental Fee and Process Card Charge to make 
Line 314: stories meet this criterion. 
Line 315: Testable means that the user can conﬁrm that the story is done. Having 
Line 316: acceptance tests makes a story testable, and passing those tests shows that the 
Line 317: system meets the customer needs. As will be shown later, having acceptance tests 
Line 318: that can be automated ensures that previous stories are not broken when new 
Line 319: stories are implemented. 
Line 320: There may be other reasons to break a story into multiple stories, even if it 
Line 321: meets these criteria. For example, not all the details of a story may need to be 
Line 322: completed to deliver business value. So the details not currently required might 
Line 323: be incorporated into a new story to be delivered later. Any member of the triad 
Line 324: might think that some aspects of a story are riskier than normal. So the member 
Line 325: might create a story to investigate those aspects early on in a project. 
Line 326: The triad spends a few minutes reviewing each story against the INVEST 
Line 327: criteria. Then Debbie ﬁnishes, “I think we’re ready to develop more details and 
Line 328: speciﬁc acceptance tests for the ﬁrst story.” 
Line 329: Summary
Line 330: • Requirement stories can be user stories or constraint stories. 
Line 331: • Every user story has a role and an action and usually a reason. 
Line 332: • Roles are the parts people play in a process, not individuals 
Line 333: • Stories should be written in the customer’s language 
Line 334: • Stories should meet the INVEST criteria—independent, negotiable, valu-
Line 335: able, estimable, small, and testable 
Line 336: • Each story should have acceptance criteria 
Line 337: • Acceptance criteria can help determine the size of stories. 